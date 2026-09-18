/* ########################################################################## */
/* ################################### INFO ################################# */
/* ########################################################################## */

/* This script magnifies the class diagrams of the documentation when they are
   hovered: the diagram is scaled up in place, around the position of the cursor,
   and clipped to its original frame, so that the area under the cursor becomes
   readable. Moving the cursor moves the magnified area, and leaving the diagram
   restores it. Links of the diagram stay clickable while it is magnified. */

/* ########################################################################## */
/* ################################# CONTENTS ############################### */
/* ########################################################################## */

document.addEventListener("DOMContentLoaded", () => {

    // The diagram is magnified up to its natural size (one pixel per unit of its viewBox), but at least a bit
    const MINIMUM_ZOOM = 1.5;
    const MAXIMUM_ZOOM = 4.0;

    for (const container of document.querySelectorAll(".class-diagram")) {

        // Inline SVG of the diagram
        const svg = container.querySelector("svg");
        if (!svg || !svg.viewBox || !svg.viewBox.baseVal) {
            continue;
        }
        const naturalWidth = svg.viewBox.baseVal.width;

        // Magnify around the cursor
        container.addEventListener("mousemove", (event) => {
            const frame = container.getBoundingClientRect();
            if (frame.width === 0) {
                return;
            }
            const x = (event.clientX - frame.left) / frame.width * 100;
            const y = (event.clientY - frame.top) / frame.height * 100;
            const zoom = Math.min(MAXIMUM_ZOOM, Math.max(MINIMUM_ZOOM, naturalWidth / frame.width));
            svg.style.transformOrigin = `${x}% ${y}%`;
            svg.style.transform = `scale(${zoom})`;
            container.classList.add("is-magnified");
        });

        // Restore the diagram when the cursor leaves it
        container.addEventListener("mouseleave", () => {
            svg.style.transform = "";
            container.classList.remove("is-magnified");
        });
    }
});

/* ########################################################################## */
/* ########################################################################## */
