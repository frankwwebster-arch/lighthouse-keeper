#!/usr/bin/env node
/** Verify V5's user-approved rear endpoint and immutable integration boundary. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-orthographic-views-2026-10-13-v5')
const REGISTER = path.join(PACK, 'batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-orthographic-v5/index.html')
const fail = (message: string): never => { throw new Error(`Keeper Prime orthographic V5: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const verify = (record: Record<string, any>, label: string) => {
  const file = path.join(ROOT, record.file)
  if (!fs.existsSync(file) || sha256(file) !== record.sha256) fail(`${label} missing or hash changed`)
  return file
}

for (const file of [REGISTER, PUBLIC, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-orthographic-views-2026-10-13-v5' || register.status !== 'approved-rear-endpoint-authority-for-kp-rig') fail('batch identity/status changed')
if (register.approval?.approvedBy !== 'Frank' || register.approval?.wording !== "They don't look like toe caps, they are excellent. Approved.") fail('approval record changed')
const frontFile = verify(register.approvedFront, 'approved front')
verify(register.selectedSide, 'selected side')
const approvedSource = verify(register.approvedSource, 'approved source')
if (sha256(path.join(ROOT, register.approvedSource.originalFile)) !== register.approvedSource.originalSha256 || register.approvedSource.regenerated !== false) fail('approved source provenance changed')
if (sha256(approvedSource) !== '2371101e33fcd2b9b27cbfdbcecdc1587c41783d5773605117a4678b5ac3ecc6') fail('wrong first boot source selected')
const oldBackFile = verify(register.history.v2InvalidBack, 'invalid V2 back')
const strictBackFile = verify(register.history.v4SupersededBack, 'superseded V4 back')
for (const key of ['v2Register', 'v3Register', 'v4Register']) verify(register.history[key], key)
const approvedFile = verify(register.approvedRearEndpoint, 'approved V5 rear endpoint')
if (sha256(path.join(ROOT, register.approvedRearEndpoint.sidecar)) !== register.approvedRearEndpoint.sidecarSha256) fail('sidecar hash changed')
if (register.approvedRearEndpoint.animationAuthoringAllowed !== true || register.approvedRearEndpoint.productionPromotionAllowed !== false) fail('approval boundary changed')
if (register.renderQualityContract?.approvedArtworkMaster !== register.approvedSource.file || register.renderQualityContract?.masterMustRemainSmooth !== true) fail('smooth artwork-master authority changed')
if (register.renderQualityContract?.registeredProxyResampling !== 'LANCZOS' || register.renderQualityContract?.nearestNeighbourMasterResamplingAllowed !== false || register.renderQualityContract?.roughOrJaggedInternalLineworkAllowed !== false) fail('smooth resampling/linework gate changed')
if (register.renderQualityContract?.actualMasterDimensions?.[0] < register.renderQualityContract?.minimumMasterDimensions?.[0] || register.renderQualityContract?.actualMasterDimensions?.[1] < register.renderQualityContract?.minimumMasterDimensions?.[1]) fail('approved artwork master is below its minimum dimensions')
for (const [name, evidence] of Object.entries(register.evidence as Record<string, any>)) verify(evidence, `${name} evidence`)
verify(register.legacyPoseEvidence, 'legacy pose evidence')

const front = PNG.sync.read(fs.readFileSync(frontFile))
const oldBack = PNG.sync.read(fs.readFileSync(oldBackFile))
const strictBack = PNG.sync.read(fs.readFileSync(strictBackFile))
const approved = PNG.sync.read(fs.readFileSync(approvedFile))
if (front.width !== 256 || front.height !== 320 || approved.width !== 256 || approved.height !== 320) fail('cell geometry changed')
let alphaMismatch = 0
let changedInside = 0
let changedOutside = 0
let changedFromV4 = 0
let edge = 0
for (let y = 0; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
  const offset = ((y * 256) + x) * 4
  if (front.data[offset + 3] !== approved.data[offset + 3]) alphaMismatch += 1
  let changed = false
  let differsFromV4 = false
  for (let channel = 0; channel < 4; channel += 1) {
    if (oldBack.data[offset + channel] !== approved.data[offset + channel]) changed = true
    if (strictBack.data[offset + channel] !== approved.data[offset + channel]) differsFromV4 = true
  }
  if (changed) {
    if (y >= 273 && y < 316) changedInside += 1
    else changedOutside += 1
  }
  if (differsFromV4) changedFromV4 += 1
  if ((x === 0 || x === 255 || y === 0 || y === 319) && approved.data[offset + 3] > 0) edge += 1
}
if (alphaMismatch !== 0 || register.validation.alphaMismatchPixels !== 0 || register.validation.alphaMatchesApprovedFrontExactly !== true) fail('approved back alpha is not exact')
if (changedOutside !== 0 || register.validation.changedPixelsOutsideEditRegion !== 0 || register.validation.upperBodyMatchesV2Exactly !== true) fail('pixels changed outside boot region')
if (changedInside <= 0 || changedInside !== register.validation.changedPixelsInsideEditRegion) fail('approved boot region did not change deterministically')
if (changedFromV4 <= 0 || changedFromV4 !== register.validation.pixelsDifferentFromV4) fail('V5 is not distinct from superseded V4')
if (edge !== 0 || !register.validation.transparentSafetyGutter || !register.validation.same298PixelHeight) fail('gutter or height contract failed')
if (register.validation.sideLandmarkRegistrationReady !== false) fail('V3 side block was lost')
if (register.validation.productionSpritesChanged !== false || register.validation.runtimeManifestChanged !== false || register.validation.animationDraftsChanged !== false) fail('production boundary changed')
for (const cue of ['rounded rear heel-counter panels', 'central vertical back seams', 'rear heel backs', 'rear sole edges']) if (!register.orientationContract.requiredBootCues.includes(cue)) fail(`missing approved rear cue ${cue}`)
for (const cue of ['forward-facing construction', 'front vamp highlights', 'shoelaces']) if (!register.orientationContract.forbiddenBootCues.includes(cue)) fail(`missing forbidden cue ${cue}`)
const html = fs.readFileSync(PUBLIC, 'utf8')
for (const phrase of ['They don\'t look like toe caps, they are excellent. Approved.', 'exact first edit Frank approved', 'Approved smooth artwork master', '1122 × 1402', 'Lanczos resampling', 'Rough full-resolution renders', 'rounded rear heel-counter panels', '0 of 81,920 alpha values differ', 'Rows 0–272 remain byte-identical to V2', 'KP Rig V1', 'selected side remains blocked at 5/15']) if (!html.includes(phrase)) fail(`public review omits ${phrase}`)
console.log(`Keeper Prime orthographic V5 verified: approved source pinned; ${changedInside} boot-region pixels changed, 0 outside, 0/81,920 alpha mismatches, ${changedFromV4} pixels distinguish V5 from V4.`)
