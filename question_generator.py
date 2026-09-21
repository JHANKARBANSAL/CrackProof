from prompts import (
    QUESTION_GENERATION_PROMPT,
    CONTINUATION_QUESTION_PROMPT
)
from llm_client import ask_llm


FALLBACK_SEED_QUESTIONS = {
    "OOP": "Explain the four fundamental principles of Object-Oriented Programming (Encapsulation, Abstraction, Inheritance, and Polymorphism) and how they promote modular, maintainable software design.",
    "Java": "Explain the difference between `==` and `.equals()` in Java, and why it is critical to override `hashCode()` whenever you override `equals()`.",
    "DBMS": "Explain the ACID properties of relational database management systems and describe how transaction isolation levels prevent issues like dirty reads and phantom reads.",
    "OS": "Explain the fundamental differences between a process and a thread. How does the operating system manage context switching between them?",
    "Computer Networks": "Explain the step-by-step process of what happens when a user types a URL (such as https://google.com) into a browser and presses Enter, including DNS, TCP handshake, and TLS negotiation.",
    "DSA": "Explain the internal mechanics of a Hash Table, how hash collisions are resolved (chaining vs open addressing), and the time complexities of core operations."
}


def generate_first_question(topic):
    """
    Returns the first question as text. Falls back to curated seed question
    if the model call fails or takes too long.
    """

    prompt = QUESTION_GENERATION_PROMPT.format(
        topic=topic
    )

    try:
        res = ask_llm(prompt)
        if res and res.strip():
            return res.strip()
    except Exception as err:
        print(f"  [question_generator] LLM question generation error: {err}")

    # Fallback to curated seed question matching topic
    for key, seed_q in FALLBACK_SEED_QUESTIONS.items():
        if key.lower() in topic.lower() or topic.lower() in key.lower():
            return seed_q

    return FALLBACK_SEED_QUESTIONS["OOP"]


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
