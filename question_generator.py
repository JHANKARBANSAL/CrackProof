from prompts import (
    QUESTION_GENERATION_PROMPT,
    CONTINUATION_QUESTION_PROMPT
)
from llm_client import ask_llm


def generate_first_question(topic):
    """
    Returns the first question as text, or None if the model failed.
    """

    prompt = QUESTION_GENERATION_PROMPT.format(
        topic=topic
    )

    return ask_llm(prompt)


def generate_continuation_question(topic, interview_history):
    """
    Returns a new question on the same topic, or None if the model failed.
    """

    previous_questions = []

    for turn in interview_history:

        # Only consider questions from the current topic
        if turn["topic"] == topic:
            previous_questions.append(turn["question"])

    formatted_questions = "\n".join(
        f"{i + 1}. {question}"
        for i, question in enumerate(previous_questions)
    )

    prompt = CONTINUATION_QUESTION_PROMPT.format(
        topic=topic,
        previous_questions=formatted_questions
    )

    return ask_llm(prompt)


if __name__ == "__main__":

    topic = input("Enter the topic you want to practice: ")

    question = generate_first_question(topic)

    print("\nInterviewer:")
    print(question)
