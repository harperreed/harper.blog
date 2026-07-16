// ABOUTME: Pre-paint dark-mode guard: applies the persisted light/dark override before first render.
// ABOUTME: Loaded synchronously in <head> as an external file because the CSP forbids inline scripts.
(function () {
    try {
        var m = localStorage.getItem("mode");
        if (m === "dark" || m === "light") {
            document.documentElement.dataset.mode = m;
        }
    } catch (e) {
        /* storage unavailable: fall back to the OS preference */
    }
})();
