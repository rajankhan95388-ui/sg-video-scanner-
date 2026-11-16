from app.policies import PACKS, evaluate

def test_three_independent_platforms():
    assert set(PACKS) == {"facebook","instagram","youtube"}
    assert PACKS["facebook"] is not PACKS["instagram"]

def test_no_signals_never_pass():
    for platform in PACKS:
        findings = evaluate(platform, [])
        assert all(f["status"] in {"not_run","not_verified"} for f in findings)

def test_youtube_content_id_stays_unverified():
    signal = type("S", (), {"kind":"licensed_fingerprint_match","status":"not_detected","confidence":0.99,"evidence":[]})()
    findings = evaluate("youtube", [signal])
    item = next(f for f in findings if f["finding_id"] == "YT_CONTENT_ID")
    assert item["status"] == "not_verified"


def test_unconfigured_adapter_returns_not_run():
    import asyncio
    from app.adapters import UnconfiguredAdapter
    result = asyncio.run(UnconfiguredAdapter("ocr", ["ocr_text_signal"]).analyze("private-ref"))
    assert result.state == "not_configured"
    assert result.signals[0].status == "not_run"
