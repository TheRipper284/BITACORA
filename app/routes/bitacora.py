from sqlalchemy import or_

from datetime import date, datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from app.models import (
    Empresa,
    Nave,
    Area,
    Personal,
    Auditor,
    RegistroBitacora,
    TipoRequerimiento
)

from app.services.bitacora_service import (
    crear_registro,
    registrar_salida
)

from app.extensions import db

import re


bitacora_bp = Blueprint(
    "bitacora",
    __name__,
    url_prefix="/bitacora"
)


# ============================================================
# INICIO
# ============================================================

@bitacora_bp.route("/")
@login_required
def index():

    from app.models import RegistroBitacora

    registros_activos = (
        RegistroBitacora.query
        .filter(
            RegistroBitacora.hora_salida.is_(None)
        )
        .order_by(
            RegistroBitacora.fecha.desc(),
            RegistroBitacora.hora_entrada.desc()
        )
        .all()
    )

    return render_template(
        "bitacora/index.html",
        usuario=current_user,
        registros_activos=registros_activos
    )


# ============================================================
# REGISTRAR
# ============================================================

@bitacora_bp.route(
    "/registrar",
    methods=["GET", "POST"]
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
                fecha=fecha,
                hora_entrada=hora_entrada,
                soporte=request.form[
                    "soporte"
                ].strip(),
                empresa_id=empresa_id,
                actividad=request.form[
                    "actividad"
                ].strip(),
                nave_id=nave_id,
                area_id=area_id,
                bitacora_lectora=request.form[
                    "bitacora_lectora"
                ].strip(),
                codigo_requerimiento=(
                    request.form[
                        "codigo_requerimiento"
                    ]
                ),
                argonite_anexo1=argonite,
                personal_id=personal_id,
                auditor_id=auditor_id,
                amonestacion=amonestacion,
                comentario=request.form.get(
                    "comentario",
                    ""
                ).strip()
            )

            flash(
                f"Registro {registro.numero} "
                "creado correctamente.",
                "success"
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
        empresas=empresas,
        naves=naves,
        areas=areas,
        personal=personal,
        auditores=auditores
    )


# ============================================================
# API - AREAS POR NAVE
# ============================================================

@bitacora_bp.route(
    "/api/areas/<int:nave_id>"
)
@login_required
def obtener_areas(nave_id):

    areas = (
        Area.query
        .filter_by(
            nave_id=nave_id,
            activo=True
        )
        .order_by(Area.nombre)
        .all()
    )

    return jsonify([
        {
            "id": area.id,
            "nombre": area.nombre
        }
        for area in areas
    ])


# ============================================================
# REGISTRAR SALIDA
# ============================================================

@bitacora_bp.route(
    "/salida/<int:registro_id>",
    methods=["POST"]
)
@login_required
def salida(registro_id):

    from app.models import RegistroBitacora

    registro = db.session.get(
        RegistroBitacora,
        registro_id
    )

    if not registro:

        flash(
            "El registro no existe.",
            "error"
        )

        return redirect(
            url_for("bitacora.index")
        )

    try:

        registrar_salida(registro)

        flash(
            "Hora de salida registrada correctamente.",
            "success"
        )

    except ValueError as error:

        flash(
            str(error),
            "error"
        )

    return redirect(
        url_for("bitacora.index")
    )


# ============================================================
# CONSULTAR
# ============================================================

@bitacora_bp.route("/consultar")
@login_required
def consultar():

    query = RegistroBitacora.query

    fecha_inicio = request.args.get(
        "fecha_inicio",
        ""
    ).strip()

    fecha_fin = request.args.get(
        "fecha_fin",
        ""
    ).strip()

    empresa_id = request.args.get(
        "empresa_id",
        ""
    ).strip()

    nave_id = request.args.get(
        "nave_id",
        ""
    ).strip()

    area_id = request.args.get(
        "area_id",
        ""
    ).strip()

    tipo_id = request.args.get(
        "tipo_id",
        ""
    ).strip()

    personal_id = request.args.get(
        "personal_id",
        ""
    ).strip()

    auditor_id = request.args.get(
        "auditor_id",
        ""
    ).strip()

    codigo = request.args.get(
        "codigo",
        ""
    ).strip().upper()

    # --------------------------------------------------------
    # FECHA INICIO
    # --------------------------------------------------------

    if fecha_inicio:

        fecha = datetime.strptime(
            fecha_inicio,
            "%Y-%m-%d"
        ).date()

        query = query.filter(
            RegistroBitacora.fecha >= fecha
        )

    # --------------------------------------------------------
    # FECHA FIN
    # --------------------------------------------------------

    if fecha_fin:

        fecha = datetime.strptime(
            fecha_fin,
            "%Y-%m-%d"
        ).date()

        query = query.filter(
            RegistroBitacora.fecha <= fecha
        )

    # --------------------------------------------------------
    # EMPRESA
    # --------------------------------------------------------

    if empresa_id:

        query = query.filter(
            RegistroBitacora.empresa_id == int(
                empresa_id
            )
        )

    # --------------------------------------------------------
    # NAVE
    # --------------------------------------------------------

    if nave_id:

        query = query.filter(
            RegistroBitacora.nave_id == int(
                nave_id
            )
        )

    # --------------------------------------------------------
    # AREA
    # --------------------------------------------------------

    if area_id:

        query = query.filter(
            RegistroBitacora.area_id == int(
                area_id
            )
        )

    # --------------------------------------------------------
    # TIPO DE REQUERIMIENTO
    # --------------------------------------------------------

    if tipo_id:

        query = query.filter(
            RegistroBitacora.tipo_requerimiento_id == int(
                tipo_id
            )
        )

    # --------------------------------------------------------
    # PERSONAL
    # --------------------------------------------------------

    if personal_id:

        query = query.filter(
            RegistroBitacora.personal_id == int(
                personal_id
            )
        )

    # --------------------------------------------------------
    # AUDITOR
    # --------------------------------------------------------

    if auditor_id:

        query = query.filter(
            RegistroBitacora.auditor_id == int(
                auditor_id
            )
        )

    # --------------------------------------------------------
    # CODIGO
    # --------------------------------------------------------

    if codigo:

        query = query.filter(
            RegistroBitacora.codigo_requerimiento.ilike(
                f"%{codigo}%"
            )
        )

    # --------------------------------------------------------
    # PAGINACION
    # --------------------------------------------------------

    pagina = request.args.get(
        "pagina",
        1,
        type=int
    )

    if pagina < 1:
        pagina = 1

    paginacion = (
        query
        .order_by(
            RegistroBitacora.fecha.desc(),
            RegistroBitacora.numero.desc()
        )
        .paginate(
            page=pagina,
            per_page=50,
            error_out=False
        )
    )

    # --------------------------------------------------------
    # CATALOGOS
    # --------------------------------------------------------

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

    tipos = (
        TipoRequerimiento.query
        .filter_by(activo=True)
        .order_by(TipoRequerimiento.nombre)
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

    return render_template(
        "bitacora/consultar.html",
        paginacion=paginacion,
        registros=paginacion.items,
        empresas=empresas,
        naves=naves,
        areas=areas,
        tipos=tipos,
        personal=personal,
        auditores=auditores
    )


# ============================================================
# DETALLE
# ============================================================

@bitacora_bp.route(
    "/detalle/<int:registro_id>"
)
@login_required
def detalle(registro_id):

    registro = db.session.get(
        RegistroBitacora,
        registro_id
    )

    if registro is None:

        flash(
            "El registro no existe.",
            "danger"
        )

        return redirect(
            url_for("bitacora.consultar")
        )

    return render_template(
        "bitacora/detalle.html",
        registro=registro
    )


# ============================================================
# EDITAR
# ============================================================

@bitacora_bp.route(
    "/editar/<int:registro_id>",
    methods=["GET", "POST"]
)
@login_required
def editar(registro_id):

    registro = db.session.get(
        RegistroBitacora,
        registro_id
    )

    if registro is None:

        flash(
            "El registro no existe.",
            "danger"
        )

        return redirect(
            url_for("bitacora.consultar")
        )

    # --------------------------------------------------------
    # CATALOGOS
    # --------------------------------------------------------

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

    tipos = (
        TipoRequerimiento.query
        .filter_by(activo=True)
        .order_by(TipoRequerimiento.nombre)
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

    # --------------------------------------------------------
    # POST
    # --------------------------------------------------------

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

            hora_salida = None

            if request.form.get("hora_salida"):

                hora_salida = datetime.strptime(
                    request.form["hora_salida"],
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

            tipo_id = int(
                request.form["tipo_id"]
            )

            personal_id = int(
                request.form["personal_id"]
            )

            auditor_id = int(
                request.form["auditor_id"]
            )

            # ------------------------------------------------
            # VALIDAR AREA
            # ------------------------------------------------

            area = db.session.get(
                Area,
                area_id
            )

            if area is None:

                raise ValueError(
                    "El área seleccionada no existe."
                )

            if area.nave_id != nave_id:

                raise ValueError(
                    "El área no pertenece a la nave seleccionada."
                )

            # ------------------------------------------------
            # VALIDAR CODIGO
            # ------------------------------------------------

            codigo = (
                request.form[
                    "codigo_requerimiento"
                ]
                .strip()
                .upper()
            )

            if not re.fullmatch(
                r"(CR|RR|IR)\d+",
                codigo
            ):

                raise ValueError(
                    "El código debe tener formato "
                    "CR/RR/IR seguido de números."
                )

            tipo_codigo = codigo[:2]

            tipo = db.session.get(
                TipoRequerimiento,
                tipo_id
            )

            if tipo is None:

                raise ValueError(
                    "El tipo de requerimiento no existe."
                )

            if tipo.codigo.upper() != tipo_codigo:

                raise ValueError(
                    "El tipo de requerimiento "
                    "no corresponde al código."
                )

            # ------------------------------------------------
            # ACTUALIZAR REGISTRO
            # ------------------------------------------------

            registro.fecha = fecha

            registro.hora_entrada = hora_entrada

            registro.hora_salida = hora_salida

            registro.soporte = (
                request.form[
                    "soporte"
                ]
                .strip()
            )

            registro.empresa_id = empresa_id

            registro.actividad = (
                request.form[
                    "actividad"
                ]
                .strip()
            )

            registro.nave_id = nave_id

            registro.area_id = area_id

            registro.bitacora_lectora = (
                request.form[
                    "bitacora_lectora"
                ]
                .strip()
            )

            registro.tipo_requerimiento_id = tipo_id

            registro.codigo_requerimiento = codigo

            registro.argonite_anexo1 = (
                request.form.get(
                    "argonite_anexo1"
                ) == "SI"
            )

            registro.personal_id = personal_id

            registro.numero_registro = int(
                request.form[
                    "numero_registro"
                ]
            )

            registro.auditor_id = auditor_id

            registro.amonestacion = int(
                request.form[
                    "amonestacion"
                ]
            )

            registro.comentario = (
                request.form.get(
                    "comentario",
                    ""
                )
                .strip()
            )

            # ------------------------------------------------
            # GUARDAR
            # ------------------------------------------------

            db.session.commit()

            flash(
                "Registro actualizado correctamente.",
                "success"
            )

            return redirect(
                url_for(
                    "bitacora.detalle",
                    registro_id=registro.id
                )
            )

        except (ValueError, KeyError) as error:

            db.session.rollback()

            flash(
                f"No se pudo actualizar el registro: {error}",
                "danger"
            )

    return render_template(
        "bitacora/editar.html",
        registro=registro,
        empresas=empresas,
        naves=naves,
        areas=areas,
        tipos=tipos,
        personal=personal,
        auditores=auditores
    )