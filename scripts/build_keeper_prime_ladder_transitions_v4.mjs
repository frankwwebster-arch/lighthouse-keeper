#!/usr/bin/env node
/** Build Ladder Transition V4: smooth opaque paint plus a persistent compositor. */

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const v3Set = 'keeper-prime-ladder-transitions-v3'
const set = 'keeper-prime-ladder-transitions-v4'
const v3Pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v3')
const pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v4')
const framesDir = path.join(pack, 'drafts/frames')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const v3SpecFile = path.join(v3Pack, 'keeper-prime-ladder-transitions-v3.json')
const v3RegisterFile = path.join(v3Pack, 'batch-register.json')
const v3PageFile = path.join(root, 'public/keeper-review', v3Set, 'index.html')
const specFile = path.join(pack, 'keeper-prime-ladder-transitions-v4.json')
const pageFile = path.join(publicDir, 'index.html')
const solidPaintFloor = 240

const read = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = file => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => {
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n')
}

for (const file of [v3SpecFile, v3RegisterFile, v3PageFile]) {
  if (!fs.existsSync(file)) throw new Error(`missing ${file}`)
}
fs.mkdirSync(framesDir, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const v3Spec = read(v3SpecFile)
const v3Register = read(v3RegisterFile)
const spec = structuredClone(v3Spec)
spec.set = set
spec.layering = {
  orderBackToFront: ['ladder', 'keeper', 'floor', 'door', 'guides'],
  keeperAlphaMode: 'solid-paint-floor-240-with-original-antialiased-fringe',
  ladderPixelsSuppressed: false,
  persistentCompositor: true,
  purpose: 'keep every ladder pixel, make Keeper interior paint fully opaque, retain the smooth source fringe, and never replace DOM during playback',
}
spec.opacity = {
  solidPaintFloor,
  operation: 'source alpha >= 240 becomes 255; source alpha 1..239 and its RGB remain byte-identical',
  appliesTo: 'all 29 unique Keeper review frames',
}
spec.delivery = {
  allUniqueFramesDecodedBeforePlayback: true,
  allUniqueFramesMountedBeforePlayback: true,
  frameSwitch: 'atomic visibility switch between persistent decoded image nodes',
  architectureRebuiltDuringPlayback: false,
}

const urlMap = new Map()
const publishedAssets = []
const alphaNormalization = []
for (const entry of v3Register.publishedAssets) {
  const source = path.join(root, entry.source)
  if (!fs.existsSync(source) || sha(source) !== entry.sourceSha256) throw new Error(`source drift: ${entry.source}`)
  const input = PNG.sync.read(fs.readFileSync(source))
  const output = new PNG({ width: input.width, height: input.height })
  let hardenedPixels = 0
  let preservedFringePixels = 0
  for (let offset = 0; offset < input.data.length; offset += 4) {
    for (let channel = 0; channel < 4; channel++) output.data[offset + channel] = input.data[offset + channel]
    const alpha = input.data[offset + 3]
    if (alpha >= solidPaintFloor) {
      output.data[offset + 3] = 255
      hardenedPixels += Number(alpha !== 255)
    } else if (alpha > 0) preservedFringePixels++
  }
  const base = path.basename(source, '.png')
  const draft = path.join(framesDir, `${base}-paint-opaque.png`)
  fs.writeFileSync(draft, PNG.sync.write(output))
  const digest = sha(draft)
  const publicName = `${base}-paint-opaque-${digest.slice(0, 16)}.png`
  const published = path.join(assetsDir, publicName)
  fs.copyFileSync(draft, published)
  const url = `/keeper-review/${set}/assets/${publicName}`
  urlMap.set(entry.url, url)
  publishedAssets.push({
    source: rel(source),
    sourceSha256: entry.sourceSha256,
    draft: rel(draft),
    draftSha256: digest,
    published: rel(published),
    url,
    bytes: fs.statSync(published).size,
    changeScope: 'alpha-only solid-paint normalization with source fringe retained',
  })
  alphaNormalization.push({
    source: rel(source),
    sourceSha256: entry.sourceSha256,
    draft: rel(draft),
    draftSha256: digest,
    pixels: [input.width, input.height],
    solidPaintFloor,
    hardenedPixels,
    preservedFringePixels,
    rgbChangedPixels: 0,
  })
}

for (const route of Object.values(spec.routes)) {
  for (const frame of route.frames) {
    const nextUrl = urlMap.get(frame.src)
    if (!nextUrl) throw new Error(`unmapped V3 URL: ${frame.src}`)
    frame.src = nextUrl
  }
}
writeJson(specFile, spec)

let html = fs.readFileSync(v3PageFile, 'utf8')
html = html.replaceAll('Keeper Prime ladder transitions V3', 'Keeper Prime ladder transitions V4')
html = html.replace(
  'Opacity correction of V2: the complete ladder now remains present in every frame, while the Keeper alone is alpha-hardened after registration. Timing and geometry are unchanged.',
  'Flicker correction of V3: Keeper interior paint is opaque, the original smooth antialiased fringe is restored, and every decoded frame remains mounted throughout playback. Timing and geometry are unchanged.',
)
html = html.replace(
  'Four exact mirrored left/right gait cycles close the storey without phase remainder. Turns remain 20 fps and climbing 6.67 fps. No ladder pixel is hidden by a review mask.',
  'Four exact mirrored left/right gait cycles close the storey without phase remainder. Turns remain 20 fps and climbing 6.67 fps. The complete ladder is persistent and no playback frame rebuilds the scene.',
)
html = html.replace(
  '.keeper{position:absolute;width:32px;height:40px;object-fit:contain;transform-origin:50% 98.75%;z-index:4}',
  '.keeper{position:absolute;width:32px;height:40px;object-fit:contain;transform-origin:50% 98.75%;z-index:4;visibility:hidden;will-change:transform,left,top,visibility}.keeper.active{visibility:visible}',
)
html = html.replace(
  '<section class="metrics"><article><b>Opaque Keeper</b>alpha ≥128 hardened after resize</article><article><b>Complete ladder</b>zero suppressed rung pixels</article>',
  '<section class="metrics"><article><b>Opaque paint</b>solid interior raised to alpha 255</article><article><b>Smooth fringe</b>source antialiasing retained</article><article><b>Persistent compositor</b>zero DOM replacement during playback</article><article><b>Complete ladder</b>zero suppressed rung pixels</article>',
)
html = html.replace(
  'First inspect the bottom turn and climbing loop: the ladder must remain structurally complete with rungs visible through genuine gaps, but never bleed through painted Keeper pixels. Timing, roots, geometry and the accepted hand/foot rung tolerance are unchanged from V2.',
  'Inspect the complete route for any flash or blank repaint: all Keeper frames and the complete ladder are mounted before playback begins. Rungs remain visible through genuine gaps but cannot bleed through solid Keeper paint. Timing, roots, geometry and the accepted hand/foot rung tolerance are unchanged from V2/V3.',
)
html = html.replace(/const SPEC=.*?;\nconst routeSelect=/s, `const SPEC=${JSON.stringify(spec)};\nconst routeSelect=`)

const runtimeStart = html.indexOf('const routeSelect=')
const runtimeEnd = html.indexOf('</script>', runtimeStart)
if (runtimeStart < 0 || runtimeEnd < 0) throw new Error('V3 runtime boundary changed')
const runtime = `const routeSelect=document.getElementById('route'),stages=[...document.querySelectorAll('.stage')],controls=[...document.querySelectorAll('button,select')];let routeId='gait',index=0,timer=null,speed=1;
for(const [id,route] of Object.entries(SPEC.routes)){const option=document.createElement('option');option.value=id;option.textContent=route.title;routeSelect.append(option)}
function active(){return SPEC.routes[routeId].frames}function px(value,scale){return value*scale+'px'}
const unique=[...new Set(Object.values(SPEC.routes).flatMap(route=>route.frames.map(frame=>frame.src)))],decoded=new Map();
function add(world,className,left,top,width,height,scale){const e=document.createElement('div');e.className=className;e.style.left=px(left,scale);e.style.top=px(top,scale);e.style.width=px(width,scale);e.style.height=px(height,scale);world.append(e);return e}
function prepareStage(stage){const scale=Number(stage.dataset.scale),world=stage.querySelector('.world'),nodes={rungs:[],keepers:new Map(),active:null};world.replaceChildren();add(world,'rail',95,4,1.5,112,scale);add(world,'rail',111.5,4,1.5,112,scale);for(let y=3.5;y<=116;y+=7.5){const rung=add(world,'rung',95,y,18,1,scale);rung.dataset.baseY=String(y);nodes.rungs.push(rung)}add(world,'floor',0,116,172,16,scale);add(world,'floor',0,56,95,4,scale);add(world,'floor',113,56,59,4,scale);nodes.leftDoor=add(world,'door',8,68,24,48,scale);nodes.rightDoor=add(world,'door',158,8,14,48,scale);for(const src of unique){const img=decoded.get(src).cloneNode();img.className='keeper';img.alt='Keeper ladder frame';img.decoding='sync';world.append(img);nodes.keepers.set(src,img)}nodes.cell=add(world,'cell',0,0,32,40,scale);nodes.root=add(world,'root',0,0,1.2,1.2,scale);stage._nodes=nodes}
function renderStage(stage){const scale=Number(stage.dataset.scale),frame=active()[index],nodes=stage._nodes,offset=frame.ladderOffsetLp||0;for(const rung of nodes.rungs)rung.style.transform=\`translateY(\${offset*scale}px)\`;nodes.leftDoor.style.visibility=(routeId==='approach'||routeId==='full')?'visible':'hidden';nodes.rightDoor.style.visibility=(routeId==='exit'||routeId==='full')?'visible':'hidden';const img=nodes.keepers.get(frame.src);img.style.left=px(frame.xLp-16,scale);img.style.top=px(frame.rootYLp-40,scale);img.style.width=px(32,scale);img.style.height=px(40,scale);img.style.transform=\`scale(\${frame.artScale})\`;if(nodes.active!==img){if(nodes.active)nodes.active.classList.remove('active');img.classList.add('active');nodes.active=img}nodes.cell.style.left=px(frame.xLp-16,scale);nodes.cell.style.top=px(frame.rootYLp-40,scale);nodes.root.style.left=px(frame.xLp-.6,scale);nodes.root.style.top=px(frame.rootYLp-.6,scale)}
function render(){stages.forEach(renderStage);const frames=active(),f=frames[index];document.getElementById('readout').textContent=\`\${SPEC.routes[routeId].title} · F\${index+1}/\${frames.length} · \${f.phase} · root (\${f.xLp}, \${f.rootYLp}) lp\`;document.getElementById('progress').style.width=((index+1)/frames.length*100)+'%'}
function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){const frames=active();if(index>=frames.length-1){if(!document.getElementById('loop').checked)return stop();index=0}else index++;render();timer=setTimeout(tick,frames[index].durationMs/speed)}function play(){stop();if(index>=active().length-1)index=0;render();timer=setTimeout(tick,active()[index].durationMs/speed)}
routeSelect.onchange=e=>{stop();routeId=e.target.value;index=0;render();play()};document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{stop();index=Math.max(0,index-1);render()};document.getElementById('next').onclick=()=>{stop();index=Math.min(active().length-1,index+1);render()};document.getElementById('restart').onclick=()=>{stop();index=0;render();play()};document.getElementById('guides').onchange=e=>stages.forEach(stage=>stage.classList.toggle('hide-guides',!e.target.checked));document.getElementById('speed').oninput=e=>{speed=Number(e.target.value)/100;document.getElementById('speedLabel').textContent=e.target.value+'%';if(timer)play()};
function preload(src){return new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>{const ready=()=>{decoded.set(src,image);resolve()};const promise=image.decode?.();promise?promise.then(ready).catch(ready):ready()};image.onerror=()=>reject(new Error(src));image.src=src})}Promise.all(unique.map(preload)).then(()=>{stages.forEach(prepareStage);controls.forEach(control=>control.disabled=false);document.getElementById('loading').textContent=\`All \${unique.length} unique frames decoded and persistently mounted before playback\`;requestAnimationFrame(()=>requestAnimationFrame(()=>{render();play()}))}).catch(error=>{document.getElementById('loading').textContent='Playback locked: '+error.message});
`
html = html.slice(0, runtimeStart) + runtime + html.slice(runtimeEnd)
fs.writeFileSync(pageFile, html)

fs.writeFileSync(path.join(pack, 'HANDOFF.md'), `# Keeper Prime ladder transitions V4

V4 supersedes V3 for review. It restores each original source frame's smooth antialiased fringe, raises only solid paint (alpha >= ${solidPaintFloor}) to fully opaque, and retains all RGB values. The complete ladder is never masked. The review compositor decodes and mounts all 29 unique frames before playback, then performs atomic visibility switches without recreating either the Keeper or architecture. V2/V3 timing, frame order, roots, geometry and accepted hand/foot-to-rung tolerance remain exact. Nothing is promoted.

Review: \`/keeper-review/${set}/\`.
`)

const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-ladder-transitions-2026-10-16-v4',
  status: 'draft-awaiting-visual-review',
  purpose: 'Remove edge shimmer and DOM repaint flashes while keeping the complete ladder and opaque Keeper paint.',
  authorities: {
    v3Spec: { file: rel(v3SpecFile), sha256: sha(v3SpecFile) },
    v3Register: { file: rel(v3RegisterFile), sha256: sha(v3RegisterFile) },
    v3Page: { file: rel(v3PageFile), sha256: sha(v3PageFile) },
  },
  alphaNormalization,
  spec: { file: rel(specFile), sha256: sha(specFile) },
  reviewPage: { file: rel(pageFile), sha256: sha(pageFile), publicReview: `/keeper-review/${set}/`, preloadsAllUniqueFrames: true, mountsAllUniqueFrames: true },
  publishedAssets,
  changes: {
    v3BinaryEdgeRejected: true,
    ladderPixelsSuppressed: false,
    keeperRgbChanged: false,
    solidPaintFloor,
    sourceFringePreserved: true,
    persistentCompositor: true,
    rootOrGeometryChanged: false,
    timingChangedFromV3: false,
    rungContactChanged: false,
  },
  validation: { productionChanged: false, runtimeChanged: false, finalChanged: false },
  approvalBoundary: { candidateApproved: false, finalLaneEntryAllowed: false, productionPromotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and ${rel(publicDir)}; V1/V2/V3, approved sources, Final, runtime and production remain unchanged.`,
}
writeJson(path.join(pack, 'batch-register.json'), register)

console.log(JSON.stringify({ page: rel(pageFile), uniqueFrames: publishedAssets.length, solidPaintFloor, persistentCompositor: true, ladderPixelsSuppressed: false }, null, 2))
