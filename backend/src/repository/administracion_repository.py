
from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.usuario import Perfil, Rol, Usuario
from src.models.personal import Trabajador


class AdministracionRepository:
    """Consultas y operaciones de persistencia para HU-01."""

    @staticmethod
    async def buscar_por_correo(
        db: AsyncSession,
        correo: str,
    ) -> Usuario | None:
        resultado = await db.execute(
            select(Usuario).where(
                func.lower(Usuario.correo) == correo.lower()
            )
        )
        return resultado.scalar_one_or_none()

    @staticmethod
    async def buscar_por_nombre_usuario(
        db: AsyncSession,
        nombre_usuario: str,
    ) -> Usuario | None:
        resultado = await db.execute(
            select(Usuario).where(
                func.lower(Usuario.nombre_usuario)
                == nombre_usuario.lower()
            )
        )
        return resultado.scalar_one_or_none()

    @staticmethod
    async def buscar_por_documento(
        db: AsyncSession,
        documento: str,
    ) -> Usuario | None:
        resultado = await db.execute(
            select(Usuario).where(Usuario.documento == documento)
        )
        return resultado.scalar_one_or_none()

    @staticmethod
    async def obtener_rol_por_id(
        db: AsyncSession,
        rol_id: int,
    ) -> Rol | None:
        resultado = await db.execute(
            select(Rol).where(
                Rol.id_rol == rol_id,
                Rol.estado == "activo",
            )
        )
        return resultado.scalar_one_or_none()

    @staticmethod
    async def listar_roles(
        db: AsyncSession,
        solo_activos: bool = True,
    ) -> list[Rol]:
        """Obtiene los roles registrados en la base de datos."""

        consulta = select(Rol).order_by(Rol.id_rol.asc())

        if solo_activos:
            consulta = consulta.where(Rol.estado == "activo")

        resultado = await db.execute(consulta)
        return list(resultado.scalars().all())

    @staticmethod
    async def crear_usuario_con_perfil(
        db: AsyncSession,
        *,
        nombres: str,
        apellidos: str,
        nombre_usuario: str,
        correo: str,
        password_hash: str,
        documento: str,
        rol: Rol,
        fecha_inicio: date,
        perfil_activo: bool,
        cargo: str | None = None,
    ) -> tuple[Usuario, Perfil, Trabajador | None]:
        """Crea usuario, perfil y trabajador cuando corresponde."""

        estado = "activo" if perfil_activo else "inactivo"

        usuario = Usuario(
            nombres=nombres,
            apellidos=apellidos,
            nombre_completo=f"{nombres} {apellidos}",
            nombre_usuario=nombre_usuario,
            correo=correo,
            password_hash=password_hash,
            documento=documento,
            estado="activo",
        )

        db.add(usuario)
        await db.flush()

        perfil = Perfil(
            id_usuario=usuario.id_usuario,
            id_rol=rol.id_rol,
            fecha_inicio=fecha_inicio,
            fecha_fin=None,
            estado=estado,
        )

        db.add(perfil)
        await db.flush()

        trabajador = None

        if rol.nombre_rol.strip().lower() == "trabajador":
            if not cargo:
                raise ValueError(
                    "El cargo es obligatorio para el rol trabajador."
                )

            trabajador = Trabajador(
                id_perfil=perfil.id_perfil,
                cargo=cargo,
                estado=estado,
            )
            db.add(trabajador)
            await db.flush()

        return usuario, perfil, trabajador

    @staticmethod
    async def listar_usuarios(
        db: AsyncSession,
        *,
        offset: int,
        limit: int,
    ) -> tuple[list[Usuario], int]:
        consulta_total = select(func.count()).select_from(Usuario)
        total_resultado = await db.execute(consulta_total)
        total = total_resultado.scalar_one()

        consulta = (
            select(Usuario)
            .options(
                selectinload(Usuario.perfiles).selectinload(Perfil.rol)
            )
            .order_by(Usuario.fecha_registro.desc())
            .offset(offset)
            .limit(limit)
        )

        resultado = await db.execute(consulta)
        return list(resultado.scalars().all()), total

    @staticmethod
    async def buscar_usuario_por_id(
        db: AsyncSession,
        id_usuario: UUID,
    ) -> Usuario | None:
        consulta = (
            select(Usuario)
            .options(
                selectinload(Usuario.perfiles).selectinload(Perfil.rol)
            )
            .where(Usuario.id_usuario == id_usuario)
        )
        resultado = await db.execute(consulta)
        return resultado.scalar_one_or_none()

    @staticmethod
    async def actualizar_usuario(
        db: AsyncSession,
        usuario: Usuario,
        cambios: dict,
    ) -> Usuario:
        for campo, valor in cambios.items():
            setattr(usuario, campo, valor)

        if "nombres" in cambios or "apellidos" in cambios:
            usuario.nombre_completo = (
                f"{usuario.nombres} {usuario.apellidos}"
            )

        await db.flush()
        return usuario

    @staticmethod
    async def obtener_usuario_para_cambio_perfil(
        db: AsyncSession,
        id_usuario: UUID,
    ) -> Usuario | None:
        """Bloquea la fila del usuario durante el cambio de perfil."""

        consulta = (
            select(Usuario)
            .options(
                selectinload(Usuario.perfiles).selectinload(Perfil.rol),
                selectinload(Usuario.perfiles).selectinload(
                    Perfil.trabajador
                ),
            )
            .where(Usuario.id_usuario == id_usuario)
            .with_for_update()
        )

        resultado = await db.execute(consulta)
        return resultado.scalar_one_or_none()

    @staticmethod
    async def crear_perfil(
        db: AsyncSession,
        *,
        usuario: Usuario,
        rol: Rol,
        fecha_inicio: date,
        cargo: str | None = None,
    ) -> tuple[Perfil, Trabajador | None]:
        """Crea el nuevo perfil y el trabajador si corresponde."""

        perfil = Perfil(
            id_usuario=usuario.id_usuario,
            id_rol=rol.id_rol,
            fecha_inicio=fecha_inicio,
            fecha_fin=None,
            estado="activo",
        )

        db.add(perfil)
        await db.flush()

        trabajador = None

        if rol.nombre_rol.strip().lower() == "trabajador":
            if not cargo:
                raise ValueError(
                    "El cargo es obligatorio para el rol trabajador."
                )

            trabajador = Trabajador(
                id_perfil=perfil.id_perfil,
                cargo=cargo,
                estado="activo",
            )
            db.add(trabajador)
            await db.flush()

        return perfil, trabajador
