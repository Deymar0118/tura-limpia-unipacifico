from typing import Optional
from sqlalchemy import Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class Barrio(Base):
    __tablename__ = "barrios"

    id_barrio: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_barrio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    comuna: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'activo'"))

    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="barrio")
    paradas: Mapped[list["ParadaRuta"]] = relationship(back_populates="barrio")