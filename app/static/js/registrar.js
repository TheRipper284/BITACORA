/**
 * Formulario registrar: nave → área → auditores
 */
(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        const naveSelect = document.getElementById("nave_id");
        const areaSelect = document.getElementById("area_id");
        const auditorSelect = document.getElementById("auditor_id");

        if (!naveSelect || !areaSelect || !auditorSelect) {
            return;
        }

        const api = window.BitacoraNaveArea;

        async function cargarAuditores() {
            const naveId = naveSelect.value;
            const areaId = areaSelect.value;

            api.clearSelect(auditorSelect, "Selecciona nave y área");
            auditorSelect.disabled = true;

            if (!naveId || !areaId) {
                return;
            }

            try {
                const response = await fetch(
                    `/bitacora/api/auditores/${naveId}/${areaId}`
                );

                if (!response.ok) {
                    throw new Error(
                        "No fue posible cargar los auditores."
                    );
                }

                const auditores = await response.json();

                if (auditores.length === 0) {
                    api.clearSelect(
                        auditorSelect,
                        "No hay auditores asignados"
                    );
                    return;
                }

                api.fillSelect(
                    auditorSelect,
                    auditores,
                    "Seleccionar auditor",
                    "nombre"
                );
                auditorSelect.disabled = false;
            } catch (error) {
                console.error(error);
                api.clearSelect(
                    auditorSelect,
                    "Error al cargar auditores"
                );
            }
        }

        function limpiarAuditor() {
            api.clearSelect(auditorSelect, "Selecciona nave y área");
            auditorSelect.disabled = true;
        }

        api.bindNaveAreaCascade(naveSelect, areaSelect, {
            onAreaCleared: limpiarAuditor,
        });

        areaSelect.addEventListener("change", cargarAuditores);
    });
})();
