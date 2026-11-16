# Engine architecture
Upload gateway -> private quarantine storage -> signature/MIME/duration validation + malware scan -> durable queue -> isolated media workers -> normalized signals -> independent platform policy engine -> immutable report.

Shared adapters: scene/frame sampling with source timestamps; OCR; ASR transcript segments; audio classification and licensed fingerprint provider; visual similarity against creator-owned/licensed corpus; safety classifier. Every adapter returns `detected|not_detected|not_run|not_verified`, confidence, timestamped evidence and limitations.

Worker states: uploaded -> quarantined -> validated -> queued -> extracting -> analyzing -> policy_evaluation -> report_ready. Failures are rejected/partial/failed, never pass. Account-level checks remain not_verified without authorized account data. Proprietary matching stays not_verified without a licensed integration.

Production security: private object storage, random keys, malware scanning, sandboxed parsers, size/duration/codec limits, CPU/RAM/time quotas, signed short-lived URLs, encryption, auth, rate limits, audit logs, secrets management and deletion/retention workflow.
