// Interactive optimizer explorer: random simple functions + slider to probe x
// Usage:
//   <div data-widget="opt-explorer" data-min="0" data-max="10" data-type="random"></div>
// Types: random | concave | multi
export default function init(el){
  const min = parseFloat(el.getAttribute('data-min') || '0');
  const max = parseFloat(el.getAttribute('data-max') || '10');
  let kind = (el.getAttribute('data-type') || 'random').toLowerCase();

  // Container and basic layout
  const container = document.createElement('div');
  container.style.margin = '0 auto 12px';
  container.style.maxWidth = '900px';

  const controls = document.createElement('div');
  controls.style.display = 'flex';
  controls.style.flexWrap = 'wrap';
  controls.style.gap = '8px';
  controls.style.alignItems = 'center';
  controls.style.margin = '0 0 8px 0';

  const typeLabel = document.createElement('label');
  typeLabel.textContent = 'Function:';
  typeLabel.style.fontSize = '0.9rem';
  const typeSel = document.createElement('select');
  for (const v of ['random','concave','multi']){
    const o = document.createElement('option'); o.value = v; o.textContent = v; if (v===kind) o.selected = true; typeSel.appendChild(o);
  }

  const newBtn = document.createElement('button');
  newBtn.textContent = 'New Function';
  newBtn.className = 'button';

  const xLabel = document.createElement('label'); xLabel.textContent = 'x:'; xLabel.style.marginLeft = '12px'; xLabel.style.fontSize = '0.9rem';
  const slider = document.createElement('input'); slider.type = 'range'; slider.min = String(min); slider.max = String(max); slider.step = '0.01'; slider.value = String((min+max)/2);

  const readout = document.createElement('div');
  readout.style.fontFamily = 'var(--mono, ui-monospace, SFMono-Regular, Menlo, monospace)';
  readout.style.fontSize = '0.9rem';
  readout.style.marginLeft = 'auto';

  controls.append(typeLabel, typeSel, newBtn, xLabel, slider, readout);

  const canvas = document.createElement('canvas');
  canvas.width = 900; canvas.height = 520;
  canvas.style.width = '100%'; canvas.style.height = 'auto';
  canvas.style.background = '#fff'; canvas.style.border = '1px solid var(--border)'; canvas.style.borderRadius = '6px';

  container.append(controls, canvas);
  el.replaceWith(container);

  const ctx = canvas.getContext('2d');
  const P = { left: 60, right: 30, top: 30, bottom: 50,
    width(){ return canvas.width - this.left - this.right; },
    height(){ return canvas.height - this.top - this.bottom; }
  };

  function toX(x){ return P.left + (x - min) * (P.width()/(max-min)); }
  function fromX(px){ return min + (px - P.left) * (max-min)/P.width(); }
  let ymin = -5, ymax = 5;
  function toY(y){ return canvas.height - P.bottom - (y - ymin) * (P.height()/(ymax - ymin || 1)); }

  // Function generators
  function rand(a,b){ return a + Math.random()*(b-a); }
  function genConcave(){
    const b = rand(min+0.2*(max-min), max-0.2*(max-min));
    const a = rand(0.2, 1.2); // width
    const c = rand(-1.5, 1.5);
    return {
      type: 'concave',
      f: (x) => -a*(x-b)*(x-b) + c,
      label: `f(x) = -${a.toFixed(2)}(x-${b.toFixed(2)})^2 + ${c.toFixed(2)}`
    };
  }
  function genMulti(){
    const k = rand(0.6, 1.2);
    const A = rand(1.0, 2.0), B = rand(0.5, 1.5);
    const quad = rand(0.01, 0.08); // slight downward bowl to keep bounded
    const phase = rand(0, Math.PI);
    return {
      type: 'multi',
      f: (x) => A*Math.sin(k*x + phase) + B*Math.cos(2*k*x + 0.3) - quad*(x-0.5*(min+max))**2,
      label: `A sin(kx)+B cos(2kx) - q(x-c)^2`
    };
  }
  function genRandom(){
    return Math.random() < 0.5 ? genConcave() : genMulti();
  }

  let fn = kind==='concave' ? genConcave() : kind==='multi' ? genMulti() : genRandom();

  // Sampling helpers
  function sample(){
    const N = 400; const xs = new Array(N); const ys = new Array(N);
    for (let i=0;i<N;i++){
      const x = min + (max-min)*i/(N-1);
      xs[i] = x; ys[i] = fn.f(x);
    }
    // update y-range with a small margin
    let lo = Math.min(...ys), hi = Math.max(...ys);
    if (Math.abs(hi-lo) < 1e-6){ hi = lo + 1; }
    const pad = 0.08 * (hi - lo);
    ymin = lo - pad; ymax = hi + pad;
    return {xs, ys};
  }

  function findExtrema(xs, ys){
    const locals = [];
    let gi = 0;
    for (let i=1;i<ys.length-1;i++){
      const dy1 = ys[i] - ys[i-1];
      const dy2 = ys[i+1] - ys[i];
      if (dy1 > 0 && dy2 < 0) locals.push({i, x: xs[i], y: ys[i]}); // local max
      if (ys[i] > ys[gi]) gi = i;
    }
    const global = {i: gi, x: xs[gi], y: ys[gi]};
    return {locals, global};
  }

  function grid(){
    ctx.fillStyle = '#ffffff'; ctx.fillRect(0,0,canvas.width,canvas.height);
    // grid
    ctx.strokeStyle = '#e6e6e9'; ctx.lineWidth = 1;
    const steps = 10;
    for (let i=0;i<=steps;i++){
      const x = P.left + i*P.width()/steps; ctx.beginPath(); ctx.moveTo(x, P.top); ctx.lineTo(x, canvas.height - P.bottom); ctx.stroke();
      const y = P.top + i*P.height()/steps; ctx.beginPath(); ctx.moveTo(P.left, y); ctx.lineTo(canvas.width - P.right, y); ctx.stroke();
    }
    // axes
    ctx.strokeStyle = '#000'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(P.left, canvas.height - P.bottom); ctx.lineTo(canvas.width - P.right, canvas.height - P.bottom); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(P.left, canvas.height - P.bottom); ctx.lineTo(P.left, P.top); ctx.stroke();
    // axis labels
    ctx.fillStyle = '#333'; ctx.font = '12px system-ui, sans-serif';
    ctx.fillText('x', canvas.width - P.right - 10, canvas.height - P.bottom + 24);
    ctx.fillText('f(x)', P.left - 36, P.top + 12);
  }

  function draw(){
    const {xs, ys} = sample();
    const ex = findExtrema(xs, ys);
    grid();
    // curve
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--accent') || '#0b66d6';
    ctx.lineWidth = 2; ctx.beginPath();
    xs.forEach((x, i) => {
      const X = toX(x), Y = toY(ys[i]);
      if (i===0) ctx.moveTo(X,Y); else ctx.lineTo(X,Y);
    });
    ctx.stroke();
    // local maxima
    ctx.fillStyle = '#f2a441';
    ex.locals.forEach(p => { ctx.beginPath(); ctx.arc(toX(p.x), toY(p.y), 4, 0, Math.PI*2); ctx.fill(); });
    // global maximum
    ctx.fillStyle = '#e14b4b';
    ctx.beginPath(); ctx.arc(toX(ex.global.x), toY(ex.global.y), 5, 0, Math.PI*2); ctx.fill();

    // probe marker at slider x
    const x0 = parseFloat(slider.value);
    const y0 = fn.f(x0);
    ctx.strokeStyle = '#666'; ctx.setLineDash([4,4]);
    ctx.beginPath(); ctx.moveTo(toX(x0), canvas.height - P.bottom); ctx.lineTo(toX(x0), P.top); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#333'; ctx.font = '14px system-ui, sans-serif';
    ctx.fillText(fn.label, P.left + 8, P.top + 16);
    readout.textContent = `x=${x0.toFixed(2)}  f(x)=${y0.toFixed(3)}  |  global max ≈ (${ex.global.x.toFixed(2)}, ${ex.global.y.toFixed(3)})`;
  }

  // Events
  typeSel.addEventListener('change', () => { kind = typeSel.value; newRandom(); });
  newBtn.addEventListener('click', newRandom);
  slider.addEventListener('input', draw);

  function newRandom(){
    if (kind === 'concave') fn = genConcave();
    else if (kind === 'multi') fn = genMulti();
    else fn = genRandom();
    draw();
  }

  // Initial draw
  newRandom();
}

