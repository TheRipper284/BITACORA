from app import create_app
from app.extensions import db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():

    usuario = Usuario.query.filter_by(
        usuario="admin"
    ).first()

    if usuario:

        print("El usuario Admin ya existe... ")

    else:

        admin=Usuario(
            nombre="Administrador",
            usuario="admin",
            rol="ADMIN",
            activo=True
        )

        admin.establecer_password(
            "Admin123!"
        )

        db.session.add(admin)
        db.session.commit()

        print("Administrador creado correctamente...😎😉")