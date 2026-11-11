from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth import verificar_token
from src.schemas.auth import RolEnum, TokenPayload

bearer_scheme = HTTPBearer()


def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> TokenPayload:
    token = credentials.credentials
    payload = verificar_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token incorrecto",
        )

    return TokenPayload(
        sub=payload["sub"],
        roles=payload["roles"],
        exp=payload["exp"],
    )


def requiere_rol(*roles_permitidos: RolEnum):
    def verificar(usuario: TokenPayload = Depends(obtener_usuario_actual)):
        if not usuario.roles or not any(rol in roles_permitidos for rol in usuario.roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado",
            )
        return usuario
    return verificar
