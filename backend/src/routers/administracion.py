
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.schemas.auth import TokenPayload
from src.schemas.usuario import (
    UsuarioAdminCreate,
    UsuarioAdminCreateResponse,
)
from src.schemas.administracion import (
    UsuarioActualizarRequest,
    PerfilAsignarRequest,
    UsuarioListadoResponse,
    UsuarioListadoItem,
)
from src.security.auth_depends import requiere_admin_db
from src.services.administracion_service import (
    AdministracionService,
)


router = APIRouter(
    prefix="/administracion",
    tags=["Administración"],
)


@router.get(
    "/",
    summary="Acceso administrativo",
    description="Comprueba el acceso exclusivo para administradores.",
)
async def acceso_administrativo(
    usuario: TokenPayload = Depends(requiere_admin_db),
):
    return {
        "mensaje": "Acceso autorizado.",
        "usuario": usuario.sub,
        "rol": usuario.rol,
    }


@router.get(
    "/roles",
    summary="Listar roles",
    description="Obtiene los roles disponibles en el sistema.",
)
async def listar_roles(
    solo_activos: bool = Query(default=True),
    db: AsyncSession = Depends(get_db),
    usuario: TokenPayload = Depends(requiere_admin_db),
):
    servicio = AdministracionService(db)
    return await servicio.listar_roles(solo_activos=solo_activos)


@router.post(
    "/usuarios",
    response_model=UsuarioAdminCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description=(
        "Registra un usuario, asigna su perfil y crea "
        "el registro laboral cuando corresponde."
    ),
)
async def registrar_usuario(
    datos: UsuarioAdminCreate,
    db: AsyncSession = Depends(get_db),
    usuario: TokenPayload = Depends(requiere_admin_db),
):
    servicio = AdministracionService(db)
    return await servicio.registrar_usuario(datos)


@router.get(
    "/usuarios",
    response_model=UsuarioListadoResponse,
    summary="Listar usuarios",
)
async def listar_usuarios(
    pagina: int = Query(default=1, ge=1),
    por_pagina: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    usuario: TokenPayload = Depends(requiere_admin_db),
):
    servicio = AdministracionService(db)
    return await servicio.listar_usuarios(
        pagina=pagina,
        por_pagina=por_pagina,
    )


@router.get(
    "/usuarios/{id_usuario}",
    response_model=UsuarioListadoItem,
    summary="Consultar usuario por ID",
)
async def obtener_usuario_por_id(
    id_usuario: UUID,
    db: AsyncSession = Depends(get_db),
    usuario: TokenPayload = Depends(requiere_admin_db),
):
    servicio = AdministracionService(db)
    return await servicio.obtener_usuario_por_id(id_usuario)


@router.put(
    "/usuarios/{id_usuario}",
    response_model=UsuarioListadoItem,
    summary="Actualizar usuario",
)
async def actualizar_usuario(
    id_usuario: UUID,
    datos: UsuarioActualizarRequest,
    db: AsyncSession = Depends(get_db),
    usuario: TokenPayload = Depends(requiere_admin_db),
):
    servicio = AdministracionService(db)
    return await servicio.actualizar_usuario(id_usuario, datos)


@router.post(
    "/usuarios/{id_usuario}/perfiles",
    response_model=UsuarioListadoItem,
    status_code=status.HTTP_200_OK,
    summary="Cambiar rol de usuario",
    description=(
        "Finaliza el perfil activo anterior y crea uno nuevo. "
        "Conserva el historial y crea el registro laboral "
        "cuando el nuevo rol es trabajador."
    ),
)
async def cambiar_rol_usuario(
    id_usuario: UUID,
    datos: PerfilAsignarRequest,
    db: AsyncSession = Depends(get_db),
    usuario: TokenPayload = Depends(requiere_admin_db),
):
    servicio = AdministracionService(db)
    return await servicio.cambiar_rol_usuario(
        id_usuario,
        datos,
    )
