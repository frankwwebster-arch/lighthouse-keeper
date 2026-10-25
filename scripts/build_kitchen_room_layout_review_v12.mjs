#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const V11_DIR = 'art/drafts/kitchen-room-layout-review-2026-10-25-v11/native-assets'
const OUT = 'art/drafts/kitchen-room-layout-review-2026-10-25-v12/native-assets'
const PUBLIC = 'public/keeper-review/kitchen-room-layout-v12/assets'
const PAGE_DIR = 'public/keeper-review/kitchen-room-layout-v12'
const V11_PAGE = 'public/keeper-review/kitchen-room-layout-v11/index.html'
const V11_REGISTER = `${V11_DIR}/extraction-register.json`
const V11_REGISTER_SHA256 = 'ff79b7db93ae3ddceaaadc35b2a731656b2cb7f78f5bd8b2ccdca6550a93b26c'

const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => sha256(fs.readFileSync(file))
const offset = (png, x, y) => (y * png.width + x) * 4
const readPng = file => PNG.sync.read(fs.readFileSync(file))
const blank = (width, height) => new PNG({ width, height, colorType: 6 })
const replace = (text, before, after) => {
  if (!text.includes(before)) throw new Error(`V11 page transform target missing: ${before.slice(0, 100)}`)
  return text.replace(before, after)
}

fs.mkdirSync(OUT, { recursive: true })
fs.mkdirSync(PUBLIC, { recursive: true })
fs.mkdirSync(PAGE_DIR, { recursive: true })
if (hash(V11_REGISTER) !== V11_REGISTER_SHA256) throw new Error('Kitchen V11 register changed')
const v11 = JSON.parse(fs.readFileSync(V11_REGISTER, 'utf8'))
const outputs = {}

// V12 is a separate, discardable draft. Copy every V11 output except the
// rejected oven fascia pulse; changed outputs are then replaced below.
for (const [id, source] of Object.entries(v11.outputs)) {
  if (id === 'oven-broken-fascia-pulse') continue
  const bytes = fs.readFileSync(source.file)
  if (sha256(bytes) !== source.sha256) throw new Error(`${id} V11 source changed`)
  const filename = `${id}-native.png`
  fs.writeFileSync(path.join(OUT, filename), bytes)
  fs.writeFileSync(path.join(PUBLIC, filename), bytes)
  outputs[id] = {
    ...source,
    file: `${OUT}/${filename}`,
    publicReviewFile: `${PUBLIC}/${filename}`,
    inheritedByteIdenticalFromV11: true,
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
    inheritedByteIdenticalFromV11: false,
    ...metadata,
  }
}

// Remove only the rejected open-oven fault overlay. The approved locked base
// underneath therefore supplies the complete closed oven in Broken state.
const fittedBroken = readPng(v11.outputs['fitted-overlay-broken'].file)
const ovenModuleBounds = [915, 110, 220, 160]
for (let y = ovenModuleBounds[1]; y < ovenModuleBounds[1] + ovenModuleBounds[3]; y += 1) {
  for (let x = ovenModuleBounds[0]; x < ovenModuleBounds[0] + ovenModuleBounds[2]; x += 1) {
    fittedBroken.data.fill(0, offset(fittedBroken, x, y), offset(fittedBroken, x, y) + 4)
  }
}
writeOutput('fitted-overlay-broken', fittedBroken, {
  predecessorSha256: v11.outputs['fitted-overlay-broken'].sha256,
  ovenModuleBounds,
  correction: 'rejected open-oven fault pixels removed; approved closed oven remains visible from the locked fitted base',
})

// Build one exact closed-cavity replacement from the approved base. It covers
// only the glass/cavity rectangle, preserving the closed door and all fascia.
const fittedBase = readPng(v11.outputs['fitted-units-static'].file)
const ovenLit = blank(fittedBase.width, fittedBase.height)
const cavityBounds = [942, 171, 171, 81]
for (let y = cavityBounds[1]; y < cavityBounds[1] + cavityBounds[3]; y += 1) {
  for (let x = cavityBounds[0]; x < cavityBounds[0] + cavityBounds[2]; x += 1) {
    const source = offset(fittedBase, x, y)
    const target = offset(ovenLit, x, y)
    ovenLit.data.set(fittedBase.data.subarray(source, source + 4), target)
  }
}
for (let y = 178; y <= 235; y += 1) for (let x = 949; x <= 1106; x += 1) {
  const i = offset(ovenLit, x, y)
  const r = ovenLit.data[i], g = ovenLit.data[i + 1], b = ovenLit.data[i + 2]
  const luminance = r * .2126 + g * .7152 + b * .0722
  const spread = Math.max(r, g, b) - Math.min(r, g, b)
  if (luminance < 30 || luminance > 125 || spread > 48) continue
  const upperGain = 1 + Math.max(0, 220 - y) / 260
  ovenLit.data[i] = Math.min(255, Math.round((luminance * 2.7 + 24) * upperGain))
  ovenLit.data[i + 1] = Math.min(205, Math.round((luminance * 1.18 + 18) * upperGain))
  ovenLit.data[i + 2] = Math.min(62, Math.round(luminance * .24 + 4))
}
writeOutput('oven-broken-cavity-light', ovenLit, {
  predecessorSha256: v11.outputs['oven-broken-cavity-light'].sha256,
  cavityBounds,
  source: 'approved closed fitted-unit base',
  recomposedFromApprovedClosedBase: true,
  inheritedByteIdenticalFromV11: true,
  correction: 'closed oven flicker is confined behind the existing door glass; no open-door or fascia overlay remains',
  animation: 'irregular complete closed-cavity lit/dark replacement in review shell',
})

// Crop each dishwasher warning lens to an isolated draggable image. Four
// transparent pixels remain around every opaque edge, including frame edges.
const warningBases = []
for (let number = 1; number <= 3; number += 1) {
  const id = `dishwasher-warning-${number}`
  const source = readPng(v11.outputs[id].file)
  let minX = source.width, minY = source.height, maxX = -1, maxY = -1
  for (let y = 0; y < source.height; y += 1) for (let x = 0; x < source.width; x += 1) {
    if (!source.data[offset(source, x, y) + 3]) continue
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  const gutter = 4
  const cropX = minX - gutter, cropY = minY - gutter
  const crop = blank(maxX - minX + 1 + gutter * 2, maxY - minY + 1 + gutter * 2)
  for (let y = minY; y <= maxY; y += 1) for (let x = minX; x <= maxX; x += 1) {
    const from = offset(source, x, y), to = offset(crop, x - cropX, y - cropY)
    crop.data.set(source.data.subarray(from, from + 4), to)
  }
  warningBases.push([cropX, cropY])
  writeOutput(id, crop, {
    predecessorSha256: v11.outputs[id].sha256,
    sourceOpaqueBounds: [minX, minY, maxX - minX + 1, maxY - minY + 1],
    basePosition: [cropX, cropY],
    transparentSafetyGutter: gutter,
    correction: 'isolated tight warning-lens layer for exact native-pixel review positioning',
  })
}

for (const keeperName of ['prime-keeper-neutral-native-256x320.png', 'prime-keeper-seated-back-native-256x320.png']) {
  const archive = JSON.parse(fs.readFileSync('review-archive/index.json', 'utf8'))
  const entry = archive.legacyPaths[`/keeper-review/kitchen-room-layout-v11/assets/${keeperName}`]
  if (!entry) throw new Error(`Missing archived V11 Keeper ${keeperName}`)
  fs.writeFileSync(path.join(PUBLIC, keeperName), fs.readFileSync(path.join('review-archive', entry.object.replace(/^review-archive\//, ''))))
}

const register = {
  ...v11,
  schema: 'lighthouse-keeper/kitchen-native-assets@12',
  status: 'review-only-unapproved-v12-closed-oven-and-position-calibration',
  predecessor: { register: V11_REGISTER, sha256: V11_REGISTER_SHA256 },
  corrections: {
    ...v11.corrections,
    sinkGush: 'unchanged native V11 geyser pixels translated eight native pixels rearward in the review composition',
    bowl: 'V11 broken-bowl pixels remain unapproved and byte-identical; review exposes an exact native-pixel contact-depth control',
    dishwasher: 'three isolated warning lenses can be dragged independently and report exact native-pixel offsets',
    oven: 'Broken retains the approved closed oven; only the exact cavity behind its glass flickers, with no fascia or open-door overlay',
  },
  reviewCalibration: {
    sinkEffectOffsetY: -8,
    dishwasherWarningBasePositions: warningBases,
    dishwasherWarningInitialOffsets: [[0, 0], [0, 0], [0, 0]],
    brokenBowlInitialContactOffsetY: 0,
  },
  outputs,
}
fs.writeFileSync(path.join(OUT, 'extraction-register.json'), `${JSON.stringify(register, null, 2)}\n`)

let page = fs.readFileSync(V11_PAGE, 'utf8')
page = replace(page, '<title>Kitchen V11 · broken oven, bowl contact and appliance spills</title>', '<title>Kitchen V12 · closed oven flicker and exact effect positioning</title>')
page = replace(page, '<h1>Broken oven, bowl contact and appliance spills</h1>', '<h1>Closed oven flicker and exact effect positioning</h1>')
page = replace(page,
  '<p class="lede">V10 remains immutable predecessor evidence. V11 replaces the flat oven glow with a true lit/dark cavity state and an independent fixed fascia pulse, registers the broken bowl on its intact shell rather than its hanging shard, restores separate dishwasher and fridge spills without assigning water to the oven, and gives the broken sink an intentionally OTT upward geyser.</p>',
  '<p class="lede">V11 remains immutable predecessor evidence. V12 shifts the unchanged sink geyser eight native pixels behind the basin front, keeps the Broken oven closed while its interior flickers behind the existing glass, removes the rejected fascia overlay, and exposes exact native-pixel calibration for the dishwasher lenses and broken-bowl contact.</p>')
page = page.replaceAll('/keeper-review/kitchen-room-layout-v11/assets/', '/keeper-review/kitchen-room-layout-v12/assets/')
page = replace(page, "const ROOT='/keeper-review/kitchen-room-layout-v12/assets/',V='?v=11';", "const ROOT='/keeper-review/kitchen-room-layout-v12/assets/',V='?v=12';")
page = page.replaceAll('Review-only V11', 'Review-only V12')
page = page.replaceAll('V11 corrected loose family', 'V12 calibration family')
page = replace(page,
  '<button id="reset" class="primary" disabled>Reset layout</button>',
  '<button id="reset" class="primary" disabled>Reset layout</button><button id="resetLights" disabled>Reset dishwasher lights</button><button id="copyOffsets" disabled>Copy light offsets</button>')
page = replace(page,
  '<label><input id="showSeat" type="checkbox" checked disabled> Rear-seat proof</label>',
  '<label><input id="showSeat" type="checkbox" checked disabled> Rear-seat proof</label><label>Broken bowl contact <input id="bowlDepth" type="range" min="-18" max="18" step="1" value="0" disabled> <output id="bowlDepthValue">0 px</output></label>')
page = replace(page,
  '<p class="key"><strong>Movement:</strong> drag loose assets. Destinations stay on the 114-source-pixel pace lattice. Camera zoom applies to the composed room. Prime’s approved 256 × 320 source cell is displayed at 347.43 × 434.29 kitchen pixels so both art families describe the same world scale.</p>',
  '<p class="key"><strong>Movement:</strong> drag loose assets. In Broken state, drag each dishwasher lens directly; offsets are rounded to exact native pixels and shown below. Use Broken bowl contact to move the unchanged draft body fore/aft without altering its pixels. Destinations stay on the 114-source-pixel pace lattice.</p>')
page = replace(page,
  '<img id="ovenLight" class="ovenLight" hidden alt="Oven broken lit cavity state"><img id="ovenFascia" class="ovenFascia" hidden alt="Oven broken fascia pulse">',
  '<img id="ovenLight" class="ovenLight" hidden alt="Closed oven interior flicker behind existing glass">')
page = replace(page,
  '<div class="readout"><span id="status">Waiting for native assets.</span><code id="layout"></code></div>',
  '<div class="readout"><span id="status">Waiting for native assets.</span><code id="layout"></code><span>Dishwasher lens offsets</span><code id="lightOffsets">L1 +0,+0 · L2 +0,+0 · L3 +0,+0</code></div>')
page = replace(page,
  '.camera.broken .ovenLight{animation:ovenBlink 2.3s steps(1,end) infinite}.camera.broken .ovenFascia{animation:ovenFasciaPulse 3.7s steps(1,end) infinite}',
  '.camera.broken .ovenLight{animation:ovenBlink 2.3s steps(1,end) infinite}')
page = replace(page,
  '.run .sinkGush{top:-160px;height:444px}',
  '.run .sinkGush{top:-168px;height:444px}.run img{pointer-events:none}.run .warningLight{inset:auto;width:auto;height:auto;max-width:none;pointer-events:auto;cursor:grab;touch-action:none}.run .warningLight:active{cursor:grabbing}')
page = replace(page,
  '@keyframes ovenFasciaPulse{0%,11%,18%,56%,64%,91%,100%{opacity:0}12%,17%,57%,63%,92%,96%{opacity:1}}',
  '')
page = replace(page,
  "const FITTED={base:'fitted-units-static-native.png',on:'fitted-overlay-on-native.png',broken:'fitted-overlay-broken-native.png',water:'broken-floor-water-native.png',oven:'oven-broken-cavity-light-native.png',ovenFascia:'oven-broken-fascia-pulse-native.png',warnings:",
  "const FITTED={base:'fitted-units-static-native.png',on:'fitted-overlay-on-native.png',broken:'fitted-overlay-broken-native.png',water:'broken-floor-water-native.png',oven:'oven-broken-cavity-light-native.png',warnings:")
page = replace(page,
  'let model=defaults(),ready=false,drag=null;const $=id=>document.getElementById(id),url=name=>ROOT+ASSETS[name].files[model.state[name]]+V;',
  `const WARNING_BASES=${JSON.stringify(warningBases)};let model=defaults(),ready=false,drag=null,warningDrag=null,warningOffsets=[[0,0],[0,0],[0,0]],bowlDepth=0;const $=id=>document.getElementById(id),url=name=>ROOT+ASSETS[name].files[model.state[name]]+V;`)
page = replace(page,
  "function supportFor(name){return ASSETS[name].kind==='floor'?(name==='chair'?FLOOR_Y+24:FLOOR_Y):WORKTOP_Y}",
  "function supportFor(name){return ASSETS[name].kind==='floor'?(name==='chair'?FLOOR_Y+24:FLOOR_Y):WORKTOP_Y+(name==='bowl'&&model.state.bowl==='broken'?bowlDepth:0)}")
page = replace(page,
  "function renderLayout(){$('layout').textContent='anchors · '+Object.keys(ASSETS).map(n=>n+':'+centreFor(n)/PACE+'p').join(' · ')}",
  "function renderLayout(){$('layout').textContent='anchors · '+Object.keys(ASSETS).map(n=>n+':'+centreFor(n)/PACE+'p').join(' · ');$('bowlDepthValue').textContent=(bowlDepth>0?'+':'')+bowlDepth+' px'}")
page = replace(page,
  "function setCameraZoom(){const z=Number($('zoom').value);",
  "function renderWarningPositions(){document.querySelectorAll('.warningLight').forEach((node,n)=>{node.style.left=WARNING_BASES[n][0]+warningOffsets[n][0]+'px';node.style.top=WARNING_BASES[n][1]+warningOffsets[n][1]+'px'});$('lightOffsets').textContent=warningOffsets.map((o,n)=>'L'+(n+1)+' '+(o[0]>=0?'+':'')+o[0]+','+(o[1]>=0?'+':'')+o[1]).join(' · ')}function startWarningDrag(e){if(!ready||$('runState').value!=='broken')return;const n=Number(e.currentTarget.dataset.warningIndex),scale=$('camera').getBoundingClientRect().width/STAGE_W;warningDrag={node:e.currentTarget,n,x:e.clientX,y:e.clientY,ox:warningOffsets[n][0],oy:warningOffsets[n][1],scale};e.currentTarget.setPointerCapture(e.pointerId);e.currentTarget.onpointermove=moveWarningDrag;e.currentTarget.onpointerup=endWarningDrag;e.currentTarget.onpointercancel=endWarningDrag;e.preventDefault()}function moveWarningDrag(e){if(!warningDrag)return;warningOffsets[warningDrag.n]=[Math.round(warningDrag.ox+(e.clientX-warningDrag.x)/warningDrag.scale),Math.round(warningDrag.oy+(e.clientY-warningDrag.y)/warningDrag.scale)];renderWarningPositions()}function endWarningDrag(){if(!warningDrag)return;warningDrag.node.onpointermove=warningDrag.node.onpointerup=warningDrag.node.onpointercancel=null;$('status').textContent='Dishwasher lens '+(warningDrag.n+1)+' placed at exact native offset '+warningOffsets[warningDrag.n].join(',')+'.';warningDrag=null}function resetWarningPositions(){warningOffsets=[[0,0],[0,0],[0,0]];renderWarningPositions();$('status').textContent='Dishwasher lenses restored to V12 base positions.'}function setCameraZoom(){const z=Number($('zoom').value);")
page = replace(page, "$('ovenLight').hidden=state!=='broken';$('ovenFascia').hidden=state!=='broken';", "$('ovenLight').hidden=state!=='broken';")
page = replace(page,
  "state==='broken'?'BROKEN: OTT sink geyser; bowl shell registered to worktop; oven cavity and fascia animate independently; sink, dishwasher and fridge spills remain floor-plane layers.'",
  "state==='broken'?'BROKEN: rear-shifted sink geyser; draggable dishwasher lenses; closed oven cavity flicker; sink, dishwasher and fridge spills remain floor-plane layers.'")
page = replace(page,
  "function reset(){model=defaults();$('runState').value='off';setGlobalState('off');$('status').textContent='V11 starting layout restored.'}",
  "function reset(){model=defaults();warningOffsets=[[0,0],[0,0],[0,0]];bowlDepth=0;$('bowlDepth').value='0';$('runState').value='off';setGlobalState('off');renderWarningPositions();$('status').textContent='V12 starting layout restored.'}")
page = replace(page,
  "$('ovenLight').src=ROOT+FITTED.oven+V;$('ovenFascia').src=ROOT+FITTED.ovenFascia+V;document.querySelectorAll('.warningLight').forEach((i,n)=>i.src=ROOT+FITTED.warnings[n]+V);",
  "$('ovenLight').src=ROOT+FITTED.oven+V;document.querySelectorAll('.warningLight').forEach((i,n)=>{i.src=ROOT+FITTED.warnings[n]+V;i.dataset.warningIndex=n;i.onpointerdown=startWarningDrag});renderWarningPositions();")
page = replace(page,
  "'Ready: V11 broken oven, bowl contact and appliance spills corrected.'",
  "'Ready: V12 closed-oven flicker and exact effect-position controls loaded.'")
page = replace(page,
  "$('reset').onclick=reset;$('runState').onchange=()=>setGlobalState($('runState').value);",
  "$('reset').onclick=reset;$('resetLights').onclick=resetWarningPositions;$('copyOffsets').onclick=async()=>{const text=$('lightOffsets').textContent;try{await navigator.clipboard.writeText(text);$('status').textContent='Dishwasher offsets copied: '+text}catch{$('status').textContent='Dishwasher offsets: '+text}};$('bowlDepth').oninput=()=>{bowlDepth=Number($('bowlDepth').value);renderRoom();$('status').textContent='Broken bowl contact moved '+(bowlDepth>0?'+':'')+bowlDepth+' native px.'};$('runState').onchange=()=>setGlobalState($('runState').value);")
page = page.replaceAll('Kitchen V11', 'Kitchen V12')
page = replace(page,
  '<section class="panel"><h2>V10 predecessor ↔ V11 Broken-state correction</h2><p>The fitted-unit base, V10 ON sink, loose-asset pixels, room geometry, pace lattice and gameplay remain unchanged. V11 changes only separate fault/effect layers and the broken bowl\'s declared support row.</p><div class="comparison"><article><h3>Broken bowl contact</h3><p>V10 used deepest alpha row 64, so the dangling shard lifted the shell. V11 declares shell row 54 as the worktop contact; rows 55–64 hang in front of the fascia.</p></article><article><h3>Broken oven, geyser and floor spills</h3><p>The oven now alternates between complete dark and lit cavity states while its fixed fascia lens pulses independently. A three-frame OTT geyser shoots upward from the basin. Floor water is separately registered beneath the sink, dishwasher and fridge, with no oven-owned spill.</p></article></div></section>',
  '<section class="panel"><h2>V11 predecessor ↔ V12 positioning correction</h2><p>The approved fitted base, loose-asset pixels, pace lattice, room grid and gameplay remain unchanged.</p><div class="comparison"><article><h3>Direct positioning</h3><p>Drag the three warning lenses independently in Broken state and report the exact offsets shown beneath the room. The broken bowl remains visibly unapproved; its contact-depth slider moves the unchanged pixels in exact native increments.</p></article><article><h3>Closed oven and sink depth</h3><p>The rejected open oven and fascia layers are gone. Broken now uses the approved closed oven with only its behind-glass cavity flickering. The unchanged V11 geyser is composed eight pixels farther back.</p></article></div></section>')
page = page.replaceAll('V11 inherits the approved fitted base byte-for-byte from V4; only separate fault/effect layers and the broken-bowl support datum change from V10.', 'V12 inherits the approved fitted base byte-for-byte from V4; only separate review effects and positioning controls change from V11.')
page = page.replaceAll('Reject V11 by discarding only its page, route and V11 native correction directory. V1–V10 and live 84 × 74 gameplay remain unchanged.', 'Reject V12 by discarding only its page, route and V12 native correction directory. V1–V11 and live 84 × 74 gameplay remain unchanged.')
page = page.replaceAll('Dishwasher lamps and oven cavity light remain independent overlays.', 'Dishwasher lamps remain independently positioned overlays; the oven uses one closed-cavity light-state replacement.')
page = page.replaceAll('V11 corrected loose bodies.', 'V12 unchanged loose bodies.')
if (page.includes('ovenFascia') || page.includes('fascia pulse')) throw new Error('Rejected oven fascia survived V12 page transform')
fs.writeFileSync(path.join(PAGE_DIR, 'index.html'), page)

const record = {
  schema: 'lighthouse-keeper/kitchen-room-layout-review@12',
  version: 12,
  createdOn: '2026-10-25',
  status: 'review-only-awaiting-position-calibration-and-bowl-redraft-direction',
  reviewRoute: '/keeper-review/kitchen-room-layout-v12/',
  supersedesReview: '/keeper-review/kitchen-room-layout-v11/',
  authority: {
    document: 'docs/KITCHEN_ASSET_AUTHORITY.md',
    contract: 'data/kitchen_asset_contract_v1.json',
    roomGrid: 'data/kitchen_room_grid_contract_v2.json',
    lockedFittedBaseSha256: outputs['fitted-units-static'].sha256,
  },
  nativeAssets: {
    register: `${OUT}/extraction-register.json`,
    registerSha256: hash(`${OUT}/extraction-register.json`),
    predecessorRegister: V11_REGISTER,
    predecessorRegisterSha256: V11_REGISTER_SHA256,
    scaleAppliedToKitchenArt: false,
    downscalingApplied: false,
    resamplingApplied: false,
    approvedBaseColourTransformApplied: false,
    separateLightEffectToneMapApplied: true,
  },
  corrections: register.corrections,
  reviewCalibration: register.reviewCalibration,
  boundary: {
    runtimeChanged: false,
    gameplayChanged: false,
    approvedFittedUnitsChanged: false,
    roomGridChanged: false,
    rollback: 'Rejecting V12 discards only its route, page and V12 native correction directory. V1-V11, the V4 fitted-unit lock, Runtime Promotion V1 and retained 84 x 74 runtime room remain byte-identical.',
  },
}
fs.writeFileSync('data/kitchen_room_layout_review_v12.json', `${JSON.stringify(record, null, 2)}\n`)
fs.mkdirSync('art/drafts/kitchen-room-layout-review-2026-10-25-v12', { recursive: true })
fs.writeFileSync('art/drafts/kitchen-room-layout-review-2026-10-25-v12/HANDOFF.md', `# Kitchen Room Layout Review V12\n\nV12 is a reversible review-only correction derived from immutable V11.\n\n- The approved fitted base is byte-identical.\n- Broken keeps the approved closed oven and flickers only the cavity behind its glass.\n- The rejected open-door and fascia layers are absent.\n- The V11 geyser pixels are unchanged and composed eight native pixels farther back.\n- Dishwasher lenses are isolated four-gutter crops with exact native-pixel drag readouts.\n- The broken bowl pixels remain unapproved and unchanged; a contact-depth control is supplied for diagnosis.\n- Runtime, gameplay and the exact 84 × 74 room grid are unchanged.\n\nReject V12 by discarding only this directory, its data record and its review route/page.\n`)

console.log(`Built Kitchen V12: ${Object.keys(outputs).length} native outputs; warning bases ${JSON.stringify(warningBases)}; closed oven flicker; sink offset -8 px.`)
