import hmac
import hashlib

from app.core.config import settings


def validate_tribute_signature(payload: bytes, signature: str | None) -> bool:
    if not signature:
        return False

    expected = hmac.new(
        settings.TRIBUTE_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected, signature)
