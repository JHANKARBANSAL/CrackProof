EVIDENCE_TYPES = [
    "FUNDAMENTAL",
    "REASONING",
    "APPLICATION",
    "EDGE_CASE"
]

# Weight of each status when scoring a dimension.
STATUS_WEIGHTS = {
    "DEMONSTRATED": 1.0,
    "PARTIALLY_DEMONSTRATED": 0.5,
    "NOT_DEMONSTRATED": 0.0
}


def merge_statuses(statuses):
    """
    Collapse several statuses reported for the SAME dimension in the
    SAME question into one observation.

    The prompt already tells Gemini to return each dimension at most
    once per question, but the model can still slip. We must never
    count those as independent tests, and we must not silently keep
    only the first one, because that would hide conflicting evidence.

    Identical statuses collapse to themselves. Conflicting statuses
    resolve conservatively to PARTIALLY_DEMONSTRATED.
    """

    unique_statuses = set(statuses)

    if len(unique_statuses) == 1:
        return statuses[0]

    return "PARTIALLY_DEMONSTRATED"


def classify_evidence(tested: int, evidence_score: float) -> str:
    """
    Convert repeated observations into an evidence-strength label.

    IMPORTANT:
    These are prototype engineering heuristics, not scientifically
    validated psychometric or assessment thresholds.
    """

    if tested == 0:
        return "NOT_TESTED"

    # A single observation is not enough to claim a stable pattern.
    if tested == 1:

        if evidence_score == 1.0:
            return "POSITIVE_EVIDENCE"

        if evidence_score == 0.5:
            return "PARTIAL_EVIDENCE"

        return "NEGATIVE_EVIDENCE"

    if evidence_score >= 0.75:
        return "STRONG_EVIDENCE"

    if evidence_score >= 0.50:
        return "MIXED_EVIDENCE"

    return "WEAK_EVIDENCE"


def aggregate_depth_evidence(interview_turns):
    """
    Aggregate depth evidence from multiple interview turns.

    interview_turns should contain the turns we want to assess,
    for example the latest 5-question batch.

    A dimension appears in evaluation.evidence ONLY when the question
    actually tested it, so tested == 0 means "never asked about",
    not "failed".

    Every question contributes AT MOST ONE observation per dimension,
    so `tested` can never exceed len(interview_turns).
    """

    summary = {}

    for evidence_type in EVIDENCE_TYPES:
        summary[evidence_type] = {
            "tested": 0,
            "demonstrated": 0,
            "partially_demonstrated": 0,
            "not_demonstrated": 0,
            "evidence_examples": []
        }

    for turn in interview_turns:

        evaluation = turn["evaluation"]

        # -------------------------------------------------
        # STEP 1: group this ONE question's evidence by
        # dimension, so duplicates cannot become two tests.
        # -------------------------------------------------

        grouped = {}

        for evidence in evaluation.evidence:

            evidence_type = evidence.evidence_type

            # Defensive check against unknown dimensions
            if evidence_type not in summary:
                continue

            if evidence_type not in grouped:
                grouped[evidence_type] = []

            grouped[evidence_type].append(evidence)

        # -------------------------------------------------
        # STEP 2: fold each dimension into ONE observation
        # -------------------------------------------------

        for evidence_type, items in grouped.items():

            statuses = [item.status for item in items]

            merged_status = merge_statuses(statuses)

            # Keep every explanation so traceability is not lost
            explanations = [
                item.evidence_from_answer for item in items
            ]

            merged_explanation = " | ".join(explanations)

            data = summary[evidence_type]

            # One question -> exactly one test of this dimension
            data["tested"] += 1

            if merged_status == "DEMONSTRATED":
                data["demonstrated"] += 1

            elif merged_status == "PARTIALLY_DEMONSTRATED":
                data["partially_demonstrated"] += 1

            else:
                data["not_demonstrated"] += 1

            data["evidence_examples"].append({
                "question_number": turn["question_number"],
                "question": turn["question"],
                "status": merged_status,
                "evidence_from_answer": merged_explanation,

                # True when the model returned this dimension more
                # than once for this question and we merged it.
                "merged_from_duplicates": len(items) > 1,
                "original_statuses": statuses
            })

    # -----------------------------------------------------
    # STEP 3: score and classify each dimension
    # -----------------------------------------------------

    for evidence_type in EVIDENCE_TYPES:

        data = summary[evidence_type]

        tested = data["tested"]

        if tested == 0:
            data["evidence_score"] = 0.0

        else:
            weighted = (
                data["demonstrated"]
                * STATUS_WEIGHTS["DEMONSTRATED"]

                + data["partially_demonstrated"]
                * STATUS_WEIGHTS["PARTIALLY_DEMONSTRATED"]
            )

            data["evidence_score"] = weighted / tested

        data["level"] = classify_evidence(
            tested=tested,
            evidence_score=data["evidence_score"]
        )

    return summary
