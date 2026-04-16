import json
from models import AssessmentInput
from logic import compare_assessments

# ה-JSON המדויק שסופק
raw_json_data = {
    "status": "success",
    "candidate": "Ittay Namet",
    "analysis_result": {
        "candidate_name": "Ittay Namet",
        "match_percentage": 70,
        "detailed_scores": {
            "Fluent_Communication": 8,
            "Punctuality": 5,
            "Integrity_Reliability": 8,
            "Career_Stability": 10,
            "Efficiency_Agility": 7,
            "High_Energy_Motivation": 7,
            "Adaptability_Inclusion": 6,
            "Target_Age_Group": 10,
            "Clean_Record": 5,
            "Team_Player": 8,
            "Active_Listening": 5,
            "Customer_Centricity": 5,
            "O": 7
        },
        "summary": "איתי נמט מפגין יציבות תעסוקתית מרשימה ביותר...",
        "sources": [
            "https://il.linkedin.com/in/ittai-namet-9583b045",
            "https://www.facebook.com/inamet/",
            "https://www.facebook.com/inamet/videos/1121993119103039/"
        ],
        "recommendation": "Proceed"
    }
}

def run_demonstration():
    print("--- טעינת נתונים מ-JSON ---")
    # יצירת אובייקט AssessmentInput מה-JSON (וילדציה אוטומטית של Pydantic)
    social_data = AssessmentInput(**raw_json_data)
    
    # נדמה נתונים נוספים מהצ'אט לצורך השוואה (עם שינויים קלים)
    chat_json_data = raw_json_data.copy()
    chat_json_data["analysis_result"]["detailed_scores"]["Punctuality"] = 10 # שינוי משמעותי
    chat_data = AssessmentInput(**chat_json_data)
    
    print(f"Candidate: {social_data.candidate}")
    print(f"Match Percentage: {social_data.analysis_result.match_percentage}%")
    print("-" * 30)
    
    # הרצת לוגיקת ההשוואה
    score, has_gap, gaps = compare_assessments(social_data, chat_data)
    
    print(f"Unified Score: {score}")
    print(f"Significant Gap Found: {has_gap}")
    
    if gaps:
        print("Gaps Details:")
        for gap in gaps:
            print(f" - {gap}")
    else:
        print("No significant gaps found.")

if __name__ == "__main__":
    run_demonstration()
