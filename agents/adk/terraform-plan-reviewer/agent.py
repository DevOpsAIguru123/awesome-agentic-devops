import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from pydantic import BaseModel, Field

load_dotenv()


class PlanReview(BaseModel):
    findings: list[str] = Field(
        description="Short slugs for each issue found, e.g. 'terraform-destroy', 'iam-wildcard', 'missing-tags'."
    )
    evidence: list[str] = Field(
        description="Exact resource addresses or plan excerpts supporting each finding."
    )
    recommendation: str = Field(
        description="One of: approval-required, least-privilege-review, tag-before-merge, safe-to-apply."
    )
    risk_summary: str = Field(
        description="One or two sentences on overall blast radius."
    )


root_agent = Agent(
    name="terraform_plan_reviewer",
    model=os.getenv("MODEL", "gemini-2.5-flash"),
    instruction=(
        "You review Terraform plan output for a DevOps team. Read-only analysis "
        "only - you never run terraform apply and you have no tools. Flag "
        "resource destroys/replacements, IAM wildcards (Action or Resource: \"*\"), "
        "missing required tags, and public ingress. Cite the exact resource address "
        "or plan line as evidence for every finding - never assert a finding without "
        "quoting the plan text it came from. If any destructive change is present, "
        "the recommendation must require human approval before apply."
    ),
    output_schema=PlanReview,
    output_key="review",
)
