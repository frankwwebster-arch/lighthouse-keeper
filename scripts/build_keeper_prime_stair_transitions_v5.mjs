import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { PNG } from 'pngjs'

const root = process.cwd()
const previousSet = 'keeper-prime-stair-transitions-v4'
const set = 'keeper-prime-stair-transitions-v5'
const previousPack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-16-v4')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-16-v5')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')

fs.mkdirSync(pack, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const previousSpecFile = path.join(previousPack, 'keeper-prime-stair-transitions-v4.json')
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

function opaquePixels(file) {
  const png = PNG.sync.read(fs.readFileSync(file))
  let count = 0
  for (let offset = 3; offset < png.data.length; offset += 4) if (png.data[offset] > 0) count++
  return count
}

const walkF7 = path.join(root, 'art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames/keeper_prime_walk-right_f7.png')
const stairPassing = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16/drafts/frames/keeper_prime_stair_left-foot-passing-compact_side-left_f01.png')
const walkOpaquePixels = opaquePixels(walkF7)
const stairOpaquePixels = opaquePixels(stairPassing)
const stairArtScale = Math.sqrt(walkOpaquePixels / stairOpaquePixels)
if (walkOpaquePixels !== 27322 || stairOpaquePixels !== 24299) throw new Error('whole-silhouette authority changed')

const isStair = (frame) => frame.sourceFrame?.startsWith('stair:') || frame.sourceFrame?.startsWith('stair-mount:')
const remapFrame = (frame) => ({
  ...frame,
  src: frame.src.replace(`/keeper-review/${previousSet}/`, `/keeper-review/${set}/`),
  ...(isStair(frame) ? { artScale: stairArtScale } : {}),
})

const spec = {
  ...previousSpec,
  schema: 'lighthouse-keeper/stair-transitions@5',
  set,
  status: 'stair-family-whole-silhouette-registration-awaiting-review',
  routes: Object.fromEntries(Object.entries(previousSpec.routes).map(([key, route]) => [key, { ...route, frames: route.frames.map(remapFrame) }])),
  sizeRegistration: {
    method: 'uniform whole-silhouette opaque-area display registration around the registered root; no source pixels rewritten',
    rootInCellLp: [16, 39.5],
    walkAuthority: rel(walkF7),
    stairAuthority: rel(stairPassing),
    walkOpaquePixels,
    stairOpaquePixels,
    stairArtScale,
    registeredStairEquivalentOpaquePixels: stairOpaquePixels * stairArtScale * stairArtScale,
    appliesTo: 'every stair and stair-mount frame in every route',
  },
}
const specFile = path.join(pack, 'keeper-prime-stair-transitions-v5.json')
writeJson(specFile, spec)

let html = fs.readFileSync(previousPageFile, 'utf8')
html = html
  .replaceAll(previousSet, set)
  .replaceAll('stair transitions V4', 'stair transitions V5')
  .replaceAll('Stair transitions V4', 'Stair transitions V5')
  .replace('The stair family is uniformly root-registered to the approved walk height, removing the frame 16→17 shrink without changing drawings or timing.', 'The stair family is uniformly registered to the approved walk’s whole silhouette mass, correcting the remaining frame 16→17 contraction without changing drawings or timing.')
  .replace('<b>exact height</b>walk → climb<p>293-px walk cap/root span → 293-px registered stair span.</p>', '<b>equal silhouette mass</b>walk → climb<p>27,322-px walk pose → 27,322-px equivalent registered stair pose.</p>')
  .replace('V4 keeps the exact V2/V3 route and source bytes, then applies one uniform 1.028× root-anchored display registration to every stair-family frame. It introduces no new Keeper pixels and no one-frame-only correction.', 'V5 keeps the exact route and source bytes, then applies one uniform 1.060× root-anchored whole-silhouette registration to every stair-family frame. It introduces no new Keeper pixels and no one-frame-only correction.')

const specStart = html.indexOf('const SPEC=')
const routesStart = html.indexOf(';const routes=', specStart)
if (specStart < 0 || routesStart < 0) throw new Error('cannot replace embedded V4 spec')
html = `${html.slice(0, specStart)}const SPEC=${JSON.stringify(spec)}${html.slice(routesStart)}`
const pageFile = path.join(publicDir, 'index.html')
fs.writeFileSync(pageFile, html)

const handoffFile = path.join(pack, 'HANDOFF.md')
fs.writeFileSync(handoffFile, `# Keeper Prime stair transitions V5\n\nV4 matched only cap-to-root height, but Frank still saw the complete Keeper contract at F16→F17. V5 measures whole opaque silhouette mass: mirrored Walk V6 F7 contains ${walkOpaquePixels.toLocaleString('en-GB')} opaque source pixels and the Stair V16 LEFT compact passing authority contains ${stairOpaquePixels.toLocaleString('en-GB')}. Uniform linear scale is therefore sqrt(${walkOpaquePixels}/${stairOpaquePixels}) = ${stairArtScale.toFixed(9)}×. Every stair and stair-mount route frame receives that same root-anchored registration, so the correction remains stable across the climb and upper landing. V4 remains immutable. Source images, frame order, timing, roots, doors, Final, runtime and production remain unchanged.\n\nReview: \`/keeper-review/${set}/\`.\n`)

const authority = (file) => ({ file: rel(file), sha256: sha(file) })
const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-stair-transitions-2026-10-16-v5',
  status: spec.status,
  purpose: 'Correct the persistent walk-to-stair contraction using whole-silhouette mass rather than height alone.',
  previousCandidate: { register: rel(previousRegisterFile), sha256: sha(previousRegisterFile), immutable: true },
  correction: {
    reportedSeam: 'lower route frames 16 → 17',
    rejectedMeasurement: 'cap-to-root height alone',
    walkOpaquePixels,
    stairOpaquePixels,
    stairArtScale,
    registeredStairEquivalentOpaquePixels: stairOpaquePixels * stairArtScale * stairArtScale,
    appliesToAllStairRouteFrames: true,
    transformOrigin: 'registered root [16,39.5] lp',
    sourcePixelsChanged: false,
    timingChanged: false,
    rootMotionChanged: false,
  },
  authorities: { walkF7: authority(walkF7), stairPassing: authority(stairPassing) },
  spec: authority(specFile),
  handoff: authority(handoffFile),
  reviewPage: { ...authority(pageFile), publicReview: `/keeper-review/${set}/`, preloadsAllUniqueFrames: true },
  publishedAssets: published,
  validation: {
    uniquePublishedFrames: published.length,
    stairFramesRegistered: Object.values(spec.routes).reduce((count, route) => count + route.frames.filter(isStair).length, 0),
    routeLengthsUnchanged: true,
    sourceHashesUnchanged: true,
    approvedPixelBytesChanged: false,
    finalChanged: false,
    runtimeChanged: false,
    productionChanged: false,
  },
  approvalBoundary: { reviewCandidateApproved: false, finalLaneEntryAllowed: false, productionPromotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and ${rel(publicDir)}; V1–V4 and every approved source remain unchanged.`,
}
writeJson(path.join(pack, 'batch-register.json'), register)

console.log(JSON.stringify({ page: rel(pageFile), stairArtScale, walkOpaquePixels, stairOpaquePixels, routes: Object.fromEntries(Object.entries(spec.routes).map(([key, route]) => [key, route.frames.length])) }, null, 2))
