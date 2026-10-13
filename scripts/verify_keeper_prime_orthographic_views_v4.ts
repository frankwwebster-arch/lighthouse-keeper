#!/usr/bin/env node
/** Verify V4's rear-facing boot correction and strict unchanged-region boundary. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-orthographic-views-2026-10-13-v4')
const REGISTER = path.join(PACK, 'batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-orthographic-v4/index.html')
const fail = (message: string): never => { throw new Error(`Keeper Prime orthographic V4: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const verify = (record: Record<string, any>, label: string) => { const file = path.join(ROOT, record.file); if (!fs.existsSync(file) || sha256(file) !== record.sha256) fail(`${label} missing or hash changed`); return file }

for (const file of [REGISTER, PUBLIC, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-orthographic-views-2026-10-13-v4' || register.status !== 'draft-back-boot-correction-awaiting-visual-approval') fail('batch identity/status changed')
const frontFile = verify(register.approvedFront, 'approved front')
verify(register.selectedSide, 'selected side')
const oldBackFile = verify(register.rejectedV2Back, 'rejected V2 back')
verify(register.generatedSource, 'generated source')
verify(register.rejectedGeneratedAttempt, 'rejected rounded-heel attempt')
verify(register.legacyPoseEvidence, 'legacy pose evidence')
const candidateFile = verify(register.candidate, 'V4 candidate')
if (sha256(path.join(ROOT, register.candidate.sidecar)) !== register.candidate.sidecarSha256 || register.candidate.promotionAllowed !== false) fail('candidate sidecar or promotion boundary changed')
for (const [name, evidence] of Object.entries(register.evidence as Record<string, any>)) verify(evidence, `${name} evidence`)
for (const [key, expected] of [['v2Register', 'v2RegisterSha256'], ['v3Register', 'v3RegisterSha256']] as const) if (sha256(path.join(ROOT, register.immutablePredecessors[key])) !== register.immutablePredecessors[expected]) fail(`${key} changed`)

const front = PNG.sync.read(fs.readFileSync(frontFile))
const oldBack = PNG.sync.read(fs.readFileSync(oldBackFile))
const candidate = PNG.sync.read(fs.readFileSync(candidateFile))
if (front.width !== 256 || front.height !== 320 || candidate.width !== 256 || candidate.height !== 320) fail('cell geometry changed')
let alphaMismatch = 0; let changedInside = 0; let changedOutside = 0; let edge = 0
for (let y = 0; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
  const offset = ((y * 256) + x) * 4
  if (front.data[offset + 3] !== candidate.data[offset + 3]) alphaMismatch += 1
  let changed = false
  for (let channel = 0; channel < 4; channel += 1) if (oldBack.data[offset + channel] !== candidate.data[offset + channel]) changed = true
  if (changed) { if (y >= 273 && y < 316) changedInside += 1; else changedOutside += 1 }
  if ((x === 0 || x === 255 || y === 0 || y === 319) && candidate.data[offset + 3] > 0) edge += 1
}
if (alphaMismatch !== 0 || register.validation.alphaMismatchPixels !== 0 || register.validation.alphaMatchesApprovedFrontExactly !== true) fail('corrected back alpha is not exact')
if (changedOutside !== 0 || register.validation.changedPixelsOutsideEditRegion !== 0 || register.validation.upperBodyMatchesV2Exactly !== true) fail('pixels changed outside boot region')
if (changedInside <= 0 || changedInside !== register.validation.changedPixelsInsideEditRegion) fail('boot region did not change deterministically')
if (edge !== 0 || !register.validation.transparentSafetyGutter || !register.validation.same298PixelHeight) fail('gutter or height contract failed')
if (register.validation.sideLandmarkRegistrationReady !== false) fail('V3 side block was lost')
if (register.validation.productionSpritesChanged !== false || register.validation.runtimeManifestChanged !== false || register.validation.animationDraftsChanged !== false) fail('production boundary changed')
for (const cue of ['flat squared heel backs', 'rectangular heel-counter panels', 'vertical back seams', 'rear sole edges']) if (!register.orientationContract.requiredBootCues.includes(cue)) fail(`missing rear cue ${cue}`)
for (const cue of ['front toe caps', 'rounded toe-like panels', 'front vamp highlights', 'shoelaces']) if (!register.orientationContract.forbiddenBootCues.includes(cue)) fail(`missing forbidden cue ${cue}`)
const html = fs.readFileSync(PUBLIC, 'utf8')
for (const phrase of ['feet face the player', 'rear-facing boots', 'front toe caps', 'flat squared heel backs', 'rectangular heel-counter panels', 'vertical back seams', '0 of 81,920 alpha values differ', 'Rows 0–272 are byte-identical to V2', 'selected side remains blocked']) if (!html.includes(phrase)) fail(`public review omits ${phrase}`)
console.log(`Keeper Prime orthographic V4 verified: ${changedInside} lower-region pixels changed, 0 outside, 0/81,920 alpha mismatches, side remains blocked.`)
