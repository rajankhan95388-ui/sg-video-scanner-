# API
- `GET /health`: reports analysis engine connection state.
- `GET /v1/platforms`: supported platform identifiers.
- `GET /v1/policies/{platform}`: independent rule pack and source provenance.
- `POST /v1/scans` multipart (`platform`, `video`): 500 MB max, extension/signature validation, SHA-256. Current response is `state=intake_only`, `overall_status=not_scanned`; media is not persisted and no scan is performed.

Production additions not implemented: `GET /v1/scans/{id}`, `GET /v1/scans/{id}/report`, `DELETE /v1/scans/{id}`, durable job queue, upload-session URL and private object storage.
