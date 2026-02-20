(function () {
  const nav = document.getElementById('site-nav');
  const toggle = document.getElementById('nav-toggle');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { nav.classList.remove('open'); });
    });
  }

  // Active link: точное совпадение или вложенный путь (для Услуги /uslugi/*)
  const path = (window.location.pathname.replace(/\/+$/, '') || '/');
  document.querySelectorAll('nav a[href]').forEach(function (a) {
    try {
      const url = new URL(a.getAttribute('href'), window.location.origin);
      const p = (url.pathname.replace(/\/+$/, '') || '/');
      const exact = p === path;
      const parentMatch = p !== '/' && path !== p && path.indexOf(p + '/') === 0;
      if (exact || parentMatch) a.setAttribute('aria-current', 'page');
    } catch (e) {}
  });

  // Modals
  function closeAllModals() {
    document.querySelectorAll('.modal-overlay.is-open').forEach(function (m) {
      m.classList.remove('is-open');
      m.setAttribute('aria-hidden', 'true');
    });
  }
  document.querySelectorAll('[data-modal]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var id = btn.getAttribute('data-modal');
      var modal = document.getElementById('modal-' + id);
      if (modal) {
        closeAllModals();
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
      }
    });
  });
  document.querySelectorAll('[data-close-modal]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var modal = btn.closest('.modal-overlay');
      if (modal) {
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
      }
    });
  });
  document.querySelectorAll('.modal-overlay').forEach(function (overlay) {
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) {
        closeAllModals();
      }
    });
    var box = overlay.querySelector('.modal-box');
    if (box) box.addEventListener('click', function (e) { e.stopPropagation(); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAllModals();
  });

  // Tabs (portfolio filter)
  document.querySelectorAll('.tabs').forEach(function (tabsEl) {
    tabsEl.querySelectorAll('button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        tabsEl.querySelectorAll('button').forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        var filter = btn.getAttribute('data-filter');
        var container = document.querySelector('.portfolio-cards-filterable');
        if (container && filter) {
          container.querySelectorAll('[data-category]').forEach(function (card) {
            var cat = card.getAttribute('data-category');
            card.style.display = (filter === 'all' || cat === filter) ? '' : 'none';
          });
        }
      });
    });
  });
})();
