// Injects the shared sidebar into #sidebar and marks active link.
// Also renders optional next/prev links for section pages.

(function(){
  function getRoot() {
    const script = document.currentScript || document.querySelector('script[src*="site-nav.js"]');
    const abs = new URL(script ? script.getAttribute('src') : 'assets/js/site-nav.js', document.baseURI);
    // Trim to repo root (folder containing assets/)
    return abs.href.replace(/assets\/js\/site-nav\.js(?:\?.*)?$/, '');
  }

  async function injectSidebar(){
    const container = document.getElementById('sidebar');
    if (!container) return;
    const root = getRoot();
    try {
      const res = await fetch(root + 'assets/partials/sidebar.html');
      const html = await res.text();
      container.innerHTML = html;
      // Fix links to be rooted at the project base
      container.querySelectorAll('a[href^="/"]').forEach(a => {
        const path = a.getAttribute('href').replace(/^\//,'');
        a.setAttribute('href', root + path);
      });
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
      // absolute path is converted later to root-relative
      '/pages/optimizing-theory/index.html',
      // add more pages here as they are created
    ],
  };

  function renderPrevNext(){
    const el = document.getElementById('section-nav');
    if (!el) return;
    const root = getRoot();
    const path = location.pathname;
    let foundSection = null;
    for (const [section, pages] of Object.entries(NAV)) {
      // Normalize page hrefs to match current path
      const norm = pages.map(p => new URL(p.replace(/^\//,''), root).pathname);
      const idx = norm.indexOf(path);
      if (idx !== -1) {
        foundSection = { section, pages: norm, idx };
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
    // Toggle button
    const btn = document.getElementById('navToggle');
    const backdrop = document.getElementById('backdrop');
    function toggle(open){
      const willOpen = open ?? !document.body.classList.contains('nav-open');
      document.body.classList.toggle('nav-open', willOpen);
      if (btn) btn.setAttribute('aria-expanded', String(willOpen));
    }
    if (btn) btn.addEventListener('click', () => toggle());
    if (backdrop) backdrop.addEventListener('click', () => toggle(false));
    document.addEventListener('keydown', (e)=>{ if (e.key === 'Escape') toggle(false); });

    // Theme toggle
    const tbtn = document.getElementById('themeToggle');
    const root = document.documentElement;
    const saved = localStorage.getItem('theme');
    if (saved === 'light' || saved === 'dark') {
      root.setAttribute('data-theme', saved);
    }
    function updateLabel(){
      if (!tbtn) return;
      const mode = root.getAttribute('data-theme') || 'auto';
      tbtn.textContent = mode === 'dark' ? '☾' : (mode === 'light' ? '☀' : '◎');
      tbtn.title = 'Toggle light/dark (current: ' + mode + ')';
    }
    updateLabel();
    if (tbtn) tbtn.addEventListener('click', () => {
      const current = root.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : (current === 'light' ? null : 'dark');
      if (next) {
        root.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
      } else {
        root.removeAttribute('data-theme');
        localStorage.removeItem('theme');
      }
      updateLabel();
    });

    // Font size slider (global)
    const fs = document.getElementById('fontSize');
    const rootEl = document.documentElement;
    const savedFs = parseInt(localStorage.getItem('fontSizePct') || '', 10);
    const initialFs = Number.isFinite(savedFs) ? savedFs : 140;
    rootEl.style.fontSize = initialFs + '%';
    if (fs) {
      fs.value = String(initialFs);
      fs.addEventListener('input', () => {
        const v = Math.max(90, Math.min(220, parseInt(fs.value, 10) || initialFs));
        rootEl.style.fontSize = v + '%';
        localStorage.setItem('fontSizePct', String(v));
      });
    }
  });
})();
