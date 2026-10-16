import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const pack = path.join(root, 'art/drafts/keeper-prime-seated-six-view-2026-10-16-v1')
const registerFile = path.join(pack, 'batch-register.json')
const geometryFile = path.join(pack, 'keeper-prime-seated-six-view-v1.json')
const pageFile = path.join(root, 'public/keeper-review/keeper-prime-seated-six-view-v1/index.html')
const approvalFile = path.join(root, 'docs/review/keeper-prime-stair-descent-v2-approval-2026-10-16.json')
const read = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message: string): never => { throw new Error(`[keeper-prime-seated-six-view-v1] ${message}`) }
for (const file of [registerFile, geometryFile, pageFile, approvalFile, path.join(pack, 'HANDOFF.md'), path.join(pack, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(root, file)}`)

const register = read(registerFile)
const geometry = read(geometryFile)
const approval = read(approvalFile)
if (register.batchId !== 'keeper-prime-seated-six-view-2026-10-16-v1' || register.status !== 'draft-seated-foundation-awaiting-frank') fail('batch identity/status changed')
if (geometry.schema !== 'lighthouse-keeper/seated-foundation@1' || geometry.status !== 'draft-awaiting-frank') fail('geometry identity/status changed')
if (approval.decision !== 'approved-with-accepted-visual-limitation' || !approval.approvalBoundary.v2ArtworkAndRouteApproved || approval.approvalBoundary.runtimePromotionPerformed || approval.approvalBoundary.productionPromotionPerformed) fail('stair descent approval boundary changed')
if (approval.futureSceneryContract.newelPosts !== 2 || !approval.futureSceneryContract.geometryMustRemain.includes('fourteen-riser')) fail('future staircase scenery/geometry contract changed')
if (geometry.cell.logical.join(',') !== '32,40' || geometry.cell.pixels.join(',') !== '256,320' || geometry.cell.density !== 8) fail('registered cell changed')
if (geometry.sharedDatums.seatPointLp.join(',') !== '16,29' || geometry.sharedDatums.seatHeightAboveFloorLp !== 11 || geometry.sharedDatums.floorOpaqueMaximumY !== 315 || geometry.sharedDatums.transparentSafetyGutterMinimumPx !== 4) fail('seat/floor datum changed')

const expected = ['front', 'rear-left', 'side-left', 'back', 'side-right', 'rear-right']
if (geometry.directions.map((x: any) => x.id).join(',') !== expected.join(',')) fail('six-view order changed')
function alphaBounds(png: PNG) {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) if (png.data[(y * png.width + x) * 4 + 3] > 0) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  return { minX, minY, maxX, maxY, width: maxX - minX + 1, height: maxY - minY + 1 }
}
const pngs = new Map<string, PNG>()
for (const direction of geometry.directions) {
  const file = path.join(root, direction.image)
  const sidecarFile = file.replace(/\.png$/, '.json')
  if (!fs.existsSync(file) || sha(file) !== direction.sha256) fail(`${direction.id} frame hash changed`)
  if (!fs.existsSync(sidecarFile)) fail(`${direction.id} sidecar missing`)
  const png = PNG.sync.read(fs.readFileSync(file)); pngs.set(direction.id, png)
  if (png.width !== 256 || png.height !== 320) fail(`${direction.id} cell is not 256x320`)
  const b = alphaBounds(png)
  if (JSON.stringify(b) !== JSON.stringify(direction.registeredBounds)) fail(`${direction.id} registered bounds changed`)
  if (b.minY !== 52 || b.maxY !== 315 || b.height !== 264) fail(`${direction.id} height/floor registration changed`)
  if (Math.abs((b.minX + b.maxX) / 2 - 127.5) > 0.5) fail(`${direction.id} horizontal centre changed`)
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) {
    if (x >= 4 && x < png.width - 4 && y >= 4 && y < png.height - 4) continue
    if (png.data[(y * png.width + x) * 4 + 3] !== 0) fail(`${direction.id} violates four-pixel transparent safety gutter`)
  }
  const sidecar = read(sidecarFile)
  if (sidecar.w !== 32 || sidecar.h !== 40 || sidecar.frames !== 1 || sidecar.density !== 8 || sidecar.anchor.join(',') !== '16,40' || sidecar.seatPoint.join(',') !== '16,29' || sidecar.startPose !== direction.pose || sidecar.endPose !== direction.pose) fail(`${direction.id} sidecar disagrees with frame/geometry`)
}
function assertExactMirror(leftId: string, rightId: string) {
  const left = pngs.get(leftId)!, right = pngs.get(rightId)!
  for (let y = 0; y < right.height; y++) for (let x = 0; x < right.width; x++) for (let channel = 0; channel < 4; channel++) {
    if (left.data[(y * left.width + x) * 4 + channel] !== right.data[(y * right.width + (right.width - 1 - x)) * 4 + channel]) fail(`${leftId} is not the exact mirror of ${rightId}`)
  }
}
assertExactMirror('side-left', 'side-right')
assertExactMirror('rear-left', 'rear-right')

for (const lane of ['authorities', 'historicalSeatedReferences', 'generatedSources']) for (const [id, record] of Object.entries(register[lane]) as any) {
  const file = path.join(root, record.file)
  if (!fs.existsSync(file) || sha(file) !== record.sha256) fail(`${lane}.${id} authority hash changed`)
}
if (register.geometry.sha256 !== sha(geometryFile) || register.evidence.contactSheet.sha256 !== sha(path.join(root, register.evidence.contactSheet.file)) || register.publicPage.sha256 !== sha(pageFile)) fail('registered evidence/page hash stale')
for (const flag of ['canonicalRawChanged', 'approvedPrimeAuthoritiesChanged', 'historicalDraftsChanged', 'finalChanged', 'runtimeChanged', 'productionChanged', 'endpointApprovalGranted', 'transitionAnimationApprovalGranted', 'promotionAllowed']) if (register.boundaries[flag] !== false) fail(`${flag} boundary changed`)
const html = fs.readFileSync(pageFile, 'utf8')
for (const phrase of ['Previous view', 'Next view', 'Exact game raster', 'seat datum · y 29 lp · 11 lp above floor', 'All six registered views', 'Promise.all(unique.map(preload))', 'Approving these locks the targets']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (html.indexOf('Promise.all(unique.map(preload))') > html.indexOf('controls.forEach(x=>x.disabled=false)')) fail('controls unlock before complete preload/decode')
console.log(JSON.stringify({ ok: true, views: expected, sharedAlphaHeight: 264, seatHeightLp: 11, exactMirrors: ['side-left/right', 'rear-left/right'], productionChanged: false }, null, 2))

