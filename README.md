# SG Video Scanner MVP v3
Independent creator-protection tool; not affiliated with Meta, Instagram or YouTube.

This developer pack implements a FastAPI intake scaffold, SHA-256 hashing, basic MP4/WebM signature checks, three separate platform policy packs, normalized signal/report contracts, conservative status mapping and tests.

**It is not an AI scanner.** No frame decoding, OCR, ASR, moderation inference, audio fingerprinting, Content ID or Meta Rights Manager matching occurs. The upload endpoint explicitly returns `not_scanned`; it does not save the video for later processing.

Run: `pip install -r requirements.txt` then `uvicorn app.main:app --reload`. API docs at `/docs`.

Production blockers: private object storage, malware scanning, sandboxed media workers, durable queue, real analysis adapters, licensed fingerprint provider, authentication, quotas, retention/deletion, policy specialist review and security testing. Never guarantee safety, monetization or copyright clearance.
