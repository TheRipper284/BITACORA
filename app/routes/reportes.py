from flask import Blueprint

from app.routes.auth import admin_required


reportes_bp = Blueprint(
    "reportes",
    __name__,
    url_prefix="/reportes"
)


@reportes_bp.route("/")
@admin_required
def index():
    return "Reportes"