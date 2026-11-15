import uuid
from datetime import date
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Perfil, Rol, Usuario, UsuarioPerfil

ESTADO_ACTIVO = "activo"


class UsuarioRepository:
    """Acceso a datos de usuarios y de su rol (usuario_perfil → perfiles → roles)."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def buscar_por_correo_o_usuario(self, identificador: str) -> Usuario | None:
        """Busca por correo si el identificador contiene '@'; si no, por nombre de usuario."""
        if "@" in identificador:
            condicion = func.lower(Usuario.correo) == identificador.lower()
        else:
            condicion = Usuario.nombre_usuario == identificador
        resultado = await self.db.execute(select(Usuario).where(condicion))
        return resultado.scalar_one_or_none()

    async def buscar_por_id(self, id_usuario: uuid.UUID) -> Usuario | None:
        return await self.db.get(Usuario, id_usuario)

    async def obtener_rol_activo(self, id_usuario: uuid.UUID) -> str | None:
        """Retorna el nombre del rol del perfil vigente más reciente del usuario, o None."""
        hoy = date.today()
        consulta = (
            select(Rol.nombre_rol)
            .join(Perfil, Perfil.id_rol == Rol.id_rol)
            .join(UsuarioPerfil, UsuarioPerfil.id_perfil == Perfil.id_perfil)
            .where(
                UsuarioPerfil.id_usuario == id_usuario,
                UsuarioPerfil.fecha_inicio <= hoy,
                or_(UsuarioPerfil.fecha_fin.is_(None), UsuarioPerfil.fecha_fin >= hoy),
                Perfil.estado == ESTADO_ACTIVO,
                Rol.estado == ESTADO_ACTIVO,
            )
            .order_by(UsuarioPerfil.fecha_inicio.desc())
            .limit(1)
        )
        resultado = await self.db.execute(consulta)
        return resultado.scalar_one_or_none()
