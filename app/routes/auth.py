from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user,logout_user, current_user, login_required

from app.models.usuario import Usuario

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("bitacora.index"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")

        usuario_db = Usuario.query.filter_by(
            usuario=usuario
        ).first()

        if not usuario_db:

            flash(
                "Usuario o contraseña incorrecta.",
                "error"
            )

            return render_template(
                "auth/login.html"
            )

        if not usuario_db.activo:

            flash(
                "El usuario está desactivado.",
                "error"
            )

            return render_template(
                "auth/login.html"
            )

        if not usuario_db.verificar_password(password):
            flash(
                "Usuario o contraseña incorrecta.",
                "error"
            )

            return render_template(
                "auth/login.html"
            )

        login_user(usuario_db)

        return redirect(
            url_for("bitacora.index")
        )

    return render_template(
        "auth/login.html"
    )

@auth_bp.route("/logout")
def logout():

    logout_user()

    return redirect(
        url_for("auth.login")
    )

def admin_required(view):

    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwarps):

        if not current_user.es_admin():

            abort(403)

        return view(*args, **kwarps)

    return wrapped_view