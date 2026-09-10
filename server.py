"""
Web server - UI aur Python backend ke beech ka pul.

Chalane ka tareeka:

    python3 server.py

Phir browser mein kholo:  http://localhost:5000

Ye khud koi interview logic nahi rakhta. Sirf HTTP request leke
InterviewSession ko bulata hai aur jawab JSON mein wapas bhejta hai.

Abhi login nahi hai. Sessions memory mein rehte hain, matlab server
band hone par khali ho jaate hain - par har answer disk par
interview_history.json mein save hota rehta hai, to kaam nahi jaata.
"""

import os
import traceback

from flask import Flask, jsonify, request, send_from_directory

from interview_session import InterviewSession


app = Flask(__name__, static_folder=None)

UI_DIR = "ui"

# interview_id -> InterviewSession
# Abhi memory mein hai. Login aane par ye database mein jayega.
sessions = {}


def get_session(interview_id):
    """Session dhoondo. Na mile to None."""

    return sessions.get(interview_id)


def fail(message, code=400):
    return jsonify({"ok": False, "message": message}), code


# ========================================================
# UI
# ========================================================

@app.get("/")
def home():
    return send_from_directory(UI_DIR, "index.html")


# ========================================================
# INTERVIEW
# ========================================================

@app.post("/api/start")
def start():
    """Naya interview shuru karo. Body: {"topic": "DBMS"}"""

    data = request.get_json(silent=True) or {}

    topic = (data.get("topic") or "").strip()

    if not topic:
        return fail("Please choose a topic.")

    session = InterviewSession(topic)

    sessions[session.interview_id] = session

    return jsonify(session.current_question())


@app.post("/api/answer")
def answer():
    """
    Recording lo, text banao, aur batao ki bharose ke laayak hai
    ya nahi.

    Form data: interview_id + audio file
    """

    interview_id = request.form.get("interview_id", "")

    session = get_session(interview_id)

    if session is None:
        return fail("That interview is no longer active.", 404)

    if "audio" not in request.files:
        return fail("No audio was received.")

    upload = request.files["audio"]

    # Browser aksar webm bhejta hai, kabhi wav
    extension = "webm"

    if upload.filename and "." in upload.filename:
        extension = upload.filename.rsplit(".", 1)[1].lower()

    path = session.audio_path(extension)

    upload.save(path)

    return jsonify(session.transcribe(path))


@app.post("/api/retry")
def retry():
    """Wahi sawaal dobara record karna hai."""

    data = request.get_json(silent=True) or {}

    session = get_session(data.get("interview_id", ""))

    if session is None:
        return fail("That interview is no longer active.", 404)

    session.retry()

    return jsonify(session.current_question())


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

    session = get_session(data.get("interview_id", ""))

    if session is None:
        return fail("That interview is no longer active.", 404)

    transcript = (data.get("transcript") or "").strip()

    if not transcript:
        return fail("There is no answer to evaluate.")

    audio_path = data.get("audio_path") or session.audio_path()

    return jsonify(session.evaluate(transcript, audio_path))


@app.post("/api/next")
def next_question():
    """Pichhle answer ke gap par agla sawaal."""

    data = request.get_json(silent=True) or {}

    session = get_session(data.get("interview_id", ""))

    if session is None:
        return fail("That interview is no longer active.", 404)

    return jsonify(session.next_question())


@app.post("/api/continue")
def continue_topic():
    """
    Batch ke baad aage badho.

    Body: {"interview_id": "...", "topic": "OS"}
    topic diya ho to naya topic, warna wahi chalta rahega.
    """

    data = request.get_json(silent=True) or {}

    session = get_session(data.get("interview_id", ""))

    if session is None:
        return fail("That interview is no longer active.", 404)

    topic = (data.get("topic") or "").strip()

    if topic and topic != session.topic:
        return jsonify(session.change_topic(topic))

    return jsonify(session.continue_same_topic())


@app.post("/api/report")
def report():
    """
    Is batch ka report.

    Candidate ne beech mein roka ho ya paanchon kiye hon - dono
    mein yahi chalta hai.
    """

    data = request.get_json(silent=True) or {}

    session = get_session(data.get("interview_id", ""))

    if session is None:
        return fail("That interview is no longer active.", 404)

    return jsonify(session.report())


# ========================================================
# HISTORY
# ========================================================

@app.get("/api/history")
def history():
    """
    Purane interviews ki list, disk se padhkar.

    Abhi login nahi hai isliye saare interviews dikhte hain. Login
    aane par ye user ke hisaab se filter hoga.
    """

    import json

    folder = "recordings"

    rows = []

    if not os.path.isdir(folder):
        return jsonify({"ok": True, "interviews": []})

    for name in sorted(os.listdir(folder), reverse=True):

        path = os.path.join(folder, name, "interview_history.json")

        if not os.path.exists(path):
            continue

        try:
            with open(path) as f:
                turns = json.load(f)
        except Exception:
            continue

        if not turns:
            continue

        rows.append({
            "interview_id": turns[0].get("interview_id", name),
            "topic": turns[0].get("topic", ""),
            "questions_answered": len(turns),
            "folder": name,
        })

    return jsonify({"ok": True, "interviews": rows})


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

    return jsonify({
        "ok": False,
        "message": "Something went wrong on the server.",
        "detail": str(error),
    }), 500


if __name__ == "__main__":

    print("\n  CrackProof")
    print("  http://localhost:5000\n")

    app.run(port=5000, debug=False)
