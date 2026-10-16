import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const v1Pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v1')
const pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v2')
const v1SpecFile = path.join(v1Pack, 'keeper-prime-ladder-transitions-v1.json')
const v1RegisterFile = path.join(v1Pack, 'batch-register.json')
const v1PageFile = path.join(root, 'public/keeper-review/keeper-prime-ladder-transitions-v1/index.html')
const specFile = path.join(pack, 'keeper-prime-ladder-transitions-v2.json')
const registerFile = path.join(pack, 'batch-register.json')
const pageFile = path.join(root, 'public/keeper-review/keeper-prime-ladder-transitions-v2/index.html')
const read = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message: string): never => { throw new Error(`[keeper-prime-ladder-transitions-v2] ${message}`) }

for (const file of [v1SpecFile, v1RegisterFile, v1PageFile, specFile, registerFile, pageFile]) if (!fs.existsSync(file)) fail(`missing ${path.relative(root, file)}`)
const v1 = read(v1SpecFile)
const spec = read(specFile)
const register = read(registerFile)

if (spec.set !== 'keeper-prime-ladder-transitions-v2' || spec.status !== 'draft-awaiting-visual-review') fail('candidate identity changed')
if (spec.timing.turnFrameDurationMs !== 50 || spec.timing.climbFrameDurationMs !== 150) fail('reviewed timing changed')
if (spec.layering.centralRungOccluderWidthLp !== 12 || spec.layering.centralRungOccluderHeightLp !== 38) fail('occlusion geometry changed')
if (JSON.stringify(spec.geometry) !== JSON.stringify(v1.geometry) || JSON.stringify(spec.registration) !== JSON.stringify(v1.registration)) fail('V1 geometry or registration changed')

const ladderAssets = new Set(['contactA', 'passingA', 'contactB', 'passingB', 'mount', 'dismountRight', 'dismountLanded'])
const clean = (frame: any) => {
  const value = { ...frame }
  delete value.src
  delete value.durationMs
  delete value.ladderOcclusion
  return value
}
for (const [routeId, route] of Object.entries<any>(spec.routes)) {
  const prior = v1.routes[routeId]
  if (!prior || route.frames.length !== prior.frames.length) fail(`${routeId} route length changed`)
  for (let index = 0; index < route.frames.length; index++) {
    const frame = route.frames[index]
    const old = prior.frames[index]
    if (JSON.stringify(clean(frame)) !== JSON.stringify(clean(old))) fail(`${routeId} F${index + 1} artwork/order/root changed`)
    const expectedDuration = frame.sourceFrame.startsWith('turn') ? 50 : ladderAssets.has(frame.sourceFrame) ? 150 : old.durationMs
    if (frame.durationMs !== expectedDuration) fail(`${routeId} F${index + 1} has wrong timing`)
    const shouldOcclude = Math.abs(frame.xLp - 104) <= 7 && (frame.sourceFrame.startsWith('turn') || frame.sourceFrame === 'back' || ladderAssets.has(frame.sourceFrame))
    if ((frame.ladderOcclusion === 'central-body') !== shouldOcclude) fail(`${routeId} F${index + 1} has wrong ladder layering state`)
    if (!frame.src.startsWith('/keeper-review/keeper-prime-ladder-transitions-v2/assets/')) fail(`${routeId} F${index + 1} has stale asset prefix`)
  }
}

for (const [key, authority] of Object.entries<any>(register.authorities)) {
  const file = path.join(root, authority.file)
  if (!fs.existsSync(file) || sha(file) !== authority.sha256) fail(`${key} authority changed`)
}
const v1Register = read(v1RegisterFile)
const v1Hashes = new Map(v1Register.publishedAssets.map((entry: any) => [path.basename(entry.published), entry.sourceSha256]))
if (register.publishedAssets.length !== v1Register.publishedAssets.length) fail('published asset count changed')
for (const entry of register.publishedAssets) {
  const expected = v1Hashes.get(path.basename(entry.published))
  const file = path.join(root, entry.published)
  if (!expected || expected !== entry.sourceSha256 || !fs.existsSync(file) || sha(file) !== expected) fail(`V1 artwork byte changed: ${entry.published}`)
}
if (register.changes.artworkPixelsChanged !== false || register.changes.geometryChanged !== false || register.changes.rungContactChanged !== false) fail('V2 scope widened')
if (!register.changes.centralRungOcclusionLayerAdded) fail('rung occlusion correction missing')
if (register.validation.productionChanged || register.validation.runtimeChanged || register.validation.finalChanged) fail('promotion boundary changed')
if (register.approvalBoundary.candidateApproved || register.approvalBoundary.productionPromotionAllowed) fail('candidate promoted without approval')

const html = fs.readFileSync(pageFile, 'utf8')
for (const required of ['Keeper Prime ladder transitions V2', '20 fps', '6.67 fps', '.rungOccluder', "frame.ladderOcclusion==='central-body'", 'Promise.all(unique.map(preload))', '← Frame', 'Frame →']) if (!html.includes(required)) fail(`review contract missing: ${required}`)
const urls = new Set(Object.values<any>(spec.routes).flatMap((route: any) => route.frames.map((frame: any) => frame.src)))
if (urls.size !== 29) fail(`unexpected unique frame count: ${urls.size}`)

console.log(JSON.stringify({
  ok: true,
  routes: Object.fromEntries(Object.entries<any>(spec.routes).map(([key, route]) => [key, route.frames.length])),
  uniqueFrames: urls.size,
  turnFrameDurationMs: 50,
  climbFrameDurationMs: 150,
  artworkPixelsChanged: false,
  productionChanged: false,
}, null, 2))
