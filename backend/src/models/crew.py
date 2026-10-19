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
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.sector import Barrio
    from src.models.user import Usuario


class CuadrillaBarrio(Base):
    __tablename__ = "cuadrilla_barrio"

    __table_args__ = (
        CheckConstraint(
            "turno IN ('MAÑANA', 'TARDE', 'NOCHE')",
            name="ck_cuadrilla_barrio_turno",
        ),
    )

    id_cuadrilla: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    id_barrio: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("barrio.id_barrio", ondelete="RESTRICT"),
        nullable=False,
    )

    id_trabajador: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario", ondelete="CASCADE"),
        nullable=False,
    )

    turno: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'MAÑANA'"),
    )

    fecha_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    fecha_fin: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )

    asignado_por: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario"),
        nullable=False,
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
    )

    # Relaciones ORM
    barrio: Mapped["Barrio"] = relationship()
    trabajador: Mapped["Usuario"] = relationship(foreign_keys=[id_trabajador])
    asignador: Mapped["Usuario"] = relationship(foreign_keys=[asignado_por])