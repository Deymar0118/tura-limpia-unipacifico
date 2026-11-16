from datetime import datetime, timedelta, timezone
import jwt
from src.core.config import get_settings


def crear_access_token(id_usuario: str, rol: str) -> str:
    """Genera un JWT de acceso firmado con el id del usuario y su rol."""
    settings = get_settings()
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": id_usuario, "rol": rol, "exp": expira}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def verificar_token(token: str) -> dict | None:
    """Decodifica y valida un JWT. Retorna el payload o None si es inválido o expiró."""
    settings = get_settings()
    try:
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            options={"require": ["sub", "rol", "exp"]},
        )
    except jwt.InvalidTokenError:
        return None
