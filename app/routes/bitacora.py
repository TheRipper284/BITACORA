from flask import Blueprint, render_template
from flask_login import login_required,current_user

bitacora_bp = Blueprint(
    "bitacora",
    __name__,
    url_prefix="/bitacora"
)

@bitacora_bp.route("/")
@login_required
def index():

    return render_template(
        "bitacora/index.html",
        usuario=current_user
    )