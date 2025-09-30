// Injects the shared sidebar into #sidebar and marks active link.
// Also renders optional next/prev links for section pages.

(function(){
  async function injectSidebar(){
    const host = location.origin;
    const base = location.pathname.replace(/\/[^/]*$/, '/');
    const container = document.getElementById('sidebar');
    if (!container) return;
    try {
      const res = await fetch('/assets/partials/sidebar.html');
      const html = await res.text();
      container.innerHTML = html;
      // Mark active link
      const links = container.querySelectorAll('a[data-match]');
      links.forEach(a => {
        const pat = a.getAttribute('data-match');
        if (location.pathname.endsWith(pat) || location.pathname.includes(pat)) {
          a.classList.add('active');
        }
      });
    } catch (e) {
      // no-op
    }
  }

  // Ordered navigation per section
  const NAV = {
    'optimizing-theory': [
      '/pages/optimizing-theory/index.html',
      // add more pages here as they are created
    ],
  };

  function renderPrevNext(){
    const el = document.getElementById('section-nav');
    if (!el) return;
    const path = location.pathname;
    let foundSection = null;
    for (const [section, pages] of Object.entries(NAV)) {
      const idx = pages.indexOf(path);
      if (idx !== -1) {
        foundSection = { section, pages, idx };
        break;
      }
    }
    if (!foundSection) return;
    const { pages, idx } = foundSection;
    const prev = pages[idx-1];
    const next = pages[idx+1];
    const makeBtn = (href, label, disabled) => disabled ?
      `<span class="button" style="opacity:.5;pointer-events:none">${label}</span>` :
      `<a class="button" href="${href}">${label}</a>`;
    el.innerHTML = `
      <div class="buttons">
        ${makeBtn(prev, '← Previous', !prev)}
        ${makeBtn(next, 'Next →', !next)}
      </div>
    `;
  }

  document.addEventListener('DOMContentLoaded', function(){
    injectSidebar();
    renderPrevNext();
  });
})();

