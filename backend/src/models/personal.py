from datetime import date
from typing import Optional
from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class Trabajador(Base):
    __tablename__ = "trabajadores"

    id_trabajador: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), unique=True, nullable=False)
    cargo: Mapped[str] = mapped_column(String(50), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo")

    usuario: Mapped["Usuario"] = relationship(back_populates="trabajador")
    conductor: Mapped[Optional["Conductor"]] = relationship(back_populates="trabajador", uselist=False)


class Conductor(Base):
    __tablename__ = "conductores"

    id_conductor: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_trabajador: Mapped[int] = mapped_column(ForeignKey("trabajadores.id_trabajador"), unique=True, nullable=False)
    categoria_licencia: Mapped[str] = mapped_column(String(20), nullable=False)
    num_licencia: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    vencimiento_licencia: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo")

    trabajador: Mapped["Trabajador"] = relationship(back_populates="conductor")
    programaciones: Mapped[list["ProgramacionRuta"]] = relationship(back_populates="conductor")


class Cuadrilla(Base):
    __tablename__ = "cuadrillas"

    id_cuadrilla: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_cuadrilla: Mapped[str] = mapped_column(String(100), nullable=False)
    num_integrantes: Mapped[int] = mapped_column(Integer, default=1)
    tipo_cuadrilla: Mapped[str] = mapped_column(String(50), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo")

    programaciones: Mapped[list["ProgramacionRuta"]] = relationship(back_populates="cuadrilla")


class TrabajadorCuadrilla(Base):
    __tablename__ = "trabajador_cuadrilla"

    id_trabajador: Mapped[int] = mapped_column(ForeignKey("trabajadores.id_trabajador"), primary_key=True)
    id_cuadrilla: Mapped[int] = mapped_column(ForeignKey("cuadrillas.id_cuadrilla"), primary_key=True)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)