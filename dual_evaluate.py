"""
Har answer ko DO models se judge karwata hai aur dekhta hai kahan
jhagda hai.

Kyun? Kyunki 640 evaluations haath se check karna bahut hai. Par:

  dono agree karein  ->  shayad theek hai, sirf sample check karo
  dono alag bolein   ->  YAHAN insaan chahiye

Aksar 60-70% mein dono agree karte hain, to insaan ka kaam teen
guna kam ho jaata hai. Aur bonus - jahan models jhagadte hain wahi
sabse mushkil cases hote hain, jo training ke liye sabse keemti bhi
hain.

Chalane ka tareeka:

    python3 dual_evaluate.py --limit 20     (test ke liye)
    python3 dual_evaluate.py                (poora)

Beech mein rok do to koi baat nahi - dobara chalane par jahan chhoda
tha wahin se shuru hoga.

Result evaluations.jsonl mein jaata hai.
"""

import json
import os
import sys
import time

import llm_client
from evaluator import AnswerEvaluation
from prompts import EVALUATION_PROMPT, GROUNDING_BLOCK
from grounding import get_reference


IN_FILE = "synthetic_answers.jsonl"
OUT_FILE = "evaluations.jsonl"

MODEL_A = "openai/gpt-oss-120b"
MODEL_B = "openai/gpt-oss-20b"

# Score itna alag ho to jhagda maano
SCORE_GAP = 3


def judge(question, answer, reference, model):
    """Ek model se ek evaluation. Fail ho to None."""

    prompt = EVALUATION_PROMPT.format(
        question=question,
        transcript=answer
    )

    if reference:
        prompt = prompt + GROUNDING_BLOCK.format(reference=reference)

    old_model = llm_client.MODEL
    llm_client.MODEL = model
    llm_client._client = None

    try:
        result = llm_client.ask_llm(prompt, schema=AnswerEvaluation,
                                    retries=2)
    finally:
        llm_client.MODEL = old_model
        llm_client._client = None

    if result is None:
        return None

    return result.model_dump()


def evidence_map(evaluation):
    """
    Evidence ko dictionary bana do: dimension -> status

    Isse do evaluations compare karna aasan ho jaata hai.
    """

    result = {}

    for item in evaluation.get("evidence", []):
        result[item["evidence_type"]] = item["status"]

    return result


def find_disagreement(first, second):
    """
    Do evaluations compare karo.

    Return: list of wajahein. Khaali list matlab dono agree karte hain.
    """

    problems = []

    if first["verdict"] != second["verdict"]:
        problems.append(
            "verdict: " + first["verdict"] + " vs " + second["verdict"]
        )

    gap = abs(first["correctness_score"] - second["correctness_score"])
    if gap >= SCORE_GAP:
        problems.append(
            "correctness: " + str(first["correctness_score"])
            + " vs " + str(second["correctness_score"])
        )

    gap = abs(first["depth_score"] - second["depth_score"])
    if gap >= SCORE_GAP:
        problems.append(
            "depth: " + str(first["depth_score"])
            + " vs " + str(second["depth_score"])
        )

    # Kaunse dimensions test hue, aur unka status
    map_one = evidence_map(first)
    map_two = evidence_map(second)

    all_dimensions = set(map_one.keys()) | set(map_two.keys())

    for dimension in sorted(all_dimensions):

        status_one = map_one.get(dimension, "NOT_TESTED")
        status_two = map_two.get(dimension, "NOT_TESTED")

        if status_one != status_two:
            problems.append(
                dimension + ": " + status_one + " vs " + status_two
            )

    return problems


def load_done():
    """
    Jo pehle ho chuke hain unke keys, taaki dobara na karein.
    """

    done = set()

    if not os.path.exists(OUT_FILE):
        return done

    with open(OUT_FILE) as f:
        for line in f:
            try:
                row = json.loads(line)
                done.add(row["question"] + "|" + row["style"])
            except Exception:
                pass

    return done


def main():

    if not os.path.exists(IN_FILE):
        print("\n" + IN_FILE + " nahi mili.")
        print("Pehle ye chalao:  python3 synthetic_answers.py\n")
        return

    limit = None

    if "--limit" in sys.argv:
        spot = sys.argv.index("--limit")
        limit = int(sys.argv[spot + 1])

    rows = []
    with open(IN_FILE) as f:
        for line in f:
            rows.append(json.loads(line))

    if limit:
        rows = rows[:limit]

    done = load_done()

    print("\n" + str(len(rows)) + " answers")
    print(str(len(done)) + " pehle se ho chuke, unhe chhod raha hoon")
    print("Har answer par 2 models chalenge\n")

    agreed = 0
    disagreed = 0
    failed = 0

    output = open(OUT_FILE, "a")

    for number, row in enumerate(rows):

        key = row["question"] + "|" + row["style"]

        if key in done:
            continue

        label = "[" + str(number + 1) + "/" + str(len(rows)) + "] "
        label = label + row["subject"] + "/" + row["style"]

        # Wahi reference jo asli app deta hai
        reference, sources = get_reference(row["question"], row["subject"])

        first = judge(row["question"], row["answer"], reference, MODEL_A)
        second = judge(row["question"], row["answer"], reference, MODEL_B)

        if first is None or second is None:
            print(label + "  -> FAILED")
            failed = failed + 1
            continue

        problems = find_disagreement(first, second)

        if problems:
            disagreed = disagreed + 1
            print(label + "  -> CHECK: " + problems[0])
        else:
            agreed = agreed + 1
            print(label + "  -> agree (" + first["verdict"] + ")")

        output.write(json.dumps({
            "subject": row["subject"],
            "question": row["question"],
            "style": row["style"],
            "answer": row["answer"],
            "reference_sources": sources,
            "model_a": MODEL_A,
            "model_b": MODEL_B,
            "evaluation_a": first,
            "evaluation_b": second,
            "disagreements": problems,
            "needs_review": len(problems) > 0,
            "verified": False,
        }) + "\n")

        output.flush()

        time.sleep(1)

    output.close()

    total = agreed + disagreed

    print("\n" + "=" * 46)
    print("Dono agree kiye   : " + str(agreed))
    print("Jhagda hua        : " + str(disagreed) + "   <- ye check karne hain")
    print("Fail hue          : " + str(failed))

    if total:
        percent = round(disagreed * 100 / total)
        print("")
        print("Insaan ka kaam    : " + str(disagreed) + " out of "
              + str(total) + " (" + str(percent) + "%)")

    print("Save hua          : " + OUT_FILE)
    print("=" * 46 + "\n")


if __name__ == "__main__":
    main()
