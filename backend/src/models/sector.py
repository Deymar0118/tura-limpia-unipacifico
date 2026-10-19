from typing import Optional, List

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Sector(Base):
    __tablename__ = "sector"

    id_sector: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
    )

    descripcion: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # Relación bidireccional opcional con Barrio
    barrios: Mapped[List["Barrio"]] = relationship(
        "Barrio",
        back_populates="sector",
        cascade="all, delete-orphan",
    )


class Barrio(Base):
    __tablename__ = "barrio"

    __table_args__ = (
        UniqueConstraint(
            "nombre",
            "id_sector",
            name="uq_barrio_nombre_sector",
        ),
    )

    id_barrio: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    id_sector: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("sector.id_sector", ondelete="RESTRICT"),
        nullable=True,
    )

    fuente_nombre: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("TRUE"),
    )

    # Relación bidireccional opcional con Sector
    sector: Mapped[Optional["Sector"]] = relationship(
        "Sector",
        back_populates="barrios",
    )