def select_probe_strategy(evaluation):

    # Priority 1:
    # Candidate ne technically galat understanding dikhayi
    if evaluation.misconceptions:
        return {
            "strategy": "MISCONCEPTION_PROBE",
            "target": evaluation.misconceptions[0]
        }

    # Priority 2:
    # Current question ka important/core concept miss hua
    if evaluation.missing_core_concepts:
        return {
            "strategy": "CORE_GAP_PROBE",
            "target": evaluation.missing_core_concepts[0]
        }

    # Priority 3:
    # Basic answer correct hai, ab deeper understanding test karo
    if evaluation.deeper_concepts_to_probe:
        return {
            "strategy": "DEPTH_PROBE",
            "target": evaluation.deeper_concepts_to_probe[0]
        }

    # Priority 4:
    # Koi obvious gap nahi mila → application test karo
    return {
        "strategy": "APPLICATION_PROBE",
        "target": "practical application of the concept"
    }