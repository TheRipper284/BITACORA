from app.extensions import db


class Auditor(db.Model):

    __tablename__ = "auditores"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    nave_id = db.Column(
        db.Integer,
        db.ForeignKey("naves.id"),
        nullable=True
    )

    area_id = db.Column(
        db.Integer,
        db.ForeignKey("areas.id"),
        nullable=True
    )

    activo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    nave = db.relationship(
        "Nave",
        back_populates="auditores"
    )

    area = db.relationship(
        "Area",
        back_populates="auditores"
    )

    registros = db.relationship(
        "RegistroBitacora",
        back_populates="auditor"
    )