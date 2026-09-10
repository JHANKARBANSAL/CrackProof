"""
Report ka DATA banata hai. Kuch print nahi karta.

Ye isliye alag hai ki aage UI banegi. Terminal aur UI dono ko wahi
data chahiye - bas dikhane ka tareeka alag hoga. Agar calculate aur
print ek hi jagah hote, to UI ko sab dobara likhna padta.

    reporting.py  ->  data banao       (ye file)
    display.py    ->  terminal pe dikhao
    (aage)        ->  UI pe dikhao

Use:
    from reporting import build_report
    report = build_report(current_batch)
"""

from depth_aggregator import aggregate_depth_evidence
from assessment_metrics import calculate_batch_metrics
from assessment_generator import generate_final_assessment


def build_report(current_batch):
    """
    Ek batch ka poora report data banata hai.

    Return karta hai ek dictionary:

        {
          "ok": True/False,          # report ban paayi ya nahi
          "message": "...",          # ok False ho to wajah
          "topic": "DBMS",
          "depth_profile": {...},
          "metrics": {...},
          "assessment": FinalAssessment ya None,
          "assessment_error": "..." ya None,
          "limited_evidence": True/False,
        }

    Sirf woh turns aate hain jo interview_history mein hain, isliye
    adhoora ya bina-jawab wala sawaal report mein kabhi nahi aayega.
    """

    # Assessment ke liye kam se kam ek poora answer chahiye.
    # Yahan rok dene se koi bhi caller khaali batch pe LLM call
    # nahi kara sakta.
    if not current_batch:
        return {
            "ok": False,
            "message": (
                "At least one completed answer is required "
                "to generate an assessment."
            ),
        }

    depth_profile = aggregate_depth_evidence(current_batch)

    # Batch apna topic khud rakhta hai, isliye baad mein topic
    # badalne se ye report galat label nahi legi.
    batch_topic = current_batch[0]["topic"]

    metrics = calculate_batch_metrics(current_batch, depth_profile)

    # Narrative assessment LLM se aata hai, isliye fail ho sakta hai.
    # Uske fail hone se upar wale deterministic numbers nahi jaane
    # chahiye - isliye alag se pakad rahe hain.
    assessment = None
    assessment_error = None

    try:
        assessment = generate_final_assessment(
            topic=batch_topic,
            interview_turns=current_batch,
            depth_profile=depth_profile,
            metrics=metrics
        )

    except Exception as error:
        assessment_error = str(error)

    return {
        "ok": True,
        "message": "",
        "topic": batch_topic,
        "depth_profile": depth_profile,
        "metrics": metrics,
        "assessment": assessment,
        "assessment_error": assessment_error,
        "limited_evidence": metrics["questions_answered"] < 5,
    }
