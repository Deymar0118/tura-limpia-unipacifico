from datetime import time, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    SmallInteger,
    Time,
    DateTime,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.route import Ruta
    from src.models.sector import Barrio


class RutaBarrio(Base):
    __tablename__ = "ruta_barrio"

    __table_args__ = (
        CheckConstraint(
            "orden > 0",
            name="ck_ruta_barrio_orden",
        ),
        UniqueConstraint(
            "id_ruta",
            "orden",
            name="uq_ruta_barrio_orden",
        ),
    )

    id_ruta: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ruta.id_ruta", ondelete="CASCADE"),
        primary_key=True,
    )

    id_barrio: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("barrio.id_barrio", ondelete="RESTRICT"),
        primary_key=True,
    )

    orden: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    hora_estimada_llegada: Mapped[Optional[time]] = mapped_column(
        Time,
        nullable=True,
    )

    # Relaciones ORM
    ruta: Mapped["Ruta"] = relationship(
        back_populates="barrios_asociados"
    )

    barrio: Mapped["Barrio"] = relationship()


class HorarioRuta(Base):
    __tablename__ = "horario_ruta"

    __table_args__ = (
        CheckConstraint(
            "dia_semana BETWEEN 1 AND 7",
            name="ck_horario_ruta_dia_semana",
        ),
        CheckConstraint(
            "hora_fin > hora_inicio",
            name="ck_horario_ruta_horas",
        ),
        UniqueConstraint(
            "id_ruta",
            "dia_semana",
            "hora_inicio",
            name="uq_horario_ruta_dia_hora",
        ),
    )

    id_horario: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    id_ruta: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("ruta.id_ruta", ondelete="CASCADE"),
        nullable=False,
    )

    dia_semana: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    hora_inicio: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    hora_fin: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
    )

    # Relaciones ORM
    ruta: Mapped["Ruta"] = relationship(
        back_populates="horarios"
    )