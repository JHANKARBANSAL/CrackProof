"""
Training ke liye nakli candidate answers banata hai.

Kyun nakli? Kyunki 200 asli answers bolne mein 10 ghante lagenge.
Answer ek INPUT hai, label nahi - isliye use banwana theek hai.
Label (evaluation sahi thi ya nahi) insaan hi banayega, aur wahi
asli training data hai.

Har answer jaan-boojhkar BOLA HUA jaisa hota hai - bina punctuation,
natural flow mein. Kyunki asli app mein input Whisper ka transcript
hota hai, likha hua essay nahi. Agar saaf-suthre answers par train
karenge to model woh cheez seekhega jo use kabhi milti hi nahi.

Chalane ka tareeka:

    python3 synthetic_answers.py --questions 5     (test ke liye)
    python3 synthetic_answers.py --questions 40    (poora)

Result synthetic_answers.jsonl mein jaata hai.
"""

import json
import os
import sys
import time

from corpus_topics import TOPICS
from question_generator import generate_first_question
from llm_client import ask_llm


OUT_FILE = "synthetic_answers.jsonl"


# Har style ek alag tarah ka candidate hai.
#
# Ye list jaan-boojhkar poori rakhi hai. Agar sirf achhe aur bure
# answers honge, to model beech ke cases par kabhi theek nahi hoga -
# aur asli interview mein zyadatar answers beech ke hi hote hain.

STYLES = [

    ("EXCELLENT",
     "A complete, correct answer. Explains what it is, why it works, "
     "gives a concrete example, and mentions one limitation or "
     "trade-off. This should demonstrate every depth dimension."),

    ("SOLID_NO_EXAMPLE",
     "Correct and well reasoned, explains why it works, but gives no "
     "concrete example or code at all. Application should be missing."),

    ("FACTS_NO_REASONING",
     "States the correct facts and definitions accurately, but never "
     "explains why or how anything works. Pure recall, no mechanism."),

    ("PARTIAL",
     "Gets the core definition right but stops early. Misses an "
     "important part of what the question asked for. Not wrong, just "
     "incomplete."),

    ("MISCONCEPTION",
     "Gets the core idea right, then states one specific technical "
     "claim that is confidently and clearly WRONG. Keep the tone "
     "certain, as if the candidate believes it."),

    ("TWO_MISCONCEPTIONS",
     "Mostly correct, but contains two separate incorrect technical "
     "claims stated with confidence."),

    ("VAGUE",
     "Uses the right words but says nothing with substance. Circular, "
     "hand-wavy, could apply to almost any topic. Sounds like someone "
     "covering for not knowing."),

    ("VERBOSE_EMPTY",
     "Long and confident sounding, four or five sentences, but "
     "contains no actual technical content. Repeats the question back "
     "in different words."),

    ("WRONG",
     "Confidently incorrect from the start. The central claim is "
     "simply false, though it sounds plausible."),

    ("OFF_TOPIC",
     "Answers a different but related question from the same subject. "
     "Correct in itself, but does not address what was asked."),

    ("VERY_SHORT",
     "One short sentence. Correct as far as it goes, but tiny. Tests "
     "whether a brief answer is judged on content, not length."),

    ("CODE_EXAMPLE",
     "Answers mainly by walking through a concrete code example or "
     "scenario out loud, with little formal definition. Application "
     "should be strong, fundamentals weaker."),

    ("EDGE_CASE_FOCUS",
     "Skips the basics and goes straight to limitations, failure "
     "cases and trade-offs. Edge case strong, fundamentals thin."),

    ("CONTRADICTS_SELF",
     "Starts with a correct statement, then says something later in "
     "the answer that contradicts it, without noticing."),

    ("HINGLISH",
     "Correct and reasonably complete, but mixes Hindi and English "
     "the way Indian students actually speak. This must NOT be "
     "penalised, so it tests that rule."),

    ("CORRECT_BEYOND_REFERENCE",
     "Correct, and includes one accurate technical detail that a "
     "basic encyclopedia article would probably not mention. Tests "
     "that a right answer is not marked wrong just because the "
     "reference material does not cover it."),
]


PROMPT = """You are writing a SPOKEN answer for a mock technical interview.

QUESTION:
{question}

WRITE THIS KIND OF ANSWER:
{instruction}

HOW IT MUST SOUND:
This is a speech-to-text transcript of someone answering out loud.
So: no bullet points, no headings, no markdown, no code blocks.
Little or no punctuation. Natural spoken flow, with the occasional
"so" or "basically" or a restarted sentence. Between 20 and 90 words.

CRITICAL:
Stay fully in character as the candidate. The candidate has no idea
what kind of answer they are giving - they believe they are simply
answering the question.

So never describe the answer while writing it. Never write phrases
like "the wrong claim is", "here is a misconception", "this part is
vague", "I am contradicting myself", or "the answer repeats the
question". A real person would never say those things out loud.

If the instruction says to include something incorrect, just say the
incorrect thing plainly and confidently, as if you believe it.

Write only the answer text. Nothing else."""


def make_answer(question, instruction):
    """Ek nakli answer banata hai. Fail ho to None."""

    prompt = PROMPT.format(question=question, instruction=instruction)

    return ask_llm(prompt)


def make_questions(how_many):
    """
    Har subject se baari-baari sawaal banata hai, taaki dataset
    ek hi topic par jhuk na jaye.
    """

    subjects = list(TOPICS.keys())
    questions = []

    while len(questions) < how_many:

        subject = subjects[len(questions) % len(subjects)]

        print("  sawaal bana raha hoon [" + subject + "] ...", end=" ")

        question = generate_first_question(subject)

        if question is None:
            print("fail")
            continue

        question = " ".join(question.split())

        questions.append({"subject": subject, "question": question})
        print(question[:60])

        time.sleep(1)

    return questions


def main():

    how_many = 5

    if "--questions" in sys.argv:
        spot = sys.argv.index("--questions")
        how_many = int(sys.argv[spot + 1])

    print("\n" + str(how_many) + " sawaal x " + str(len(STYLES))
          + " styles = " + str(how_many * len(STYLES)) + " answers\n")

    questions = make_questions(how_many)

    print("\nAb answers bana raha hoon...\n")

    rows = []

    for item in questions:

        for name, instruction in STYLES:

            answer = make_answer(item["question"], instruction)

            if answer is None:
                print("  [" + name + "] fail")
                continue

            answer = " ".join(answer.split())

            rows.append({
                "subject": item["subject"],
                "question": item["question"],
                "style": name,
                "answer": answer,
            })

            print("  [" + item["subject"] + "/" + name + "] "
                  + answer[:58])

            time.sleep(1)

    with open(OUT_FILE, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

    print("\n" + str(len(rows)) + " answers -> " + OUT_FILE)

    # Kaunse style kitne bane
    counts = {}
    for row in rows:
        counts[row["style"]] = counts.get(row["style"], 0) + 1

    print("\nStyle ke hisaab se:")
    for name, _ in STYLES:
        print("  " + name.ljust(26) + str(counts.get(name, 0)))


if __name__ == "__main__":
    main()
