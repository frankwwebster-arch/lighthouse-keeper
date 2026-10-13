#!/usr/bin/env node
/** Verify V9's single added rear-quarter frame and unchanged V7 base. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v9')
const REGISTER = path.join(PACK, 'batch-register.json')
const V7_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v7/batch-register.json')
const V8_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v8/batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-turn-side-back-v9')
const ROUTE = '/keeper-review/keeper-prime-turn-side-back-v9'
const ANGLES = [90, 98, 105, 120, 135, 150, 165, 172.5, 180]
const fail = (message: string): never => { throw new Error(`Keeper Prime Turn V9: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, V7_REGISTER, V8_REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const v7 = JSON.parse(fs.readFileSync(V7_REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-turn-side-back-2026-10-13-v9' || register.status !== 'draft-v9-single-intermediate-awaiting-visual-approval') fail('identity/status changed')
if (register.v7Base?.registerSha256 !== hash(V7_REGISTER) || register.rejectedV8?.registerSha256 !== hash(V8_REGISTER) || register.rejectedV8?.disposition !== 'rejected provenance; no V8 frame reused') fail('V7/V8 provenance changed')
if (register.rejectedV8?.feedback !== "It's now significantly more jerky, so that's not an improvement") fail('rejection feedback changed')
const frames = register.frames as Record<string, any>[]
if (frames.length !== 9 || JSON.stringify(frames.map(frame => frame.angleDegrees)) !== JSON.stringify(ANGLES)) fail('nine-frame angle plan changed')
const pngs = frames.map((frame, index) => {
  const file = path.join(ROOT, frame.file)
  if (hash(file) !== frame.sha256) fail(`F${index + 1} hash changed`)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 256 || png.height !== 320 || frame.floorY !== 316 || frame.edgeAlphaPixels !== 0) fail(`F${index + 1} geometry changed`)
  for (let x = 0; x < 256; x += 1) if (png.data[x * 4 + 3] || png.data[((319 * 256 + x) * 4) + 3]) fail(`F${index + 1} touches horizontal edge`)
  for (let y = 1; y < 319; y += 1) if (png.data[(y * 256) * 4 + 3] || png.data[(y * 256 + 255) * 4 + 3]) fail(`F${index + 1} touches vertical edge`)
  return png
})
for (let index = 0; index < 7; index += 1) if (!fs.readFileSync(path.join(ROOT, frames[index].file)).equals(fs.readFileSync(path.join(ROOT, v7.frames[index].file)))) fail(`F${index + 1} is not exact V7`)
if (!fs.readFileSync(path.join(ROOT, frames[8].file)).equals(fs.readFileSync(path.join(ROOT, v7.frames[7].file)))) fail('F9 is not exact V7 F8')
if (frames[7].source !== 'new-172.5-intermediate' || frames[7].opaqueHeight !== 297 || frames[7].opaqueBoundsExclusive[3] !== 316) fail('single midpoint declaration changed')
if (register.midpoint?.sourceSha256 !== hash(path.join(ROOT, register.midpoint.source)) || register.midpoint?.registration?.targetHeight !== 297 || register.midpoint?.registration?.axisX !== 128 || register.midpoint?.registration?.floorY !== 316 || register.midpoint?.registration?.filter !== 'Lanczos') fail('midpoint source/registration changed')
if (register.midpoint?.trouserBootMaskOverlapPixels !== 0) fail('midpoint trouser/boot masks overlap')
for (const check of Object.values(register.midpoint.componentChecks) as Record<string, any>[]) for (const [fileKey, hashKey] of [['coverageMask', 'coverageMaskSha256'], ['changedMask', 'changedMaskSha256']] as const) if (hash(path.join(ROOT, check[fileKey])) !== check[hashKey]) fail(`midpoint ${fileKey} changed`)
const earCounts = frames.slice(6).map(frame => frame.farLeftEarSkinPixels)
if (JSON.stringify(earCounts) !== '[0,18,181]' || JSON.stringify(register.earOcclusion?.farLeftEarSkinPixels) !== '[0,18,181]') fail(`rear-ear sequence changed: ${JSON.stringify(earCounts)}`)
for (let index = 1; index < frames.length; index += 1) {
  if (Math.abs(frames[index].opaqueHeight - frames[index - 1].opaqueHeight) > 2) fail(`height jumps at F${index}→F${index + 1}`)
  if (Math.abs(frames[index].alphaCentroid[0] - frames[index - 1].alphaCentroid[0]) > 3) fail(`horizontal centre jumps at F${index}→F${index + 1}`)
  if (Math.abs(frames[index].alphaCentroid[1] - frames[index - 1].alphaCentroid[1]) > 5) fail(`vertical centre jumps at F${index}→F${index + 1}`)
}
for (const direction of ['forward', 'reverse'] as const) {
  const record = register.animation[direction]
  if (hash(path.join(ROOT, record.file)) !== record.sha256 || hash(path.join(ROOT, record.sidecar)) !== record.sidecarSha256) fail(`${direction} hash changed`)
  const sidecar = JSON.parse(fs.readFileSync(path.join(ROOT, record.sidecar), 'utf8'))
  if (sidecar.frames !== 9 || sidecar.fps !== 9 || sidecar.durationSeconds !== 1) fail(`${direction} sidecar cadence changed`)
  const strip = PNG.sync.read(fs.readFileSync(path.join(ROOT, record.file)))
  if (strip.width !== 2304 || strip.height !== 320) fail(`${direction} strip geometry changed`)
  for (let frame = 0; frame < 9; frame += 1) for (let y = 0; y < 320; y += 1) {
    const expected = pngs[direction === 'forward' ? frame : 8 - frame]
    const start = ((y * strip.width) + frame * 256) * 4
    if (!strip.data.subarray(start, start + 1024).equals(expected.data.subarray(y * 1024, y * 1024 + 1024))) fail(`${direction} strip F${frame + 1} disagrees`)
  }
}
for (const flag of ['allEightV7FramesByteIdentical', 'exactlyOneNewFrame', 'everyFrameFloorY316', 'everyFrameTransparentCellEdge', 'midpointTrouserBootMasksDisjoint']) if (register.validation?.[flag] !== true) fail(`${flag} changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'finalLaneChanged', 'priorDraftsChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (register.approvalBoundary?.v9Approved !== false || register.approvalBoundary?.v8Reactivated !== false || register.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')
for (const evidence of Object.values(register.evidence) as Record<string, any>[]) if (hash(path.join(ROOT, evidence.file)) !== evidence.sha256) fail(`evidence changed: ${evidence.file}`)
const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Keeper Prime Turn V9', 'one intermediate only', 'V8 is rejected provenance', 'id="previous"', 'id="next"', 'id="oldPlayer"', 'id="comparePlayer"', '128px;height:160px']) if (!html.includes(phrase)) fail(`review omits ${phrase}`)
if (html.includes('src="assets/')) fail('review uses relative asset route')
for (let index = 1; index <= 9; index += 1) {
  const asset = fs.readdirSync(path.join(PUBLIC, 'assets')).find(name => name.startsWith(`frame${index}-`))
  if (!asset || !html.includes(`${ROUTE}/assets/${asset}`) || hash(path.join(PUBLIC, 'assets', asset)) !== frames[index - 1].sha256) fail(`public F${index} changed`)
}
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('playback script missing')
new Function(script)
console.log('Keeper Prime Turn V9 verified: exact V7 frames plus one 172.5° midpoint; 9 fps/one second; stable geometry, progressive ear, strip/sidecar/public agreement; V8 rejected; no promotion.')
