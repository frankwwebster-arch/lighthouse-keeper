#!/usr/bin/env node
/** Verify the reversible 15/15 smooth Keeper Prime side-right candidate. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const DRAFT = path.join(PACK, 'drafts/keeper_prime_master-neutral-standing-side-right_f1.png')
const SIDECAR = DRAFT.replace(/\.png$/, '.json')
const RAW = path.join(PACK, 'sources/keeper-prime-side-right-rigged-generated.png')
const CLEAN = path.join(PACK, 'sources/keeper-prime-side-right-rigged-clean-master.png')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-side-right-rigged-v1')
const MOTION_APPROVAL = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v4/batch-register.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime side-right rigged V1: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, DRAFT, SIDECAR, RAW, CLEAN, MOTION_APPROVAL, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}

const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-side-right-rigged-2026-10-13-v1' || register.status !== 'draft-smooth-side-right-15-of-15-awaiting-visual-approval') fail('batch identity/status changed')
if (sha256(RAW) !== '275caba38f9168a8b6627b5e8c8164959a216e30fd06032dfaaa2eb90be63393') fail('generated source changed')
if (register.generation?.rawSource?.sha256 !== sha256(RAW) || register.generation?.cleanMaster?.sha256 !== sha256(CLEAN)) fail('source hash record changed')
if (register.generation?.lowAlphaCleanupThreshold !== 8 || register.generation?.visibleRgbPixelsChangedByCleanup !== 0) fail('alpha-cleanup boundary changed')

for (const authority of ['front', 'back', 'rig'] as const) {
  const record = register.authorities?.[authority]
  if (!record || sha256(path.join(ROOT, record.file)) !== record.sha256 || sha256(path.join(ROOT, record.register)) !== record.registerSha256) fail(`${authority} authority changed`)
}
const historical = register.authorities?.historicalSideDesign
if (!historical || historical.landmarkPasses !== 5 || sha256(path.join(ROOT, historical.file)) !== historical.sha256 || sha256(path.join(ROOT, historical.auditRegister)) !== historical.auditRegisterSha256) fail('historical 5/15 side provenance changed')
const motionApproval = JSON.parse(fs.readFileSync(MOTION_APPROVAL, 'utf8')) as Record<string, any>
if (register.authorities?.motionApproval?.sha256 !== sha256(MOTION_APPROVAL) || register.authorities?.motionApproval?.wording !== 'Approved, very good indeed' || motionApproval.approval?.wording !== 'Approved, very good indeed') fail('Motion V3 approval pin changed')

const raw = PNG.sync.read(fs.readFileSync(RAW))
const clean = PNG.sync.read(fs.readFileSync(CLEAN))
const draft = PNG.sync.read(fs.readFileSync(DRAFT))
if (raw.width !== 1122 || raw.height !== 1402 || clean.width !== 1122 || clean.height !== 1402) fail('smooth master geometry changed')
if (draft.width !== 256 || draft.height !== 320) fail('registered proxy geometry changed')
if (register.candidate?.sha256 !== sha256(DRAFT) || register.candidate?.sidecarSha256 !== sha256(SIDECAR)) fail('candidate/sidecar hash record changed')
if (JSON.stringify(register.candidate?.geometry?.opaqueBoundsExclusive) !== '[77,18,179,316]' || register.candidate?.geometry?.edgeAlphaPixels !== 0) fail('registered bounds/gutter changed')
if (register.candidate?.registration?.registrationScale !== 0.234461054288 || JSON.stringify(register.candidate?.registration?.registeredSize) !== '[102,298]' || JSON.stringify(register.candidate?.registration?.registeredOffset) !== '[77,18]' || register.candidate?.registration?.filter !== 'Lanczos' || register.candidate?.registration?.creativePixelWarp !== false) fail('uniform registration contract changed')

let edgeAlpha = 0
for (let x = 0; x < draft.width; x += 1) edgeAlpha += Number(draft.data[(x * 4) + 3] > 0) + Number(draft.data[(((draft.height - 1) * draft.width + x) * 4) + 3] > 0)
for (let y = 1; y < draft.height - 1; y += 1) edgeAlpha += Number(draft.data[((y * draft.width) * 4) + 3] > 0) + Number(draft.data[((y * draft.width + draft.width - 1) * 4) + 3] > 0)
if (edgeAlpha !== 0) fail(`proxy has ${edgeAlpha} opaque edge pixels`)

const expectedIds = ['capTop', 'badgeCentre', 'earCentre', 'shoulderApex', 'beardBase', 'armStripeTop', 'armStripeCentre', 'armStripeBase', 'midriffStripeTop', 'midriffStripeCentre', 'midriffStripeBase', 'palmCentre', 'palmBase', 'kneeBandCentre', 'floor']
const landmarks = register.verticalLandmarks as Record<string, any>[]
if (JSON.stringify(landmarks.map((item) => item.id)) !== JSON.stringify(expectedIds)) fail('15-point landmark order changed')
for (const item of landmarks) {
  if (item.targetY !== item.candidateY || item.deltaY !== 0 || item.requiredDeltaY !== 0 || item.passesExact !== true || item.pixelEvidence?.passes !== true) fail(`${item.id} no longer passes exactly`)
  const [x, y] = item.pixelEvidence.sample as number[]
  const alpha = draft.data[((y * draft.width + x) * 4) + 3]
  if (alpha !== item.pixelEvidence.alpha || alpha < 64) fail(`${item.id} pixel evidence changed`)
}
if (register.validation?.exactLandmarkPassCount !== 15 || register.validation?.exactLandmarkTotal !== 15 || register.validation?.allPixelEvidencePresent !== true || register.validation?.transparentCellEdge !== true || register.validation?.uniformRegistrationOnly !== true) fail('15/15 validation changed')
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'animationDraftsChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['rightFacing90Degrees', 'solidDarkRectangularProfileEye', 'separateMoustache', 'readableClosedMouth', 'rearHairDistinctFromForwardBeard', 'singleBroadUniformStripe', 'sideFacingBoots', 'smoothHighResolutionMaster']) if (register.identityChecks?.[flag] !== true) fail(`${flag} identity check changed`)
for (const flag of ['whiteEyeGlint', 'smileOrGrin']) if (register.identityChecks?.[flag] !== false) fail(`${flag} rejection check changed`)
if (register.approvalBoundary?.sideArtworkApproved !== false || register.approvalBoundary?.turnAnimationAuthoringAllowed !== false || register.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')

const sidecar = JSON.parse(fs.readFileSync(SIDECAR, 'utf8')) as Record<string, any>
if (sidecar.w !== 32 || sidecar.h !== 40 || sidecar.density !== 8 || sidecar.frames !== 1 || JSON.stringify(sidecar.anchor) !== '[16,40]' || sidecar.sha256 !== sha256(DRAFT)) fail('strip/sidecar agreement changed')
if (JSON.stringify(sidecar.verticalLandmarks) !== JSON.stringify(landmarks)) fail('sidecar landmarks differ from register')

for (const record of Object.values(register.evidence) as Record<string, any>[]) if (!fs.existsSync(path.join(ROOT, record.file)) || sha256(path.join(ROOT, record.file)) !== record.sha256) fail(`evidence missing or changed: ${record.file}`)
for (const source of [register.authorities.front, register.authorities.back, historical, register.evidence.landmarkBoard, register.evidence.orthographicLineup, register.evidence.frontGhostOverSide, register.generation.cleanMaster, register.candidate]) {
  const publicAsset = fs.readdirSync(path.join(PUBLIC, 'assets')).find((name) => name.includes(source.sha256.slice(0, 16)))
  if (!publicAsset || sha256(path.join(PUBLIC, 'assets', publicAsset)) !== source.sha256) fail(`public copy missing or changed for ${source.file}`)
}

const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Keeper Prime side-right · rig-derived V1', 'New smooth candidate · 15/15 geometry · awaiting visual approval', 'Nothing has entered Final or production', 'Smooth high-resolution master', 'Historical preferred side · 5/15', 'Front ghost opacity', 'all 15 registered features', 'permit turn-animation authoring', 'It would not promote production sprites']) if (!html.includes(phrase)) fail(`public review omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('public ghost-control script missing')
new Function(script)

console.log('Keeper Prime side-right rigged V1 verified: smooth source, 256×320 proxy, exact 15/15 landmarks, transparent gutter, immutable authorities and no production/animation promotion.')
