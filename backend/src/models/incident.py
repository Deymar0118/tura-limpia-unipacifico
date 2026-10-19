import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

if TYPE_CHECKING:
    from src.models.run import Recorrido
    from src.models.sector import Barrio
    from src.models.user import Usuario


class Incidencia(Base):
    __tablename__ = "incidencia"

    __table_args__ = (
        CheckConstraint(
            "tipo IN ('VEHICULO_AVERIADO', 'VIA_BLOQUEADA', 'CLIMA', 'ACUMULACION_RESIDUOS', 'OTRO')",
            name="ck_incidencia_tipo",
        ),
        CheckConstraint(
            "estado IN ('ABIERTA', 'EN_ATENCION', 'CERRADA')",
            name="ck_incidencia_estado",
        ),
    )

    id_incidencia: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    id_recorrido: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("recorrido.id_recorrido", ondelete="SET NULL"),
        nullable=True,
    )

    id_barrio: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("barrio.id_barrio", ondelete="SET NULL"),
        nullable=True,
    )

    tipo: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    estado: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'ABIERTA'"),
    )

    registrada_por: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("usuario.id_usuario"),
        nullable=False,
    )

    registrada_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
    )

    # Relaciones ORM
    recorrido: Mapped[Optional["Recorrido"]] = relationship()
    barrio: Mapped[Optional["Barrio"]] = relationship()
    usuario: Mapped["Usuario"] = relationship()