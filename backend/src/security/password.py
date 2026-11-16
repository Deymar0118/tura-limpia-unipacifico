import bcrypt

# bcrypt solo procesa los primeros 72 bytes de la contraseña
_BCRYPT_MAX_BYTES = 72


def hashear_password(password: str) -> str:
    """Genera el hash bcrypt de una contraseña en texto plano."""
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > _BCRYPT_MAX_BYTES:
        raise ValueError("La contraseña no puede superar los 72 bytes")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    """Compara una contraseña en texto plano con su hash bcrypt."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False
