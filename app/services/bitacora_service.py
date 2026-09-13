from datetime import date, time
from app.extensions import db
from app.models import (RegistroBitacora, TipoRequerimiento)

def obtener_siguiente_numero(fecha):
    ultimo = (
        RegistroBitacora.query
        .filter_by(fecha=fecha)
        .order_by(
            RegistroBitacora.numero.desc()
        )
        .first()
    )

    if ultimo:
        return ultimo.numero + 1
    return 1

def obtener_tipo_requerimiento(codigo):
    codigo = codigo.strip().upper()

    if codigo.startswith("CR"):
        prefijo = "CR"
    elif codigo.startswith("IR"):
        prefijo = "IR"
    elif codigo.startswith("RR"):
        prefijo = "RR"

    else:
        raise ValueError(
            "El codigo debe de comenzar con CR, IR o RR."
        )

    tipo = TipoRequerimiento.query.filter_by(
        codigo=prefijo
    ).first()

    if not tipo:
        raise ValueError(
            "El tipi de requerimiento non existe."
        )

    return tipo

def crear_registro(
        fecha,
        hora_entrada,
        soporte,
        empresa_id,
        actividad,
        nave_id,
        area_id,
        bitacora_lectora,
        codigo_requerimiento,
        argonite_anexo1,
        personal_id,
        auditor_id,
        amonestacion,
        comentario
):

    tipo_requerimiento = obtener_tipo_requerimiento(
        codigo_requerimiento
    )

    numero = obtener_siguiente_numero(
        fecha
    )

    registro = RegistroBitacora(
        numero = numero,
        fecha = fecha,
        hora_entrada = hora_entrada,
        soporte = soporte,
        empresa_id = empresa_id,
        actividad = actividad,
        nave_id = nave_id,
        area_id = area_id,
        bitacora_lectora = bitacora_lectora,
        tipo_requerimiento_id = (tipo_requerimiento.id
    ),

        codigo_requerimiento = (
            codigo_requerimiento.strip().upper()
        ),

        argonite_anexo1 = argonite_anexo1,
        personal_id = personal_id,
        numero_registro = 1,
        auditor_id = auditor_id,
        amonestacion = amonestacion,
        comentario = comentario
    )

    db.session.add(registro)
    db.session.commit()

    return registro