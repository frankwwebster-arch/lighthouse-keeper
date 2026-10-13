#!/usr/bin/env node
/** Verify the reversible smooth Keeper Prime front ↔ side Turn V1 draft. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-turn-front-side-2026-10-13-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const APPROVAL = path.join(ROOT, 'art/drafts/keeper-prime-side-right-rigged-2026-10-13-v2/batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-turn-front-side-v1')
const APPROVAL_PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-side-right-rigged-v2/index.html')
const FRONT = path.join(ROOT, 'art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png')
const SIDE = path.join(ROOT, 'art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png')
const fail = (message: string): never => { throw new Error(`Keeper Prime Turn V1: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, APPROVAL, APPROVAL_PAGE, FRONT, SIDE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const approval = JSON.parse(fs.readFileSync(APPROVAL, 'utf8')) as Record<string, any>
if (approval.status !== 'approved-side-right-artwork-authority' || approval.approval?.wording !== 'Approve side-right V1 and build Turn V1.' || approval.approvalBoundary?.authorizesTurnV1Draft !== true || approval.approvalBoundary?.productionPromotionAllowed !== false) fail('Side-right V1 approval gate changed')
const approvalHtml = fs.readFileSync(APPROVAL_PAGE, 'utf8')
for (const phrase of ['Approved artwork authority', 'Approve side-right V1 and build Turn V1.', 'It does not approve the turn before review']) if (!approvalHtml.includes(phrase)) fail(`side approval page omits ${phrase}`)

const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-turn-front-side-2026-10-13-v1' || register.status !== 'draft-turn-v1-awaiting-visual-approval') fail('batch identity/status changed')
if (register.authorities?.sideRight?.approvalSha256 !== sha256(APPROVAL) || register.authorities?.sideRight?.approvalWording !== approval.approval.wording) fail('side approval provenance changed')
for (const key of ['front', 'sideRight', 'rig']) {
  const authority = register.authorities?.[key]
  if (!authority || sha256(path.join(ROOT, authority.file)) !== authority.sha256) fail(`${key} authority changed`)
  if (authority.register && sha256(path.join(ROOT, authority.register)) !== authority.registerSha256) fail(`${key} authority register changed`)
}

const expectedSourceHashes: Record<number, string> = {
  8: '29f23079bfe63ddab7d50add9b3e5358f58ab29cad84280450c1e59a3ca7fbb9',
  15: '894869db11e0fb84fa84870f478c4f2c8ae110d1f357f0c62bd013498855bae4',
  30: 'd6c76526c9681500c86f9e9f179ccdeb08344bece58344379c58d5425c58a3b4',
  45: '15d497d1ab4d174568c3015d31d7f91f243ef25dd088b918b3da08171cc13339',
  60: '2ef10d4cd629608e94425958ce217892ddb1673e4a60e8726fa8e7b4b4329458',
  75: '63ef7693361c62adc6577ea0fc2557747ed720edc0f5bc91d2c3fc0a70feade0',
}
if (register.generation?.creativePixelWarp !== false || register.generation?.lowAlphaCleanupThreshold !== 8) fail('generation/registration boundary changed')
for (const source of register.generation.rawSources as Record<string, any>[]) if (source.sha256 !== expectedSourceHashes[source.angleDegrees] || sha256(path.join(ROOT, source.file)) !== source.sha256) fail(`generated ${source.angleDegrees}° source changed`)
for (const clean of register.generation.cleanSources as Record<string, any>[]) if (sha256(path.join(ROOT, clean.file)) !== clean.sha256) fail(`clean ${clean.angleDegrees}° source changed`)

const frames = register.frames as Record<string, any>[]
if (JSON.stringify(frames.map((frame) => frame.angleDegrees)) !== '[0,8,15,30,45,60,75,90]') fail('turn angle progression changed')
if (frames.length !== 8 || register.animation?.fps !== 8 || register.animation?.durationSeconds !== 1) fail('turn timing changed')
const framePngs = frames.map((frame) => PNG.sync.read(fs.readFileSync(path.join(ROOT, frame.file))))
for (const [index, frame] of frames.entries()) {
  const local = path.join(ROOT, frame.file)
  if (sha256(local) !== frame.sha256) fail(`frame ${index + 1} hash changed`)
  const png = framePngs[index]
  if (png.width !== 256 || png.height !== 320) fail(`frame ${index + 1} geometry changed`)
  if (JSON.stringify(frame.opaqueBoundsExclusive.slice(1, 4).filter((_: number, i: number) => i !== 1)) !== '[18,316]' || frame.opaqueHeight !== 298) fail(`frame ${index + 1} standing height changed`)
  if (frame.edgeAlphaPixels !== 0) fail(`frame ${index + 1} touches a cell edge`)
  for (let x = 0; x < png.width; x += 1) if (png.data[(x * 4) + 3] || png.data[(((png.height - 1) * png.width + x) * 4) + 3]) fail(`frame ${index + 1} has top/bottom edge alpha`)
  for (let y = 1; y < png.height - 1; y += 1) if (png.data[((y * png.width) * 4) + 3] || png.data[((y * png.width + png.width - 1) * 4) + 3]) fail(`frame ${index + 1} has side-edge alpha`)
  if (frame.registration && (frame.registration.creativePixelWarp !== false || frame.registration.filter !== 'Lanczos' || frame.registration.registeredSize[1] !== 298)) fail(`frame ${index + 1} registration changed`)
}
if (!fs.readFileSync(path.join(ROOT, frames[0].file)).equals(fs.readFileSync(FRONT))) fail('front endpoint is not byte-identical')
if (!fs.readFileSync(path.join(ROOT, frames.at(-1)!.file)).equals(fs.readFileSync(SIDE))) fail('side endpoint is not byte-identical')

const forwardPath = path.join(ROOT, register.animation.forward.file)
const reversePath = path.join(ROOT, register.animation.reverse.file)
for (const [direction, file, expectedHash] of [['forward', forwardPath, '8abdcde40f587f40b9b9f1487f06db7ba63d281409a1165b630671c58c7db66d'], ['reverse', reversePath, '3842b22f0e40bfc237d76ec6dec223c78d5695a5f6ccb82e890e56fb83b578fa']] as const) {
  if (sha256(file) !== expectedHash || register.animation[direction].sha256 !== expectedHash) fail(`${direction} strip changed`)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 2048 || png.height !== 320) fail(`${direction} strip geometry changed`)
  for (let frame = 0; frame < 8; frame += 1) {
    const expected = framePngs[direction === 'forward' ? frame : 7 - frame]
    for (let y = 0; y < 320; y += 1) {
      const actualStart = ((y * png.width) + frame * 256) * 4
      const expectedStart = y * 256 * 4
      if (!png.data.subarray(actualStart, actualStart + 1024).equals(expected.data.subarray(expectedStart, expectedStart + 1024))) fail(`${direction} frame ${frame + 1} disagrees with source frame`)
    }
  }
  const sidecarPath = path.join(ROOT, register.animation[direction].sidecar)
  if (sha256(sidecarPath) !== register.animation[direction].sidecarSha256) fail(`${direction} sidecar changed`)
  const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8'))
  for (const [key, value] of Object.entries({w: 32, h: 40, density: 8, frames: 8, fps: 8})) if (sidecar[key] !== value) fail(`${direction} sidecar ${key} changed`)
  if (sidecar.sha256 !== expectedHash) fail(`${direction} strip/sidecar hash disagrees`)
}

for (const seam of register.continuity as Record<string, any>[]) {
  if (seam.opaqueHeightDelta !== 0 || Math.abs(seam.opaqueWidthDelta) > 13 || Math.abs(seam.headAlphaCentroidDelta[0]) > 2 || Math.abs(seam.headAlphaCentroidDelta[1]) > 1) fail(`continuity bound failed at ${seam.fromFrame}→${seam.toFrame}`)
}
for (const flag of ['frontEndpointByteIdentical', 'sideEndpointByteIdentical', 'reverseIsExactFrameOrderReverse', 'everyFrameTransparentCellEdge', 'uniformRegistrationOnly']) if (register.validation?.[flag] !== true) fail(`${flag} validation changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'otherAnimationDraftsChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (register.approvalBoundary?.sideRightArtworkApproved !== true || register.approvalBoundary?.turnV1Approved !== false || register.approvalBoundary?.finalLaneEntryAllowed !== false || register.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')

for (const evidence of Object.values(register.evidence) as Record<string, any>[]) if (!fs.existsSync(path.join(ROOT, evidence.file)) || sha256(path.join(ROOT, evidence.file)) !== evidence.sha256) fail(`evidence missing or changed: ${evidence.file}`)
for (const item of [...frames, register.animation.forward, register.animation.reverse, ...Object.values(register.evidence) as Record<string, any>[]]) {
  const publicAsset = fs.readdirSync(path.join(PUBLIC, 'assets')).find((name) => name.includes(item.sha256.slice(0, 16)))
  if (!publicAsset || sha256(path.join(PUBLIC, 'assets', publicAsset)) !== item.sha256) fail(`public asset missing for ${item.file}`)
}
const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Keeper Prime Turn V1 · front ↔ side-right', 'Eight-pose smooth draft · awaiting visual approval', 'Front → side', 'Side → front', 'Loop both', 'Route context', 'Nothing has entered Final or production', 'Side-right V1 is approved. Turn V1 is not.', 'height remains 298px throughout']) if (!html.includes(phrase)) fail(`public review omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('public playback script missing')
new Function(script)

console.log('Keeper Prime Turn V1 verified: 8 smooth poses, exact approved endpoints, exact reversible strips, 298px height, transparent gutters, bounded continuity and no production promotion.')
