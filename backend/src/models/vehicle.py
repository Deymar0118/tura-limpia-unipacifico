
import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    CheckConstraint,
    Date,
    Numeric,
    SmallInteger,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.shift import AsignacionTurno


class Vehiculo(Base):
    __tablename__ = "vehiculo"

    __table_args__ = (
        CheckConstraint(
            "estado IN ('DISPONIBLE', 'EN_SERVICIO', "
            "'MANTENIMIENTO', 'FUERA_DE_SERVICIO')",
            name="ck_vehiculo_estado",
        ),
        CheckConstraint(
            "anio IS NULL OR anio > 0",
            name="ck_vehiculo_anio",
        ),
        CheckConstraint(
            "capacidad_kg IS NULL OR capacidad_kg > 0",
            name="ck_vehiculo_capacidad",
        ),
    )

    id_vehiculo: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    placa: Mapped[str] = mapped_column(
        String(10), nullable=False, unique=True
    )

    tipo: Mapped[str] = mapped_column(
        String(30), nullable=False
    )

    marca: Mapped[Optional[str]] = mapped_column(
        String(40), nullable=True
    )

    modelo: Mapped[Optional[str]] = mapped_column(
        String(40), nullable=True
    )

    anio: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )

    capacidad_kg: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2), nullable=True
    )

    soat_vence: Mapped[Optional[date]] = mapped_column(
        Date, nullable=True
    )

    revision_vence: Mapped[Optional[date]] = mapped_column(
        Date, nullable=True
    )

    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'DISPONIBLE'"),
    )

    asignaciones_turno: Mapped[list["AsignacionTurno"]] = relationship(
        back_populates="vehiculo"
    )
