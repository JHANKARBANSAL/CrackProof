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
import re
import socket
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
        try:
            import psycopg2
            import psycopg2.extras

            return psycopg2.connect(
                DATABASE_URL,
                cursor_factory=psycopg2.extras.RealDictCursor,
                connect_timeout=4
            )
        except Exception:
            # Switching databases on an outage can mix account IDs and lose history.
            raise RuntimeError("Could not connect to the configured PostgreSQL database. Please retry.") from None

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

    connection = connect()
    # Both databases support CURRENT_TIMESTAMP.
    now = "CURRENT_TIMESTAMP"
    if using_postgres():
        auto_id = "SERIAL PRIMARY KEY"
    else:
        auto_id = "INTEGER PRIMARY KEY AUTOINCREMENT"

    run(connection, """
        CREATE TABLE IF NOT EXISTS users (
            id            """ + auto_id + """,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name          TEXT,
            created_at    TEXT NOT NULL DEFAULT """ + now + """
        )
    """)

    # Agar purani database file hai toh name column add kar do
    if using_postgres():
        run(connection, "ALTER TABLE users ADD COLUMN IF NOT EXISTS name TEXT")
        connection.commit()
    else:
        try:
            run(connection, "ALTER TABLE users ADD COLUMN name TEXT")
            connection.commit()
        except Exception:
            connection.rollback()

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

    run(connection, """
        CREATE TABLE IF NOT EXISTS interview_sessions (
            interview_id TEXT PRIMARY KEY,
            owner_key TEXT NOT NULL,
            state_json TEXT NOT NULL,
            revision INTEGER NOT NULL DEFAULT 0
        )
    """)

    run(connection, """
        CREATE TABLE IF NOT EXISTS candidate_profiles (
            owner_key TEXT PRIMARY KEY,
            profile_json TEXT NOT NULL
        )
    """)
    run(connection, """
        CREATE TABLE IF NOT EXISTS panel_sessions (
            panel_id TEXT PRIMARY KEY,
            owner_key TEXT NOT NULL,
            state_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            revision INTEGER NOT NULL DEFAULT 0
        )
    """)
    run(connection, "CREATE INDEX IF NOT EXISTS panels_by_owner ON panel_sessions (owner_key, created_at DESC)")
    connection.commit()
    connection.close()


def load_profile(owner):
    connection = connect()
    try:
        row = run(connection, "SELECT profile_json FROM candidate_profiles WHERE owner_key = ?", (owner,)).fetchone()
        return json.loads(row["profile_json"]) if row else None
    finally:
        connection.close()


def load_panel(panel_id, owner):
    connection = connect()
    try:
        row = run(connection, "SELECT state_json, revision FROM panel_sessions WHERE panel_id = ? AND owner_key = ?", (panel_id, owner)).fetchone()
        return (json.loads(row["state_json"]), row["revision"]) if row else None
    finally:
        connection.close()


def save_panel(state, owner, revision=None):
    """An optimistic lock prevents two tabs from answering the same turn twice."""
    connection = connect()
    try:
        if revision is None:
            cursor = run(connection, """INSERT INTO panel_sessions (panel_id, owner_key, state_json, created_at)
                VALUES (?, ?, ?, ?) ON CONFLICT (panel_id) DO NOTHING""",
                (state["id"], owner, json.dumps(state), state["created_at"]))
        else:
            cursor = run(connection, """UPDATE panel_sessions SET state_json = ?, revision = revision + 1
                WHERE panel_id = ? AND owner_key = ? AND revision = ?""",
                (json.dumps(state), state["id"], owner, revision))
        changed = cursor.rowcount == 1
        connection.commit()
        return changed
    finally:
        connection.close()


def list_panels(owner):
    connection = connect()
    try:
        rows = run(connection, "SELECT state_json FROM panel_sessions WHERE owner_key = ? ORDER BY created_at DESC LIMIT 20", (owner,)).fetchall()
        result = []
        for row in rows:
            state = json.loads(row["state_json"])
            result.append({"id": state["id"], "created_at": state["created_at"],
                           "target_role": state["profile"]["target_role"], "status": state["status"],
                           "answered": len(state["turns"])})
        return result
    finally:
        connection.close()


def save_profile(owner, profile):
    connection = connect()
    try:
        run(connection, """
            INSERT INTO candidate_profiles (owner_key, profile_json) VALUES (?, ?)
            ON CONFLICT (owner_key) DO UPDATE SET profile_json = excluded.profile_json
        """, (owner, json.dumps(profile)))
        connection.commit()
    finally:
        connection.close()


# ========================================================
# USERS
# ========================================================

DISPOSABLE_DOMAINS = {
    "tempmail.com", "mailinator.com", "10minutemail.com", "guerrillamail.com",
    "sharklasers.com", "throwawaymail.com", "yopmail.com", "temp-mail.org",
    "fakeinbox.com", "dispostable.com", "getairmail.com", "trashmail.com",
    "mohmal.com", "burnermail.io", "maildrop.cc", "nada.ltd", "crazymailing.com",
    "generator.email", "armyspy.com", "cuvox.de", "dayrep.com", "fleckens.hu",
    "gustr.com", "jourrapide.com", "rhyta.com", "superrito.com", "teleworm.us"
}

COMMON_DOMAIN_TYPOS = {
    "gma.com": "gmail.com",
    "gmai.com": "gmail.com",
    "gamil.com": "gmail.com",
    "gmial.com": "gmail.com",
    "gmaill.com": "gmail.com",
    "gmaik.com": "gmail.com",
    "gmeil.com": "gmail.com",
    "gmail.co": "gmail.com",
    "gemail.com": "gmail.com",
    "gmal.com": "gmail.com",
    "g-mail.com": "gmail.com",
    "yaho.com": "yahoo.com",
    "yahooo.com": "yahoo.com",
    "yhoo.com": "yahoo.com",
    "yaho.co.in": "yahoo.co.in",
    "yaho.in": "yahoo.in",
    "hotmial.com": "hotmail.com",
    "hotmai.com": "hotmail.com",
    "hotmil.com": "hotmail.com",
    "hotmali.com": "hotmail.com",
    "outlok.com": "outlook.com",
    "outloo.com": "outlook.com",
    "outllok.com": "outlook.com",
    "icld.com": "icloud.com",
    "iclou.com": "icloud.com",
    "redifmail.com": "rediffmail.com",
}

DUMMY_DOMAINS = {
    "test.com", "example.com", "sample.com", "fake.com", "dummy.com",
    "abc.com", "xyz.com", "def.com", "foo.com", "bar.com", "domain.com",
    "email.com", "user.com", "company.com", "site.com", "none.com",
    "nothing.com", "whatever.com", "h.com", "b.c", "test.in", "sample.org",
    "fakeemail.com"
}

POPULAR_DOMAINS = [
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com",
    "proton.me", "protonmail.com", "zoho.com", "aol.com", "rediffmail.com"
]

EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
)

try:
    from email_validator import validate_email as check_email_deliverability, EmailNotValidError
    _has_email_validator = True
except ImportError:
    _has_email_validator = False


def _levenshtein(s1, s2):
    if len(s1) < len(s2):
        return _levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def validate_email_address(email):
    """
    Validates email format, typo detection, placeholder domains, disposable providers, and DNS deliverability.
    Return: (is_valid: bool, error_message: str | None)
    """
    if not email:
        return False, "Email address is required."

    email = email.strip().lower()

    # Syntax check
    if not EMAIL_REGEX.match(email):
        return False, "Please enter a valid email address (e.g. name@example.com)."

    username, domain = email.split("@", 1)

    # Username checks
    if len(username) < 2:
        return False, "Email username must be at least 2 characters long."

    # Domain parts check (reject single letter domains like 'h.com')
    domain_parts = domain.split(".")
    if any(len(part) < 2 for part in domain_parts[:-1]):
        return False, f"Domain '{domain}' is not a valid domain name."

    # TLD check
    tld = domain_parts[-1]
    if len(tld) < 2 or not tld.isalpha():
        return False, f"Invalid top-level domain '.{tld}'."

    # Direct typo dictionary check (e.g. gma.com -> gmail.com)
    if domain in COMMON_DOMAIN_TYPOS:
        suggested = COMMON_DOMAIN_TYPOS[domain]
        return False, f"Did you mean '@{suggested}'? '{domain}' is not a valid email provider."

    # Levenshtein distance typo check against popular domains (1 or 2 typos)
    for pop in POPULAR_DOMAINS:
        dist = _levenshtein(domain, pop)
        if 0 < dist <= 2 and domain not in POPULAR_DOMAINS:
            return False, f"Did you mean '@{pop}'? '{domain}' appears to be a typo."

    # Dummy / placeholder domains check
    if domain in DUMMY_DOMAINS:
        return False, f"Domain '{domain}' is a placeholder / invalid email domain."

    # Disposable domains check
    if domain in DISPOSABLE_DOMAINS:
        return False, "Temporary or disposable email addresses are not allowed."

    # Whitelist for local internal development
    if domain == "crackproof.dev":
        return True, None

    # Deep RFC deliverability check (checks if domain accepts email, MX records, Null MX)
    if _has_email_validator:
        try:
            check_email_deliverability(email, check_deliverability=True)
            return True, None
        except EmailNotValidError as e:
            return False, str(e)
        except Exception:
            pass

    # Live DNS check to verify that the domain actually exists
    try:
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(3.0)
        try:
            socket.gethostbyname(domain)
        finally:
            socket.setdefaulttimeout(old_timeout)
    except socket.gaierror:
        return False, f"Domain '@{domain}' does not exist. Please check your email."
    except Exception:
        # Fallback if offline or timeout, do not block legitimate users
        pass

    return True, None


def create_user(email, password, name=None):
    """
    Naya account banata hai.

    Return: (user_id, None) ya (None, "wajah")
    """

    email = (email or "").strip().lower()
    name = (name or "").strip()

    is_valid, err_msg = validate_email_address(email)
    if not is_valid:
        return None, err_msg

    if not name:
        name = email.split("@")[0].capitalize()

    if len(password or "") < 6:
        return None, "Password must be at least 6 characters."

    connection = connect()

    try:
        if using_postgres():
            # Postgres lastrowid nahi deta, isliye nayi id maang lete hain
            cursor = run(
                connection,
                "INSERT INTO users (email, password_hash, name)"
                " VALUES (?, ?, ?) RETURNING id",
                (email, generate_password_hash(password), name)
            )
            new_id = cursor.fetchone()["id"]
        else:
            cursor = run(
                connection,
                "INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)",
                (email, generate_password_hash(password), name)
            )
            new_id = cursor.lastrowid

        connection.commit()

        return new_id, None

    except Exception as error:
        # email UNIQUE hai, isliye dobara daalne par yahan aayenge.
        # SQLite ise IntegrityError kehta hai, Postgres UniqueViolation.
        connection.rollback()

        name_err = type(error).__name__

        if "Integrity" in name_err or "Unique" in name_err:
            return None, "An account with that email already exists."

        raise

    finally:
        connection.close()


def check_login(email, password):
    """
    Email aur password sahi hain?

    Return: (user_dict, None) on success, ya (None, error_message) on failure.
    """

    email = (email or "").strip().lower()
    if not email:
        return None, "Please enter your email address."

    connection = connect()

    row = run(
        connection,
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()

    connection.close()

    if row is None:
        return None, "No account found with this email. Please check your email or sign up."

    if not check_password_hash(row["password_hash"], password or ""):
        return None, "Incorrect password. Please check your password and try again."

    user_data = dict(row)
    display_name = user_data.get("name") or user_data["email"].split("@")[0].capitalize()
    return {
        "id": user_data["id"],
        "email": user_data["email"],
        "name": display_name
    }, None


def get_user(user_id):
    """User ki jaankari id se."""

    connection = connect()

    row = run(
        connection,
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    connection.close()

    if row is None:
        return None

    user_data = dict(row)
    display_name = user_data.get("name") or user_data["email"].split("@")[0].capitalize()
    return {
        "id": user_data["id"],
        "email": user_data["email"],
        "name": display_name,
        "created_at": user_data.get("created_at")
    }


# ========================================================
# INTERVIEWS
# ========================================================

def save_interview(user_id, interview_id, topic, report, connection=None):
    """
    Ek poora interview user ke naam save karta hai.

    Wahi interview_id dobara aaye to update ho jaata hai, naya row
    nahi banta - jaise candidate ne batch 1 ke baad batch 2 kiya ho.
    """

    metrics = (report or {}).get("metrics", {})

    own_connection = connection is None
    connection = connection or connect()

    existing = run(
        connection,
        "SELECT id FROM interviews WHERE user_id = ? AND interview_id = ?",
        (user_id, interview_id)
    ).fetchone()

    values = (
        topic,
        len(report["turns"]) if "turns" in report else metrics.get("questions_answered", 0),
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

    if own_connection:
        connection.commit()
        connection.close()


def load_session(interview_id, owner_key):
    connection = connect()
    try:
        row = run(connection,
            "SELECT state_json, revision FROM interview_sessions WHERE interview_id = ? AND owner_key = ?",
            (interview_id, owner_key)).fetchone()
        return (json.loads(row["state_json"]), row["revision"]) if row else None
    finally:
        connection.close()


def save_session(interview_id, owner_key, state, revision=None, report=None):
    """Save state and history together; reject a competing request's stale copy."""
    connection = connect()
    try:
        if revision is None:
            run(connection,
                "INSERT INTO interview_sessions (interview_id, owner_key, state_json) VALUES (?, ?, ?)",
                (interview_id, owner_key, json.dumps(state)))
        else:
            cursor = run(connection,
                "UPDATE interview_sessions SET state_json = ?, revision = revision + 1 WHERE interview_id = ? AND owner_key = ? AND revision = ?",
                (json.dumps(state), interview_id, owner_key, revision))
            if cursor.rowcount != 1:
                connection.rollback()
                return False
        if report and owner_key.startswith("user:"):
            save_interview(int(owner_key.split(":", 1)[1]), interview_id,
                           state["topic"], report, connection=connection)
        connection.commit()
        return True
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def list_guest_sessions(owner_key):
    connection = connect()
    try:
        rows = run(connection,
            "SELECT state_json FROM interview_sessions WHERE owner_key = ?",
            (owner_key,)).fetchall()
        return [json.loads(row["state_json"]) for row in rows]
    finally:
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
    run(connection, "DELETE FROM interview_sessions WHERE interview_id = ? AND owner_key = ?",
        (interview_id, "user:" + str(user_id)))
    run(connection, "DELETE FROM feedback WHERE interview_id = ? AND user_id = ?", (interview_id, user_id))
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
    run(connection, "DELETE FROM interview_sessions WHERE owner_key = ?", ("user:" + str(user_id),))
    run(connection, "DELETE FROM candidate_profiles WHERE owner_key = ?", ("user:" + str(user_id),))
    run(connection, "DELETE FROM panel_sessions WHERE owner_key = ?", ("user:" + str(user_id),))
    run(connection, "DELETE FROM feedback WHERE user_id = ?", (user_id,))
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
