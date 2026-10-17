#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const set = "keeper-prime-darts-context-v3";
const pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v3");
const output = path.join(root, "public/keeper-review", set);
const assets = path.join(output, "assets");
const v2Pack = path.join(root, "art/drafts/keeper-prime-darts-context-2026-10-17-v2");
const v2Register = JSON.parse(fs.readFileSync(path.join(v2Pack, "batch-register.json"), "utf8"));
const walkDir = path.join(root, "art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames");
const bridgeDir = path.join(root, "art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames");
const turnRegisterFile = path.join(root, "art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json");
const turnRegister = JSON.parse(fs.readFileSync(turnRegisterFile, "utf8"));
const turnFiles = turnRegister.approvedCandidate.frames.map((entry) => path.join(root, entry.file));
const collectFiles = {
  partial: path.join(root, "art/drafts/keeper-prime-stair-transitions-2026-10-15-v1/drafts/frames/keeper_prime_door-reach-right_partial.png"),
  full: path.join(root, "art/drafts/keeper-prime-stair-transitions-2026-10-15-v1/drafts/frames/keeper_prime_door-reach-right_full.png"),
};
const timingFile = path.join(root, "data/keeper_timing_policy.json");
const timing = JSON.parse(fs.readFileSync(timingFile, "utf8")).transitionProfile;
const sha = (file) => crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
const rel = (file) => path.relative(root, file).split(path.sep).join("/");
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

const actionFiles = v2Register.candidate.frames.map((entry) => path.join(root, entry.file));
const walkFiles = Array.from({ length: 8 }, (_, index) => path.join(walkDir, `keeper_prime_walk-right_f${index + 1}.png`));
const bridgeFiles = Array.from({ length: 5 }, (_, index) => path.join(bridgeDir, `keeper_prime_stop-to-walk-right_f${index + 1}.png`));
for (const file of [...actionFiles, ...walkFiles, ...bridgeFiles, ...turnFiles, ...Object.values(collectFiles)]) {
  if (!fs.existsSync(file)) throw new Error(`Missing authority: ${rel(file)}`);
}

fs.mkdirSync(pack, { recursive: true });
fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(assets, { recursive: true });

const published = [];
const byHash = new Map();
function publish(file, label) {
  const digest = sha(file);
  if (byHash.has(digest)) return byHash.get(digest);
  const name = `${label}-${digest.slice(0, 16)}${path.extname(file)}`;
  fs.copyFileSync(file, path.join(assets, name));
  const entry = { source: rel(file), sourceSha256: digest, url: `/keeper-review/${set}/assets/${name}` };
  published.push(entry);
  byHash.set(digest, entry);
  return entry;
}

const action = actionFiles.map((file) => publish(file, "dart"));
const walk = walkFiles.map((file) => publish(file, "walk"));
const bridge = bridgeFiles.map((file) => publish(file, "bridge"));
const turn = turnFiles.map((file) => publish(file, "turn"));
const collect = Object.fromEntries(Object.entries(collectFiles).map(([key, file]) => [key, publish(file, "collect")]));

const stage = {
  logicalWidth: 172,
  logicalHeight: 56,
  floorBottomLp: 52,
  intendedGameScaleCssPxPerLp: 4,
  ocheRootXLp: 125,
  collectionRootXLp: 155.5,
  cupboardDoor: { state: "closed", presentation: "edge-on", rimXLp: [170.25, 171.75] },
  dartboard: { presentation: "edge-on outer rim only", planeXLp: 169.125, centreYLp: 30.5, heightLp: 9.5 },
};
const ACTION_ANCHOR = [28, 40];
const STANDARD_ANCHOR = [16, 40];
const dartYs = [28.6, 30.5, 32.2];
const flightProgress = [0.08, 0.3, 0.55, 0.78, 0.94];
const coreDurations = [170, 220, 230, 210, 175, 145, 115, 95, 95, 95, 115, 150, 175, 150];
const coreStart = 8;
const postureCount = 7;
const route = [];
const add = (asset, phase, label, rootXLp, durationMs, extra = {}) => route.push({
  src: asset.url,
  phase,
  label,
  rootXLp,
  bottomLp: 52,
  durationMs,
  anchorLp: extra.anchorLp ?? STANDARD_ANCHOR,
  flipX: extra.flipX ?? false,
  boardDarts: extra.boardDarts ?? 0,
  ...extra,
});

function addThrowSet(setNumber, rootXLp, startingBoardDarts) {
  add(action[0], `set ${setNumber} entry`, "byte-exact Prime side neutral", rootXLp, 100, { anchorLp: ACTION_ANCHOR, boardDarts: startingBoardDarts });
  for (let index = 1; index <= postureCount; index += 1) {
    add(action[index], `set ${setNumber} stance`, `approved posture bridge · F${index + 1}`, rootXLp, 1000 / timing.turnFps, { anchorLp: ACTION_ANCHOR, boardDarts: startingBoardDarts });
  }
  let boardDarts = startingBoardDarts;
  for (let dart = 1; dart <= 3; dart += 1) {
    for (let core = 0; core < 14; core += 1) {
      const flyingDart = core >= 5 && core <= 9 ? {
        number: dart,
        yLp: dartYs[dart - 1],
        startXLp: rootXLp + 15,
        targetXLp: stage.dartboard.planeXLp,
        progress: flightProgress[core - 5],
      } : null;
      if (core === 10) boardDarts = dart;
      add(
        action[coreStart + core],
        core < 5 ? `set ${setNumber} · dart ${dart} anticipation` : core < 11 ? `set ${setNumber} · dart ${dart} flight` : `set ${setNumber} · dart ${dart} recovery`,
        `identical V2 throw core · dart ${dart} · F${core + 1}`,
        rootXLp,
        coreDurations[core],
        { anchorLp: ACTION_ANCHOR, boardDarts, setNumber, throwNumber: dart, coreFrame: core + 1, flyingDart },
      );
    }
  }
  for (let index = coreStart + 14; index < action.length; index += 1) {
    add(action[index], index === action.length - 1 ? `set ${setNumber} complete` : `set ${setNumber} stance exit`, index === action.length - 1 ? "byte-exact Prime side neutral" : "approved posture bridge return", rootXLp, index === action.length - 1 ? 100 : 1000 / timing.turnFps, { anchorLp: ACTION_ANCHOR, boardDarts: 3, setNumber });
  }
}

function addStopToStop(direction, phase, from, boardDarts) {
  let x = from;
  const sign = direction === "right" ? 1 : -1;
  const flipX = direction === "left";
  for (const [imageIndex, delta] of [[1, 2], [2, 6], [3, 12], [4, 18]]) {
    x += sign * delta / 8;
    add(bridge[imageIndex], phase, `approved acceleration · ${delta} ku`, x, 1000 / timing.decelerationFps, { flipX, boardDarts });
  }
  for (let index = 0; index < 8; index += 1) {
    x += sign * 21 / 8;
    const imageIndex = (index + 1) % 8;
    add(walk[imageIndex], phase, `approved Walk V6 · F${imageIndex + 1}`, x, 1000 / timing.walkFps, { flipX, boardDarts });
  }
  for (const [imageIndex, delta] of [[3, 18], [2, 12], [1, 6], [0, 2]]) {
    x += sign * delta / 8;
    add(bridge[imageIndex], phase, `approved deceleration · ${delta} ku`, x, 1000 / timing.decelerationFps, { flipX, boardDarts });
  }
  return x;
}

function addTurn(from, to, phase, rootXLp, boardDarts) {
  if (from === "right" && to === "left") {
    for (let index = 1; index < turn.length; index += 1) add(turn[index], phase, `approved side-right → back · F${index + 1}`, rootXLp, 1000 / timing.turnFps, { boardDarts });
    for (let index = turn.length - 2; index >= 0; index -= 1) add(turn[index], phase, `approved back → side-left · F${index + 1}`, rootXLp, 1000 / timing.turnFps, { flipX: true, boardDarts });
  } else if (from === "left" && to === "right") {
    for (let index = 1; index < turn.length; index += 1) add(turn[index], phase, `approved side-left → back · F${index + 1}`, rootXLp, 1000 / timing.turnFps, { flipX: true, boardDarts });
    for (let index = turn.length - 2; index >= 0; index -= 1) add(turn[index], phase, `approved back → side-right · F${index + 1}`, rootXLp, 1000 / timing.turnFps, { boardDarts });
  } else throw new Error(`Unsupported turn ${from} → ${to}`);
}

let rootX = stage.ocheRootXLp - 46.75;
for (let index = 0; index < 16; index += 1) {
  rootX += 21 / 8;
  add(walk[index % 8], "walk to oche", `approved Walk V6 · F${index % 8 + 1}`, rootX, 1000 / timing.walkFps);
}
for (const [imageIndex, delta] of [[3, 18], [2, 12], [1, 6], [0, 2]]) {
  rootX += delta / 8;
  add(bridge[imageIndex], "stop at oche", `approved deceleration · ${delta} ku`, rootX, 1000 / timing.decelerationFps);
}
if (rootX !== stage.ocheRootXLp) throw new Error(`Oche approach ended at ${rootX}`);
addThrowSet(1, rootX, 0);
const loopStart = route.length - 1;

rootX = addStopToStop("right", "walk to collect", rootX, 3);
if (rootX !== stage.collectionRootXLp) throw new Error(`Collection approach ended at ${rootX}`);
for (let remaining = 3; remaining >= 1; remaining -= 1) {
  const dart = 4 - remaining;
  add(collect.partial, "collect darts", `reach toward dart ${dart}`, rootX, 110, { boardDarts: remaining });
  add(collect.full, "collect darts", `hand meets dart ${dart}`, rootX, 150, { boardDarts: remaining });
  add(collect.full, "collect darts", `dart ${dart} removed`, rootX, 100, { boardDarts: remaining - 1 });
  add(collect.partial, "collect darts", `retract with dart ${dart}`, rootX, 110, { boardDarts: remaining - 1 });
}
add(bridge[0], "collection complete", "byte-exact Prime side neutral", rootX, 100, { boardDarts: 0 });
addTurn("right", "left", "turn at board", rootX, 0);
rootX = addStopToStop("left", "walk back to oche", rootX, 0);
if (rootX !== stage.ocheRootXLp) throw new Error(`Return walk ended at ${rootX}`);
addTurn("left", "right", "turn at oche", rootX, 0);
addThrowSet(2, rootX, 0);
const loopEnd = route.length - 1;

const data = {
  schema: "lighthouse-keeper/darts-context@3",
  set,
  status: "draft-awaiting-frank",
  stage,
  route,
  ranges: {
    complete: [0, route.length - 1],
    firstThrowSet: [route.findIndex((entry) => entry.phase === "set 1 entry"), loopStart],
    repeatableActivity: [loopStart, loopEnd],
    secondThrowSet: [route.findIndex((entry) => entry.phase === "set 2 entry"), loopEnd],
  },
};
const dataFile = path.join(pack, "keeper-prime-darts-context-v3.json");
writeJson(dataFile, data);
const publicDataFile = path.join(output, "route.json");
writeJson(publicDataFile, data);

const app = `const ROUTE_URL='/keeper-review/${set}/route.json';let route,ranges,index=0,timer=null,playing=false;const stages=[...document.querySelectorAll('.stage')],controls=[...document.querySelectorAll('button,select,input')];function loadImage(src){return new Promise((ok,no)=>{const i=new Image();i.onload=()=>{const d=i.decode?.();d?d.then(ok).catch(ok):ok()};i.onerror=()=>no(new Error('Could not load '+src));i.src=src})}function place(im,f,z){const a=f.anchorLp||[16,40],w=a[0]===28?56:32;im.src=f.src;im.style.cssText+=';width:'+(w*z)+'px;height:'+(40*z)+'px;left:'+((f.rootXLp-a[0])*z)+'px;top:'+((f.bottomLp-a[1])*z)+'px;transform:'+(f.flipX?'scaleX(-1)':'none')}function setup(){for(const s of stages){const z=+s.dataset.scale;s.style.width=${stage.logicalWidth}*z+'px';s.style.height=${stage.logicalHeight}*z+'px';const rim=document.createElement('i');rim.className='door-rim';rim.style.cssText='left:'+(${stage.cupboardDoor.rimXLp[0]}*z)+'px;top:'+(4*z)+'px;width:'+(1.5*z)+'px;height:'+(48*z)+'px';s.appendChild(rim);const board=document.createElement('i');board.className='board-edge';board.style.cssText='left:'+(${stage.dartboard.planeXLp}*z)+'px;top:'+(${stage.dartboard.centreYLp-stage.dartboard.heightLp/2}*z)+'px;width:'+Math.max(1,1.25*z)+'px;height:'+(${stage.dartboard.heightLp}*z)+'px';s.appendChild(board);for(let n=0;n<3;n++){const dart=document.createElement('i');dart.className='stuck';dart.dataset.dart=n;dart.style.cssText='left:'+(${stage.dartboard.planeXLp-3.8}*z)+'px;top:'+(${JSON.stringify(dartYs)}[n]*z)+'px;width:'+(3.8*z)+'px;height:'+Math.max(1,.45*z)+'px';s.appendChild(dart)}const projectile=document.createElement('i');projectile.className='projectile';projectile.innerHTML='<b></b>';s.appendChild(projectile);for(const cls of ['ghost prime','ghost adjacent','actor']){const img=document.createElement('img');img.className=cls;s.appendChild(img)}}}function activeBounds(){const mode=document.getElementById('mode').value;return mode==='activity'?ranges.repeatableActivity:mode==='first'?ranges.firstThrowSet:ranges.complete}function render(){const f=route[index],p=route[Math.max(0,index-1)];for(const s of stages){const z=+s.dataset.scale;place(s.querySelector('.actor'),f,z);place(s.querySelector('.adjacent'),p,z);place(s.querySelector('.prime'),{...f,src:route[ranges.firstThrowSet[0]].src,anchorLp:[28,40],flipX:false},z);s.querySelector('.prime').style.display=document.getElementById('primeGhost').checked?'block':'none';s.querySelector('.adjacent').style.display=document.getElementById('adjacentGhost').checked?'block':'none';s.querySelectorAll('.stuck').forEach((d,n)=>d.style.display=n<f.boardDarts?'block':'none');const q=s.querySelector('.projectile');if(f.flyingDart){const x=f.flyingDart.startXLp+(f.flyingDart.targetXLp-f.flyingDart.startXLp)*f.flyingDart.progress;q.style.cssText='display:block;left:'+(x*z)+'px;top:'+(f.flyingDart.yLp*z)+'px;width:'+(3.5*z)+'px;height:'+Math.max(1,.45*z)+'px'}else q.style.display='none'}document.getElementById('readout').innerHTML='<b>'+f.phase+'</b> · frame '+(index+1)+' / '+route.length+' · '+f.label+' · root '+f.rootXLp.toFixed(3)+' lp · board '+f.boardDarts+'/3'+(f.flyingDart?' · dart '+f.flyingDart.number+' airborne':'')}function stop(){playing=false;if(timer)clearTimeout(timer);timer=null}function step(delta){stop();const [a,b]=activeBounds();index=index<a||index>b?a:index+delta;if(index>b)index=a;if(index<a)index=b;render()}function tick(){if(!playing)return;render();const f=route[index],[a,b]=activeBounds(),speed=+document.getElementById('speed').value;timer=setTimeout(()=>{if(index>=b){if(document.getElementById('mode').value==='once'){stop();return}index=document.getElementById('mode').value==='activity'?a+1:a}else index++;tick()},f.durationMs/speed)}document.getElementById('prev').onclick=()=>step(-1);document.getElementById('next').onclick=()=>step(1);document.getElementById('play').onclick=()=>{stop();playing=true;tick()};document.getElementById('pause').onclick=stop;document.getElementById('mode').onchange=()=>{stop();index=activeBounds()[0];render()};document.getElementById('primeGhost').onchange=render;document.getElementById('adjacentGhost').onchange=render;setup();fetch(ROUTE_URL).then(r=>{if(!r.ok)throw new Error('Route '+r.status);return r.json()}).then(async d=>{route=d.route;ranges=d.ranges;await Promise.all([...new Set(route.map(f=>f.src))].map(loadImage));controls.forEach(x=>x.disabled=false);document.getElementById('loading').textContent='All '+new Set(route.map(f=>f.src)).size+' unique sprite images loaded and decoded.';index=0;render();playing=true;tick()}).catch(e=>document.getElementById('loading').textContent='Reviewer locked: '+e.message);`;
fs.writeFileSync(path.join(output, "app.js"), app);

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime darts V3</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#edf8fb;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1500px;margin:auto;padding:20px}header{border-bottom:1px solid #284653}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.panel{background:#10232d;border:1px solid #2d4a58;border-radius:12px;padding:16px;margin:16px 0}.rule{border-left:4px solid #72e2a5;background:#14281f;padding:12px}.warn{border-left:4px solid #e8b852;background:#2a2518;padding:12px}.controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center}button,select{font:inherit;color:white;background:#173d52;border:1px solid #527484;border-radius:8px;padding:8px 11px}button:disabled,select:disabled{opacity:.45}.viewport{overflow-x:auto;padding:8px;background:#061016;border-radius:8px}.stage{position:relative;flex:none;background:linear-gradient(#16303a 0 91%,#3f5660 91% 94%,#18252c 94%);overflow:hidden}.stage:after{content:'';position:absolute;left:0;right:0;top:92.8%;border-top:1px solid #78909a}.actor,.ghost{position:absolute;object-fit:contain;transform-origin:center;z-index:5}.ghost{opacity:.23;filter:hue-rotate(115deg) saturate(1.8);z-index:4}.adjacent{filter:hue-rotate(280deg) saturate(1.8)}.door-rim{position:absolute;background:linear-gradient(90deg,#3d2b1e,#9c744b,#4a3321);border:1px solid #d1aa70;z-index:1}.board-edge{position:absolute;border-radius:50%;background:#151719;border:1px solid #dfcaa3;box-shadow:-2px 0 #a63b35;z-index:2}.stuck,.projectile{position:absolute;background:#dce5e8;border-radius:2px;z-index:7;transform:translateY(-50%)}.stuck:before,.projectile:before{content:'';position:absolute;left:0;top:-75%;width:24%;height:250%;background:#d92e2e;clip-path:polygon(0 0,100% 28%,100% 72%,0 100%)}.projectile b{position:absolute;right:-12%;top:-70%;width:20%;height:240%;background:#2b2b2b;border-radius:50%}.phase,#readout b{color:#73e3a8}.readout{font-variant-numeric:tabular-nums;min-height:3em}.scales{display:grid;gap:16px}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.metric b{display:block;font-size:21px;color:#72e2a5}@media(max-width:900px){.metrics{grid-template-columns:1fr}}
</style></head><body><header><a href="/keeper-review/keeper-prime-context-workbench-v2/">← Context workbench V2</a><h1>Keeper Prime darts · complete-context V3</h1><span class="status">Review draft · nothing promoted</span><p>Walk to the oche, throw three visible darts, collect all three, turn once, walk back, turn once, and throw the same three again.</p></header><main><p class="rule"><strong>Corrected room logic:</strong> the cupboard door is closed and seen edge-on. Only its thin rim and the dartboard edge are visible. The board centre is at 30.5 logical pixels, aligned to the approved full-reach hand.</p><section class="panel"><div class="controls"><button id="prev" disabled>← One frame</button><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="next" disabled>One frame →</button><select id="mode" disabled><option value="full">Loop complete route</option><option value="activity">Loop collect → return → throw again</option><option value="first">First approach + three throws</option><option value="once">Complete route once</option></select><select id="speed" disabled><option value=".75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select><label><input id="primeGhost" type="checkbox" disabled> Exact Prime ghost</label><label><input id="adjacentGhost" type="checkbox" disabled> Previous-frame ghost</label></div><p id="loading" class="readout">Loading route and decoding every unique sprite image…</p><p id="readout" class="readout"></p></section><section class="panel scales"><div><h2>Large inspection · 8×</h2><div class="viewport"><div class="stage" data-scale="8"></div></div></div><div><h2>Proposed game presentation · 4×</h2><div class="viewport"><div class="stage" data-scale="4"></div></div></div><div><h2>Literal logical raster · 1×</h2><div class="viewport"><div class="stage" data-scale="1"></div></div></div></section><section class="metrics"><div class="panel metric"><b>6 flights</b>each dart visibly travels into the board</div><div class="panel metric"><b>2 necessary turns</b>one at the board; one at the oche</div><div class="panel metric"><b>30.5 lp</b>exact full-stride stop-to-stop return</div><div class="panel metric"><b>exact loop seam</b>same Prime pixels, root and 3-dart state</div></section><p class="warn"><strong>Approval boundary:</strong> this is a new V3 route and measured scenery proposal. It reuses the V2 character pixels byte-for-byte, changes no approved art, and promotes nothing.</p></main><script src="/keeper-review/${set}/app.js"></script></body></html>`;
const pageFile = path.join(output, "index.html");
fs.writeFileSync(pageFile, html);

const register = {
  schema: "lighthouse-keeper/review-batch@1",
  batchId: "keeper-prime-darts-context-2026-10-17-v3",
  status: "draft-awaiting-frank",
  purpose: "Corrected edge-on cupboard-door darts loop with visible projectiles, practical collection height and only two necessary turn events.",
  authorities: {
    inheritedV2Candidate: { register: rel(path.join(v2Pack, "batch-register.json")), sha256: sha(path.join(v2Pack, "batch-register.json")), role: "all character action pixels; reused byte-for-byte" },
    approvedWalk: { directory: rel(walkDir), role: "all horizontal locomotion" },
    approvedStopBridge: { directory: rel(bridgeDir), role: "all acceleration/deceleration" },
    approvedTurn: { register: rel(turnRegisterFile), sha256: sha(turnRegisterFile), role: "two necessary 180-degree turns only" },
    approvedCollectionReach: Object.fromEntries(Object.entries(collectFiles).map(([key, file]) => [key, { file: rel(file), sha256: sha(file) }])),
  },
  candidate: { routeData: rel(dataFile), routeDataSha256: sha(dataFile), page: rel(pageFile), pageSha256: sha(pageFile) },
  checks: {
    v2ActionPixelsReusedByteForByte: actionFiles.every((file, index) => sha(file) === v2Register.candidate.frames[index].sha256),
    closedDoorEdgeOnly: true,
    practicalBoardReachAlignment: true,
    projectileFlights: route.filter((entry) => entry.flyingDart).length,
    turnEvents: 2,
    fullStrideCollectionAndReturnLp: 30.5,
    repeatableLoopEndpointsExact: route[loopStart].src === route[loopEnd].src && route[loopStart].rootXLp === route[loopEnd].rootXLp && route[loopStart].boardDarts === route[loopEnd].boardDarts,
  },
  publishedAssets: published,
  approvalBoundary: { candidateApproved: false, timingApproved: false, finalChanged: false, runtimeChanged: false, productionChanged: false, promotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; V1, V2 and every authority remain unchanged.`,
};
writeJson(path.join(pack, "batch-register.json"), register);
fs.writeFileSync(path.join(pack, "HANDOFF.md"), `# Keeper Prime Darts Context V3\n\nReview-only correction. The V2 character art is reused byte-for-byte. V3 changes only route choreography and measured room-state presentation: a closed edge-on cupboard door, a reachable dartboard rim, six visible flights/impacts, and a repeatable collect-return-rethrow activity loop. Nothing is promoted.\n`);
console.log(JSON.stringify({ set, routeFrames: route.length, loopRange: data.ranges.repeatableActivity, uniqueAssets: published.length, page: rel(pageFile) }, null, 2));
