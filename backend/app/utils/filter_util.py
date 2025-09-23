from typing import Optional

def normalize_filter(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    if not value or value.lower() == "null":
        return None
    return value