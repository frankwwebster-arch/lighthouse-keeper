import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const v2Pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v2')
const pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v3')
const v2SpecFile = path.join(v2Pack, 'keeper-prime-ladder-transitions-v2.json')
const v2RegisterFile = path.join(v2Pack, 'batch-register.json')
const v2PageFile = path.join(root, 'public/keeper-review/keeper-prime-ladder-transitions-v2/index.html')
const specFile = path.join(pack, 'keeper-prime-ladder-transitions-v3.json')
const registerFile = path.join(pack, 'batch-register.json')
const pageFile = path.join(root, 'public/keeper-review/keeper-prime-ladder-transitions-v3/index.html')
const read = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message: string): never => { throw new Error(`[keeper-prime-ladder-transitions-v3] ${message}`) }

for (const file of [v2SpecFile, v2RegisterFile, v2PageFile, specFile, registerFile, pageFile]) if (!fs.existsSync(file)) fail(`missing ${path.relative(root, file)}`)
const v2 = read(v2SpecFile)
const spec = read(specFile)
const register = read(registerFile)
if (spec.set !== 'keeper-prime-ladder-transitions-v3' || spec.status !== 'draft-awaiting-visual-review') fail('candidate identity changed')
if (spec.opacity.threshold !== 128 || spec.layering.keeperAlphaMode !== 'binary-threshold-128-after-registration' || spec.layering.ladderPixelsSuppressed !== false) fail('opacity/layering contract changed')
if (JSON.stringify(spec.geometry) !== JSON.stringify(v2.geometry) || JSON.stringify(spec.registration) !== JSON.stringify(v2.registration) || JSON.stringify(spec.timing) !== JSON.stringify(v2.timing)) fail('V2 geometry, registration or timing changed')

const clean = (frame: any) => { const value = { ...frame }; delete value.src; delete value.ladderOcclusion; return value }
for (const [routeId, route] of Object.entries<any>(spec.routes)) {
  const prior = v2.routes[routeId]
  if (!prior || route.frames.length !== prior.frames.length) fail(`${routeId} route length changed`)
  for (let index = 0; index < route.frames.length; index++) {
    const frame = route.frames[index]
    if (JSON.stringify(clean(frame)) !== JSON.stringify(clean(prior.frames[index]))) fail(`${routeId} F${index + 1} order/root/timing changed`)
    if ('ladderOcclusion' in frame) fail(`${routeId} F${index + 1} retained V2 rung suppression`)
    if (!frame.src.startsWith('/keeper-review/keeper-prime-ladder-transitions-v3/assets/')) fail(`${routeId} F${index + 1} has stale asset prefix`)
  }
}

for (const [key, authority] of Object.entries<any>(register.authorities)) {
  const file = path.join(root, authority.file)
  if (!fs.existsSync(file) || sha(file) !== authority.sha256) fail(`${key} authority changed`)
}
if (register.alphaNormalization.length !== 29 || register.publishedAssets.length !== 29) fail('unique frame inventory changed')
for (const record of register.alphaNormalization) {
  const sourceFile = path.join(root, record.source)
  const draftFile = path.join(root, record.draft)
  if (!fs.existsSync(sourceFile) || sha(sourceFile) !== record.sourceSha256) fail(`source changed: ${record.source}`)
  if (!fs.existsSync(draftFile) || sha(draftFile) !== record.draftSha256) fail(`draft changed: ${record.draft}`)
  const source = PNG.sync.read(fs.readFileSync(sourceFile))
  const draft = PNG.sync.read(fs.readFileSync(draftFile))
  if (source.width !== draft.width || source.height !== draft.height) fail(`cell geometry changed: ${record.draft}`)
  let retainedRgbChanges = 0
  let edgeAlpha = 0
  for (let offset = 0; offset < draft.data.length; offset += 4) {
    const expected = source.data[offset + 3] >= 128 ? 255 : 0
    if (draft.data[offset + 3] !== expected) fail(`non-binary or wrong alpha: ${record.draft}`)
    if (expected === 255) for (let channel = 0; channel < 3; channel++) retainedRgbChanges += Number(draft.data[offset + channel] !== source.data[offset + channel])
  }
  for (let x = 0; x < draft.width; x++) edgeAlpha += Number(draft.data[x * 4 + 3] > 0) + Number(draft.data[((draft.height - 1) * draft.width + x) * 4 + 3] > 0)
  for (let y = 1; y < draft.height - 1; y++) edgeAlpha += Number(draft.data[y * draft.width * 4 + 3] > 0) + Number(draft.data[(y * draft.width + draft.width - 1) * 4 + 3] > 0)
  if (retainedRgbChanges !== 0 || record.retainedRgbChangedPixels !== 0) fail(`retained RGB changed: ${record.draft}`)
  if (edgeAlpha !== 0) fail(`opaque cell edge: ${record.draft}`)
}
for (const entry of register.publishedAssets) {
  const file = path.join(root, entry.published)
  if (!fs.existsSync(file) || sha(file) !== entry.draftSha256) fail(`published/draft mismatch: ${entry.published}`)
}
if (!register.changes.v2RungOccluderRemoved || register.changes.ladderPixelsSuppressed !== false || register.changes.keeperRgbChanged !== false || register.changes.timingChangedFromV2 !== false) fail('V3 scope widened')
if (register.validation.productionChanged || register.validation.runtimeChanged || register.validation.finalChanged) fail('promotion boundary changed')
if (register.approvalBoundary.candidateApproved || register.approvalBoundary.productionPromotionAllowed) fail('candidate promoted without approval')

const html = fs.readFileSync(pageFile, 'utf8')
for (const required of ['Keeper Prime ladder transitions V3', 'Opaque Keeper', 'Complete ladder', 'zero suppressed rung pixels', 'Promise.all(unique.map(preload))', '← Frame', 'Frame →']) if (!html.includes(required)) fail(`review contract missing: ${required}`)
for (const forbidden of ['.rungOccluder', "frame.ladderOcclusion==='central-body'"]) if (html.includes(forbidden)) fail(`V2 ladder suppression remains: ${forbidden}`)
const urls = new Set(Object.values<any>(spec.routes).flatMap((route: any) => route.frames.map((frame: any) => frame.src)))
if (urls.size !== 29) fail(`unexpected unique frame count: ${urls.size}`)

console.log(JSON.stringify({
  ok: true,
  uniqueFrames: urls.size,
  alphaThreshold: 128,
  keeperRgbChanged: false,
  ladderPixelsSuppressed: false,
  timingChangedFromV2: false,
  productionChanged: false,
}, null, 2))
