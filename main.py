import hashlib
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.policies import PACKS, evaluate
from app.contracts import Report, Source

app = FastAPI(title="SG Video Scanner API", version="0.4.0")
MAX_BYTES = 500 * 1024 * 1024
ALLOWED = {".mp4", ".mov", ".m4v", ".webm"}

def detect_container(header: bytes):
    if len(header) >= 8 and header[4:8] == b"ftyp": return "mp4_family"
    if header.startswith(bytes.fromhex("1a45dfa3")): return "webm_matroska"
    return None

@app.get("/health")
def health():
    return {"status":"ok","version":"0.4.0","analysis_engine":"not_connected"}

@app.get("/v1/platforms")
def platforms():
    return {"platforms":sorted(PACKS)}

@app.get("/v1/policies/{platform}")
def get_policy(platform: str):
    key = platform.lower()
    if key not in PACKS: raise HTTPException(404,"unknown platform")
    return PACKS[key]

@app.post("/v1/scans", status_code=202)
async def create_scan(platform: str = Form(...), video: UploadFile = File(...)):
    key = platform.lower().strip()
    if key not in PACKS: raise HTTPException(400,"platform must be facebook, instagram, or youtube")
    filename = Path(video.filename or "upload").name
    if Path(filename).suffix.lower() not in ALLOWED: raise HTTPException(415,"unsupported extension")
    digest, size, header = hashlib.sha256(), 0, b""
    try:
        while chunk := await video.read(1024 * 1024):
            if not header: header = chunk[:32]
            size += len(chunk)
            if size > MAX_BYTES: raise HTTPException(413,"maximum upload size is 500 MB")
            digest.update(chunk)
        if size == 0: raise HTTPException(400,"empty upload")
        container = detect_container(header)
        if not container: raise HTTPException(415,"unrecognized MP4/MOV or WebM file signature")
        p = PACKS[key]
        report = Report(platform=key, overall_status="not_scanned",
          media={"filename":filename,"size_bytes":size,"sha256":digest.hexdigest(),"container_detected":container},
          policy_version=p["version"], policy_sources=[Source(**s) for s in p["sources"]],
          findings=evaluate(key, []),
          disclaimer="Only upload intake and SHA-256 hashing occurred. No video/audio/OCR/AI/copyright analysis was performed.")
        return {"accepted":True,"state":"intake_only","report":report.model_dump(mode="json"),
                "notice":"No scan was run; media workers and analysis adapters are not connected."}
    finally:
        await video.close()
