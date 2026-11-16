import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.contracts import ScanReport
from app.media_engine import MAX_BYTES, probe_media, sha256_file
from app.policies import validate_platform

app = FastAPI(
    title="SG Video Scanner — Phase 1 Media Engine",
    description="Independent creator tool. Metadata intake only; not a policy verdict."
)

@app.get("/health")
def health():
    return {
        "ok": True,
        "phase": "1",
        "status": "metadata_only"
    }

@app.post("/scan", response_model=ScanReport)
async def scan(
    platform: str = Form(...),
    video: UploadFile = File(...)
):
    try:
        platform = validate_platform(platform)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    suffix = Path(video.filename or "upload.bin").suffix[:10]
    temp_path = None
    size = 0

    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix
        ) as temp:
            temp_path = Path(temp.name)

            while True:
                chunk = await video.read(1024 * 1024)
                if not chunk:
                    break

                size += len(chunk)

                if size > MAX_BYTES:
                    raise HTTPException(
                        status_code=413,
                        detail="File exceeds 500 MB limit"
                    )

                temp.write(chunk)

        digest = sha256_file(temp_path)
        meta = probe_media(temp_path)

        return ScanReport(
            status="metadata_only",
            platform=platform,
            filename=video.filename or "upload.bin",
            sha256=digest,
            duration_seconds=meta.get("duration_seconds"),
            width=meta.get("width"),
            height=meta.get("height"),
            note=(
                "This phase extracts a file hash and available media "
                "metadata only. It does not perform AI moderation, OCR, "
                "speech recognition, copyright matching, or monetization prediction."
            )
        )

    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)
        await video.close()
