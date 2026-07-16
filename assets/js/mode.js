// ABOUTME: Light/dark toggle: binds the nav's #mode-toggle button, persists the override in localStorage,
// ABOUTME: and keeps the button label naming the mode you'd switch to (labels arrive via data-label-* attributes).
(function () {
    var root = document.documentElement;
    var btn = document.getElementById("mode-toggle");
    if (!btn) {
        return;
    }
    var media = window.matchMedia("(prefers-color-scheme: dark)");

    function effectiveMode() {
        if (root.dataset.mode === "dark" || root.dataset.mode === "light") {
            return root.dataset.mode;
        }
        return media.matches ? "dark" : "light";
    }

    function renderLabel() {
        var next = effectiveMode() === "dark" ? "light" : "dark";
        var label = next === "dark" ? btn.dataset.labelDark : btn.dataset.labelLight;
        btn.textContent = "◐ " + label;
    }

    btn.addEventListener("click", function () {
        var next = effectiveMode() === "dark" ? "light" : "dark";
        root.dataset.mode = next;
        try {
            localStorage.setItem("mode", next);
        } catch (e) {
            /* private browsing: the override just won't persist */
        }
        renderLabel();
    });

    if (typeof media.addEventListener === "function") {
        media.addEventListener("change", renderLabel);
    }
    renderLabel();
})();
