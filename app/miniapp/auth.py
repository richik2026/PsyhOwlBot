import hashlib
import hmac
from urllib.parse import parse_qsl


def verify_init_data(init_data: str, bot_token: str) -> bool:
    """Verify Telegram WebApp initData signature."""

    data = dict(parse_qsl(init_data, strict_parsing=False))
    received_hash = data.pop("hash", None)

    if not received_hash:
        return False

    data_check_string = "\n".join(
        f"{key}={value}"
        for key, value in sorted(data.items())
    )

    secret_key = hmac.new(
        b"WebAppData",
        bot_token.encode(),
        hashlib.sha256,
    ).digest()

    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(
        calculated_hash,
        received_hash,
    )
