"""
Kya reference material dene se evaluation stable hoti hai?

drift_test.py ne dikhaya tha ki wahi answer har baar alag grade
hota hai. Ye test poochhta hai: agar model ko sahi paragraph pehle
se de diya jaye, to kya woh sthir ho jaata hai?

Yahan koi chunking, embedding ya retriever nahi hai. Reference
paragraph neeche haath se likha hua hai, seedha
knowledge/DBMS/database_normalization.md se copy kiya gaya.

Chalane ka tareeka:

    python3 grounding_test.py

Ye ~10 Groq calls lega. Kisi existing file ko badalta nahi hai.
"""

from evaluator import AnswerEvaluation
from llm_client import ask_llm, describe
from prompts import EVALUATION_PROMPT


RUNS = 5


# drift_test.py ka bilkul wahi sawaal aur wahi answer.
# Isi pe missing concepts har run mein alag aaye the.
QUESTION = "Why do we normalize a database?"

TRANSCRIPT = (
    "We normalize so the database is organised properly and "
    "there is no repetition of data. It makes the tables "
    "cleaner and the database works better and faster when "
    "we have more data."
)


# knowledge/DBMS/database_normalization.md se seedha copy kiya hua.
REFERENCE = """
Database normalization is the process of structuring a relational
database in accordance with a series of normal forms to reduce data
redundancy and improve data integrity. It was first proposed by
British computer scientist Edgar F. Codd as part of his relational
model. Normalization entails organizing the columns (attributes) and
tables (relations) of a database to ensure that their dependencies are
properly enforced by database integrity constraints.

The objectives of normalization beyond 1NF were stated by Codd as:
to free the collection of relations from undesirable insertion,
update and deletion dependencies; to reduce the need for restructuring
the collection of relations as new types of data are introduced; to
make the relational model more informative to users; and to make the
collection of relations neutral to query statistics.

When an attempt is made to modify a relation, the following
undesirable side effects may arise in relations that have not been
sufficiently normalized:

Insertion anomaly: there are circumstances in which certain facts
cannot be recorded at all.

Update anomaly: the same information can be expressed on multiple
rows, therefore updates may result in logical inconsistencies.

Deletion anomaly: the deletion of data representing certain facts
necessitates the deletion of data representing completely different
facts.

A fully normalized database can be extended to accommodate new types
of data with minimal changes to its existing structure.

Codd introduced the first normal form (1NF) in 1970, then the second
(2NF) and third (3NF) in 1971, and Codd and Boyce defined
Boyce-Codd normal form (BCNF) in 1974. Informally, a relation is
often described as normalized if it meets third normal form. Most 3NF
relations are free of insertion, update and deletion anomalies.
"""


# Ye woh hissa hai jo baad mein prompts.py mein jayega.
# Abhi yahan rakha hai taaki existing code na badle.
GROUNDING_BLOCK = """

REFERENCE MATERIAL:

The text below is from a reference source on this topic. Judge the
candidate's answer against this material rather than from memory.

{reference}

IMPORTANT: This reference may be incomplete. If the candidate says
something correct that is not covered here, do NOT mark it wrong.
Only list a missing core concept when the reference shows it is
genuinely required to answer THIS question.
"""


def evaluate_once(with_reference):
    """Ek evaluation. with_reference=True ho to reference bhi bhejo."""

    prompt = EVALUATION_PROMPT.format(
        question=QUESTION,
        transcript=TRANSCRIPT
    )

    if with_reference:
        prompt = prompt + GROUNDING_BLOCK.format(reference=REFERENCE)

    return ask_llm(prompt, schema=AnswerEvaluation, retries=2)


def collect(with_reference, label):
    """RUNS baar evaluate karo aur results ki list do."""

    print("\n" + label)

    results = []

    for number in range(1, RUNS + 1):

        print("  run " + str(number) + "/" + str(RUNS) + " ... ", end="")

        answer = evaluate_once(with_reference)

        if answer is None:
            print("FAILED")
            continue

        print(
            answer.verdict
            + "  c=" + str(answer.correctness_score)
            + "  d=" + str(answer.depth_score)
        )

        results.append(answer)

    return results


def spread(numbers):
    """Sabse bada minus sabse chhota."""

    if not numbers:
        return 0

    return max(numbers) - min(numbers)


def show_report(results, label):

    print("\n--- " + label + " ---")

    if len(results) < 2:
        print("  Itne results nahi ki compare kar sakein.")
        return

    # ---------- 1. VERDICT ----------
    verdicts = []
    for r in results:
        verdicts.append(r.verdict)

    counts = {}
    for v in verdicts:
        counts[v] = counts.get(v, 0) + 1

    print("\n  1. VERDICT DISTRIBUTION")
    for v in counts:
        print("     " + v + ": " + str(counts[v]) + "/" + str(len(verdicts)))

    if len(counts) == 1:
        print("     -> STABLE")
    else:
        print("     -> DRIFTED (" + str(len(counts)) + " alag verdicts)")

    # ---------- 2. SCORES ----------
    correctness = []
    depth = []
    for r in results:
        correctness.append(r.correctness_score)
        depth.append(r.depth_score)

    print("\n  2. SCORE VARIANCE")
    print("     correctness: " + str(correctness)
          + "   spread = " + str(spread(correctness)))
    print("     depth      : " + str(depth)
          + "   spread = " + str(spread(depth)))

    # ---------- 3. MISSING CONCEPTS ----------
    concept_sets = []
    for r in results:
        one_set = set()
        for c in r.missing_core_concepts:
            one_set.add(c.lower().strip())
        concept_sets.append(frozenset(one_set))

    unique_concept_sets = set(concept_sets)

    print("\n  3. MISSING CONCEPTS CONSISTENCY")
    print("     " + str(len(unique_concept_sets))
          + " alag sets in " + str(len(concept_sets)) + " runs")

    if len(unique_concept_sets) == 1:
        print("     -> IDENTICAL har run")
    else:
        print("     -> VARIED")

    for i in range(len(concept_sets)):
        print("     run " + str(i + 1) + ": "
              + str(sorted(concept_sets[i])))

    # ---------- 4. MISCONCEPTIONS ----------
    misconception_sets = []
    for r in results:
        one_set = set()
        for m in r.misconceptions:
            one_set.add(m.lower().strip())
        misconception_sets.append(frozenset(one_set))

    unique_misconceptions = set(misconception_sets)

    print("\n  4. MISCONCEPTION CONSISTENCY")
    print("     " + str(len(unique_misconceptions))
          + " alag sets in " + str(len(misconception_sets)) + " runs")

    if len(unique_misconceptions) == 1:
        print("     -> IDENTICAL har run")
    else:
        print("     -> VARIED")

    for i in range(len(misconception_sets)):
        print("     run " + str(i + 1) + ": "
              + str(sorted(misconception_sets[i])))


def main():

    print("\n" + "=" * 60)
    print("GROUNDING TEST")
    print("=" * 60)
    print("Model     : " + describe())
    print("Question  : " + QUESTION)
    print("Runs      : " + str(RUNS) + " baseline + " + str(RUNS) + " grounded")

    baseline = collect(False, "BASELINE (bina reference ke)")
    grounded = collect(True, "GROUNDED (reference ke saath)")

    print("\n\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    show_report(baseline, "BASELINE")
    show_report(grounded, "GROUNDED")

    print("\n\n" + "=" * 60)
    print("KYA MATLAB HAI")
    print("=" * 60)
    print(
        "\nAgar GROUNDED ke verdict, scores aur missing concepts\n"
        "BASELINE se zyada sthir hain, to reference material se\n"
        "farak padta hai aur poora RAG pipeline banana sahi hai.\n"
        "\nAgar dono lagbhag ek jaise hain, to Wikipedia ka content\n"
        "is kaam ke liye kaafi nahi hai, aur chunking/embeddings\n"
        "banane se pehle content ke baare mein sochna padega.\n"
    )


if __name__ == "__main__":
    main()
