import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.route import Ruta
    from src.models.route_schedule import HorarioRuta
    from src.models.user import Usuario
    from src.models.vehicle import Vehiculo


class Recorrido(Base):
    __tablename__ = "recorrido"

    __table_args__ = (
        CheckConstraint(
            "estado IN ('PROGRAMADO', 'EN_CURSO', 'EN_PAUSA', 'COMPLETADO', 'CANCELADO')",
            name="ck_recorrido_estado",
        ),
        CheckConstraint(
            "(estado <> 'CANCELADO' OR motivo IS NOT NULL) AND (con_retraso = FALSE OR motivo IS NOT NULL)",
            name="ck_recorrido_motivo_obligatorio",
        ),
        UniqueConstraint(
            "id_ruta",
            "fecha",
            "id_horario",
            name="uq_recorrido_ruta_fecha_horario",
        ),
    )

    id_recorrido: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    id_ruta: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ruta.id_ruta", ondelete="RESTRICT"),
        nullable=False,
    )

    id_horario: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("horario_ruta.id_horario", ondelete="SET NULL"),
        nullable=True,
    )

    id_conductor: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario", ondelete="SET NULL"),
        nullable=True,
    )

    id_vehiculo: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("vehiculo.id_vehiculo", ondelete="SET NULL"),
        nullable=True,
    )

    fecha: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'PROGRAMADO'"),
    )

    con_retraso: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )

    inicio_real: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    fin_real: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    motivo: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    actualizado_por: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario", ondelete="SET NULL"),
        nullable=True,
    )

    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
    )

    # Relaciones ORM
    ruta: Mapped["Ruta"] = relationship()
    horario: Mapped[Optional["HorarioRuta"]] = relationship()
    conductor: Mapped[Optional["Usuario"]] = relationship(foreign_keys=[id_conductor])
    vehiculo: Mapped[Optional["Vehiculo"]] = relationship()
    actualizador: Mapped[Optional["Usuario"]] = relationship(foreign_keys=[actualizado_por])


class HistorialEstadoRecorrido(Base):
    __tablename__ = "historial_estado_recorrido"

    id_historial: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    id_recorrido: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("recorrido.id_recorrido", ondelete="CASCADE"),
        nullable=False,
    )

    estado_anterior: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
    )

    estado_nuevo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    id_usuario: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario"),
        nullable=False,
    )

    motivo: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
    )

    # Relaciones ORM
    recorrido: Mapped["Recorrido"] = relationship()
    usuario: Mapped["Usuario"] = relationship()