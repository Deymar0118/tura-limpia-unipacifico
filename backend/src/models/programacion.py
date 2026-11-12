import uuid
from datetime import date, time
from typing import Optional
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, Time, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base

programacion_dia = Table(
    "programacion_dia",
    Base.metadata,
    Column(
        "id_programacion",
        UUID(as_uuid=True),
        ForeignKey("programaciones_ruta.id_programacion", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "id_dia",
        Integer,
        ForeignKey("dias_semana.id_dia", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class DiaSemana(Base):
    __tablename__ = "dias_semana"

    id_dia: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_dia: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)


class Turno(Base):
    __tablename__ = "turnos"

    id_turno: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_turno: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'activo'"))

    asignaciones: Mapped[list["Asignacion"]] = relationship(back_populates="turno")


class ProgramacionRuta(Base):
    __tablename__ = "programaciones_ruta"

    id_programacion: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    id_macroruta: Mapped[int] = mapped_column(
        Integer, ForeignKey("macrorutas.id_macroruta", ondelete="RESTRICT"), nullable=False, index=True
    )
    id_cuadrilla: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cuadrillas.id_cuadrilla", ondelete="RESTRICT"), nullable=False, index=True
    )
    id_conductor: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conductores.id_conductor", ondelete="RESTRICT"), nullable=False, index=True
    )
    vigencia_desde: Mapped[date] = mapped_column(Date, nullable=False)
    vigencia_hasta: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'activo'"))

    macroruta: Mapped["Macroruta"] = relationship(back_populates="programaciones")
    cuadrilla: Mapped["Cuadrilla"] = relationship(back_populates="programaciones")
    conductor: Mapped["Conductor"] = relationship(back_populates="programaciones")
    dias: Mapped[list["DiaSemana"]] = relationship(secondary=programacion_dia)
    asignaciones: Mapped[list["Asignacion"]] = relationship(
        back_populates="programacion", cascade="all, delete-orphan", passive_deletes=True
    )


class Asignacion(Base):
    __tablename__ = "asignaciones"

    id_asignacion: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    id_programacion: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("programaciones_ruta.id_programacion", ondelete="CASCADE"), nullable=False, index=True
    )
    id_vehiculo: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vehiculos.id_vehiculo", ondelete="RESTRICT"), nullable=False, index=True
    )
    id_turno: Mapped[int] = mapped_column(
        Integer, ForeignKey("turnos.id_turno", ondelete="RESTRICT"), nullable=False, index=True
    )
    fecha: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'programada'"))

    programacion: Mapped["ProgramacionRuta"] = relationship(back_populates="asignaciones")
    vehiculo: Mapped["Vehiculo"] = relationship(back_populates="asignaciones")
    turno: Mapped["Turno"] = relationship(back_populates="asignaciones")
    ejecuciones: Mapped[list["EjecucionRuta"]] = relationship(back_populates="asignacion")