#!/usr/bin/env node
/** Verify KP Rig Motion V3 changes only the requested walk cadence. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v3')
const REGISTER = path.join(PACK, 'batch-register.json')
const MOTION = path.join(PACK, 'motion/keeper-prime-rig-motion-v3.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-rig-v3')
const V1_RIG = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v1/rig/keeper-prime-rig-v1.json')
const V2_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v2/batch-register.json')
const V2_MOTION = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v2/motion/keeper-prime-rig-motion-v2.json')
const V2_PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-rig-v2/index.html')
const FEEDBACK = 'He needs to do more leg movement during the walk, moves too fast with too few steps. Otherwise very good indeed.'
const fail = (message: string): never => { throw new Error(`Keeper Prime Rig Motion V3: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const distance = (a: number[], b: number[]) => Math.hypot(b[0] - a[0], b[1] - a[1])

for (const file of [REGISTER, MOTION, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html'), path.join(PUBLIC, 'keeper-prime-rig-motion-v3.json')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
if (sha256(V2_REGISTER) !== 'd8ae1525d70d60835e63e1a202d24fdf1b0c57889294be64d0460143010e6bae') fail('V2 register changed')
if (sha256(V2_MOTION) !== 'bedfc66f174e7ce7598ca55b642595dc28cb6b805a82828df4a9f296ea45059e') fail('V2 motion changed')
if (sha256(V2_PAGE) !== 'af4614387401b0f2f3c548bd274a3bbe806bf6f4d91b64ff836eb62440ef1287') fail('V2 public page changed')

const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-construction-rig-2026-10-13-v3' || register.status !== 'walk-cadence-revision-awaiting-review') fail('batch identity/status changed')
if (register.feedback?.by !== 'Frank' || register.feedback?.wording !== FEEDBACK) fail('feedback record changed')
if (register.predecessor?.registerSha256 !== sha256(V2_REGISTER) || register.predecessor?.motionSha256 !== sha256(V2_MOTION) || register.predecessor?.publicPageSha256 !== sha256(V2_PAGE)) fail('V2 provenance pins changed')
if (register.motion?.sha256 !== sha256(MOTION)) fail('motion hash changed')
if (!fs.readFileSync(MOTION).equals(fs.readFileSync(path.join(PUBLIC, 'keeper-prime-rig-motion-v3.json')))) fail('public motion JSON differs')

const motion = JSON.parse(fs.readFileSync(MOTION, 'utf8')) as Record<string, any>
const v2 = JSON.parse(fs.readFileSync(V2_MOTION, 'utf8')) as Record<string, any>
if (motion.status !== 'approved-rig-walk-cadence-revision-awaiting-review' || JSON.stringify(Object.keys(motion.clips)) !== JSON.stringify(['idle', 'walk', 'reach', 'sitStand'])) fail('motion identity/clip order changed')
for (const clipId of ['idle', 'reach', 'sitStand']) if (JSON.stringify(motion.clips[clipId]) !== JSON.stringify(v2.clips[clipId])) fail(`${clipId} differs from V2`)

const walk = motion.clips.walk
if (walk.frames.length !== 150 || walk.fps !== 30 || walk.durationSeconds !== 5 || walk.gaitCycles !== 4 || walk.impliedSteps !== 8) fail('walk cadence contract changed')
if (walk.rootTravelPixels !== 840 || walk.rootSpeedPixelsPerSecond !== 168 || walk.thighSwingDegrees !== 32 || walk.maximumKneeLiftDegrees !== 44) fail('walk speed/articulation contract changed')
if (v2.clips.walk.frames.length !== 60 || register.walkRevision?.previousRootSpeedPixelsPerSecond !== 420 || register.walkRevision?.candidateRootSpeedPixelsPerSecond !== 168) fail('V2/V3 comparison changed')
const firstRoot = walk.frames[0].joints.root[0] + walk.frames[0].offsetX
const lastRoot = walk.frames.at(-1).joints.root[0] + walk.frames.at(-1).offsetX
if (lastRoot - firstRoot !== 840 || firstRoot > -50 || lastRoot < 690 || walk.startsFullyHidden !== true || walk.endsFullyHidden !== true) fail('walk does not retain hidden 840px root travel')

const rig = JSON.parse(fs.readFileSync(V1_RIG, 'utf8')) as Record<string, any>
const pairs: [string, string, string][] = [['shoulderNear', 'elbowNear', 'upperArm'], ['elbowNear', 'wristNear', 'forearm'], ['wristNear', 'handNear', 'wristToPalmCentre'], ['shoulderFar', 'elbowFar', 'upperArm'], ['elbowFar', 'wristFar', 'forearm'], ['wristFar', 'handFar', 'wristToPalmCentre'], ['hipNear', 'kneeNear', 'thigh'], ['kneeNear', 'ankleNear', 'shin'], ['hipFar', 'kneeFar', 'thigh'], ['kneeFar', 'ankleFar', 'shin']]
let maximumError = 0
for (const frame of walk.frames) for (const [a, b, kind] of pairs) maximumError = Math.max(maximumError, Math.abs(distance(frame.joints[a], frame.joints[b]) - rig.invariantSegmentLengths[kind]))
if (maximumError >= 0.000001 || motion.validation?.maximumInvariantSegmentErrorPixels !== 0) fail(`fixed segment lengths drift by ${maximumError}`)
for (const flag of ['finishedRasterDeformed', 'productionSpritesChanged', 'runtimeManifestChanged', 'animationDraftsChanged']) if (motion.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (register.approvalBoundary?.motionRevisionApproved !== false || register.approvalBoundary?.finishedAnimationApproved !== false || register.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')
if (fs.existsSync(path.join(PACK, 'drafts'))) fail('motion proof must not contain finished artwork')

const evidence = path.join(ROOT, register.evidence.motionContactSheet.file)
if (!fs.existsSync(evidence) || sha256(evidence) !== register.evidence.motionContactSheet.sha256) fail('contact sheet missing or changed')
const sheet = PNG.sync.read(fs.readFileSync(evidence))
if (sheet.width !== 920 || sheet.height !== 740) fail('contact sheet geometry changed')
const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Keeper Prime Rig V3', 'slower walk revision awaiting review', 'more leg movement, more steps and a slower walk', 'eight steps over five seconds', 'greater thigh swing and knee lift', 'it never walks on the spot', 'construction mannequin, not finished Keeper raster art', '8 steps / 5 seconds · 168 px/s root speed']) if (!html.includes(phrase)) fail(`public review omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('public interaction script missing')
new Function(script)

console.log('Keeper Prime Rig Motion V3 verified: V2 immutable; idle/reach/sit-stand identical; walk revised from 2 to 8 steps and 420 to 168 px/s; exact limb lengths; no production change.')
