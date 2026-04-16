from models import AssessmentInput, AnalysisResult, DetailedScores

# פונקציית עזר ליצירת נתונים עם ערכי ברירת מחדל כדי לקצר את הקוד
def create_mock_assessment(name: str, match_pct: int, scores: dict) -> AssessmentInput:
    detailed_scores = DetailedScores(
        Fluent_Communication=scores.get("Fluent_Communication", 7),
        Punctuality=scores.get("Punctuality", 7),
        Integrity_Reliability=scores.get("Integrity_Reliability", 7),
        Career_Stability=scores.get("Career_Stability", 7),
        Efficiency_Agility=scores.get("Efficiency_Agility", 7),
        High_Energy_Motivation=scores.get("High_Energy_Motivation", 7),
        Adaptability_Inclusion=scores.get("Adaptability_Inclusion", 7),
        Target_Age_Group=scores.get("Target_Age_Group", 10),
        Clean_Record=scores.get("Clean_Record", 5),
        Team_Player=scores.get("Team_Player", 7),
        Active_Listening=scores.get("Active_Listening", 7),
        Customer_Centricity=scores.get("Customer_Centricity", 7),
        O=scores.get("O", 7)
    )
    
    analysis = AnalysisResult(
        candidate_name=name,
        match_percentage=match_pct,
        detailed_scores=detailed_scores,
        summary="Test summary",
        sources=["http://test.com"],
        recommendation="Proceed"
    )
    
    return AssessmentInput(
        status="success",
        candidate=name,
        analysis_result=analysis
    )

# --- מקרה 1: מועמד עקבי (אין פערים משמעותיים) ---
social_consistent = create_mock_assessment("Test Candidate", 80, {"Punctuality": 8, "Career_Stability": 9})
chat_consistent = create_mock_assessment("Test Candidate", 82, {"Punctuality": 7, "Career_Stability": 8})

# --- מקרה 2: מועמד עם פער (דורש בירור בראיון) ---
social_gap = create_mock_assessment("Gap Candidate", 90, {"Punctuality": 10, "Career_Stability": 10})
chat_gap = create_mock_assessment("Gap Candidate", 50, {"Punctuality": 4, "Career_Stability": 5}) # פער גדול