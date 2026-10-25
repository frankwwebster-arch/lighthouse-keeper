#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const V12_DIR = 'art/drafts/kitchen-room-layout-review-2026-10-25-v12/native-assets'
const OUT = 'art/drafts/kitchen-room-layout-review-2026-10-25-v13/native-assets'
const PUBLIC = 'public/keeper-review/kitchen-room-layout-v13/assets'
const PAGE_DIR = 'public/keeper-review/kitchen-room-layout-v13'
const V12_PAGE = 'public/keeper-review/kitchen-room-layout-v12/index.html'
const V12_REGISTER = `${V12_DIR}/extraction-register.json`
const V12_REGISTER_SHA256 = 'fa7eb77f5d9b68db2e104e369401bc1e8e410d15ef78ad9a4ab8c9d7fcbdacfd'

const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => sha256(fs.readFileSync(file))
const offset = (png, x, y) => (y * png.width + x) * 4
const readPng = file => PNG.sync.read(fs.readFileSync(file))
const blank = (width, height) => new PNG({ width, height, colorType: 6 })
const clone = png => {
  const copy = blank(png.width, png.height)
  copy.data.set(png.data)
  return copy
}
const replace = (text, before, after) => {
  if (!text.includes(before)) throw new Error(`V12 page transform target missing: ${before.slice(0, 120)}`)
  return text.replace(before, after)
}
const blendPixel = (png, x, y, rgba) => {
  if (x < 0 || y < 0 || x >= png.width || y >= png.height) return
  const i = offset(png, x, y), sourceAlpha = rgba[3] / 255, targetAlpha = png.data[i + 3] / 255
  const outAlpha = sourceAlpha + targetAlpha * (1 - sourceAlpha)
  if (!outAlpha) return
  for (let channel = 0; channel < 3; channel += 1) png.data[i + channel] = Math.round((rgba[channel] * sourceAlpha + png.data[i + channel] * targetAlpha * (1 - sourceAlpha)) / outAlpha)
  png.data[i + 3] = Math.round(outAlpha * 255)
}
const paintDisc = (png, cx, cy, radius, rgba) => {
  for (let y = Math.floor(cy - radius); y <= Math.ceil(cy + radius); y += 1) for (let x = Math.floor(cx - radius); x <= Math.ceil(cx + radius); x += 1) {
    if ((x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2) blendPixel(png, x, y, rgba)
  }
}
const strokeCurve = (png, points, radius, rgba) => {
  for (let index = 1; index < points.length; index += 1) {
    const [x0, y0] = points[index - 1], [x1, y1] = points[index]
    const steps = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0)))
    for (let step = 0; step <= steps; step += 1) {
      const t = step / steps
      paintDisc(png, x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, radius, rgba)
    }
  }
}
const pointInPolygon = (x, y, polygon) => {
  let inside = false
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const [xi, yi] = polygon[i], [xj, yj] = polygon[j]
    if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) inside = !inside
  }
  return inside
}

fs.mkdirSync(OUT, { recursive: true })
fs.mkdirSync(PUBLIC, { recursive: true })
fs.mkdirSync(PAGE_DIR, { recursive: true })
if (hash(V12_REGISTER) !== V12_REGISTER_SHA256) throw new Error('Kitchen V12 register changed')
const v12 = JSON.parse(fs.readFileSync(V12_REGISTER, 'utf8'))
const outputs = {}

for (const [id, source] of Object.entries(v12.outputs)) {
  const bytes = fs.readFileSync(source.file)
  if (sha256(bytes) !== source.sha256) throw new Error(`${id} V12 source changed`)
  const filename = `${id}-native.png`
  fs.writeFileSync(path.join(OUT, filename), bytes)
  fs.writeFileSync(path.join(PUBLIC, filename), bytes)
  outputs[id] = {
    ...source,
    file: `${OUT}/${filename}`,
    publicReviewFile: `${PUBLIC}/${filename}`,
    inheritedByteIdenticalFromV12: true,
  }
}

const writeOutput = (id, png, metadata) => {
  const filename = `${id}-native.png`
  const bytes = PNG.sync.write(png, { colorType: 6 })
  fs.writeFileSync(path.join(OUT, filename), bytes)
  fs.writeFileSync(path.join(PUBLIC, filename), bytes)
  outputs[id] = {
    ...(outputs[id] ?? {}),
    file: `${OUT}/${filename}`,
    publicReviewFile: `${PUBLIC}/${filename}`,
    dimensions: [png.width, png.height],
    sha256: sha256(bytes),
    inheritedByteIdenticalFromV12: false,
    ...metadata,
  }
}

// Redraw the broken state from the complete standard bowl so the full curved
// body and foot/base are real source pixels. A connected jagged notch removes
// the front-left wall; the base, contact plane and eight-pixel gutter survive.
const bowl = clone(readPng(v12.outputs['bowl-standard'].file))
const missingFrontLeft = [[31, 42], [58, 44], [52, 53], [63, 59], [54, 68], [67, 77], [57, 87], [44, 82], [34, 73], [24, 61]]
for (let y = 0; y < bowl.height; y += 1) for (let x = 0; x < bowl.width; x += 1) {
  if (!pointInPolygon(x + .5, y + .5, missingFrontLeft)) continue
  bowl.data.fill(0, offset(bowl, x, y), offset(bowl, x, y) + 4)
}
const dark = [30, 35, 36, 255]
for (let y = 1; y < bowl.height - 1; y += 1) for (let x = 1; x < bowl.width - 1; x += 1) {
  const i = offset(bowl, x, y)
  if (!bowl.data[i + 3]) continue
  let bordersBreak = false
  for (let dy = -1; dy <= 1; dy += 1) for (let dx = -1; dx <= 1; dx += 1) {
    if (pointInPolygon(x + dx + .5, y + dy + .5, missingFrontLeft)) bordersBreak = true
  }
  if (bordersBreak) bowl.data.set(dark, i)
}
const crackPaths = [
  [[59, 44], [66, 50], [64, 57], [70, 62]],
  [[57, 87], [64, 93], [62, 100], [67, 105]],
  [[34, 73], [28, 79], [30, 86]],
]
for (const points of crackPaths) {
  for (let index = 1; index < points.length; index += 1) {
    const [x0, y0] = points[index - 1], [x1, y1] = points[index]
    const steps = Math.ceil(Math.hypot(x1 - x0, y1 - y0))
    for (let step = 0; step <= steps; step += 1) {
      const x = Math.round(x0 + (x1 - x0) * step / steps), y = Math.round(y0 + (y1 - y0) * step / steps), i = offset(bowl, x, y)
      if (bowl.data[i + 3]) bowl.data.set(dark, i)
    }
  }
}
writeOutput('bowl-broken', bowl, {
  predecessorSha256: v12.outputs['bowl-broken'].sha256,
  constructionAuthority: v12.outputs['bowl-standard'].file,
  constructionAuthoritySha256: v12.outputs['bowl-standard'].sha256,
  contactRow: 116,
  contactSurfaceRow: 116,
  deepestAlphaRow: 116,
  anchorX: 69,
  fullBaseRetained: true,
  missingSection: 'connected jagged front-left wall notch',
  detachedDebrisRemoved: true,
  contactShadowIncluded: false,
  correction: 'complete bowl body and foot/base retained; only a connected front-left section is missing, with restrained cracks and no debris',
})

// Neutralise the three rejected static warning-lens positions inside the
// separate Broken overlay. The new independently animated lenses are then the
// sole light pixels, so accepted offsets cannot expose old arcs to their right.
const broken = clone(readPng(v12.outputs['fitted-overlay-broken'].file))
const oldLensRects = [[722, 118, 18, 20], [744, 118, 18, 20], [766, 118, 18, 20]]
for (const [rectX, rectY, rectW, rectH] of oldLensRects) {
  for (let y = rectY; y < rectY + rectH; y += 1) {
    const samples = []
    for (let x = 790; x <= 820; x += 1) {
      const i = offset(broken, x, y)
      if (broken.data[i + 3]) samples.push([broken.data[i], broken.data[i + 1], broken.data[i + 2], broken.data[i + 3]])
    }
    const rgba = samples.length ? [0, 1, 2, 3].map(channel => Math.round(samples.reduce((sum, sample) => sum + sample[channel], 0) / samples.length)) : [248, 238, 209, 255]
    for (let x = rectX; x < rectX + rectW; x += 1) broken.data.set(rgba, offset(broken, x, y))
  }
}
writeOutput('fitted-overlay-broken', broken, {
  predecessorSha256: v12.outputs['fitted-overlay-broken'].sha256,
  neutralisedWarningLensRects: oldLensRects,
  correction: 'old fixed warning lamps and their right-edge arcs are replaced by panel pixels in the separate Broken overlay',
})

const warningPalettes = {
  amber: [245, 159, 31],
  cyan: [31, 174, 224],
  violet: [157, 83, 214],
}
const recolourLens = (source, targetRgb) => {
  const target = clone(source)
  for (let y = 0; y < target.height; y += 1) for (let x = 0; x < target.width; x += 1) {
    const i = offset(target, x, y), a = target.data[i + 3]
    if (!a) continue
    const r = target.data[i], g = target.data[i + 1], b = target.data[i + 2]
    const luminance = r * .2126 + g * .7152 + b * .0722
    const spread = Math.max(r, g, b) - Math.min(r, g, b)
    if (luminance < 42 || (luminance > 210 && spread < 45)) continue
    const gain = Math.max(.28, Math.min(1.2, luminance / 150))
    target.data[i] = Math.min(255, Math.round(targetRgb[0] * gain))
    target.data[i + 1] = Math.min(255, Math.round(targetRgb[1] * gain))
    target.data[i + 2] = Math.min(255, Math.round(targetRgb[2] * gain))
  }
  return target
}
const warningFiles = []
for (let number = 1; number <= 3; number += 1) {
  const source = readPng(v12.outputs[`dishwasher-warning-${number}`].file)
  const family = []
  for (const [colour, rgb] of Object.entries(warningPalettes)) {
    const id = colour === 'amber' ? `dishwasher-warning-${number}` : `dishwasher-warning-${number}-${colour}`
    writeOutput(id, recolourLens(source, rgb), {
      predecessorSha256: v12.outputs[`dishwasher-warning-${number}`].sha256,
      basePosition: v12.outputs[`dishwasher-warning-${number}`].basePosition,
      transparentSafetyGutter: 4,
      lightColour: colour,
      targetRgb: rgb,
      correction: 'isolated complete lens with no adjacent panel or neighbouring-light pixels',
    })
    family.push(`${id}-native.png`)
  }
  warningFiles.push(family)
}

// Preserve the three appliance spill ownership zones, but remove the sink's
// straight clip edges and deepen only the dishwasher-owned spill. The added
// dishwasher water is translucent, irregular and finely stippled with foam;
// it never enters the oven interval.
const water = clone(readPng(v12.outputs['broken-floor-water'].file))
const sinkLeft = [384, 382, 380, 378, 375, 373, 371, 369, 368, 369, 371, 373, 375]
const sinkRight = [618, 620, 623, 626, 629, 632, 634, 636, 638, 640, 640, 640, 640]
for (let y = 10; y <= 22; y += 1) {
  const left = sinkLeft[y - 10], right = sinkRight[y - 10]
  for (let x = 360; x < left; x += 1) water.data.fill(0, offset(water, x, y), offset(water, x, y) + 4)
  for (let x = right + 1; x <= 640; x += 1) water.data.fill(0, offset(water, x, y), offset(water, x, y) + 4)
  for (const x of [left, left + 1, right - 1, right]) water.data[offset(water, x, y) + 3] = Math.round(water.data[offset(water, x, y) + 3] * .62)
}
// Remove the predecessor's rectangular dishwasher patch before composing the
// larger V13 spill. This keeps the water's silhouette organic at both ends.
for (let y = 0; y < water.height; y += 1) for (let x = 650; x <= 930; x += 1) {
  water.data.fill(0, offset(water, x, y), offset(water, x, y) + 4)
}
const BODY = [83, 177, 207, 82], DEEP = [34, 132, 171, 66], LIGHT = [173, 222, 231, 112], FOAM = [245, 249, 239, 158]
strokeCurve(water, [[663, 20], [691, 16], [722, 19], [751, 17], [782, 21], [815, 17], [846, 20], [876, 16], [903, 21]], 6.5, BODY)
strokeCurve(water, [[672, 28], [705, 24], [741, 30], [777, 25], [812, 31], [848, 25], [879, 31], [902, 27]], 7.5, BODY)
strokeCurve(water, [[695, 37], [728, 33], [763, 39], [799, 34], [836, 39], [870, 34], [900, 38]], 4.5, DEEP)
let seed = 0x13d15a7
const random = () => {
  seed = (seed * 1664525 + 1013904223) >>> 0
  return seed / 0x100000000
}
for (let index = 0; index < 76; index += 1) {
  const x = 673 + Math.floor(random() * 232), y = 14 + Math.floor(random() * 27)
  const radius = .55 + random() * 1.25
  paintDisc(water, x, y, radius, random() > .34 ? FOAM : LIGHT)
}
for (const points of [
  [[678, 20], [696, 18], [714, 21], [732, 18]],
  [[744, 28], [762, 25], [780, 29], [798, 25]],
  [[810, 20], [829, 17], [848, 21], [868, 18]],
  [[847, 35], [865, 32], [884, 36], [905, 33]],
]) strokeCurve(water, points, .85, FOAM)
for (let y = 0; y < water.height; y += 1) for (let x = 911; x <= 1144; x += 1) {
  water.data.fill(0, offset(water, x, y), offset(water, x, y) + 4)
}
writeOutput('broken-floor-water', water, {
  predecessorSha256: v12.outputs['broken-floor-water'].sha256,
  supportPlane: 'walking-floor',
  spillIntervals: { sink: [360, 640], dishwasher: [650, 910], oven: null, fridge: [1145, 1375] },
  sinkEdgeTreatment: 'native-pixel tapered irregular alpha boundary; no full-height vertical clip edge',
  dishwasherTreatment: 'expanded translucent puddle with deterministic fine foam stipple and streaks; no outlined cartoon bubbles',
  correction: 'sink clip edges softened; dishwasher-owned frothy spill enlarged without assigning water to the oven',
})

for (const keeperName of ['prime-keeper-neutral-native-256x320.png', 'prime-keeper-seated-back-native-256x320.png']) {
  const archive = JSON.parse(fs.readFileSync('review-archive/index.json', 'utf8'))
  const entry = archive.legacyPaths[`/keeper-review/kitchen-room-layout-v12/assets/${keeperName}`]
  if (!entry) throw new Error(`Missing archived V12 Keeper ${keeperName}`)
  fs.writeFileSync(path.join(PUBLIC, keeperName), fs.readFileSync(path.join('review-archive', entry.object.replace(/^review-archive\//, ''))))
}

const acceptedWarningOffsets = [[-5, -2], [-5, -2], [-5, -2]]
const register = {
  ...v12,
  schema: 'lighthouse-keeper/kitchen-native-assets@13',
  status: 'review-only-unapproved-v13-bowl-lights-and-water-redraft',
  predecessor: { register: V12_REGISTER, sha256: V12_REGISTER_SHA256 },
  corrections: {
    ...v12.corrections,
    bowl: 'complete standard-bowl body and foot/base retained; connected front-left wall section removed with restrained cracks and no debris',
    dishwasher: 'accepted -5,-2 offsets; old arcs removed; amber/cyan/violet isolated lenses change colour and blink at irregular random intervals',
    floorWater: 'sink edges taper organically; dishwasher spill is larger, translucent and finely frothy; oven remains dry',
    movement: 'drag mutation is scoped by asset kind so worktop movement cannot alter table, chair or any floor anchor',
  },
  reviewCalibration: {
    ...v12.reviewCalibration,
    dishwasherWarningAcceptedOffsets: acceptedWarningOffsets,
    dishwasherWarningColours: Object.keys(warningPalettes),
    dishwasherWarningFiles: warningFiles,
    brokenBowlInitialContactOffsetY: 0,
  },
  outputs,
}
fs.writeFileSync(path.join(OUT, 'extraction-register.json'), `${JSON.stringify(register, null, 2)}\n`)

let page = fs.readFileSync(V12_PAGE, 'utf8')
page = replace(page, '<title>Kitchen V12 · closed oven flicker and exact effect positioning</title>', '<title>Kitchen V13 · complete bowl, calibrated lights and organic spills</title>')
page = replace(page, '<h1>Closed oven flicker and exact effect positioning</h1>', '<h1>Complete bowl, calibrated lights and organic spills</h1>')
page = replace(page,
  '<p class="lede">V11 remains immutable predecessor evidence. V12 shifts the unchanged sink geyser eight native pixels behind the basin front, keeps the Broken oven closed while its interior flickers behind the existing glass, removes the rejected fascia overlay, and exposes exact native-pixel calibration for the dishwasher lenses and broken-bowl contact.</p>',
  '<p class="lede">V12 remains immutable predecessor evidence. V13 restores the broken bowl\'s complete foot/base, applies the approved −5,−2 dishwasher-lens offsets, removes the exposed old-lens arcs, introduces irregular amber/cyan/violet warning colours, enlarges the dishwasher\'s fine frothy spill and removes the sink puddle\'s straight clip edges.</p>')
page = page.replaceAll('/keeper-review/kitchen-room-layout-v12/assets/', '/keeper-review/kitchen-room-layout-v13/assets/')
page = replace(page, "const ROOT='/keeper-review/kitchen-room-layout-v13/assets/',V='?v=12';", "const ROOT='/keeper-review/kitchen-room-layout-v13/assets/',V='?v=13';")
page = page.replaceAll('Review-only V12', 'Review-only V13')
page = page.replaceAll('V12 calibration family', 'V13 corrected family')
page = replace(page,
  "const FITTED={base:'fitted-units-static-native.png',on:'fitted-overlay-on-native.png',broken:'fitted-overlay-broken-native.png',water:'broken-floor-water-native.png',oven:'oven-broken-cavity-light-native.png',warnings:['dishwasher-warning-1-native.png','dishwasher-warning-2-native.png','dishwasher-warning-3-native.png'],sink:",
  `const FITTED={base:'fitted-units-static-native.png',on:'fitted-overlay-on-native.png',broken:'fitted-overlay-broken-native.png',water:'broken-floor-water-native.png',oven:'oven-broken-cavity-light-native.png',warnings:${JSON.stringify(warningFiles)},sink:`)
page = replace(page, 'contacts:{standard:116,broken:54},anchors:{standard:69,broken:65}', 'contacts:{standard:116,broken:116},anchors:{standard:69,broken:69}')
page = replace(page,
  'const WARNING_BASES=[[720,116],[742,116],[764,116]];let model=defaults(),ready=false,drag=null,warningDrag=null,warningOffsets=[[0,0],[0,0],[0,0]],bowlDepth=0;',
  `const WARNING_BASES=[[720,116],[742,116],[764,116]],ACCEPTED_WARNING_OFFSETS=${JSON.stringify(acceptedWarningOffsets)};let model=defaults(),ready=false,drag=null,warningDrag=null,warningOffsets=ACCEPTED_WARNING_OFFSETS.map(offset=>[...offset]),warningTimers=[],bowlDepth=0;`)
page = replace(page,
  '.camera.broken .w1{animation:blinkA 2.5s steps(1,end) infinite}.camera.broken .w2{animation:blinkB 3s steps(1,end) infinite}.camera.broken .w3{animation:blinkC 3.5s steps(1,end) infinite}',
  '')
page = replace(page, '.asset{position:absolute;z-index:5;max-width:none;cursor:grab;filter:none}', '.asset{position:absolute;z-index:5;max-width:none;cursor:grab;filter:none;touch-action:none}')
page = replace(page,
  "function startDrag(e){if(!ready)return;const node=e.currentTarget,name=node.dataset.name;if((name==='kettle'||name==='toaster')&&model.state[name]==='broken'){$('status').textContent=ASSETS[name].label+' is broken and movement-locked.';return}const p=point(e);drag={node,name,dx:p.x-parseFloat(node.style.left),dy:p.y-parseFloat(node.style.top)};node.setPointerCapture(e.pointerId);node.style.zIndex=20;node.onpointermove=moveDrag;node.onpointerup=endDrag;node.onpointercancel=endDrag}",
  "function startDrag(e){if(!ready)return;const node=e.currentTarget,name=node.dataset.name;if((name==='kettle'||name==='toaster')&&model.state[name]==='broken'){$('status').textContent=ASSETS[name].label+' is broken and movement-locked.';return}e.preventDefault();e.stopPropagation();const p=point(e);drag={node,name,dx:p.x-parseFloat(node.style.left),dy:p.y-parseFloat(node.style.top),lastPoint:p,counterBefore:{...model.counter},worktopBefore:{...model.worktop},floorBefore:{...model.floor}};node.setPointerCapture(e.pointerId);node.style.zIndex=20;node.onpointermove=moveDrag;node.onpointerup=endDrag;node.onpointercancel=endDrag;node.onlostpointercapture=endDrag;document.addEventListener('pointerup',endDrag,{once:true});document.addEventListener('pointercancel',endDrag,{once:true})}")
page = replace(page,
  "function moveDrag(e){if(!drag)return;const p=point(e),w=drag.node.naturalWidth,h=drag.node.naturalHeight;drag.node.style.left=Math.max(0,Math.min(STAGE_W-w,p.x-drag.dx))+'px';drag.node.style.top=Math.max(0,Math.min(STAGE_H-h,p.y-drag.dy))+'px'}",
  "function moveDrag(e){if(!drag)return;e.preventDefault();e.stopPropagation();const p=point(e),w=drag.node.naturalWidth,h=drag.node.naturalHeight;drag.lastPoint=p;drag.node.style.left=Math.max(0,Math.min(STAGE_W-w,p.x-drag.dx))+'px';drag.node.style.top=Math.max(0,Math.min(STAGE_H-h,p.y-drag.dy))+'px'}")
page = replace(page,
  "function endDrag(e){if(!drag)return;const {node,name}=drag,p=point(e),kind=ASSETS[name].kind;node.onpointermove=node.onpointerup=node.onpointercancel=null;if(kind==='counter')swap(model.counter,name,nearest(p.x,COUNTER_CENTRES.slice(0,2)));else if(kind==='worktop')model.worktop[name]=nearest(p.x,COUNTER_CENTRES);else model.floor[name]=nearest(p.x,FLOOR_CENTRES);$('status').textContent=ASSETS[name].label+' snapped to pace '+centreFor(name)/PACE+'.';drag=null;renderRoom()}",
  "function endDrag(e){if(!drag)return;if(e?.preventDefault)e.preventDefault();if(e?.stopPropagation)e.stopPropagation();const active=drag,{node,name}=active,p=e&&Number.isFinite(e.clientX)?point(e):active.lastPoint,kind=ASSETS[name].kind;drag=null;node.onpointermove=node.onpointerup=node.onpointercancel=node.onlostpointercapture=null;if(kind==='counter')swap(model.counter,name,nearest(p.x,COUNTER_CENTRES.slice(0,2)));else if(kind==='worktop')model.worktop[name]=nearest(p.x,COUNTER_CENTRES);else model.floor[name]=nearest(p.x,FLOOR_CENTRES);if(kind!=='counter')model.counter={...active.counterBefore};if(kind!=='worktop')model.worktop={...active.worktopBefore};if(kind!=='floor')model.floor={...active.floorBefore};$('status').textContent=ASSETS[name].label+' snapped to pace '+centreFor(name)/PACE+'. '+(kind==='worktop'?'Table and chair anchors unchanged.':'Only the '+kind+' placement scope changed.');renderRoom()}")
page = replace(page,
  "function renderWarningPositions(){document.querySelectorAll('.warningLight').forEach((node,n)=>{node.style.left=WARNING_BASES[n][0]+warningOffsets[n][0]+'px';node.style.top=WARNING_BASES[n][1]+warningOffsets[n][1]+'px'});$('lightOffsets').textContent=warningOffsets.map((o,n)=>'L'+(n+1)+' '+(o[0]>=0?'+':'')+o[0]+','+(o[1]>=0?'+':'')+o[1]).join(' · ')}",
  "function renderWarningPositions(){document.querySelectorAll('.warningLight').forEach((node,n)=>{node.style.left=WARNING_BASES[n][0]+warningOffsets[n][0]+'px';node.style.top=WARNING_BASES[n][1]+warningOffsets[n][1]+'px'});$('lightOffsets').textContent=warningOffsets.map((o,n)=>'L'+(n+1)+' '+(o[0]>=0?'+':'')+o[0]+','+(o[1]>=0?'+':'')+o[1]).join(' · ')}function scheduleWarning(n){clearTimeout(warningTimers[n]);const node=document.querySelectorAll('.warningLight')[n],tick=()=>{const family=FITTED.warnings[n],previous=Number(node.dataset.colour||-1);let next=Math.floor(Math.random()*family.length);if(next===previous)next=(next+1)%family.length;node.dataset.colour=next;node.src=ROOT+family[next]+V;node.style.opacity=Math.random()<.24?0:1;warningTimers[n]=setTimeout(tick,170+Math.floor(Math.random()*630))};tick()}")
page = replace(page,
  "function resetWarningPositions(){warningOffsets=[[0,0],[0,0],[0,0]];renderWarningPositions();$('status').textContent='Dishwasher lenses restored to V12 base positions.'}",
  "function resetWarningPositions(){warningOffsets=ACCEPTED_WARNING_OFFSETS.map(offset=>[...offset]);renderWarningPositions();$('status').textContent='Dishwasher lenses restored to accepted −5,−2 offsets.'}")
page = replace(page,
  "function reset(){model=defaults();warningOffsets=[[0,0],[0,0],[0,0]];bowlDepth=0;",
  "function reset(){model=defaults();warningOffsets=ACCEPTED_WARNING_OFFSETS.map(offset=>[...offset]);bowlDepth=0;")
page = replace(page,
  "document.querySelectorAll('.warningLight').forEach((i,n)=>{i.src=ROOT+FITTED.warnings[n]+V;i.dataset.warningIndex=n;i.onpointerdown=startWarningDrag});renderWarningPositions();",
  "document.querySelectorAll('.warningLight').forEach((i,n)=>{i.src=ROOT+FITTED.warnings[n][0]+V;i.dataset.warningIndex=n;i.onpointerdown=startWarningDrag;scheduleWarning(n)});renderWarningPositions();")
page = replace(page, "[...Object.values(FITTED).flat()].map", "[...Object.values(FITTED).flat(Infinity)].map")
page = page.replaceAll('Kitchen V12', 'Kitchen V13')
page = page.replaceAll('V12 unchanged loose bodies.', 'V13 corrected loose bodies.')
page = replace(page,
  "state==='broken'?'BROKEN: rear-shifted sink geyser; draggable dishwasher lenses; closed oven cavity flicker; sink, dishwasher and fridge spills remain floor-plane layers.'",
  "state==='broken'?'BROKEN: complete-base bowl; accepted multicolour dishwasher lenses; larger fine-froth dishwasher spill; tapered sink spill; closed oven cavity flicker.'")
page = replace(page,
  "'Ready: V12 closed-oven flicker and exact effect-position controls loaded.'",
  "'Ready: V13 complete-base bowl, accepted multicolour lights and organic spill corrections loaded.'")
page = replace(page, "'V12 starting layout restored.'", "'V13 starting layout restored.'")
page = replace(page,
  '<section class="panel"><h2>V11 predecessor ↔ V12 positioning correction</h2><p>The approved fitted base, loose-asset pixels, pace lattice, room grid and gameplay remain unchanged.</p><div class="comparison"><article><h3>Direct positioning</h3><p>Drag the three warning lenses independently in Broken state and report the exact offsets shown beneath the room. The broken bowl remains visibly unapproved; its contact-depth slider moves the unchanged pixels in exact native increments.</p></article><article><h3>Closed oven and sink depth</h3><p>The rejected open oven and fascia layers are gone. Broken now uses the approved closed oven with only its behind-glass cavity flickering. The unchanged V11 geyser is composed eight pixels farther back.</p></article></div></section>',
  '<section class="panel"><h2>V12 predecessor ↔ V13 asset corrections</h2><p>The approved fitted base, pace lattice, room grid and gameplay remain unchanged.</p><div class="comparison"><article><h3>Complete bowl and scoped movement</h3><p>The broken bowl is rebuilt from the complete standard body, retaining its full foot/base while removing a connected front-left section. Worktop dragging is mutation-scoped and cannot change table or chair anchors.</p></article><article><h3>Accepted lights and organic water</h3><p>All lenses start at the accepted −5,−2 offsets. Old arcs are removed; amber, cyan and violet states change at irregular random intervals. The dishwasher spill is larger and finely frothy, while the sink spill no longer ends in straight vertical cuts.</p></article></div></section>')
page = page.replaceAll('V12 inherits the approved fitted base byte-for-byte from V4; only separate review effects and positioning controls change from V11.', 'V13 inherits the approved fitted base byte-for-byte from V4; only separate broken-state assets, effects and review controls change from V12.')
page = page.replaceAll('Reject V12 by discarding only its page, route and V12 native correction directory. V1–V11 and live 84 × 74 gameplay remain unchanged.', 'Reject V13 by discarding only its page, route and V13 native correction directory. V1–V12 and live 84 × 74 gameplay remain unchanged.')
page = page.replaceAll('Dishwasher lamps remain independently positioned overlays; the oven uses one closed-cavity light-state replacement.', 'Dishwasher lamps remain independent accepted-offset overlays with irregular amber/cyan/violet changes; the oven uses one closed-cavity light-state replacement.')
page = page.replaceAll('L1 +0,+0 · L2 +0,+0 · L3 +0,+0', 'L1 -5,-2 · L2 -5,-2 · L3 -5,-2')
page = page.replaceAll('Use Broken bowl contact to move the unchanged draft body fore/aft without altering its pixels.', 'Use Broken bowl contact to verify its complete foot/base contact fore/aft without affecting table or chair anchors.')
fs.writeFileSync(path.join(PAGE_DIR, 'index.html'), page)

const record = {
  schema: 'lighthouse-keeper/kitchen-room-layout-review@13',
  version: 13,
  createdOn: '2026-10-25',
  status: 'review-only-awaiting-v13-bowl-light-and-water-review',
  reviewRoute: '/keeper-review/kitchen-room-layout-v13/',
  supersedesReview: '/keeper-review/kitchen-room-layout-v12/',
  authority: {
    document: 'docs/KITCHEN_ASSET_AUTHORITY.md',
    contract: 'data/kitchen_asset_contract_v1.json',
    roomGrid: 'data/kitchen_room_grid_contract_v2.json',
    lockedFittedBaseSha256: outputs['fitted-units-static'].sha256,
  },
  nativeAssets: {
    register: `${OUT}/extraction-register.json`,
    registerSha256: hash(`${OUT}/extraction-register.json`),
    predecessorRegister: V12_REGISTER,
    predecessorRegisterSha256: V12_REGISTER_SHA256,
    scaleAppliedToKitchenArt: false,
    downscalingApplied: false,
    resamplingApplied: false,
    approvedBaseColourTransformApplied: false,
    separateEffectColourTransformsApplied: true,
  },
  corrections: register.corrections,
  reviewCalibration: register.reviewCalibration,
  boundary: {
    runtimeChanged: false,
    gameplayChanged: false,
    approvedFittedUnitsChanged: false,
    roomGridChanged: false,
    rollback: 'Rejecting V13 discards only its route, page and V13 native correction directory. V1-V12, the V4 fitted-unit lock, Runtime Promotion V1 and retained 84 x 74 runtime room remain byte-identical.',
  },
}
fs.writeFileSync('data/kitchen_room_layout_review_v13.json', `${JSON.stringify(record, null, 2)}\n`)
fs.mkdirSync('art/drafts/kitchen-room-layout-review-2026-10-25-v13', { recursive: true })
fs.writeFileSync('art/drafts/kitchen-room-layout-review-2026-10-25-v13/HANDOFF.md', `# Kitchen Room Layout Review V13\n\nV13 is a reversible review-only correction derived from immutable V12.\n\n- The approved fitted base is byte-identical.\n- Broken bowl is rebuilt from the complete standard body and retains its full foot/base.\n- Worktop dragging is scoped and cannot mutate table/chair floor anchors.\n- Dishwasher warning lights start at Frank's accepted -5,-2 offsets. Old arcs are neutralised and isolated amber/cyan/violet lenses change at irregular random intervals.\n- Dishwasher-owned water is larger, translucent and finely frothy; it does not enter the oven interval.\n- Sink spill edges taper at native-pixel resolution rather than ending as straight vertical clips.\n- Runtime, gameplay and the exact 84 x 74 room grid are unchanged.\n\nReject V13 by discarding only this directory, its data record and its review route/page.\n`)

console.log(`Built Kitchen V13: ${Object.keys(outputs).length} outputs; complete-base bowl; accepted warning offsets ${JSON.stringify(acceptedWarningOffsets)}; multicolour lights; organic sink/dishwasher water.`)
