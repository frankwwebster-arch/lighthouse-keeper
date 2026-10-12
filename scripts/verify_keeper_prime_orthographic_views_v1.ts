#!/usr/bin/env node
/** Verify the Prime Keeper 0°/90°/180° orthographic review contract. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-orthographic-views-2026-10-13-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const MASTER_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-master-2026-10-12-v1/master-pack-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-orthographic-v1/index.html')
const fail = (message: string): never => { throw new Error(`Keeper Prime orthographic V1: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, MASTER_REGISTER, PUBLIC, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const master = JSON.parse(fs.readFileSync(MASTER_REGISTER, 'utf8')) as Record<string, any>
if (master.status !== 'approved-permanent-identity-authority' || master.approval?.wording !== 'Approved. Make sure this is NEVER forgotten.') fail('approved master authority was forgotten')
if (register.batchId !== 'keeper-prime-orthographic-views-2026-10-13-v1' || register.status !== 'draft-awaiting-visual-approval') fail('batch identity/status changed')
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
verifyRecord(register.generatedSources.sideRight90, 'generated side source')
verifyRecord(register.generatedSources.back180, 'generated back source')
if (register.rejectedProvenance?.length !== 1 || !register.rejectedProvenance[0].reason.includes('misidentifying it as beard')) fail('rejected too-short rear-hair provenance changed')
verifyRecord(register.rejectedProvenance[0], 'rejected back source')

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
let maxAllRowCenterDelta = 0
for (let y = 18; y < 316; y += 1) {
  const bounds = (png: PNG) => {
    const xs: number[] = []
    for (let x = 0; x < png.width; x += 1) if (png.data[((y * png.width) + x) * 4 + 3] >= 128) xs.push(x)
    if (!xs.length) fail(`missing occupied silhouette at y=${y}`)
    return { centerX: (xs[0] + xs.at(-1)! + 1) / 2 }
  }
  maxAllRowCenterDelta = Math.max(maxAllRowCenterDelta, Math.abs(bounds(back).centerX - bounds(front).centerX))
}
if (maxAllRowCenterDelta > 0.5 || register.validation.backMaxAllOccupiedRowCenterDelta !== maxAllRowCenterDelta) fail('back/front centreline diverges on an occupied row')
if (!register.validation.sharedCapTop || !register.validation.sharedFloor || !register.validation.transparentSafetyGutters) fail('alignment validations no longer pass')
if (register.geometry.sideRight90.opaqueWidth >= register.geometry.approvedFront.opaqueWidth) fail('90-degree side does not narrow from the front silhouette')
if (Math.abs(register.geometry.back180.opaqueWidth - register.geometry.approvedFront.opaqueWidth) > 8) fail('180-degree back width diverges from approved front')
if (Math.abs(register.geometry.back180.opaqueCenterX - 128) > 1 || Math.abs(register.geometry.sideRight90.opaqueCenterX - 128) > 1) fail('candidate identity axis drifted')
if (register.validation.backMaxRegisteredWidthDelta > 4 || register.validation.backMaxRegisteredCenterDelta > 0.5) fail('back/front registered silhouette cross-sections diverge')
for (const [y, record] of Object.entries(register.crossSections as Record<string, any>)) {
  if (Math.abs(record.backWidthDeltaFromFront) > 4 || Math.abs(record.backCenterDeltaFromFront) > 0.5) fail(`back/front cross-section diverges at y=${y}`)
}

for (const [name, record] of Object.entries(register.evidence as Record<string, any>)) verifyRecord(record, `${name} evidence`)
const html = fs.readFileSync(PUBLIC, 'utf8')
for (const phrase of ['Prime Master V1 is permanently approved', '90° right side', '180° back', 'Ghost overlays', 'cyan ghost', 'one broad pale jumper band', 'Silhouette cross-sections', 'within 4 source pixels', 'every occupied row', 'Rejected provenance', 'Too-short rear-hair edit', 'This is not a candidate']) {
  if (!html.includes(phrase)) fail(`public review omits ${phrase}`)
}
console.log(`Keeper Prime orthographic V1 verified: ${candidateFiles.length} candidates, shared cap y=18/floor y=316, centred axes, transparent gutters, permanent front authority pinned.`)
