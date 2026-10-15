import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'

const root = process.cwd()
const previousSet = 'keeper-prime-stair-transitions-v5'
const set = 'keeper-prime-stair-transitions-v6'
const previousPack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-16-v5')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-16-v6')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')

fs.mkdirSync(pack, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const previousSpecFile = path.join(previousPack, 'keeper-prime-stair-transitions-v5.json')
const previousRegisterFile = path.join(previousPack, 'batch-register.json')
const previousPageFile = path.join(root, 'public/keeper-review', previousSet, 'index.html')
const previousSpec = readJson(previousSpecFile)
const previousRegister = readJson(previousRegisterFile)

const published = previousRegister.publishedAssets.map((asset) => {
  const source = path.join(root, asset.source)
  if (!fs.existsSync(source) || sha(source) !== asset.sourceSha256) throw new Error(`source authority changed ${asset.source}`)
  const filename = path.basename(asset.url)
  fs.copyFileSync(source, path.join(assetsDir, filename))
  return { ...asset, url: `/keeper-review/${set}/assets/${filename}` }
})

const walkOpaquePixels = 27322
const stairOpaquePixels = 24299
const circulationArtScale = Math.sqrt(stairOpaquePixels / walkOpaquePixels)
const isStair = (frame) => frame.sourceFrame?.startsWith('stair:') || frame.sourceFrame?.startsWith('stair-mount:')
const remapFrame = (frame) => {
  const next = { ...frame, src: frame.src.replace(`/keeper-review/${previousSet}/`, `/keeper-review/${set}/`) }
  if (isStair(next)) delete next.artScale
  else next.artScale = circulationArtScale
  return next
}

const spec = {
  ...previousSpec,
  schema: 'lighthouse-keeper/stair-transitions@6',
  set,
  status: 'door-hidden-circulation-scale-handoff-awaiting-review',
  routes: Object.fromEntries(Object.entries(previousSpec.routes).map(([key, route]) => [key, { ...route, frames: route.frames.map(remapFrame) }])),
  sizeRegistration: {
    method: 'door-hidden change from normal room scale to one constant stair-circulation scale; native approved stair frames remain unscaled',
    rootInCellLp: [16, 39.5],
    walkOpaquePixels,
    stairOpaquePixels,
    circulationArtScale,
    registeredWalkEquivalentOpaquePixels: walkOpaquePixels * circulationArtScale * circulationArtScale,
    departureHandoff: 'completed while Keeper is fully behind the lower room door before visible travel',
    arrivalHandoff: 'reset only after Keeper is fully behind the upper room door',
    visibleRouteScaleRule: 'all walk, turn, bridge and reach frames use circulationArtScale; all Stair V16 frames use native scale 1',
  },
}
const specFile = path.join(pack, 'keeper-prime-stair-transitions-v6.json')
writeJson(specFile, spec)

let html = fs.readFileSync(previousPageFile, 'utf8')
html = html
  .replaceAll(previousSet, set)
  .replaceAll('stair transitions V5', 'stair transitions V6')
  .replaceAll('Stair transitions V5', 'Stair transitions V6')
  .replace('The stair family is uniformly registered to the approved walk’s whole silhouette mass, correcting the remaining frame 16→17 contraction without changing drawings or timing.', 'Normal room scale changes to one constant circulation scale only while the Keeper is door-hidden; every visible walk, stair, turn and exit frame then remains consistent.')
  .replace('<b>equal silhouette mass</b>walk → climb<p>27,322-px walk pose → 27,322-px equivalent registered stair pose.</p>', '<b>hidden handoff</b>room → stairs<p>Normal scale changes behind the door; visible travel stays at one circulation scale.</p>')
  .replace('V5 keeps the exact route and source bytes, then applies one uniform 1.060× root-anchored whole-silhouette registration to every stair-family frame. It introduces no new Keeper pixels and no one-frame-only correction.', 'V6 keeps native Stair V16 pixels at scale 1 and uses one constant 0.943× root-anchored scale for every walk, turn, bridge and reach frame between the two opaque doors. The normal/circulation scale handoffs occur only under complete door occlusion.')

const specStart = html.indexOf('const SPEC=')
const routesStart = html.indexOf(';const routes=', specStart)
if (specStart < 0 || routesStart < 0) throw new Error('cannot replace embedded V5 spec')
html = `${html.slice(0, specStart)}const SPEC=${JSON.stringify(spec)}${html.slice(routesStart)}`
const pageFile = path.join(publicDir, 'index.html')
fs.writeFileSync(pageFile, html)

const handoffFile = path.join(pack, 'HANDOFF.md')
fs.writeFileSync(handoffFile, `# Keeper Prime stair transitions V6\n\nFrank established that any scale reconciliation can happen while the Keeper is fully obscured behind the room door; it must not happen at the visible walk-to-stair seam. V6 therefore leaves the approved Stair V16 family at native scale 1. The door-to-door circulation route uses one constant walk/turn/bridge/reach scale of sqrt(${stairOpaquePixels}/${walkOpaquePixels}) = ${circulationArtScale.toFixed(9)}×, matching Walk F7's opaque silhouette mass to the stair mount. The normal-room-to-circulation handoff is complete before the Keeper becomes visible at the lower door, and the inverse handoff happens only after he is fully hidden at the upper door. V5 remains rejected provenance. Source images, order, timing, roots, stairs, doors, Final, runtime and production remain unchanged.\n\nReview: \`/keeper-review/${set}/\`.\n`)

const authority = (file) => ({ file: rel(file), sha256: sha(file) })
const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-stair-transitions-2026-10-16-v6',
  status: spec.status,
  purpose: 'Move scale reconciliation under complete door occlusion and hold one visible scale through the entire stair route.',
  previousCandidate: { register: rel(previousRegisterFile), sha256: sha(previousRegisterFile), immutable: true, disposition: 'superseded-height-and-stair-scaling-approach' },
  correction: {
    reportedSeam: 'lower route frames 16 → 17', circulationArtScale,
    registeredWalkEquivalentOpaquePixels: walkOpaquePixels * circulationArtScale * circulationArtScale,
    stairArtScale: 1, visibleScaleChanges: 0,
    departureScaleHandoffFullyDoorHidden: true, arrivalScaleHandoffFullyDoorHidden: true,
    sourcePixelsChanged: false, timingChanged: false, rootMotionChanged: false,
  },
  spec: authority(specFile), handoff: authority(handoffFile),
  reviewPage: { ...authority(pageFile), publicReview: `/keeper-review/${set}/`, preloadsAllUniqueFrames: true },
  publishedAssets: published,
  validation: { uniquePublishedFrames: published.length, routeLengthsUnchanged: true, sourceHashesUnchanged: true, approvedPixelBytesChanged: false, finalChanged: false, runtimeChanged: false, productionChanged: false },
  approvalBoundary: { reviewCandidateApproved: false, finalLaneEntryAllowed: false, productionPromotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and ${rel(publicDir)}; V1–V5 and every approved source remain unchanged.`,
}
writeJson(path.join(pack, 'batch-register.json'), register)

console.log(JSON.stringify({ page: rel(pageFile), circulationArtScale, stairArtScale: 1, equivalentOpaquePixels: walkOpaquePixels * circulationArtScale * circulationArtScale, routes: Object.fromEntries(Object.entries(spec.routes).map(([key, route]) => [key, route.frames.length])) }, null, 2))
