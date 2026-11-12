import uuid
from datetime import datetime, time
from typing import Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, Numeric, String, Text, Time, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class EjecucionRuta(Base):
    __tablename__ = "ejecuciones_ruta"

    id_ejecucion: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    id_asignacion: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("asignaciones.id_asignacion", ondelete="RESTRICT"), nullable=False, index=True
    )
    id_vehiculo: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("vehiculos.id_vehiculo", ondelete="RESTRICT"), nullable=False, index=True
    )
    fecha_hora_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fecha_hora_fin: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duracion_real: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'en_proceso'"))

    asignacion: Mapped["Asignacion"] = relationship(back_populates="ejecuciones")
    vehiculo: Mapped["Vehiculo"] = relationship(back_populates="ejecuciones")
    ubicaciones_gps: Mapped[list["UbicacionGPS"]] = relationship(
        back_populates="ejecucion", cascade="all, delete-orphan", passive_deletes=True
    )
    novedades: Mapped[list["Novedad"]] = relationship(
        back_populates="ejecucion", cascade="all, delete-orphan", passive_deletes=True
    )


class CuadrillaEjecucion(Base):
    __tablename__ = "cuadrilla_ejecucion"

    id_cuadrilla: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cuadrillas.id_cuadrilla", ondelete="CASCADE"), primary_key=True
    )
    id_ejecucion: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("ejecuciones_ruta.id_ejecucion", ondelete="CASCADE"), primary_key=True
    )
    hora_inicio: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    hora_fin: Mapped[Optional[time]] = mapped_column(Time, nullable=True)


class EjecucionParada(Base):
    __tablename__ = "ejecucion_parada"

    id_ejecucion: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("ejecuciones_ruta.id_ejecucion", ondelete="CASCADE"), primary_key=True
    )
    id_parada: Mapped[int] = mapped_column(
        Integer, ForeignKey("paradas_ruta.id_parada", ondelete="RESTRICT"), primary_key=True
    )
    hora_llegada_real: Mapped[Optional[time]] = mapped_column(Time, nullable=True)
    observacion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class UbicacionGPS(Base):
    __tablename__ = "ubicaciones_gps"

    id_ubicacion: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_ejecucion: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("ejecuciones_ruta.id_ejecucion", ondelete="CASCADE"), nullable=False, index=True
    )
    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()"), index=True
    )
    latitud: Mapped[float] = mapped_column(Numeric(10, 8), nullable=False)
    longitud: Mapped[float] = mapped_column(Numeric(11, 8), nullable=False)
    coordenadas: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    velocidad: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    ejecucion: Mapped["EjecucionRuta"] = relationship(back_populates="ubicaciones_gps")