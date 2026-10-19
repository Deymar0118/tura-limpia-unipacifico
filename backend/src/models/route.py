import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.user import Usuario
    from src.models.route_schedule import HorarioRuta, RutaBarrio


class Ruta(Base):
    __tablename__ = "ruta"

    __table_args__ = (
        CheckConstraint(
            "estado IN ('BORRADOR', 'ACTIVA', 'SUSPENDIDA', 'INACTIVA')",
            name="ck_ruta_estado",
        ),
    )

    id_ruta: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    codigo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'BORRADOR'"),
    )

    creada_por: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario"),
        nullable=False,
    )

    actualizado_en: Mapped[datetime] = mapped_column(
        server_default=text("now()"),
        nullable=False,
    )

    # Relaciones ORM
    creador: Mapped["Usuario"] = relationship()

    barrios_asociados: Mapped[List["RutaBarrio"]] = relationship(
        back_populates="ruta",
        cascade="all, delete-orphan",
    )

    horarios: Mapped[List["HorarioRuta"]] = relationship(
        back_populates="ruta",
        cascade="all, delete-orphan",
    )