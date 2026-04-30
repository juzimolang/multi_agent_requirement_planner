from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class RequirementInput(BaseModel):
    text: str = Field(..., min_length=1, description="Original requirement text from the user or product owner.")


class RequirementAnalysis(BaseModel):
    core_goal: str
    target_users: List[str]
    pain_points: List[str]
    explicit_requirements: List[str]
    implicit_requirements: List[str]
    open_questions: List[str]
    acceptance_criteria: List[str]


class ArchitecturePlan(BaseModel):
    overview: str
    major_components: List[str]
    api_draft: List[str]
    data_model_notes: List[str]
    implementation_steps: List[str]
    integration_points: List[str]


class RiskAssessment(BaseModel):
    technical_risks: List[str]
    product_risks: List[str]
    security_privacy_risks: List[str]
    operational_risks: List[str]
    mitigations: List[str]


class TestPlan(BaseModel):
    unit_tests: List[str]
    integration_tests: List[str]
    edge_cases: List[str]
    manual_review_checks: List[str]


class ReviewDocument(BaseModel):
    title: str
    requirement_analysis: RequirementAnalysis
    architecture_plan: ArchitecturePlan
    risk_assessment: RiskAssessment
    test_plan: TestPlan
    final_summary: str


class PlanRequest(BaseModel):
    requirement: str = Field(..., min_length=1)
    mock: bool = Field(default=True, description="Use deterministic mock agents instead of OpenAI.")


class PlanResponse(BaseModel):
    markdown: str
    document: ReviewDocument
