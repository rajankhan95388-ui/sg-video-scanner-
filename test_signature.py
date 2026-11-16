from app.main import detect_container

def test_mp4():
    assert detect_container(bytes.fromhex("000000186674797069736f6d")) == "mp4_family"

def test_webm():
    assert detect_container(bytes.fromhex("1a45dfa372657374")) == "webm_matroska"

def test_unknown():
    assert detect_container(b"not-video") is None
