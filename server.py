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
import secrets
import tempfile
import traceback

from flask import Flask, jsonify, request, send_from_directory, session

import database
from interview_session import InterviewSession


app = Flask(__name__, static_folder=None)

# Login cookie ko sign karne ke liye. Har baar naya banane se server
# restart hone par log out ho jaate hain, isliye ek baar bana ke
# .secret_key file mein rakh lete hain.
if os.path.exists(".secret_key"):
    app.secret_key = open(".secret_key").read().strip()
else:
    app.secret_key = secrets.token_hex(32)
    with open(".secret_key", "w") as f:
        f.write(app.secret_key)

database.setup()

UI_DIR = "ui"

# interview_id -> InterviewSession
# Abhi memory mein hai. Login aane par ye database mein jayega.
sessions = {}


def get_session(interview_id):
    """Session dhoondo. Na mile to None."""

    return sessions.get(interview_id)


def fail(message, code=400):
    return jsonify({"ok": False, "message": message}), code


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
        data.get("email"), data.get("password")
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

    user = database.check_login(data.get("email"), data.get("password"))

    if user is None:
        # Email galat hai ya password - dono par ek hi jawab, taaki
        # koi ye pata na kar sake ki kaunsa email registered hai.
        return fail("That email and password do not match.", 401)

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

    interview = InterviewSession(topic)

    sessions[interview.interview_id] = interview

    return jsonify(interview.current_question())


@app.post("/api/answer")
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

    # Audio yahan SAVE NAHI hoti.
    #
    # Recording browser ke apne storage (IndexedDB) mein rehti hai.
    # Server ko sirf transcribe karne ke liye chahiye, uske baad nahi.
    # Isse do faayde hain: kisi ki awaaz server par padi nahi rehti,
    # aur koi storage bill bhi nahi banta.
    #
    # Transcript aur evaluation database mein jaate hain - wahi cheez
    # har device par chahiye hoti hai.
    handle, temp_path = tempfile.mkstemp(suffix="." + extension)
    os.close(handle)

    try:
        upload.save(temp_path)
        result = interview.transcribe(temp_path)

        # UI ko asli path nahi dena - woh browser ke storage ka
        # key use karega
        result["audio_path"] = "browser"

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

    interview.retry()

    return jsonify(interview.current_question())


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

    audio_path = data.get("audio_path") or interview.audio_path()

    return jsonify(interview.evaluate(transcript, audio_path))


@app.post("/api/next")
def next_question():
    """Pichhle answer ke gap par agla sawaal."""

    data = request.get_json(silent=True) or {}

    interview = get_session(data.get("interview_id", ""))

    if interview is None:
        return fail("That interview is no longer active.", 404)

    return jsonify(interview.next_question())


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

    if topic and topic != interview.topic:
        return jsonify(interview.change_topic(topic))

    return jsonify(interview.continue_same_topic())


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

    # Logged in ho to ye interview account mein save ho jaye.
    # Guest ka interview save nahi hota - uske liye account chahiye.
    user = current_user()

    if user and result.get("ok"):
        database.save_interview(
            user["id"], interview.interview_id, interview.topic, result
        )

    result["saved"] = bool(user)

    return jsonify(result)


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

    if user is None:
        return jsonify({"ok": True, "interviews": [], "signed_in": False})

    return jsonify({
        "ok": True,
        "signed_in": True,
        "interviews": database.list_interviews(user["id"]),
    })


@app.get("/api/interview/<interview_id>")
def one_interview(interview_id):
    """Ek purana interview poora khol ke dekhne ke liye."""

    user = current_user()

    if user is None:
        return fail("Please sign in to view your interviews.", 401)

    data = database.get_interview(user["id"], interview_id)

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

    return jsonify({
        "ok": False,
        "message": "Something went wrong on the server.",
        "detail": str(error),
    }), 500


if __name__ == "__main__":

    # Host PORT deta hai to wahi use karo, warna 5000
    port = int(os.environ.get("PORT", 5000))

    print("\n  CrackProof")
    print("  http://localhost:" + str(port) + "\n")

    app.run(host="0.0.0.0", port=port, debug=False)
