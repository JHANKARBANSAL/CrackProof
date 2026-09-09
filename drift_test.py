"""
Does Gemini give the SAME verdict for the SAME answer every time?

Run this before deciding whether RAG is worth building. If verdicts are
stable, Gemini's own explanation is trustworthy and grounding adds less
than expected. If they drift, the same answer is being graded
differently on different days, and grounding is genuinely needed.

Usage:
    python3 drift_test.py
"""

from evaluator import evaluate_answer


RUNS = 5


# Three realistic answers. The borderline ones matter most: a clearly
# correct or clearly wrong answer is easy, but real candidates live in
# the middle, and that is where a grader either holds steady or wobbles.
SAMPLES = [
    {
        "label": "STRONG answer",
        "question": "What is the difference between a class and an object?",
        "transcript": (
            "A class is a blueprint or template that defines the "
            "structure and behaviour, meaning the attributes and the "
            "methods. An object is a concrete instance of that class "
            "created at runtime. So if Car is the class, then myCar "
            "is an object with its own values for the attributes, and "
            "each object gets its own copy of the instance variables."
        ),
    },
    {
        "label": "MIXED answer (correct fact + misconception)",
        "question": "What is the difference between a class and an object?",
        "transcript": (
            "A class is a blueprint and an object is an instance of "
            "the class. But I think the memory for all the instances "
            "is allocated when the class is loaded, so all objects "
            "already exist after loading."
        ),
    },
    {
        "label": "VAGUE answer (borderline)",
        "question": "Why do we normalize a database?",
        "transcript": (
            "We normalize so the database is organised properly and "
            "there is no repetition of data. It makes the tables "
            "cleaner and the database works better and faster when "
            "we have more data."
        ),
    },
]


def summarise(evaluations):
    """Turn several evaluations of one answer into comparable values."""

    verdicts = [e.verdict for e in evaluations]
    correctness = [e.correctness_score for e in evaluations]
    depth = [e.depth_score for e in evaluations]

    # Concept wording varies run to run, so compare the SETS
    concept_sets = [
        frozenset(c.lower().strip() for c in e.missing_core_concepts)
        for e in evaluations
    ]

    dimension_sets = [
        frozenset(
            (ev.evidence_type, ev.status) for ev in e.evidence
        )
        for e in evaluations
    ]

    return verdicts, correctness, depth, concept_sets, dimension_sets


def main():

    print("\n" + "=" * 60)
    print(f"VERDICT DRIFT TEST  ({RUNS} runs per answer)")
    print("=" * 60)

    unstable_count = 0
    completed_samples = 0

    for sample in SAMPLES:

        print(f"\n\n### {sample['label']}")
        print(f"Q: {sample['question']}")

        evaluations = []

        for run in range(1, RUNS + 1):

            print(f"  run {run}/{RUNS} ...", end=" ", flush=True)

            evaluation = evaluate_answer(
                question=sample["question"],
                transcript=sample["transcript"]
            )

            if evaluation is None:
                print("FAILED (skipped)")
                continue

            print(
                f"{evaluation.verdict} "
                f"c={evaluation.correctness_score} "
                f"d={evaluation.depth_score}"
            )

            evaluations.append(evaluation)

        if len(evaluations) < 2:
            print(
                "  Not enough successful runs to compare "
                "(likely the daily quota ran out)."
            )
            continue

        completed_samples += 1

        verdicts, correctness, depth, concepts, dimensions = \
            summarise(evaluations)

        print("\n  RESULT")

        # --- verdict ---
        unique_verdicts = set(verdicts)

        if len(unique_verdicts) == 1:
            print(f"    Verdict:      STABLE  ({verdicts[0]})")
        else:
            unstable_count += 1
            print(f"    Verdict:      DRIFTED  {sorted(unique_verdicts)}")

        # --- scores ---
        c_spread = max(correctness) - min(correctness)
        d_spread = max(depth) - min(depth)

        print(
            f"    Correctness:  {min(correctness)}-{max(correctness)} "
            f"(spread {c_spread})"
        )
        print(
            f"    Depth:        {min(depth)}-{max(depth)} "
            f"(spread {d_spread})"
        )

        if c_spread >= 3 or d_spread >= 3:
            unstable_count += 1
            print("                  ^ large spread")

        # --- missing concepts ---
        if len(set(concepts)) == 1:
            print("    Missing concepts: IDENTICAL every run")
        else:
            print(
                f"    Missing concepts: VARIED across "
                f"{len(set(concepts))} different sets"
            )
            for i, concept_set in enumerate(concepts, start=1):
                print(f"      run {i}: {sorted(concept_set) or '[]'}")

        # --- depth dimensions ---
        if len(set(dimensions)) == 1:
            print("    Depth evidence:   IDENTICAL every run")
        else:
            print(
                f"    Depth evidence:   VARIED across "
                f"{len(set(dimensions))} different sets"
            )
            for i, dimension_set in enumerate(dimensions, start=1):
                print(f"      run {i}: {sorted(dimension_set)}")

    # ---------------------------------------------------
    print("\n\n" + "=" * 60)
    print("WHAT THIS MEANS")
    print("=" * 60)

    # Do not claim a conclusion the run did not actually earn.
    if completed_samples < len(SAMPLES):
        print(
            f"\nINCONCLUSIVE: only {completed_samples} of "
            f"{len(SAMPLES)} answers were tested. The rest could not "
            "run, so this tells you nothing about them."
        )
        print(
            "Run again after the quota resets before drawing any "
            "conclusion about drift."
        )

    if completed_samples == 0:
        pass

    elif unstable_count == 0:
        print(
            f"\nAcross the {completed_samples} answer(s) that did run, "
            "verdicts and scores held steady."
        )
    else:
        print(
            f"\n{unstable_count} instability signal(s) found. The same "
            "answer is being graded differently on different runs, each "
            "time with a confident explanation. Grounding the evaluator "
            "in reference material is justified."
        )

    print(
        "\nNote: 'missing concepts VARIED' matters most. Those strings "
        "drive probe selection and the final report, so if they move, "
        "the whole interview moves with them.\n"
    )


if __name__ == "__main__":
    main()
