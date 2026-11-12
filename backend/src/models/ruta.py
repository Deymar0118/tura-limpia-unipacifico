from datetime import time
from typing import Optional
from sqlalchemy import ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class Macroruta(Base):
    __tablename__ = "macrorutas"

    id_macroruta: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_macroruta: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tipo_servicio: Mapped[str] = mapped_column(String(50), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo")

    microrutas: Mapped[list["Microruta"]] = relationship(back_populates="macroruta")
    programaciones: Mapped[list["ProgramacionRuta"]] = relationship(back_populates="macroruta")


class Microruta(Base):
    __tablename__ = "microrutas"

    id_microruta: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_macroruta: Mapped[int] = mapped_column(ForeignKey("macrorutas.id_macroruta"), nullable=False)
    nombre_microruta: Mapped[str] = mapped_column(String(100), nullable=False)
    trazado: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="activo")

    macroruta: Mapped["Macroruta"] = relationship(back_populates="microrutas")
    paradas: Mapped[list["ParadaRuta"]] = relationship(back_populates="microruta")


class ParadaRuta(Base):
    __tablename__ = "paradas_ruta"

    id_parada: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_microruta: Mapped[int] = mapped_column(ForeignKey("microrutas.id_microruta"), nullable=False)
    id_barrio: Mapped[int] = mapped_column(ForeignKey("barrios.id_barrio"), nullable=False)
    orden_visita: Mapped[int] = mapped_column(Integer, nullable=False)
    hora_estimada_llegada: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="activo")

    microruta: Mapped["Microruta"] = relationship(back_populates="paradas")
    barrio: Mapped["Barrio"] = relationship(back_populates="paradas")