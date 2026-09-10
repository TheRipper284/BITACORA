from app.extensions import db

class Nave(db.Model):

    __tablename__ = 'naves'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    codigo = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )

    activo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    areas = db.relationship(
        "Area",
        back_populates="nave",
        cascade="all, delete-orphan"
    )

    registros = db.relationship(
        "RegistroBitacora",
        back_populates="nave"
    )