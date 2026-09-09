from pydantic import BaseModel

from prompts import FINAL_ASSESSMENT_PROMPT
from llm_client import ask_llm


class FinalAssessment(BaseModel):
    """
    Narrative half of the report only.

    Deliberately contains NO numeric fields: every number in the final
    report is computed in assessment_metrics.py and must not be
    reproducible, or overridable, by the model.
    """

    demonstrated_strengths: list[str]

    developing_areas: list[str]

    recurring_knowledge_gaps: list[str]

    persistent_misconceptions: list[str]

    insufficiently_tested_areas: list[str]

    recommended_revision_topics: list[str]

    summary: str


def _build_questions_block(interview_turns) -> str:
    """
    Render the per-question evidence given to the model.

    probe_strategy and probe_target are internal adaptive-interview
    machinery and are deliberately NOT included, so they cannot leak
    into the candidate-facing report.
    """

    lines = []

    for turn in interview_turns:

        evaluation = turn["evaluation"]

        lines.append(f"Question {turn['question_number']}:")
        lines.append(f"  Question: {turn['question']}")
        lines.append(f"  Candidate answer: {turn['transcript']}")
        lines.append(f"  Verdict: {evaluation.verdict}")
        lines.append(
            f"  Correctness score: {evaluation.correctness_score}/10"
        )
        lines.append(
            f"  Depth score: {evaluation.depth_score}/10"
        )

        lines.append(
            "  Correct points: "
            + (", ".join(evaluation.correct_points) or "none")
        )

        lines.append(
            "  Missing core concepts: "
            + (", ".join(evaluation.missing_core_concepts) or "none")
        )

        lines.append(
            "  Misconceptions: "
            + (", ".join(evaluation.misconceptions) or "none")
        )

        lines.append("")

    return "\n".join(lines)


def _build_depth_profile_block(depth_profile) -> str:

    lines = []

    for evidence_type, data in depth_profile.items():

        if data["tested"] == 0:
            lines.append(
                f"{evidence_type}: NOT_TESTED "
                "(the interview never asked about this dimension; "
                "this is not a weakness)"
            )
            continue

        lines.append(
            f"{evidence_type}: level={data['level']}, "
            f"tested={data['tested']}, "
            f"demonstrated={data['demonstrated']}, "
            f"partially_demonstrated="
            f"{data['partially_demonstrated']}, "
            f"not_demonstrated={data['not_demonstrated']}, "
            f"evidence_score={round(data['evidence_score'], 2)}"
        )

        for example in data["evidence_examples"]:
            lines.append(
                f"  Q{example['question_number']} "
                f"{example['status']}: "
                f"{example['evidence_from_answer']}"
            )

    return "\n".join(lines)


def _build_metrics_block(metrics) -> str:

    lines = [
        f"Questions answered: {metrics['questions_answered']}",
        "Average correctness score: "
        f"{metrics['average_correctness_score']}/10",
        "Average depth score: "
        f"{metrics['average_depth_score']}/10",
        f"Verdict distribution: {metrics['verdict_distribution']}",
        "Depth dimensions tested: "
        f"{metrics['tested_dimension_count']} of "
        f"{metrics['total_dimensions']} "
        f"({', '.join(metrics['tested_dimensions']) or 'none'})",
        "Depth dimensions NOT tested: "
        f"{', '.join(metrics['untested_dimensions']) or 'none'}",
    ]

    lines.append("")
    lines.append("Raw missing-concept occurrences across the batch:")

    if metrics["knowledge_gap_records"]:
        for record in metrics["knowledge_gap_records"]:
            lines.append(
                f"  Q{record['question_number']}: {record['concept']}"
            )
    else:
        lines.append("  none")

    lines.append("")
    lines.append("Raw misconception occurrences across the batch:")

    if metrics["misconception_records"]:
        for record in metrics["misconception_records"]:
            lines.append(
                f"  Q{record['question_number']}: "
                f"{record['misconception']}"
            )
    else:
        lines.append("  none")

    return "\n".join(lines)


def generate_final_assessment(
    topic,
    interview_turns,
    depth_profile,
    metrics
):
    """
    Build grounded structured input, send it to the model, return the
    parsed narrative assessment, or None if the model failed.

    This function performs no metric computation of its own. Every
    number it shows the model was already computed deterministically.
    """

    prompt = FINAL_ASSESSMENT_PROMPT.format(
        topic=topic,
        questions_block=_build_questions_block(interview_turns),
        depth_profile_block=_build_depth_profile_block(depth_profile),
        metrics_block=_build_metrics_block(metrics),
        overall_readiness=metrics["overall_readiness"]
    )

    return ask_llm(prompt, schema=FinalAssessment)
