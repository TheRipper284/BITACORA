/**
 * Cascada nave → áreas (API /bitacora/api/areas/:naveId)
 */
(function (global) {
    "use strict";

    async function fetchAreas(naveId) {
        const response = await fetch(
            `/bitacora/api/areas/${naveId}`
        );

        if (!response.ok) {
            throw new Error("No fue posible cargar las áreas.");
        }

        return response.json();
    }

    function clearSelect(selectEl, placeholder) {
        selectEl.innerHTML = "";
        const option = document.createElement("option");
        option.value = "";
        option.textContent = placeholder;
        selectEl.appendChild(option);
    }

    function fillSelect(selectEl, items, placeholder, labelKey) {
        clearSelect(selectEl, placeholder);

        items.forEach(function (item) {
            const option = document.createElement("option");
            option.value = item.id;
            option.textContent = item[labelKey];
            selectEl.appendChild(option);
        });
    }

    /**
     * @param {HTMLSelectElement} naveSelect
     * @param {HTMLSelectElement} areaSelect
     * @param {{ onAreaCleared?: function, onAreasLoaded?: function }} hooks
     */
    function bindNaveAreaCascade(naveSelect, areaSelect, hooks) {
        if (!naveSelect || !areaSelect) {
            return;
        }

        const onAreaCleared = hooks && hooks.onAreaCleared;
        const onAreasLoaded = hooks && hooks.onAreasLoaded;

        naveSelect.addEventListener("change", async function () {
            const naveId = this.value;

            clearSelect(areaSelect, "Selecciona primero una nave");
            areaSelect.disabled = true;

            if (onAreaCleared) {
                onAreaCleared();
            }

            if (!naveId) {
                return;
            }

            try {
                const areas = await fetchAreas(naveId);
                fillSelect(
                    areaSelect,
                    areas,
                    "Seleccionar área",
                    "nombre"
                );
                areaSelect.disabled = false;

                if (onAreasLoaded) {
                    onAreasLoaded();
                }
            } catch (error) {
                console.error(error);
                alert("No fue posible cargar las áreas.");
            }
        });
    }

    global.BitacoraNaveArea = {
        bindNaveAreaCascade: bindNaveAreaCascade,
        fetchAreas: fetchAreas,
        clearSelect: clearSelect,
        fillSelect: fillSelect,
    };
})(window);
