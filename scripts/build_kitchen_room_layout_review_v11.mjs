#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const V10_DIR = 'art/drafts/kitchen-room-layout-review-2026-10-25-v10/native-assets'
const OUT = 'art/drafts/kitchen-room-layout-review-2026-10-25-v11/native-assets'
const PUBLIC = 'public/keeper-review/kitchen-room-layout-v11/assets'
const PAGE_DIR = 'public/keeper-review/kitchen-room-layout-v11'
const V10_PAGE = 'public/keeper-review/kitchen-room-layout-v10/index.html'
const V10_REGISTER = `${V10_DIR}/extraction-register.json`
const V10_REGISTER_SHA256 = '421ff8176eddf1fc76a6a2c46a9a450d7bad55dc5f27898aed0f86d382568683'
const V7_WATER = 'art/drafts/kitchen-room-layout-review-2026-10-25-v7/native-assets/broken-floor-water-native.png'
const V7_WATER_SHA256 = '64c0a95c793a321fae60f54f9553f6470805ec93e68f86b676004554fbbb61f6'

const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => sha256(fs.readFileSync(file))
const offset = (png, x, y) => (y * png.width + x) * 4
const readPng = file => PNG.sync.read(fs.readFileSync(file))
const blank = (width, height) => new PNG({ width, height, colorType: 6 })
const copyPixel = (source, target, sx, sy, tx = sx, ty = sy) => {
  const from = offset(source, sx, sy), to = offset(target, tx, ty)
  target.data.set(source.data.subarray(from, from + 4), to)
}
const compositePixel = (base, overlay, x, y) => {
  const bi = offset(base, x, y), oi = offset(overlay, x, y), alpha = overlay.data[oi + 3] / 255
  return [
    Math.round(overlay.data[oi] * alpha + base.data[bi] * (1 - alpha)),
    Math.round(overlay.data[oi + 1] * alpha + base.data[bi + 1] * (1 - alpha)),
    Math.round(overlay.data[oi + 2] * alpha + base.data[bi + 2] * (1 - alpha)),
    Math.round((alpha + (base.data[bi + 3] / 255) * (1 - alpha)) * 255),
  ]
}

fs.mkdirSync(OUT, { recursive: true })
fs.mkdirSync(PUBLIC, { recursive: true })
fs.mkdirSync(PAGE_DIR, { recursive: true })
if (hash(V10_REGISTER) !== V10_REGISTER_SHA256) throw new Error('Kitchen V10 register changed')
if (hash(V7_WATER) !== V7_WATER_SHA256) throw new Error('Kitchen V7 full floor-water source changed')
const v10 = JSON.parse(fs.readFileSync(V10_REGISTER, 'utf8'))
const outputs = {}

for (const [id, source] of Object.entries(v10.outputs)) {
  const bytes = fs.readFileSync(source.file)
  if (sha256(bytes) !== source.sha256) throw new Error(`${id} V10 source changed`)
  const filename = `${id}-native.png`
  fs.writeFileSync(path.join(OUT, filename), bytes)
  fs.writeFileSync(path.join(PUBLIC, filename), bytes)
  outputs[id] = {
    ...source,
    file: `${OUT}/${filename}`,
    publicReviewFile: `${PUBLIC}/${filename}`,
    inheritedByteIdenticalFromV10: true,
  }
}

const writeOutput = (id, png, metadata) => {
  const filename = `${id}-native.png`, bytes = PNG.sync.write(png, { colorType: 6 })
  fs.writeFileSync(path.join(OUT, filename), bytes)
  fs.writeFileSync(path.join(PUBLIC, filename), bytes)
  outputs[id] = {
    ...(outputs[id] ?? {}),
    file: `${OUT}/${filename}`,
    publicReviewFile: `${PUBLIC}/${filename}`,
    dimensions: [png.width, png.height],
    sha256: sha256(bytes),
    inheritedByteIdenticalFromV10: false,
    ...metadata,
  }
}

// The intact shell ends at row 54. Rows 55-64 belong only to the hanging shard,
// which must overlap the fascia rather than lift the bowl off the worktop.
outputs['bowl-broken'] = {
  ...outputs['bowl-broken'],
  contactRow: 54,
  contactSurfaceRow: 54,
  deepestAlphaRow: 64,
  hangingShardRows: [55, 64],
  correction: 'intact shell row 54 is the declared worktop contact; the connected shard hangs ten pixels in front of the fascia',
}

// Restore only the sink, dishwasher and fridge spills on the separate walking
// plane. The oven interval stays fully transparent and the fitted-run box is
// never involved in water registration.
const sinkWater = readPng(v10.outputs['broken-floor-water'].file)
const fullWater = readPng(V7_WATER)
const floorWater = blank(sinkWater.width, sinkWater.height)
for (let y = 0; y < sinkWater.height; y += 1) for (let x = 0; x < sinkWater.width; x += 1) {
  if (sinkWater.data[offset(sinkWater, x, y) + 3]) copyPixel(sinkWater, floorWater, x, y)
}
for (const [minX, maxX] of [[700, 910], [1145, 1375]]) {
  for (let y = 16; y < fullWater.height; y += 1) for (let x = minX; x <= maxX; x += 1) {
    const i = offset(fullWater, x, y), r = fullWater.data[i], g = fullWater.data[i + 1], b = fullWater.data[i + 2], a = fullWater.data[i + 3]
    const waterPixel = a && ((g > 100 && b > 145 && b > r + 20) || (r > 175 && g > 185 && b > 185))
    if (waterPixel) copyPixel(fullWater, floorWater, x, y)
  }
}
writeOutput('broken-floor-water', floorWater, {
  source: V7_WATER,
  sourceSha256: V7_WATER_SHA256,
  predecessorSha256: v10.outputs['broken-floor-water'].sha256,
  supportPlane: 'walking-floor',
  spillIntervals: { sink: [360, 640], dishwasher: [700, 910], oven: null, fridge: [1145, 1375] },
  correction: 'separate floor-plane spills restored beneath sink, dishwasher and fridge; oven interval remains transparent',
})

// Escalate the broken sink into an intentionally exaggerated three-frame
// upward geyser. Existing native gush pixels are retained at their exact run
// coordinates; the added water uses a small palette sampled from those pixels
// and occupies a taller transparent effect canvas. No fitted asset is resized.
const WATER = {
  outline: [55, 135, 178, 245],
  body: [86, 195, 251, 235],
  light: [196, 242, 250, 255],
  white: [245, 253, 253, 255],
}
const paintDisc = (png, cx, cy, radius, rgba) => {
  for (let y = Math.floor(cy - radius); y <= Math.ceil(cy + radius); y += 1) for (let x = Math.floor(cx - radius); x <= Math.ceil(cx + radius); x += 1) {
    if (x < 0 || y < 0 || x >= png.width || y >= png.height || (x - cx) ** 2 + (y - cy) ** 2 > radius ** 2) continue
    const i = offset(png, x, y), sourceAlpha = rgba[3] / 255, targetAlpha = png.data[i + 3] / 255
    const outAlpha = sourceAlpha + targetAlpha * (1 - sourceAlpha)
    if (!outAlpha) continue
    for (let channel = 0; channel < 3; channel += 1) png.data[i + channel] = Math.round((rgba[channel] * sourceAlpha + png.data[i + channel] * targetAlpha * (1 - sourceAlpha)) / outAlpha)
    png.data[i + 3] = Math.round(outAlpha * 255)
  }
}
const strokeCurve = (png, points, radius, rgba) => {
  for (let index = 1; index < points.length; index += 1) {
    const [x0, y0] = points[index - 1], [x1, y1] = points[index], steps = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0)))
    for (let step = 0; step <= steps; step += 1) {
      const t = step / steps
      paintDisc(png, x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, radius, rgba)
    }
  }
}
for (let frame = 0; frame < 3; frame += 1) {
  const source = readPng(v10.outputs[`sink-broken-gush-${frame + 1}`].file)
  const geyser = blank(source.width, source.height + 160)
  for (let y = 0; y < source.height; y += 1) for (let x = 0; x < source.width; x += 1) {
    if (source.data[offset(source, x, y) + 3]) copyPixel(source, geyser, x, y, x, y + 160)
  }
  const baseX = 557 + [-4, 3, 0][frame], baseY = 258, topY = [25, 11, 34][frame]
  const main = []
  for (let y = baseY; y >= topY; y -= 3) {
    const progress = (baseY - y) / (baseY - topY)
    main.push([baseX + Math.sin(progress * 9 + frame * 1.7) * (3 + progress * 5), y])
  }
  strokeCurve(geyser, main, 11, WATER.outline)
  strokeCurve(geyser, main, 8, WATER.body)
  strokeCurve(geyser, main.map(([x, y]) => [x - 3, y]), 2.2, WATER.white)
  const arc = direction => {
    const points = []
    for (let step = 0; step <= 36; step += 1) {
      const t = step / 36
      points.push([baseX + direction * (14 + 132 * t), baseY - 205 * t + 130 * t * t + Math.sin(t * 8 + frame) * 3])
    }
    strokeCurve(geyser, points, 5.5, WATER.outline)
    strokeCurve(geyser, points, 3.5, WATER.body)
    strokeCurve(geyser, points.map(([x, y]) => [x - direction, y - 1]), 1.2, WATER.light)
  }
  arc(-1)
  arc(1)
  const droplets = [
    [-104, -151, 6], [-75, -194, 4], [-42, -222, 5], [36, -211, 4], [78, -181, 6], [119, -132, 5],
    [-132, -89, 4], [143, -74, 4], [-26, -238, 3], [22, -244, 3],
  ]
  for (const [dx, dy, radius] of droplets) {
    const x = baseX + dx + ((frame * 7 + dx) % 9), y = baseY + dy + ((frame * 5 + dy) % 7)
    paintDisc(geyser, x, y, radius, WATER.outline)
    paintDisc(geyser, x - 1, y - 1, Math.max(1, radius - 2), WATER.light)
  }
  writeOutput(`sink-broken-gush-${frame + 1}`, geyser, {
    predecessorSha256: v10.outputs[`sink-broken-gush-${frame + 1}`].sha256,
    runAlignmentOffsetY: 160,
    effectBounds: [410, 0, 300, 444],
    correction: 'OTT upward basin geyser on a taller transparent fault layer; original native tap gush retained at exact coordinates',
    animationFrame: frame + 1,
  })
}

// The lit oven state is a complete opaque replacement of the existing cavity
// pixels, not a translucent blob. The frame, racks and linework are copied from
// the composed V10 broken state; only neutral interior pixels receive a warm
// light-state tone. Hiding the layer reveals the exact dark V10 cavity.
const fittedBase = readPng(v10.outputs['fitted-units-static'].file)
const fittedBroken = readPng(v10.outputs['fitted-overlay-broken'].file)
const ovenLit = blank(fittedBase.width, fittedBase.height)
const cavity = [942, 171, 171, 81]
for (let y = cavity[1]; y < cavity[1] + cavity[3]; y += 1) for (let x = cavity[0]; x < cavity[0] + cavity[2]; x += 1) {
  const rgba = compositePixel(fittedBase, fittedBroken, x, y), i = offset(ovenLit, x, y)
  ovenLit.data.set(rgba, i)
}
for (let y = 178; y <= 235; y += 1) for (let x = 949; x <= 1106; x += 1) {
  const i = offset(ovenLit, x, y), r = ovenLit.data[i], g = ovenLit.data[i + 1], b = ovenLit.data[i + 2]
  const luminance = r * .2126 + g * .7152 + b * .0722
  const spread = Math.max(r, g, b) - Math.min(r, g, b)
  if (luminance < 30 || luminance > 125 || spread > 48) continue
  const upperGain = 1 + Math.max(0, 220 - y) / 260
  ovenLit.data[i] = Math.min(255, Math.round((luminance * 2.7 + 24) * upperGain))
  ovenLit.data[i + 1] = Math.min(205, Math.round((luminance * 1.18 + 18) * upperGain))
  ovenLit.data[i + 2] = Math.min(62, Math.round(luminance * .24 + 4))
}
writeOutput('oven-broken-cavity-light', ovenLit, {
  predecessorSha256: v10.outputs['oven-broken-cavity-light'].sha256,
  cavityBounds: cavity,
  correction: 'opaque lit-cavity state made from exact V10 cavity pixels; no translucent ellipse, food, tray, door, handle or fascia content',
  animation: 'irregular complete lit/dark cavity replacement in review shell',
})

// Pulse the existing red fascia lens independently without moving it.
const fascia = blank(fittedBase.width, fittedBase.height)
const fasciaBounds = [1092, 112, 20, 29]
for (let y = fasciaBounds[1]; y < fasciaBounds[1] + fasciaBounds[3]; y += 1) for (let x = fasciaBounds[0]; x < fasciaBounds[0] + fasciaBounds[2]; x += 1) {
  const rgba = compositePixel(fittedBase, fittedBroken, x, y), i = offset(fascia, x, y)
  fascia.data.set(rgba, i)
  if (rgba[0] > 100 && rgba[0] > rgba[1] * 1.45 && rgba[0] > rgba[2] * 1.45) {
    fascia.data[i] = 255
    fascia.data[i + 1] = Math.min(92, Math.round(rgba[1] * 1.35 + 18))
    fascia.data[i + 2] = Math.min(48, rgba[2] + 10)
  }
}
writeOutput('oven-broken-fascia-pulse', fascia, {
  source: 'composed V10 broken fitted run',
  fasciaBounds,
  correction: 'fixed red fascia lens brightens in place on an independent irregular pulse',
})

for (const keeperName of ['prime-keeper-neutral-native-256x320.png', 'prime-keeper-seated-back-native-256x320.png']) {
  const archive = JSON.parse(fs.readFileSync('review-archive/index.json', 'utf8'))
  const entry = archive.legacyPaths[`/keeper-review/kitchen-room-layout-v10/assets/${keeperName}`]
  if (!entry) throw new Error(`Missing archived V10 Keeper ${keeperName}`)
  fs.writeFileSync(path.join(PUBLIC, keeperName), fs.readFileSync(path.join('review-archive', entry.object.replace(/^review-archive\//, ''))))
}

const register = {
  ...v10,
  schema: 'lighthouse-keeper/kitchen-native-assets@11',
  status: 'review-only-unapproved-v11-broken-oven-bowl-contact-and-spills',
  predecessor: { register: V10_REGISTER, sha256: V10_REGISTER_SHA256 },
  corrections: {
    ...v10.corrections,
    bowl: 'intact shell row 54 is the explicit worktop contact; hanging shard rows 55-64 overlap the fascia',
    oven: 'actual opaque cavity-state replacement flickers; fascia lens pulses independently; no flat translucent overlay',
    sinkGush: 'three-frame OTT geyser shoots upward from the basin on a taller transparent effect layer',
    floorWater: 'separate spills beneath sink, dishwasher and fridge; no oven spill and no fitted-run registration',
  },
  outputs,
}
fs.writeFileSync(path.join(OUT, 'extraction-register.json'), `${JSON.stringify(register, null, 2)}\n`)

let page = fs.readFileSync(V10_PAGE, 'utf8')
page = page
  .replace('<title>Kitchen V10 · straight ON tap stream</title>', '<title>Kitchen V11 · broken oven, bowl contact and appliance spills</title>')
  .replace('<h1>Straight ON tap stream</h1>', '<h1>Broken oven, bowl contact and appliance spills</h1>')
  .replace('V9 remains immutable predecessor evidence. V10 changes only the ON sink-water alpha: water falls in one straight vertical line from the tap outlet, with no splash or pooling at its base. Every other V9 pixel and all behaviour remain byte-identical.', 'V10 remains immutable predecessor evidence. V11 replaces the flat oven glow with a true lit/dark cavity state and an independent fixed fascia pulse, registers the broken bowl on its intact shell rather than its hanging shard, restores separate dishwasher and fridge spills without assigning water to the oven, and gives the broken sink an intentionally OTT upward geyser.')
  .replaceAll('/keeper-review/kitchen-room-layout-v10/assets/', '/keeper-review/kitchen-room-layout-v11/assets/')
  .replace("const ROOT='/keeper-review/kitchen-room-layout-v11/assets/',V='?v=10';", "const ROOT='/keeper-review/kitchen-room-layout-v11/assets/',V='?v=11';")
  .replace('Review-only V10', 'Review-only V11')
  .replace('V10 corrected loose family · native source pixels', 'V11 corrected loose family · native source pixels')
  .replace('V10 inherits the approved fitted base byte-for-byte from V4; only the separate ON sink-water alpha mask changes from V9.', 'V11 inherits the approved fitted base byte-for-byte from V4; only separate fault/effect layers and the broken-bowl support datum change from V10.')
  .replace('Reject V10 by discarding only its page, route and V10 native correction directory. V1–V9 and live 84 × 74 gameplay remain unchanged.', 'Reject V11 by discarding only its page, route and V11 native correction directory. V1–V10 and live 84 × 74 gameplay remain unchanged.')
  .replace("broken:64},anchors:{standard:69,broken:65}", "broken:54},anchors:{standard:69,broken:65}")
  .replace("oven:'oven-broken-cavity-light-native.png',warnings", "oven:'oven-broken-cavity-light-native.png',ovenFascia:'oven-broken-fascia-pulse-native.png',warnings")
  .replace('<img id="ovenLight" class="ovenLight" hidden alt="Oven broken cavity light">', '<img id="ovenLight" class="ovenLight" hidden alt="Oven broken lit cavity state"><img id="ovenFascia" class="ovenFascia" hidden alt="Oven broken fascia pulse">')
  .replace('.camera.broken .ovenLight{animation:ovenBlink 2.3s steps(1,end) infinite}', '.camera.broken .ovenLight{animation:ovenBlink 2.3s steps(1,end) infinite}.camera.broken .ovenFascia{animation:ovenFasciaPulse 3.7s steps(1,end) infinite}')
  .replace('.camera.broken .g1{animation:gush1 .36s steps(1,end) infinite}.camera.broken .g2{animation:gush2 .36s steps(1,end) infinite}.camera.broken .g3{animation:gush3 .36s steps(1,end) infinite}', '.camera.broken .g1{animation:gush1 .27s steps(1,end) infinite}.camera.broken .g2{animation:gush2 .27s steps(1,end) infinite}.camera.broken .g3{animation:gush3 .27s steps(1,end) infinite}.run{overflow:visible}.run .sinkGush{top:-160px;height:444px}')
  .replace('@keyframes gush1{', '@keyframes ovenFasciaPulse{0%,11%,18%,56%,64%,91%,100%{opacity:0}12%,17%,57%,63%,92%,96%{opacity:1}}@keyframes gush1{')
  .replace("$('ovenLight').hidden=state!=='broken';", "$('ovenLight').hidden=state!=='broken';$('ovenFascia').hidden=state!=='broken';")
  .replace("$('ovenLight').src=ROOT+FITTED.oven+V;", "$('ovenLight').src=ROOT+FITTED.oven+V;$('ovenFascia').src=ROOT+FITTED.ovenFascia+V;")
  .replace("'BROKEN: fixed units plus independent damage/effect layers.'", "'BROKEN: OTT sink geyser; bowl shell registered to worktop; oven cavity and fascia animate independently; sink, dishwasher and fridge spills remain floor-plane layers.'")
  .replace("'OFF: locked fitted base and V10 corrected loose bodies.'", "'OFF: locked fitted base and V11 corrected loose bodies.'")
  .replace("'V10 starting layout restored.'", "'V11 starting layout restored.'")
  .replace("'Ready: V10 ON tap stream is straight with no pooling.'", "'Ready: V11 broken oven, bowl contact and appliance spills corrected.'")

const proof = `<section class="panel"><h2>V10 predecessor ↔ V11 Broken-state correction</h2><p>The fitted-unit base, V10 ON sink, loose-asset pixels, room geometry, pace lattice and gameplay remain unchanged. V11 changes only separate fault/effect layers and the broken bowl's declared support row.</p><div class="comparison"><article><h3>Broken bowl contact</h3><p>V10 used deepest alpha row 64, so the dangling shard lifted the shell. V11 declares shell row 54 as the worktop contact; rows 55–64 hang in front of the fascia.</p></article><article><h3>Broken oven, geyser and floor spills</h3><p>The oven now alternates between complete dark and lit cavity states while its fixed fascia lens pulses independently. A three-frame OTT geyser shoots upward from the basin. Floor water is separately registered beneath the sink, dishwasher and fridge, with no oven-owned spill.</p></article></div></section>`
page = page.replace(/<section class="panel"><h2>V9 predecessor ↔ V10 ON sink correction<\/h2>.*?<\/section>(?=<section class="panel"><h2>Scale registration<\/h2>)/s, proof)
page = page.replace(/const predecessorProofUrls=\[[^;]+;/, "const predecessorProofUrls=[];")
page = page.replaceAll('Kitchen V10', 'Kitchen V11')
fs.writeFileSync(path.join(PAGE_DIR, 'index.html'), page)

const record = {
  schema: 'lighthouse-keeper/kitchen-room-layout-review@11', version: 11, createdOn: '2026-10-25',
  status: 'review-only-awaiting-broken-state-review', reviewRoute: '/keeper-review/kitchen-room-layout-v11/', supersedesReview: '/keeper-review/kitchen-room-layout-v10/',
  authority: { document: 'docs/KITCHEN_ASSET_AUTHORITY.md', contract: 'data/kitchen_asset_contract_v1.json', roomGrid: 'data/kitchen_room_grid_contract_v2.json', lockedFittedBaseSha256: outputs['fitted-units-static'].sha256 },
  nativeAssets: { register: `${OUT}/extraction-register.json`, registerSha256: hash(`${OUT}/extraction-register.json`), predecessorRegister: V10_REGISTER, predecessorRegisterSha256: V10_REGISTER_SHA256, scaleAppliedToKitchenArt: false, downscalingApplied: false, resamplingApplied: false, approvedBaseColourTransformApplied: false, separateLightEffectToneMapApplied: true },
  corrections: register.corrections,
  boundary: { runtimeChanged: false, gameplayChanged: false, approvedFittedUnitsChanged: false, roomGridChanged: false, rollback: 'Rejecting V11 discards only its route, page and V11 native correction directory. V1-V10, the V4 fitted-unit lock, Runtime Promotion V1 and retained 84 x 74 runtime room remain byte-identical.' },
}
fs.writeFileSync('data/kitchen_room_layout_review_v11.json', `${JSON.stringify(record, null, 2)}\n`)
fs.mkdirSync('art/drafts/kitchen-room-layout-review-2026-10-25-v11', { recursive: true })
fs.writeFileSync('art/drafts/kitchen-room-layout-review-2026-10-25-v11/HANDOFF.md', '# Kitchen Room Layout Review V11\n\nV11 is a reversible review-only correction derived from immutable V10. The broken bowl uses intact shell row 54 as its worktop contact so the connected shard hangs in front of the fascia. The oven alternates between complete opaque dark/lit cavity states, with a separate fixed fascia-lens pulse. An exaggerated three-frame geyser shoots upward from the broken sink. Walking-plane spills are present beneath the sink, dishwasher and fridge only. The approved fitted base, V10 ON sink, exact pace grid, gameplay and runtime art remain unchanged.\n')
fs.writeFileSync('art/drafts/kitchen-room-layout-review-2026-10-25-v11/PROMPT_LOG.md', '# Kitchen V11 edit record\n\nThe final output uses deterministic 1:1 native-pixel edits to immutable V10 and the hash-pinned V7 floor-water source. No asset is AI-generated, scaled, resampled or substituted. The only tone mapping is confined to the separate oven lit-state effect; the approved fitted base remains byte-identical.\n')
console.log(`Built Kitchen V11 with ${Object.keys(outputs).length} native outputs.`)
