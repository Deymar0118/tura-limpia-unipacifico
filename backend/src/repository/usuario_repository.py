
import uuid
from datetime import date

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Perfil, Rol, Usuario, UsuarioPerfil


ESTADO_ACTIVO = "activo"


class UsuarioRepository:
    """Acceso a datos de usuarios y sus roles."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def buscar_por_correo_o_usuario(
        self,
        identificador: str,
    ) -> Usuario | None:
        """Busca por correo o nombre de usuario."""

        identificador = identificador.strip()

        if "@" in identificador:
            condicion = (
                func.lower(Usuario.correo)
                == identificador.lower()
            )
        else:
            condicion = (
                func.lower(Usuario.nombre_usuario)
                == identificador.lower()
            )

        resultado = await self.db.execute(
            select(Usuario).where(condicion)
        )

        return resultado.scalar_one_or_none()

    async def buscar_por_id(
        self,
        id_usuario: uuid.UUID,
    ) -> Usuario | None:
        return await self.db.get(Usuario, id_usuario)

    async def buscar_por_correo(
        self,
        correo: str,
    ) -> Usuario | None:
        resultado = await self.db.execute(
            select(Usuario).where(
                func.lower(Usuario.correo) == correo.lower()
            )
        )
        return resultado.scalar_one_or_none()

    async def buscar_por_nombre_usuario(
        self,
        nombre_usuario: str,
    ) -> Usuario | None:
        resultado = await self.db.execute(
            select(Usuario).where(
                func.lower(Usuario.nombre_usuario)
                == nombre_usuario.lower()
            )
        )
        return resultado.scalar_one_or_none()

    async def obtener_perfil_por_rol(
        self,
        nombre_rol: str,
    ) -> Perfil | None:
        """Obtiene un perfil activo asociado a un rol activo."""

        resultado = await self.db.execute(
            select(Perfil)
            .join(Rol, Perfil.id_rol == Rol.id_rol)
            .where(
                Rol.nombre_rol == nombre_rol,
                Rol.estado == ESTADO_ACTIVO,
                Perfil.estado == ESTADO_ACTIVO,
            )
            .limit(1)
        )

        return resultado.scalar_one_or_none()

    async def crear_usuario_ciudadano(
        self,
        nombres: str,
        apellidos: str,
        nombre_usuario: str,
        correo: str,
        password_hash: str,
        telefono: str | None,
        perfil: Perfil,
    ) -> Usuario:
        """Crea el usuario y le asigna el perfil ciudadano."""

        usuario = Usuario(
            nombres=nombres,
            apellidos=apellidos,
            nombre_completo=f"{nombres} {apellidos}",
            nombre_usuario=nombre_usuario,
            correo=correo,
            password_hash=password_hash,
            telefono=telefono,
        )

        self.db.add(usuario)
        await self.db.flush()

        asignacion = UsuarioPerfil(
            id_usuario=usuario.id_usuario,
            id_perfil=perfil.id_perfil,
            fecha_inicio=date.today(),
        )

        self.db.add(asignacion)
        await self.db.flush()

        return usuario

    async def obtener_rol_activo(
        self,
        id_usuario: uuid.UUID,
    ) -> str | None:
        """Retorna el rol vigente más reciente del usuario."""

        hoy = date.today()

        consulta = (
            select(Rol.nombre_rol)
            .join(Perfil, Perfil.id_rol == Rol.id_rol)
            .join(
                UsuarioPerfil,
                UsuarioPerfil.id_perfil == Perfil.id_perfil,
            )
            .where(
                UsuarioPerfil.id_usuario == id_usuario,
                UsuarioPerfil.fecha_inicio <= hoy,
                or_(
                    UsuarioPerfil.fecha_fin.is_(None),
                    UsuarioPerfil.fecha_fin >= hoy,
                ),
                Perfil.estado == ESTADO_ACTIVO,
                Rol.estado == ESTADO_ACTIVO,
            )
            .order_by(UsuarioPerfil.fecha_inicio.desc())
            .limit(1)
        )

        resultado = await self.db.execute(consulta)

        return resultado.scalar_one_or_none()
