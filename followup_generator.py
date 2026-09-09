from prompts import FOLLOWUP_PROMPT
from llm_client import ask_llm


def generate_followup(topic, question, transcript, probe):
    """
    Returns the next question as text, or None if the model failed.
    """

    prompt = FOLLOWUP_PROMPT.format(
        topic=topic,
        question=question,
        transcript=transcript,
        strategy=probe["strategy"],
        target=probe["target"]
    )

    return ask_llm(prompt)
