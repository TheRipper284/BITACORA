from app import create_app
from app.extensions import db

from app.models import (Personal, Auditor, TipoPersonal)

app = create_app()

with app.app_context():

    tipo_usuario = TipoPersonal.query.filter_by(
        nombre = "Usuario"
    ).first()

    tipo_visitante = TipoPersonal.query.filter_by(
        nombre = "Visitante"
    ).first()

    if not tipo_usuario or not tipo_visitante:
        print("Primero ejecuta el seed personal.")
        raise SystemExit

    personal_existente = Personal.query.filter_by(
        nombre = "Julio Caute"
    ).first()

    if not personal_existente:
        db.session.add(
            Personal(
                nombre = "Julio Caute",
                tipo_personal_id = tipo_usuario.id,
                numero_registro=1
            )
        )

    visitante_existente = Personal.query.filter_by(
        nombre = "Juan Luna"
    ).first()

    if not visitante_existente:

        db.session.add(
            Personal(
                nombre = "Juan Luna",
                tipo_personal_id = tipo_visitante.id,
                numero_registro = 1
            )
        )

    auditor_existente = Auditor.query.filter_by(
        nombre = "Julio Caute"
    ).first()

    if not auditor_existente:

        db.session.add(
            Auditor(
                nombre = "Julio Caute"
            )
        )

        db.session.commit()

        print("Personal y auditor de prueba creados.")