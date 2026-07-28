"""Validated input-independent advisory models."""

from pydantic import BaseModel, Field


class PriorityAction(BaseModel):
    """One proposed remediation supported by exact scanner finding IDs."""

    finding_ids: list[str] = Field(min_length=1)
    action: str
    rationale: str
    compatibility_impact: str


class AgentReview(BaseModel):
    """Non-authoritative review returned by Claude."""

    executive_summary: str
    risk_assessment: str
    prioritized_actions: list[PriorityAction]
    attack_paths: list[str]
    verification_steps: list[str]
    limitations: list[str]
