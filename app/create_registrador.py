from app import create_app
from app.extensions import db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():

    usuario = Usuario.query.filter_by(
        usuario="registrador"
    ).first()

    if usuario:
        print(
            "El usuario registrador ya existe."
        )

    else:
        registrador = Usuario(
            nombre="Registrador",
            usuario="registrador",
            rol="REGISTRADOR",
            activo=True
        )
        registrador.establecer_password(
            "Registro123!"
        )
        db.session.add(registrador)
        db.session.commit()

        print(
            "Registrador creado correctamente."
        )