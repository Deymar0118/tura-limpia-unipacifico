
"""
Inicializa los roles del sistema y el usuario Administrador principal.

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
from src.models import Perfil, Rol, Usuario
from src.schemas.auth import RolEnum
from src.security.password import hashear_password


async def obtener_o_crear_rol(
    db: AsyncSession,
    nombre_rol: str,
) -> Rol:
    """Obtiene o crea un rol."""

    rol = (
        await db.execute(
            select(Rol).where(Rol.nombre_rol == nombre_rol)
        )
    ).scalar_one_or_none()

    if not rol:
        rol = Rol(
            nombre_rol=nombre_rol,
            estado="activo",
        )
        db.add(rol)
        await db.flush()
        print(f"Rol creado: {nombre_rol}")

    return rol


async def main() -> None:
    load_dotenv()

    correo = os.getenv("ADMIN_CORREO", "").strip().lower()
    password = os.getenv("ADMIN_PASSWORD", "")
    nombre_usuario = os.getenv(
        "ADMIN_USUARIO", "admin"
    ).strip().lower()

    if not correo or len(password) < 8 or not nombre_usuario:
        sys.exit(
            "Define ADMIN_CORREO, ADMIN_PASSWORD "
            "(mínimo 8 caracteres) y ADMIN_USUARIO en .env"
        )

    try:
        async with AsyncSessionLocal() as db:
            # Crear u obtener todos los roles.
            roles = {}

            for rol_enum in RolEnum:
                roles[rol_enum] = await obtener_o_crear_rol(
                    db,
                    rol_enum.value,
                )

            # Buscar administrador por correo.
            admin = (
                await db.execute(
                    select(Usuario).where(
                        Usuario.correo == correo
                    )
                )
            ).scalar_one_or_none()

            if not admin:
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
                    estado="activo",
                )

                db.add(admin)
                await db.flush()

                print(f"Administrador creado: {correo}")

            else:
                print(f"El usuario {correo} ya existe.")

            # Buscar el perfil administrador del usuario.
            perfil_admin = (
                await db.execute(
                    select(Perfil).where(
                        Perfil.id_usuario == admin.id_usuario,
                        Perfil.id_rol == roles[RolEnum.ADMIN].id_rol,
                    )
                )
            ).scalar_one_or_none()

            if not perfil_admin:
                perfil_admin = Perfil(
                    id_usuario=admin.id_usuario,
                    id_rol=roles[RolEnum.ADMIN].id_rol,
                    fecha_inicio=date.today(),
                    estado="activo",
                )

                db.add(perfil_admin)
                print("Perfil administrador asignado.")
            else:
                print("El usuario ya tiene el perfil administrador.")

            await db.commit()

            print("\nInicialización completada correctamente.")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
