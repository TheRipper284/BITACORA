from app.extensions import db

class Auditor(db.Model):

    __tablename__ = 'auditores'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(150),
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
        back_populates="auditor"
    )