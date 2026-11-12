from datetime import date, datetime
from typing import Optional
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class Rol(Base):
    __tablename__ = "roles"

    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre_rol: Mapped[str] = mapped_column(String(50), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo")

    perfiles: Mapped[list["Perfil"]] = relationship(back_populates="rol")


class Perfil(Base):
    __tablename__ = "perfiles"

    id_perfil: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_rol: Mapped[int] = mapped_column(ForeignKey("roles.id_rol"), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo")

    rol: Mapped["Rol"] = relationship(back_populates="perfiles")
    usuarios_perfil: Mapped[list["UsuarioPerfil"]] = relationship(back_populates="perfil")


class UsuarioPerfil(Base):
    __tablename__ = "usuario_perfil"

    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"), primary_key=True)
    id_perfil: Mapped[int] = mapped_column(ForeignKey("perfiles.id_perfil"), primary_key=True)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="perfiles")
    perfil: Mapped["Perfil"] = relationship(back_populates="usuarios_perfil")


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_barrio: Mapped[Optional[int]] = mapped_column(ForeignKey("barrios.id_barrio"), nullable=True)
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    nombre_completo: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    nombre_usuario: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    correo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    contraseña_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    documento: Mapped[Optional[str]] = mapped_column(String(30), unique=True, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="activo")
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    barrio: Mapped[Optional["Barrio"]] = relationship(back_populates="usuarios")
    perfiles: Mapped[list["UsuarioPerfil"]] = relationship(back_populates="usuario")
    trabajador: Mapped[Optional["Trabajador"]] = relationship(back_populates="usuario", uselist=False)
    novedades: Mapped[list["Novedad"]] = relationship(back_populates="usuario")