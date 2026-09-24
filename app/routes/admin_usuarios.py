from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user

from app.routes.admin import admin_bp
from app.routes.auth import admin_required

from app.extensions import db
from app.models.usuario import Usuario


def _redirect_usuarios():
    return redirect(url_for("admin.usuarios"))


@admin_bp.route("/usuarios")
@admin_required
def usuarios():
    lista = (
        Usuario.query.order_by(
            Usuario.activo.desc(),
            Usuario.usuario,
        ).all()
    )
    return render_template("admin/usuarios.html", usuarios=lista)


@admin_bp.route("/usuarios/agregar", methods=["POST"])
@admin_required
def agregar_usuario():
    try:
        nombre = request.form.get("nombre", "").strip()
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")
        rol = request.form.get("rol", "").strip().upper()

        if not nombre or len(nombre) > 150:
            raise ValueError("Nombre inválido.")
        if not usuario or len(usuario) > 50:
            raise ValueError("Usuario inválido.")
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        if rol not in ("ADMIN", "REGISTRADOR"):
            raise ValueError("Rol inválido.")

        if Usuario.query.filter_by(usuario=usuario).first():
            raise ValueError("Ese nombre de usuario ya existe.")

        nuevo = Usuario(
            nombre=nombre,
            usuario=usuario,
            rol=rol,
            activo=True,
        )
        nuevo.establecer_password(password)
        db.session.add(nuevo)
        db.session.commit()
        flash("Usuario creado correctamente.", "success")
    except ValueError as error:
        db.session.rollback()
        flash(str(error), "error")
    except Exception:
        db.session.rollback()
        flash("No fue posible crear el usuario.", "error")
    return _redirect_usuarios()


@admin_bp.route("/usuarios/<int:usuario_id>/toggle", methods=["POST"])
@admin_required
def toggle_usuario(usuario_id):
    usuario = db.session.get(Usuario, usuario_id)
    if not usuario:
        flash("El usuario no existe.", "error")
        return _redirect_usuarios()
    if usuario.id == current_user.id:
        flash("No puedes desactivar tu propia cuenta.", "error")
        return _redirect_usuarios()
    usuario.activo = not usuario.activo
    db.session.commit()
    flash("Estado de usuario actualizado.", "success")
    return _redirect_usuarios()


@admin_bp.route("/usuarios/<int:usuario_id>/password", methods=["POST"])
@admin_required
def restablecer_password(usuario_id):
    try:
        password = request.form.get("password", "")
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        usuario = db.session.get(Usuario, usuario_id)
        if not usuario:
            raise ValueError("El usuario no existe.")
        usuario.establecer_password(password)
        db.session.commit()
        flash("Contraseña actualizada.", "success")
    except ValueError as error:
        db.session.rollback()
        flash(str(error), "error")
    except Exception:
        db.session.rollback()
        flash("No fue posible actualizar la contraseña.", "error")
    return _redirect_usuarios()
