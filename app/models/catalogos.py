from app.extensions import db

class TipoPersonal(db.Model):

    __tablename__ = "tipos_personal"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(30),
        nullable=False,
        unique=True
    )

    activo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    personal = db.relationship(
        "Personal",
        back_populates="tipo_personal"
    )

class TipoRequerimiento(db.Model):

    __tablename__ = "tipos_requerimiento"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    codigo = db.Column(
        db.String(10),
        nullable=False,
        unique=True
    )

    nombre = db.Column(
        db.String(30),
        nullable=False,
    )

    activo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    registros = db.relationship(
        "RegistroBitacora",
        back_populates="tipo_requerimiento"
    )