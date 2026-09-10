from app.extensions import db

class Empresa(db.Model):

    __tablename__ = 'empresa'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    activo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    registros = db.relationship(
        "RegistroBitacora",
        back_populates="empresa"
    )