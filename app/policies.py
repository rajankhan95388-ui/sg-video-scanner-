PLATFORMS = {"facebook", "instagram", "youtube"}

def validate_platform(platform: str) -> str:
    value = platform.strip().lower()
    if value not in PLATFORMS:
        raise ValueError("platform must be facebook, instagram, or youtube")
    return value
