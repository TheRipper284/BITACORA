/**
 * Admin auditores: cascada nave → área al agregar
 */
(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        const naveSelect = document.getElementById("nave_id");
        const areaSelect = document.getElementById("area_id");

        if (!naveSelect || !areaSelect || !window.BitacoraNaveArea) {
            return;
        }

        window.BitacoraNaveArea.bindNaveAreaCascade(
            naveSelect,
            areaSelect
        );
    });
})();
