from flask import render_template, request, redirect, url_for, flash

from app.routes.admin import admin_bp
from app.routes.auth import admin_required

from app.extensions import db
from app.models import Nave, Area, Empresa, TipoPersonal, TipoRequerimiento


def _redirect_catalogos():
    return redirect(url_for("admin.catalogos"))


@admin_bp.route("/catalogos")
@admin_required
def catalogos():
    naves = (
        Nave.query.order_by(Nave.activo.desc(), Nave.codigo).all()
    )
    empresas = (
        Empresa.query.order_by(Empresa.activo.desc(), Empresa.nombre).all()
    )
    tipos_personal = (
        TipoPersonal.query.order_by(
            TipoPersonal.activo.desc(),
            TipoPersonal.nombre,
        ).all()
    )
    tipos_requerimiento = (
        TipoRequerimiento.query.order_by(
            TipoRequerimiento.activo.desc(),
            TipoRequerimiento.codigo,
        ).all()
    )
    return render_template(
        "admin/catalogos.html",
        naves=naves,
        empresas=empresas,
        tipos_personal=tipos_personal,
        tipos_requerimiento=tipos_requerimiento,
    )


@admin_bp.route("/catalogos/nave", methods=["POST"])
@admin_required
def agregar_nave():
    try:
        codigo = request.form.get("codigo", "").strip().upper()
        if not codigo or len(codigo) > 20:
            raise ValueError("Código de nave inválido.")
        if Nave.query.filter_by(codigo=codigo).first():
            raise ValueError("Ya existe una nave con ese código.")
        db.session.add(Nave(codigo=codigo, activo=True))
        db.session.commit()
        flash("Nave agregada correctamente.", "success")
    except ValueError as error:
        db.session.rollback()
        flash(str(error), "error")
    except Exception:
        db.session.rollback()
        flash("No fue posible agregar la nave.", "error")
    return _redirect_catalogos()


@admin_bp.route("/catalogos/nave/<int:nave_id>/toggle", methods=["POST"])
@admin_required
def toggle_nave(nave_id):
    nave = db.session.get(Nave, nave_id)
    if not nave:
        flash("La nave no existe.", "error")
        return _redirect_catalogos()
    nave.activo = not nave.activo
    db.session.commit()
    flash("Estado de nave actualizado.", "success")
    return _redirect_catalogos()


@admin_bp.route("/catalogos/area", methods=["POST"])
@admin_required
def agregar_area():
    try:
        nave_id = int(request.form["nave_id"])
        nombre = request.form.get("nombre", "").strip().upper()
        if not nombre or len(nombre) > 50:
            raise ValueError("Nombre de área inválido.")
        nave = db.session.get(Nave, nave_id)
        if not nave or not nave.activo:
            raise ValueError("Nave no válida.")
        existe = Area.query.filter_by(nave_id=nave_id, nombre=nombre).first()
        if existe:
            if not existe.activo:
                existe.activo = True
                db.session.commit()
                flash("Área reactivada.", "success")
                return _redirect_catalogos()
            raise ValueError("El área ya existe en esa nave.")
        db.session.add(Area(nave_id=nave_id, nombre=nombre, activo=True))
        db.session.commit()
        flash("Área agregada correctamente.", "success")
    except ValueError as error:
        db.session.rollback()
        flash(str(error), "error")
    except Exception:
        db.session.rollback()
        flash("No fue posible agregar el área.", "error")
    return _redirect_catalogos()


@admin_bp.route("/catalogos/area/<int:area_id>/toggle", methods=["POST"])
@admin_required
def toggle_area(area_id):
    area = db.session.get(Area, area_id)
    if not area:
        flash("El área no existe.", "error")
        return _redirect_catalogos()
    area.activo = not area.activo
    db.session.commit()
    flash("Estado de área actualizado.", "success")
    return _redirect_catalogos()


@admin_bp.route("/catalogos/empresa", methods=["POST"])
@admin_required
def agregar_empresa():
    try:
        nombre = request.form.get("nombre", "").strip()
        if not nombre or len(nombre) > 100:
            raise ValueError("Nombre de empresa inválido.")
        existente = Empresa.query.filter_by(nombre=nombre).first()
        if existente:
            if not existente.activo:
                existente.activo = True
                db.session.commit()
                flash("Empresa reactivada.", "success")
                return _redirect_catalogos()
            raise ValueError("La empresa ya existe.")
        db.session.add(Empresa(nombre=nombre, activo=True))
        db.session.commit()
        flash("Empresa agregada correctamente.", "success")
    except ValueError as error:
        db.session.rollback()
        flash(str(error), "error")
    except Exception:
        db.session.rollback()
        flash("No fue posible agregar la empresa.", "error")
    return _redirect_catalogos()


@admin_bp.route("/catalogos/empresa/<int:empresa_id>/toggle", methods=["POST"])
@admin_required
def toggle_empresa(empresa_id):
    empresa = db.session.get(Empresa, empresa_id)
    if not empresa:
        flash("La empresa no existe.", "error")
        return _redirect_catalogos()
    empresa.activo = not empresa.activo
    db.session.commit()
    flash("Estado de empresa actualizado.", "success")
    return _redirect_catalogos()


@admin_bp.route("/catalogos/tipo-personal", methods=["POST"])
@admin_required
def agregar_tipo_personal():
    try:
        nombre = request.form.get("nombre", "").strip()
        if not nombre or len(nombre) > 50:
            raise ValueError("Nombre inválido.")
        if TipoPersonal.query.filter_by(nombre=nombre).first():
            raise ValueError("El tipo de personal ya existe.")
        db.session.add(TipoPersonal(nombre=nombre, activo=True))
        db.session.commit()
        flash("Tipo de personal agregado.", "success")
    except ValueError as error:
        db.session.rollback()
        flash(str(error), "error")
    except Exception:
        db.session.rollback()
        flash("No fue posible agregar el tipo.", "error")
    return _redirect_catalogos()


@admin_bp.route(
    "/catalogos/tipo-personal/<int:tipo_id>/toggle",
    methods=["POST"],
)
@admin_required
def toggle_tipo_personal(tipo_id):
    tipo = db.session.get(TipoPersonal, tipo_id)
    if not tipo:
        flash("El tipo no existe.", "error")
        return _redirect_catalogos()
    tipo.activo = not tipo.activo
    db.session.commit()
    flash("Estado actualizado.", "success")
    return _redirect_catalogos()


@admin_bp.route("/catalogos/tipo-requerimiento", methods=["POST"])
@admin_required
def agregar_tipo_requerimiento():
    try:
        codigo = request.form.get("codigo", "").strip().upper()
        nombre = request.form.get("nombre", "").strip()
        if not codigo or len(codigo) > 10:
            raise ValueError("Código inválido.")
        if not nombre or len(nombre) > 100:
            raise ValueError("Nombre inválido.")
        if TipoRequerimiento.query.filter_by(codigo=codigo).first():
            raise ValueError("El código ya existe.")
        db.session.add(
            TipoRequerimiento(codigo=codigo, nombre=nombre, activo=True)
        )
        db.session.commit()
        flash("Tipo de requerimiento agregado.", "success")
    except ValueError as error:
        db.session.rollback()
        flash(str(error), "error")
    except Exception:
        db.session.rollback()
        flash("No fue posible agregar el tipo.", "error")
    return _redirect_catalogos()


@admin_bp.route(
    "/catalogos/tipo-requerimiento/<int:tipo_id>/toggle",
    methods=["POST"],
)
@admin_required
def toggle_tipo_requerimiento(tipo_id):
    tipo = db.session.get(TipoRequerimiento, tipo_id)
    if not tipo:
        flash("El tipo no existe.", "error")
        return _redirect_catalogos()
    tipo.activo = not tipo.activo
    db.session.commit()
    flash("Estado actualizado.", "success")
    return _redirect_catalogos()
