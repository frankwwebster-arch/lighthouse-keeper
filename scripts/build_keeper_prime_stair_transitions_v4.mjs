import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { PNG } from 'pngjs'

const root = process.cwd()
const previousSet = 'keeper-prime-stair-transitions-v3'
const set = 'keeper-prime-stair-transitions-v4'
const previousPack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-16-v3')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-16-v4')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')

fs.mkdirSync(pack, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const previousSpecFile = path.join(previousPack, 'keeper-prime-stair-transitions-v3.json')
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

function alphaBounds(file) {
  const png = PNG.sync.read(fs.readFileSync(file))
  let minY = png.height
  let maxY = -1
  for (let y = 0; y < png.height; y++) {
    for (let x = 0; x < png.width; x++) {
      if (png.data[(y * png.width + x) * 4 + 3] > 0) {
        minY = Math.min(minY, y)
        maxY = Math.max(maxY, y)
      }
    }
  }
  if (maxY < 0) throw new Error(`empty authority ${rel(file)}`)
  return { minY, maxY }
}

const walkF7 = path.join(root, 'art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames/keeper_prime_walk-right_f7.png')
const stairPassing = path.join(root, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16/drafts/frames/keeper_prime_stair_left-foot-passing-compact_side-left_f01.png')
const rootYSourcePx = 316 // 39.5 lp in the 8×, 40-lp cell
const walkCapToRootPx = rootYSourcePx - alphaBounds(walkF7).minY
const stairCapToRootPx = rootYSourcePx - alphaBounds(stairPassing).minY
const stairArtScale = walkCapToRootPx / stairCapToRootPx
if (walkCapToRootPx !== 293 || stairCapToRootPx !== 285) throw new Error('cap-to-root authority changed')

const isStair = (frame) => frame.sourceFrame?.startsWith('stair:') || frame.sourceFrame?.startsWith('stair-mount:')
const remapFrame = (frame) => ({
  ...frame,
  src: frame.src.replace(`/keeper-review/${previousSet}/`, `/keeper-review/${set}/`),
  ...(isStair(frame) ? { artScale: stairArtScale } : {}),
})

const spec = {
  ...previousSpec,
  schema: 'lighthouse-keeper/stair-transitions@4',
  set,
  status: 'stair-family-scale-registration-awaiting-review',
  routes: Object.fromEntries(Object.entries(previousSpec.routes).map(([key, route]) => [key, { ...route, frames: route.frames.map(remapFrame) }])),
  sizeRegistration: {
    method: 'uniform complete-cell display scale around the registered root; no source pixels rewritten',
    rootInCellLp: [16, 39.5],
    walkAuthority: rel(walkF7),
    stairAuthority: rel(stairPassing),
    walkCapToRootSourcePx: walkCapToRootPx,
    stairCapToRootSourcePx: stairCapToRootPx,
    stairArtScale,
    registeredStairCapToRootSourcePx: stairCapToRootPx * stairArtScale,
    appliesTo: 'every stair and stair-mount frame in every route',
  },
}
const specFile = path.join(pack, 'keeper-prime-stair-transitions-v4.json')
writeJson(specFile, spec)

let html = fs.readFileSync(previousPageFile, 'utf8')
html = html
  .replaceAll(previousSet, set)
  .replaceAll('stair transitions V3', 'stair transitions V4')
  .replaceAll('Stair transitions V3', 'Stair transitions V4')
  .replace('The unchanged V2 seam correction with a stable reviewer and the actual default 4× in-game presentation.', 'The stair family is uniformly root-registered to the approved walk height, removing the frame 16→17 shrink without changing drawings or timing.')
  .replace('transform-origin:center', 'transform-origin:50% 98.75%')
  .replace('<b>smoothed seam</b>walk → climb<p>Compact Walk F7 → compact passing bridge → V16 F1.</p>', '<b>exact height</b>walk → climb<p>293-px walk cap/root span → 293-px registered stair span.</p>')
  .replace('V2 rotates the cyclic walk phase and reuses the exact approved compact left-foot passing drawing as a single mount bridge; it introduces no new Keeper pixels.', 'V4 keeps the exact V2/V3 route and source bytes, then applies one uniform 1.028× root-anchored display registration to every stair-family frame. It introduces no new Keeper pixels and no one-frame-only correction.')

const oldTransform = "img.style.transform=frame.flipX?'scaleX(-1)':'none';"
const newTransform = "const transforms=[];if(frame.flipX)transforms.push('scaleX(-1)');if(frame.artScale)transforms.push('scale('+frame.artScale+')');img.style.transform=transforms.join(' ')||'none';"
if (!html.includes(oldTransform)) throw new Error('cannot replace V3 transform logic')
html = html.replace(oldTransform, newTransform)

const specStart = html.indexOf('const SPEC=')
const routesStart = html.indexOf(';const routes=', specStart)
if (specStart < 0 || routesStart < 0) throw new Error('cannot replace embedded V3 spec')
html = `${html.slice(0, specStart)}const SPEC=${JSON.stringify(spec)}${html.slice(routesStart)}`
const pageFile = path.join(publicDir, 'index.html')
fs.writeFileSync(pageFile, html)

const handoffFile = path.join(pack, 'HANDOFF.md')
fs.writeFileSync(handoffFile, `# Keeper Prime stair transitions V4\n\nV4 corrects Frank's reported F16→F17 character shrink. Measured from the shared registered root at source y=316, mirrored Walk V6 F7 has a 293-pixel cap-to-root span while the approved Stair V16 family has 285 pixels. Every stair and stair-mount route frame now receives the same uniform ${stairArtScale.toFixed(9)}× display registration around [16,39.5] logical pixels. This makes the cap-to-root span exactly 293 source pixels, preserves each approved drawing and avoids moving the size change to the next frame or the upper landing. V3 remains immutable. Timing, route order, roots, doors, Final, runtime and production remain unchanged.\n\nReview: \`/keeper-review/${set}/\`.\n`)

const authority = (file) => ({ file: rel(file), sha256: sha(file) })
const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-stair-transitions-2026-10-16-v4',
  status: spec.status,
  purpose: 'Remove the visible walk-to-stair scale contraction without altering approved pixels, timing or route roots.',
  previousCandidate: { register: rel(previousRegisterFile), sha256: sha(previousRegisterFile), immutable: true },
  correction: {
    reportedSeam: 'lower route frames 16 → 17',
    walkCapToRootSourcePx: walkCapToRootPx,
    stairCapToRootSourcePx: stairCapToRootPx,
    stairArtScale,
    registeredStairCapToRootSourcePx: stairCapToRootPx * stairArtScale,
    appliesToAllStairRouteFrames: true,
    transformOrigin: 'registered root [16,39.5] lp',
    sourcePixelsChanged: false,
    timingChanged: false,
    rootMotionChanged: false,
  },
  authorities: {
    walkF7: authority(walkF7),
    stairPassing: authority(stairPassing),
  },
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
  rollback: `Delete only ${rel(pack)} and ${rel(publicDir)}; V1–V3 and every approved source remain unchanged.`,
}
writeJson(path.join(pack, 'batch-register.json'), register)

console.log(JSON.stringify({ page: rel(pageFile), stairArtScale, walkCapToRootPx, stairCapToRootPx, routes: Object.fromEntries(Object.entries(spec.routes).map(([key, route]) => [key, route.frames.length])) }, null, 2))
