import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const v3Pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v3')
const pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v4')
const v3SpecFile = path.join(v3Pack, 'keeper-prime-ladder-transitions-v3.json')
const v3RegisterFile = path.join(v3Pack, 'batch-register.json')
const v3PageFile = path.join(root, 'public/keeper-review/keeper-prime-ladder-transitions-v3/index.html')
const specFile = path.join(pack, 'keeper-prime-ladder-transitions-v4.json')
const registerFile = path.join(pack, 'batch-register.json')
const pageFile = path.join(root, 'public/keeper-review/keeper-prime-ladder-transitions-v4/index.html')
const read = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message: string): never => { throw new Error(`[keeper-prime-ladder-transitions-v4] ${message}`) }

for (const file of [v3SpecFile, v3RegisterFile, v3PageFile, specFile, registerFile, pageFile]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(root, file)}`)
}
const v3 = read(v3SpecFile)
const spec = read(specFile)
const register = read(registerFile)
if (spec.set !== 'keeper-prime-ladder-transitions-v4' || spec.status !== 'draft-awaiting-visual-review') fail('candidate identity changed')
if (spec.opacity.solidPaintFloor !== 240 || spec.layering.keeperAlphaMode !== 'solid-paint-floor-240-with-original-antialiased-fringe') fail('opacity contract changed')
if (!spec.layering.persistentCompositor || spec.layering.ladderPixelsSuppressed !== false) fail('layering/compositor contract changed')
if (!spec.delivery.allUniqueFramesDecodedBeforePlayback || !spec.delivery.allUniqueFramesMountedBeforePlayback || spec.delivery.architectureRebuiltDuringPlayback) fail('stable delivery contract changed')
if (JSON.stringify(spec.geometry) !== JSON.stringify(v3.geometry) || JSON.stringify(spec.registration) !== JSON.stringify(v3.registration) || JSON.stringify(spec.timing) !== JSON.stringify(v3.timing)) fail('V3 geometry, registration or timing changed')

const clean = (frame: any) => { const value = { ...frame }; delete value.src; return value }
for (const [routeId, route] of Object.entries<any>(spec.routes)) {
  const prior = v3.routes[routeId]
  if (!prior || route.frames.length !== prior.frames.length) fail(`${routeId} route length changed`)
  for (let index = 0; index < route.frames.length; index++) {
    const frame = route.frames[index]
    if (JSON.stringify(clean(frame)) !== JSON.stringify(clean(prior.frames[index]))) fail(`${routeId} F${index + 1} order/root/timing changed`)
    if (!frame.src.startsWith('/keeper-review/keeper-prime-ladder-transitions-v4/assets/')) fail(`${routeId} F${index + 1} has stale asset prefix`)
  }
}

for (const [key, authority] of Object.entries<any>(register.authorities)) {
  const file = path.join(root, authority.file)
  if (!fs.existsSync(file) || sha(file) !== authority.sha256) fail(`${key} authority changed`)
}
if (register.alphaNormalization.length !== 29 || register.publishedAssets.length !== 29) fail('unique frame inventory changed')
let totalFringe = 0
for (const record of register.alphaNormalization) {
  const sourceFile = path.join(root, record.source)
  const draftFile = path.join(root, record.draft)
  if (!fs.existsSync(sourceFile) || sha(sourceFile) !== record.sourceSha256) fail(`source changed: ${record.source}`)
  if (!fs.existsSync(draftFile) || sha(draftFile) !== record.draftSha256) fail(`draft changed: ${record.draft}`)
  const source = PNG.sync.read(fs.readFileSync(sourceFile))
  const draft = PNG.sync.read(fs.readFileSync(draftFile))
  if (source.width !== draft.width || source.height !== draft.height) fail(`cell geometry changed: ${record.draft}`)
  let hardened = 0
  let fringe = 0
  let edgeAlpha = 0
  for (let offset = 0; offset < draft.data.length; offset += 4) {
    const alpha = source.data[offset + 3]
    const expected = alpha >= 240 ? 255 : alpha
    if (draft.data[offset + 3] !== expected) fail(`wrong alpha transform: ${record.draft}`)
    for (let channel = 0; channel < 3; channel++) if (draft.data[offset + channel] !== source.data[offset + channel]) fail(`RGB changed: ${record.draft}`)
    hardened += Number(alpha >= 240 && alpha !== 255)
    fringe += Number(alpha > 0 && alpha < 240)
  }
  for (let x = 0; x < draft.width; x++) edgeAlpha += Number(draft.data[x * 4 + 3] > 0) + Number(draft.data[((draft.height - 1) * draft.width + x) * 4 + 3] > 0)
  for (let y = 1; y < draft.height - 1; y++) edgeAlpha += Number(draft.data[y * draft.width * 4 + 3] > 0) + Number(draft.data[(y * draft.width + draft.width - 1) * 4 + 3] > 0)
  if (hardened !== record.hardenedPixels || fringe !== record.preservedFringePixels || record.rgbChangedPixels !== 0) fail(`alpha audit drift: ${record.draft}`)
  if (fringe < 100) fail(`smooth source fringe was not retained: ${record.draft}`)
  if (edgeAlpha !== 0) fail(`opaque cell edge: ${record.draft}`)
  totalFringe += fringe
}
for (const entry of register.publishedAssets) {
  const file = path.join(root, entry.published)
  if (!fs.existsSync(file) || sha(file) !== entry.draftSha256) fail(`published/draft mismatch: ${entry.published}`)
}
if (!register.changes.v3BinaryEdgeRejected || !register.changes.sourceFringePreserved || !register.changes.persistentCompositor) fail('V4 correction scope missing')
if (register.changes.ladderPixelsSuppressed !== false || register.changes.keeperRgbChanged !== false || register.changes.timingChangedFromV3 !== false) fail('V4 scope widened')
if (register.validation.productionChanged || register.validation.runtimeChanged || register.validation.finalChanged) fail('promotion boundary changed')
if (register.approvalBoundary.candidateApproved || register.approvalBoundary.productionPromotionAllowed) fail('candidate promoted without approval')

const html = fs.readFileSync(pageFile, 'utf8')
for (const required of ['Keeper Prime ladder transitions V4', 'Persistent compositor', 'prepareStage(stage)', 'decoded.get(src).cloneNode()', 'requestAnimationFrame(()=>requestAnimationFrame', 'All ${unique.length} unique frames decoded and persistently mounted', '← Frame', 'Frame →']) {
  if (!html.includes(required)) fail(`review contract missing: ${required}`)
}
for (const forbidden of ["function architecture(world,scale,frame){world.innerHTML=''", "function renderStage(stage){const scale=Number(stage.dataset.scale),world=stage.querySelector('.world'),frame=active()[index];architecture", '.rungOccluder', "frame.ladderOcclusion==='central-body'"]) {
  if (html.includes(forbidden)) fail(`unstable or rejected compositor remains: ${forbidden}`)
}
const prepareStart = html.indexOf('function prepareStage(stage)')
const renderStart = html.indexOf('function renderStage(stage)')
const renderEnd = html.indexOf('function render()', renderStart)
if (prepareStart < 0 || renderStart < 0 || renderEnd < 0) fail('stable compositor functions missing')
const renderBody = html.slice(renderStart, renderEnd)
for (const forbidden of ['createElement', 'append(', 'appendChild', 'replaceChildren', '.src=']) if (renderBody.includes(forbidden)) fail(`playback mutates DOM/assets: ${forbidden}`)
const urls = new Set(Object.values<any>(spec.routes).flatMap((route: any) => route.frames.map((frame: any) => frame.src)))
if (urls.size !== 29) fail(`unexpected unique frame count: ${urls.size}`)

console.log(JSON.stringify({
  ok: true,
  uniqueFrames: urls.size,
  solidPaintFloor: 240,
  preservedFringePixels: totalFringe,
  keeperRgbChanged: false,
  persistentCompositor: true,
  ladderPixelsSuppressed: false,
  timingChangedFromV3: false,
  productionChanged: false,
}, null, 2))
