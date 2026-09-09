from typing import Literal

from pydantic import BaseModel, Field
from prompts import EVALUATION_PROMPT, GROUNDING_BLOCK
from llm_client import ask_llm

# 👇 YAHA ADD KARO
class DepthEvidence(BaseModel):
    evidence_type: Literal[
        "FUNDAMENTAL",
        "REASONING",
        "APPLICATION",
        "EDGE_CASE"
    ]

    # Three-state, because one dimension can be partly right and
    # partly wrong within a single answer.
    status: Literal[
        "DEMONSTRATED",
        "PARTIALLY_DEMONSTRATED",
        "NOT_DEMONSTRATED"
    ]

    evidence_from_answer: str


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
    evidence: list[DepthEvidence]
    reasoning: str

def evaluate_answer(question: str, transcript: str, reference: str = ""):
    """
    Returns an AnswerEvaluation, or None if the model could not be
    reached. The caller must check for None.

    reference is optional text from the knowledge base. When it is
    given, the model judges the answer against that text instead of
    from memory. When it is empty the behaviour is exactly as before,
    so a retrieval failure never stops the interview.
    """

    prompt = EVALUATION_PROMPT.format(
        question=question,
        transcript=transcript
    )

    if reference:
        prompt = prompt + GROUNDING_BLOCK.format(reference=reference)

    return ask_llm(prompt, schema=AnswerEvaluation)
