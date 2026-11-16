
from fastapi import APIRouter, Depends

from src.schemas.auth import RolEnum, TokenPayload
from src.security.auth_depends import requiere_rol


router = APIRouter(
    prefix="/administracion",
    tags=["Administración"],
)


@router.get(
    "/",
    summary="Acceso administrativo",
    description="Endpoint protegido exclusivo para administradores.",
)
async def acceso_administrativo(
    usuario: TokenPayload = Depends(
        requiere_rol(RolEnum.ADMIN)
    ),
):
    return {
        "mensaje": "Acceso autorizado.",
        "usuario": usuario.sub,
        "rol": usuario.rol,
    }
