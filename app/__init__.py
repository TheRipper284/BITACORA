from flask import Flask, redirect, url_for
from flask_wtf import CSRFProtect

from config import Config
from app.extensions import db, migrate, login_manager

csrf = CSRFProtect()

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app import models

    from app.routes.auth import auth_bp
    from app.routes.bitacora import bitacora_bp
    from app.routes.admin import admin_bp
    from app.routes.reportes import reportes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(bitacora_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reportes_bp)

    @app.route("/")
    def root():
        return redirect(url_for("bitacora.index"))

    @app.errorhandler(403)
    def accero_denegado(error):
        from flask import render_template

        return render_template(
            "403.html"
        ),403

    @app.errorhandler(404)
    def pagina_no_encontrada(error):
        from flask import render_template

        return render_template("404.html"), 404

    return app
