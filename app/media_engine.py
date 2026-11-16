import hashlib
import shutil
import subprocess
from pathlib import Path
from typing import Any

MAX_BYTES = 500 * 1024 * 1024
MAX_DURATION_SECONDS = 20 * 60
MAX_FRAMES = 8

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def probe_media(path: Path) -> dict[str, Any]:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return {"available": False, "reason": "ffprobe is not installed"}
    command = [
        ffprobe, "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,width,height",
        "-of", "json", str(path)
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                timeout=20, check=True)
        import json
        data = json.loads(result.stdout or "{}")
        duration = None
        try:
            duration = float(data.get("format", {}).get("duration"))
        except (TypeError, ValueError):
            pass
        video = next((s for s in data.get("streams", [])
                      if s.get("codec_type") == "video"), {})
        return {
            "available": True,
            "duration_seconds": duration,
            "width": video.get("width"),
            "height": video.get("height"),
        }
    except Exception as exc:
        return {"available": False, "reason": str(exc)}

def sample_frames(path: Path, output_dir: Path, duration: float | None) -> list[str]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg or not duration or duration <= 0 or duration > MAX_DURATION_SECONDS:
        return []
    output_dir.mkdir(parents=True, exist_ok=True)
    count = min(MAX_FRAMES, max(1, int(duration // 15) + 1))
    saved = []
    for index in range(count):
        at = min(max(0.1, duration * (index + 0.5) / count), duration - 0.1)
        target = output_dir / f"frame_{index + 1:02d}.jpg"
        command = [ffmpeg, "-v", "error", "-ss", str(at), "-i", str(path),
                   "-frames:v", "1", "-vf", "scale='min(1280,iw)':-2",
                   "-y", str(target)]
        try:
            subprocess.run(command, capture_output=True, timeout=15, check=True)
            if target.exists() and target.stat().st_size:
                saved.append(str(target))
        except Exception:
            continue
    return saved
