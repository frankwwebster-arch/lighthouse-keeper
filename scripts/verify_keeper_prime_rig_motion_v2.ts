#!/usr/bin/env node
/** Verify the immutable KP Rig V1 approval record and its V2 construction-motion proof. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v2')
const REGISTER = path.join(PACK, 'batch-register.json')
const MOTION = path.join(PACK, 'motion/keeper-prime-rig-motion-v2.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-rig-v2')
const V1_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v1/batch-register.json')
const V1_RIG = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v1/rig/keeper-prime-rig-v1.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime Rig Motion V2: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const distance = (a: number[], b: number[]) => Math.hypot(b[0] - a[0], b[1] - a[1])
const jointDelta = (a: Record<string, number[]>, b: Record<string, number[]>) => Math.max(...Object.keys(a).map((name) => distance(a[name], b[name])))

for (const file of [REGISTER, MOTION, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html'), path.join(PUBLIC, 'keeper-prime-rig-motion-v2.json')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
if (sha256(V1_REGISTER) !== '78ba5378f680413b15a73784f9b4b7bb8fa3d177933876b62c75f847e8f2720d') fail('approved V1 register changed')
if (sha256(V1_RIG) !== '5786df6eb654471f81dda161fc909a5768abb2d96aade24fb84448beb7cdf765') fail('approved V1 rig changed')

const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-construction-rig-2026-10-13-v2' || register.status !== 'approved-rig-motion-demo-awaiting-review') fail('batch identity/status changed')
if (register.approval?.approvedBy !== 'Frank' || register.approval?.approvedOn !== '2026-10-13' || register.approval?.wording !== "Approve KP Rig V1, let's see it animated") fail('V1 approval record changed')
if (register.approvedV1?.registerSha256 !== sha256(V1_REGISTER) || register.approvedV1?.rigSha256 !== sha256(V1_RIG)) fail('V1 provenance pins changed')
if (register.motion?.sha256 !== sha256(MOTION)) fail('motion JSON hash changed')
if (!fs.readFileSync(MOTION).equals(fs.readFileSync(path.join(PUBLIC, 'keeper-prime-rig-motion-v2.json')))) fail('public motion JSON differs')

const motion = JSON.parse(fs.readFileSync(MOTION, 'utf8')) as Record<string, any>
if (motion.status !== 'approved-rig-construction-motion-awaiting-review' || motion.stage?.width !== 640 || motion.stage?.height !== 340 || motion.stage?.floorY !== 316) fail('motion identity/stage changed')
if (motion.rig?.sha256 !== sha256(V1_RIG)) fail('motion no longer pins approved rig')
if (JSON.stringify(Object.keys(motion.clips)) !== JSON.stringify(['idle', 'walk', 'reach', 'sitStand'])) fail('clip order/set changed')
if (motion.rendering?.constructionMannequinOnly !== true || motion.rendering?.finishedRasterArtDeformed !== false || motion.rendering?.smoothFinishedArtRequiredLater !== true) fail('rendering boundary changed')

const rig = JSON.parse(fs.readFileSync(V1_RIG, 'utf8')) as Record<string, any>
const pairs = (view: string): [string, string, string][] => view === 'front'
  ? [['shoulderLeft', 'elbowLeft', 'upperArm'], ['elbowLeft', 'wristLeft', 'forearm'], ['wristLeft', 'handLeft', 'wristToPalmCentre'], ['shoulderRight', 'elbowRight', 'upperArm'], ['elbowRight', 'wristRight', 'forearm'], ['wristRight', 'handRight', 'wristToPalmCentre'], ['hipLeft', 'kneeLeft', 'thigh'], ['kneeLeft', 'ankleLeft', 'shin'], ['hipRight', 'kneeRight', 'thigh'], ['kneeRight', 'ankleRight', 'shin']]
  : [['shoulderNear', 'elbowNear', 'upperArm'], ['elbowNear', 'wristNear', 'forearm'], ['wristNear', 'handNear', 'wristToPalmCentre'], ['shoulderFar', 'elbowFar', 'upperArm'], ['elbowFar', 'wristFar', 'forearm'], ['wristFar', 'handFar', 'wristToPalmCentre'], ['hipNear', 'kneeNear', 'thigh'], ['kneeNear', 'ankleNear', 'shin'], ['hipFar', 'kneeFar', 'thigh'], ['kneeFar', 'ankleFar', 'shin']]
let maximumError = 0
for (const [clipId, clip] of Object.entries(motion.clips) as [string, Record<string, any>][]) {
  if (!Array.isArray(clip.frames) || clip.frames.length < 2 || clip.fps !== 30 || clip.loop !== true) fail(`${clipId} metadata changed`)
  for (const frame of clip.frames) for (const [a, b, kind] of pairs(clip.view)) maximumError = Math.max(maximumError, Math.abs(distance(frame.joints[a], frame.joints[b]) - rig.invariantSegmentLengths[kind]))
}
if (maximumError >= 0.000001 || motion.validation?.maximumInvariantSegmentErrorPixels !== 0 || motion.validation?.allInvariantSegmentErrorsBelowOneMillionthPixel !== true) fail(`fixed segment lengths drift by ${maximumError}`)

const walk = motion.clips.walk
const walkFirstRoot = walk.frames[0].joints.root[0] + walk.frames[0].offsetX
const walkLastRoot = walk.frames.at(-1).joints.root[0] + walk.frames.at(-1).offsetX
if (walk.rootMotion !== true || walk.rootTravelPixels !== 840 || walkLastRoot - walkFirstRoot !== 840 || walkFirstRoot > -50 || walkLastRoot < 690 || walk.startsFullyHidden !== true || walk.endsFullyHidden !== true) fail('walk must translate 840px and reset fully off-stage')
if (jointDelta(motion.clips.reach.frames[0].joints, motion.clips.reach.frames.at(-1).joints) !== 0) fail('reach does not return to exact neutral')
if (jointDelta(motion.clips.sitStand.frames[0].joints, motion.clips.sitStand.frames.at(-1).joints) !== 0) fail('sit/stand does not return to exact neutral')
for (const ankle of ['ankleNear', 'ankleFar']) {
  const first = motion.clips.sitStand.frames[0].joints[ankle]
  if (motion.clips.sitStand.frames.some((frame: any) => distance(first, frame.joints[ankle]) !== 0)) fail(`${ankle} is not planted`)
}
for (const flag of ['finishedRasterDeformed', 'productionSpritesChanged', 'runtimeManifestChanged', 'animationDraftsChanged']) if (motion.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (register.approvalBoundary?.motionReviewAllowsSideArtworkAuthoring !== true || register.approvalBoundary?.finishedAnimationApproved !== false || register.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')
if (fs.existsSync(path.join(PACK, 'drafts'))) fail('motion proof must not contain finished draft artwork')

const evidence = path.join(ROOT, register.evidence.motionContactSheet.file)
if (!fs.existsSync(evidence) || sha256(evidence) !== register.evidence.motionContactSheet.sha256) fail('contact sheet missing or changed')
const sheet = PNG.sync.read(fs.readFileSync(evidence))
if (sheet.width !== 920 || sheet.height !== 740) fail('contact sheet geometry changed')
const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['KP Rig V1 approved', 'construction mannequin, not finished Keeper raster art', 'Restrained idle', 'Walk with root travel', 'Controlled right-hand reach', 'planted ankles', 'it never walks on the spot', 'Show bones', 'Motion trail', 'smooth 90° side artwork draft']) if (!html.includes(phrase)) fail(`public review omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('public interaction script missing')
new Function(script)

console.log('Keeper Prime Rig Motion V2 verified: approved V1 unchanged; 4 construction clips; exact registered limb lengths; 840px off-stage walk; planted sit/stand ankles; no finished-art or production change.')
