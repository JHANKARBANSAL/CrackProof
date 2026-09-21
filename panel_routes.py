"""Owner-scoped panel endpoints. Answers are saved before the next AI call."""
import hashlib
import os
import re
import tempfile

from flask import jsonify, request

import database
import panel_session
from transcriber import transcribe_audio


def register_panel_routes(app, owner_key, fail):
    def load(panel_id):
        if not re.fullmatch(r"[a-f0-9]{32}", panel_id):
            return None
        return database.load_panel(panel_id, owner_key())

    def commit(state, revision):
        if database.save_panel(state, owner_key(), revision):
            return jsonify(ok=True, session=state)
        fresh = load(state["id"])
        return jsonify(ok=False, message="This interview changed in another request. The latest saved turn is shown.",
                       session=fresh[0] if fresh else None), 409

    @app.get("/api/panels")
    def panels():
        owner = owner_key()
        return jsonify(ok=True, profile=database.load_profile(owner), sessions=database.list_panels(owner),
                       personas=panel_session.PERSONAS, total_turns=panel_session.TOTAL_TURNS)

    @app.post("/api/panels/start")
    def start_panel():
        data = request.get_json(silent=True) or {}
        token = data.get("request_id")
        if not isinstance(token, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{16,80}", token):
            return fail("Please retry starting the panel with a valid request ID.")
        owner = owner_key()
        # Retrying a timed-out start returns the same session, scoped to this owner.
        panel_id = hashlib.sha256((owner + ":" + token).encode()).hexdigest()[:32]
        saved = load(panel_id)
        if saved:
            return jsonify(ok=True, session=saved[0])
        profile = database.load_profile(owner)
        if not profile:
            return fail("Save your target role and skills in My Profile first.", 400)
        state = panel_session.new_session(panel_id, profile)
        database.save_panel(state, owner)
        return jsonify(ok=True, session=load(panel_id)[0])

    @app.get("/api/panels/<panel_id>")
    def get_panel(panel_id):
        saved = load(panel_id)
        return jsonify(ok=True, session=saved[0]) if saved else fail("Panel interview not found.", 404)

    @app.post("/api/panels/<panel_id>/advance")
    def advance_panel(panel_id):
        saved = load(panel_id)
        if not saved:
            return fail("Panel interview not found.", 404)
        state, revision = saved
        if state["status"] == "completed" or state["current"]:
            return jsonify(ok=True, session=state)
        if state["status"] == "report_pending":
            report = panel_session.build_report(state)
            if report is None:
                return fail("Feedback is unavailable right now. Your answers are saved; retry feedback.", 502)
            state.update(report=report, status="completed")
        else:
            question = panel_session.next_question(state)
            if question is None:
                return fail("Could not prepare the next question. Your answers are saved; please retry.", 502)
            state["current"] = question
        return commit(state, revision)

    @app.post("/api/panels/<panel_id>/answer")
    def answer_panel(panel_id):
        saved = load(panel_id)
        if not saved:
            return fail("Panel interview not found.", 404)
        state, revision = saved
        data = request.get_json(silent=True) or {}
        number, answer = data.get("question_number"), data.get("answer")
        if type(number) is not int or not isinstance(answer, str) or not 1 <= len(answer.strip()) <= 6000:
            return fail("Send a question number and an answer of 1–6000 characters.")
        if 1 <= number <= len(state["turns"]) and state["turns"][number - 1]["answer"] == answer.strip():
            return jsonify(ok=True, session=state)
        if state["status"] != "active" or not state["current"] or number != state["current"]["number"]:
            return jsonify(ok=False, message="This question is already submitted or no longer active. Review the saved conversation.", session=state), 409
        state["turns"].append({**state["current"], "answer": answer.strip()})
        state["current"] = None
        if len(state["turns"]) == panel_session.TOTAL_TURNS:
            state["status"] = "report_pending"
        return commit(state, revision)

    @app.post("/api/panels/<panel_id>/finish")
    def finish_panel(panel_id):
        saved = load(panel_id)
        if not saved:
            return fail("Panel interview not found.", 404)
        state, revision = saved
        if state["status"] != "active":
            return jsonify(ok=True, session=state)
        if not state["turns"]:
            return fail("Submit at least one answer before requesting feedback.")
        state.update(status="report_pending", current=None)
        return commit(state, revision)

    @app.post("/api/panels/<panel_id>/transcribe")
    def transcribe_panel(panel_id):
        saved = load(panel_id)
        if not saved:
            return fail("Panel interview not found.", 404)
        state = saved[0]
        if state["status"] != "active" or not state["current"] or request.form.get("question_number") != str(state["current"]["number"]):
            return fail("This question is no longer active. Reopen the saved panel.", 409)
        upload = request.files.get("audio")
        extension = (upload.filename or "").rsplit(".", 1)[-1].lower() if upload else ""
        if extension not in {"webm", "mp4", "m4a", "mp3", "ogg", "wav", "flac"}:
            return fail("Please provide a supported audio recording.")
        handle, path = tempfile.mkstemp(suffix="." + extension)
        os.close(handle)
        try:
            upload.save(path)
            if not os.path.getsize(path):
                return fail("The recording was empty. Retry or type your answer.")
            transcript, problem = transcribe_audio(path)
            if problem or not transcript.strip():
                return fail(problem or "No clear speech found. Retry or type your answer.")
            return jsonify(ok=True, transcript=transcript)
        finally:
            os.remove(path)
