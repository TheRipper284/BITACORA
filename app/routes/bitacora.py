from flask import Blueprint

bitacora_bp = Blueprint(
    "bitacora",
    __name__,
    url_prefix="/bitacora"
)

@bitacora_bp.route("/")
def index():
    return "Bitacora"