// Widget loader: scans for [data-widget] placeholders and initializes modules.
(function(){
  function getRoot() {
    const script = document.currentScript || document.querySelector('script[src*="widgets/init.js"]');
    const abs = new URL(script ? script.getAttribute('src') : 'assets/widgets/init.js', document.baseURI);
    return abs.href.replace(/assets\/widgets\/init\.js(?:\?.*)?$/, '');
  }

  async function initWidgets(){
    const root = getRoot();
    const els = document.querySelectorAll('[data-widget]');
    for (const el of els) {
      const name = el.getAttribute('data-widget');
      if (!name) continue;
      try {
        const modUrl = new URL(`assets/widgets/${name}.js`, root).href;
        const mod = await import(modUrl);
        const fn = mod.default || mod.init;
        if (typeof fn === 'function') fn(el);
      } catch (e) {
        console.warn('Widget load failed:', name, e);
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWidgets);
  } else {
    initWidgets();
  }
})();

