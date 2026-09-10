from flask import Blueprint

reportes_bp = Blueprint(
    "reportes",
    __name__,
    url_prefix="/reportes"
)

@reportes_bp.route("/")
def index():
    return "Reportes"