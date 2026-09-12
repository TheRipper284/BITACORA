from flask import Flask
from flask_login import current_user

from config import Config
from app.extensions import db, migrate, login_manager

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app import models

    from app.routes.auth import auth_bp
    from app.routes.bitacora import bitacora_bp
    from app.routes.admin import admin_bp
    from app.routes.reportes import reportes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(bitacora_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reportes_bp)

    @app.errorhandler(403)
    def accero_denegado(error):
        from flask import render_template

        return render_template(
            "403.html"
        ),403

    return app
