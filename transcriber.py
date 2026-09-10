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


# Ye Whisper ke apne standard thresholds hain (OpenAI ke code se).
# Inhe dheela rakha hai jaan-boojhkar: asli garbage pakadna hai, par
# chhota ya kamzor answer reject nahi karna. Ek genuine chhote answer
# ka avg_logprob -0.6 tha, aur woh in thresholds se pass ho jaata hai.
MIN_AVG_LOGPROB = -1.0
MAX_NO_SPEECH = 0.6
MAX_NON_LATIN_RATIO = 0.20


def read_quality(result):
    """
    Whisper ke jawab mein se confidence ke numbers nikalta hai.

    Segments ka average leta hai. Kuch na mile to khaali dictionary,
    jiska matlab hai "pata nahi" - aur tab hum flag nahi karte.
    """

    quality = {
        "language": result.get("language", ""),
        "avg_logprob": None,
        "no_speech_prob": None,
    }

    segments = result.get("segments") or []

    if not segments:
        return quality

    logprobs = []
    no_speech = []

    for segment in segments:

        if segment.get("avg_logprob") is not None:
            logprobs.append(segment["avg_logprob"])

        if segment.get("no_speech_prob") is not None:
            no_speech.append(segment["no_speech_prob"])

    if logprobs:
        quality["avg_logprob"] = sum(logprobs) / len(logprobs)

    if no_speech:
        quality["no_speech_prob"] = sum(no_speech) / len(no_speech)

    return quality


def non_latin_ratio(text):
    """
    Kitne characters Latin alphabet se bahar ke hain.

    Cyrillic/Chinese jaise characters aa jayein to ye number bada
    ho jaata hai. Space aur punctuation nahi ginte.
    """

    letters = []

    for letter in text:
        if letter.isalpha():
            letters.append(letter)

    if not letters:
        return 0.0

    foreign = 0

    for letter in letters:
        # ord() 127 se upar matlab normal English letter nahi hai
        if ord(letter) > 127:
            foreign = foreign + 1

    return foreign / len(letters)


def find_problem(text, quality):
    """
    Transcript bharose ke laayak hai ya nahi.

    Problem mile to uski wajah (string) deta hai, warna None.
    """

    if not text or not text.strip():
        return "No speech could be transcribed."

    # 1. Whisper ne koi aur bhasha detect ki
    language = (quality.get("language") or "").lower()

    if language and language not in ("en", "english"):
        return (
            "The audio was detected as '" + language
            + "', not English."
        )

    # 2. Latin ke bahar ke characters bahut zyada
    ratio = non_latin_ratio(text)

    if ratio > MAX_NON_LATIN_RATIO:
        return (
            "The transcript is mostly non-English characters ("
            + str(int(ratio * 100)) + "%)."
        )

    # 3. Whisper ko apne hi transcript pe bharosa nahi tha
    logprob = quality.get("avg_logprob")

    if logprob is not None and logprob < MIN_AVG_LOGPROB:
        return (
            "The transcription confidence was too low ("
            + str(round(logprob, 2)) + ")."
        )

    # 4. Whisper ko laga ki bola hi kuch nahi gaya
    no_speech = quality.get("no_speech_prob")

    if no_speech is not None and no_speech > MAX_NO_SPEECH:
        return "Mostly silence was detected in the recording."

    return None


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
    """
    Groq ke whisper-large-v3 se transcript.

    Return: (text, quality)

    quality mein woh numbers hote hain jinse pata chalta hai ki
    Whisper ko kitna bharosa tha apne transcript pe.
    """

    client = _get_groq_client()

    with open(audio_path, "rb") as audio_file:
        data = audio_file.read()

    answer = client.audio.transcriptions.create(
        file=(os.path.basename(audio_path), data),
        model=GROQ_MODEL,
        language="en",
        # verbose_json maangne se confidence bhi milti hai
        response_format="verbose_json",
    )

    result = answer.model_dump()

    return result.get("text", "").strip(), read_quality(result)


def transcribe_with_local(audio_path):
    """
    Laptop ke apne whisper se transcript.

    Return: (text, quality) - Groq wale jaisa hi.
    """

    global _local_model

    if _local_model is None:
        print("Loading local Whisper model (ek baar)...")
        import whisper
        _local_model = whisper.load_model(LOCAL_MODEL)

    result = _local_model.transcribe(audio_path)

    return result["text"].strip(), read_quality(result)


def transcribe_audio(audio_path):
    """
    Voice file ko text mein badalta hai.

    Return: (text, problem)

    problem None hai to transcript bharose ke laayak hai.
    problem string hai to usme wajah likhi hai, aur main.py candidate
    se answer dobara record karwa leta hai.

    Pehle chuna hua tareeka, phir doosra. Dono fail ho to khaali text.
    """

    order = [
        ("local", transcribe_with_local),
        ("Groq", transcribe_with_groq),
    ]

    if MODE != "local":
        order.reverse()

    text = ""
    quality = {}

    for name, function in order:

        try:
            print("Converting speech to text (" + name + ")...")
            text, quality = function(audio_path)
            break

        except Exception as error:
            print("  " + name + " transcription failed:", error)

    return text, find_problem(text, quality)
