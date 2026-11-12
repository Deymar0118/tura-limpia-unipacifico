from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class Novedad(Base):
    __tablename__ = "novedades"

    id_novedad: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_ejecucion: Mapped[int] = mapped_column(ForeignKey("ejecuciones_ruta.id_ejecucion"), nullable=False)
    id_usuario: Mapped[Optional[int]] = mapped_column(ForeignKey("usuarios.id_usuario"), nullable=True)
    tipo_novedad: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    direccion_ref: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="reportada")

    ejecucion: Mapped["EjecucionRuta"] = relationship(back_populates="novedades")
    usuario: Mapped[Optional["Usuario"]] = relationship(back_populates="novedades")