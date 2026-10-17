#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-context-workbench-v2";
const output = path.join(root, "public/keeper-review", set);
const pack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v2");
const v1Dir = path.join(root, "public/keeper-review/keeper-prime-context-workbench-v1");
const dartsData = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v3/keeper-prime-darts-context-v3.json"), "utf8"));
const dartsV2Register = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v2/batch-register.json"), "utf8"));
const dartsV3Register = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v3/batch-register.json"), "utf8"));
const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

const v1Catalog = JSON.parse(fs.readFileSync(path.join(v1Dir, "catalog.json"), "utf8"));
const inventory = JSON.parse(fs.readFileSync(path.join(v1Dir, "inventory.json"), "utf8"));
fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(output, { recursive: true });
const assetDir = path.join(output, "assets");
fs.mkdirSync(assetDir, { recursive: true });
fs.mkdirSync(pack, { recursive: true });

const sourceByUrl = new Map([...dartsV2Register.publishedAssets, ...dartsV3Register.publishedAssets].map((entry) => [entry.url, path.join(root, entry.source)]));
const workbenchAssets = [];
const publishedByHash = new Map();
function localise(url) {
  const source = sourceByUrl.get(url);
  if (!source) throw new Error(`No source provenance for ${url}`);
  const digest = sha(source);
  if (publishedByHash.has(digest)) return publishedByHash.get(digest).url;
  const name = `frame-${digest.slice(0, 16)}${path.extname(source)}`;
  fs.copyFileSync(source, path.join(assetDir, name));
  const entry = { source: rel(source), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  publishedByHash.set(digest, entry);
  workbenchAssets.push(entry);
  return entry.url;
}

const sequences = v1Catalog.sequences.map((sequence) => sequence.id === "darts-v2" ? {
  id: "darts-v3",
  title: "Candidate · approach → throw 3 → collect → return → throw 3",
  status: "corrected candidate awaiting Frank",
  summary: "Closed edge-on cupboard door, visible flights and impacts, practical collection height, and only the two turns required at the board and oche.",
  kind: "external",
  url: "/keeper-review/keeper-prime-darts-context-v3/",
} : sequence.kind === "native" ? { ...sequence, frames: sequence.frames.map((frame) => ({ ...frame, src: localise(frame.src) })) } : sequence);
const exactPrimeGhost = localise(dartsData.route[dartsData.ranges.firstThrowSet[0]].src);
const catalog = {
  ...v1Catalog,
  schema: "lighthouse-keeper/context-workbench@2",
  set,
  exactPrimeGhost,
  inventoryUrl: `/keeper-review/${set}/inventory.json`,
  sequences,
  deliveryCorrection: "All catalogue and script URLs are root-absolute so Vercel's trailing-slash normalisation cannot redirect a JSON request to HTML.",
};
const catalogFile = path.join(output, "catalog.json");
writeJson(catalogFile, catalog);
writeJson(path.join(output, "inventory.json"), inventory);

const app = `const CATALOG_URL='/keeper-review/${set}/catalog.json';let catalog,selected,timeline=[],index=0,timer=null,playing=false;const stages=[...document.querySelectorAll('.stage')],controls=[...document.querySelectorAll('button,select,input')];function preload(src){return new Promise((ok,no)=>{const i=new Image();i.onload=()=>{const d=i.decode?.();d?d.then(ok).catch(ok):ok()};i.onerror=()=>no(new Error('Could not load '+src));i.src=src})}function place(im,f,z){const a=f.anchorLp||[16,40],w=a[0]===28?56:32;im.src=f.src;im.style.width=w*z+'px';im.style.height=40*z+'px';im.style.left=(f.rootXLp-a[0])*z+'px';im.style.top=((f.bottomLp??52)-a[1])*z+'px';im.style.transform=f.flipX?'scaleX(-1)':'none'}function setup(){for(const s of stages){const z=+s.dataset.scale;s.style.width=172*z+'px';s.style.height=56*z+'px';for(const cls of ['ghost prime','ghost adjacent','actor']){const i=document.createElement('img');i.className=cls;s.appendChild(i)}}}function activeSlice(){if(!selected||selected.kind!=='native')return[];const [a,b]=selected.coreRange,start=document.getElementById('before').checked?0:a,end=document.getElementById('after').checked?selected.frames.length-1:b;return selected.frames.slice(start,end+1)}function stop(){playing=false;if(timer)clearTimeout(timer);timer=null}function choose(){stop();selected=catalog.sequences.find(x=>x.id===document.getElementById('sequence').value);document.getElementById('summary').innerHTML='<span class="badge">'+selected.status+'</span> · '+selected.summary;const external=selected.kind==='external';document.getElementById('native').classList.toggle('hidden',external);document.getElementById('externalWrap').classList.toggle('hidden',!external);for(const id of ['before','after','loop','speed','prev','play','pause','next','primeGhost','adjacentGhost'])document.getElementById(id).disabled=external;if(external){document.getElementById('external').src=selected.url;document.getElementById('readout').textContent='The complete dedicated contextual reviewer is loaded below with its own frame, loop, speed and ghost controls.';return}timeline=activeSlice();index=0;render();playing=true;tick()}function render(){if(!timeline.length)return;const f=timeline[index],p=timeline[Math.max(0,index-1)];for(const s of stages){const z=+s.dataset.scale;place(s.querySelector('.actor'),f,z);place(s.querySelector('.adjacent'),p,z);place(s.querySelector('.prime'),{...f,src:catalog.exactPrimeGhost,anchorLp:[28,40],flipX:false},z);s.querySelector('.prime').style.display=document.getElementById('primeGhost').checked?'block':'none';s.querySelector('.adjacent').style.display=document.getElementById('adjacentGhost').checked?'block':'none'}document.getElementById('readout').innerHTML='<b>'+f.phase+'</b> · frame '+(index+1)+' / '+timeline.length+' · '+f.label+' · root '+f.rootXLp.toFixed(3)+' lp'}function tick(){if(!playing||!timeline.length)return;render();const f=timeline[index],speed=+document.getElementById('speed').value;timer=setTimeout(()=>{if(index>=timeline.length-1){if(!document.getElementById('loop').checked){stop();return}index=0}else index++;tick()},f.durationMs/speed)}function step(delta){stop();index+=delta;if(index>=timeline.length)index=0;if(index<0)index=timeline.length-1;render()}document.getElementById('sequence').onchange=choose;for(const id of ['before','after'])document.getElementById(id).onchange=()=>{stop();timeline=activeSlice();index=0;render()};document.getElementById('prev').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);document.getElementById('play').onclick=()=>{stop();playing=true;tick()};document.getElementById('pause').onclick=stop;document.getElementById('primeGhost').onchange=render;document.getElementById('adjacentGhost').onchange=render;setup();fetch(CATALOG_URL).then(r=>{if(!r.ok)throw new Error('Catalogue '+r.status);return r.json()}).then(async c=>{catalog=c;const select=document.getElementById('sequence');for(const s of c.sequences){const o=document.createElement('option');o.value=s.id;o.textContent=s.title;select.appendChild(o)}const unique=[...new Set(c.sequences.filter(s=>s.kind==='native').flatMap(s=>s.frames.map(f=>f.src)).concat(c.exactPrimeGhost))];await Promise.all(unique.map(preload));controls.forEach(x=>x.disabled=false);document.getElementById('loading').textContent='Catalogue loaded; all '+unique.length+' unique native-route images decoded before playback was enabled.';choose()}).catch(e=>document.getElementById('loading').textContent='Workbench locked: '+e.message);`;
fs.writeFileSync(path.join(output, "app.js"), app);

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper contextual animation workbench V2</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#edf8fb;font:15px/1.45 system-ui,sans-serif}header,main{width:100%;margin:auto;padding:20px}header{border-bottom:1px solid #284653}a{color:#8ed7ff}.status,.badge{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:4px 9px}.panel{background:#10232d;border:1px solid #2d4a58;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}button,select{font:inherit;color:white;background:#173d52;border:1px solid #527484;border-radius:8px;padding:8px 11px}button:disabled,select:disabled,input:disabled{opacity:.45}.viewport{width:100%;overflow:auto;padding:8px;background:#061016;border-radius:8px}.stage{position:relative;flex:none;background:linear-gradient(#16303a 0 91%,#3f5660 91% 94%,#18252c 94%);overflow:hidden}.stage:after{content:'';position:absolute;left:0;right:0;top:92.8%;border-top:1px solid #78909a}.actor,.ghost{position:absolute;object-fit:contain;transform-origin:center;z-index:4}.ghost{opacity:.23;filter:hue-rotate(115deg) saturate(1.8);z-index:3}.adjacent{filter:hue-rotate(280deg) saturate(1.8)}#readout b{color:#73e3a8}.readout{font-variant-numeric:tabular-nums;min-height:3em}.scales{display:grid;gap:16px}.hidden{display:none}.external{width:100%;height:1550px;border:0;background:#07131b;border-radius:9px}.notice{border-left:4px solid #72e2a5;background:#14281f;padding:12px}
</style></head><body><header><h1>Prime Keeper contextual animation workbench V2</h1><span class="status">Review-only · nothing promoted</span><p>Select an animation to see it in the full transition context appropriate to it. V2 fixes the deployed catalogue-loading fault and gives the large inspection pane the full browser width.</p></header><main><p class="notice"><strong>Coverage:</strong> all 308 production animations remain in the <a href="/keeper-review/${set}/inventory.json">read-only inventory</a>. Seven current authorities or candidates are exposed for visual review here.</p><section class="panel"><div class="controls"><select id="sequence" disabled></select><label><input id="before" type="checkbox" checked disabled> Preceding transition</label><label><input id="after" type="checkbox" checked disabled> Finishing transition</label><label><input id="loop" type="checkbox" checked disabled> Loop</label><select id="speed" disabled><option value=".75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select><button id="prev" disabled>← One frame</button><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="next" disabled>One frame →</button><label><input id="primeGhost" type="checkbox" disabled> Exact Prime ghost</label><label><input id="adjacentGhost" type="checkbox" disabled> Previous-frame ghost</label></div><p id="loading" class="readout">Loading catalogue and decoding native-route images…</p><p id="summary"></p><p id="readout" class="readout"></p></section><section id="native" class="panel scales"><div><h2>Large inspection · 8×</h2><div class="viewport"><div class="stage" data-scale="8"></div></div></div><div><h2>Proposed game presentation · 4×</h2><div class="viewport"><div class="stage" data-scale="4"></div></div></div><div><h2>Literal logical raster · 1×</h2><div class="viewport"><div class="stage" data-scale="1"></div></div></div></section><section id="externalWrap" class="panel hidden"><p class="notice">This is a complete contextual reviewer. Use its controls below; Darts V3 includes its own complete-route and repeatable-activity modes.</p><iframe id="external" class="external" title="Selected complete animation review"></iframe></section></main><script src="/keeper-review/${set}/app.js"></script></body></html>`;
const pageFile = path.join(output, "index.html");
fs.writeFileSync(pageFile, html);

const register = {
  schema: "lighthouse-keeper/review-batch@1",
  batchId: "keeper-prime-context-workbench-2026-10-17-v2",
  status: "review-tool-awaiting-frank",
  purpose: catalog.purpose,
  predecessor: { page: "public/keeper-review/keeper-prime-context-workbench-v1/index.html", role: "immutable failed deployment retained as provenance" },
  catalog: { file: rel(catalogFile), sha256: sha(catalogFile) },
  page: { file: rel(pageFile), sha256: sha(pageFile) },
  coverage: sequences.map(({ id, title, status, kind }) => ({ id, title, status, kind })),
  features: ["root-absolute deployment-safe data loading", "animation selector", "preceding transition toggle", "finishing transition toggle", "whole/core looping", "frame stepping", "speed multiplier", "full-width 8x/4x/1x views", "exact Prime ghost", "previous-frame onion skin", "dedicated Darts V3 contextual reviewer", "complete 308-row inventory"],
  publishedAssets: workbenchAssets,
  boundaries: catalog.boundaries,
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; V1 and every animation source remain unchanged.`,
};
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), `# Prime Keeper Context Workbench V2\n\nV2 corrects V1's trailing-slash deployment bug by using root-absolute catalogue, script and inventory URLs. It retains the complete 308-row inventory and the seven current review choices, with Darts updated to its dedicated V3 contextual reviewer. Nothing is promoted.\n`);
console.log(JSON.stringify({ set, sequences: sequences.length, native: sequences.filter((entry) => entry.kind === "native").length, external: sequences.filter((entry) => entry.kind === "external").length, page: rel(pageFile) }, null, 2));
