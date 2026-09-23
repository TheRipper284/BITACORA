from datetime import datetime
import re

from app.extensions import db

from app.models import (
    RegistroBitacora,
    TipoRequerimiento,
    Area,
    Nave,
    Auditor
)


# ============================================================
# NUMERO CONSECUTIVO
# ============================================================

def obtener_siguiente_numero(fecha):

    ultimo = (
        RegistroBitacora.query
        .filter_by(
            fecha=fecha
        )
        .order_by(
            RegistroBitacora.numero.desc()
        )
        .first()
    )

    if ultimo:
        return ultimo.numero + 1

    return 1


# ============================================================
# TIPO DE REQUERIMIENTO
# ============================================================

def obtener_tipo_requerimiento(codigo):

    codigo = codigo.strip().upper()

    if not re.fullmatch(
        r"(CR|IR|RR)\d+",
        codigo
    ):
        raise ValueError(
            "El código debe tener formato "
            "CR21308038, IR21308038 o RR21308038."
        )

    prefijo = codigo[:2]

    tipo = (
        TipoRequerimiento.query
        .filter_by(
            codigo=prefijo,
            activo=True
        )
        .first()
    )

    if not tipo:
        raise ValueError(
            "El tipo de requerimiento no existe "
            "o está inactivo."
        )

    return tipo


# ============================================================
# VALIDAR AREA
# ============================================================

def validar_area(area_id, nave_id):

    area = (
        Area.query
        .filter_by(
            id=area_id,
            nave_id=nave_id,
            activo=True
        )
        .first()
    )

    if not area:
        raise ValueError(
            "El área seleccionada no existe, "
            "está inactiva o no pertenece a la nave."
        )

    return area


# ============================================================
# VALIDAR AUDITOR
# ============================================================

def validar_auditor(
    auditor_id,
    nave_id,
    area_id
):

    auditor = (
        Auditor.query
        .filter_by(
            id=auditor_id,
            nave_id=nave_id,
            area_id=area_id,
            activo=True
        )
        .first()
    )

    if not auditor:
        raise ValueError(
            "El auditor seleccionado no pertenece "
            "a la nave y área seleccionadas."
        )

    return auditor


# ============================================================
# VALIDAR CATALOGOS
# ============================================================

def validar_catalogos(
    nave_id,
    area_id,
    auditor_id
):

    nave = db.session.get(
        Nave,
        nave_id
    )

    if not nave or not nave.activo:
        raise ValueError(
            "La nave seleccionada no existe "
            "o está inactiva."
        )

    validar_area(
        area_id=area_id,
        nave_id=nave_id
    )

    auditor = validar_auditor(
        auditor_id=auditor_id,
        nave_id=nave_id,
        area_id=area_id
    )

    return nave, auditor


# ============================================================
# CREAR REGISTRO
# ============================================================

def crear_registro(
    fecha,
    hora_entrada,
    soporte,
    empresa,
    actividad,
    nave_id,
    area_id,
    bitacora_lectora,
    codigo_requerimiento,
    argonite_anexo1,
    tipo_personal,
    nombre,
    auditor_id,
    amonestacion,
    comentario
):

    # --------------------------------------------------------
    # EMPRESA
    # --------------------------------------------------------

    empresa = empresa.strip()

    if not empresa:
        raise ValueError(
            "La empresa es obligatoria."
        )

    if len(empresa) > 150:
        raise ValueError(
            "La empresa no puede superar "
            "los 150 caracteres."
        )

    # --------------------------------------------------------
    # TIPO DE PERSONA
    # --------------------------------------------------------

    tipo_personal = tipo_personal.strip()

    if tipo_personal not in (
        "Usuario",
        "Visitante"
    ):
        raise ValueError(
            "El tipo de persona no es válido."
        )

    # --------------------------------------------------------
    # NOMBRE
    # --------------------------------------------------------

    nombre = nombre.strip()

    if not nombre:
        raise ValueError(
            "El nombre de la persona es obligatorio."
        )

    if len(nombre) > 150:
        raise ValueError(
            "El nombre no puede superar "
            "los 150 caracteres."
        )

    # --------------------------------------------------------
    # CODIGO
    # --------------------------------------------------------

    codigo_requerimiento = (
        codigo_requerimiento
        .strip()
        .upper()
    )

    tipo_requerimiento = (
        obtener_tipo_requerimiento(
            codigo_requerimiento
        )
    )

    # --------------------------------------------------------
    # CATALOGOS
    # --------------------------------------------------------

    validar_catalogos(
        nave_id=nave_id,
        area_id=area_id,
        auditor_id=auditor_id
    )

    # --------------------------------------------------------
    # NUMERO
    # --------------------------------------------------------

    numero = obtener_siguiente_numero(
        fecha
    )

    # --------------------------------------------------------
    # REGISTRO
    # --------------------------------------------------------

    registro = RegistroBitacora(

        numero=numero,

        fecha=fecha,

        hora_entrada=hora_entrada,

        soporte=soporte,

        empresa=empresa,

        actividad=actividad,

        nave_id=nave_id,

        area_id=area_id,

        bitacora_lectora=bitacora_lectora,

        tipo_requerimiento_id=tipo_requerimiento.id,

        codigo_requerimiento=codigo_requerimiento,

        argonite_anexo1=argonite_anexo1,

        tipo_personal=tipo_personal,

        nombre=nombre,

        numero_registro=1,

        auditor_id=auditor_id,

        amonestacion=amonestacion,

        comentario=comentario
    )

    try:

        db.session.add(
            registro
        )

        db.session.commit()

    except Exception:

        db.session.rollback()

        raise

    return registro


# ============================================================
# REGISTRAR SALIDA
# ============================================================

def registrar_salida(registro):

    if registro.hora_salida is not None:

        raise ValueError(
            "Este registro ya tiene hora de salida."
        )

    ahora = datetime.now()

    registro.hora_salida = (
        ahora.time()
    )

    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        raise

    return registro