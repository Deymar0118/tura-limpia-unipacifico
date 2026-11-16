
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError

from src.schemas.auth import RolEnum, TokenPayload
from src.security.tokens import verificar_token


bearer_scheme = HTTPBearer(
    auto_error=False,
    scheme_name="JWTBearer",
    description="Introduce el token JWT de acceso.",
)


def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
) -> TokenPayload:
    """Valida el JWT y obtiene la identidad del usuario."""

    payload = (
        verificar_token(credentials.credentials)
        if credentials
        else None
    )

    try:
        if payload:
            return TokenPayload(
                sub=payload["sub"],
                rol=payload["rol"],
            )

    except (ValidationError, KeyError, TypeError):
        pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def requiere_rol(*roles_permitidos: RolEnum):
    """Restringe el acceso a los roles autorizados."""

    def verificar(
        usuario: TokenPayload = Depends(obtener_usuario_actual),
    ) -> TokenPayload:

        if usuario.rol not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado.",
            )

        return usuario

    return verificar
