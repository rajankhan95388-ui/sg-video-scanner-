from pydantic import BaseModel
from typing import List, Optional

class Finding(BaseModel):
    code: str
    severity: str
    message: str
    timestamp_seconds: Optional[float] = None
    recommendation: Optional[str] = None

class ScanReport(BaseModel):
    status: str = "not_scanned"
    platform: str
    filename: str
    sha256: str
    duration_seconds: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    sampled_frames: int = 0
    findings: List[Finding] = []
    note: str = "Media metadata only; no AI policy or copyright decision was performed."
