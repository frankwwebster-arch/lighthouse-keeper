#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-context-workbench-v1";
const outputDir = path.join(root, "public/keeper-review", set);
const dartsPack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v2");
const dartsRegister = JSON.parse(fs.readFileSync(path.join(dartsPack, "batch-register.json"), "utf8"));
const dartsData = JSON.parse(fs.readFileSync(path.join(dartsPack, "keeper-prime-darts-context-v2.json"), "utf8"));
const inventory = JSON.parse(fs.readFileSync(path.join(root, "data/keeper-prime-animation-bank-audit-v1.json"), "utf8"));
const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

fs.rmSync(outputDir, { recursive: true, force: true });
fs.mkdirSync(outputDir, { recursive: true });

const urlBySource = new Map(dartsRegister.publishedAssets.map((entry) => [entry.source, entry.url]));
const urlByHash = new Map(dartsRegister.publishedAssets.map((entry) => [entry.sourceSha256, entry.url]));
function asset(relativePath) {
  const absolute = path.join(root, relativePath);
  const url = urlBySource.get(relativePath) ?? (fs.existsSync(absolute) ? urlByHash.get(sha(absolute)) : null);
  if (!url) throw new Error(`Darts V2 did not publish ${relativePath}`);
  return url;
}
const walk = Array.from({ length: 8 }, (_, index) => asset(`art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames/keeper_prime_walk-right_f${index + 1}.png`));
const bridge = Array.from({ length: 5 }, (_, index) => asset(`art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames/keeper_prime_stop-to-walk-right_f${index + 1}.png`));
const turnRegister = JSON.parse(fs.readFileSync(path.join(root, "art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json"), "utf8"));
const turn = turnRegister.approvedCandidate.frames.map((entry) => asset(entry.file));
const exactPrime = asset("art/drafts/keeper-prime-darts-context-2026-10-17-v2/drafts/frames/keeper_prime_darts-right_endpoint.png");
const timing = JSON.parse(fs.readFileSync(path.join(root, "data/keeper_timing_policy.json"), "utf8")).transitionProfile;

const makeFrame = (src, phase, label, rootXLp, durationMs, extra = {}) => ({ src, phase, label, rootXLp, bottomLp: 52, durationMs, anchorLp: [16, 40], flipX: false, boardDarts: 0, ...extra });

function buildStopWalkStop() {
  const frames = [];
  let x = 54;
  for (let i = 0; i < 4; i += 1) frames.push(makeFrame(bridge[0], "preceding neutral", "exact Prime side neutral", x, 90));
  const coreStart = frames.length;
  for (const [imageIndex, delta] of [[1, 2], [2, 6], [3, 12], [4, 18]]) { x += delta / 8; frames.push(makeFrame(bridge[imageIndex], "accelerate", `approved bridge · ${delta} ku`, x, 1000 / timing.decelerationFps)); }
  for (let i = 0; i < 16; i += 1) { x += 21 / 8; const image = (i + 1) % 8; frames.push(makeFrame(walk[image], "approved walk", `Walk V6 · F${image + 1}`, x, 1000 / timing.walkFps)); }
  for (const [imageIndex, delta] of [[3, 18], [2, 12], [1, 6], [0, 2]]) { x += delta / 8; frames.push(makeFrame(bridge[imageIndex], "decelerate", `approved bridge · ${delta} ku`, x, 1000 / timing.decelerationFps)); }
  const coreEnd = frames.length - 1;
  for (let i = 0; i < 4; i += 1) frames.push(makeFrame(bridge[0], "finishing neutral", "exact Prime side neutral", x, 90));
  return { id: "approved-stop-walk-stop", title: "Approved · stop → walk → stop", status: "approved core authority", summary: "Exact approved bridge and Walk V6 pixels with approved Fast Timing V1.", kind: "native", stage: "plain-room", frames, coreRange: [coreStart, coreEnd] };
}

function buildTurnRound() {
  const frames = [];
  let x = 88;
  for (let i = 0; i < 8; i += 1) { x += 21 / 8; frames.push(makeFrame(walk[i], "preceding walk", `Walk V6 · F${i + 1}`, x, 1000 / timing.walkFps)); }
  for (const [imageIndex, delta] of [[3, 18], [2, 12], [1, 6], [0, 2]]) { x += delta / 8; frames.push(makeFrame(bridge[imageIndex], "preceding stop", `approved deceleration · ${delta} ku`, x, 1000 / timing.decelerationFps)); }
  const coreStart = frames.length;
  for (let i = 1; i < turn.length; i += 1) frames.push(makeFrame(turn[i], "turn to back", `Turn V9 · F${i + 1}`, x, 1000 / timing.turnFps));
  for (let i = turn.length - 2; i >= 0; i -= 1) frames.push(makeFrame(turn[i], "turn to side-left", `Turn V9 mirrored reverse · F${i + 1}`, x, 1000 / timing.turnFps, { flipX: true }));
  const coreEnd = frames.length - 1;
  for (const [imageIndex, delta] of [[1, 2], [2, 6], [3, 12], [4, 18]]) { x -= delta / 8; frames.push(makeFrame(bridge[imageIndex], "finishing acceleration", `approved bridge mirrored · ${delta} ku`, x, 1000 / timing.decelerationFps, { flipX: true })); }
  for (let i = 0; i < 8; i += 1) { x -= 21 / 8; const image = (i + 1) % 8; frames.push(makeFrame(walk[image], "finishing walk", `Walk V6 mirrored · F${image + 1}`, x, 1000 / timing.walkFps, { flipX: true })); }
  return { id: "approved-turn-round", title: "Approved components · walk → stop → 180° turn → walk", status: "approved component composition", summary: "The exact approved walk, stop and side↔back turn authorities composed into one contextual route.", kind: "native", stage: "plain-room", frames, coreRange: [coreStart, coreEnd] };
}

const sequences = [
  buildStopWalkStop(),
  buildTurnRound(),
  { id: "darts-v2", title: "Candidate · three darts → collect → leave", status: "new candidate awaiting Frank", summary: "Three repeated throws, board state, full-stride collection and departure. Use ghosts carefully.", kind: "native", stage: "darts-room", frames: dartsData.route, coreRange: dartsData.actionRange },
  { id: "stair-ascent", title: "Approved · room → stair ascent → upper door", status: "approved route", summary: "Complete approved Stair Transition V6 route.", kind: "external", url: "/keeper-review/keeper-prime-stair-transitions-v6/" },
  { id: "stair-descent", title: "Approved · upper door → stair descent → lower door", status: "approved with accepted slight overstride", summary: "Complete approved Stair Descent V2 route; final rail/balustrade will mask some foot motion.", kind: "external", url: "/keeper-review/keeper-prime-stair-descent-v2/" },
  { id: "ladder-ascent", title: "Approved motion · room → ladder → upper door", status: "approved motion; turn speed deferred", summary: "Complete Ladder Transition V6 page using approved V4/V5 motion and flat door correction.", kind: "external", url: "/keeper-review/keeper-prime-ladder-transitions-v6/" },
  { id: "seated-foundation", title: "Candidate · six seated endpoints V2", status: "foundation awaiting Frank", summary: "V2 keeps the six V1 Keeper images exact, fixes review loading and proves chair contact. Stand↔sit transitions are intentionally not claimed yet.", kind: "external", url: "/keeper-review/keeper-prime-seated-six-view-v2/" },
];

const catalog = {
  schema: "lighthouse-keeper/context-workbench@1", set, generatedOn: "2026-10-17", status: "review-only",
  purpose: "View every published Prime animation in the wider transition context appropriate to it, with optional preceding and finishing transitions.",
  exactPrimeGhost: exactPrime,
  inventorySummary: inventory.summary,
  inventoryUrl: "./inventory.json",
  sequences,
  boundaries: { finalChanged: false, runtimeChanged: false, productionChanged: false, approvalsChanged: false },
};
const catalogFile = path.join(outputDir, "catalog.json");
writeJson(catalogFile, catalog);
writeJson(path.join(outputDir, "inventory.json"), inventory);

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prime Keeper Context Workbench V1</title><style>
*{box-sizing:border-box}body{margin:0;background:#06121a;color:#eef8fb;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:20px}header{border-bottom:1px solid #294653}a{color:#8ed7ff}.status{display:inline-block;padding:5px 10px;border:1px solid #e7b956;color:#ffe09c;border-radius:999px}.panel{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:9px;flex-wrap:wrap;align-items:center}button,select{font:inherit;color:white;background:#173e53;border:1px solid #527585;border-radius:8px;padding:8px 11px}button:disabled,select:disabled{opacity:.45}.notice{border-left:4px solid #74e3a8;background:#142820;padding:12px}.warn{border-left:4px solid #e7b956;background:#2b2518;padding:12px}.viewport{overflow-x:auto;background:#050e14;padding:8px;border-radius:8px}.stage{position:relative;flex:none;background:linear-gradient(#17313b 0 91%,#405761 91% 94%,#17242b 94%);overflow:hidden}.stage:after{content:'';position:absolute;left:0;right:0;top:92.8%;border-top:1px solid #7d929a}.actor,.ghost{position:absolute;object-fit:contain;transform-origin:center;z-index:4}.ghost{opacity:.23;filter:hue-rotate(115deg) saturate(1.8);z-index:3}.adjacent{filter:hue-rotate(280deg) saturate(1.8)}.door{position:absolute;background:#6d5035;border:1px solid #c19a68;z-index:1}.board{position:absolute;border-radius:50%;background:radial-gradient(circle,#ead7af 0 12%,#233640 13% 25%,#d75545 26% 38%,#f1e4c8 39% 51%,#233640 52% 64%,#d75545 65% 77%,#f1e4c8 78%);border:1px solid #091015;z-index:2}.stuck{position:absolute;background:#d92e2e;z-index:3}.phase{color:#74e3a8;font-weight:700}.readout{font-variant-numeric:tabular-nums;min-height:3em}.external{width:100%;height:920px;border:1px solid #365665;border-radius:10px;background:#07131b}.badge{color:#ffe09c}.scales{display:grid;gap:15px}.hidden{display:none}@media(max-width:700px){.external{height:720px}}
</style></head><body><header><a href="/animation-workbench">← Existing animation workbench</a><h1>Prime Keeper Context Workbench V1</h1><span class="status">Draft and approved authorities · nothing promoted</span><p>Select a route, then review its core animation alone or with the preceding and finishing transition chains that the game will use.</p></header><main><p class="notice"><strong>Rule:</strong> an action is not reviewable in isolation. Native routes let you toggle their approach and finish. Longer approved stair/ladder routes open in their complete dedicated reviewer inside this page.</p><p class="warn"><strong>Bank coverage:</strong> all 308 production animations and technical neutrals have been measured and classified. This first workbench deliberately exposes only seven routes whose present status can be defended. The remaining 301 stay in the normalisation queue; they have not been silently approved. <a href="./inventory.json">Open the complete machine-readable inventory.</a></p><section class="panel"><div class="controls"><label>Animation <select id="sequence" disabled></select></label><label><input id="before" type="checkbox" checked disabled> preceding transition</label><label><input id="after" type="checkbox" checked disabled> finishing transition</label><label><input id="loop" type="checkbox" checked disabled> loop selection</label><label>speed <select id="speed" disabled><option value=".5">0.5×</option><option value=".75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option><option value="2">2×</option></select></label><button id="prev" disabled>← frame</button><button id="play" disabled>play</button><button id="pause" disabled>pause</button><button id="next" disabled>frame →</button><label><input id="primeGhost" type="checkbox" disabled> Prime ghost</label><label><input id="adjacentGhost" type="checkbox" disabled> previous-frame ghost</label></div><p id="loading" class="readout">Loading catalogue and decoding all native-route images…</p><p id="summary"></p><p id="readout" class="readout"></p></section><section id="native" class="panel scales"><div><h2>Large inspection · 8×</h2><div class="viewport"><div class="stage" data-scale="8"></div></div></div><div><h2>Proposed game presentation · 4×</h2><div class="viewport"><div class="stage" data-scale="4"></div></div></div><div><h2>Literal logical raster · 1×</h2><div class="viewport"><div class="stage" data-scale="1"></div></div></div></section><section id="externalWrap" class="panel hidden"><p class="warn">This longer route is already a complete contextual review. Use its own controls inside the embedded page.</p><iframe id="external" class="external" title="Selected complete animation review"></iframe></section></main><script>
let catalog,selected,timeline=[],index=0,timer=null;const stages=[...document.querySelectorAll('.stage')],controls=[...document.querySelectorAll('button,select,input')];function preload(src){return new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>{const d=i.decode?.();d?d.then(resolve).catch(resolve):resolve()};i.onerror=()=>reject(new Error(src));i.src=src})}function place(im,f,z){const w=f.anchorLp?.[0]===28?56:32,anchor=f.anchorLp||[16,40];im.src=f.src;im.style.width=(w*z)+'px';im.style.height=(40*z)+'px';im.style.left=((f.rootXLp-anchor[0])*z)+'px';im.style.top=(((f.bottomLp??52)-anchor[1])*z)+'px';im.style.transform=f.flipX?'scaleX(-1)':'none'}function setup(){for(const s of stages){const z=+s.dataset.scale;s.style.width=(172*z)+'px';s.style.height=(56*z)+'px';for(let n=0;n<3;n++){const q=document.createElement('i');q.className='stuck';q.dataset.dart=n;q.style.left=((165.5+n*.45)*z)+'px';q.style.top=((16.1+n*.65)*z)+'px';q.style.width=(2.5*z)+'px';q.style.height=Math.max(1,.5*z)+'px';s.appendChild(q)}for(const cls of ['ghost prime','ghost adjacent','actor']){const im=document.createElement('img');im.className=cls;s.appendChild(im)}}}function scenery(){for(const s of stages){s.querySelectorAll('.door,.board').forEach(x=>x.remove());if(selected.stage!=='darts-room')continue;const z=+s.dataset.scale,d=document.createElement('div'),b=document.createElement('div');d.className='door';d.style.cssText='left:'+(162*z)+'px;top:'+(4*z)+'px;width:'+(10*z)+'px;height:'+(48*z)+'px';b.className='board';b.style.cssText='left:'+(162*z)+'px;top:'+(13*z)+'px;width:'+(8*z)+'px;height:'+(8*z)+'px';s.prepend(b);s.prepend(d)}}function slice(){if(selected.kind!=='native')return[];const [a,b]=selected.coreRange,start=document.getElementById('before').checked?0:a,end=document.getElementById('after').checked?selected.frames.length-1:b;return selected.frames.slice(start,end+1)}function choose(){stop();selected=catalog.sequences.find(x=>x.id===document.getElementById('sequence').value);document.getElementById('summary').innerHTML='<span class="badge">'+selected.status+'</span> · '+selected.summary;const external=selected.kind==='external';document.getElementById('native').classList.toggle('hidden',external);document.getElementById('externalWrap').classList.toggle('hidden',!external);for(const id of ['before','after','loop','speed','prev','play','pause','next','primeGhost','adjacentGhost'])document.getElementById(id).disabled=external;if(external){document.getElementById('external').src=selected.url;document.getElementById('readout').textContent='Complete dedicated contextual reviewer loaded below.';return}timeline=slice();index=0;scenery();render()}function render(){if(!timeline.length)return;const f=timeline[index],prev=timeline[Math.max(0,index-1)];for(const s of stages){const z=+s.dataset.scale;place(s.querySelector('.actor'),f,z);place(s.querySelector('.adjacent'),prev,z);place(s.querySelector('.prime'),{...f,src:catalog.exactPrimeGhost,anchorLp:[28,40],flipX:false},z);s.querySelector('.prime').style.display=document.getElementById('primeGhost').checked?'block':'none';s.querySelector('.adjacent').style.display=document.getElementById('adjacentGhost').checked?'block':'none';s.querySelectorAll('.stuck').forEach((d,n)=>d.style.display=n<(f.boardDarts||0)?'block':'none')}document.getElementById('readout').innerHTML='<span class="phase">'+f.phase+'</span> · '+(index+1)+' / '+timeline.length+' · '+f.label+' · root '+f.rootXLp.toFixed(3)+' lp'}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){if(!timeline.length)return;render();const f=timeline[index],speed=+document.getElementById('speed').value;timer=setTimeout(()=>{if(index>=timeline.length-1){if(!document.getElementById('loop').checked){stop();return}index=0}else index++;tick()},f.durationMs/speed)}document.getElementById('sequence').onchange=choose;for(const id of ['before','after'])document.getElementById(id).onchange=()=>{stop();timeline=slice();index=0;render()};document.getElementById('prev').onclick=()=>{stop();index=index<=0?timeline.length-1:index-1;render()};document.getElementById('next').onclick=()=>{stop();index=index>=timeline.length-1?0:index+1;render()};document.getElementById('play').onclick=()=>{stop();tick()};document.getElementById('pause').onclick=stop;document.getElementById('primeGhost').onchange=render;document.getElementById('adjacentGhost').onchange=render;setup();fetch('./catalog.json').then(r=>r.json()).then(async c=>{catalog=c;const sel=document.getElementById('sequence');for(const s of c.sequences){const o=document.createElement('option');o.value=s.id;o.textContent=s.title;sel.appendChild(o)}const unique=[...new Set(c.sequences.filter(s=>s.kind==='native').flatMap(s=>s.frames.map(f=>f.src)).concat(c.exactPrimeGhost))];await Promise.all(unique.map(preload));controls.forEach(x=>x.disabled=false);document.getElementById('loading').textContent='All '+unique.length+' unique native-route images decoded before playback was enabled.';choose();tick()}).catch(e=>document.getElementById('loading').textContent='Workbench locked: '+e.message)
</script></body></html>`;
const pageFile = path.join(outputDir, "index.html");
fs.writeFileSync(pageFile, html);

const register = {
  schema: "lighthouse-keeper/review-batch@1", batchId: "keeper-prime-context-workbench-2026-10-17-v1", status: "review-tool-awaiting-frank",
  purpose: catalog.purpose, catalog: { file: rel(catalogFile), sha256: sha(catalogFile) }, page: { file: rel(pageFile), sha256: sha(pageFile) },
  coverage: sequences.map(({ id, title, status, kind }) => ({ id, title, status, kind })),
  features: ["animation selector", "preceding transition toggle", "finishing transition toggle", "whole/core looping", "frame stepping", "speed multiplier", "8x/4x/1x simultaneous views", "exact Prime ghost", "previous-frame onion skin", "full-route embedding", "complete 308-row inventory"],
  boundaries: catalog.boundaries,
  rollback: `Delete only public/keeper-review/${set} and art/drafts/keeper-prime-context-workbench-2026-10-17-v1.`,
};
const pack = path.join(root, "art/drafts/keeper-prime-context-workbench-2026-10-17-v1");
fs.mkdirSync(pack, { recursive: true });
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), `# Prime Keeper Context Workbench V1\n\nReview-only selector at \`/keeper-review/${set}/\`. Approved core routes and new candidates are explicitly labelled. Native routes can include/exclude preceding and finishing transitions; vertical routes retain their dedicated complete reviewers. Nothing is promoted.\n`);
console.log(JSON.stringify({ set, sequences: sequences.length, native: sequences.filter((entry) => entry.kind === "native").length, external: sequences.filter((entry) => entry.kind === "external").length, page: rel(pageFile) }, null, 2));
