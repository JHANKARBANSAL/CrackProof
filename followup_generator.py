import os
from dotenv import load_dotenv
from google import genai
from prompts import FOLLOWUP_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_followup(topic, question, transcript, probe):

    prompt = FOLLOWUP_PROMPT.format(
        topic=topic,
        question=question,
        transcript=transcript,
        strategy=probe["strategy"],
        target=probe["target"]
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()