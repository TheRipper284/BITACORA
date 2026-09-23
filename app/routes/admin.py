from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import current_user

from app.routes.auth import admin_required

from app.extensions import db

from app.models import (
    Auditor,
    Nave,
    Area
)


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# ============================================================
# INICIO ADMIN
# ============================================================

@admin_bp.route("/")
@admin_required
def index():

    return render_template(
        "admin/index.html",
        usuario=current_user
    )


# ============================================================
# AUDITORES
# ============================================================

@admin_bp.route("/auditores")
@admin_required
def auditores():

    lista = (
        Auditor.query
        .order_by(
            Auditor.activo.desc(),
            Auditor.nombre
        )
        .all()
    )

    naves = (
        Nave.query
        .filter_by(
            activo=True
        )
        .order_by(
            Nave.codigo
        )
        .all()
    )

    return render_template(
        "admin/auditores.html",
        auditores=lista,
        naves=naves
    )


# ============================================================
# AGREGAR AUDITOR
# ============================================================

@admin_bp.route(
    "/auditores/agregar",
    methods=["POST"]
)
@admin_required
def agregar_auditor():

    try:

        nombre = (
            request.form[
                "nombre"
            ]
            .strip()
        )

        nave_id = int(
            request.form[
                "nave_id"
            ]
        )

        area_id = int(
            request.form[
                "area_id"
            ]
        )


        if not nombre:

            raise ValueError(
                "El nombre del auditor es obligatorio."
            )


        if len(nombre) > 150:

            raise ValueError(
                "El nombre no puede superar "
                "los 150 caracteres."
            )


        nave = db.session.get(
            Nave,
            nave_id
        )

        if not nave or not nave.activo:

            raise ValueError(
                "La nave seleccionada no existe "
                "o está inactiva."
            )


        area = db.session.get(
            Area,
            area_id
        )

        if not area or not area.activo:

            raise ValueError(
                "El área seleccionada no existe "
                "o está inactiva."
            )


        if area.nave_id != nave_id:

            raise ValueError(
                "El área no pertenece "
                "a la nave seleccionada."
            )


        existente = (
            Auditor.query
            .filter_by(
                nombre=nombre
            )
            .first()
        )


        if existente:

            if existente.activo:

                raise ValueError(
                    "Ya existe un auditor "
                    "con ese nombre."
                )


            existente.nave_id = nave_id

            existente.area_id = area_id

            existente.activo = True

            db.session.commit()

            flash(
                "El auditor fue reactivado correctamente.",
                "success"
            )

            return redirect(
                url_for(
                    "admin.auditores"
                )
            )


        auditor = Auditor(

            nombre=nombre,

            nave_id=nave_id,

            area_id=area_id,

            activo=True
        )


        db.session.add(
            auditor
        )

        db.session.commit()


        flash(
            "Auditor agregado correctamente.",
            "success"
        )


    except ValueError as error:

        db.session.rollback()

        flash(
            str(error),
            "error"
        )


    except Exception as error:

        db.session.rollback()

        print(
            "ERROR AL AGREGAR AUDITOR:"
        )

        print(
            type(error).__name__
        )

        print(error)

        flash(
            "No fue posible agregar el auditor.",
            "error"
        )


    return redirect(
        url_for(
            "admin.auditores"
        )
    )


# ============================================================
# DESACTIVAR AUDITOR
# ============================================================

@admin_bp.route(
    "/auditores/<int:auditor_id>/eliminar",
    methods=["POST"]
)
@admin_required
def eliminar_auditor(
    auditor_id
):

    auditor = db.session.get(
        Auditor,
        auditor_id
    )


    if not auditor:

        flash(
            "El auditor no existe.",
            "error"
        )

        return redirect(
            url_for(
                "admin.auditores"
            )
        )


    auditor.activo = False

    db.session.commit()


    flash(
        "Auditor desactivado correctamente.",
        "success"
    )


    return redirect(
        url_for(
            "admin.auditores"
        )
    )