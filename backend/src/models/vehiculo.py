from typing import Optional
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id_vehiculo: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    placa: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    num_interno: Mapped[str] = mapped_column(String(20), nullable=False)
    marca: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    modelo: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    capacidad_ton: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    estado_operativo: Mapped[str] = mapped_column(String(30), default="operativo")

    asignaciones: Mapped[list["Asignacion"]] = relationship(back_populates="vehiculo")
    ejecuciones: Mapped[list["EjecucionRuta"]] = relationship(back_populates="vehiculo")