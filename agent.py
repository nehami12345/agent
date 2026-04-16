import json
import os
from openai import OpenAI
from models import AssessmentInput, FinalAssessmentOutput
from logic import compare_assessments

# אתחול לקוח OpenAI (יש לוודא שמשתנה הסביבה OPENAI_API_KEY מוגדר במערכת)
client = OpenAI()

def build_system_prompt() -> str:
    """
    מגדיר את תפקיד הסוכן, חוקי הפעולה, ומונע הזיות (Anti-Hallucination).
    """
    return """
    אתה סוכן AI מומחה למשאבי אנוש ופסיכולוגיה תעסוקתית. 
    תפקידך לנתח נתונים של מועמד משני מקורות (ניתוח רשתות חברתיות ואינטראקציה בצ'אט) ולהפיק פרופיל אחוד.
    
    חוקי ברזל (Strict Rules):
    1. אל תמציא תכונות אופי או נתונים שלא הופיעו בקלט (No Hallucinations).
    2. אם סופק לך מידע על "פער משמעותי" (Significant Gap), עליך להתייחס אליו כנקודת סיכון מרכזית לראיון.
    3. נסח 2-4 שאלות ראיון התנהגותיות (Behavioral Questions) שנועדו לחקור ספציפית את הפערים שזוהו.
    4. על השאלות להיות מנוסחות כך שהמראיין האנושי יוכל להקריא אותן ישירות למועמד (לדוגמה: "ספר לי על מקרה שבו...").
    5. עליך להחזיר את התשובה בפורמט JSON מדויק שתואם לסכמה המבוקשת, ללא טקסט נוסף.
    """

def build_user_prompt(social_data: AssessmentInput, chat_data: AssessmentInput, unified_score: int, has_gap: bool, gap_details: list) -> str:
    """
    בונה את הבקשה הספציפית עבור המועמד הנוכחי, כולל הנתונים שעובדו מראש.
    """
    return f"""
    להלן נתוני המועמד שעובדו מראש:
    
    - ציון ממוצע מחושב: {unified_score}
    - האם זוהה פער משמעותי באלגוריתם: {has_gap}
    - פירוט הפערים שחושבו: {gap_details}
    
    נתוני מקור 1 (רשתות חברתיות):
    {social_data.model_dump_json(indent=2)}
    
    נתוני מקור 2 (אינטראקציית צ'אט):

        {chat_data.model_dump_json(indent=2)}
    
    אנא נתח את הנתונים והחזר את אובייקט ה-JSON הסופי בהתאם להנחיות.
    """
def generate_final_assessment(social_data: AssessmentInput, chat_data: AssessmentInput) -> FinalAssessmentOutput:
    """
    הפונקציה המרכזית: מריצה את אלגוריתם ההשוואה וקוראת ל-LLM כדי לקבל את הפלט הסופי באמצעות Structured Outputs.
    """
    # 1. הפעלת לוגיקת ההשוואה הדטרמיניסטית (Pre-Processing)
    unified_score, has_gap, gap_details = compare_assessments(social_data, chat_data)
    
    # 2. בניית ה-Prompts
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(social_data, chat_data, unified_score, has_gap, gap_details)
    
    # 3. קריאה ל-OpenAI API עם Structured Outputs (Pydantic)
    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06", # מודל התומך ב-Structured Outputs בצורה מובנית
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format=FinalAssessmentOutput,
        temperature=0.1 # טמפרטורה נמוכה לשמירה על עקביות ומניעת הזיות
    )
    
    # 4. החזרת האובייקט המובנה (Pydantic Object)
    return response.choices[0].message.parsed

# --- אזור בדיקה (טסט מקומי) ---
if __name__ == "__main__":
    import mock_data
    
    print("--- מריץ סוכן עבור מועמד עם פער (דורש API Key) ---")
    try:
        # הפעלת הסוכן על נתוני ה-Mock
        final_result = generate_final_assessment(mock_data.social_gap, mock_data.chat_gap)
        
        # הדפסת התוצאה הסופית כ-JSON קריא
        print(final_result.model_dump_json(indent=2))
        
    except Exception as e:
        print(f"שגיאה במהלך הפעלת הסוכן: {e}")
        print("אנא ודאי שמשתנה הסביבה OPENAI_API_KEY מוגדר כראוי במערכת.")
