from datetime import date, datetime
from flask import (Blueprint, render_template, request, redirect, url_for, flash)
from flask_login import (login_required, current_user)
from app.models import (Empresa, Nave, Area, Personal, Auditor)
from app.services.bitacora_service import (crear_registro)

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

@bitacora_bp.route(
    "/registrar",
    methods = ["GET", "POST"]
)
@login_required
def registrar():

    empresas = (
        Empresa.query
        .filter_by(activo=True)
        .order_by(Empresa.nombre)
        .all()
    )

    naves = (
        Nave.query
        .filter_by(activo=True)
        .order_by(Nave.codigo)
        .all()
    )

    areas = (
        Area.query
        .filter_by(activo=True)
        .order_by(Area.nombre)
        .all()
    )

    personal = (
        Personal.query
        .filter_by(activo=True)
        .order_by(Personal.nombre)
        .all()
    )

    auditores = (
        Auditor.query
        .filter_by(activo=True)
        .order_by(Auditor.nombre)
        .all()
    )

    if request.method == "POST":

        try:

            fecha = datetime.strptime(
                request.form["fecha"],
                "%Y-%m-%d"
            ).date()

            hora_entrada = datetime.strptime(
                request.form["hora_entrada"],
                "%H:%M"
            ).time()

            empresa_id = int(
                request.form["empresa_id"]
            )

            nave_id = int(
                request.form["nave_id"]
            )

            area_id = int(
                request.form["area_id"]
            )

            personal_id = int(
                request.form["personal_id"]
            )

            auditor_id = int(
                request.form["auditor_id"]
            )

            argonite = (
                request.form.get(
                    "argonite_anexo1"
                ) == "SI"
            )

            amonestacion = int(
                request.form.get(
                    "amonestacion",
                    0
                )
            )

            registro = crear_registro(
                fecha = fecha,

                hora_entrada = hora_entrada,

                soporte = request.form[
                    "soporte"
                ].strip(),

                empresa_id = empresa_id,

                actividad = request.form[
                    "actividad"
                ].strip(),

                nave_id = nave_id,

                area_id = area_id,

                bitacora_lectora = request.form[
                    "bitacora_lectora"
                ].strip(),

                codigo_requerimiento = (
                    request.form[
                        "codigo_requerimiento"
                    ]
                ),

                argonite_anexo1 = argonite,

                personal_id = personal_id,

                auditor_id = auditor_id,

                amonestacion = amonestacion,

                comentario = request.form.get(
                    "comentario",
                    ""
                ).strip()
            )

            flash(
                f"Registro {registro.numero} "
                "creado correctamente.",
                "succes"
            )

            return redirect(
                url_for(
                    "bitacora.registrar"
                )
            )

        except ValueError as error:

            flash(
                str(error),
                "error"
            )

        except Exception as error:
            print("ERROR AL CREAR REGISTRO:")
            print(type(error).__name__)
            print(error)

            flash(
                f"No fue posible crear tu registro: {error}",
                "error"
        )

    return render_template(
        "bitacora/registrar.html",
        empresas = empresas,
        naves = naves,
        areas = areas,
        personal = personal,
        auditores = auditores
    )