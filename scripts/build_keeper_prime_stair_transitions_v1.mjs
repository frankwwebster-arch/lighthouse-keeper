#!/usr/bin/env node
/** Build the first exact Keeper Prime door/walk/stair transition review. */
import crypto from 'node:crypto'
import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-stair-transitions-v1'
const pack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-15-v1')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const stairPack = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16')
const walkPack = path.join(root, 'art/drafts/keeper-prime-walk-2026-10-14-v6')
const turnPack = path.join(root, 'art/drafts/keeper-prime-turn-front-side-2026-10-13-v1')
const bridgePack = path.join(root, 'art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1')
const stairRigPath = path.join(stairPack, 'stair-contact-rig-v16.json')
const stairRegisterPath = path.join(stairPack, 'batch-register.json')
const stairApprovalPath = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v17/batch-register.json')
const walkApprovalPath = path.join(root, 'art/drafts/keeper-prime-walk-2026-10-14-v7/batch-register.json')
const stopWalkApprovalPath = path.join(root, 'art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v2/batch-register.json')
const turnRegisterPath = path.join(turnPack, 'batch-register.json')
const sideBackApprovalPath = path.join(root, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json')
const timingApprovalPath = path.join(root, 'art/drafts/keeper-fast-transition-timing-2026-10-14-v1/approval-register.json')
const reachSources = {
  partial: path.join(pack, 'sources/generated/keeper-prime-door-reach-right-partial-generated.png'),
  full: path.join(pack, 'sources/generated/keeper-prime-door-reach-right-full-generated.png'),
}
const reachFrames = {
  partial: path.join(pack, 'drafts/frames/keeper_prime_door-reach-right_partial.png'),
  full: path.join(pack, 'drafts/frames/keeper_prime_door-reach-right_full.png'),
}
const reachRegistered = {
  partial: path.join(pack, 'drafts/registered/keeper_prime_door-reach-right_partial-registered.png'),
  full: path.join(pack, 'drafts/registered/keeper_prime_door-reach-right_full-registered.png'),
}
const reachMaskPath = path.join(pack, 'drafts/masks/keeper_prime_door-reach-right_arm-mask.png')
const rejectedStudyPaths = [
  path.join(pack, 'sources/rejected/keeper-prime-top-landing-pass-too-wide.png'),
  path.join(pack, 'sources/rejected/keeper-prime-top-landing-pass-rejected-three-arms.png'),
]
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

for (const file of [stairRigPath, stairRegisterPath, stairApprovalPath, walkApprovalPath, stopWalkApprovalPath, turnRegisterPath, sideBackApprovalPath, timingApprovalPath, ...Object.values(reachSources), ...rejectedStudyPaths, path.join(pack, 'HANDOFF.md'), path.join(pack, 'PROMPT_LOG.md')]) {
  if (!fs.existsSync(file)) throw new Error(`missing ${rel(file)}`)
}

const stairRig = JSON.parse(fs.readFileSync(stairRigPath, 'utf8'))
const stairRegister = JSON.parse(fs.readFileSync(stairRegisterPath, 'utf8'))
const turnRegister = JSON.parse(fs.readFileSync(turnRegisterPath, 'utf8'))
const sideBackApproval = JSON.parse(fs.readFileSync(sideBackApprovalPath, 'utf8'))
const timing = JSON.parse(fs.readFileSync(timingApprovalPath, 'utf8')).approval.profile
const geometry = stairRig.geometry
if (geometry.risers !== 14 || geometry.treadRunLp !== 7 || geometry.flightRunLp !== 98 || geometry.flightRiseLp !== 60) throw new Error('approved V16 stair geometry changed')

fs.rmSync(publicDir, { recursive: true, force: true })
fs.mkdirSync(assetsDir, { recursive: true })
fs.mkdirSync(path.dirname(reachFrames.partial), { recursive: true })
fs.mkdirSync(path.dirname(reachRegistered.partial), { recursive: true })
fs.mkdirSync(path.dirname(reachMaskPath), { recursive: true })

function normalizeReach(source, target, filter) {
  execFileSync('ffmpeg', ['-loglevel', 'error', '-y', '-i', source, '-vf', filter, '-frames:v', '1', '-pix_fmt', 'rgba', target])
}
normalizeReach(reachSources.partial, reachRegistered.partial, 'scale=279:349:flags=lanczos,crop=256:320:6:9')
normalizeReach(reachSources.full, reachRegistered.full, 'scale=280:350:flags=lanczos,crop=256:320:3:10')
const sideNeutralPath = path.join(root, sideBackApproval.approvedCandidate.frames[0].file)
const reachPolygon = [[96, 108], [120, 108], [151, 139], [251, 139], [251, 201], [157, 204], [146, 236], [96, 236]]
function insidePolygon(x, y, polygon) {
  let inside = false
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const [xi, yi] = polygon[i], [xj, yj] = polygon[j]
    if (((yi > y) !== (yj > y)) && (x < ((xj - xi) * (y - yi) / (yj - yi)) + xi)) inside = !inside
  }
  return inside
}
function compositeReach(registeredPath, targetPath) {
  const base = PNG.sync.read(fs.readFileSync(sideNeutralPath))
  const registered = PNG.sync.read(fs.readFileSync(registeredPath))
  const mask = new PNG({ width: 256, height: 320 })
  for (let y = 0; y < 320; y++) for (let x = 0; x < 256; x++) {
    const offset = (y * 256 + x) * 4
    const selected = insidePolygon(x + 0.5, y + 0.5, reachPolygon)
    if (selected) registered.data.copy(base.data, offset, offset, offset + 4)
    mask.data[offset] = mask.data[offset + 1] = mask.data[offset + 2] = selected ? 255 : 0
    mask.data[offset + 3] = 255
  }
  fs.writeFileSync(targetPath, PNG.sync.write(base))
  return mask
}
const reachMask = compositeReach(reachRegistered.partial, reachFrames.partial)
compositeReach(reachRegistered.full, reachFrames.full)
fs.writeFileSync(reachMaskPath, PNG.sync.write(reachMask))

const publishedByHash = new Map()
const published = []
function publish(file) {
  const digest = sha(file)
  if (publishedByHash.has(digest)) return publishedByHash.get(digest)
  const target = path.join(assetsDir, `frame-${digest.slice(0, 16)}.png`)
  fs.copyFileSync(file, target)
  const record = { source: rel(file), sourceSha256: digest, url: `/keeper-review/${set}/assets/${path.basename(target)}` }
  publishedByHash.set(digest, record)
  published.push(record)
  return record
}

const walkFiles = Array.from({ length: 8 }, (_, index) => path.join(walkPack, `drafts/frames/keeper_prime_walk-right_f${index + 1}.png`))
const walk = walkFiles.map(publish)
const sideBackFiles = sideBackApproval.approvedCandidate.frames.map((frame) => path.join(root, frame.file))
const sideBack = sideBackFiles.map(publish)
const bridgeFiles = Array.from({ length: 5 }, (_, index) => path.join(bridgePack, `drafts/frames/keeper_prime_stop-to-walk-right_f${index + 1}.png`))
const bridge = bridgeFiles.map(publish)
const reach = { partial: publish(reachFrames.partial), full: publish(reachFrames.full) }
const stairBySource = new Map(stairRegister.assets.map((asset) => [asset.source, publish(path.join(root, asset.source))]))
const stair = stairRig.timeline.map((frame) => {
  const sourceRel = stairRegister.assets.find((asset) => asset.url === frame.src)?.source
  if (!sourceRel || !stairBySource.has(sourceRel)) throw new Error(`cannot resolve V16 ${frame.src}`)
  return { ...frame, src: stairBySource.get(sourceRel).url }
})

const walkMs = 1000 / timing.walkFps
const turnMs = 1000 / timing.turnFps
const stairMs = geometry.frameDurationMs
const floorBottomLp = geometry.floorTopLp - 0.5
const upperBottomLp = geometry.floorTopLp + geometry.flightRiseLp - 0.5
const doorXLp = 140.5
const hiddenXLp = 161.5
const lowerStairRootLp = geometry.floorSupportCentreLp
const landingRootLp = 14.5
const doorStopRootLp = 130
const doorHandleXLp = 144
const candidate42DeltasKu = [3, 7, 13, 19]
const walkDeltaLp = 21 / 8

const copyFrame = (frame, extra = {}) => ({ ...frame, ...extra })
const lowerWalk = []
for (let index = 0; index < 16; index++) {
  const cycleFrame = index % 8
  lowerWalk.push({
    src: walk[cycleFrame].url,
    flipX: true,
    xLp: hiddenXLp - (index + 1) * walkDeltaLp,
    bottomLp: floorBottomLp,
    durationMs: walkMs,
    phase: index < 8 ? 'walk begins behind door; emerge' : 'visible whole-cycle stair approach',
    label: `mirrored approved Walk V6 F${cycleFrame + 1}`,
    sourceFrame: `walk:${cycleFrame + 1}`,
    lowerDoorOpen: 1,
    upperDoorOpen: 0,
  })
}
const lowerClimb = stair.slice(0, 7).map((frame) => copyFrame(frame, { flipX: false, durationMs: stairMs, phase: 'approved V16 climb begins without stopping', sourceFrame: `stair:${frame.frame}`, lowerDoorOpen: 1, upperDoorOpen: 0 }))
const lowerTimeline = [...lowerWalk, ...lowerClimb]

const lastStair = stair.slice(-5).map((frame) => copyFrame(frame, { flipX: false, durationMs: stairMs, phase: 'approved V16 reaches upper landing', sourceFrame: `stair:${frame.frame}`, lowerDoorOpen: 0, upperDoorOpen: 0 }))
const landingPass = {
  src: walk[2].url,
  flipX: true,
  xLp: 20.5,
  bottomLp: upperBottomLp,
  durationMs: walkMs,
  phase: 'trailing foot passes fully onto flat landing',
  label: 'mirrored approved Walk V6 F3 · compact landing pass',
  sourceFrame: 'walk:3',
  lowerDoorOpen: 0,
  upperDoorOpen: 0,
}
const landingSettle = {
  src: sideBack[0].url,
  flipX: true,
  xLp: landingRootLp,
  bottomLp: upperBottomLp,
  durationMs: walkMs,
  phase: 'both feet established; brief registered neutral',
  label: 'exact approved side authority mirrored left',
  sourceFrame: 'side-back:1',
  lowerDoorOpen: 0,
  upperDoorOpen: 0,
}
const turnAround = []
for (let frame = 2; frame <= 9; frame++) turnAround.push({ src: sideBack[frame - 1].url, flipX: true, xLp: landingRootLp, bottomLp: upperBottomLp, durationMs: turnMs, phase: 'clockwise turn side-left toward back', label: `approved Turn V9 F${frame} mirrored`, sourceFrame: `side-back:${frame}`, lowerDoorOpen: 0, upperDoorOpen: 0 })
for (let frame = 8; frame >= 1; frame--) turnAround.push({ src: sideBack[frame - 1].url, flipX: false, xLp: landingRootLp, bottomLp: upperBottomLp, durationMs: turnMs, phase: 'clockwise turn back toward side-right', label: `approved Turn V9 F${frame}`, sourceFrame: `side-back:${frame}`, lowerDoorOpen: 0, upperDoorOpen: 0 })

const acceleration = []
let exitRootLp = landingRootLp
for (let index = 0; index < candidate42DeltasKu.length; index++) {
  exitRootLp += candidate42DeltasKu[index] / 8
  acceleration.push({
    src: bridge[index + 1].url,
    flipX: false,
    xLp: exitRootLp,
    bottomLp: upperBottomLp,
    durationMs: walkMs,
    phase: 'grid-closing stop-to-walk acceleration',
    label: `approved bridge pose ${index + 2} · candidate-42 root +${candidate42DeltasKu[index]} ku`,
    sourceFrame: `bridge:${index + 2}`,
    deltaKu: candidate42DeltasKu[index],
    lowerDoorOpen: 0,
    upperDoorOpen: 0,
  })
}
if (exitRootLp !== 19.75) throw new Error(`candidate-42 endpoint changed: ${exitRootLp}`)
const hallwayWalk = []
for (let index = 0; index < 40; index++) {
  const walkFrame = ((index + 1) % 8) + 1 // bridge ends on F1; continue at F2
  const xLp = exitRootLp + (index + 1) * walkDeltaLp
  hallwayWalk.push({
    src: walk[walkFrame - 1].url,
    flipX: false,
    xLp,
    bottomLp: upperBottomLp,
    durationMs: walkMs,
    phase: 'walk through upper hallway toward closed door',
    label: `approved Walk V6 F${walkFrame}`,
    sourceFrame: `walk:${walkFrame}`,
    lowerDoorOpen: 0,
    upperDoorOpen: 0,
  })
}
if (hallwayWalk.at(-1).xLp !== 124.75 || hallwayWalk.at(-1).sourceFrame !== 'walk:1') throw new Error('upper approach walk endpoint changed')
const deceleration = []
let stopRootLp = hallwayWalk.at(-1).xLp
for (let index = 0; index < candidate42DeltasKu.length; index++) {
  const deltaKu = [...candidate42DeltasKu].reverse()[index]
  stopRootLp += deltaKu / 8
  deceleration.push({
    src: bridge[3 - index].url,
    flipX: false,
    xLp: stopRootLp,
    bottomLp: upperBottomLp,
    durationMs: walkMs,
    phase: 'decelerate to door-handle stop',
    label: `approved bridge pose ${4 - index} · candidate-42 root +${deltaKu} ku`,
    sourceFrame: `bridge:${4 - index}`,
    deltaKu,
    lowerDoorOpen: 0,
    upperDoorOpen: 0,
  })
}
if (stopRootLp !== doorStopRootLp) throw new Error(`door stop root changed: ${stopRootLp}`)
const doorAction = [
  { src: reach.partial.url, sourceFrame: 'door-reach:partial', durationMs: 100, phase: 'right hand begins reaching for handle', label: 'new Prime door reach · partial', upperDoorOpen: 0 },
  { src: reach.full.url, sourceFrame: 'door-reach:full', durationMs: 120, phase: 'right hand meets handle', label: 'new Prime door reach · full contact', upperDoorOpen: 0 },
  { src: reach.full.url, sourceFrame: 'door-reach:full', durationMs: 90, phase: 'right hand pulls; door starts opening', label: 'full reach · door one-third open', upperDoorOpen: 1 / 3 },
  { src: reach.full.url, sourceFrame: 'door-reach:full', durationMs: 90, phase: 'right hand pulls; door continues opening', label: 'full reach · door two-thirds open', upperDoorOpen: 2 / 3 },
  { src: reach.full.url, sourceFrame: 'door-reach:full', durationMs: 140, phase: 'door reaches fully open position', label: 'full reach · door open', upperDoorOpen: 1 },
  { src: reach.partial.url, sourceFrame: 'door-reach:partial', durationMs: 100, phase: 'right hand retracts from handle', label: 'new Prime door reach · retract', upperDoorOpen: 1 },
  { src: sideBack[0].url, sourceFrame: 'side-back:1', durationMs: 70, phase: 'brief exact side neutral before stepping through', label: 'approved side authority · open door', upperDoorOpen: 1 },
].map((frame) => ({ ...frame, flipX: false, xLp: doorStopRootLp, bottomLp: upperBottomLp, lowerDoorOpen: 0 }))
const doorAcceleration = []
let doorExitRootLp = doorStopRootLp
for (let index = 0; index < candidate42DeltasKu.length; index++) {
  doorExitRootLp += candidate42DeltasKu[index] / 8
  doorAcceleration.push({ src: bridge[index + 1].url, flipX: false, xLp: doorExitRootLp, bottomLp: upperBottomLp, durationMs: walkMs, phase: 'accelerate through open doorway', label: `approved bridge pose ${index + 2} · +${candidate42DeltasKu[index]} ku`, sourceFrame: `bridge:${index + 2}`, deltaKu: candidate42DeltasKu[index], lowerDoorOpen: 0, upperDoorOpen: 1 })
}
const doorWalk = []
for (let index = 0; index < 10; index++) {
  const walkFrame = ((index + 1) % 8) + 1
  const xLp = doorExitRootLp + (index + 1) * walkDeltaLp
  doorWalk.push({ src: walk[walkFrame - 1].url, flipX: false, xLp, bottomLp: upperBottomLp, durationMs: walkMs, phase: xLp === doorXLp ? 'cross registered open doorway' : xLp > doorXLp ? 'continue behind opaque open door leaf' : 'step into open doorway', label: `approved Walk V6 F${walkFrame}`, sourceFrame: `walk:${walkFrame}`, lowerDoorOpen: 0, upperDoorOpen: 1 })
}
const doorCrossingIndex = doorWalk.findIndex((frame) => frame.xLp === doorXLp)
if (doorCrossingIndex !== 1 || doorWalk.at(-1).xLp !== hiddenXLp) throw new Error('upper open-door exit closure changed')
const upperTimeline = [...lastStair, landingPass, landingSettle, ...turnAround, ...acceleration, ...hallwayWalk, ...deceleration, ...doorAction, ...doorAcceleration, ...doorWalk]
const fullTimeline = [...lowerWalk, ...stair.map((frame) => copyFrame(frame, { flipX: false, durationMs: stairMs, phase: 'approved V16 full climb', sourceFrame: `stair:${frame.frame}`, lowerDoorOpen: 1, upperDoorOpen: 0 })), landingPass, landingSettle, ...turnAround, ...acceleration, ...hallwayWalk, ...deceleration, ...doorAction, ...doorAcceleration, ...doorWalk]

const spec = {
  schema: 'lighthouse-keeper/stair-transitions@1',
  status: 'draft-two-route-transition-review-awaiting-frank',
  units: { kuPerLp: 8, walkDeltaKu: 21, walkDeltaLp, cell: [256, 320], density: 8 },
  geometry: {
    stair: { risers: 14, treadRunLp: 7, flightRunLp: 98, flightRiseLp: 60, lowerFloorYLp: 20, upperFloorYLp: 80 },
    transferDoorXLp: doorXLp,
    hiddenRootXLp: hiddenXLp,
    lowerStairRootLp,
    upperLandingRootLp: landingRootLp,
    upperDoorStopRootLp: doorStopRootLp,
    upperDoorHandleXLp: doorHandleXLp,
    lowerDoorToStairLp: doorXLp - lowerStairRootLp,
    upperLandingToDoorLp: doorXLp - landingRootLp,
    doorToHiddenLp: hiddenXLp - doorXLp,
  },
  rootMotion: {
    lower: 'two exact 21-lp walk cycles, first behind/through the door and second fully visible, then a moving V16 F1 join',
    upperAccelerationCandidate: { id: 'candidate-42', deltasKu: candidate42DeltasKu, totalKu: candidate42DeltasKu.reduce((a, b) => a + b, 0), totalLp: candidate42DeltasKu.reduce((a, b) => a + b, 0) / 8, artworkChanged: false },
    upper: 'landing at x=14.5; clockwise side-left→back→side-right turn; candidate-42 acceleration, five exact cycles and reverse bridge stop at x=130; right-hand reach opens the door; candidate-42 restart crosses x=140.5 and reaches x=161.5 fully hidden',
    turnParityRule: 'bottom-right→top-left travel turns clockwise side-left→back→side-right; the opposite bottom-left→top-right flight turns clockwise side-right→front→side-left',
  },
  timing: { walkFps: timing.walkFps, turnFps: timing.turnFps, stairFrameMs: stairMs, terminalStairHoldRemovedForContinuation: true },
  routes: {
    lowerJoin: { id: 'lower', title: 'Door → walk → stair start', frames: lowerTimeline },
    upperExit: { id: 'upper', title: 'Stair exit → clockwise turn → walk → open door → exit', frames: upperTimeline },
    fullFlow: { id: 'full', title: 'Door → walk → full climb → clockwise turn → open door → exit', frames: fullTimeline },
  },
  boundaries: { approvedSourcePixelsChanged: false, cssMirroringOnlyForApprovedFrames: true, newKeeperDoorReachArtworkPresent: true, newKeeperArtworkAccepted: false, rejectedGeneratedStudyUsed: false, finalChanged: false, runtimeChanged: false, productionChanged: false },
}
const specPath = path.join(pack, 'keeper-prime-stair-transitions-v1.json')
writeJson(specPath, spec)

const stairsMarkup = Array.from({ length: geometry.risers }, (_, index) => { const n = index + 1; return `<span class="step" data-x="${geometry.stairBaseRightLp - n * geometry.treadRunLp}" data-y="${geometry.floorTopLp}" data-w="${geometry.treadRunLp}" data-h="${n * geometry.riserRiseLp}"></span>` }).join('')
const htmlBase = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keeper Prime stair transitions V1</title><style>
*{box-sizing:border-box}body{margin:0;background:#07131b;color:#eef7fa;font:15px/1.45 system-ui,sans-serif}header,main{max-width:1320px;margin:auto;padding:22px}header{border-bottom:1px solid #294654}a{color:#8ed7ff}.status{display:inline-block;border:1px solid #e8b852;color:#ffe09d;border-radius:999px;padding:5px 10px}.rule{border-left:4px solid #75e6a7;background:#17271f;padding:12px 14px}.panel{background:#10232d;border:1px solid #2c4a59;border-radius:12px;padding:16px;margin:16px 0}.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}button,select{font:inherit;color:#fff;background:#194057;border:1px solid #507587;border-radius:8px;padding:8px 12px}button:disabled,select:disabled{opacity:.45}.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}.stageScroll{overflow:auto}.stage{position:relative;overflow:hidden;background:#122b37;border:1px solid #496878}.stage.large{width:960px;height:750px}.stage.game{width:160px;height:125px}.world{position:absolute;inset:0}.step{position:absolute;background:#536775;border-top-style:solid;border-top-color:#d0dee6;border-left-style:solid;border-left-color:#263d49}.deck,.floor{position:absolute;background:#536775;border-top-style:solid;border-top-color:#d0dee6}.doorFrame{position:absolute;border-style:solid;border-color:#8ea7b4;background:#1b3441;z-index:2}.doorLeaf{position:absolute;background:linear-gradient(90deg,#284756,#426574);border-left-style:solid;border-left-color:#a8c0ca;z-index:8}.walker{position:absolute;object-fit:contain;z-index:4;transform-origin:center}.rootDot{position:absolute;border-radius:50%;background:#ff4f7a;z-index:10;display:none}.rootLine{position:absolute;border-left-style:dashed;border-left-color:#ff8ca6;z-index:9;display:none}.showRoots .rootDot,.showRoots .rootLine{display:block}.hideDoors .doorLeaf{display:none}.views{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:22px;align-items:start}.progress{height:8px;background:#1a3542;border-radius:99px;overflow:hidden}.progress span{display:block;height:100%;background:#75e6a7}.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}.metric b{display:block;font-size:24px;color:#75e6a7}.warn{border-left:4px solid #e8b852;background:#2a2518;padding:12px 14px}@media(max-width:1120px){.views{grid-template-columns:1fr}.stage.large{width:960px}}
</style></head><body><header><a href="/keeper-review/keeper-prime-stair-ascent-v16/">← Approved Stair Ascent V16</a><h1>Keeper Prime stair transitions V1</h1><span class="status">Reversible route candidate · nothing promoted</span><p>Two exact door/stair joins using approved Keeper pixels, plus a complete end-to-end inspection route.</p></header><main><p class="rule"><strong>Primary checks:</strong> he begins walking while hidden behind the lower door; the walk ends directly in a moving first stair frame; both feet establish on the upper landing before the turn; and the hallway walk crosses the same registered door axis without sliding or walking on the spot.</p><section class="panel"><div class="controls"><label>Sequence <select id="route" disabled><option value="lower">1 · Door → walk → stair start</option><option value="upper">2 · Stair exit → turn → hallway → door</option><option value="full">3 · Complete lower-door to upper-door flow</option></select></label><button id="play" disabled>Play</button><button id="pause" disabled>Pause</button><button id="prev" disabled>← Previous frame</button><button id="next" disabled>Next frame →</button><button id="restart" disabled>Restart</button><label><input id="loop" type="checkbox"> Loop</label><label><input id="roots" type="checkbox"> Root guide</label><label><input id="doors" type="checkbox" checked> Door occlusion</label></div><p id="loading" class="readout">Loading and decoding every unique frame…</p><p id="readout" class="readout"></p><div class="progress"><span id="progress"></span></div></section><section class="panel views"><div><h2>Large transition inspection</h2><div class="stageScroll"><div class="stage large" data-scale="6"><div class="world">${stairsMarkup}<div class="floor lower"></div><div class="deck upper"></div><div class="doorFrame lowerDoor"></div><div class="doorFrame upperDoor"></div><div class="doorLeaf lowerLeaf"></div><div class="doorLeaf upperLeaf"></div><div class="rootLine"></div><div class="rootDot"></div><img class="walker" alt="Keeper stair transition"></div></div></div></div><div><h2>Exact game scale</h2><p>1 CSS px = 1 logical px.</p><div class="stage game" data-scale="1"><div class="world">${stairsMarkup}<div class="floor lower"></div><div class="deck upper"></div><div class="doorFrame lowerDoor"></div><div class="doorFrame upperDoor"></div><div class="doorLeaf lowerLeaf"></div><div class="doorLeaf upperLeaf"></div><div class="rootLine"></div><div class="rootDot"></div><img class="walker" alt="Exact-scale Keeper stair transition"></div></div></div></section><section class="metrics"><div class="panel metric"><b>21 lp</b>door → stair root<p>One fully visible walk cycle after emerging.</p></div><div class="panel metric"><b>0 held frames</b>walk → climb<p>Mirrored Walk F8 hands into advancing V16 F1.</p></div><div class="panel metric"><b>126 lp</b>landing → door<p>Twelve step intervals across the upper hallway.</p></div><div class="panel metric"><b>21 lp</b>door → hidden<p>One further cycle behind the opaque leaf.</p></div></section><p class="warn"><strong>One root-motion item is deliberately under review:</strong> the upper stop-to-walk bridge uses the proposed 3, 7, 13, 19 ku displacement schedule (42 ku / 5.25 lp total) with the exact approved bridge drawings. That makes the registered landing-to-door distance close exactly without altering a pixel. It does not rewrite the approved stop→walk→stop authority.</p><section class="panel"><h2>Art boundary</h2><p>Walk V6, Stair Ascent V16, the side authority, the turn drawings and the stop-to-walk bridge remain byte-identical. Left-facing poses are browser-mirrored only. Both generated landing studies were rejected—one changed the silhouette and the other had three arms—and neither is loaded by this page. Final, runtime and production remain unchanged.</p></section></main><script>
const SPEC=${JSON.stringify(spec)};const routes={lower:SPEC.routes.lowerJoin,upper:SPEC.routes.upperExit,full:SPEC.routes.fullFlow};const unique=[...new Set(Object.values(routes).flatMap(route=>route.frames.map(frame=>frame.src)))];const stages=[...document.querySelectorAll('.stage')],controls=[...document.querySelectorAll('button,select')];let routeId='lower',index=0,timer=null;
function px(value,scale){return value*scale+'px'}function layout(stage){const s=Number(stage.dataset.scale),world=stage.querySelector('.world');world.querySelectorAll('.step').forEach(el=>{el.style.left=px(Number(el.dataset.x),s);el.style.bottom=px(Number(el.dataset.y),s);el.style.width=px(Number(el.dataset.w),s);el.style.height=px(Number(el.dataset.h),s);el.style.borderTopWidth=px(.5,s);el.style.borderLeftWidth=px(.2,s)});for(const el of world.querySelectorAll('.lower')){el.style.left=px(116,s);el.style.bottom='0';el.style.width=px(44,s);el.style.height=px(20,s);el.style.borderTopWidth=px(.5,s)}for(const el of world.querySelectorAll('.upper')){el.style.left='0';el.style.bottom=px(78,s);el.style.width=px(160,s);el.style.height=px(2,s);el.style.borderTopWidth=px(.5,s)}for(const el of world.querySelectorAll('.doorFrame')){const upper=el.classList.contains('upperDoor');el.style.left=px(131.5,s);el.style.bottom=px(upper?80:20,s);el.style.width=px(18,s);el.style.height=px(44,s);el.style.borderWidth=px(.5,s)}for(const el of world.querySelectorAll('.doorLeaf')){const upper=el.classList.contains('upperLeaf');el.style.bottom=px(upper?80:20,s);el.style.height=px(44,s);el.style.borderLeftWidth=px(.5,s)}for(const el of world.querySelectorAll('.doorKnob')){const upper=el.classList.contains('upperKnob');el.style.left=px(${doorHandleXLp}-.7,s);el.style.bottom=px((upper?80:20)+19.3,s);el.style.width=el.style.height=px(1.4,s)}}
function active(){return routes[routeId].frames}function render(){const frames=active(),frame=frames[index];for(const stage of stages){const s=Number(stage.dataset.scale),img=stage.querySelector('.walker'),dot=stage.querySelector('.rootDot'),line=stage.querySelector('.rootLine');img.src=frame.src;img.style.width=px(32,s);img.style.height=px(40,s);img.style.left=px(frame.xLp-16,s);img.style.bottom=px(frame.bottomLp,s);img.style.transform=frame.flipX?'scaleX(-1)':'none';dot.style.width=dot.style.height=px(1.4,s);dot.style.left=px(frame.xLp-.7,s);dot.style.bottom=px((frame.bottomLp+.5)-.7,s);line.style.left=px(frame.xLp,s);line.style.bottom='0';line.style.height=px(125,s);line.style.borderLeftWidth=px(.25,s);for(const leaf of stage.querySelectorAll('.doorLeaf')){const upper=leaf.classList.contains('upperLeaf'),open=upper?(frame.upperDoorOpen??0):(frame.lowerDoorOpen??0);leaf.style.left=px(137+(3.5*open),s);leaf.style.width=px(12.5+(7*open),s);leaf.style.zIndex=open>.8?'8':'3'}}document.getElementById('readout').textContent=routes[routeId].title+' · F'+(index+1)+'/'+frames.length+' · '+frame.phase+' · root ('+frame.xLp.toFixed(3)+', '+(frame.bottomLp+.5).toFixed(3)+') lp · '+frame.label;document.getElementById('progress').style.width=((index+1)/frames.length*100)+'%'}
function stop(){if(timer)clearTimeout(timer);timer=null}function tick(){const frames=active();if(index>=frames.length-1){if(!document.getElementById('loop').checked)return stop();index=0}else index++;render();timer=setTimeout(tick,frames[index].durationMs)}function play(){stop();if(index>=active().length-1)index=0;render();timer=setTimeout(tick,active()[index].durationMs)}function preload(src){return new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>{const decoded=im.decode?.();decoded?decoded.then(resolve).catch(resolve):resolve()};im.onerror=()=>reject(new Error(src));im.src=src})}
document.getElementById('route').onchange=e=>{stop();routeId=e.target.value;index=0;render();play()};document.getElementById('play').onclick=play;document.getElementById('pause').onclick=stop;document.getElementById('prev').onclick=()=>{stop();index=Math.max(0,index-1);render()};document.getElementById('next').onclick=()=>{stop();index=Math.min(active().length-1,index+1);render()};document.getElementById('restart').onclick=()=>{stop();index=0;render();play()};document.getElementById('roots').onchange=e=>stages.forEach(stage=>stage.classList.toggle('showRoots',e.target.checked));document.getElementById('doors').onchange=e=>stages.forEach(stage=>stage.classList.toggle('hideDoors',!e.target.checked));stages.forEach(layout);Promise.all(unique.map(preload)).then(()=>{controls.forEach(control=>control.disabled=false);document.getElementById('loading').textContent='All '+unique.length+' unique frame images decoded before playback';render();play()}).catch(error=>{document.getElementById('loading').textContent='Playback locked: '+error.message});
</script></body></html>`
const html = htmlBase
  .replace('Two exact door/stair joins using approved Keeper pixels, plus a complete end-to-end inspection route.', 'Two measured door/stair joins using approved Keeper authorities plus a new reversible right-hand door-reach candidate.')
  .replace('both feet establish on the upper landing before the turn; and the hallway walk crosses the same registered door axis without sliding or walking on the spot.', 'both feet establish on the upper landing before a clockwise turn via the back view; then he stops at the handle, reaches with his right hand, opens the door and walks through until hidden.')
  .replace('Stair exit → turn → hallway → door', 'Stair exit → clockwise turn → walk → open door → exit')
  .replace('One root-motion item is deliberately under review:', 'Two linked items are deliberately under review:')
  .replace('the upper stop-to-walk bridge uses the proposed 3, 7, 13, 19 ku displacement schedule (42 ku / 5.25 lp total) with the exact approved bridge drawings. That makes the registered landing-to-door distance close exactly without altering a pixel. It does not rewrite the approved stop→walk→stop authority.', 'the upper start/stop bridges use the proposed 3, 7, 13, 19 ku root schedule with exact approved bridge drawings, and the two new Prime door-reach drawings are candidate art. The Keeper stops at x=130 lp, reaches the handle at x=144 lp, opens the door, returns briefly to exact neutral, then walks through. Neither item rewrites an approval record.')
  .replace('Walk V6, Stair Ascent V16, the side authority, the turn drawings and the stop-to-walk bridge remain byte-identical. Left-facing poses are browser-mirrored only. Both generated landing studies were rejected—one changed the silhouette and the other had three arms—and neither is loaded by this page. Final, runtime and production remain unchanged.', 'Walk V6, Stair Ascent V16, approved Turn V9 and the stop/walk bridge remain byte-identical. The landing turn now follows the clockwise side-left → back → side-right path; the opposite flight must use clockwise side-right → front → side-left. The two generated landing studies remain rejected, including the three-armed result. Only the two clearly labelled right-hand door-reach frames are new candidate art. Final, runtime and production remain unchanged.')
  .replaceAll('<div class="doorLeaf upperLeaf"></div><div class="rootLine">', '<div class="doorLeaf upperLeaf"></div><div class="doorKnob lowerKnob"></div><div class="doorKnob upperKnob"></div><div class="rootLine">')
  .replace('.doorLeaf{position:absolute;background:linear-gradient(90deg,#284756,#426574);border-left-style:solid;border-left-color:#a8c0ca;z-index:8}', '.doorLeaf{position:absolute;background:linear-gradient(90deg,#284756,#426574);border-left-style:solid;border-left-color:#a8c0ca;z-index:3}.doorKnob{position:absolute;border-radius:50%;background:#f5c842;border:1px solid #5c4611;z-index:9}')
const pagePath = path.join(publicDir, 'index.html')
fs.writeFileSync(pagePath, html)

const authority = (file) => ({ file: rel(file), sha256: sha(file) })
const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-stair-transitions-2026-10-15-v1',
  status: spec.status,
  purpose: 'Review the exact lower door-to-stair join and upper stair-to-hallway-to-door exit before runtime wiring.',
  authorities: {
    approvedStairAscent: authority(stairApprovalPath),
    stairV16Rig: authority(stairRigPath),
    approvedWalk: authority(walkApprovalPath),
    approvedStopWalkStop: authority(stopWalkApprovalPath),
    approvedSideBackTurn: authority(sideBackApprovalPath),
    oppositeParityFrontTurnSource: authority(turnRegisterPath),
    fastTiming: authority(timingApprovalPath),
  },
  generation: {
    selectedKeeperArtwork: 'two new reversible candidate door-reach drawings only; all other displayed Keeper art is exact authority art',
    doorReachCandidates: [
      { role: 'partial right-hand reach', source: authority(reachSources.partial), registeredSource: authority(reachRegistered.partial), maskedDraft: authority(reachFrames.partial), selectedForReviewOnly: true },
      { role: 'full right-hand handle contact', source: authority(reachSources.full), registeredSource: authority(reachRegistered.full), maskedDraft: authority(reachFrames.full), selectedForReviewOnly: true },
    ],
    doorReachMask: { ...authority(reachMaskPath), polygon: reachPolygon, outsideMaskAuthority: rel(sideNeutralPath), outsideMaskAuthoritySha256: sha(sideNeutralPath) },
    cssMirroring: ['Walk V6 for left travel', 'approved Turn V9 for side-left to back', 'exact side endpoint for landing settle'],
    rejectedStudies: [
      { file: rel(rejectedStudyPaths[0]), sha256: sha(rejectedStudyPaths[0]), reason: 'Not used: materially wider silhouette and changed identity/rendering compared with the accepted authorities.' },
      { file: rel(rejectedStudyPaths[1]), sha256: sha(rejectedStudyPaths[1]), reason: 'Not used: wrong-facing pose with three arms.' },
    ],
    promptLog: rel(path.join(pack, 'PROMPT_LOG.md')),
  },
  spec: authority(specPath),
  reviewPage: { ...authority(pagePath), publicReview: `/keeper-review/${set}/`, controls: ['sequence', 'play', 'pause', 'previous-frame', 'next-frame', 'restart', 'loop', 'root-guide', 'door-occlusion'], preloadsAllUniqueFrames: true },
  publishedAssets: published,
  validation: {
    uniquePublishedFrames: published.length,
    lowerFrames: lowerTimeline.length,
    upperFrames: upperTimeline.length,
    fullFrames: fullTimeline.length,
    lowerDoorToStairLp: doorXLp - lowerStairRootLp,
    lowerPauseFramesAtJoin: 0,
    lowerLastWalkFrame: 'Walk V6 F8 mirrored',
    lowerFirstClimbFrame: 'Stair Ascent V16 F1',
    upperBothFeetEstablishedBeforeTurn: true,
    upperLandingToDoorLp: doorXLp - landingRootLp,
    upperDoorStopRootLp: doorStopRootLp,
    upperDoorHandleXLp: doorHandleXLp,
    clockwiseLandingTurnViaBack: true,
    oppositeFlightClockwiseTurnViaFront: true,
    doorReachCandidateFrames: 2,
    doorActionTimelineFrames: doorAction.length,
    upperDoorToHiddenLp: hiddenXLp - doorXLp,
    upperDoorCrossingAfterRestartFrame: doorCrossingIndex + 1,
    upperAccelerationTotalKu: candidate42DeltasKu.reduce((a, b) => a + b, 0),
    walkingOnSpotFrames: 0,
    approvedPixelBytesChanged: false,
    newDoorReachCandidateArtworkPresent: true,
    generatedStudyUsed: false,
    finalChanged: false,
    runtimeChanged: false,
    productionChanged: false,
  },
  approvalBoundary: { reviewCandidateApproved: false, candidate42RootMotionApproved: false, doorReachArtworkApproved: false, finalLaneEntryAllowed: false, productionPromotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and ${rel(publicDir)}; all approved source art and historical reviews remain unchanged.`,
}
writeJson(path.join(pack, 'batch-register.json'), register)
console.log(JSON.stringify({ page: rel(pagePath), uniqueFrames: published.length, routes: { lower: lowerTimeline.length, upper: upperTimeline.length, full: fullTimeline.length }, doorCrossingAfterRestartFrame: doorCrossingIndex + 1 }, null, 2))
