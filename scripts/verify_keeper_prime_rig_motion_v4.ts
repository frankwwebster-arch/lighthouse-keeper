#!/usr/bin/env node
/** Verify the immutable approval record for KP Rig Motion V3. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v4')
const REGISTER = path.join(PACK, 'batch-register.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime Rig Motion V4 approval: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-construction-rig-2026-10-13-v4' || register.status !== 'approved-motion-authority') fail('batch identity/status changed')
if (register.approval?.approvedBy !== 'Frank' || register.approval?.approvedOn !== '2026-10-13' || register.approval?.wording !== 'Approved, very good indeed') fail('approval wording changed')

for (const [key, hashKey] of [['register', 'registerSha256'], ['motion', 'motionSha256'], ['publicPage', 'publicPageSha256']] as [string, string][]) {
  const file = path.join(ROOT, register.approvedCandidate[key])
  if (!fs.existsSync(file) || sha256(file) !== register.approvedCandidate[hashKey]) fail(`approved V3 ${key} changed`)
}
const motion = JSON.parse(fs.readFileSync(path.join(ROOT, register.approvedCandidate.motion), 'utf8')) as Record<string, any>
const walk = motion.clips?.walk
if (walk?.frames?.length !== 150 || walk?.fps !== 30 || walk?.durationSeconds !== 5 || walk?.gaitCycles !== 4 || walk?.impliedSteps !== 8 || walk?.rootTravelPixels !== 840 || walk?.rootSpeedPixelsPerSecond !== 168 || walk?.thighSwingDegrees !== 32 || walk?.maximumKneeLiftDegrees !== 44) fail('approved walk metrics changed')
if (motion.validation?.maximumInvariantSegmentErrorPixels !== 0 || JSON.stringify(register.approvedMotion?.unchangedFromV2) !== JSON.stringify(['idle', 'reach', 'sitStand'])) fail('approved invariant/unchanged clips changed')
const boundary = register.approvalBoundary
if (boundary?.constructionMotionApproved !== true || boundary?.authorizesSmoothSideRightDraft !== true || boundary?.finishedKeeperArtworkApproved !== false || boundary?.finishedAnimationApproved !== false || boundary?.productionPromotionAllowed !== false) fail('approval boundary changed')
for (const forbidden of ['motion', 'evidence', 'drafts', 'sources']) if (fs.existsSync(path.join(PACK, forbidden))) fail(`approval record must not duplicate or generate ${forbidden}`)

console.log('Keeper Prime Rig Motion approval verified: exact V3 bytes pinned; eight-step/five-second cadence approved; smooth 15/15 side draft authorized; no art or production promotion.')
