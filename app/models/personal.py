from app.extensions import db


class Personal(db.Model):
    __tablename__ = "personal"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    tipo_personal_id = db.Column(
        db.Integer,
        db.ForeignKey("tipos_personal.id"),
        nullable=False
    )

    numero_registro = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    activo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    tipo_personal = db.relationship(
        "TipoPersonal",
        back_populates="personal"
    )