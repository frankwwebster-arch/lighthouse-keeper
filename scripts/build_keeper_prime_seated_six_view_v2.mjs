#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const sourceSet = 'keeper-prime-seated-six-view-v1'
const set = 'keeper-prime-seated-six-view-v2'
const sourcePack = path.join(root, 'art/drafts/keeper-prime-seated-six-view-2026-10-16-v1')
const pack = path.join(root, 'art/drafts/keeper-prime-seated-six-view-2026-10-17-v2')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const geometry = JSON.parse(fs.readFileSync(path.join(sourcePack, `${sourceSet}.json`), 'utf8'))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = file => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

fs.mkdirSync(pack, { recursive: true })
fs.rmSync(publicDir, { recursive: true, force: true })
fs.mkdirSync(assetsDir, { recursive: true })

const seatY = 29 * 8
const seatX = 16 * 8
const views = []
for (const direction of geometry.directions) {
  const source = path.join(root, direction.image)
  const png = PNG.sync.read(fs.readFileSync(source))
  const alpha = png.data[(seatY * png.width + seatX) * 4 + 3]
  if (alpha < 192) throw new Error(`${direction.id}: no opaque pelvis at exact seat contact ${seatX},${seatY}`)
  for (const y of [seatY - 1, seatY, seatY + 1]) {
    let count = 0
    for (let x = 0; x < png.width; x++) if (png.data[(y * png.width + x) * 4 + 3] >= 192) count++
    if (count < 96) throw new Error(`${direction.id}: body does not continuously occupy seat plane at y=${y}`)
  }
  const digest = sha(source)
  const assetName = `seat-${direction.id}-${digest.slice(0, 16)}.png`
  fs.copyFileSync(source, path.join(assetsDir, assetName))
  views.push({
    id: direction.id,
    src: `/keeper-review/${set}/assets/${assetName}`,
    source: rel(source),
    sha256: digest,
    contact: { pixel: [seatX, seatY], logical: [16, 29], alpha },
    bounds: direction.registeredBounds,
  })
}

const contact = {
  schema: 'lighthouse-keeper/seated-contact-proof@1',
  set,
  status: 'review-draft-no-promotion',
  sourceSet,
  cell: { logical: [32, 40], pixels: [256, 320], density: 8, anchorLp: [16, 40] },
  chair: {
    surfaceTopLp: 29,
    surfaceTopPixel: seatY,
    heightAboveFloorLp: 11,
    renderLayer: 'behind-keeper',
    rule: 'The chair top edge is exactly y=29 lp. The opaque pelvis crosses that same pixel row in every view, so there is neither a visible gap nor a foreground surface cutting through the Keeper.',
  },
  loading: {
    firstViewRenderedBeforePreload: true,
    primaryViewsGateControls: true,
    auxiliaryComparisonsGateControls: false,
    failureReporting: 'per URL via Promise.allSettled',
  },
  views,
  boundaries: { sourcePixelsChanged: false, v1Changed: false, runtimeChanged: false, finalChanged: false, productionChanged: false, promotionAllowed: false },
}
const contactFile = path.join(pack, 'keeper-prime-seated-six-view-v2.json')
writeJson(contactFile, contact)

const cards = views.map(view => `<article><h3>${view.id.replaceAll('-', ' ')}</h3><div class="cell"><div class="chair small"></div><img src="${view.src}" alt="Prime Keeper seated ${view.id}"><i class="contactDot" aria-hidden="true"></i></div></article>`).join('')
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime seated six-view V2</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1380px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.panel{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}button{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled{opacity:.45}.stageGrid{display:grid;grid-template-columns:minmax(700px,768px) minmax(260px,1fr);gap:24px;align-items:start}.stage{position:relative;width:768px;height:960px;background:repeating-conic-gradient(#17303b 0 25%,#112833 0 50%) 50%/48px 48px;overflow:hidden}.stage img,.cell img,.game img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;z-index:2}.chair{position:absolute;left:15%;right:15%;top:72.5%;height:9%;background:#6b4a2a;border:0;border-top:6px solid #c49255;z-index:1}.chair:before,.chair:after{content:'';position:absolute;top:100%;width:8%;height:190%;background:#6b4a2a}.chair:before{left:5%}.chair:after{right:5%}.seatLine{position:absolute;left:0;right:0;top:72.5%;border-top:3px solid #ffd25f;z-index:4;pointer-events:none}.floorLine{position:absolute;left:0;right:0;top:98.75%;border-top:3px solid #62e0aa;z-index:4}.contactDot{position:absolute;left:50%;top:72.5%;width:13px;height:13px;transform:translate(-50%,-50%);border-radius:50%;background:#ff5c82;border:2px solid white;z-index:5}.labels{position:absolute;inset:0;z-index:5;pointer-events:none}.labels b{position:absolute;left:8px;padding:2px 5px;background:#07131bcc}.labels .seat{top:calc(72.5% - 31px);color:#ffe095}.labels .floor{top:calc(98.75% - 31px);color:#8df2c4}.gameWrap{display:grid;grid-template-columns:32px 256px;gap:18px;align-items:start}.game{position:relative;width:32px;height:40px;background:#17303b}.game.zoom{width:256px;height:320px;image-rendering:pixelated}.game .chair{border-top-width:1px}.game.zoom .chair{border-top-width:2px}.game .contactDot{width:1px;height:1px;border:0}.game.zoom .contactDot{width:6px;height:6px;border:1px solid white}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee;min-height:3em}.cards{display:grid;grid-template-columns:repeat(3,minmax(250px,1fr));gap:14px}.cards article{background:#0c1d26;border:1px solid #2c4a59;border-radius:10px;padding:12px}.cards h3{text-transform:capitalize}.cell{position:relative;width:256px;height:320px;margin:auto;background:repeating-conic-gradient(#17303b 0 25%,#112833 0 50%) 50%/16px 16px}.cell .chair{border-top-width:2px}.cell .contactDot{width:6px;height:6px;border:1px solid white}@media(max-width:1100px){.stageGrid{grid-template-columns:1fr}.stage{max-width:100%;height:auto;aspect-ratio:4/5}.cards{grid-template-columns:repeat(2,1fr)}}@media(max-width:720px){.cards{grid-template-columns:1fr}.gameWrap{grid-template-columns:1fr}}
</style></head><body><header><a href="/keeper-review/${sourceSet}/">← Historical V1</a><h1>Keeper Prime seated six-view V2</h1><span class="status">Loading + physical seat-contact correction · no art promotion</span><p>The same six reversible endpoint drawings, now shown against a chair whose top surface is mathematically locked to the Keeper’s pelvis contact plane.</p></header><main><p class="rule"><strong>Seat rule:</strong> the chair surface begins at exactly y=29 logical pixels (232 source pixels), 11 logical pixels above the floor. The pink contact marker is that exact coordinate. The chair is behind the Keeper: the pelvis covers the surface at contact, while the top remains visible beside him. There is no vertical gap and the chair never crosses in front of his body.</p><section class="panel"><div class="controls"><button id="prev" disabled>← Previous view</button><button id="next" disabled>Next view →</button><button id="play" disabled>Rotate views</button><button id="pause" disabled>Pause</button><label><input id="guides" type="checkbox" checked> Show contact proof</label></div><p id="loading" class="readout">The first view is visible immediately. Checking all six primary images…</p><p id="readout" class="readout"></p></section><section class="panel stageGrid"><div><h2>Large contact inspection</h2><div class="stage"><div class="chair"></div><img id="large" alt="Selected seated Prime Keeper view"><span class="seatLine"></span><span class="floorLine"></span><i class="contactDot"></i><div class="labels"><b class="seat">chair top + pelvis contact · y 29 lp</b><b class="floor">floor anchor · y 40 lp</b></div></div></div><div><h2>Game composition</h2><p>Literal 32 × 40 raster and an 8× nearest-neighbour inspection of those same logical pixels.</p><div class="gameWrap"><div class="game"><div class="chair"></div><img id="game" alt="Literal game raster"><i class="contactDot"></i></div><div class="game zoom"><div class="chair"></div><img id="zoom" alt="Magnified exact game raster"><i class="contactDot"></i></div></div></div></section><section class="panel"><h2>All six physical contacts</h2><div class="cards">${cards}</div></section></main><script>
const views=${JSON.stringify(views)};let index=0,timer=null;const large=document.getElementById('large'),game=document.getElementById('game'),zoom=document.getElementById('zoom'),buttons=[...document.querySelectorAll('button')];function render(){const v=views[index];large.src=game.src=zoom.src=v.src;document.getElementById('readout').textContent=(index+1)+' / '+views.length+' · '+v.id.replaceAll('-',' ')+' · exact contact '+v.contact.logical.join(',')+' lp / '+v.contact.pixel.join(',')+' px · alpha '+v.contact.alpha}function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){index=(index+1)%views.length;render();timer=setTimeout(tick,900)}document.getElementById('prev').onclick=()=>{stop();index=(index+views.length-1)%views.length;render()};document.getElementById('next').onclick=()=>{stop();index=(index+1)%views.length;render()};document.getElementById('play').onclick=()=>{stop();tick()};document.getElementById('pause').onclick=stop;document.getElementById('guides').onchange=e=>document.querySelectorAll('.seatLine,.floorLine,.contactDot,.labels').forEach(x=>x.style.display=e.target.checked?'block':'none');function preload(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const decoded=im.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};im.onerror=()=>reject(new Error(src));im.src=src})}render();Promise.allSettled(views.map(v=>preload(v.src))).then(results=>{const failed=results.map((r,i)=>r.status==='rejected'?views[i].id:null).filter(Boolean);if(failed.length){document.getElementById('loading').textContent='Review locked: failed primary images: '+failed.join(', ');return}buttons.forEach(x=>x.disabled=false);document.getElementById('loading').textContent='All six primary seated images loaded and decoded. Controls enabled.'})
</script></body></html>`
const pageFile = path.join(publicDir, 'index.html')
fs.writeFileSync(pageFile, html)

const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-seated-six-view-2026-10-17-v2',
  status: 'draft-contact-and-loading-correction-awaiting-frank',
  source: { set: sourceSet, geometry: rel(path.join(sourcePack, `${sourceSet}.json`)), geometrySha256: sha(path.join(sourcePack, `${sourceSet}.json`)) },
  contactProof: { file: rel(contactFile), sha256: sha(contactFile) },
  page: { file: rel(pageFile), sha256: sha(pageFile) },
  boundaries: contact.boundaries,
  rollback: `Delete only ${rel(pack)} and public/keeper-review/${set}; V1 and every source image remain unchanged.`,
}
writeJson(path.join(pack, 'batch-register.json'), register)
console.log(JSON.stringify({ set, views: views.length, seatTopLp: 29, seatTopPixel: seatY, sourcePixelsChanged: false, review: rel(pageFile) }, null, 2))
