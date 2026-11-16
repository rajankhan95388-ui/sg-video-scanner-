from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class Evidence(BaseModel):
    kind: str
    description: str
    start_seconds: float | None = Field(default=None, ge=0)
    end_seconds: float | None = Field(default=None, ge=0)

class Signal(BaseModel):
    signal_id: str
    kind: str
    status: Literal["detected", "not_detected", "not_run", "not_verified"]
    confidence: float | None = Field(default=None, ge=0, le=1)
    evidence: list[Evidence] = []
    limitations: list[str] = []

class Source(BaseModel):
    source_id: str
    title: str
    url: str
    source_revision: str
    checked_on: str
    validation_status: Literal["verified", "partial", "pending_validation"]

class Finding(BaseModel):
    finding_id: str
    category: str
    title: str
    status: Literal["pass", "risk_detected", "manual_review", "not_verified", "not_run"]
    severity: Literal["critical", "high", "medium", "low", "info", "unknown"] = "unknown"
    confidence: float | None = Field(default=None, ge=0, le=1)
    explanation: str
    evidence: list[Evidence] = []
    remediation: list[str] = []
    source_ids: list[str] = []
    limitations: list[str] = []

class Report(BaseModel):
    model_config = ConfigDict(extra="forbid")
    report_version: str = "1.2.0"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    platform: Literal["facebook", "instagram", "youtube"]
    overall_status: Literal["not_scanned", "processing", "risk_detected", "manual_review", "partial", "failed"]
    media: dict
    policy_version: str
    policy_sources: list[Source]
    signals: list[Signal] = []
    findings: list[Finding] = []
    disclaimer: str
