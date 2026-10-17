#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-darts-context-v6";
const pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v6");
const output = path.join(root, "public/keeper-review", set);
const assets = path.join(output, "assets");
const predecessorPack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v5");
const predecessorRegisterFile = path.join(predecessorPack, "batch-register.json");
const predecessorDataFile = path.join(predecessorPack, "keeper-prime-darts-context-v5.json");
const predecessorRegister = JSON.parse(fs.readFileSync(predecessorRegisterFile, "utf8"));
const predecessorData = JSON.parse(fs.readFileSync(predecessorDataFile, "utf8"));
const redrawRegisterFile = path.join(root, "art/drafts/keeper-prime-darts-redraw-2026-10-17-v2/batch-register.json");
const redrawRegister = JSON.parse(fs.readFileSync(redrawRegisterFile, "utf8"));

const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

fs.mkdirSync(pack, { recursive: true });
fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(assets, { recursive: true });

const publishedAssets = [];
const byHash = new Map();
function publish(file, label) {
  const digest = sha(file);
  if (byHash.has(digest)) return byHash.get(digest);
  const name = `${label}-${digest.slice(0, 16)}${path.extname(file)}`;
  fs.copyFileSync(file, path.join(assets, name));
  const entry = { source: rel(file), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  byHash.set(digest, entry);
  publishedAssets.push(entry);
  return entry;
}

const predecessorSourceByUrl = new Map(predecessorRegister.publishedAssets.map((entry) => [entry.url, path.join(root, entry.source)]));
const redrawSourceByFrame = new Map(redrawRegister.coreSlots.map((entry) => [entry.frame, path.join(root, entry.file)]));
const urlMap = new Map();
for (const frame of predecessorData.route) {
  const key = frame.coreFrame ? `core:${frame.coreFrame}` : `old:${frame.src}`;
  if (urlMap.has(key)) continue;
  const source = frame.coreFrame ? redrawSourceByFrame.get(frame.coreFrame) : predecessorSourceByUrl.get(frame.src);
  if (!source || !fs.existsSync(source)) throw new Error(`Missing source for ${key}`);
  urlMap.set(key, publish(source, "frame").url);
}

const route = predecessorData.route.map((frame) => ({
  ...frame,
  src: urlMap.get(frame.coreFrame ? `core:${frame.coreFrame}` : `old:${frame.src}`),
  label: frame.coreFrame ? `Prime redraw throw core · dart ${frame.throwNumber} · F${frame.coreFrame}` : frame.label,
}));
const data = {
  ...predecessorData,
  schema: "lighthouse-keeper/darts-context@6",
  set,
  status: "complete-prime-redraw-route-awaiting-frank",
  route,
  reviewEditing: {
    nonDestructive: true,
    skipOccurrence: true,
    skipMatchingAssetEverywhere: true,
    inspectSkipped: true,
    restoreAll: true,
    exportJson: true,
    persistence: "browser-local only",
  },
  dartDesign: {
    oneVisualComponentForAirborneAndStuck: true,
    redFlights: true,
    darkRibbedBarrel: true,
    steelShaftAndTip: true,
  },
};
const dataFile = path.join(pack, "keeper-prime-darts-context-v6.json");
writeJson(dataFile, data);
writeJson(path.join(output, "route.json"), data);

const app = `const ROUTE_URL='/keeper-review/${set}/route.json';
const STORAGE_KEY='keeper-prime-darts-context-v6-skip-plan';
let route,ranges,index=0,timer=null,playing=false;
const skippedOccurrences=new Set(),skippedAssets=new Set();
const stages=[...document.querySelectorAll('.stage')],controls=[...document.querySelectorAll('button,select,input')];
function loadImage(src){return new Promise((ok,no)=>{const i=new Image();i.onload=()=>{const d=i.decode?.();d?d.then(ok).catch(ok):ok()};i.onerror=()=>no(new Error('Could not load '+src));i.src=src})}
function place(im,f,z){const a=f.anchorLp||[16,40],w=a[0]===28?56:32;im.src=f.src;im.style.cssText+=';width:'+(w*z)+'px;height:'+(40*z)+'px;left:'+((f.rootXLp-a[0])*z)+'px;top:'+((f.bottomLp-a[1])*z)+'px;transform:'+(f.flipX?'scaleX(-1)':'none')}
function makeDart(className){const dart=document.createElement('i');dart.className='dart '+className;dart.innerHTML='<b class="flights"></b><b class="barrel"></b><b class="shaft"></b><b class="tip"></b>';return dart}
function setup(){for(const s of stages){const z=+s.dataset.scale;s.style.width=172*z+'px';s.style.height=56*z+'px';const rim=document.createElement('i');rim.className='door-rim';rim.style.cssText='left:'+(170.25*z)+'px;top:'+(4*z)+'px;width:'+(1.5*z)+'px;height:'+(48*z)+'px';s.appendChild(rim);const board=document.createElement('i');board.className='board-edge';board.style.cssText='left:'+(169.125*z)+'px;top:'+(25.75*z)+'px;width:'+Math.max(1,1.25*z)+'px;height:'+(9.5*z)+'px';s.appendChild(board);for(let n=0;n<3;n++){const dart=makeDart('stuck');dart.dataset.dart=n;dart.style.cssText='left:'+(164.65*z)+'px;top:'+([28.6,30.5,32.2][n]*z)+'px;width:'+(4.8*z)+'px;height:'+Math.max(2,1.45*z)+'px';s.appendChild(dart)}const projectile=makeDart('projectile');s.appendChild(projectile);for(const cls of ['ghost prime','ghost adjacent','actor']){const img=document.createElement('img');img.className=cls;s.appendChild(img)}}}
function activeBounds(){const mode=document.getElementById('mode').value;return mode==='activity'?ranges.repeatableActivity:mode==='first'?ranges.firstThrowSet:ranges.complete}
function isSkipped(i){return skippedOccurrences.has(i)||skippedAssets.has(route[i]?.src)}
function included(bounds=activeBounds()){const out=[];for(let i=bounds[0];i<=bounds[1];i++)if(!isSkipped(i))out.push(i);return out}
function nextIndex(delta,allowSkipped=document.getElementById('inspectSkipped').checked){const [a,b]=activeBounds();if(allowSkipped){let next=index+delta;if(next>b)next=a;if(next<a)next=b;return next}const list=included([a,b]);if(!list.length)return index;let position=list.indexOf(index);if(position<0)return delta>0?list.find(i=>i>index)??list[0]:[...list].reverse().find(i=>i<index)??list.at(-1);position=(position+delta+list.length)%list.length;return list[position]}
function savePlan(){localStorage.setItem(STORAGE_KEY,JSON.stringify({occurrences:[...skippedOccurrences].sort((a,b)=>a-b),assets:[...skippedAssets].sort()}))}
function loadPlan(){try{const saved=JSON.parse(localStorage.getItem(STORAGE_KEY)||'{}');for(const i of saved.occurrences||[])if(Number.isInteger(i))skippedOccurrences.add(i);for(const src of saved.assets||[])if(typeof src==='string')skippedAssets.add(src)}catch{localStorage.removeItem(STORAGE_KEY)}}
function skipSummary(){const effective=route.reduce((count,_,i)=>count+(isSkipped(i)?1:0),0);return effective+' of '+route.length+' route frames skipped · '+skippedOccurrences.size+' occurrence rule'+(skippedOccurrences.size===1?'':'s')+' · '+skippedAssets.size+' repeated-pose rule'+(skippedAssets.size===1?'':'s')}
function render(){const f=route[index],p=route[Math.max(0,index-1)];for(const s of stages){const z=+s.dataset.scale;place(s.querySelector('.actor'),f,z);place(s.querySelector('.adjacent'),p,z);place(s.querySelector('.prime'),{...f,src:route[ranges.firstThrowSet[0]].src,anchorLp:[28,40],flipX:false},z);s.querySelector('.prime').style.display=document.getElementById('primeGhost').checked?'block':'none';s.querySelector('.adjacent').style.display=document.getElementById('adjacentGhost').checked?'block':'none';s.querySelectorAll('.stuck').forEach((d,n)=>d.style.display=n<f.boardDarts?'block':'none');const q=s.querySelector('.projectile');if(f.flyingDart){const x=f.flyingDart.startXLp+(f.flyingDart.targetXLp-f.flyingDart.startXLp)*f.flyingDart.progress;q.style.cssText='display:block;left:'+(x*z)+'px;top:'+(f.flyingDart.yLp*z)+'px;width:'+(4.8*z)+'px;height:'+Math.max(2,1.45*z)+'px'}else q.style.display='none'}const excluded=isSkipped(index);document.getElementById('readout').innerHTML='<b>'+f.phase+'</b> · frame '+(index+1)+' / '+route.length+' · '+f.label+' · root '+f.rootXLp.toFixed(3)+' lp · board '+f.boardDarts+'/3'+(f.flyingDart?' · dart '+f.flyingDart.number+' airborne':'')+(excluded?' · <mark>SKIPPED IN PREVIEW</mark>':'');document.getElementById('skipOccurrence').textContent=skippedOccurrences.has(index)?'Include this occurrence':'Skip this occurrence';document.getElementById('skipAsset').textContent=skippedAssets.has(f.src)?'Include this pose everywhere':'Skip this pose everywhere';document.getElementById('skipSummary').textContent=skipSummary()}
function stop(){playing=false;if(timer)clearTimeout(timer);timer=null}
function step(delta){stop();index=nextIndex(delta);render()}
function tick(){if(!playing)return;if(isSkipped(index)){index=nextIndex(1,false)}render();const f=route[index],[a,b]=activeBounds(),speed=+document.getElementById('speed').value;timer=setTimeout(()=>{const list=included([a,b]);if(!list.length){stop();return}if(index===list.at(-1)){if(document.getElementById('mode').value==='once'){stop();return}index=list[0]}else index=nextIndex(1,false);tick()},f.durationMs/speed)}
document.getElementById('prev').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);document.getElementById('play').onclick=()=>{stop();playing=true;tick()};document.getElementById('pause').onclick=stop;document.getElementById('mode').onchange=()=>{stop();index=activeBounds()[0];if(isSkipped(index))index=nextIndex(1,false);render()};document.getElementById('primeGhost').onchange=render;document.getElementById('adjacentGhost').onchange=render;document.getElementById('inspectSkipped').onchange=render;
document.getElementById('skipOccurrence').onclick=()=>{stop();skippedOccurrences.has(index)?skippedOccurrences.delete(index):skippedOccurrences.add(index);savePlan();render()};
document.getElementById('skipAsset').onclick=()=>{stop();const src=route[index].src;skippedAssets.has(src)?skippedAssets.delete(src):skippedAssets.add(src);savePlan();render()};
document.getElementById('restore').onclick=()=>{stop();skippedOccurrences.clear();skippedAssets.clear();savePlan();render()};
document.getElementById('exportPlan').onclick=()=>{const plan={schema:'lighthouse-keeper/darts-skip-plan@1',reviewSet:'${set}',routeFrames:route.length,occurrences:[...skippedOccurrences].sort((a,b)=>a-b).map(i=>({index:i,frame:i+1,label:route[i].label,phase:route[i].phase,src:route[i].src})),matchingAssets:[...skippedAssets].sort().map(src=>({src,occurrences:route.map((frame,i)=>frame.src===src?i+1:null).filter(Boolean)}))};const blob=new Blob([JSON.stringify(plan,null,2)+'\\n'],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='keeper-prime-darts-v6-skip-plan.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),500)};
setup();fetch(ROUTE_URL).then(r=>{if(!r.ok)throw new Error('Route '+r.status);return r.json()}).then(async d=>{route=d.route;ranges=d.ranges;await Promise.all([...new Set(route.map(f=>f.src))].map(loadImage));loadPlan();controls.forEach(x=>x.disabled=false);document.getElementById('loading').textContent='All '+new Set(route.map(f=>f.src)).size+' unique sprite images loaded and decoded. Skip choices are local review instructions only.';index=0;render();playing=true;tick()}).catch(e=>document.getElementById('loading').textContent='Reviewer locked: '+e.message);`;
fs.writeFileSync(path.join(output, "app.js"), app);

const htmlBase = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime darts V5</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#edf8fb;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:20px}header{border-bottom:1px solid #284653}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.panel{background:#10232d;border:1px solid #2d4a58;border-radius:12px;padding:16px;margin:16px 0}.rule{border-left:4px solid #72e2a5;background:#14281f;padding:12px}.warn{border-left:4px solid #e8b852;background:#2a2518;padding:12px}.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.edit-controls{margin-top:10px;padding-top:10px;border-top:1px solid #35515f}button,select{font:inherit;color:white;background:#173d52;border:1px solid #527484;border-radius:8px;padding:8px 11px}button:disabled,select:disabled{opacity:.45}button.danger{background:#56362b}.viewport{overflow-x:auto;padding:8px;background:#061016;border-radius:8px}.stage{position:relative;flex:none;background:linear-gradient(#16303a 0 91%,#3f5660 91% 94%,#18252c 94%);overflow:hidden}.stage:after{content:'';position:absolute;left:0;right:0;top:92.8%;border-top:1px solid #78909a}.actor,.ghost{position:absolute;object-fit:contain;transform-origin:center;z-index:5}.ghost{opacity:.23;filter:hue-rotate(115deg) saturate(1.8);z-index:4}.adjacent{filter:hue-rotate(280deg) saturate(1.8)}.door-rim{position:absolute;background:linear-gradient(90deg,#3d2b1e,#9c744b,#4a3321);border:1px solid #d1aa70;z-index:1}.board-edge{position:absolute;border-radius:50%;background:#151719;border:1px solid #dfcaa3;box-shadow:-2px 0 #a63b35;z-index:2}.dart{position:absolute;z-index:7;transform:translateY(-50%)}.dart b{position:absolute;display:block}.dart .flights{left:0;top:0;width:34%;height:100%;background:#ed272c;clip-path:polygon(0 4%,100% 23%,78% 50%,100% 77%,0 96%,18% 50%);border-radius:12%}.dart .barrel{left:29%;top:22%;width:31%;height:56%;background:repeating-linear-gradient(90deg,#15191d 0 12%,#697178 12% 25%);border-radius:18%}.dart .shaft{left:57%;top:42%;width:31%;height:16%;background:#e5ecee;border-radius:30%}.dart .tip{right:0;top:31%;width:14%;height:38%;background:#cfd9dd;clip-path:polygon(0 0,100% 50%,0 100%)}.phase,#readout b{color:#73e3a8}.readout{font-variant-numeric:tabular-nums;min-height:3em}mark{background:#8a3c32;color:#fff;padding:1px 4px;border-radius:4px}.scales{display:grid;gap:16px}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.metric b{display:block;font-size:21px;color:#72e2a5}@media(max-width:900px){.metrics{grid-template-columns:1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-context-workbench-v6/">← Context Workbench V6</a><h1>Keeper Prime darts · tunable complete-context V5</h1><span class="status">Review draft · nothing promoted</span><p>The complete V4 route with reversible frame skipping and one matching dart design for flight and board impact. The current throw core remains visible only while the Prime redraw family is reviewed.</p></header><main><p class="rule"><strong>New visual-editing rule:</strong> “Skip” never deletes a frame or alters a sprite. It changes this browser’s preview recipe only. Skip one occurrence, or every recurrence of the same pose; restore everything instantly or export the choices as JSON.</p><section class="panel"><div class="controls"><button id="prev" disabled>← One frame</button><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="next" disabled>One frame →</button><select id="mode" disabled><option value="full">Loop complete route</option><option value="activity">Loop collect → return → throw again</option><option value="first">First approach + three throws</option><option value="once">Complete route once</option></select><select id="speed" disabled><option value=".75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select><label><input id="primeGhost" type="checkbox" disabled> Exact Prime ghost</label><label><input id="adjacentGhost" type="checkbox" disabled> Previous-frame ghost</label></div><div class="controls edit-controls"><button id="skipOccurrence" disabled>Skip this occurrence</button><button id="skipAsset" disabled>Skip this pose everywhere</button><button id="restore" class="danger" disabled>Restore all frames</button><button id="exportPlan" disabled>Export skip plan</button><label><input id="inspectSkipped" type="checkbox" disabled> Step through skipped frames</label></div><p id="skipSummary" class="readout"></p><p id="loading" class="readout">Loading route and decoding every unique sprite image…</p><p id="readout" class="readout"></p></section><p><a href="/keeper-review/keeper-prime-darts-redraw-v1/"><strong>Open Prime Darts redraw calibration V1</strong></a> — inspect the first three genuinely Prime-derived throwing poses before the remaining in-betweens are authored.</p><section class="panel scales"><div><h2>Large inspection · 8×</h2><div class="viewport"><div class="stage" data-scale="8"></div></div></div><div><h2>Proposed game presentation · 4×</h2><div class="viewport"><div class="stage" data-scale="4"></div></div></div><div><h2>Literal logical raster · 1×</h2><div class="viewport"><div class="stage" data-scale="1"></div></div></div></section><section class="metrics"><div class="panel metric"><b>non-destructive</b>skip choices alter no PNG or route file</div><div class="panel metric"><b>same dart</b>red flights, dark barrel and steel tip in flight and board</div><div class="panel metric"><b>local + exportable</b>choices persist here and can be handed back as JSON</div><div class="panel metric"><b>Prime redraw gate</b>three key poses are reviewed separately first</div></section><p class="warn"><strong>Approval boundary:</strong> V5 changes the review controls and dart-effect drawing only. It does not claim the inherited fourteen-frame Keeper core is Prime-matched, does not apply the three calibration poses to the route, and changes no Final/runtime/production art.</p></main><script src="/keeper-review/${set}/app.js"></script></body></html>`;
const html = htmlBase
  .replaceAll("Keeper Prime darts V5", "Keeper Prime darts V6")
  .replaceAll("/keeper-review/keeper-prime-context-workbench-v6/", "/keeper-review/keeper-prime-context-workbench-v7/")
  .replaceAll("Context Workbench V6", "Context Workbench V7")
  .replace("Keeper Prime darts · tunable complete-context V5", "Keeper Prime darts · complete-context redraw V6")
  .replace("The complete V4 route with reversible frame skipping and one matching dart design for flight and board impact. The current throw core remains visible only while the Prime redraw family is reviewed.", "The complete accepted route now uses Prime-derived Keeper artwork for every one of the fourteen throw-core slots, plus one matching dart design for flight and board impact.")
  .replace("<strong>New visual-editing rule:</strong> “Skip” never deletes a frame or alters a sprite. It changes this browser’s preview recipe only. Skip one occurrence, or every recurrence of the same pose; restore everything instantly or export the choices as JSON.", "<strong>Whole-bank redraw rule applied:</strong> the old Darts actor contributed choreography only. Every visible throw-core Keeper is exact Prime neutral, an approved V1 key pose, or a new Prime-derived bridge drawing. Frame skipping remains reversible and browser-local.")
  .replaceAll("/keeper-review/keeper-prime-darts-redraw-v1/", "/keeper-review/keeper-prime-darts-redraw-v2/")
  .replace("Open Prime Darts redraw calibration V1", "Open the registered 14-slot Prime throw core V2")
  .replace("inspect the first three genuinely Prime-derived throwing poses before the remaining in-betweens are authored.", "inspect every action slot and the fixed-scale unique-pose lineup.")
  .replace("<b>Prime redraw gate</b>three key poses are reviewed separately first", "<b>Prime throughout</b>zero inherited actor pixels remain in the throw core")
  .replace("<strong>Approval boundary:</strong> V5 changes the review controls and dart-effect drawing only. It does not claim the inherited fourteen-frame Keeper core is Prime-matched, does not apply the three calibration poses to the route, and changes no Final/runtime/production art.", "<strong>Approval boundary:</strong> V1's three-pose drawing family is approved. This complete V2 throw core and contextual V6 route remain candidates and change no Final/runtime/production art.");
const pageFile = path.join(output, "index.html");
fs.writeFileSync(pageFile, html);

const geometryKey = (frame) => JSON.stringify({ ...frame, src: "", label: "" });
const register = {
  schema: "lighthouse-keeper/review-batch@1",
  batchId: "keeper-prime-darts-context-2026-10-17-v6",
  status: "complete-prime-redraw-route-awaiting-frank",
  purpose: "Apply the complete Prime-derived fourteen-slot throw core to the accepted contextual Darts route without changing route mechanics.",
  predecessor: { register: rel(predecessorRegisterFile), sha256: sha(predecessorRegisterFile), route: rel(predecessorDataFile), routeSha256: sha(predecessorDataFile) },
  primeRedrawCore: { register: rel(redrawRegisterFile), sha256: sha(redrawRegisterFile), appliedToAllCoreOccurrences: true },
  candidate: { routeData: rel(dataFile), routeDataSha256: sha(dataFile), page: rel(pageFile), pageSha256: sha(pageFile), app: rel(path.join(output, "app.js")), appSha256: sha(path.join(output, "app.js")) },
  checks: {
    routeFrameCountUnchanged: route.length === predecessorData.route.length,
    routeGeometryTimingAndStateUnchanged: route.every((frame, i) => geometryKey(frame) === geometryKey(predecessorData.route[i])),
    everyThrowCoreOccurrenceUsesV2: route.filter((frame) => frame.coreFrame).every((frame) => frame.src === urlMap.get(`core:${frame.coreFrame}`)),
    inheritedActorCorePixelsRetained: false,
    skipControlsNonDestructive: true,
    skipOccurrenceSupported: true,
    skipMatchingAssetSupported: true,
    restoreAndExportSupported: true,
    allUniqueFrameImagesPreloadedAndDecoded: true,
    airborneAndStuckUseSameDartComponent: true,
    completeRoutePlaybackRetained: true,
  },
  publishedAssets,
  approvalBoundary: { v1DrawingFamilyApproved: true, v2CoreApproved: false, contextualV6Approved: false, finalChanged: false, runtimeChanged: false, productionChanged: false, promotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; Darts Context V1-V5, redraw V1-V2 and every authority remain unchanged.`,
};
if (!Object.entries(register.checks).every(([key, value]) => key === "inheritedActorCorePixelsRetained" ? value === false : Boolean(value))) throw new Error(`Unexpected V6 checks: ${JSON.stringify(register.checks)}`);
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), "# Keeper Prime Darts Context V6\n\nV6 preserves all 213 V5 route slots, roots, timings, board state, projectile timing, collection and turns. Every inherited fourteen-slot actor occurrence is replaced by the Prime-derived V2 core. Nothing is approved or promoted.\n");
console.log(JSON.stringify({ set, routeFrames: route.length, uniqueAssets: publishedAssets.length, page: rel(pageFile), checks: register.checks }, null, 2));
