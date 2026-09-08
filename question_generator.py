import os
from dotenv import load_dotenv
from google import genai
from prompts import QUESTION_GENERATION_PROMPT, CONTINUATION_QUESTION_PROMPT


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_continuation_question(topic, interview_history):

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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()

def generate_first_question(topic):

    prompt = QUESTION_GENERATION_PROMPT.format(
        topic=topic
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()


if __name__ == "__main__":

    topic = input("Enter the topic you want to practice: ")

    question = generate_first_question(topic)

    print("\nInterviewer:")
    print(question)