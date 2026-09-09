from depth_aggregator import EVIDENCE_TYPES

TOTAL_DIMENSIONS = len(EVIDENCE_TYPES)

VERDICTS = [
    "CORRECT",
    "PARTIALLY_CORRECT",
    "INCORRECT"
]


def determine_readiness(
    average_correctness_score: float,
    average_depth_score: float
) -> str:
    """
    Overall label for the CURRENT five-question batch.

    IMPORTANT:
    These are PROTOTYPE ENGINEERING HEURISTICS chosen by judgment.
    They are NOT validated psychometric or assessment thresholds.
    STRONG does not mean "job ready" or "will pass interviews" — it
    describes performance in this interview batch only.

    The scores come from AnswerEvaluation, where correctness_score and
    depth_score are both constrained to 0-10, so these cutoffs are on
    the same scale.

    NOTE ON MISCONCEPTIONS:
    The original design also wanted a "no repeated serious
    misconception" condition. The project has no stable misconception
    ids or categories, only free-text strings, and exact string
    matching is not a reliable way to decide that two differently
    worded misconceptions are the same one. Rather than pretend
    otherwise, readiness is computed from correctness and depth alone.
    All misconception evidence is still preserved and passed to the
    LLM for semantic synthesis. A misconception-based readiness
    penalty is DEFERRED until misconception grouping is deterministic.
    """

    if average_correctness_score >= 7.5 and average_depth_score >= 7.0:
        return "STRONG"

    if average_correctness_score >= 5.0 and average_depth_score >= 4.5:
        return "DEVELOPING"

    return "NEEDS_IMPROVEMENT"


def calculate_batch_metrics(interview_turns, depth_profile):
    """
    Deterministic metrics for one completed batch of interview turns.

    Computation only. No LLM is involved here, and nothing in this
    module may be overridden by an LLM later in the pipeline.
    """

    questions_answered = len(interview_turns)

    # -------------------------------------------------
    # AVERAGE SCORES
    # -------------------------------------------------

    if questions_answered == 0:
        average_correctness_score = 0.0
        average_depth_score = 0.0

    else:
        correctness_total = sum(
            turn["evaluation"].correctness_score
            for turn in interview_turns
        )

        depth_total = sum(
            turn["evaluation"].depth_score
            for turn in interview_turns
        )

        average_correctness_score = round(
            correctness_total / questions_answered, 2
        )

        average_depth_score = round(
            depth_total / questions_answered, 2
        )

    # -------------------------------------------------
    # VERDICT DISTRIBUTION
    # -------------------------------------------------

    verdict_distribution = {verdict: 0 for verdict in VERDICTS}

    for turn in interview_turns:

        verdict = turn["evaluation"].verdict

        if verdict in verdict_distribution:
            verdict_distribution[verdict] += 1

    # -------------------------------------------------
    # RAW GAP AND MISCONCEPTION RECORDS
    #
    # Keep every occurrence with its question number so the report
    # stays traceable. Deliberately NO string-equality de-duplication:
    # two differently worded entries may be the same underlying gap,
    # and only semantic synthesis can tell. That grouping is the LLM's
    # job; Python's job is to preserve the raw evidence and counts.
    # -------------------------------------------------

    knowledge_gap_records = []
    misconception_records = []

    for turn in interview_turns:

        evaluation = turn["evaluation"]
        question_number = turn["question_number"]

        for concept in evaluation.missing_core_concepts:
            knowledge_gap_records.append({
                "question_number": question_number,
                "concept": concept
            })

        for misconception in evaluation.misconceptions:
            misconception_records.append({
                "question_number": question_number,
                "misconception": misconception
            })

    # -------------------------------------------------
    # EVIDENCE COVERAGE
    #
    # This is COVERAGE OF DEPTH DIMENSIONS.
    # It is NOT an assessment confidence probability, and 0.75 must
    # never be described as "75% confident".
    # -------------------------------------------------

    tested_dimensions = []
    untested_dimensions = []

    for evidence_type in EVIDENCE_TYPES:

        data = depth_profile.get(evidence_type, {})

        if data.get("tested", 0) > 0:
            tested_dimensions.append(evidence_type)

        else:
            untested_dimensions.append(evidence_type)

    coverage_ratio = round(
        len(tested_dimensions) / TOTAL_DIMENSIONS, 2
    )

    # -------------------------------------------------
    # OVERALL READINESS (deterministic, never LLM-generated)
    # -------------------------------------------------

    overall_readiness = determine_readiness(
        average_correctness_score=average_correctness_score,
        average_depth_score=average_depth_score
    )

    return {
        "questions_answered": questions_answered,
        "average_correctness_score": average_correctness_score,
        "average_depth_score": average_depth_score,
        "verdict_distribution": verdict_distribution,
        "knowledge_gap_records": knowledge_gap_records,
        "misconception_records": misconception_records,
        "tested_dimensions": tested_dimensions,
        "untested_dimensions": untested_dimensions,
        "tested_dimension_count": len(tested_dimensions),
        "total_dimensions": TOTAL_DIMENSIONS,
        "coverage_ratio": coverage_ratio,
        "overall_readiness": overall_readiness
    }
