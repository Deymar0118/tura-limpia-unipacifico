
import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.shift import AsignacionTurno


class Usuario(Base):
    __tablename__ = "usuario"

    __table_args__ = (
        CheckConstraint(
            "rol IN ('ADMINISTRADOR', 'GERENTE', 'CONDUCTOR', "
            "'TRABAJADOR', 'CLIENTE')",
            name="ck_usuario_rol",
        ),
    )

    id_usuario: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    documento: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True
    )

    nombres: Mapped[str] = mapped_column(
        String(80), nullable=False
    )

    apellidos: Mapped[str] = mapped_column(
        String(80), nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(120), nullable=False, unique=True
    )

    telefono: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )

    rol: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    activo: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("TRUE")
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
    )

    conductor_perfil: Mapped[Optional["PerfilConductor"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    reportes: Mapped[list["ReporteCiudadano"]] = relationship(
        back_populates="usuario",
        passive_deletes=True,
    )

    asignaciones_turno: Mapped[list["AsignacionTurno"]] = relationship(
        back_populates="conductor"
    )


class PerfilConductor(Base):
    __tablename__ = "perfil_conductor"

    id_conductor: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario", ondelete="CASCADE"),
        primary_key=True,
    )

    licencia_numero: Mapped[str] = mapped_column(
        String(30), nullable=False, unique=True
    )

    licencia_categoria: Mapped[str] = mapped_column(
        String(10), nullable=False
    )

    licencia_vence: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="conductor_perfil"
    )


class ReporteCiudadano(Base):
    __tablename__ = "reporte_ciudadano"

    __table_args__ = (
        CheckConstraint(
            "estado_reporte IN "
            "('PENDIENTE', 'EN_REVISION', 'RESUELTO', 'RECHAZADO')",
            name="ck_reporte_ciudadano_estado",
        ),
    )

    id_reporte: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    id_usuario: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario", ondelete="SET NULL"),
        nullable=True,
    )

    tipo_reporte: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    direccion_ref: Mapped[Optional[str]] = mapped_column(
        String(200), nullable=True
    )

    estado_reporte: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'PENDIENTE'"),
    )

    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
    )

    usuario: Mapped[Optional["Usuario"]] = relationship(
        back_populates="reportes"
    )
