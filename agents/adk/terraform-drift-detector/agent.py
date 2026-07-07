import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from pydantic import BaseModel, Field

load_dotenv()


class DriftReview(BaseModel):
    drift_detected: bool = Field(
        description="True when the Terraform refresh-only plan shows infrastructure drift."
    )
    findings: list[str] = Field(
        description="Short slugs for drift findings, e.g. 'bucket-label-drift', 'iam-drift', 'no-drift'."
    )
    evidence: list[str] = Field(
        description="Exact Terraform plan lines or resource addresses that support each finding."
    )
    severity: str = Field(
        description="One of: none, low, medium, high, critical."
    )
    discord_message: str = Field(
        description="A concise Discord-ready message summarizing detected drift or confirming no drift."
    )


root_agent = Agent(
    name="terraform_drift_detector",
    model=os.getenv("MODEL", "gemini-2.5-flash"),
    instruction=(
        "You review Terraform refresh-only plan output for infrastructure drift. "
        "A no-drift plan usually says the real remote objects still match the "
        "configuration, no changes are needed, or no differences were found. "
        "If no drift is present, set drift_detected to false, severity to none, "
        "findings to ['no-drift'], and keep evidence short. "
        "If drift is present, set drift_detected to true and cite exact resource "
        "addresses or plan lines as evidence. Focus on remote object changes, "
        "deleted resources, IAM changes, public access, networking exposure, "
        "security-sensitive changes, and production-impacting drift. "
        "Do not invent findings. The discord_message must be concise and actionable."
    ),
    output_schema=DriftReview,
    output_key="drift_review",
)
