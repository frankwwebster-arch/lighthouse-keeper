#!/usr/bin/env node
/** Verify the reversible Walk V6 frame-8 lower-body repair. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-14-v6')
const V5 = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-14-v5')
const V4 = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-14-v4')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-walk-v6')
const PREFIX = '/keeper-review/keeper-prime-walk-v6/assets/'
const fail = (message: string): never => { throw new Error(`Keeper Prime Walk V6: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

const registerPath = path.join(PACK, 'batch-register.json')
for (const file of [registerPath, path.join(PACK, 'HANDOFF.md'), path.join(PUBLIC, 'index.html')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const register = JSON.parse(fs.readFileSync(registerPath, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-walk-2026-10-14-v6' || register.status !== 'draft-frame8-lower-body-repair-awaiting-visual-approval') fail('batch identity or status changed')
if (sha256(path.join(ROOT, register.previousCandidate.file ?? register.previousCandidate.register)) !== register.previousCandidate.sha256 || register.previousCandidate.filesChanged !== false) fail('V5 provenance changed')
if (sha256(path.join(ROOT, register.acceptedFrame8Base.file)) !== register.acceptedFrame8Base.sha256) fail('accepted V4 frame-8 base changed')
if (sha256(path.join(ROOT, register.generation.selectedSource.file)) !== register.generation.selectedSource.sha256) fail('selected arm source changed')

const frames = register.frames as Record<string, any>[]
if (!Array.isArray(frames) || frames.length !== 8 || register.animation?.frames !== 8 || register.animation?.fps !== 8 || register.animation?.loop !== true) fail('animation contract changed')
const pngs = frames.map((frame, index) => {
  const file = path.join(ROOT, frame.file)
  if (sha256(file) !== frame.sha256 || frame.edgeAlphaPixels !== 0 || frame.opaqueBoundsExclusive[3] !== 316) fail(`frame ${index + 1} hash/floor/gutter changed`)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 256 || png.height !== 320) fail(`frame ${index + 1} geometry changed`)
  for (let x = 0; x < 256; x += 1) if (png.data[x * 4 + 3] || png.data[(((319) * 256 + x) * 4) + 3]) fail(`frame ${index + 1} horizontal edge alpha`)
  for (let y = 1; y < 319; y += 1) if (png.data[(y * 256) * 4 + 3] || png.data[(y * 256 + 255) * 4 + 3]) fail(`frame ${index + 1} vertical edge alpha`)
  return png
})

for (let frame = 1; frame <= 7; frame += 1) {
  const previous = path.join(V5, `drafts/frames/keeper_prime_walk-right_f${frame}.png`)
  if (frames[frame - 1].sha256 !== sha256(previous) || frames[frame - 1].provenance?.byteIdenticalToV5 !== true) fail(`frame ${frame} is not byte-identical to V5`)
}
const repaired = pngs[7]
const accepted = PNG.sync.read(fs.readFileSync(path.join(V4, 'drafts/frames/keeper_prime_walk-right_f8.png')))
const v5Frame8 = path.join(V5, 'drafts/frames/keeper_prime_walk-right_f8.png')
if (frames[7].sha256 === sha256(v5Frame8) || frames[7].sha256 === sha256(path.join(V4, 'drafts/frames/keeper_prime_walk-right_f8.png'))) fail('frame 8 did not produce a distinct arm-only repair')
const provenance = frames[7].provenance
if (provenance?.pixelAudit?.changedPixels <= 0 || provenance?.pixelAudit?.changedOutsideDeclaredRegion !== 0 || provenance?.declaredEditPolygons?.length !== 2) fail('frame 8 escaped its two arm polygons')

// All pixels below the two arm masks are exact accepted F8 pixels.
for (let y = 245; y < 320; y += 1) {
  const start = y * 256 * 4
  const end = start + 256 * 4
  if (!repaired.data.subarray(start, end).equals(accepted.data.subarray(start, end))) fail(`frame 8 lower-leg/boot row ${y} differs from accepted F8`)
}
// The central upper-trouser/leg region that visibly warped in V5 is also exact.
for (let y = 230; y < 245; y += 1) for (let x = 100; x < 174; x += 1) {
  const offset = (y * 256 + x) * 4
  if (!repaired.data.subarray(offset, offset + 4).equals(accepted.data.subarray(offset, offset + 4))) fail(`frame 8 central trouser pixel ${x},${y} differs from accepted F8`)
}

const stripPath = path.join(ROOT, register.animation.strip.file)
if (sha256(stripPath) !== register.animation.strip.sha256) fail('strip changed')
const strip = PNG.sync.read(fs.readFileSync(stripPath))
if (strip.width !== 2048 || strip.height !== 320) fail('strip geometry changed')
for (let frame = 0; frame < 8; frame += 1) for (let y = 0; y < 320; y += 1) {
  const actual = strip.data.subarray(((y * 2048) + frame * 256) * 4, ((y * 2048) + frame * 256) * 4 + 1024)
  const expected = pngs[frame].data.subarray(y * 1024, y * 1024 + 1024)
  if (!actual.equals(expected)) fail(`strip frame ${frame + 1} disagrees with source frame`)
}
const sidecarPath = path.join(ROOT, register.animation.strip.sidecar)
const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8')) as Record<string, any>
if (sha256(sidecarPath) !== register.animation.strip.sidecarSha256 || sidecar.sha256 !== sha256(stripPath) || sidecar.frames !== 8 || sidecar.fps !== 8 || sidecar.status !== 'walk-v6-frame8-leg-repair-review-draft-not-production') fail('strip/sidecar agreement changed')

const previous = register.previousWalkV5FrameComparison as Record<string, any>[]
if (!Array.isArray(previous) || previous.length !== 8) fail('V5 comparison inventory changed')
for (const item of previous) if (sha256(path.join(ROOT, item.source)) !== item.sourceSha256 || sha256(path.join(ROOT, item.public)) !== item.publicSha256 || item.sourceSha256 !== item.publicSha256 || item.byteIdentical !== true) fail(`V5 comparison frame ${item.frame} changed`)

for (const item of [...frames, register.animation.strip, ...Object.values(register.evidence) as Record<string, any>[]]) {
  const publicAsset = fs.readdirSync(path.join(PUBLIC, 'assets')).find(name => name.includes(item.sha256.slice(0, 16)))
  if (!publicAsset || sha256(path.join(PUBLIC, 'assets', publicAsset)) !== item.sha256) fail(`public asset missing for ${item.file}`)
}
const htmlPath = path.join(PUBLIC, 'index.html')
if (register.reviewPage.sha256 !== sha256(htmlPath) || register.reviewPage.assetPrefix !== PREFIX || register.reviewPage.relativeAssetUrls !== false) fail('review page record changed')
const html = fs.readFileSync(htmlPath, 'utf8')
for (const phrase of ['Keeper Prime Walk V6 · right-facing', 'Frame-8 lower-body repair · awaiting visual approval', 'Walk V5 versus Walk V6 · synchronized exact game size', 'F1–F7 are byte-identical', 'accepted V4 frame-8 lower body', 'Nothing has entered Final or production']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (html.includes('src="assets/')) fail('relative public asset URL remains')
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('playback script missing')
new Function(script)

for (const flag of ['framesOneThroughSevenByteIdenticalToV5', 'frame8ChangesConfinedToTwoArmPolygons', 'frame8LowerBodyRestoredFromAcceptedV4Base', 'everyOutputCellHasTransparentEdge', 'stripMatchesFrames', 'sidecarMatchesStrip']) if (register.validation?.[flag] !== true) fail(`${flag} changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'workbenchFinalChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['walkV6Approved', 'walkStopApproved', 'finalLaneEntryAllowed', 'productionPromotionAllowed']) if (register.approvalBoundary?.[flag] !== false) fail(`${flag} approval boundary changed`)

console.log('Keeper Prime Walk V6 verified: F1-F7 exact V5; F8 arm-only repair; accepted central trousers, lower legs and boots restored; gutter/strip/sidecar/public agreement exact; no promotion.')
