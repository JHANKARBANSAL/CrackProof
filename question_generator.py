import os

from dotenv import load_dotenv
from google import genai

from prompts import QUESTION_GENERATION_PROMPT


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


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