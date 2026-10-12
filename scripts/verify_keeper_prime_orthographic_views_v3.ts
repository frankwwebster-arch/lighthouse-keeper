#!/usr/bin/env node
/** Verify V3's hard height and front-to-side vertical-landmark audit. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-orthographic-views-2026-10-13-v3')
const REGISTER = path.join(PACK, 'batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-orthographic-v3/index.html')
const fail = (message: string): never => { throw new Error(`Keeper Prime orthographic V3: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, PUBLIC, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-orthographic-views-2026-10-13-v3' || register.status !== 'draft-landmark-redraft-required') fail('batch identity/status changed')
if (register.alignmentContract?.opaqueHeight !== 298 || register.alignmentContract?.capTopY !== 18 || register.alignmentContract?.floorY !== 316 || register.alignmentContract?.requiredLandmarkDeltaY !== 0) fail('hard alignment contract changed')
if (!register.validation?.allViewsSameHeight || !register.validation?.allViewsShareCapTop || !register.validation?.allViewsShareFloor) fail('front/side/back height lock failed')
if (register.validation?.sideLandmarkRegistrationReady !== false) fail('selected V2 side must not be described as landmark-ready')
if (register.validation?.productionSpritesChanged !== false || register.validation?.runtimeManifestChanged !== false || register.validation?.animationDraftsChanged !== false) fail('production boundary changed')

const verify = (record: Record<string, any>, label: string) => {
  const file = path.join(ROOT, record.file)
  if (!fs.existsSync(file) || sha256(file) !== record.sha256) fail(`${label} missing or hash changed`)
}
verify(register.approvedFront, 'approved front')
if (sha256(path.join(ROOT, register.approvedFront.register)) !== register.approvedFront.registerSha256) fail('approved front register hash changed')
if (sha256(path.join(ROOT, register.immutableV2.register)) !== register.immutableV2.registerSha256) fail('V2 register hash changed')
verify(register.immutableV2.side, 'selected V2 side')
verify(register.immutableV2.back, 'V2 back')
verify(register.evidence.landmarkBoard, 'landmark board')
for (const [index, record] of register.rejectedGeneratedAttempts.entries()) verify(record, `rejected generated attempt ${index + 1}`)

const required = ['capTop', 'badgeCentre', 'earCentre', 'shoulderApex', 'beardBase', 'armStripeTop', 'armStripeCentre', 'armStripeBase', 'midriffStripeTop', 'midriffStripeCentre', 'midriffStripeBase', 'palmCentre', 'palmBase', 'kneeBandCentre', 'floor']
const landmarks = new Map((register.verticalLandmarks as Record<string, any>[]).map(item => [item.id, item]))
for (const id of required) if (!landmarks.has(id)) fail(`missing landmark ${id}`)
for (const item of landmarks.values()) {
  if (item.deltaY !== item.sideY - item.frontY || item.requiredDeltaY !== 0 || item.passesExact !== (item.deltaY === 0)) fail(`invalid landmark arithmetic for ${item.id}`)
}
const passCount = [...landmarks.values()].filter(item => item.passesExact).length
if (passCount !== register.validation.exactLandmarkPassCount || landmarks.size !== register.validation.exactLandmarkTotal) fail('landmark pass totals changed')
for (const id of ['badgeCentre', 'shoulderApex', 'beardBase', 'midriffStripeCentre', 'palmCentre']) if (landmarks.get(id)?.passesExact) fail(`${id} discrepancy was hidden`)
for (const id of ['capTop', 'armStripeTop', 'armStripeCentre', 'armStripeBase', 'floor']) if (!landmarks.get(id)?.passesExact) fail(`${id} known exact datum changed`)

const html = fs.readFileSync(PUBLIC, 'utf8')
for (const phrase of ['V2 exact front/back overlay', 'exactly 298 source pixels high', 'Front ↔ side vertical skeleton', 'beard base', 'shoulders, arm stripe and midriff stripe', 'selected side requires landmark redraft', 'Rejected generated correction attempts', 'not transition-ready']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
console.log(`Keeper Prime orthographic V3 verified: all views 298px high; ${passCount}/${landmarks.size} exact internal datums; selected side correctly blocked for landmark redraft.`)
