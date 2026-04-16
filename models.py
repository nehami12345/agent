from pydantic import BaseModel
from typing import List, Dict

# --- Input Models ---

class AssessmentInput(BaseModel):
    source: str  # "social_analysis" or "chat_interaction"
    metrics: Dict[str, int]  # e.g., {"patience": 90, "communication": 85}
    behavioral_traits: List[str]
    raw_score: int

# --- Output Models ---

class InterviewQuestion(BaseModel):
    question: str
    reasoning: str

class DiscrepancyAnalysis(BaseModel):
    has_significant_gap: bool
    gap_description: str

class FinalAssessmentOutput(BaseModel):
    unified_score: int
    profile_summary: str
    discrepancy_analysis: DiscrepancyAnalysis
    interviewer_guide: List[InterviewQuestion]
