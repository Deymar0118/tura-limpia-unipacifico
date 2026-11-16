
import uuid
from datetime import date

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.models.usuario import Perfil, Rol, Usuario
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


async def obtener_rol_actual_db(
    usuario: TokenPayload,
    db: AsyncSession,
) -> RolEnum:
    """
    Consulta en PostgreSQL el rol vigente del usuario.

    No confía en el rol almacenado en el JWT.
    Comprueba el estado del usuario, perfil y rol.
    """

    try:
        id_usuario = uuid.UUID(usuario.sub)

    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identidad de usuario inválida.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    hoy = date.today()

    consulta = (
        select(Rol.nombre_rol)
        .select_from(Usuario)
        .join(
            Perfil,
            Perfil.id_usuario == Usuario.id_usuario,
        )
        .join(
            Rol,
            Rol.id_rol == Perfil.id_rol,
        )
        .where(
            Usuario.id_usuario == id_usuario,
            Usuario.estado == "activo",
            Perfil.estado == "activo",
            Perfil.fecha_inicio <= hoy,
            or_(
                Perfil.fecha_fin.is_(None),
                Perfil.fecha_fin > hoy,
            ),
            Rol.estado == "activo",
        )
        .limit(1)
    )

    resultado = await db.execute(consulta)
    nombre_rol = resultado.scalar_one_or_none()

    if nombre_rol is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo o sin perfil vigente.",
        )

    try:
        return RolEnum(nombre_rol)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario tiene un rol no reconocido.",
        )


def requiere_rol(*roles_permitidos: RolEnum):
    """
    Restringe el acceso según el rol vigente en PostgreSQL.

    Los permisos no dependen del rol almacenado en el JWT.
    """

    async def verificar(
        usuario: TokenPayload = Depends(obtener_usuario_actual),
        db: AsyncSession = Depends(get_db),
    ) -> TokenPayload:

        rol_actual = await obtener_rol_actual_db(usuario, db)

        if rol_actual not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado.",
            )

        return TokenPayload(
            sub=usuario.sub,
            rol=rol_actual,
        )

    return verificar


async def requiere_admin_db(
    usuario: TokenPayload = Depends(obtener_usuario_actual),
    db: AsyncSession = Depends(get_db),
) -> TokenPayload:
    """
    Comprueba en PostgreSQL que el usuario siga activo
    y tenga un perfil administrativo vigente.
    """

    rol_actual = await obtener_rol_actual_db(usuario, db)

    if rol_actual != RolEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador.",
        )

    return TokenPayload(
        sub=usuario.sub,
        rol=rol_actual,
    )
