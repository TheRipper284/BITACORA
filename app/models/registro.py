from app.extensions import db


class RegistroBitacora(db.Model):
    __tablename__ = "registros_bitacora"

    id = db.Column(
        db.BigInteger,
        primary_key=True
    )

    numero = db.Column(
        db.Integer,
        nullable=False
    )

    fecha = db.Column(
        db.Date,
        nullable=False
    )

    hora_entrada = db.Column(
        db.Time,
        nullable=False
    )

    hora_salida = db.Column(
        db.Time,
        nullable=True
    )

    soporte = db.Column(
        db.String(100),
        nullable=False
    )

    empresa = db.Column(
        db.String(150),
        nullable=False
    )

    actividad = db.Column(
        db.Text,
        nullable=False
    )

    nave_id = db.Column(
        db.Integer,
        db.ForeignKey("naves.id"),
        nullable=False
    )

    area_id = db.Column(
        db.Integer,
        db.ForeignKey("areas.id"),
        nullable=False
    )

    bitacora_lectora = db.Column(
        db.String(50),
        nullable=False,
        default="Bitacora"
    )

    tipo_requerimiento_id = db.Column(
        db.Integer,
        db.ForeignKey("tipos_requerimiento.id"),
        nullable=False
    )

    codigo_requerimiento = db.Column(
        db.String(20),
        nullable=False
    )

    argonite_anexo1 = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    personal_id = db.Column(
        db.Integer,
        db.ForeignKey("personal.id"),
        nullable=False
    )

    numero_registro = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    auditor_id = db.Column(
        db.Integer,
        db.ForeignKey("auditores.id"),
        nullable=False
    )

    amonestacion = db.Column(
        db.SmallInteger,
        nullable=False,
        default=0
    )

    comentario = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    # ========================================================
    # RELACIONES
    # ========================================================

    nave = db.relationship(
        "Nave",
        back_populates="registros"
    )

    area = db.relationship(
        "Area",
        back_populates="registros"
    )

    tipo_requerimiento = db.relationship(
        "TipoRequerimiento",
        back_populates="registros"
    )

    personal = db.relationship(
        "Personal",
        back_populates="registros"
    )

    auditor = db.relationship(
        "Auditor",
        back_populates="registros"
    )

    # ========================================================
    # INDICES
    # ========================================================

    __table_args__ = (
        db.Index(
            "ix_registro_fecha",
            "fecha"
        ),

        db.Index(
            "ix_registro_empresa",
            "empresa"
        ),

        db.Index(
            "ix_registro_codigo",
            "codigo_requerimiento"
        ),

        db.Index(
            "ix_registro_personal",
            "personal_id"
        ),

        db.Index(
            "ix_registros_nave_fecha",
            "nave_id",
            "fecha"
        ),

        db.Index(
            "ix_registros_area_fecha",
            "area_id",
            "fecha"
        ),

        db.Index(
            "ix_registros_empresa_fecha",
            "empresa",
            "fecha"
        ),
    )