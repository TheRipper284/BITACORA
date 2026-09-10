from app import create_app
from app.extensions import db

from app.models import (
    Empresa,
    Nave,
    Area,
    TipoPersonal,
    TipoRequerimiento
)

app = create_app()

with app.app_context():

    # Empresa

    empresa = Empresa.query.filter_by(
        nombre="SIISA GLOBAL"
    ).first()

    if not empresa:

        empresa = Empresa(
            nombre="SIISA GLOBAL"
        )

        db.session.add(empresa)

    # Naves

    for codigo in ["A19", "A20"]:

        nave = Nave.query.filter_by(
            codigo=codigo
        ).first()

        if not nave:

            nave = Nave(
                codigo=codigo
            )

            db.session.add(nave)

    # Areas

    naves = Nave.query.all()

    for nave in naves:

        for nombre_area in [
            "LDR",
            "ITROOM"
        ]:

            area = Area.query.filter_by(
                nave_id=nave.id,
                nombre=nombre_area
            ).first()

            if not area:

                db.session.add(
                    Area(
                        nave_id=nave.id,
                        nombre=nombre_area
                    )
                )

    # Tipo Personal

    for nombre in [
        "Usuario",
        "Visitante"
    ]:
        tipo = TipoPersonal.query.filter_by(
            nombre=nombre
        ).first()

        if not tipo:

            db.session.add(
                TipoPersonal(
                    nombre=nombre
                )
            )

    # Tipo Requerimiento

    tipos = [
        ("RR", "Ticket"),
        ("IR", "Incidente"),
        ("CR", "Cambio"),
    ]

    for codigo, nombre in tipos:

        tipo = TipoRequerimiento.query.filter_by(
            codigo=codigo
        ).first()

        if not tipo:

            db.session.add(
                TipoRequerimiento(
                    codigo=codigo,
                    nombre=nombre
                )
            )

    db.session.commit()

    print("Datos iniciales creados correctamente.")