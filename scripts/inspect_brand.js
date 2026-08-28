/* Marka token çıkarımı. javascript_tool ile markanın YAZI SAYFASINDA çalıştırılır.
   Ön koşul: viewport 1440px+ sabitlenmiş, çerez bandı reddedilmiş olmalı. */
(() => {
  const px = e => Math.round(e.getBoundingClientRect().width);
  const isNeutral = c => {
    const m = c.match(/[\d.]+/g);
    if (!m) return true;
    if (m.length > 3 && Number(m[3]) === 0) return true;
    const [r, g, b] = m.map(Number);
    return Math.max(r, g, b) - Math.min(r, g, b) < 18;
  };

  const ps = [...document.querySelectorAll('p')].filter(p => p.innerText.trim().length > 120);
  const p = ps[0];
  if (!p) return JSON.stringify({ hata: 'Gövde paragrafı bulunamadı. Yazı detay sayfasında mı?' });

  const body = p.closest('[class*=article-body],[class*=post-content],article,main') || p.parentElement;
  const pcs = getComputedStyle(p);
  const h1 = document.querySelector('h1');
  const h2 = body.querySelector('h2');

  const tally = {};
  [...document.querySelectorAll('*')].slice(0, 3000).forEach(e => {
    const cs = getComputedStyle(e);
    ['backgroundColor', 'color', 'borderTopColor'].forEach(k => {
      const v = cs[k];
      if (v && v !== 'rgba(0, 0, 0, 0)' && !isNeutral(v)) tally[v] = (tally[v] || 0) + 1;
    });
  });

  const radii = new Set();
  [...document.querySelectorAll('[class*=card],[class*=Card],[class*=box],[class*=pill]')]
    .slice(0, 60).forEach(e => {
      const r = getComputedStyle(e).borderRadius;
      if (r && r !== '0px' && r.indexOf(' ') === -1) radii.add(r);
    });

  const logos = [...document.querySelectorAll('img')]
    .filter(e => /logo|brand/i.test((e.getAttribute('src') || '') + ' ' + (e.getAttribute('alt') || '') + ' ' + (e.getAttribute('class') || '')))
    .slice(0, 6)
    .map(e => ({ src: e.currentSrc || e.src, alt: e.alt, nat: e.naturalWidth + 'x' + e.naturalHeight, kare: e.naturalWidth === e.naturalHeight }));

  return JSON.stringify({
    url: location.href,
    viewport: innerWidth,
    govdeZemin: getComputedStyle(document.body).backgroundColor,
    icerikKolonu: px(body),
    paragraf: { font: pcs.fontFamily.split(',')[0].replace(/["']/g, ''), size: pcs.fontSize, lh: pcs.lineHeight, renk: pcs.color },
    h1: h1 ? { size: getComputedStyle(h1).fontSize, weight: getComputedStyle(h1).fontWeight, renk: getComputedStyle(h1).color } : null,
    h2: h2 ? { size: getComputedStyle(h2).fontSize, weight: getComputedStyle(h2).fontWeight, renk: getComputedStyle(h2).color } : null,
    markaRenkleri: Object.entries(tally).sort((a, b) => b[1] - a[1]).slice(0, 8),
    koseYaricaplari: [...radii].slice(0, 6),
    koyuTema: matchMedia('(prefers-color-scheme:dark)').matches || !!document.querySelector('[data-theme],[class*=dark-mode]'),
    logolar: logos
  }, null, 1);
})()
