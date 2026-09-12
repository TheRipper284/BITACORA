from flask import Blueprint, render_template
from flask_login import current_user

from app.routes.auth import admin_required

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

@admin_bp.route("/")
@admin_required
def index():

    return render_template(
        "admin/index.html",
        usuario=current_user
    )