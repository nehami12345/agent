from models import AssessmentInput

# --- מקרה 1: מועמד עקבי (אין פערים משמעותיים) ---
social_consistent = AssessmentInput(
    source="social_analysis",
    metrics={"patience": 85, "communication": 80},
    behavioral_traits=["Friendly", "Polite", "Responsive"],
    raw_score=82
)

chat_consistent = AssessmentInput(
    source="chat_interaction",
    metrics={"patience": 80, "communication": 85},
    behavioral_traits=["Responsive", "Direct", "Polite"],
    raw_score=83
)

# --- מקרה 2: מועמד עם פער (דורש בירור בראיון) ---
social_gap = AssessmentInput(
    source="social_analysis",
    metrics={"patience": 90, "communication": 85},
    behavioral_traits=["Calm", "Articulate", "Patient"],
    raw_score=88
)

chat_gap = AssessmentInput(
    source="chat_interaction",
    metrics={"patience": 40, "communication": 60},  # פער עצום בסבלנות ובתקשורת
    behavioral_traits=["Impatient", "Short answers", "Rude"],
    raw_score=50
)