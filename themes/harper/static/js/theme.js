// Theme toggle: reads/writes localStorage, updates the ◐ label.
// The no-flash init in <head> has already set data-theme before paint.
(function () {
  var root = document.documentElement;
  var btns = document.querySelectorAll('[data-theme-toggle]');

  function label() {
    var cur = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    btns.forEach(function (b) { b.textContent = '◐ ' + cur; });
  }

  label();

  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      label();
    });
  });
})();
