from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError
from src.schemas.auth import RolEnum, TokenPayload
from src.security.tokens import verificar_token

bearer_scheme = HTTPBearer(auto_error=False)


def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> TokenPayload:
    """Valida el token Bearer de la petición y retorna los datos del usuario autenticado."""
    payload = verificar_token(credentials.credentials) if credentials else None
    try:
        if payload:
            return TokenPayload(sub=payload["sub"], rol=payload["rol"])
    except ValidationError:
        pass
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )


def requiere_rol(*roles_permitidos: RolEnum):
    """Restringe un endpoint a los roles indicados (permisos según el rol, RF-06)."""
    def verificar(usuario: TokenPayload = Depends(obtener_usuario_actual)) -> TokenPayload:
        if usuario.rol not in roles_permitidos:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
        return usuario
    return verificar
