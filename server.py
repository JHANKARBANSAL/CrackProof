"""
Web server - UI aur Python backend ke beech ka pul.

Chalane ka tareeka:

    python3 server.py

Phir browser mein kholo:  http://localhost:5000

Ye khud koi interview logic nahi rakhta. Sirf HTTP request leke
InterviewSession ko bulata hai aur jawab JSON mein wapas bhejta hai.

Accounts, guest ownership, interview state and reports are persisted
in the configured database so different server workers share state.
"""

import datetime
import json
import os
import re
import secrets
import tempfile
import traceback

from flask import Flask, jsonify, request, send_from_directory, session

import database
import candidate_profile
from panel_routes import register_panel_routes
from pydantic import ValidationError
from interview_session import InterviewSession, RECORDINGS_DIR


app = Flask(__name__, static_folder=None)
app.config.update(MAX_CONTENT_LENGTH=25 * 1024 * 1024,
                  SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

# Login cookie ko sign karne ki chaabi.
#
# Server ke liye ye environment se aati hai. Wahan disk har restart par
# saaf ho jaata hai, to file mein rakhi chaabi har baar nayi banti - aur
# nayi chaabi ka matlab hai saare log out ho gaye.
#
# Laptop par environment mein kuch nahi hota, isliye ek baar bana ke
# .secret_key file mein rakh lete hain. Wahan disk bachta hai.
app.secret_key = os.getenv("SECRET_KEY", "").strip()

if not app.secret_key:

    if os.path.exists(".secret_key"):
        with open(".secret_key") as key_file:
            app.secret_key = key_file.read().strip()
    else:
        app.secret_key = secrets.token_hex(32)
        with open(".secret_key", "w") as f:
            f.write(app.secret_key)

database.setup()

UI_DIR = "ui"


@app.before_request
def validate_json_body():
    if request.path.startswith("/api/") and request.is_json:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return fail("Please send a valid JSON object.")
        for field in ("topic", "email", "password", "name", "interview_id", "transcript"):
            if field in data and data[field] is not None and not isinstance(data[field], str):
                return fail("Invalid value for " + field + ".")

def get_session(interview_id):
    """Only load a persisted interview owned by this account or guest cookie."""
    if not isinstance(interview_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", interview_id):
        return None
    owner = owner_key()
    saved = database.load_session(interview_id, owner)
    if not saved:
        return None
    state, revision = saved
    obj = InterviewSession.restore(state)
    obj._owner_key, obj._revision = owner, revision
    return obj


def owner_key():
    user = current_user()
    if user:
        return "user:" + str(user["id"])
    if "guest_id" not in session:
        session["guest_id"] = secrets.token_hex(24)
    return "guest:" + session["guest_id"]


def session_response(interview, result):
    if result.get("ok"):
        saved = database.save_session(
            interview.interview_id, interview._owner_key, interview.snapshot(),
            interview._revision, report=interview.saved_report())
        if not saved:
            return fail("Another request updated this interview. Please retry your last action.", 409)
    return jsonify(result)


def interview_records():
    """Read only this visitor's history. Caller-supplied guest IDs grant no access."""
    user = current_user()
    if user:
        records = [database.get_interview(user["id"], row["interview_id"])
                   for row in database.list_interviews(user["id"])]
        return [record for record in records if record is not None]
    rows = []
    for state in database.list_guest_sessions(owner_key()):
        interview = InterviewSession.restore(state)
        report = interview.saved_report()
        if report:
            rows.append({"interview_id": interview.interview_id, "topic": interview.topic,
                         "created_at": interview.created_at, "report": report,
                         "questions_answered": len(interview.history),
                         "readiness": report["metrics"]["overall_readiness"]})
    return sorted(rows, key=lambda row: str(row["created_at"]), reverse=True)


def fail(message, code=400):
    return jsonify({"ok": False, "message": message}), code


register_panel_routes(app, owner_key, fail)


@app.route("/api/profile", methods=["GET", "POST"])
def profile():
    owner = owner_key()
    if request.method == "GET":
        return jsonify(ok=True, profile=database.load_profile(owner))
    try:
        confirmed = candidate_profile.CandidateProfile.model_validate(request.get_json(silent=True) or {})
    except ValidationError as error:
        first = error.errors()[0]
        return fail("Please check " + ".".join(map(str, first["loc"])) + ": " + first["msg"])
    database.save_profile(owner, confirmed.model_dump())
    return jsonify(ok=True, profile=confirmed.model_dump())


@app.post("/api/profile/job-description")
def review_job_description():
    try:
        data = candidate_profile.JobDescriptionInput.model_validate(request.get_json(silent=True) or {})
    except ValidationError:
        return fail("Choose a target role and enter a job description of up to 8,000 characters.")
    review = candidate_profile.review_job_description(data.target_role, data.job_description)
    if review is None:
        return fail("The AI review is unavailable. You can retry or continue with your profile.", 502)
    return jsonify(ok=True, review=review.model_dump())


@app.post("/api/resume/parse")
def parse_resume():
    # Initialize ownership before returning so later saves use the same guest cookie.
    owner_key()
    upload = request.files.get("resume")
    if not upload or not (upload.filename or "").lower().endswith(".pdf"):
        return fail("Please select a PDF resume, or enter details manually.")
    try:
        text = candidate_profile.read_resume(upload.read(candidate_profile.MAX_PDF_BYTES + 1))
    except ValueError as error:
        return fail(str(error))
    details = candidate_profile.extract_details(text)
    if details is None:
        return fail("Resume analysis is unavailable. Your setup is unchanged; retry or enter details manually.", 502)
    return jsonify(ok=True, details=details.model_dump())


def current_user():
    """
    Abhi kaun logged in hai. Koi nahi to None.

    Guest bhi None hi hota hai - guest ka interview save nahi hota.
    """

    user_id = session.get("user_id")

    if user_id is None:
        return None

    return database.get_user(user_id)


# ========================================================
# ACCOUNTS
# ========================================================

@app.post("/api/signup")
def signup():
    """Naya account. Body: {"email": "...", "password": "..."}"""

    data = request.get_json(silent=True) or {}

    user_id, error = database.create_user(
        data.get("email"), data.get("password"), data.get("name")
    )

    if error:
        return fail(error)

    session["user_id"] = user_id

    return jsonify({
        "ok": True,
        "user": database.get_user(user_id),
    })


@app.post("/api/login")
def login():
    """Login. Body: {"email": "...", "password": "..."}"""

    data = request.get_json(silent=True) or {}

    user, error = database.check_login(data.get("email"), data.get("password"))

    if error:
        return fail(error, 401)

    session["user_id"] = user["id"]

    return jsonify({"ok": True, "user": user})


@app.post("/api/logout")
def logout():
    session.pop("user_id", None)
    return jsonify({"ok": True})


@app.get("/api/me")
def me():
    """UI shuru mein poochhta hai: koi logged in hai kya?"""

    user = current_user()

    return jsonify({"ok": True, "user": user})


# ========================================================
# UI
# ========================================================

@app.get("/")
def home():
    return send_from_directory(UI_DIR, "index.html")


@app.get("/style.css")
def serve_css():
    return send_from_directory(UI_DIR, "style.css")


@app.get("/app.js")
def serve_js():
    return send_from_directory(UI_DIR, "app.js")


@app.get("/App.jsx")
def serve_jsx():
    return send_from_directory(UI_DIR, "App.jsx", mimetype="text/javascript")


@app.get("/vendor/<path:filename>")
def serve_vendor(filename):
    return send_from_directory(os.path.join(UI_DIR, "vendor"), filename)


@app.get("/Images/<path:filename>")
def serve_images(filename):
    return send_from_directory("Images", filename)


@app.get("/<path:filename>")
def serve_ui_file(filename):
    if filename.startswith("api/"):
        return fail("Not found", 404)
    if os.path.exists(os.path.join(UI_DIR, filename)):
        return send_from_directory(UI_DIR, filename)
    return fail("Not found", 404)


# ========================================================
# INTERVIEW
# ========================================================

@app.post("/api/start")
def start():
    """Naya interview shuru karo. Body: {"topic": "DBMS"}"""

    data = request.get_json(silent=True) or {}

    topic = (data.get("topic") or "").strip()

    topic = _normalize_topic_name(topic)
    if topic not in {"OOP", "Java", "DBMS", "OS", "Computer Networks", "DSA"}:
        return fail("Please choose a topic.")

    interview = InterviewSession(topic)
    interview._owner_key, interview._revision = owner_key(), None
    return session_response(interview, interview.current_question())


@app.post("/api/answer")
@app.post("/api/transcribe")
def answer():
    """
    Recording lo, text banao, aur batao ki bharose ke laayak hai
    ya nahi.

    Form data: interview_id + audio file
    """

    interview_id = request.form.get("interview_id", "")

    interview = get_session(interview_id)

    if interview is None:
        return fail("That interview is no longer active.", 404)

    if "audio" not in request.files:
        return fail("No audio was received.")

    upload = request.files["audio"]

    # Browser aksar webm bhejta hai, kabhi wav
    extension = "webm"

    if upload.filename and "." in upload.filename:
        extension = upload.filename.rsplit(".", 1)[1].lower()
    if extension not in {"webm", "mp4", "m4a", "mp3", "ogg", "wav", "flac"}:
        return fail("Please upload a supported audio recording.")

    # Audio is temporary on the server. Playback remains available in
    # the current browser page; transcripts and evaluations are persisted.
    handle, temp_path = tempfile.mkstemp(suffix="." + extension)
    os.close(handle)

    try:
        upload.save(temp_path)
        if os.path.getsize(temp_path) == 0:
            return fail("The recording is empty. Please record your answer again.")
        result = interview.transcribe(temp_path)

        # UI ko asli path nahi dena - woh browser ke storage ka
        # key use karega
        result["audio_path"] = "browser"

        if not result.get("ok"):
            result["message"] = result.get("problem") or "No clear speech detected. Please speak into your microphone and try again."

        return jsonify(result)

    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass


@app.post("/api/retry")
def retry():
    """Wahi sawaal dobara record karna hai."""

    data = request.get_json(silent=True) or {}

    interview = get_session(data.get("interview_id", ""))

    if interview is None:
        return fail("That interview is no longer active.", 404)

    if interview.finished or interview.question_evaluated:
        return fail("This question has already been completed.")

    interview.retry()

    return session_response(interview, interview.current_question())


@app.post("/api/evaluate")
def evaluate():
    """
    Transcript ko judge karo.

    Body: {"interview_id": "...", "transcript": "...",
           "audio_path": "..."}

    transcript alag se bhej rahe hain kyunki candidate use edit
    kar sakta hai agar Whisper ne galat suna ho.
    """

    data = request.get_json(silent=True) or {}

    interview = get_session(data.get("interview_id", ""))

    if interview is None:
        return fail("That interview is no longer active.", 404)

    transcript = (data.get("transcript") or "").strip()

    if not transcript:
        return fail("There is no answer to evaluate.")
    if len(transcript) > 30000:
        return fail("Please shorten your answer before evaluating it.")
    if data.get("question_number") not in (None, interview.current_question()["question_number"]):
        return fail("This answer belongs to a different question. Please reload the interview.", 409)

    audio_path = "browser"

    eval_result = interview.evaluate(transcript, audio_path)

    return session_response(interview, eval_result)


@app.post("/api/next")
def next_question():
    """Pichhle answer ke gap par agla sawaal."""

    data = request.get_json(silent=True) or {}

    interview = get_session(data.get("interview_id", ""))

    if interview is None:
        return fail("That interview is no longer active.", 404)

    # A delayed double click must not skip a newly generated question.
    if data.get("question_number") not in (None, interview.current_question()["question_number"]):
        return jsonify(interview.current_question())
    return session_response(interview, interview.next_question())


@app.post("/api/continue")
def continue_topic():
    """
    Batch ke baad aage badho.

    Body: {"interview_id": "...", "topic": "OS"}
    topic diya ho to naya topic, warna wahi chalta rahega.
    """

    data = request.get_json(silent=True) or {}

    interview = get_session(data.get("interview_id", ""))

    if interview is None:
        return fail("That interview is no longer active.", 404)

    topic = (data.get("topic") or "").strip()
    topic = _normalize_topic_name(topic)
    if topic and topic not in {"OOP", "Java", "DBMS", "OS", "Computer Networks", "DSA"}:
        return fail("Please choose a supported topic.")

    if topic and topic != interview.topic:
        return session_response(interview, interview.change_topic(topic))

    return session_response(interview, interview.continue_same_topic())


@app.post("/api/report")
def report():
    """
    Is batch ka report.

    Candidate ne beech mein roka ho ya paanchon kiye hon - dono
    mein yahi chalta hai.
    """

    data = request.get_json(silent=True) or {}

    interview = get_session(data.get("interview_id", ""))

    if interview is None:
        return fail("That interview is no longer active.", 404)

    result = interview.report()

    # Accounts and guests both retain owner-scoped state.
    user = current_user()

    result = dict(result, saved=bool(user))
    return session_response(interview, result)


@app.post("/api/feedback")
def feedback():
    """
    Candidate ki raay: evaluation sahi tha ya nahi.

    Guest bhi de sakta hai - user_id None ho jayega. Raay ka fayda
    evaluator sudharne mein hai, isliye use rok nahi rahe.
    """

    data = request.get_json(silent=True) or {}

    interview_id = data.get("interview_id")
    question_number = data.get("question_number")

    if not interview_id or question_number is None:
        return fail("Missing interview or question.")

    user = current_user()

    interview = get_session(interview_id)
    stored = database.get_interview(user["id"], interview_id) if user and not interview else None
    turns = interview.snapshot()["history"] if interview else ((stored or {}).get("report") or {}).get("turns", [])
    if type(question_number) is not int or not any(t.get("question_number") == question_number for t in turns):
        return fail("That completed question was not found.", 404)
    if type(data.get("was_fair")) is not bool:
        return fail("Please select whether the evaluation was fair.")

    database.save_feedback(
        user["id"] if user else None,
        interview_id,
        question_number,
        bool(data.get("was_fair")),
    )

    return jsonify({"ok": True})


# ========================================================
# HISTORY
# ========================================================

@app.get("/api/history")
def history():
    """
    Is user ke purane interviews.

    Logged in na ho to khaali list - kisi ka data bina login ke
    nahi dikhta.
    """

    user = current_user()

    return jsonify({
        "ok": True,
        "signed_in": bool(user),
        "interviews": [{k: v for k, v in row.items() if k != "report"} for row in interview_records()],
    })


@app.get("/api/topics")
def topics_list():
    """
    Saare 6 topics ki list aur candidate ke actual questions answered.
    """
    user = current_user()
    counts = {}
    if user:
        interviews = database.list_interviews(user["id"])
        for row in interviews:
            t = row.get("topic", "")
            counts[t] = counts.get(t, 0) + (row.get("questions_answered") or 0)

    topics = [
        {
            "name": "OOP",
            "display_name": "Object Oriented Programming",
            "icon": "/Images/cube.png",
            "total_questions": 8,
            "questions_answered": counts.get("OOP", 0) + counts.get("Object Oriented Programming", 0)
        },
        {
            "name": "Java",
            "display_name": "Java",
            "icon": "/Images/java.png",
            "total_questions": 8,
            "questions_answered": counts.get("Java", 0)
        },
        {
            "name": "DBMS",
            "display_name": "DBMS",
            "icon": "/Images/database.png",
            "total_questions": 8,
            "questions_answered": counts.get("DBMS", 0) + counts.get("Database Management Systems", 0)
        },
        {
            "name": "OS",
            "display_name": "Operating Systems",
            "icon": "/Images/gear.png",
            "total_questions": 8,
            "questions_answered": counts.get("OS", 0) + counts.get("Operating Systems", 0)
        },
        {
            "name": "Computer Networks",
            "display_name": "Computer Networks",
            "icon": "/Images/network.png",
            "total_questions": 8,
            "questions_answered": counts.get("Computer Networks", 0) + counts.get("CN", 0)
        },
        {
            "name": "DSA",
            "display_name": "Data Structures & Algorithms",
            "icon": "/Images/network.png",
            "total_questions": 8,
            "questions_answered": counts.get("DSA", 0) + counts.get("Data Structures & Algorithms", 0)
        }
    ]

    return jsonify({"ok": True, "topics": topics})


def _normalize_topic_name(t):
    aliases = {"oop": "OOP", "object oriented programming": "OOP", "java": "Java",
               "dbms": "DBMS", "database management systems": "DBMS",
               "os": "OS", "operating systems": "OS", "cn": "Computer Networks",
               "computer networks": "Computer Networks", "dsa": "DSA",
               "data structures & algorithms": "DSA", "data structures and algorithms": "DSA"}
    return aliases.get(str(t or "").strip().lower(), "")


def record_turns(record):
    turns = (record.get("report") or {}).get("turns", [])
    # Legacy account reports sometimes only kept turns on disk. The record has
    # already been owner-checked; never read a path supplied by a guest.
    iv_id = record["interview_id"]
    if not turns and current_user() and re.fullmatch(r"[A-Za-z0-9_-]{1,64}", iv_id):
        path = os.path.join(RECORDINGS_DIR, "interview_" + iv_id, "interview_history.json")
        try:
            with open(path) as file:
                turns = json.load(file)
        except (OSError, ValueError):
            pass
    return turns


@app.get("/api/history/topics")
def history_topics():
    """
    Returns list of 6 topics with real-time attempt counts for the CURRENT user.
    """
    topics_meta = [
        {"name": "OOP", "display_name": "Object Oriented Programming", "icon": "/Images/cube.png", "subtitle": "View your past questions and answers", "attempts": 0},
        {"name": "Java", "display_name": "Java", "icon": "/Images/java.png", "subtitle": "View your past questions and answers", "attempts": 0},
        {"name": "DBMS", "display_name": "DBMS", "icon": "/Images/database.png", "subtitle": "View your past questions and answers", "attempts": 0},
        {"name": "OS", "display_name": "Operating Systems", "icon": "/Images/gear.png", "subtitle": "View your past questions and answers", "attempts": 0},
        {"name": "Computer Networks", "display_name": "Computer Networks", "icon": "/Images/network.png", "subtitle": "View your past questions and answers", "attempts": 0},
        {"name": "DSA", "display_name": "Data Structures & Algorithms", "icon": "/Images/network.png", "subtitle": "View your past questions and answers", "attempts": 0}
    ]
    attempts_by_topic = {t["name"]: 0 for t in topics_meta}

    for record in interview_records():
        turns = record_turns(record)
        if turns:
            for turn in turns:
                norm = _normalize_topic_name(turn.get("topic"))
                if norm in attempts_by_topic:
                    attempts_by_topic[norm] += 1
        else:
            norm = _normalize_topic_name(record.get("topic"))
            if norm in attempts_by_topic:
                attempts_by_topic[norm] += record.get("questions_answered") or 0

    for t in topics_meta:
        t["attempts"] = attempts_by_topic[t["name"]]

    return jsonify({"ok": True, "topics": topics_meta})


@app.get("/api/history/subject/<topic>")
def history_subject(topic):
    """
    Returns real-time questions practiced for the requested subject by the CURRENT user.
    """
    norm_req = _normalize_topic_name(topic)
    questions = []
    for record in interview_records():
        iv_id = record["interview_id"]
        turns = record_turns(record)
        formatted_time = str(record.get("created_at") or "")

        for idx, turn in enumerate(turns):
            turn_topic = _normalize_topic_name(turn.get("topic"))
            if turn_topic == norm_req:
                ev = turn.get("evaluation") or {}
                c_score = ev.get("correctness_score", 0)
                raw_v = ev.get("verdict", "")
                verdict = {"CORRECT": "CORRECT", "PARTIALLY_CORRECT": "PARTIAL"}.get(raw_v, "NEEDS_WORK")

                turn_time = turn.get("timestamp") or formatted_time
                questions.append({
                    "id": f"{iv_id}_{turn.get('question_number', idx+1)}",
                    "interview_id": iv_id,
                    "question_number": turn.get("question_number", idx + 1),
                    "topic": norm_req,
                    "question": turn.get("question", "Interview Question"),
                    "transcript": turn.get("transcript", ""),
                    "timestamp": turn_time,
                    "raw_time": str(turn_time),
                    "score": c_score,
                    "score_display": f"{c_score}/10",
                    "verdict": verdict,
                    "evaluation": {
                        "verdict": raw_v,
                        "correctness_score": c_score,
                        "depth_score": ev.get("depth_score", 0),
                        "correct_points": ev.get("correct_points") or [],
                        "missing_core_concepts": ev.get("missing_core_concepts") or [],
                        "misconceptions": ev.get("misconceptions") or [],
                        "evidence": ev.get("evidence") or [],
                        "reasoning": ev.get("reasoning") or "",
                        "citations": ev.get("citations") or [],
                        "reference_sources": turn.get("reference_sources") or [],
                        "sources": turn.get("reference_sources") or []
                    }
                })

    # Sort newest questions first
    questions.sort(key=lambda x: x.get("raw_time", ""), reverse=True)

    return jsonify({
        "ok": True,
        "subject": norm_req,
        "questions": questions
    })


@app.get("/api/interview/<interview_id>")
def one_interview(interview_id):
    """Ek purana interview poora khol ke dekhne ke liye."""

    user = current_user()

    data = database.get_interview(user["id"], interview_id) if user else None
    if not user:
        interview = get_session(interview_id)
        if interview and interview.history:
            data = {"interview_id": interview_id, "topic": interview.topic,
                    "report": interview.saved_report()}

    if data is None:
        return fail("That interview was not found.", 404)

    return jsonify({"ok": True, "interview": data})


@app.post("/api/interview/<interview_id>/delete")
def remove_interview(interview_id):
    """
    Interview mitao - recordings samet.

    Voice recordings personal data hain, isliye list se hatana kaafi
    nahi, file bhi mitni chahiye.
    """

    user = current_user()

    if user is None:
        return fail("Please sign in first.", 401)

    if not database.delete_interview(user["id"], interview_id):
        return fail("That interview was not found.", 404)

    return jsonify({"ok": True})


@app.post("/api/account/delete")
def remove_account():
    """Account aur uska saara data mitao."""

    user = current_user()

    if user is None:
        return fail("Please sign in first.", 401)

    database.delete_account(user["id"])
    session.pop("user_id", None)

    return jsonify({"ok": True})


# ========================================================
# ERRORS
# ========================================================

@app.errorhandler(Exception)
def any_error(error):
    """
    Koi bhi anhandled error aaye to saaf JSON bhejo, HTML page nahi.
    Browser ko JSON hi samajh aata hai.
    """

    traceback.print_exc()

    code = 500
    if hasattr(error, "code") and isinstance(error.code, int):
        code = error.code

    return jsonify({
        "ok": False,
        "message": "Something went wrong on the server." if code == 500 else str(error),
    }), code


if __name__ == "__main__":

    # Host PORT deta hai to wahi use karo, warna 5000
    port = int(os.environ.get("PORT", 5000))

    print("\n  CrackProof")
    print("  http://localhost:" + str(port) + "\n")

    app.run(host="0.0.0.0", port=port, debug=False)
