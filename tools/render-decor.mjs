#!/usr/bin/env node
// Renders the website's own decorations into email-safe pictures, so every inbox shows
// the same bunting, pins, tape, airmail edges, stamp, calendar page, hills and taped photos
// as ourspecialvillagetn.com (Gmail ignores the CSS the site draws them with).
//
// Nothing here is new art: each piece is the site's CSS or SVG (public/css/shell.css,
// css/pages/village-hall.css, newsletter.css, hope.css, js/site.js treelines) drawn in a
// browser, around Taylor's paintings and the families' photos.
//
//   cd ../OurSpecialVillage/public && python3 -m http.server 8765 &
//   node tools/render-decor.mjs --site http://localhost:8765 --fonts ../OurSpecialVillage/public/fonts
//   (add --only stops to redo just the In this issue stops)
//
// Inputs are listed in tools/decor.json. Then run tools/build-october-2026.py and tools/build-issues.py.
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, all) => (v.startsWith('--') ? a.concat([[v.slice(2), all[i + 1]]]) : a), []));
const SITE = (args.site || 'http://localhost:8765').replace(/\/$/, '');
const FONTS = path.resolve(args.fonts || path.join(ROOT, '..', 'OurSpecialVillage', 'public', 'fonts'));
const cfg = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools', 'decor.json'), 'utf8'));

let chromium;
try { ({ chromium } = await import('playwright')); } catch {
  ({ chromium } = await import('/opt/node22/lib/node_modules/playwright/index.mjs'));
}

const C = { navy: '#1d2c4c', navyDeep: '#14203a', cream: '#f7f1e2', paper: '#fffcf5', note: '#fffdf7', gold: '#d7a43e',
  goldDeep: '#b4861f', goldSoft: '#f3e5c0', brick: '#a9542f', blueInk: '#3c5378', sage: '#7d8f63', cork: '#ecd9ae' };

const font = (f) => 'data:font/woff2;base64,' + fs.readFileSync(path.join(FONTS, f)).toString('base64');
const FONT_CSS = `@font-face{font-family:Outfit;src:url(${font('outfit-var.woff2')}) format('woff2');font-weight:100 900}
@font-face{font-family:Mulish;src:url(${font('mulish-var.woff2')}) format('woff2');font-weight:200 1000}
@font-face{font-family:'Patrick Hand';src:url(${font('patrick-hand-latin.woff2')}) format('woff2')}`;

// Local files become data URLs (the page is served from the site's origin).
function src(p) {
  if (p.startsWith('/')) return SITE + p;
  const ext = path.extname(p).slice(1).replace('jpg', 'jpeg');
  return `data:image/${ext};base64,` + fs.readFileSync(path.join(ROOT, p)).toString('base64');
}

const browser = await chromium.launch();
const ctx = await browser.newContext({ deviceScaleFactor: 2, viewport: { width: 700, height: 900 } });
const page = await ctx.newPage();

// Render `body` (HTML) on a transparent page and screenshot the #shot element.
async function shot(body, out, { css = '', jpg = false, bg = 'transparent', width = 700 } = {}) {
  await page.setViewportSize({ width, height: 900 });
  await page.goto(SITE + '/__blank');
  await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>${FONT_CSS}
html,body{margin:0;background:${bg}}#shot{display:inline-block;position:relative}${css}</style></head><body>${body}</body></html>`, { waitUntil: 'load' });
  await page.evaluate(() => Promise.all([...document.images].map((i) => i.decode().catch(() => {}))));
  await page.waitForTimeout(80);
  const el = await page.$('#shot');
  fs.mkdirSync(path.dirname(out), { recursive: true });
  await el.screenshot({ path: out, omitBackground: !jpg, type: jpg ? 'jpeg' : 'png', quality: jpg ? 82 : undefined });
  console.log('wrote', path.relative(ROOT, out));
}

await page.route(SITE + '/__blank', (r) => r.fulfill({ contentType: 'text/html', body: '<!doctype html><title>x</title>' }));

const shared = path.join(ROOT, cfg.shared_out);

// ---------- Village Hall bunting (village-hall.html svg.vh-bunting), strung across 600px ----------
const bunting = (await (await fetch(SITE + '/village-hall.html')).text()).match(/<svg class="vh-bunting"[\s\S]*?<\/svg>/)[0];
await shot(`<div id="shot" style="width:600px;height:60px;padding:0">${bunting.replace('class="vh-bunting"', 'class="b"')}</div>`,
  path.join(shared, 'bunting.png'), { css: '.b{display:block;width:600px;height:50px;overflow:visible;filter:drop-shadow(0 4px 3px rgba(60,40,10,.16))}' });

// ---------- pushpins (village-hall.css .vh-pin / hope.css .hw-pin) ----------
for (const [name, color] of Object.entries({ brick: C.brick, blue: C.blueInk, gold: C.goldDeep, sage: C.sage })) {
  await shot(`<div id="shot" style="width:32px;height:34px"><span style="position:absolute;left:4px;top:2px;width:24px;height:24px;border-radius:50%;
    background:radial-gradient(circle at 35% 30%,#fff 0 12%,${color} 32% 100%);box-shadow:0 5px 6px -2px rgba(0,0,0,.35)"></span></div>`,
  path.join(shared, `pin-${name}.png`));
}

// ---------- airmail edges (newsletter.css .nl-card::after), top and bottom of a 532px letter ----------
const air = `linear-gradient(90deg,${C.brick} 0 10px,${C.note} 10px 16px,${C.blueInk} 16px 26px,${C.note} 26px 32px) 0 0/32px 7px repeat-x`;
await shot(`<div id="shot" style="width:532px;height:7px;overflow:hidden"><div style="height:40px;border-radius:8px;background:${air}"></div></div>`, path.join(shared, 'airmail-top.png'));
await shot(`<div id="shot" style="width:532px;height:7px;overflow:hidden"><div style="height:40px;margin-top:-33px;border-radius:8px;background:${air.replace('0 0/', '0 100%/')}"></div></div>`, path.join(shared, 'airmail-bottom.png'));

// ---------- stamp + postmark (newsletter.html .nl-stamp + .nl-postmark) ----------
const nlHtml = await (await fetch(SITE + '/newsletter.html')).text();
const postmark = nlHtml.match(/<svg class="nl-postmark"[\s\S]*?<\/svg>/)[0];
await shot(`<div id="shot" style="width:150px;height:118px">
  <span class="st"><img src="${SITE}/images/village/pictogram-mailbox-192.webp" alt=""></span>${postmark}</div>`,
  path.join(shared, 'stamp.png'), { css: `
.st{position:absolute;top:18px;right:18px;width:70px;height:82px;padding:7px;box-sizing:content-box;background:#fffdf6;rotate:6deg;display:grid;place-items:center;z-index:1;
  filter:drop-shadow(0 3px 3px rgba(60,40,10,.25));
  -webkit-mask:linear-gradient(#000 0 0) content-box,radial-gradient(circle 3.5px,transparent 95%,#000) -5px -5px/10px 10px padding-box;-webkit-mask-composite:source-over;
  mask:linear-gradient(#000 0 0) content-box,radial-gradient(circle 3.5px,transparent 95%,#000) -5px -5px/10px 10px padding-box;mask-composite:add}
.st img{width:100%;height:100%;object-fit:contain;background:${C.goldSoft};border-radius:2px;padding:4px;box-sizing:border-box}
.nl-postmark{position:absolute;top:6px;right:46px;width:86px;height:86px;color:rgba(29,44,76,.5);rotate:-14deg;z-index:2}
.nl-postmark text{font-family:Mulish}` });

// ---------- calendar page top (newsletter.css .nl-item--calendar .nl-deco): navy band + gold rings ----------
await shot(`<div id="shot" style="width:532px;height:56px"><div class="band"><span class="rings"></span></div></div>`,
  path.join(shared, 'calendar-top.png'), { css: `
.band{position:absolute;left:0;right:0;top:10px;height:46px;border-radius:8px 8px 0 0;background:${C.navy};box-shadow:inset 0 -4px 0 ${C.gold}}
.rings{position:absolute;left:18%;right:18%;top:-9px;height:20px;background:radial-gradient(circle 5px at 50% 50%,${C.gold} 90%,transparent 100%) 0 0/25% 100% space}` });

// ---------- deadline tag: brass eyelet with a twine loop (tools/tag-loop.svg, also the site's newsletter.css) ----------
// Oct 1, 2026: the straight string ran past the tag's rounded corner and stopped in mid-air.
await shot(`<div id="shot" style="line-height:0">${fs.readFileSync(path.join(ROOT, 'tools', 'tag-loop.svg'), 'utf8')}</div>`,
  path.join(shared, 'tag-eyelet.png'));


// ---------- folded-up corner (hope.css .hope-story::after) ----------
await shot(`<div id="shot" style="width:34px;height:34px;background:linear-gradient(135deg,#efe3c4 50%,${C.cork} 50%);border-radius:0 0 6px 0;box-shadow:-2px -2px 3px rgba(60,40,10,.08)"></div>`,
  path.join(shared, 'fold.png'), { css: '#shot{margin:4px}' });

// ---------- paper tape (village-hall.css .vh-tape, hope.css .hw-tape) ----------
await shot(`<div id="shot" style="width:124px;height:44px"><span class="tp"></span></div>`, path.join(shared, 'tape-blue.png'), { css: `
.tp{position:absolute;left:14px;top:8px;width:96px;height:28px;rotate:-3deg;background:rgba(228,233,242,.92);box-shadow:0 2px 4px rgba(60,40,10,.12);
  clip-path:polygon(0 8%,6% 0,12% 10%,18% 0,24% 8%,30% 0,100% 0,100% 92%,94% 100%,88% 90%,82% 100%,76% 92%,70% 100%,0 100%)}` });
await shot(`<div id="shot" style="width:124px;height:44px"><span class="tp"></span></div>`, path.join(shared, 'tape-cream.png'), { css: `
.tp{position:absolute;left:14px;top:8px;width:96px;height:28px;rotate:3deg;background:rgba(243,229,192,.95);box-shadow:0 2px 4px rgba(60,40,10,.12);
  border-left:2px dashed rgba(255,255,255,.6);border-right:2px dashed rgba(255,255,255,.6)}` });

// ---------- ticket notches (group.css .grp-ticket mask): cream half-circles bitten out of the navy ----------
await shot(`<div id="shot" style="width:16px;height:32px;background:radial-gradient(circle 16px at 0 50%,${C.cream} 96%,transparent 100%)"></div>`, path.join(shared, 'notch-l.png'));
await shot(`<div id="shot" style="width:16px;height:32px;background:radial-gradient(circle 16px at 100% 50%,${C.cream} 96%,transparent 100%)"></div>`, path.join(shared, 'notch-r.png'));

// ---------- background tiles at 1x (cork dots from .vh-board, ruled lines from .nl-item--index) ----------
{
  const p1 = await (await browser.newContext({ deviceScaleFactor: 1 })).newPage();
  await p1.setContent(`<div id="c" style="width:14px;height:14px;background:${C.cork} radial-gradient(rgba(122,91,19,.17) 1.2px,transparent 1.7px) 0 0/14px 14px"></div>
    <div id="r" style="width:8px;height:28px;background:#fffdf7 repeating-linear-gradient(180deg,transparent 0 27px,rgba(143,165,198,.32) 27px 28px)"></div>`);
  await (await p1.$('#c')).screenshot({ path: path.join(shared, 'cork.png') });
  await (await p1.$('#r')).screenshot({ path: path.join(shared, 'ruled.png') });
  console.log('wrote cork.png, ruled.png');
}

// ---------- footer hills with their treeline (every page's footer, planted by site.js) ----------
await page.setViewportSize({ width: 1200, height: 900 });
await page.goto(SITE + '/newsletter.html', { waitUntil: 'load' });
await page.addStyleTag({ content: 'html,body,.site-footer{background:transparent!important}' });
const hills = await page.$('svg.foot-hills');
await hills.screenshot({ path: path.join(shared, 'foot-hills.png'), omitBackground: true, scale: 'css' });
console.log('wrote', cfg.shared_out + '/foot-hills.png');

// ---------- About photo as a taped print (shared) ----------
async function polaroid(photo, out, { width, pad, rot, tape, bg, aspect }) {
  await shot(`<div id="shot" style="padding:22px 20px 26px;background:${bg}"><figure class="ph">
    <img src="${src(photo)}" alt=""><span class="tape"></span></figure></div>`, out, { jpg: true, bg, css: `
.ph{position:relative;margin:0;width:${width}px;padding:${pad};background:#fff;border-radius:3px;rotate:${rot};
  box-shadow:0 18px 26px -18px rgba(60,40,10,.6),0 0 0 1px rgba(60,40,10,.06)}
.ph img{display:block;width:100%;aspect-ratio:${aspect};object-fit:cover;object-position:50% 40%;border-radius:2px}
.tape{position:absolute;top:-13px;left:50%;width:${tape[0]}px;height:${tape[1]}px;margin-left:-${tape[0] / 2}px;rotate:${tape[2]};background:rgba(228,233,242,.9);
  box-shadow:0 2px 4px rgba(60,40,10,.12);clip-path:polygon(0 8%,6% 0,12% 10%,18% 0,24% 8%,30% 0,100% 0,100% 92%,94% 100%,88% 90%,82% 100%,76% 92%,70% 100%,0 100%)}` });
}
await polaroid(cfg.about_photo, path.join(shared, 'about-print.jpg'), { width: 150, pad: '8px 8px 26px', rot: '-2deg', tape: [70, 22, '4deg'], bg: C.paper, aspect: '1/1' });

// ---------- homepage pieces (index.html + css/home.css), drawn at the email's 600px ----------
// Only the site's own shapes: the dusk sky with its moon and lamp-lit houses, the wave back to
// cream, a starry night to tile behind the parent groups, the Wall of Hope string of notes,
// coloured book ribbons, and the gold stroke under the tagline.
const HOME = `${SITE}/index.html`;
const HIDE_CHROME = 'body > *:not(main){display:none!important} .motion-btn,.particles,.home-hero .cloud{display:none!important} *{animation-play-state:paused!important}';
async function homePage(season) {
  await page.setViewportSize({ width: 600, height: 900 });
  await page.goto(`${HOME}?season=${season}`, { waitUntil: 'load' });
  await page.addStyleTag({ content: HIDE_CHROME });
}
await homePage('fall');
await page.evaluate(() => document.querySelector('.dusk').classList.add('lit'));
await page.waitForTimeout(1200);
await (await page.$('.dusk-sky')).screenshot({ path: path.join(shared, 'dusk-top.png') });
await (await page.$('.dusk-wave')).screenshot({ path: path.join(shared, 'dusk-wave.png') });
console.log('wrote dusk-top.png, dusk-wave.png');

{ // stars over the dusk (home.js scatters 46 of them; seeded here so the picture never changes)
  let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const dots = Array.from({ length: 34 }, () => `<i style="left:${(rnd() * 100).toFixed(1)}%;top:${(rnd() * 100).toFixed(1)}%;width:${rnd() < 0.2 ? 3 : 2}px;height:${rnd() < 0.2 ? 3 : 2}px;opacity:${(0.35 + rnd() * 0.45).toFixed(2)}"></i>`).join('');
  const p1 = await (await browser.newContext({ deviceScaleFactor: 1 })).newPage();
  await p1.setContent(`<div id="s" style="position:relative;width:600px;height:420px;background:${C.navyDeep}">${dots}</div>
    <style>body{margin:0}#s i{position:absolute;border-radius:50%;background:#fff}</style>`);
  await (await p1.$('#s')).screenshot({ path: path.join(shared, 'stars.png') });
  console.log('wrote stars.png');
}

await shot(`<div id="shot" class="notes-wrap"><span class="notes"><i>first words</i><i>&#9829;</i><i>first friends</i><i>&#9829;</i><i>first jobs</i></span></div>`,
  path.join(shared, 'garland.png'), { css: `
.notes-wrap{width:532px;height:96px}
.notes{position:absolute;top:0;left:0;right:0;height:92px;display:flex;justify-content:space-around;align-items:flex-start;padding:0 14px}
.notes::before{content:"";position:absolute;left:0;right:0;top:14px;height:2px;background:#9d7128;border-radius:2px;box-shadow:0 2px 2px rgba(80,50,10,.15)}
.notes i{position:relative;min-width:58px;padding:20px 10px 10px;margin-top:6px;border-radius:3px;font:400 18px/1.05 'Patrick Hand';font-style:normal;color:${C.navy};text-align:center;max-width:92px;box-shadow:0 8px 12px -8px rgba(60,40,10,.45)}
.notes i::before{content:"";position:absolute;top:3px;left:50%;width:12px;height:12px;margin-left:-6px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0 14%,${C.brick} 36% 100%);box-shadow:0 2px 3px rgba(0,0,0,.3)}
.notes i:nth-child(1){background:${C.goldSoft};rotate:-5deg}
.notes i:nth-child(2){background:#f4dccd;rotate:4deg;color:#8f4424;font-size:22px;min-width:44px}
.notes i:nth-child(3){background:#e4e9f2;rotate:-2deg}
.notes i:nth-child(4){background:#e1e7d2;rotate:6deg;color:#55653e;font-size:22px;min-width:44px}
.notes i:nth-child(5){background:#f7e9c9;rotate:-4deg}` });

// book ribbons in the shelf's colours (home.css .book:nth-child)
for (const [name, color] of Object.entries({ gold: C.gold, blue: '#8fa5c6', brick: C.brick, sage: C.sage })) {
  await shot(`<div id="shot" style="width:14px;height:34px;background:${color};clip-path:polygon(0 0,100% 0,100% 100%,50% 76%,0 100%)"></div>`, path.join(shared, `ribbon-${name}.png`));
}

// the gold stroke under "Welcome to ours." (index.html .tagline svg)
await shot(`<div id="shot" style="width:200px;height:16px"><svg viewBox="0 0 200 16" width="200" height="16" style="display:block;overflow:visible"><path d="M3 10c46-7 96-9 194-3" fill="none" stroke="${C.gold}" stroke-width="5" stroke-linecap="round"/></svg></div>`,
  path.join(shared, 'swoosh.png'), { css: '#shot{padding:2px 4px}' });

// The opening: the homepage hero's sky, sun and rolling hills (home.css .home-hero, golden hour),
// with the month's painting in the panorama. Cut in two: the sky goes behind the title as a
// background picture, the hills and village sit under it as a picture.
async function hero(painting, season, outDir) {
  await homePage(season);
  await page.evaluate((p) => {
    document.body.setAttribute('data-daypart', 'golden');
    document.querySelector('.home-hero .hero-text').innerHTML = '<div style="height:300px"></div>';
    const img = document.querySelector('.home-hero .panorama img');
    img.removeAttribute('srcset'); img.src = p;
  }, src(painting));
  await page.evaluate(() => { const i = document.querySelector('.home-hero .panorama img'); return i.complete ? 1 : new Promise((r) => { i.onload = r; i.onerror = r; setTimeout(r, 5000); }); });
  await page.waitForTimeout(900);
  const hb = await (await page.$('.home-hero')).boundingBox();
  const lb = await (await page.$('.home-hero svg.land')).boundingBox();
  const cut = Math.round(lb.y - hb.y);
  await page.screenshot({ path: path.join(outDir, 'hero-sky.jpg'), type: 'jpeg', quality: 84, clip: { x: hb.x, y: hb.y, width: hb.width, height: cut } });
  await page.screenshot({ path: path.join(outDir, 'hero-land.jpg'), type: 'jpeg', quality: 80, clip: { x: hb.x, y: hb.y + cut, width: hb.width, height: hb.height - cut } });
  console.log('wrote', path.relative(ROOT, path.join(outDir, 'hero-sky.jpg')), 'and hero-land.jpg');
}

// ---------- per issue: opening landscape, Village Hall painting, taped photos, In this issue stops ----------
async function landscape(painting, season, out, { oval = false, maxH = 400 } = {}) {
  const url = `${SITE}/__nl_land_${path.basename(out, '.jpg')}_${Math.random().toString(36).slice(2)}.html?season=${season}`;
  await page.route(url, (r) => r.fulfill({ contentType: 'text/html', body: `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=600"><link rel="stylesheet" href="/css/shell.css"><style>${FONT_CSS}
html,body{margin:0;background:${C.cream}}
main > .page-hero{padding:14px 24px 0;margin:0}
.page-visual{margin:0}
.page-visual img{display:block;width:auto;max-width:100%;max-height:${maxH}px;height:auto;margin:0 auto;mix-blend-mode:multiply;${oval ? '-webkit-mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 72%,transparent 100%);mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 72%,transparent 100%);' : ''}}
</style></head><body><main><section class="page-hero"><div class="page-visual"><img src="${src(painting)}" alt=""></div></section></main>
<script src="/js/site.js"></script></body></html>` }));
  await page.setViewportSize({ width: 600, height: 900 });
  await page.goto(url, { waitUntil: 'load' });
  await page.evaluate(() => Promise.all([...document.images].map((i) => i.decode().catch(() => {}))));
  await page.waitForTimeout(150);
  const el = await page.$('main > .page-hero');
  await el.screenshot({ path: out, type: 'jpeg', quality: 80 });
  console.log('wrote', path.relative(ROOT, out));
}

async function stops(chips, out) {
  // The jump buttons' pictures: Taylor's pictograms on the site's paper circles, one transparent PNG per
  // section (jump-events.png, jump-deadlines.png, ...), so they sit on the cork board beside her letter.
  // Oct 3, 2026: no painted path between them (the road pieces dangled on phones). Oct 4: new file names,
  // because browsers kept showing the old stop-N.png pictures (the site caches images for a day); give the
  // files new names again whenever they change.
  const W = 532, H = 112, cy = 54, step = W / 4, xs = [0, 1, 2, 3].map((i) => step * i + step / 2);
  const plots = chips.map((c, i) => `<span class="plot" style="left:${xs[i] - 40}px"><img src="${SITE}/images/village/${cfg.pictograms[c]}-192.webp" alt=""></span>`).join('');
  await shot(`<div id="shot" style="width:${W}px;height:${H}px">${plots}</div>`,
  out, { css: `.plot{position:absolute;top:${cy - 40}px;width:80px;height:80px;border-radius:50%;background:${C.paper};display:grid;place-items:center;
    box-shadow:0 1px 2px rgba(29,44,76,.08),0 10px 18px -12px rgba(60,40,10,.45),0 0 0 4px ${C.paper}}.plot img{width:60px;height:auto}` });
  const box = await (await page.$('#shot')).boundingBox();
  for (const [i, c] of chips.entries()) {
    const f = path.join(path.dirname(out), `jump-${c}.png`);
    await page.screenshot({ path: f, omitBackground: true, clip: { x: box.x + xs[i] - 48, y: box.y + cy - 48, width: 96, height: 96 } });
    console.log('wrote', path.relative(ROOT, f));
  }
  fs.unlinkSync(out);
}

for (const iss of cfg.issues) {
  const out = path.join(ROOT, iss.out);
  if (args.only === 'stops') { await stops(iss.chips, path.join(out, 'stops.png')); continue; }
  await hero(iss.hero, iss.season, out);
  await landscape(iss.vh, iss.season, path.join(out, 'vh-land.jpg'), { oval: !!iss.vh_oval, maxH: 250 });
  await stops(iss.chips, path.join(out, 'stops.png'));
  if (iss.hope_photo) {
    await polaroid(iss.hope_photo, path.join(out, 'hope-print.jpg'), { width: 220, pad: '10px 10px 34px', rot: '2.5deg', tape: [96, 28, '-4deg'], bg: C.note, aspect: '4/5' });
  }
  for (const [i, g] of iss.guests.entries()) {
    await polaroid(g, path.join(out, `guest-${i + 1}-print.jpg`), { width: 150, pad: '9px 9px 30px', rot: '-2.5deg', tape: [84, 24, '3deg'], bg: C.paper, aspect: '320/418' });
  }
}

await browser.close();
