// Lightweight Markdown rendering helper for Obsidian-style notes.
// Usage option A: Inline block
//   <div id="opt-def"></div>
//   <script type="text/markdown" data-target="#opt-def">
//   # Title
//   Your markdown here...
//   </script>
//
// Usage option B: External file
//   <div data-md-src="../../notes/optimizing-theory/intro.md"></div>
//
(function(){
  const CDN_MARKED = 'https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js';
  const CDN_PURIFY = 'https://cdn.jsdelivr.net/npm/dompurify@3.0.6/dist/purify.min.js';

  function loadScript(src){
    return new Promise((resolve, reject)=>{
      const s = document.createElement('script');
      s.src = src; s.onload = resolve; s.onerror = reject; document.head.appendChild(s);
    });
  }

  async function ensureLibs(){
    if (!window.marked) await loadScript(CDN_MARKED);
    if (!window.DOMPurify) await loadScript(CDN_PURIFY);
  }

  function renderMarkdown(md){
    const html = window.marked.parse(md, { mangle: false, headerIds: true });
    return window.DOMPurify.sanitize(html);
  }

  async function renderInlineBlocks(){
    const blocks = Array.from(document.querySelectorAll('script[type="text/markdown"][data-target]'));
    if (!blocks.length) return;
    await ensureLibs();
    blocks.forEach(b=>{
      const target = document.querySelector(b.getAttribute('data-target'));
      if (target) target.innerHTML = renderMarkdown(b.textContent);
    });
  }

  async function renderExternal(){
    const containers = Array.from(document.querySelectorAll('[data-md-src]'));
    if (!containers.length) return;
    await ensureLibs();
    await Promise.all(containers.map(async el => {
      const src = el.getAttribute('data-md-src');
      try {
        const res = await fetch(src);
        const md = await res.text();
        el.innerHTML = renderMarkdown(md);
        el.classList.add('md-content');
      } catch(e){ /* ignore */ }
    }));
  }

  document.addEventListener('DOMContentLoaded', function(){
    renderInlineBlocks();
    renderExternal();
  });
})();

