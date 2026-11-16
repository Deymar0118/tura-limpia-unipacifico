
"""adaptar perfiles y trabajadores al MER

Revision ID: 25df0eba252e
Revises: 7498f02e40d5
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "25df0eba252e"
down_revision: Union[str, Sequence[str], None] = "7498f02e40d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Eliminar la tabla intermedia y sus asociaciones.
    op.drop_table("usuario_perfil")

    # 2. Eliminar trabajadores existentes, si los hubiera.
    # Esto permite modificar su relación sin conservar registros
    # incompatibles con el nuevo modelo.
    op.execute(sa.text("DELETE FROM trabajadores"))

    # 3. Eliminar los perfiles, usuarios y roles de prueba.
    op.execute(sa.text("DELETE FROM perfiles"))
    op.execute(sa.text("DELETE FROM usuarios"))
    op.execute(sa.text("DELETE FROM roles"))

    # 4. Incorporar la relación directa entre Perfil y Usuario.
    op.add_column(
        "perfiles",
        sa.Column("id_usuario", sa.UUID(), nullable=False),
    )
    op.add_column(
        "perfiles",
        sa.Column("fecha_inicio", sa.Date(), nullable=False),
    )
    op.add_column(
        "perfiles",
        sa.Column("fecha_fin", sa.Date(), nullable=True),
    )

    op.create_index(
        "ix_perfiles_id_usuario",
        "perfiles",
        ["id_usuario"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_perfiles_usuario",
        "perfiles",
        "usuarios",
        ["id_usuario"],
        ["id_usuario"],
        ondelete="CASCADE",
    )

    # 5. Cambiar la relación de Trabajador.
    op.drop_index(
        "ix_trabajadores_id_usuario",
        table_name="trabajadores",
    )

    op.drop_constraint(
        "trabajadores_id_usuario_fkey",
        "trabajadores",
        type_="foreignkey",
    )

    op.drop_column("trabajadores", "id_usuario")

    op.add_column(
        "trabajadores",
        sa.Column("id_perfil", sa.UUID(), nullable=False),
    )

    op.create_index(
        "ix_trabajadores_id_perfil",
        "trabajadores",
        ["id_perfil"],
        unique=True,
    )

    op.create_foreign_key(
        "fk_trabajadores_perfil",
        "trabajadores",
        "perfiles",
        ["id_perfil"],
        ["id_perfil"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    # Se restaura la estructura anterior, pero no los datos eliminados.

    op.drop_constraint(
        "fk_trabajadores_perfil",
        "trabajadores",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_trabajadores_id_perfil",
        table_name="trabajadores",
    )

    op.drop_column("trabajadores", "id_perfil")

    op.add_column(
        "trabajadores",
        sa.Column("id_usuario", sa.UUID(), nullable=False),
    )

    op.create_index(
        "ix_trabajadores_id_usuario",
        "trabajadores",
        ["id_usuario"],
        unique=True,
    )

    op.create_foreign_key(
        "trabajadores_id_usuario_fkey",
        "trabajadores",
        "usuarios",
        ["id_usuario"],
        ["id_usuario"],
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "fk_perfiles_usuario",
        "perfiles",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_perfiles_id_usuario",
        table_name="perfiles",
    )

    op.drop_column("perfiles", "fecha_fin")
    op.drop_column("perfiles", "fecha_inicio")
    op.drop_column("perfiles", "id_usuario")

    op.create_table(
        "usuario_perfil",
        sa.Column("id_usuario", sa.UUID(), nullable=False),
        sa.Column("id_perfil", sa.UUID(), nullable=False),
        sa.Column("fecha_inicio", sa.DATE(), nullable=False),
        sa.Column("fecha_fin", sa.DATE(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_perfil"],
            ["perfiles.id_perfil"],
            name="usuario_perfil_id_perfil_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["id_usuario"],
            ["usuarios.id_usuario"],
            name="usuario_perfil_id_usuario_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id_usuario",
            "id_perfil",
            name="usuario_perfil_pkey",
        ),
    )
