import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'

const root = process.cwd()
const previousSet = 'keeper-prime-stair-transitions-v1'
const set = 'keeper-prime-stair-transitions-v2'
const previousPack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-15-v1')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-15-v2')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')

fs.mkdirSync(pack, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const previousSpecFile = path.join(previousPack, 'keeper-prime-stair-transitions-v1.json')
const previousRegisterFile = path.join(previousPack, 'batch-register.json')
const previousPageFile = path.join(root, 'public/keeper-review', previousSet, 'index.html')
const previousSpec = readJson(previousSpecFile)
const previousRegister = readJson(previousRegisterFile)

const published = previousRegister.publishedAssets.map((asset) => {
  const source = path.join(root, asset.source)
  if (!fs.existsSync(source)) throw new Error(`missing source ${asset.source}`)
  if (sha(source) !== asset.sourceSha256) throw new Error(`source hash changed ${asset.source}`)
  const filename = path.basename(asset.url)
  const target = path.join(assetsDir, filename)
  fs.copyFileSync(source, target)
  return { ...asset, url: `/keeper-review/${set}/assets/${filename}` }
})

const urlBySource = new Map(published.map((asset) => [asset.source, asset.url]))
const remap = (frame) => ({ ...frame, src: frame.src.replace(`/keeper-review/${previousSet}/`, `/keeper-review/${set}/`) })
const walkSource = (frame) => `art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames/keeper_prime_walk-right_f${frame}.png`
const walkUrl = (frame) => {
  const url = urlBySource.get(walkSource(frame))
  if (!url) throw new Error(`missing published walk frame ${frame}`)
  return url
}

// Keep the two complete eight-frame cycles and every root position, but rotate
// their phase so the visible approach finishes on compact Walk F7 rather than
// broad Walk F8. The first cycle begins behind the door, so this changes no
// exposed start endpoint.
const oldLower = previousSpec.routes.lowerJoin.frames.map(remap)
const rotatedWalkOrder = [8, 1, 2, 3, 4, 5, 6, 7]
const lowerWalk = oldLower.slice(0, 16).map((frame, index) => {
  const walkFrame = rotatedWalkOrder[index % 8]
  return {
    ...frame,
    src: walkUrl(walkFrame),
    label: `mirrored approved Walk V6 F${walkFrame}`,
    sourceFrame: `walk:${walkFrame}`,
  }
})

const oldClimb = oldLower.slice(16)
const passingLeft = oldClimb.find((frame) => frame.sourceFrame === 'stair:4')
if (!passingLeft) throw new Error('approved compact left-foot passing frame not found')
const mountBridge = {
  ...passingLeft,
  xLp: 118.75,
  bottomLp: 19.5,
  supportTread: 0,
  targetTread: 1,
  supportXLp: 119.5,
  supportYLp: 20,
  targetXLp: 112.5,
  targetYLp: 24.285714285714285,
  durationMs: 100,
  phase: 'lift left foot from walk cadence toward first tread',
  label: 'approved LEFT compact passing · dedicated walk-to-stair bridge',
  sourceFrame: 'stair-mount:left-passing',
}
delete mountBridge.frame
delete mountBridge.movingXLp
delete mountBridge.movingYLp
delete mountBridge.supportClearanceLp
delete mountBridge.movingLegMinimumClearanceLp
delete mountBridge.movingLegPenetratingPixels

const lowerTimeline = [...lowerWalk, mountBridge, ...oldClimb]
const seamTimeline = lowerTimeline.slice(12, 21)
const upperTimeline = previousSpec.routes.upperExit.frames.map(remap)
const oldFull = previousSpec.routes.fullFlow.frames.map(remap)
const fullTimeline = [...lowerWalk, mountBridge, ...oldFull.slice(16)]

const spec = {
  ...previousSpec,
  schema: 'lighthouse-keeper/stair-transitions@2',
  set,
  status: 'walk-to-stair-seam-correction-awaiting-review',
  routeNotes: {
    ...previousSpec.routeNotes,
    lower: 'two exact approved walk cycles phase-rotated to finish on compact Walk F7, one exact approved compact passing bridge, then exact Stair V16 F1',
  },
  routes: {
    seamReview: { id: 'seam', title: 'Focused walk → stair seam', frames: seamTimeline },
    lowerJoin: { ...previousSpec.routes.lowerJoin, title: 'Door → walk → compact mount → stair start', frames: lowerTimeline },
    upperExit: { ...previousSpec.routes.upperExit, frames: upperTimeline },
    fullFlow: { ...previousSpec.routes.fullFlow, frames: fullTimeline },
  },
  boundaries: { ...previousSpec.boundaries, approvedSourcePixelsChanged: false, newWalkToStairArtworkPresent: false },
}

const specFile = path.join(pack, 'keeper-prime-stair-transitions-v2.json')
writeJson(specFile, spec)

let html = fs.readFileSync(previousPageFile, 'utf8')
html = html
  .replaceAll(previousSet, set)
  .replaceAll('stair transitions V1', 'stair transitions V2')
  .replaceAll('Stair transitions V1', 'Stair transitions V2')
  .replace('<option value="lower">1 · Door → walk → stair start</option>', '<option value="seam">1 · Focused walk → stair seam</option><option value="lower">2 · Door → walk → stair start</option>')
  .replace('<option value="upper">2 · Stair exit → clockwise turn → walk → open door → exit</option>', '<option value="upper">3 · Stair exit → clockwise turn → walk → open door → exit</option>')
  .replace('<option value="full">3 · Complete lower-door to upper-door flow</option>', '<option value="full">4 · Complete lower-door to upper-door flow</option>')
  .replace('the walk ends directly in a moving first stair frame;', 'the compact walk cadence lifts into a dedicated passing pose before first-tread contact;')
  .replace('<b>0 held frames</b>walk → climb<p>Mirrored Walk F8 hands into advancing V16 F1.</p>', '<b>0 size flash</b>walk → climb<p>Compact Walk F7 → compact passing bridge → V16 F1.</p>')
  .replace('Two measured door/stair joins using approved Keeper authorities plus a new reversible right-hand door-reach candidate.', 'The V1 routes with a corrected walk-to-stair seam using only exact approved Keeper authorities.')
  .replace('Walk V6, Stair Ascent V16, approved Turn V9 and the stop/walk bridge remain byte-identical.', 'Walk V6, Stair Ascent V16, approved Turn V9 and the stop/walk bridge remain byte-identical. V2 rotates the cyclic walk phase and reuses the exact approved compact left-foot passing drawing as a single mount bridge; it introduces no new Keeper pixels.')

const specStart = html.indexOf('const SPEC=')
const routesStart = html.indexOf(';const routes=', specStart)
if (specStart < 0 || routesStart < 0) throw new Error('cannot replace embedded V1 spec')
html = `${html.slice(0, specStart)}const SPEC=${JSON.stringify(spec)}${html.slice(routesStart)}`
html = html.replace('const routes={lower:SPEC.routes.lowerJoin,upper:SPEC.routes.upperExit,full:SPEC.routes.fullFlow}', 'const routes={seam:SPEC.routes.seamReview,lower:SPEC.routes.lowerJoin,upper:SPEC.routes.upperExit,full:SPEC.routes.fullFlow}')
html = html.replace("let routeId='lower'", "let routeId='seam'")
const pageFile = path.join(publicDir, 'index.html')
fs.writeFileSync(pageFile, html)

const handoffFile = path.join(pack, 'HANDOFF.md')
fs.writeFileSync(handoffFile, `# Keeper Prime stair transitions V2\n\nV2 corrects only the visible Walk V6 to Stair Ascent V16 seam reported on 15 October 2026. V1 changed from broad mirrored Walk F8 directly to the compact stair model at frames 16 to 17. V2 retains two full approved eight-frame walk cycles and every root position, rotates the cyclic phase to end on compact mirrored Walk F7, then inserts the exact approved Stair V16 LEFT compact passing drawing before first-tread contact. No Keeper pixels, approved source, Final, runtime or production file is changed.\n\nReview: \`/keeper-review/${set}/\`.\n`)

const authority = (file) => ({ file: rel(file), sha256: sha(file) })
const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-stair-transitions-2026-10-15-v2',
  status: spec.status,
  purpose: 'Remove the one-frame Keeper silhouette contraction at the approved walk-to-stair join without redrawing or resizing either approved animation.',
  previousCandidate: { register: rel(previousRegisterFile), sha256: sha(previousRegisterFile), immutable: true },
  authorities: previousRegister.authorities,
  correction: {
    reportedSeam: 'V1 lower route frames 16 → 17',
    previous: 'mirrored Walk V6 F8 → Stair Ascent V16 F1',
    candidate: 'mirrored Walk V6 F7 → exact approved LEFT compact passing → Stair Ascent V16 F1',
    walkPhaseOrder: rotatedWalkOrder,
    completeWalkCyclesRetained: 2,
    rootScheduleChanged: false,
    sourcePixelsChanged: false,
    newArtworkCreated: false,
  },
  spec: authority(specFile),
  handoff: authority(handoffFile),
  reviewPage: { ...authority(pageFile), publicReview: `/keeper-review/${set}/`, preloadsAllUniqueFrames: true },
  publishedAssets: published,
  validation: {
    uniquePublishedFrames: published.length,
    seamFrames: seamTimeline.length,
    lowerFrames: lowerTimeline.length,
    upperFrames: upperTimeline.length,
    fullFrames: fullTimeline.length,
    lowerLastWalkFrame: 'Walk V6 F7 mirrored',
    lowerBridgeFrame: 'Stair Ascent V16 LEFT compact passing',
    lowerFirstContactFrame: 'Stair Ascent V16 F1',
    lowerPauseFramesAtJoin: 0,
    approvedPixelBytesChanged: false,
    finalChanged: false,
    runtimeChanged: false,
    productionChanged: false,
  },
  approvalBoundary: { reviewCandidateApproved: false, finalLaneEntryAllowed: false, productionPromotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and ${rel(publicDir)}; V1 and all approved sources remain unchanged.`,
}
writeJson(path.join(pack, 'batch-register.json'), register)

console.log(JSON.stringify({ page: rel(pageFile), routes: { lower: lowerTimeline.length, upper: upperTimeline.length, full: fullTimeline.length }, uniqueFrames: published.length }, null, 2))
