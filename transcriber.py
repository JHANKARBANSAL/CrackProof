"""
Voice ko text mein badalta hai.

Do tareeke hain:

  groq   - Groq ka whisper-large-v3. Free hai, tez hai, aur bada
           model hai. Internet chahiye.

  local  - Laptop ka apna whisper. Internet nahi chahiye, par
           model load hone mein ~10 second lagte hain.

Default groq hai. Groq fail ho jaye (internet nahi, quota khatam)
to apne aap local pe chala jaata hai, taaki interview ruke nahi.

.env mein badal sakti ho:
    TRANSCRIBER=groq     (default)
    TRANSCRIBER=local
"""

import os

from dotenv import load_dotenv


load_dotenv()

MODE = os.getenv("TRANSCRIBER", "groq").strip().lower()

GROQ_MODEL = "whisper-large-v3"

LOCAL_MODEL = "small"


# Local model bahut bhaari hai, isliye sirf tab load karte hain jab
# sach mein zaroorat pade. Isse har run ka ~10 second bach jaata hai.
_local_model = None

_groq_client = None


def _get_groq_client():

    global _groq_client

    if _groq_client is None:

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found in .env")

        from openai import OpenAI

        _groq_client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    return _groq_client


def transcribe_with_groq(audio_path):
    """Groq ke whisper-large-v3 se transcript."""

    client = _get_groq_client()

    with open(audio_path, "rb") as audio_file:
        data = audio_file.read()

    answer = client.audio.transcriptions.create(
        file=(os.path.basename(audio_path), data),
        model=GROQ_MODEL,
        language="en",
    )

    return answer.text.strip()


def transcribe_with_local(audio_path):
    """Laptop ke apne whisper se transcript."""

    global _local_model

    if _local_model is None:
        print("Loading local Whisper model (ek baar)...")
        import whisper
        _local_model = whisper.load_model(LOCAL_MODEL)

    result = _local_model.transcribe(audio_path)

    return result["text"].strip()


def transcribe_audio(audio_path):
    """
    Voice file ko text mein badalta hai.

    Pehle chuna hua tareeka, phir doosra. Dono fail ho to khaali
    string, jise main.py "dobara record karo" samajh leta hai.
    """

    if MODE == "local":

        try:
            print("Converting speech to text (local)...")
            return transcribe_with_local(audio_path)

        except Exception as error:
            print("  Local transcription failed:", error)
            print("  Groq try kar raha hoon...")

        try:
            return transcribe_with_groq(audio_path)
        except Exception as error:
            print("  Groq transcription bhi failed:", error)
            return ""

    # Default: groq pehle
    try:
        print("Converting speech to text (Groq whisper-large-v3)...")
        return transcribe_with_groq(audio_path)

    except Exception as error:
        print("  Groq transcription failed:", error)
        print("  Local whisper pe ja raha hoon...")

    try:
        return transcribe_with_local(audio_path)

    except Exception as error:
        print("  Local transcription bhi failed:", error)
        return ""
