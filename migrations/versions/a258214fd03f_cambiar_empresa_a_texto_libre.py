"""Cambiar empresa a texto libre

Revision ID: a258214fd03f
Revises: 2735072c5dee
Create Date: 2026-09-20

"""

from alembic import op
import sqlalchemy as sa


revision = "a258214fd03f"
down_revision = "2735072c5dee"
branch_labels = None
depends_on = None


def upgrade():

    # 1. Crear la nueva columna temporalmente permitiendo NULL
    op.add_column(
        "registros_bitacora",
        sa.Column(
            "empresa",
            sa.String(length=150),
            nullable=True
        )
    )

    # 2. Copiar el nombre de la empresa desde la tabla empresa
    op.execute(
        """
        UPDATE registros_bitacora rb
        SET empresa = e.nombre
        FROM empresa e
        WHERE rb.empresa_id = e.id
        """
    )

    # 3. Verificar que ningún registro haya quedado sin empresa
    resultado = op.get_bind().execute(
        sa.text(
            """
            SELECT COUNT(*)
            FROM registros_bitacora
            WHERE empresa IS NULL
            """
        )
    ).scalar()

    if resultado != 0:
        raise RuntimeError(
            "La migración encontró registros sin empresa."
        )

    # 4. Ahora sí hacemos la columna obligatoria
    op.alter_column(
        "registros_bitacora",
        "empresa",
        existing_type=sa.String(length=150),
        nullable=False
    )

    # 5. Eliminar el índice anterior que dependía de empresa_id
    op.drop_index(
        "ix_registros_empresa_fecha",
        table_name="registros_bitacora"
    )

    # 6. Crear el índice equivalente usando empresa
    op.create_index(
        "ix_registros_empresa_fecha",
        "registros_bitacora",
        ["empresa", "fecha"],
        unique=False
    )

    # 7. Crear el índice individual de empresa
    op.create_index(
        "ix_registro_empresa",
        "registros_bitacora",
        ["empresa"],
        unique=False
    )

    # 8. Eliminar la FK empresa_id
    op.drop_constraint(
        "registros_bitacora_empresa_id_fkey",
        "registros_bitacora",
        type_="foreignkey"
    )

    # 9. Eliminar empresa_id
    op.drop_column(
        "registros_bitacora",
        "empresa_id"
    )


def downgrade():

    # 1. Volver a crear empresa_id
    op.add_column(
        "registros_bitacora",
        sa.Column(
            "empresa_id",
            sa.Integer(),
            nullable=True
        )
    )

    # 2. Restaurar los registros relacionándolos por nombre
    op.execute(
        """
        UPDATE registros_bitacora rb
        SET empresa_id = e.id
        FROM empresa e
        WHERE rb.empresa = e.nombre
        """
    )

    # 3. Verificar que todos tengan empresa_id
    resultado = op.get_bind().execute(
        sa.text(
            """
            SELECT COUNT(*)
            FROM registros_bitacora
            WHERE empresa_id IS NULL
            """
        )
    ).scalar()

    if resultado != 0:
        raise RuntimeError(
            "No fue posible restaurar todos los empresa_id."
        )

    # 4. Hacer empresa_id obligatorio
    op.alter_column(
        "registros_bitacora",
        "empresa_id",
        existing_type=sa.Integer(),
        nullable=False
    )

    # 5. Restaurar FK
    op.create_foreign_key(
        "registros_bitacora_empresa_id_fkey",
        "registros_bitacora",
        "empresa",
        ["empresa_id"],
        ["id"]
    )

    # 6. Eliminar índices relacionados con empresa
    op.drop_index(
        "ix_registro_empresa",
        table_name="registros_bitacora"
    )

    op.drop_index(
        "ix_registros_empresa_fecha",
        table_name="registros_bitacora"
    )

    # 7. Restaurar índice original
    op.create_index(
        "ix_registros_empresa_fecha",
        "registros_bitacora",
        ["empresa_id", "fecha"],
        unique=False
    )

    # 8. Eliminar columna de texto
    op.drop_column(
        "registros_bitacora",
        "empresa"
    )