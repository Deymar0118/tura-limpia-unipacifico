from datetime import datetime
from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.perfil import Perfil
from src.models.usuario import Usuario
from src.models.rol import Rol

class UsuarioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_usuario(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        await self.db.commit()
        await self.db.refresh(usuario)
        return usuario

    async def find_usuario_by_email(self, email: str) -> Optional[Usuario]:
        stmt = select(Usuario).where(Usuario.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_usuarios(self) -> list[Usuario]:
        stmt = select(Usuario).order_by(Usuario.nombre.asc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_all_usuarios_paginated(self, offset: int = 0, limit: int = 50) -> tuple[list[Usuario], int]:
        total_result = await self.db.execute(select(func.count()).select_from(Usuario))
        total = total_result.scalar()

        stmt = select(Usuario).order_by(Usuario.nombre.asc()).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all(), total

    async def update_usuario(self, usuario: Usuario) -> Usuario:
        await self.db.commit()
        await self.db.refresh(usuario)
        return usuario

    async def find_usuario_by_id(self, usuario_id: int) -> Optional[Usuario]:
        stmt = select(Usuario).where(Usuario.id == usuario_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_usuarios_count_by_rol(self) -> list[tuple[str, int]]:
        stmt = (
            select(Rol.nombre, func.count(Usuario.id).label("total_usuarios"))
            .outerjoin(Rol.perfiles)       
            .outerjoin(Perfil.usuarios)   
            .group_by(Rol.nombre)
            .order_by(Rol.nombre.asc())
        )
        result = await self.db.execute(stmt)
        return result.all()