import hashlib
import hmac
import json
from typing import Any, Dict, Optional


def parse_telegram_user_data(user_param: str) -> Optional[Dict[str, Any]]:
    """
    Parses user data from the user parameter
    """
    try:
        if not user_param:
            return None

        user_data = json.loads(user_param)

        return user_data
    except Exception as e:
        print(f"Error parsing Telegram user data: {e}")
        return None


def validate_telegram_data(parsed: dict, bot_token: str) -> bool:
    try:
        received_hash = parsed.pop("hash", None)

        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))

        secret_key = hmac.new(
            key=b"WebAppData", msg=bot_token.encode(), digestmod=hashlib.sha256
        ).digest()

        calculated_hash = hmac.new(
            key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        return calculated_hash == received_hash
    except Exception as e:
        print(f"Validation error: {e}")
        return False
