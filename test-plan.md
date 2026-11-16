# Test plan
Unit: platform packs isolated; missing adapter never passes; subjective detected signal becomes manual_review; proprietary/account checks remain not_verified; confidence bounded; evidence timestamps valid; every source ID resolves.

Upload: reject unknown platform, unsupported extension, empty/oversize file, invalid signature; stable SHA-256 across chunk sizes; basename-only filename; no persistent media file. Add malformed/truncated media and parser resource-abuse tests when workers are added.

Pipeline: missing audio => audio checks not_run; preserve OCR/ASR timestamps; partial failures become partial/failed; retries idempotent; reports retain policy snapshots.

Acceptance: every finding has status, severity, explanation, evidence or reason unavailable, remediation and source. Intake-only upload never claims a scan or pass.
