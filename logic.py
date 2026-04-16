from models import AssessmentInput
from typing import Tuple, List
import mock_data

def compare_assessments(social_data: AssessmentInput, chat_data: AssessmentInput) -> Tuple[int, bool, List[str]]:
    """
    משווה בין שני האבחונים ומחזיר:
    1. ציון ממוצע משוקלל (unified_score)
    2. האם יש פער משמעותי (has_significant_gap)
    3. רשימת תיאורים של הפערים שנמצאו (gap_details)
    """
    # 1. חישוב הציון הממוצע על בסיס match_percentage
    unified_score = (social_data.analysis_result.match_percentage + chat_data.analysis_result.match_percentage) // 2
    
    has_significant_gap = False
    gap_details = []
    
    # 2. מעבר על כל המדדים (Detailed Scores) והשוואה ביניהם
    # אנו משתמשים ב-dict() כדי לעבור על השדות של המודל
    social_metrics = social_data.analysis_result.detailed_scores.model_dump()
    chat_metrics = chat_data.analysis_result.detailed_scores.model_dump()
    
    for metric_name, social_value in social_metrics.items():
        if metric_name in chat_metrics:
            chat_value = chat_metrics[metric_name]
            
            # חישוב הפער המוחלט (ללא מינוס)
            gap = abs(social_value - chat_value)
            
            # הגדרת סף לפער משמעותי (למשל פער של 3 נקודות בסולם של 1-10)
            if gap >= 3:
                has_significant_gap = True
                gap_details.append(
                    f"פער במדד '{metric_name}': רשתות ({social_value}) מול צ'אט ({chat_value})"
                )
                
    return unified_score, has_significant_gap, gap_details

# --- אזור בדיקה (טסט מקומי) ---
if __name__ == "__main__":
    print("--- בודק מועמד עקבי ---")
    score1, gap_exists1, details1 = compare_assessments(mock_data.social_consistent, mock_data.chat_consistent)
    print(f"Score: {score1}, Has Gap: {gap_exists1}, Details: {details1}")
    
    print("\n--- בודק מועמד עם פער (בעייתי) ---")
    score2, gap_exists2, details2 = compare_assessments(mock_data.social_gap, mock_data.chat_gap)
    print(f"Score: {score2}, Has Gap: {gap_exists2}, Details: {details2}")