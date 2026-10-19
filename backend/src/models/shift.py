
import uuid
from datetime import date, time
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Date,
    ForeignKey,
    String,
    Time,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.user import Usuario
    from src.models.vehicle import Vehiculo


class Turno(Base):
    __tablename__ = "turno"

    id_turno: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    nombre: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
    )

    hora_inicio: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    hora_fin: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    asignaciones_turno: Mapped[list["AsignacionTurno"]] = relationship(
        back_populates="turno"
    )


class AsignacionTurno(Base):
    __tablename__ = "asignacion_turno"

    __table_args__ = (
        UniqueConstraint(
            "id_conductor",
            "id_turno",
            "fecha",
            name="uq_conductor_turno_fecha",
        ),
        UniqueConstraint(
            "id_vehiculo",
            "id_turno",
            "fecha",
            name="uq_vehiculo_turno_fecha",
        ),
    )

    id_asignacion: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    id_conductor: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario"),
        nullable=False,
    )

    id_vehiculo: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("vehiculo.id_vehiculo"),
        nullable=False,
    )

    id_turno: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("turno.id_turno"),
        nullable=False,
    )

    fecha: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    observaciones: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
    )

    conductor: Mapped["Usuario"] = relationship(
        back_populates="asignaciones_turno"
    )

    vehiculo: Mapped["Vehiculo"] = relationship(
        back_populates="asignaciones_turno"
    )

    turno: Mapped["Turno"] = relationship(
        back_populates="asignaciones_turno"
    )
