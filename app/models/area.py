from app.extensions import db

class Area(db.Model):

    __tablename__ = 'areas'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nave_id = db.Column(
        db.Integer,
        db.ForeignKey('naves.id'),
        nullable=False
    )

    nombre = db.Column(
        db.String(50),
        nullable=False,
    )

    activo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    nave = db.relationship(
        "Nave",
        back_populates="areas"
    )

    registros = db.relationship(
        "RegistroBitacora",
        back_populates="area"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "nave_id",
            "nombre",
            name="uq_area_nave_nombre"
        ),
    )