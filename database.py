"""
User accounts aur unke interviews.

Do jagah chal sakta hai, aur khud pata laga leta hai kaunsi:

    .env mein DATABASE_URL hai   ->  Supabase (Postgres)
    nahi hai                     ->  crackproof.db (SQLite)

Isliye laptop par bina kisi setup ke chalta rehta hai, aur server par
Supabase use karta hai - jahan data restart ke baad bhi bacha rehta
hai. Free hosting ka disk har restart par saaf ho jaata hai, isliye
wahan SQLite mein rakha data agli baar nahi milta.

Password kabhi plain text mein save nahi hota. Sirf uska hash rakha
jaata hai, jisse password wapas nikalna possible nahi.

Use:
    import database
    database.setup()
    user_id = database.create_user("a@b.com", "secret")
    user = database.check_login("a@b.com", "secret")
"""

import json
import os
import sqlite3

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

DB_FILE = "crackproof.db"

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()


def using_postgres():
    """Supabase use karna hai ya laptop ki SQLite file."""

    return DATABASE_URL != ""


def q(sql):
    """
    Query ko sahi database ke hisaab se theek karta hai.

    SQLite sawaal ke nishan maangta hai:   WHERE id = ?
    Postgres percent-s maangta hai:        WHERE id = %s

    Isliye saari queries "?" ke saath likhi hain, aur zaroorat padne
    par yahan badal jaati hain. Isse har query do baar likhne se bach
    jaate hain.
    """

    if using_postgres():
        return sql.replace("?", "%s")

    return sql


def connect():
    """
    Database se connection.

    Dono taraf rows dictionary jaise kaam karte hain, yaani
    row["email"] likh sakte hain, row[1] nahi.
    """

    if using_postgres():

        import psycopg2
        import psycopg2.extras

        return psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )

    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row

    return connection


def run(connection, sql, values=()):
    """
    Ek query chalata hai aur cursor deta hai.

    SQLite mein connection.execute() seedha chal jaata hai, par
    Postgres mein cursor banana padta hai. Ye dono ko ek jaisa
    bana deta hai, taaki neeche ka code do baar na likhna pade.
    """

    cursor = connection.cursor()
    cursor.execute(q(sql), values)

    return cursor


def setup():
    """
    Tables banata hai agar pehle se nahi hain.

    Har baar chalana safe hai - "IF NOT EXISTS" ka yahi matlab hai.
    """

    # Auto-badhne wali id dono jagah alag likhi jaati hai
    if using_postgres():
        auto_id = "SERIAL PRIMARY KEY"
        now = "CURRENT_TIMESTAMP"
    else:
        auto_id = "INTEGER PRIMARY KEY AUTOINCREMENT"
        now = "CURRENT_TIMESTAMP"

    connection = connect()

    run(connection, """
        CREATE TABLE IF NOT EXISTS users (
            id            """ + auto_id + """,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    TEXT NOT NULL DEFAULT """ + now + """
        )
    """)

    run(connection, """
        CREATE TABLE IF NOT EXISTS interviews (
            id                 """ + auto_id + """,
            user_id            INTEGER NOT NULL,
            interview_id       TEXT NOT NULL,
            topic              TEXT NOT NULL,
            questions_answered INTEGER NOT NULL DEFAULT 0,
            readiness          TEXT,
            report_json        TEXT,
            created_at         TEXT NOT NULL DEFAULT """ + now + """
        )
    """)

    # Har evaluation par candidate ki raay: judgement sahi tha ya nahi.
    # Ye dheere-dheere labelled data banata hai - agar kabhi apna model
    # train karna ho, to yahi uska sach hoga.
    run(connection, """
        CREATE TABLE IF NOT EXISTS feedback (
            id              """ + auto_id + """,
            user_id         INTEGER,
            interview_id    TEXT NOT NULL,
            question_number INTEGER NOT NULL,
            was_fair        INTEGER NOT NULL,
            created_at      TEXT NOT NULL DEFAULT """ + now + """
        )
    """)

    # Ek user ke interviews jaldi mil jayein
    run(connection, """
        CREATE INDEX IF NOT EXISTS interviews_by_user
        ON interviews (user_id, created_at DESC)
    """)

    connection.commit()
    connection.close()


# ========================================================
# USERS
# ========================================================

def create_user(email, password):
    """
    Naya account banata hai.

    Return: (user_id, None) ya (None, "wajah")
    """

    email = (email or "").strip().lower()

    if "@" not in email or "." not in email:
        return None, "Please enter a valid email address."

    if len(password or "") < 6:
        return None, "Password must be at least 6 characters."

    connection = connect()

    try:
        if using_postgres():
            # Postgres lastrowid nahi deta, isliye nayi id maang lete hain
            cursor = run(
                connection,
                "INSERT INTO users (email, password_hash)"
                " VALUES (?, ?) RETURNING id",
                (email, generate_password_hash(password))
            )
            new_id = cursor.fetchone()["id"]
        else:
            cursor = run(
                connection,
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, generate_password_hash(password))
            )
            new_id = cursor.lastrowid

        connection.commit()

        return new_id, None

    except Exception as error:
        # email UNIQUE hai, isliye dobara daalne par yahan aayenge.
        # SQLite ise IntegrityError kehta hai, Postgres UniqueViolation.
        connection.rollback()

        name = type(error).__name__

        if "Integrity" in name or "Unique" in name:
            return None, "An account with that email already exists."

        raise

    finally:
        connection.close()


def check_login(email, password):
    """
    Email aur password sahi hain?

    Return: user dictionary ya None.

    Galat email aur galat password - dono par ek hi jawab jaata hai,
    taaki koi ye na pata kar sake ki kaunsa email registered hai.
    """

    email = (email or "").strip().lower()

    connection = connect()

    row = run(
        connection,
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    if not check_password_hash(row["password_hash"], password or ""):
        return None

    return {"id": row["id"], "email": row["email"]}


def get_user(user_id):
    """User ki jaankari id se."""

    connection = connect()

    row = run(
        connection,
        "SELECT id, email, created_at FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


# ========================================================
# INTERVIEWS
# ========================================================

def save_interview(user_id, interview_id, topic, report):
    """
    Ek poora interview user ke naam save karta hai.

    Wahi interview_id dobara aaye to update ho jaata hai, naya row
    nahi banta - jaise candidate ne batch 1 ke baad batch 2 kiya ho.
    """

    metrics = (report or {}).get("metrics", {})

    connection = connect()

    existing = run(
        connection,
        "SELECT id FROM interviews WHERE user_id = ? AND interview_id = ?",
        (user_id, interview_id)
    ).fetchone()

    values = (
        topic,
        metrics.get("questions_answered", 0),
        metrics.get("overall_readiness"),
        json.dumps(report, default=str),
    )

    if existing:
        run(
            connection,
            """UPDATE interviews
               SET topic = ?, questions_answered = ?, readiness = ?,
                   report_json = ?
               WHERE id = ?""",
            values + (existing["id"],)
        )
    else:
        run(
            connection,
            """INSERT INTO interviews
               (user_id, interview_id, topic, questions_answered,
                readiness, report_json)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, interview_id) + values
        )

    connection.commit()
    connection.close()


def list_interviews(user_id):
    """Is user ke saare interviews, naye pehle."""

    connection = connect()

    rows = run(
        connection,
        """SELECT interview_id, topic, questions_answered, readiness,
                  created_at
           FROM interviews
           WHERE user_id = ?
           ORDER BY created_at DESC""",
        (user_id,)
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_interview(user_id, interview_id):
    """
    Ek purana interview poora khol ke dekhne ke liye.

    user_id bhi match hona zaroori hai - taaki koi doosre ka
    interview na dekh sake.
    """

    connection = connect()

    row = run(
        connection,
        """SELECT * FROM interviews
           WHERE user_id = ? AND interview_id = ?""",
        (user_id, interview_id)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    data = dict(row)

    if data.get("report_json"):
        try:
            data["report"] = json.loads(data["report_json"])
        except Exception:
            data["report"] = None

    data.pop("report_json", None)

    return data


def delete_interview(user_id, interview_id):
    """
    Ek interview mitao - database se aur uski recordings bhi.

    Voice recordings personal data hain. User bole to sach mein
    mit jaani chahiye, sirf list se hatni nahi chahiye.
    """

    connection = connect()

    row = run(
        connection,
        "SELECT id FROM interviews WHERE user_id = ? AND interview_id = ?",
        (user_id, interview_id)
    ).fetchone()

    if row is None:
        connection.close()
        return False

    run(connection, "DELETE FROM interviews WHERE id = ?", (row["id"],))
    connection.commit()
    connection.close()

    remove_recordings(interview_id)

    return True


def delete_account(user_id):
    """
    User ka poora account mitao - saare interviews aur recordings samet.
    """

    interviews = list_interviews(user_id)

    connection = connect()
    run(connection, "DELETE FROM interviews WHERE user_id = ?", (user_id,))
    run(connection, "DELETE FROM users WHERE id = ?", (user_id,))
    connection.commit()
    connection.close()

    for interview in interviews:
        remove_recordings(interview["interview_id"])

    return True


def remove_recordings(interview_id):
    """Ek interview ka recordings folder mita deta hai."""

    folder = os.path.join("recordings", "interview_" + interview_id)

    if not os.path.isdir(folder):
        return

    try:
        for name in os.listdir(folder):
            os.remove(os.path.join(folder, name))
        os.rmdir(folder)

    except Exception as error:
        print("  Could not remove recordings:", error)


def save_feedback(user_id, interview_id, question_number, was_fair):
    """
    Candidate ne bataya ki evaluation sahi tha ya nahi.

    Ek hi sawaal par dobara raay de to purani badal jaati hai,
    nayi row nahi banti.
    """

    connection = connect()

    run(
        connection,
        """DELETE FROM feedback
           WHERE interview_id = ? AND question_number = ?""",
        (interview_id, question_number)
    )

    run(
        connection,
        """INSERT INTO feedback
           (user_id, interview_id, question_number, was_fair)
           VALUES (?, ?, ?, ?)""",
        (user_id, interview_id, question_number, 1 if was_fair else 0)
    )

    connection.commit()
    connection.close()


def feedback_summary():
    """
    Ab tak kitni raay mili - fair kitni, unfair kitni.

    Isse pata chalta hai ki evaluator kitna bharosemand hai.
    """

    connection = connect()

    row = run(
        connection,
        """SELECT COUNT(*) AS total,
                  SUM(was_fair) AS fair
           FROM feedback"""
    ).fetchone()

    connection.close()

    total = row["total"] or 0
    fair = row["fair"] or 0

    return {"total": total, "fair": fair, "unfair": total - fair}
