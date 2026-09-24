from datetime import date
from io import BytesIO

from openpyxl import Workbook
from openpyxl.utils import get_column_letter

from app.models import RegistroBitacora


def generar_reporte_mensual(mes, año):
    """
    Genera un archivo Excel con todos los registros
    correspondientes al mes y año indicados.

    Retorna:
        archivo: BytesIO con el Excel generado.
        cantidad: número de registros exportados.
    """

    fecha_inicio = date(
        año,
        mes,
        1
    )

    if mes == 12:
        fecha_fin = date(
            año + 1,
            1,
            1
        )
    else:
        fecha_fin = date(
            año,
            mes + 1,
            1
        )

    registros = (
        RegistroBitacora.query
        .filter(
            RegistroBitacora.fecha >= fecha_inicio,
            RegistroBitacora.fecha < fecha_fin
        )
        .order_by(
            RegistroBitacora.fecha.asc(),
            RegistroBitacora.numero.asc()
        )
        .all()
    )

    workbook = Workbook()

    hoja = workbook.active
    hoja.title = "Bitácora"

    encabezados = [
        "No.",
        "Fecha",
        "Soporte",
        "Empresa",
        "Actividad",
        "H. Entrada",
        "H. Salida",
        "No. Mes",
        "CW/Semana",
        "Año",
        "Nave",
        "Área",
        "Bitácora lectora",
        "Tipo requerimiento",
        "IR/RR/CR",
        "Argonite/Anexo 1",
        "Tipo personal",
        "No. Registro",
        "Personal",
        "Auditoría",
        "Amonestación",
        "Comentario"
    ]

    hoja.append(encabezados)

    for registro in registros:
        hoja.append([
            registro.numero,
            registro.fecha,
            registro.soporte,
            registro.empresa,
            registro.actividad,
            registro.hora_entrada,
            registro.hora_salida,
            registro.fecha.month,
            registro.fecha.isocalendar().week,
            registro.fecha.year,
            registro.nave.codigo,
            registro.area.nombre,
            registro.bitacora_lectora,
            registro.tipo_requerimiento.nombre,
            registro.codigo_requerimiento,
            "SI" if registro.argonite_anexo1 else "NO",
            "",
            registro.tipo_personal,
            registro.numero_registro,
            registro.nombre,
            registro.auditor.nombre,
            registro.amonestacion,
            registro.comentario or ""
        ])

    # --------------------------------------------------------
    # FORMATO DE FECHAS Y HORAS
    # --------------------------------------------------------

    for fila in hoja.iter_rows(
        min_row=2
    ):
        fila[1].number_format = "dd/mm/yyyy"
        fila[5].number_format = "hh:mm"
        fila[6].number_format = "hh:mm"

    # --------------------------------------------------------
    # ENCABEZADOS
    # --------------------------------------------------------

    for celda in hoja[1]:
        celda.font = celda.font.copy(
            bold=True
        )

    # --------------------------------------------------------
    # AJUSTAR COLUMNAS
    # --------------------------------------------------------

    for columna in hoja.columns:
        max_length = 0

        numero_columna = columna[0].column

        for celda in columna:
            if celda.value is not None:
                longitud = len(
                    str(celda.value)
                )

                if longitud > max_length:
                    max_length = longitud

        ancho = min(
            max_length + 2,
            40
        )

        hoja.column_dimensions[
            get_column_letter(numero_columna)
        ].width = ancho

    # --------------------------------------------------------
    # CONGELAR ENCABEZADOS
    # --------------------------------------------------------

    hoja.freeze_panes = "A2"

    # --------------------------------------------------------
    # GENERAR ARCHIVO EN MEMORIA
    # --------------------------------------------------------

    archivo = BytesIO()

    workbook.save(archivo)

    archivo.seek(0)

    return archivo, len(registros)