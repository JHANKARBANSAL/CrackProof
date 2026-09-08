import os
from typing import Literal

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from prompts import EVALUATION_PROMPT


# Load GEMINI_API_KEY from .env
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# Structure in which we want Gemini's evaluation
class AnswerEvaluation(BaseModel):
    verdict: Literal[
        "CORRECT",
        "PARTIALLY_CORRECT",
        "INCORRECT"
    ]

    correctness_score: int = Field(ge=0, le=10)
    depth_score: int = Field(ge=0, le=10)

    correct_points: list[str]

    # Jo current question ka proper answer dene ke liye necessary tha
    missing_core_concepts: list[str]

    # Jo mandatory nahi tha, but deeper understanding test karne ke liye useful hai
    deeper_concepts_to_probe: list[str]

    misconceptions: list[str]

    reasoning: str

prompt = EVALUATION_PROMPT.format(
    question=question,
    transcript=transcript
) 


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AnswerEvaluation,
        ),
    )

    return response.parsed


# Temporary test
if __name__ == "__main__":

    question = "What is polymorphism in Java?"

    transcript = """
    Polymorphism means an object can take multiple forms.
    """

    evaluation = evaluate_answer(question, transcript)

    print("\n--- CRACKPROOF EVALUATION ---")
    print("Verdict:", evaluation.verdict)
    print("Correctness:", evaluation.correctness_score, "/10")
    print("Depth:", evaluation.depth_score, "/10")
    print("Correct Points:", evaluation.correct_points)
print("Missing Core Concepts:", evaluation.missing_core_concepts)

print(
    "Deeper Concepts To Probe:",
    evaluation.deeper_concepts_to_probe
)
    print("Misconceptions:", evaluation.misconceptions)
    print("Reasoning:", evaluation.reasoning)