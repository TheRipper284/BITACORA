"""Cambiar personal de FK a texto

Revision ID: 9e24eefec47f
Revises: a258214fd03f
Create Date: 2026-09-21 00:08:25.991121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e24eefec47f'
down_revision = 'a258214fd03f'
branch_labels = None
depends_on = None


def upgrade():

    # 1. Crear la nueva columna como nullable temporalmente
    op.add_column(
        "registros_bitacora",
        sa.Column(
            "personal",
            sa.String(length=150),
            nullable=True
        )
    )

    # 2. Copiar el nombre de Personal usando el antiguo personal_id
    op.execute(
        """
        UPDATE registros_bitacora AS rb
        SET personal = p.nombre
        FROM personal AS p
        WHERE rb.personal_id = p.id
        """
    )

    # 3. Verificar que todos los registros tengan Personal
    bind = op.get_bind()

    resultado = bind.execute(
        sa.text(
            """
            SELECT COUNT(*)
            FROM registros_bitacora
            WHERE personal IS NULL
            """
        )
    )

    registros_sin_personal = resultado.scalar()

    if registros_sin_personal != 0:
        raise RuntimeError(
            f"Hay {registros_sin_personal} registros "
            "sin nombre de Personal."
        )

    # 4. Cambiar la columna para que sea NOT NULL
    op.alter_column(
        "registros_bitacora",
        "personal",
        existing_type=sa.String(length=150),
        nullable=False
    )

    # 5. Eliminar el índice antiguo sobre personal_id
    op.drop_index(
        "ix_registro_personal",
        table_name="registros_bitacora"
    )

    # 6. Eliminar la FK antigua
    op.drop_constraint(
        "registros_bitacora_personal_id_fkey",
        "registros_bitacora",
        type_="foreignkey"
    )

    # 7. Eliminar personal_id
    op.drop_column(
        "registros_bitacora",
        "personal_id"
    )

    # 8. Crear índice nuevo sobre personal
    op.create_index(
        "ix_registro_personal",
        "registros_bitacora",
        ["personal"]
    )


def downgrade():

    # 1. Crear nuevamente personal_id
    op.add_column(
        "registros_bitacora",
        sa.Column(
            "personal_id",
            sa.Integer(),
            nullable=True
        )
    )

    # 2. Intentar recuperar el ID mediante coincidencia exacta
    op.execute(
        """
        UPDATE registros_bitacora AS rb
        SET personal_id = p.id
        FROM personal AS p
        WHERE rb.personal = p.nombre
        """
    )

    # 3. Crear nuevamente la FK
    op.create_foreign_key(
        "registros_bitacora_personal_id_fkey",
        "registros_bitacora",
        "personal",
        ["personal_id"],
        ["id"]
    )

    # 4. Eliminar índice de personal
    op.drop_index(
        "ix_registro_personal",
        table_name="registros_bitacora"
    )

    # 5. Eliminar columna personal
    op.drop_column(
        "registros_bitacora",
        "personal"
    )

    # 6. Volver a crear índice de personal_id
    op.create_index(
        "ix_registro_personal",
        "registros_bitacora",
        ["personal_id"]
    )

