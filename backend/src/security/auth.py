import uuid
import jwt
from datetime import datetime, timedelta, timezone
from src.core.config import get_settings

ALGORITHM = get_settings().jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = get_settings().access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = get_settings().refresh_token_expire_days

def _get_secret() -> str:
    return get_settings().jwt_secret_key


def crear_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire, "type": "access"})
    return jwt.encode(payload, _get_secret(), algorithm=ALGORITHM)


def crear_refresh_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload.update({"exp": expire, "type": "refresh", "jti": str(uuid.uuid4())})
    return jwt.encode(payload, _get_secret(), algorithm=ALGORITHM)


def verificar_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, _get_secret(), algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
