import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class Novedad(Base):
    __tablename__ = "novedades"

    id_novedad: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    id_ejecucion: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("ejecuciones_ruta.id_ejecucion", ondelete="CASCADE"), nullable=False, index=True
    )
    id_usuario: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", ondelete="SET NULL"), nullable=True, index=True
    )
    tipo_novedad: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    direccion_ref: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'reportada'"))

    ejecucion: Mapped["EjecucionRuta"] = relationship(back_populates="novedades")
    usuario: Mapped[Optional["Usuario"]] = relationship(back_populates="novedades")