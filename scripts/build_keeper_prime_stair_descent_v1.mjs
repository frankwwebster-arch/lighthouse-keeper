#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const sourceSet = 'keeper-prime-stair-transitions-v6'
const set = 'keeper-prime-stair-descent-v1'
const sourcePack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-16-v6')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-descent-2026-10-16-v1')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const frontTurnPack = path.join(root, 'art/drafts/keeper-prime-turn-front-side-2026-10-13-v1')
const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const authority = (file) => ({ file: rel(file), sha256: sha(file) })

fs.mkdirSync(pack, { recursive: true })
fs.rmSync(publicDir, { recursive: true, force: true })
fs.mkdirSync(assetsDir, { recursive: true })

const sourceSpecFile = path.join(sourcePack, 'keeper-prime-stair-transitions-v6.json')
const sourceRegisterFile = path.join(sourcePack, 'batch-register.json')
const sourcePageFile = path.join(root, 'public/keeper-review', sourceSet, 'index.html')
const sourceSpec = readJson(sourceSpecFile)
const sourceRegister = readJson(sourceRegisterFile)
const frontRegisterFile = path.join(frontTurnPack, 'batch-register.json')
const frontRegister = readJson(frontRegisterFile)
const circulationScale = sourceSpec.sizeRegistration.circulationArtScale

const publishedByHash = new Map()
const published = []
function publish(file) {
  const digest = sha(file)
  if (publishedByHash.has(digest)) return publishedByHash.get(digest)
  const targetName = `frame-${digest.slice(0, 16)}.png`
  fs.copyFileSync(file, path.join(assetsDir, targetName))
  const record = { source: rel(file), sourceSha256: digest, url: `/keeper-review/${set}/assets/${targetName}` }
  publishedByHash.set(digest, record)
  published.push(record)
  return record
}

for (const asset of sourceRegister.publishedAssets) {
  const file = path.join(root, asset.source)
  if (!fs.existsSync(file) || sha(file) !== asset.sourceSha256) throw new Error(`approved source changed: ${asset.source}`)
  publish(file)
}
const frontTurn = frontRegister.frames.map((frame) => publish(path.join(root, frame.file)))

const sourceAssetByUrl = new Map(sourceRegister.publishedAssets.map((asset) => [asset.url, publishedByHash.get(asset.sourceSha256).url]))
const remap = (frame, extra = {}) => ({ ...frame, src: sourceAssetByUrl.get(frame.src) ?? frame.src, ...extra })
const bySourceFrame = new Map()
for (const route of Object.values(sourceSpec.routes)) for (const frame of route.frames) if (!bySourceFrame.has(frame.sourceFrame)) bySourceFrame.set(frame.sourceFrame, remap(frame))
const pose = (id, extra = {}) => {
  const frame = bySourceFrame.get(id)
  if (!frame) throw new Error(`missing approved pose ${id}`)
  return { ...frame, ...extra }
}

const walkMs = 1000 / sourceSpec.timing.walkFps
const turnMs = 1000 / sourceSpec.timing.turnFps
const stairMs = sourceSpec.timing.stairFrameMs
const floorBottom = 19.5
const upperBottom = 79.5
const landingX = 14.5
const stopX = 130
const hiddenX = 161.5
const walkDelta = 2.625
const common = { artScale: circulationScale }

// Begin behind the open upper door, walk left, and decelerate exactly onto the registered landing root.
const upperApproach = []
for (let index = 0; index < 54; index++) {
  const walkFrame = ((index + 3) % 8) + 1
  const xLp = hiddenX - (index + 1) * walkDelta
  upperApproach.push(pose(`walk:${walkFrame}`, {
    ...common, flipX: true, xLp, bottomLp: upperBottom, durationMs: walkMs,
    phase: index < 12 ? 'emerge from upper door and continue left' : 'walk left across upper circulation landing',
    label: `mirrored approved Walk V6 F${walkFrame}`,
    lowerDoorOpen: 0,
    upperDoorOpen: xLp > 124 ? 1 : 0,
  }))
}
if (upperApproach.at(-1).xLp !== 19.75 || upperApproach.at(-1).sourceFrame !== 'walk:1') throw new Error('upper approach phase closure changed')
const upperStop = [
  [4, 17.375], [3, 15.75], [2, 14.875], [1, landingX],
].map(([frame, xLp]) => pose(`bridge:${frame}`, {
  ...common, flipX: true, xLp, bottomLp: upperBottom, durationMs: walkMs,
  phase: 'decelerate onto registered upper landing root', label: `mirrored approved bridge pose ${frame}`,
  lowerDoorOpen: 0, upperDoorOpen: 0,
}))

// Opposite zig-zag parity: side-left → front → side-right. Endpoints and intermediates are approved exact pixels.
const turnViaFront = []
for (let frame = 7; frame >= 1; frame--) turnViaFront.push({
  src: frontTurn[frame - 1].url, sourceFrame: `front-side:${frame}`, flipX: true,
  xLp: landingX, bottomLp: upperBottom, durationMs: turnMs, phase: 'turn side-left toward full front',
  label: `approved front↔side turn F${frame} mirrored`, lowerDoorOpen: 0, upperDoorOpen: 0, ...common,
})
for (let frame = 2; frame <= 8; frame++) turnViaFront.push({
  src: frontTurn[frame - 1].url, sourceFrame: `front-side:${frame}`, flipX: false,
  xLp: landingX, bottomLp: upperBottom, durationMs: turnMs, phase: 'continue from full front to side-right',
  label: `approved front→side-right F${frame}`, lowerDoorOpen: 0, upperDoorOpen: 0, ...common,
})

const topMount = [pose('walk:3', {
  ...common, flipX: false, xLp: 20.5, bottomLp: upperBottom, durationMs: walkMs,
  phase: 'leading foot leaves flat landing toward first descending tread',
  label: 'approved Walk V6 F3 · reversed landing-pass join', lowerDoorOpen: 0, upperDoorOpen: 0,
})]
const stairSource = sourceSpec.routes.fullFlow.frames.filter((frame) => /^stair:\d+$/.test(frame.sourceFrame))
if (stairSource.length !== 27) throw new Error(`expected 27 stair frames, found ${stairSource.length}`)
let descentRootX = -Infinity
const descent = [...stairSource].reverse().map((frame, index) => {
  const originalXLp = frame.xLp
  descentRootX = Math.max(descentRootX, originalXLp)
  return remap(frame, {
    flipX: true, xLp: descentRootX, durationMs: stairMs,
    phase: 'approved V16 mechanics reversed: descend one tread at a time',
    label: `descent ${index + 1}/27 · ${frame.label}`, lowerDoorOpen: 0, upperDoorOpen: 0,
    descentRootCorrectionLp: descentRootX - originalXLp,
  })
})

const lowerDismount = [
  pose('stair-mount:left-passing', { flipX: true, xLp: 118.75, bottomLp: floorBottom, durationMs: walkMs, phase: 'trailing foot clears final tread', label: 'approved compact passing pose · reversed lower mount', lowerDoorOpen: 0, upperDoorOpen: 0 }),
  pose('walk:7', { ...common, flipX: false, xLp: 119.5, bottomLp: floorBottom, durationMs: walkMs, phase: 'both feet establish on lower floor in moving cadence', label: 'approved Walk V6 F7', lowerDoorOpen: 0, upperDoorOpen: 0 }),
  pose('walk:8', { ...common, flipX: false, xLp: 122.125, bottomLp: floorBottom, durationMs: walkMs, phase: 'continue directly toward lower door', label: 'approved Walk V6 F8', lowerDoorOpen: 0, upperDoorOpen: 0 }),
  pose('walk:1', { ...common, flipX: false, xLp: 124.75, bottomLp: floorBottom, durationMs: walkMs, phase: 'continue directly toward lower door', label: 'approved Walk V6 F1', lowerDoorOpen: 0, upperDoorOpen: 0 }),
]
const lowerStop = [[4,127.125],[3,128.75],[2,129.625],[1,130]].map(([frame,xLp]) => pose(`bridge:${frame}`, {
  ...common, flipX:false, xLp, bottomLp:floorBottom, durationMs:walkMs, phase:'decelerate to lower door handle',
  label:`approved bridge pose ${frame}`, lowerDoorOpen:0, upperDoorOpen:0,
}))

const sourceDoorAction = sourceSpec.routes.upperExit.frames.filter((frame) => frame.sourceFrame?.startsWith('door-reach:') || frame.phase?.includes('brief exact'))
if (sourceDoorAction.length !== 7) throw new Error(`door action authority changed: ${sourceDoorAction.length}`)
const lowerDoorAction = sourceDoorAction.map((frame) => {
  const next = remap(frame, { ...common, xLp: stopX, bottomLp: floorBottom, lowerDoorOpen: frame.upperDoorOpen ?? 0, upperDoorOpen: 0 })
  delete next.upperDoorOpen
  next.upperDoorOpen = 0
  return next
})
const exitAcceleration = [
  [2,130.375],[3,131.25],[4,132.875],[5,135.25],
].map(([frame,xLp]) => pose(`bridge:${frame}`, { ...common, flipX:false, xLp, bottomLp:floorBottom, durationMs:walkMs, phase:'accelerate through open lower doorway', label:`approved bridge pose ${frame}`, lowerDoorOpen:1, upperDoorOpen:0 }))
const exitWalk = []
for (let index = 0; index < 10; index++) {
  const walkFrame = ((index + 1) % 8) + 1
  const xLp = 135.25 + (index + 1) * walkDelta
  exitWalk.push(pose(`walk:${walkFrame}`, { ...common, flipX:false, xLp, bottomLp:floorBottom, durationMs:walkMs,
    phase:xLp < 140.5?'step into open lower doorway':xLp===140.5?'cross registered lower doorway':'continue behind opaque door leaf until fully hidden',
    label:`approved Walk V6 F${walkFrame}`, lowerDoorOpen:1, upperDoorOpen:0 }))
}
if (exitWalk.at(-1).xLp !== hiddenX) throw new Error('lower door hidden endpoint changed')

const descentOnly = [...upperStop.slice(-1), ...turnViaFront, ...topMount, ...descent, ...lowerDismount]
const lowerExit = [...descent.slice(-5), ...lowerDismount, ...lowerStop, ...lowerDoorAction, ...exitAcceleration, ...exitWalk]
const fullFlow = [...upperApproach, ...upperStop, ...turnViaFront, ...topMount, ...descent, ...lowerDismount, ...lowerStop, ...lowerDoorAction, ...exitAcceleration, ...exitWalk]
const spec = {
  schema:'lighthouse-keeper/stair-descent@1', set, status:'draft-stair-descent-v1-awaiting-frank',
  units:sourceSpec.units, geometry:sourceSpec.geometry,
  timing:{ walkFps:sourceSpec.timing.walkFps, turnFps:sourceSpec.timing.turnFps, stairFrameMs:stairMs },
  direction:{ travel:'upper-left to lower-right', facing:'side-right', mechanics:'exact approved V16 source-frame timeline in reverse order with CSS horizontal mirroring; 0.25-lp reverse-time passing-frame root regressions clamped forward', turnParity:'side-left → front → side-right' },
  sizeRegistration:{ ...sourceSpec.sizeRegistration, visibleScaleChanges:0 },
  routes:{
    turnMount:{id:'turn',title:'Upper landing stop → turn → first steps down',frames:[...upperStop,...turnViaFront,...topMount,...descent.slice(0,7)]},
    descentOnly:{id:'descent',title:'Turn → full stair descent → lower landing',frames:descentOnly},
    lowerExit:{id:'exit',title:'Final stairs → stop → open door → exit',frames:lowerExit},
    fullFlow:{id:'full',title:'Upper door → walk → turn → descend → open lower door → exit',frames:fullFlow},
  },
  boundaries:{approvedSourcePixelsChanged:false,cssMirroringOnly:true,newKeeperArtworkPresent:false,ascentAuthorityChanged:false,finalChanged:false,runtimeChanged:false,productionChanged:false},
}
const specFile = path.join(pack, 'keeper-prime-stair-descent-v1.json')
writeJson(specFile, spec)

let html = fs.readFileSync(sourcePageFile, 'utf8')
html = html.replaceAll(sourceSet, set)
  .replaceAll('Keeper Prime stair transitions V6','Keeper Prime stair descent V1')
  .replaceAll('keeper Prime stair transitions V6','keeper Prime stair descent V1')
  .replace('<a href="/keeper-review/keeper-prime-stair-ascent-v16/">← Approved Stair Ascent V16</a>', '<a href="/keeper-review/keeper-prime-stair-transitions-v6/">← Approved upward stair route</a>')
  .replace(/<p>Normal room scale changes[\s\S]*?<\/p><\/header>/, '<p>First complete downward route: leave the upper room, turn via the front view, descend one tread at a time, then stop, open the lower door and walk through until hidden.</p></header>')
  .replace(/<p class="rule">[\s\S]*?<\/p><section class="panel">/, '<p class="rule"><strong>Primary checks:</strong> no backwards walking; the turn finishes side-right before the first descending step; right and left contacts remain exactly alternating; the final tread flows directly into the lower-floor walk; and the right-hand door reach remains clean.</p><section class="panel">')
  .replace(/<select id="route" disabled>[\s\S]*?<\/select>/, '<select id="route" disabled><option value="turn">1 · Landing stop → turn → first steps</option><option value="descent">2 · Full descent → lower landing</option><option value="exit">3 · Final stairs → open door → exit</option><option value="full">4 · Complete upper-door to lower-door flow</option></select>')
  .replace(/<section class="metrics">[\s\S]*?<section class="panel"><h2>Art boundary<\/h2><p>[\s\S]*?<\/p><\/section>/, '<section class="metrics"><div class="panel metric"><b>27 frames</b>descending stair cycle<p>Exact approved V16 order reversed; no redrawing.</p></div><div class="panel metric"><b>14 risers</b>one tread per contact<p>Alternating left/right mechanics preserved.</p></div><div class="panel metric"><b>0 visible</b>scale changes<p>Circulation scale changes only under door cover.</p></div><div class="panel metric"><b>21 lp</b>door → fully hidden<p>Same registered door crossing as the upward route.</p></div></section><p class="warn"><strong>Review status:</strong> this is a new reversible draft, not Final. The stair drawings, walk, turn, bridge and reach pixels are unchanged; only sequencing, mirroring, roots and door state are proposed.</p><section class="panel"><h2>Art boundary</h2><p>Stair Ascent V16 remains the immutable drawing authority. Descent uses those exact 27 frames in reverse time and mirrors them to face side-right. The top and bottom joins use only existing approved poses. No canonical, Final, runtime or production art has changed.</p></section>')

const specStart = html.indexOf('const SPEC=')
const routesStart = html.indexOf(';const routes=', specStart)
const uniqueStart = html.indexOf(';const unique=', routesStart)
if (specStart < 0 || routesStart < 0 || uniqueStart < 0) throw new Error('cannot replace review script data')
html = `${html.slice(0,specStart)}const SPEC=${JSON.stringify(spec)};const routes={turn:SPEC.routes.turnMount,descent:SPEC.routes.descentOnly,exit:SPEC.routes.lowerExit,full:SPEC.routes.fullFlow}${html.slice(uniqueStart)}`
html = html.replace("let routeId='seam'", "let routeId='turn'")
const pageFile = path.join(publicDir, 'index.html')
fs.writeFileSync(pageFile, html)

const handoffFile = path.join(pack, 'HANDOFF.md')
fs.writeFileSync(handoffFile, `# Keeper Prime stair descent V1\n\nThis candidate completes the missing downward stair route without changing any Keeper drawing. Stair Ascent V16's 27 approved source frames run in exact reverse order and are horizontally mirrored so the Keeper faces down the upper-left → lower-right flight. The 0.25-lp reverse-time regressions on the right passing frames are clamped to the preceding contact root; this removes a tiny backwards body twitch without changing pixels, tread height or contact roots. Direction-specific joins are newly sequenced from approved pixels: upper-door walk and stop, side-left → front → side-right turn, first step down, lower-floor dismount, walk/stop, right-hand door reach and fully hidden exit.\n\nThe visible circulation scale remains constant. Any room/circulation scale handoff occurs only under complete door occlusion. This candidate is not approved or promoted.\n\nReview: \`/keeper-review/${set}/\`.\n`)
const register = {
  schema:'lighthouse-keeper/review-batch@1', batchId:'keeper-prime-stair-descent-2026-10-16-v1', status:spec.status,
  purpose:'Complete the first downward stair route using approved mechanics and direction-specific joins.',
  authorities:{ upwardRoute:{...authority(sourceRegisterFile),immutable:true}, ascentMechanics:{file:'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16/stair-contact-rig-v16.json',sha256:sha(path.join(root,'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16/stair-contact-rig-v16.json'))}, frontSideTurn:{...authority(frontRegisterFile),immutable:true}},
  spec:authority(specFile), handoff:authority(handoffFile), reviewPage:{...authority(pageFile),publicReview:`/keeper-review/${set}/`,preloadsAllUniqueFrames:true},
  publishedAssets:published,
  validation:{uniquePublishedFrames:published.length,approvedSourceHashesPinned:true,stairFrameCount:27,reverseOrder:true,alternatingContactsPreserved:true,transparentGuttersRequired:true,finalChanged:false,runtimeChanged:false,productionChanged:false},
  approvalBoundary:{reviewCandidateApproved:false,finalLaneEntryAllowed:false,productionPromotionAllowed:false},
  rollback:`Delete only ${rel(pack)} and ${rel(publicDir)}; all ascent, prior review and approved source material remains unchanged.`,
}
writeJson(path.join(pack,'batch-register.json'),register)
console.log(JSON.stringify({page:rel(pageFile),routes:Object.fromEntries(Object.entries(spec.routes).map(([key,route])=>[key,route.frames.length])),publishedAssets:published.length},null,2))
