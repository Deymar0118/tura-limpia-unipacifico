import uuid
from datetime import date
from typing import Optional
from sqlalchemy import Date, Float, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id_vehiculo: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    placa: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    num_interno: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    marca: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    modelo: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    capacidad_ton: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fecha_adquisicion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    estado_operativo: Mapped[str] = mapped_column(String(30), nullable=False, server_default=text("'operativo'"))

    asignaciones: Mapped[list["Asignacion"]] = relationship(back_populates="vehiculo")
    ejecuciones: Mapped[list["EjecucionRuta"]] = relationship(back_populates="vehiculo")