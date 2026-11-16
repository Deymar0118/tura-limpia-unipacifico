
"""Inicializa los roles del sistema (RF-01) y el usuario Administrador principal.

Uso desde backend:
    python seed_admin.py

Lee ADMIN_CORREO, ADMIN_PASSWORD y ADMIN_USUARIO desde .env.
Puede ejecutarse varias veces sin duplicar registros.
"""

import asyncio
import os
import sys
from datetime import date

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import AsyncSessionLocal, engine
from src.models import Perfil, Rol, Usuario, UsuarioPerfil
from src.schemas.auth import RolEnum
from src.security.password import hashear_password


async def obtener_o_crear_perfil(
    db: AsyncSession,
    nombre_rol: str
) -> Perfil:
    """Obtiene o crea el rol y su perfil asociado."""

    rol = (
        await db.execute(
            select(Rol).where(Rol.nombre_rol == nombre_rol)
        )
    ).scalar_one_or_none()

    if not rol:
        rol = Rol(nombre_rol=nombre_rol)
        db.add(rol)
        await db.flush()
        print(f"Rol creado: {nombre_rol}")

    perfil = (
        await db.execute(
            select(Perfil).where(Perfil.id_rol == rol.id_rol)
        )
    ).scalars().first()

    if not perfil:
        perfil = Perfil(id_rol=rol.id_rol)
        db.add(perfil)
        await db.flush()
        print(f"Perfil creado para el rol: {nombre_rol}")

    return perfil


async def main() -> None:
    load_dotenv()

    correo = os.getenv("ADMIN_CORREO", "").strip()
    password = os.getenv("ADMIN_PASSWORD", "")
    nombre_usuario = os.getenv("ADMIN_USUARIO", "admin").strip()

    if not correo or len(password) < 8 or not nombre_usuario:
        sys.exit(
            "Define ADMIN_CORREO, ADMIN_PASSWORD "
            "(mínimo 8 caracteres) y ADMIN_USUARIO en .env"
        )

    try:
        async with AsyncSessionLocal() as db:

            # Crear u obtener los perfiles de todos los roles.
            perfiles = {}

            for rol in RolEnum:
                perfiles[rol] = await obtener_o_crear_perfil(
                    db, rol.value
                )

            # Buscar administrador por correo.
            admin = (
                await db.execute(
                    select(Usuario).where(Usuario.correo == correo)
                )
            ).scalar_one_or_none()

            if not admin:

                # Comprobar que el nombre de usuario esté disponible.
                usuario_existente = (
                    await db.execute(
                        select(Usuario).where(
                            Usuario.nombre_usuario == nombre_usuario
                        )
                    )
                ).scalar_one_or_none()

                if usuario_existente:
                    raise ValueError(
                        f"El nombre de usuario '{nombre_usuario}' "
                        "ya está registrado."
                    )

                admin = Usuario(
                    nombres="Administrador",
                    apellidos="Principal",
                    nombre_completo="Administrador Principal",
                    nombre_usuario=nombre_usuario,
                    correo=correo,
                    password_hash=hashear_password(password),
                )

                db.add(admin)
                await db.flush()

                print(f"Administrador creado: {correo}")

            else:
                print(f"El usuario {correo} ya existe.")

            # Comprobar si ya tiene asignado el perfil administrador.
            asignacion = (
                await db.execute(
                    select(UsuarioPerfil).where(
                        UsuarioPerfil.id_usuario == admin.id_usuario,
                        UsuarioPerfil.id_perfil
                        == perfiles[RolEnum.ADMIN].id_perfil,
                    )
                )
            ).scalar_one_or_none()

            if not asignacion:
                db.add(
                    UsuarioPerfil(
                        id_usuario=admin.id_usuario,
                        id_perfil=perfiles[RolEnum.ADMIN].id_perfil,
                        fecha_inicio=date.today(),
                    )
                )
                print("Rol administrador asignado.")
            else:
                print("El usuario ya tiene el rol administrador.")

            await db.commit()

            print("\nInicialización completada correctamente.")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
