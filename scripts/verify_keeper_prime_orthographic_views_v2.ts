#!/usr/bin/env node
/** Verify V2's exact approved-front/rear alpha silhouette contract. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-orthographic-views-2026-10-13-v2')
const REGISTER = path.join(PACK, 'batch-register.json')
const MASTER_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-master-2026-10-12-v1/master-pack-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-orthographic-v2/index.html')
const fail = (message: string): never => { throw new Error(`Keeper Prime orthographic V2: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, MASTER_REGISTER, PUBLIC, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const master = JSON.parse(fs.readFileSync(MASTER_REGISTER, 'utf8')) as Record<string, any>
if (master.status !== 'approved-permanent-identity-authority' || master.approval?.wording !== 'Approved. Make sure this is NEVER forgotten.') fail('approved master authority was forgotten')
if (register.batchId !== 'keeper-prime-orthographic-views-2026-10-13-v2' || register.status !== 'draft-awaiting-visual-approval') fail('batch identity/status changed')
if (register.identityContract?.masterApprovalWording !== master.approval.wording) fail('derivative pack does not repeat the permanent approval wording')
if (register.identityContract?.uniform !== 'one broad pale chest-and-sleeve band; never restore the double stripe') fail('single-band uniform contract changed')
if (register.validation?.productionSpritesChanged !== false || register.validation?.runtimeManifestChanged !== false) fail('production guard changed')

const verifyRecord = (record: Record<string, any>, label: string) => {
  const file = path.join(ROOT, record.file)
  if (!fs.existsSync(file)) fail(`${label} missing`)
  if (sha256(file) !== record.sha256) fail(`${label} hash changed`)
  return file
}
const frontFile = verifyRecord(register.approvedFront, 'approved front')
if (register.approvedFront.registerSha256 !== sha256(MASTER_REGISTER)) fail('approved front register hash changed')
verifyRecord(register.poseReferences.legacySide, 'legacy side pose reference')
verifyRecord(register.poseReferences.legacyBack, 'legacy back pose reference')
verifyRecord(register.generatedSources.back180, 'generated back source')
verifyRecord(register.previousV1.register, 'V1 register')
verifyRecord(register.previousV1.sideCandidate, 'carried-forward V1 side')
verifyRecord(register.previousV1.backCandidate, 'superseded V1 back')

const candidateFiles: string[] = []
for (const [name, record] of Object.entries(register.candidates as Record<string, any>)) {
  const file = verifyRecord(record, `${name} candidate`)
  candidateFiles.push(file)
  if (record.promotionAllowed !== false) fail(`${name} promotion boundary changed`)
  const sidecarFile = path.join(ROOT, record.sidecar)
  if (sha256(sidecarFile) !== record.sidecarSha256) fail(`${name} sidecar hash changed`)
  const sidecar = JSON.parse(fs.readFileSync(sidecarFile, 'utf8'))
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 256 || png.height !== 320 || sidecar.w !== 32 || sidecar.h !== 40 || sidecar.density !== 8 || JSON.stringify(sidecar.anchor) !== '[16,40]') fail(`${name} cell/sidecar contract changed`)
  let edge = 0; let opaque = 0; let x0 = png.width; let y0 = png.height; let x1 = 0; let y1 = 0
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    const alpha = png.data[((y * png.width) + x) * 4 + 3]
    if (alpha > 0) {
      opaque += 1; x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x + 1); y1 = Math.max(y1, y + 1)
      if (x === 0 || y === 0 || x === png.width - 1 || y === png.height - 1) edge += 1
    }
  }
  if (!opaque || edge !== 0) fail(`${name} is empty or touches a cell edge`)
  if (JSON.stringify([x0, y0, x1, y1]) !== JSON.stringify(register.geometry[name].normalizedOpaqueBoundsExclusive)) fail(`${name} opaque bounds changed`)
  if (y0 !== 18 || y1 !== 316) fail(`${name} does not share the approved cap/floor lines`)
}
const front = PNG.sync.read(fs.readFileSync(frontFile))
if (front.width !== 256 || front.height !== 320) fail('approved front geometry changed')
const back = PNG.sync.read(fs.readFileSync(path.join(ROOT, register.candidates.back180.file)))
let alphaMismatchPixels = 0
for (let index = 3; index < front.data.length; index += 4) if (front.data[index] !== back.data[index]) alphaMismatchPixels += 1
if (alphaMismatchPixels !== 0 || register.validation.backAlphaMismatchPixels !== 0 || register.validation.backAlphaMatchesFrontExactly !== true) fail('back alpha silhouette is not byte-identical to approved front')
if (!register.validation.sharedCapTop || !register.validation.sharedFloor || !register.validation.transparentSafetyGutters) fail('alignment validations no longer pass')
if (register.geometry.sideRight90.opaqueWidth >= register.geometry.approvedFront.opaqueWidth) fail('90-degree side does not narrow from the front silhouette')
if (register.candidates.sideRight90.sha256 !== register.previousV1.sideCandidate.sha256) fail('90-degree side is not byte-identical to V1')
if (register.validation.backMaxRegisteredWidthDelta !== 0 || register.validation.backMaxRegisteredCenterDelta !== 0 || register.validation.backMaxAllOccupiedRowCenterDelta !== 0) fail('exact silhouette metrics are not all zero')
for (const [y, record] of Object.entries(register.crossSections as Record<string, any>)) {
  if (record.backWidthDeltaFromFront !== 0 || record.backCenterDeltaFromFront !== 0) fail(`back/front cross-section is not exact at y=${y}`)
}

for (const [name, record] of Object.entries(register.evidence as Record<string, any>)) verifyRecord(record, `${name} evidence`)
const html = fs.readFileSync(PUBLIC, 'utf8')
for (const phrase of ['Prime Master V1 is permanently approved', '90° right side · unchanged V1', '180° back · exact silhouette', 'Ghost overlays', 'cyan ghost', 'Absolute-match contract', '81,920 alpha values', 'pixel-for-pixel identical', 'Every back width and centre delta is exactly zero', 'Previous V1 back · superseded comparison']) {
  if (!html.includes(phrase)) fail(`public review omits ${phrase}`)
}
console.log(`Keeper Prime orthographic V2 verified: ${candidateFiles.length} candidates, 0/81,920 front/back alpha mismatches, V1 side byte-identical, transparent gutters.`)
