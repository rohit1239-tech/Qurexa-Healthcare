def generate_clinical_summary(visit):
    """
    This is a placeholder AI engine.
    Later this can be replaced by LLM / ML models.
    """

    previous_visits = visit.previous_visits()

    if not previous_visits.exists():
        return (
            f"First visit for patient. "
            f"Reported symptoms: {visit.symptoms}. "
            f"Clinical notes: {visit.clinical_notes}."
        )

    history = []
    for v in previous_visits[:3]:  # last 3 visits
        history.append(v.symptoms)

    history_text = " | ".join(history)

    summary = (
        f"Patient has prior history of: {history_text}. "
        f"Current symptoms: {visit.symptoms}. "
        f"Doctor notes: {visit.clinical_notes}."
    )

    return summary
