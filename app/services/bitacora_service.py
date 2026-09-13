from datetime import date, time, datetime
from app.extensions import db
from app.models import (RegistroBitacora, TipoRequerimiento, Area)
import re

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

    if not re.fullmatch(
        r"(CR|IR|RR)\d+",
        codigo
    ):
        raise ValueError(
            "El código debe tener formato "
            "CR21308038, IR21308038 o RR21308038."
        )

    prefijo = codigo[:2]

    tipo = TipoRequerimiento.query.filter_by(
        codigo = prefijo
    ).first()

    if not tipo:
        raise ValueError(
            "El tipo de requerimineto no existe."
        )

    return tipo

def validar_area(area_id, nave_id):

    area = Area.query.filter_by(
        id=area_id,
        nave_id=nave_id,
        activo=True
    ).first()

    if not area:
        raise ValueError(
            "El área seleccionada no pertenece a la nave."
        )

    return area

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

def registrar_salida(registro):
    if registro.hora_salida is not None:
        raise ValueError(
            "Este registro ya tiene hora de salida."
        )

    ahora = datetime.now()

    registro.hora_salida = ahora.time()

    db.session.commit()

    return registro