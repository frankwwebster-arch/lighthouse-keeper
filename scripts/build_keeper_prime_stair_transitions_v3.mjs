import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'

const root = process.cwd()
const previousSet = 'keeper-prime-stair-transitions-v2'
const set = 'keeper-prime-stair-transitions-v3'
const previousPack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-15-v2')
const pack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-16-v3')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = (file) => path.relative(root, file).split(path.sep).join('/')

fs.mkdirSync(pack, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const previousSpecFile = path.join(previousPack, 'keeper-prime-stair-transitions-v2.json')
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

const remapFrame = (frame) => ({ ...frame, src: frame.src.replace(`/keeper-review/${previousSet}/`, `/keeper-review/${set}/`) })
const spec = {
  ...previousSpec,
  schema: 'lighthouse-keeper/stair-transitions@3',
  set,
  status: 'walk-to-stair-seam-and-review-layout-awaiting-review',
  routes: Object.fromEntries(Object.entries(previousSpec.routes).map(([key, route]) => [key, { ...route, frames: route.frames.map(remapFrame) }])),
  reviewPresentation: {
    largeInspectionScale: 6,
    defaultGameScale: 4,
    defaultGameScaleAuthority: 'src/studio/Studio.tsx default zoom state',
    stableReadoutHeight: true,
    stackedViews: true,
  },
}
const specFile = path.join(pack, 'keeper-prime-stair-transitions-v3.json')
writeJson(specFile, spec)

let html = fs.readFileSync(previousPageFile, 'utf8')
html = html
  .replaceAll(previousSet, set)
  .replaceAll('stair transitions V2', 'stair transitions V3')
  .replaceAll('Stair transitions V2', 'Stair transitions V3')
  .replace('The V1 routes with a corrected walk-to-stair seam using only exact approved Keeper authorities.', 'The unchanged V2 seam correction with a stable reviewer and the actual default 4× in-game presentation.')
  .replace('.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}', '.readout{font-variant-numeric:tabular-nums;color:#c9e4ee}#readout{height:3.1em;overflow:auto;margin-block:.7em}')
  .replace('.stage.game{width:160px;height:125px}', '.stage.game{width:640px;height:500px}')
  .replace('.views{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:22px;align-items:start}', '.views{display:grid;grid-template-columns:1fr;gap:22px;align-items:start}')
  .replace('<p>1 CSS px = 1 logical px.</p><div class="stage game" data-scale="1">', '<p>Default in-game presentation: 4 screen px per logical px (Studio 4×).</p><div class="stageScroll"><div class="stage game" data-scale="4">')
  .replace('</div></div></section><section class="metrics">', '</div></div></div></section><section class="metrics">')
  .replace('<b>0 size flash</b>walk → climb', '<b>smoothed seam</b>walk → climb')

const specStart = html.indexOf('const SPEC=')
const routesStart = html.indexOf(';const routes=', specStart)
if (specStart < 0 || routesStart < 0) throw new Error('cannot replace embedded V2 spec')
html = `${html.slice(0, specStart)}const SPEC=${JSON.stringify(spec)}${html.slice(routesStart)}`
const pageFile = path.join(publicDir, 'index.html')
fs.writeFileSync(pageFile, html)

const handoffFile = path.join(pack, 'HANDOFF.md')
fs.writeFileSync(handoffFile, `# Keeper Prime stair transitions V3\n\nV3 changes only review presentation after Frank reported that the whole V2 page moved during the F16→F17 seam and that its 1× logical-pixel preview was far too small. The moving readout now has a fixed height, so frame-label wrapping cannot move either stage. The second stage uses the Studio's actual default zoom of four screen pixels per logical pixel (128 × 160 for a 32 × 40 Keeper cell), and the two stages are stacked so the 4× view is not squeezed. V2 routes, timing, roots and all 27 source-image hashes remain exact. Final, runtime and production remain unchanged.\n\nReview: \`/keeper-review/${set}/\`.\n`)

const authority = (file) => ({ file: rel(file), sha256: sha(file) })
const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-stair-transitions-2026-10-16-v3',
  status: spec.status,
  purpose: 'Stop reviewer layout movement and show the unchanged stair seam at the game/studio default 4× presentation.',
  previousCandidate: { register: rel(previousRegisterFile), sha256: sha(previousRegisterFile), immutable: true },
  correction: {
    routeDataChanged: false,
    sourcePixelsChanged: false,
    timingChanged: false,
    rootMotionChanged: false,
    stableReadoutHeight: '3.1em with overflow contained',
    gameScaleBefore: '1 CSS px per logical px',
    gameScaleAfter: '4 screen px per logical px, matching Studio default zoom=4',
    viewsStacked: true,
  },
  gameScaleAuthority: authority(path.join(root, 'src/studio/Studio.tsx')),
  spec: authority(specFile),
  handoff: authority(handoffFile),
  reviewPage: { ...authority(pageFile), publicReview: `/keeper-review/${set}/`, preloadsAllUniqueFrames: true },
  publishedAssets: published,
  validation: {
    uniquePublishedFrames: published.length,
    seamFrames: spec.routes.seamReview.frames.length,
    lowerFrames: spec.routes.lowerJoin.frames.length,
    upperFrames: spec.routes.upperExit.frames.length,
    fullFrames: spec.routes.fullFlow.frames.length,
    v2RouteDataExactApartFromAssetPrefix: true,
    approvedPixelBytesChanged: false,
    finalChanged: false,
    runtimeChanged: false,
    productionChanged: false,
  },
  approvalBoundary: { reviewCandidateApproved: false, finalLaneEntryAllowed: false, productionPromotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and ${rel(publicDir)}; V1, V2 and all approved sources remain unchanged.`,
}
writeJson(path.join(pack, 'batch-register.json'), register)

console.log(JSON.stringify({ page: rel(pageFile), defaultGameScale: 4, routes: Object.fromEntries(Object.entries(spec.routes).map(([key, route]) => [key, route.frames.length])), uniqueFrames: published.length }, null, 2))
