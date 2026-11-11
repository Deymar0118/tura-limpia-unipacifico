from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.perfil import Perfil
from src.models.rol import Rol

class RolRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_rol(self, rol: Rol) -> Rol:
        self.db.add(rol)
        await self.db.commit()
        await self.db.refresh(rol)
        return rol

    async def find_rol_by_nombre(self, nombre: str) -> Optional[Rol]:
        stmt = select(Rol).where(Rol.nombre == nombre)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_roles(self) -> list[Rol]:
        stmt = select(Rol).order_by(Rol.nombre.asc())
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_active_roles_by_user(self, user_id: str) -> list[Rol]:
        stmt = (
            select(Rol)
            .join(Rol.perfiles)
            .where(
                Perfil.usuario_id == user_id,
                Perfil.is_active == True 
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
