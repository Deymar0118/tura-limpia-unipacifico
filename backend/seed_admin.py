
"""
Inicializa los roles del sistema y el superadministrador principal.

Uso desde backend:
    python seed_admin.py

Variables:
    ADMIN_CORREO
    ADMIN_PASSWORD
    ADMIN_USUARIO

La contraseña solo es obligatoria cuando se crea el administrador.
Nunca se sobrescribe la contraseña de un usuario existente.
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
    """Obtiene un rol existente o crea uno nuevo."""

    resultado = await db.execute(
        select(Rol).where(Rol.nombre_rol == nombre_rol)
    )

    rol = resultado.scalar_one_or_none()

    if rol is None:
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

    correo = os.getenv(
        "ADMIN_CORREO", ""
    ).strip().lower()

    password = os.getenv("ADMIN_PASSWORD", "")

    nombre_usuario = os.getenv(
        "ADMIN_USUARIO", "admin"
    ).strip().lower()

    if not correo or not nombre_usuario:
        sys.exit(
            "ERROR: Define ADMIN_CORREO y ADMIN_USUARIO."
        )

    try:
        async with AsyncSessionLocal() as db:
            try:
                # 1. Crear u obtener los roles.
                roles = {}

                for rol_enum in RolEnum:
                    roles[rol_enum] = await obtener_o_crear_rol(
                        db,
                        rol_enum.value,
                    )

                # 2. Buscar al administrador por correo.
                resultado = await db.execute(
                    select(Usuario).where(
                        Usuario.correo == correo
                    )
                )

                admin = resultado.scalar_one_or_none()

                if admin is None:
                    # La contraseña solo se exige para crear
                    # una cuenta que todavía no existe.
                    if len(password) < 12:
                        raise ValueError(
                            "ADMIN_PASSWORD debe tener al menos "
                            "12 caracteres para crear el administrador."
                        )

                    if len(password.encode("utf-8")) > 72:
                        raise ValueError(
                            "ADMIN_PASSWORD supera el límite "
                            "de 72 bytes de bcrypt."
                        )

                    resultado = await db.execute(
                        select(Usuario).where(
                            Usuario.nombre_usuario == nombre_usuario
                        )
                    )

                    usuario_existente = resultado.scalar_one_or_none()

                    if usuario_existente is not None:
                        raise ValueError(
                            f"El nombre de usuario '{nombre_usuario}' "
                            "ya pertenece a otra cuenta."
                        )

                    admin = Usuario(
                        nombres="Administrador",
                        apellidos="Principal",
                        nombre_completo="Administrador Principal",
                        nombre_usuario=nombre_usuario,
                        correo=correo,
                        password_hash=hashear_password(password),
                        estado="activo",
                        es_superadministrador=True,
                    )

                    db.add(admin)
                    await db.flush()

                    print(f"Superadministrador creado: {correo}")

                else:
                    print(
                        f"El administrador {correo} ya existe. "
                        "Se conservará su contraseña."
                    )

                    # No permitir que la inicialización cree
                    # un segundo superadministrador.
                    resultado = await db.execute(
                        select(Usuario).where(
                            Usuario.es_superadministrador.is_(True),
                            Usuario.id_usuario != admin.id_usuario,
                        )
                    )

                    otro_superadmin = resultado.scalar_one_or_none()

                    if otro_superadmin is not None:
                        raise ValueError(
                            "Ya existe otro superadministrador. "
                            "No se modificó la cuenta existente."
                        )

                    admin.es_superadministrador = True

                # 3. Comprobar el perfil administrador.
                resultado = await db.execute(
                    select(Perfil).where(
                        Perfil.id_usuario == admin.id_usuario,
                        Perfil.id_rol == roles[RolEnum.ADMIN].id_rol,
                    )
                )

                perfil_admin = resultado.scalar_one_or_none()

                if perfil_admin is None:
                    perfil_admin = Perfil(
                        id_usuario=admin.id_usuario,
                        id_rol=roles[RolEnum.ADMIN].id_rol,
                        fecha_inicio=date.today(),
                        estado="activo",
                    )

                    db.add(perfil_admin)

                    print("Perfil administrador asignado.")
                else:
                    print("El perfil administrador ya existe.")

                await db.commit()

                print(
                    "\nInicialización completada correctamente."
                )

            except Exception:
                await db.rollback()
                raise

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
