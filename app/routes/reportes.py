from flask import (
    Blueprint,
    request,
    send_file,
    abort
)

from app.routes.auth import admin_required
from app.services.reportes_service import generar_reporte_mensual


reportes_bp = Blueprint(
    "reportes",
    __name__,
    url_prefix="/reportes"
)


@reportes_bp.route("/exportar", methods=["GET"])
@admin_required
def exportar():
    # ==========================================
    # OBTENER MES Y AÑO
    # ==========================================

    mes = request.args.get("mes", type=int)
    año = request.args.get("año", type=int)

    # ==========================================
    # VALIDAR PARAMETROS
    # ==========================================

    if mes is None or año is None:
        abort(400, "Debes indicar mes y año.")

    if mes < 1 or mes > 12:
        abort(400, "El mes debe estar entre 1 y 12.")

    if año < 2000 or año > 2100:
        abort(400, "El año no es válido.")

    # ==========================================
    # GENERAR EXCEL
    # ==========================================

    archivo, cantidad = generar_reporte_mensual(
        mes,
        año
    )

    # ==========================================
    # DESCARGAR ARCHIVO
    # ==========================================

    return send_file(
        archivo,
        as_attachment=True,
        download_name=f"bitacora_{año}_{mes:02d}.xlsx",
        mimetype=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )