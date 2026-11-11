from turtle import update
from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.perfil import Perfil

class PerfilRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_perfil(self, perfil: Perfil) -> Perfil:
        self.db.add(perfil)
        await self.db.commit()
        await self.db.refresh(perfil)
        return perfil

    async def cambiar_estado_perfil(self, perfil_id: int, nuevo_estado: bool) -> Optional[Perfil]:
        stmt = select(Perfil).where(Perfil.id == perfil_id)
        result = await self.db.execute(stmt)
        perfil = result.scalar_one_or_none()

        if perfil:
            perfil.activo = nuevo_estado
            await self.db.commit()
            await self.db.refresh(perfil)

        return perfil

    async def delete_perfil_by_user(self, user_id: int) -> bool:
        stmt = select(Perfil).where(Perfil.usuario_id == user_id)
        result = await self.db.execute(stmt)
        perfil = result.scalar_one_or_none()

        if perfil:
            await self.db.delete(perfil)
            await self.db.commit()
            return True

        return False

    async def update_profile_status(self, user_id: str, 
                                    role_id: str, 
                                    is_active: bool) -> Optional[Perfil]:

        stmt = select(Perfil).where(
            Perfil.id_usuario == user_id, 
            Perfil.id_rol == role_id
        )
        result = await self.db.execute(stmt)
        profile = result.scalar_one_or_none()

        if profile:
            profile.is_active = is_active
            await self.db.commit()
            await self.db.refresh(profile)

        return profile

    async def deactivate_all_by_user(self, user_id: str) -> bool:
        stmt = (
            update(Perfil)
            .where(Perfil.id_usuario == user_id)
            .values(activo=False)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0