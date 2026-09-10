"""
Terminal pe cheezein dikhata hai. Kuch calculate nahi karta.

Ye developer view hai. Jab UI banegi, tab wahi data leke apne
tareeke se dikha degi - ye file badalni nahi padegi.

    reporting.py  ->  data banao
    display.py    ->  terminal pe dikhao   (ye file)
"""


def show_reference(sources):
    """Kaunse reference tukde use hue, number aur link ke saath."""

    if not sources:
        print("\nReference: none found "
              "(evaluating without grounding)")
        return

    print("\nReference used:")

    for source in sources:
        print(
            "  [" + str(source["number"]) + "]",
            source["title"],
            "- section \"" + source["section"] + "\""
        )
        if source["url"]:
            print("      ", source["url"])


def show_evaluation(evaluation, sources):
    """Ek answer ka poora evaluation."""

    # Number se asli source dhoondhne ke liye
    source_by_number = {}
    for source in sources:
        source_by_number[source["number"]] = source

    # Kaunsi baat ka kaunsa source number hai
    citation_for = {}
    for citation in evaluation.citations:
        citation_for[citation.claim.strip().lower()] = (
            citation.source_number
        )

    def print_with_source(item):
        """Ek line print karo, source mile to uske saath."""

        print("-", item)

        number = citation_for.get(item.strip().lower())

        # URL hamare apne data se aata hai, model se nahi
        source = source_by_number.get(number)

        if source:
            print(
                "    source:", source["title"],
                "- section \"" + source["section"] + "\""
            )
            if source["url"]:
                print("   ", source["url"])

    print("\n========== EVALUATION ==========")

    print("Verdict:", evaluation.verdict)
    print("Correctness:", evaluation.correctness_score, "/10")
    print("Depth:", evaluation.depth_score, "/10")

    print("\nCorrect Points:")
    show_list(evaluation.correct_points)

    print("\nMissing Core Concepts:")
    if evaluation.missing_core_concepts:
        for concept in evaluation.missing_core_concepts:
            print_with_source(concept)
    else:
        print("- None")

    print("\nDeeper Concepts To Probe:")
    show_list(evaluation.deeper_concepts_to_probe)

    print("\nMisconceptions:")
    if evaluation.misconceptions:
        for misconception in evaluation.misconceptions:
            print_with_source(misconception)
    else:
        print("- None")

    print("\nDepth Evidence:")

    if evaluation.evidence:
        for evidence in evaluation.evidence:
            print(
                f"- {evidence.evidence_type}: "
                f"{evidence.status}"
            )
            print("  Evidence:", evidence.evidence_from_answer)
    else:
        print("- No relevant evidence collected")

    print("\nReasoning:")
    print(evaluation.reasoning)


def show_list(items):
    """Chhoti si madad: list dikhao, khaali ho to '- None'."""

    if items:
        for item in items:
            print("-", item)
    else:
        print("- None")


def show_probe(probe):
    """Agla probe kya hai (ye internal hai, candidate ke liye nahi)."""

    print("\n========== NEXT PROBE ==========")
    print("Strategy:", probe["strategy"])
    print("Target:", probe["target"])


def show_depth_profile(depth_profile):
    """Poore batch ka depth evidence profile."""

    print("\n========== DEPTH EVIDENCE PROFILE ==========")

    for evidence_type, data in depth_profile.items():

        print(f"\n{evidence_type}")

        print("Tested:", data["tested"])
        print("Demonstrated:", data["demonstrated"])
        print("Partially Demonstrated:", data["partially_demonstrated"])
        print("Not Demonstrated:", data["not_demonstrated"])
        print("Evidence Score:", round(data["evidence_score"], 2))
        print("Evidence Level:", data["level"])

        if data["evidence_examples"]:

            print("Evidence:")

            for example in data["evidence_examples"]:
                print(
                    f"  Q{example['question_number']}: "
                    f"{example['status']}"
                )
                print("   ", example["evidence_from_answer"])


def show_assessment(report):
    """Final assessment - numbers pehle, phir narrative."""

    metrics = report["metrics"]

    print("\n" + "=" * 50)
    print("CRACKPROOF FINAL ASSESSMENT")
    print("=" * 50)

    print("\nTopic:", report["topic"])
    print("Questions Answered:", metrics["questions_answered"])

    print("\nOverall Readiness:")
    print(metrics["overall_readiness"])
    print("(reflects performance in this interview batch only)")

    print("\nAverage Correctness:")
    print(f"{metrics['average_correctness_score']:.2f} / 10")

    print("\nAverage Depth:")
    print(f"{metrics['average_depth_score']:.2f} / 10")

    verdicts = metrics["verdict_distribution"]

    print("\nVerdicts:")
    print("Correct:", verdicts["CORRECT"])
    print("Partially Correct:", verdicts["PARTIALLY_CORRECT"])
    print("Incorrect:", verdicts["INCORRECT"])

    print("\nEvidence Coverage:")
    print(
        f"{metrics['tested_dimension_count']} / "
        f"{metrics['total_dimensions']} depth dimensions tested"
    )

    # Ye deterministic hai, isliye LLM fail ho jaye tab bhi dikhega.
    if report["limited_evidence"]:

        answered = metrics["questions_answered"]

        print(
            "\nNote: this assessment is based on "
            f"{answered} completed "
            f"{'answer' if answered == 1 else 'answers'}, "
            "so less evidence was collected."
        )
        print(
            "Fewer answers means less evidence, "
            "not poorer performance."
        )

    if report["assessment_error"]:
        print("\nThe narrative assessment could not be generated.")
        print("Reason:", report["assessment_error"])
        print(
            "Your completed interview, depth profile and the "
            "metrics above have been preserved."
        )

    assessment = report["assessment"]

    if assessment is not None:

        sections = [
            ("Demonstrated Strengths:",
             assessment.demonstrated_strengths),
            ("Developing Areas:",
             assessment.developing_areas),
            ("Recurring Knowledge Gaps:",
             assessment.recurring_knowledge_gaps),
            ("Persistent Misconceptions:",
             assessment.persistent_misconceptions),
            ("Insufficiently Tested Areas:",
             assessment.insufficiently_tested_areas),
        ]

        for heading, items in sections:
            print(f"\n{heading}")
            show_list(items)

        print("\nRecommended Revision Topics:")

        if assessment.recommended_revision_topics:
            number = 0
            for item in assessment.recommended_revision_topics:
                number = number + 1
                print(f"{number}. {item}")
        else:
            print("- None")

        print("\nSummary:")
        print(assessment.summary)

    print("\n" + "=" * 50)


def show_report(report):
    """Poora batch report - depth profile aur assessment."""

    if not report["ok"]:
        print("\n" + report["message"])
        return

    show_depth_profile(report["depth_profile"])
    show_assessment(report)
