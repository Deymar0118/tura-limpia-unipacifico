
import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Rol(Base):
    __tablename__ = "roles"

    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_rol: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    estado: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'activo'")
    )

    perfiles: Mapped[list["Perfil"]] = relationship(back_populates="rol")


class Perfil(Base):
    __tablename__ = "perfiles"

    id_perfil: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_usuario: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    id_rol: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("roles.id_rol", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    estado: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'activo'")
    )

    usuario: Mapped["Usuario"] = relationship(back_populates="perfiles")
    rol: Mapped["Rol"] = relationship(back_populates="perfiles")
    trabajador: Mapped[Optional["Trabajador"]] = relationship(
        back_populates="perfil",
        uselist=False,
    )


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    id_barrio: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("barrios.id_barrio", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    nombre_completo: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True
    )
    nombre_usuario: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    correo: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    documento: Mapped[Optional[str]] = mapped_column(
        String(30), unique=True, nullable=True, index=True
    )
    estado: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'activo'")
    )
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    barrio: Mapped[Optional["Barrio"]] = relationship(
        back_populates="usuarios"
    )
    perfiles: Mapped[list["Perfil"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    novedades: Mapped[list["Novedad"]] = relationship(
        back_populates="usuario"
    )
