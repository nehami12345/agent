from pydantic import BaseModel
from typing import List, Dict

# --- Input Models ---

class DetailedScores(BaseModel):
    Fluent_Communication: int
    Punctuality: int
    Integrity_Reliability: int
    Career_Stability: int
    Efficiency_Agility: int
    High_Energy_Motivation: int
    Adaptability_Inclusion: int
    Target_Age_Group: int
    Clean_Record: int
    Team_Player: int
    Active_Listening: int
    Customer_Centricity: int
    O: int

class AnalysisResult(BaseModel):
    candidate_name: str
    match_percentage: int
    detailed_scores: DetailedScores
    summary: str
    sources: List[str]
    recommendation: str

class AssessmentInput(BaseModel):
    status: str
    candidate: str
    analysis_result: AnalysisResult

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