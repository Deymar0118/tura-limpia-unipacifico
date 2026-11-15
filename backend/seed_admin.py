"""Inicializa los roles del sistema (RF-01) y el usuario Administrador principal.

Uso (desde la carpeta backend, con las tablas ya creadas):
    python seed_admin.py

Lee ADMIN_CORREO, ADMIN_PASSWORD y, opcionalmente, ADMIN_USUARIO del archivo .env.
Se puede ejecutar varias veces: solo crea lo que todavía no existe.
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


async def obtener_o_crear_perfil(db: AsyncSession, nombre_rol: str) -> Perfil:
    """Retorna el perfil asociado al rol, creando el rol y el perfil si no existen."""
    rol = (await db.execute(select(Rol).where(Rol.nombre_rol == nombre_rol))).scalar_one_or_none()
    if not rol:
        rol = Rol(nombre_rol=nombre_rol)
        db.add(rol)
        await db.flush()
        print(f"Rol creado: {nombre_rol}")

    perfil = (await db.execute(select(Perfil).where(Perfil.id_rol == rol.id_rol))).scalars().first()
    if not perfil:
        perfil = Perfil(id_rol=rol.id_rol)
        db.add(perfil)
        await db.flush()
    return perfil


async def main() -> None:
    load_dotenv()
    correo = os.getenv("ADMIN_CORREO", "").strip()
    password = os.getenv("ADMIN_PASSWORD", "")
    nombre_usuario = os.getenv("ADMIN_USUARIO", "admin").strip()

    if not correo or len(password) < 8:
        sys.exit("Define ADMIN_CORREO y ADMIN_PASSWORD (mínimo 8 caracteres) en el archivo .env")

    async with AsyncSessionLocal() as db:
        perfiles = {}
        for rol in RolEnum:
            perfiles[rol] = await obtener_o_crear_perfil(db, rol.value)

        existe = (await db.execute(select(Usuario).where(Usuario.correo == correo))).scalar_one_or_none()
        if existe:
            print(f"El administrador {correo} ya existe; no se modifica.")
        else:
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
            db.add(UsuarioPerfil(
                id_usuario=admin.id_usuario,
                id_perfil=perfiles[RolEnum.ADMIN].id_perfil,
                fecha_inicio=date.today(),
            ))
            print(f"Administrador creado: {correo} (usuario: {nombre_usuario})")

        await db.commit()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
