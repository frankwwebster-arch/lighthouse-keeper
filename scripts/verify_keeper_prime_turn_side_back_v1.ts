#!/usr/bin/env node
/** Verify the reversible smooth Keeper Prime side-right ↔ back Turn V1 draft. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-turn-side-back-v1')
const SIDE = path.join(ROOT, 'art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png')
const BACK = path.join(ROOT, 'art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/drafts/keeper_prime_master-neutral-standing-back_f1.png')
const TURN_APPROVAL = path.join(ROOT, 'art/drafts/keeper-prime-turn-front-side-2026-10-13-v2/batch-register.json')
const TURN_APPROVAL_PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-turn-front-side-v2/index.html')
const fail = (message: string): never => { throw new Error(`Keeper Prime side ↔ back Turn V1: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, SIDE, BACK, TURN_APPROVAL, TURN_APPROVAL_PAGE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}

const approval = JSON.parse(fs.readFileSync(TURN_APPROVAL, 'utf8')) as Record<string, any>
if (approval.status !== 'approved-front-side-turn-artwork-authority' || approval.approvalBoundary?.authorizesSideBackTurnV1Draft !== true || approval.approvalBoundary?.productionPromotionAllowed !== false) fail('front ↔ side approval gate changed')
if (approval.approval?.wording !== 'it is ever so slightly jumpy at about 45deg in the turn but I am happy') fail('front ↔ side approval wording changed')
const approvalHtml = fs.readFileSync(TURN_APPROVAL_PAGE, 'utf8')
for (const phrase of ['Approved artwork authority', 'it is ever so slightly jumpy at about 45deg in the turn but I am happy', 'Accepted minor limitation', 'not being described as a perfect transition']) if (!approvalHtml.includes(phrase)) fail(`front ↔ side approval page omits ${phrase}`)

const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-turn-side-back-2026-10-13-v1' || register.status !== 'draft-side-back-turn-v1-awaiting-visual-approval') fail('batch identity/status changed')
if (register.authorities?.frontSideTurnApproval?.sha256 !== sha256(TURN_APPROVAL)) fail('front ↔ side approval provenance changed')
for (const key of ['sideRight', 'back', 'rig']) {
  const authority = register.authorities?.[key]
  if (!authority || sha256(path.join(ROOT, authority.file)) !== authority.sha256) fail(`${key} authority changed`)
  if (authority.register && sha256(path.join(ROOT, authority.register)) !== authority.registerSha256) fail(`${key} authority register changed`)
}

const expectedSourceHashes: Record<number, string> = {
  98: '02022fed61f97845666efcbec7a0af532436faca6fa1841144cfe7b91feec1c1',
  105: 'e619af1381e02792b49847c150c94550f1d11ddc726657817b0f23811390963b',
  120: 'd6b0819b48f69bac89f55eaa3888a4eabdf570f512e9eae19d3193c34a754a92',
  135: '886f78fed0dfb3ecd5a1f058b0aa8c7dd2d463d43a773ff3796b1b86591c73f1',
  150: 'ab82c72af84ac262825805bc6d3b033f3ea6e5cf54b9157dd145cc94ed411609',
  165: '9540a89ed35bcdeeb74b619f9bfa6e20f3d5b74af534ee08eb7219e6f982ff7b',
}
if (register.generation?.creativePixelWarp !== false || register.generation?.lowAlphaCleanupThreshold !== 8) fail('generation/registration boundary changed')
for (const source of register.generation.rawSources as Record<string, any>[]) {
  if (source.sha256 !== expectedSourceHashes[source.angleDegrees] || sha256(path.join(ROOT, source.file)) !== source.sha256) fail(`generated ${source.angleDegrees}° source changed`)
}
for (const clean of register.generation.cleanSources as Record<string, any>[]) if (sha256(path.join(ROOT, clean.file)) !== clean.sha256) fail(`clean ${clean.angleDegrees}° source changed`)
if ((register.generation.rejectedSources as Record<string, any>[]).length !== 2) fail('rejected provenance changed')
for (const rejected of register.generation.rejectedSources as Record<string, any>[]) if (sha256(path.join(ROOT, rejected.file)) !== rejected.sha256) fail(`rejected ${rejected.angleDegrees}° provenance changed`)

const frames = register.frames as Record<string, any>[]
if (JSON.stringify(frames.map((frame) => frame.angleDegrees)) !== '[90,98,105,120,135,150,165,180]') fail('turn angle progression changed')
if (frames.length !== 8 || register.animation?.fps !== 8 || register.animation?.durationSeconds !== 1) fail('turn timing changed')
const framePngs = frames.map((frame) => PNG.sync.read(fs.readFileSync(path.join(ROOT, frame.file))))
for (const [index, frame] of frames.entries()) {
  const local = path.join(ROOT, frame.file)
  if (sha256(local) !== frame.sha256) fail(`frame ${index + 1} hash changed`)
  const png = framePngs[index]
  if (png.width !== 256 || png.height !== 320) fail(`frame ${index + 1} geometry changed`)
  if (frame.opaqueBoundsExclusive[1] !== 18 || frame.opaqueBoundsExclusive[3] !== 316 || frame.opaqueHeight !== 298) fail(`frame ${index + 1} standing geometry changed`)
  if (frame.edgeAlphaPixels !== 0) fail(`frame ${index + 1} touches a cell edge`)
  for (let x = 0; x < png.width; x += 1) if (png.data[(x * 4) + 3] || png.data[(((png.height - 1) * png.width + x) * 4) + 3]) fail(`frame ${index + 1} has top/bottom edge alpha`)
  for (let y = 1; y < png.height - 1; y += 1) if (png.data[((y * png.width) * 4) + 3] || png.data[((y * png.width + png.width - 1) * 4) + 3]) fail(`frame ${index + 1} has side-edge alpha`)
  if (frame.registration && (frame.registration.creativePixelWarp !== false || frame.registration.filter !== 'Lanczos' || frame.registration.registeredSize[1] !== 298)) fail(`frame ${index + 1} registration changed`)
}
if (!fs.readFileSync(path.join(ROOT, frames[0].file)).equals(fs.readFileSync(SIDE))) fail('side endpoint is not byte-identical')
if (!fs.readFileSync(path.join(ROOT, frames.at(-1)!.file)).equals(fs.readFileSync(BACK))) fail('back endpoint is not byte-identical')

for (const direction of ['forward', 'reverse'] as const) {
  const record = register.animation[direction]
  const stripPath = path.join(ROOT, record.file)
  if (sha256(stripPath) !== record.sha256) fail(`${direction} strip hash changed`)
  const strip = PNG.sync.read(fs.readFileSync(stripPath))
  if (strip.width !== 2048 || strip.height !== 320) fail(`${direction} strip geometry changed`)
  for (let frame = 0; frame < 8; frame += 1) {
    const expected = framePngs[direction === 'forward' ? frame : 7 - frame]
    for (let y = 0; y < 320; y += 1) {
      const actualStart = ((y * strip.width) + frame * 256) * 4
      const expectedStart = y * 256 * 4
      if (!strip.data.subarray(actualStart, actualStart + 1024).equals(expected.data.subarray(expectedStart, expectedStart + 1024))) fail(`${direction} frame ${frame + 1} disagrees with source frame`)
    }
  }
  const sidecarPath = path.join(ROOT, record.sidecar)
  if (sha256(sidecarPath) !== record.sidecarSha256) fail(`${direction} sidecar changed`)
  const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8'))
  for (const [key, value] of Object.entries({ w: 32, h: 40, density: 8, frames: 8, fps: 8 })) if (sidecar[key] !== value) fail(`${direction} sidecar ${key} changed`)
  if (sidecar.sha256 !== record.sha256) fail(`${direction} strip/sidecar hash disagrees`)
}

for (const seam of register.continuity as Record<string, any>[]) {
  if (seam.opaqueHeightDelta !== 0 || Math.abs(seam.opaqueWidthDelta) > 19 || Math.abs(seam.headAlphaCentroidDelta[0]) > 2.5 || Math.abs(seam.headAlphaCentroidDelta[1]) > 1) fail(`continuity bound failed at ${seam.fromFrame}→${seam.toFrame}`)
}
for (const flag of ['sideEndpointByteIdentical', 'backEndpointByteIdentical', 'reverseIsExactFrameOrderReverse', 'everyFrameTransparentCellEdge', 'uniformRegistrationOnly']) if (register.validation?.[flag] !== true) fail(`${flag} validation changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'otherAnimationDraftsChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (register.approvalBoundary?.sideRightArtworkApproved !== true || register.approvalBoundary?.backArtworkApproved !== true || register.approvalBoundary?.frontSideTurnV1Approved !== true || register.approvalBoundary?.sideBackTurnV1Approved !== false || register.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')

for (const evidence of Object.values(register.evidence) as Record<string, any>[]) if (!fs.existsSync(path.join(ROOT, evidence.file)) || sha256(path.join(ROOT, evidence.file)) !== evidence.sha256) fail(`evidence missing or changed: ${evidence.file}`)
for (const item of [...frames, register.animation.forward, register.animation.reverse, ...Object.values(register.evidence) as Record<string, any>[]]) {
  const publicAsset = fs.readdirSync(path.join(PUBLIC, 'assets')).find((name) => name.includes(item.sha256.slice(0, 16)))
  if (!publicAsset || sha256(path.join(PUBLIC, 'assets', publicAsset)) !== item.sha256) fail(`public asset missing for ${item.file}`)
}
const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Keeper Prime Turn V1 · side-right ↔ back', 'Eight-pose smooth draft · awaiting visual approval', 'Side → back', 'Back → side', 'Loop both', 'Route context', 'Nothing has entered Final or production', 'side-right and back endpoints are approved authorities', 'Height remains 298px']) if (!html.includes(phrase)) fail(`public review omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('public playback script missing')
new Function(script)

console.log('Keeper Prime side ↔ back Turn V1 verified: 8 smooth poses, exact approved endpoints, exact reversible strips, 298px height, transparent gutters, bounded continuity and no production promotion.')
