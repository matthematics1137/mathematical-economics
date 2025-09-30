export default function init(el){
  // Read params with defaults
  const a = parseFloat(el.getAttribute('data-a') || '0.5');
  const M = parseFloat(el.getAttribute('data-m') || '100');
  const px = parseFloat(el.getAttribute('data-px') || '1');
  const py = parseFloat(el.getAttribute('data-py') || '1');

  const container = document.createElement('div');
  container.style.margin = '0 auto 12px';
  container.style.maxWidth = '900px';
  container.style.textAlign = 'center';
  const canvas = document.createElement('canvas');
  canvas.width = 900; canvas.height = 520;
  canvas.style.width = '100%'; canvas.style.height = 'auto';
  canvas.style.background = '#fff'; canvas.style.border = '1px solid var(--border)'; canvas.style.borderRadius = '6px';
  container.appendChild(canvas);
  el.replaceWith(container);

  const ctx = canvas.getContext('2d');

  const P = {
    left: 60, right: 30, top: 30, bottom: 50,
    width(){ return canvas.width - this.left - this.right; },
    height(){ return canvas.height - this.top - this.bottom; }
  };

  function toX(x){ return P.left + x * (P.width()/10); }
  function toY(y){ return canvas.height - P.bottom - y * (P.height()/10); }

  function grid(){
    ctx.fillStyle = '#ffffff'; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.strokeStyle = '#e6e6e9'; ctx.lineWidth = 1;
    for (let i=0;i<=10;i++){
      const x = toX(i);
      ctx.beginPath(); ctx.moveTo(x, P.top); ctx.lineTo(x, canvas.height - P.bottom); ctx.stroke();
      const y = toY(i);
      ctx.beginPath(); ctx.moveTo(P.left, y); ctx.lineTo(canvas.width - P.right, y); ctx.stroke();
    }
    // axes
    ctx.strokeStyle = '#000'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(P.left, canvas.height - P.bottom); ctx.lineTo(canvas.width - P.right, canvas.height - P.bottom); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(P.left, canvas.height - P.bottom); ctx.lineTo(P.left, P.top); ctx.stroke();
  }

  function draw(){
    grid();
    // Budget: py*y = M - px*x -> y = (M - px x)/py
    ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--accent') || '#0b66d6';
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (let x=0; x<=10; x+=0.02){
      const y = (M - px*x)/py; if (y<0) break;
      const X = toX(x); const Y = toY(y);
      if (x===0) ctx.moveTo(X,Y); else ctx.lineTo(X,Y);
    }
    ctx.stroke();

    // Cobb–Douglas optimum: x* = a M/px, y* = (1-a) M/py
    const xStar = a*M/px; const yStar = (1-a)*M/py;
    ctx.fillStyle = '#e14b4b';
    ctx.beginPath(); ctx.arc(toX(xStar), toY(yStar), 5, 0, Math.PI*2); ctx.fill();
    ctx.fillStyle = '#333';
    ctx.font = '14px system-ui, sans-serif';
    ctx.fillText(`x*=${xStar.toFixed(2)}, y*=${yStar.toFixed(2)}`, toX(xStar)+8, toY(yStar)-8);
  }

  draw();
}

