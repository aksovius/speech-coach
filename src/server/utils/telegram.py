import hashlib
import hmac
import json
from datetime import datetime, timezone
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
        auth_date = int(parsed.get("auth_date", 0))
        current_time = datetime.now(timezone.utc).timestamp()
        if abs(current_time - auth_date) > 900:
            print(
                f"Auth date validation failed: {current_time - auth_date} seconds difference"
            )
            return False

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
