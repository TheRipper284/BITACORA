from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

login_manager.login_view = 'auth.login'

@login_manager.user_loader
def cargar_usuario(usuario_id):

    from app.models.usuario import Usuario

    return db.session.get(
        Usuario,
        int(usuario_id)
    )