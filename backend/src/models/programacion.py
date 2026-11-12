from datetime import date, time
from typing import Optional
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base

programacion_dia = Table(
    "programacion_dia",
    Base.metadata,
    Column("id_programacion", Integer, ForeignKey("programaciones_ruta.id_programacion"), primary_key=True),
    Column("id_dia", Integer, ForeignKey("dias_semana.id_dia"), primary_key=True),
)


class DiaSemana(Base):
    __tablename__ = "dias_semana"

    id_dia: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_dia: Mapped[str] = mapped_column(String(20), nullable=False)


class Turno(Base):
    __tablename__ = "turnos"

    id_turno: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_turno: Mapped[str] = mapped_column(String(50), nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo")

    asignaciones: Mapped[list["Asignacion"]] = relationship(back_populates="turno")


class ProgramacionRuta(Base):
    __tablename__ = "programaciones_ruta"

    id_programacion: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_macroruta: Mapped[int] = mapped_column(ForeignKey("macrorutas.id_macroruta"), nullable=False)
    id_cuadrilla: Mapped[int] = mapped_column(ForeignKey("cuadrillas.id_cuadrilla"), nullable=False)
    id_conductor: Mapped[int] = mapped_column(ForeignKey("conductores.id_conductor"), nullable=False)
    vigencia_desde: Mapped[date] = mapped_column(Date, nullable=False)
    vigencia_hasta: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="activo")

    macroruta: Mapped["Macroruta"] = relationship(back_populates="programaciones")
    cuadrilla: Mapped["Cuadrilla"] = relationship(back_populates="programaciones")
    conductor: Mapped["Conductor"] = relationship(back_populates="programaciones")
    dias: Mapped[list["DiaSemana"]] = relationship(secondary=programacion_dia)
    asignaciones: Mapped[list["Asignacion"]] = relationship(back_populates="programacion")


class Asignacion(Base):
    __tablename__ = "asignaciones"

    id_asignacion: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_programacion: Mapped[int] = mapped_column(ForeignKey("programaciones_ruta.id_programacion"), nullable=False)
    id_vehiculo: Mapped[int] = mapped_column(ForeignKey("vehiculos.id_vehiculo"), nullable=False)
    id_turno: Mapped[int] = mapped_column(ForeignKey("turnos.id_turno"), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="programada")

    programacion: Mapped["ProgramacionRuta"] = relationship(back_populates="asignaciones")
    vehiculo: Mapped["Vehiculo"] = relationship(back_populates="asignaciones")
    turno: Mapped["Turno"] = relationship(back_populates="asignaciones")
    ejecuciones: Mapped[list["EjecucionRuta"]] = relationship(back_populates="asignacion")