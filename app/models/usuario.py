from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db

class Usuario(UserMixin, db.Model):

    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nombre = db.Column(
        db.String(150),
        nullable=False
    )

    usuario = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    rol = db.Column(
        db.String(20),
        nullable=False
    )

    activo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    def establecer_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verificar_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    def es_admin(self):
        return self.rol == "ADMIN"

    def es_registrador(self):
        return self.rol == "REGISTRADOR"