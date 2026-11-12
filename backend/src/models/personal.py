import uuid
from datetime import date
from typing import Optional
from sqlalchemy import Date, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class Trabajador(Base):
    __tablename__ = "trabajadores"

    id_trabajador: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    id_usuario: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    cargo: Mapped[str] = mapped_column(String(50), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'activo'"))

    usuario: Mapped["Usuario"] = relationship(back_populates="trabajador")
    conductor: Mapped[Optional["Conductor"]] = relationship(
        back_populates="trabajador", uselist=False, cascade="all, delete-orphan", passive_deletes=True
    )


class Conductor(Base):
    __tablename__ = "conductores"

    id_conductor: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    id_trabajador: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("trabajadores.id_trabajador", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    categoria_licencia: Mapped[str] = mapped_column(String(20), nullable=False)
    num_licencia: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    vencimiento_licencia: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'activo'"))

    trabajador: Mapped["Trabajador"] = relationship(back_populates="conductor")
    programaciones: Mapped[list["ProgramacionRuta"]] = relationship(back_populates="conductor")


class Cuadrilla(Base):
    __tablename__ = "cuadrillas"

    id_cuadrilla: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    nombre_cuadrilla: Mapped[str] = mapped_column(String(100), nullable=False)
    num_integrantes: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("1"))
    tipo_cuadrilla: Mapped[str] = mapped_column(String(50), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'activo'"))

    programaciones: Mapped[list["ProgramacionRuta"]] = relationship(back_populates="cuadrilla")


class TrabajadorCuadrilla(Base):
    __tablename__ = "trabajador_cuadrilla"

    id_trabajador: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("trabajadores.id_trabajador", ondelete="CASCADE"), primary_key=True
    )
    id_cuadrilla: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cuadrillas.id_cuadrilla", ondelete="CASCADE"), primary_key=True
    )
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)