#!/usr/bin/env node
/** Verify the Keeper Prime Construction Rig V1 and its non-production boundary. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-rig-v1')
const fail = (message: string): never => { throw new Error(`Keeper Prime Rig V1: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const verify = (record: Record<string, any>, label: string) => {
  const file = path.join(ROOT, record.file)
  if (!fs.existsSync(file) || sha256(file) !== record.sha256) fail(`${label} missing or hash changed`)
  return file
}
const distance = (a: number[], b: number[]) => Math.hypot(b[0] - a[0], b[1] - a[1])
const close = (a: number, b: number) => Math.abs(a - b) < 0.0002

for (const file of [REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html'), path.join(PUBLIC, 'keeper-prime-rig-v1.json')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-construction-rig-2026-10-13-v1' || register.status !== 'draft-construction-contract-awaiting-visual-approval') fail('batch identity/status changed')
const front = verify(register.authorities.front, 'approved front')
const back = verify(register.authorities.back, 'approved V5 back')
const historicalSide = verify(register.authorities.historicalSideDesign, 'historical side')
for (const authority of [register.authorities.front, register.authorities.back, register.authorities.historicalSideDesign]) {
  if (!fs.existsSync(path.join(ROOT, authority.register)) || sha256(path.join(ROOT, authority.register)) !== authority.registerSha256) fail('authority register changed')
}
if (sha256(path.join(ROOT, register.authorities.back.smoothMaster)) !== register.authorities.back.smoothMasterSha256) fail('smooth back master changed')
const rigFile = verify(register.rig, 'rig JSON')
if (!fs.readFileSync(rigFile).equals(fs.readFileSync(path.join(PUBLIC, 'keeper-prime-rig-v1.json')))) fail('public rig JSON differs')
const rig = JSON.parse(fs.readFileSync(rigFile, 'utf8')) as Record<string, any>
if (rig.status !== register.status || rig.coordinateSystem?.sourceCell?.join('x') !== '256x320' || rig.coordinateSystem?.logicalCell?.join('x') !== '32x40' || rig.coordinateSystem?.density !== 8) fail('coordinate system changed')
if (rig.coordinateSystem.axisX !== 128 || rig.coordinateSystem.capTopY !== 18 || rig.coordinateSystem.opaqueFloorY !== 316 || rig.coordinateSystem.anchor?.join(',') !== '128,320') fail('axis/cap/floor/anchor changed')

const joints = Object.fromEntries(Object.entries(rig.frontBackInvariant.joints as Record<string, any>).map(([name, record]) => [name, record.source])) as Record<string, number[]>
for (const [left, right] of [['shoulderLeft', 'shoulderRight'], ['elbowLeft', 'elbowRight'], ['wristLeft', 'wristRight'], ['handLeft', 'handRight'], ['hipLeft', 'hipRight'], ['kneeLeft', 'kneeRight'], ['ankleLeft', 'ankleRight'], ['heelLeft', 'heelRight'], ['toeLeft', 'toeRight']]) {
  if (!close(joints[left][0] + joints[right][0], 256) || !close(joints[left][1], joints[right][1])) fail(`${left}/${right} are not exact mirrors`)
}
for (const [leftA, leftB, rightA, rightB, label] of [
  ['shoulderLeft', 'elbowLeft', 'shoulderRight', 'elbowRight', 'upper arms'],
  ['elbowLeft', 'wristLeft', 'elbowRight', 'wristRight', 'forearms'],
  ['wristLeft', 'handLeft', 'wristRight', 'handRight', 'hands'],
  ['hipLeft', 'kneeLeft', 'hipRight', 'kneeRight', 'thighs'],
  ['kneeLeft', 'ankleLeft', 'kneeRight', 'ankleRight', 'shins'],
] as string[][]) if (!close(distance(joints[leftA], joints[leftB]), distance(joints[rightA], joints[rightB]))) fail(`${label} differ`)

const sideJoints = Object.fromEntries(Object.entries(rig.sideRightProjection.joints as Record<string, any>).map(([name, record]) => [name, record.source])) as Record<string, number[]>
for (const [nearA, nearB, farA, farB, label] of [
  ['shoulderNear', 'elbowNear', 'shoulderFar', 'elbowFar', 'side upper arms'],
  ['elbowNear', 'wristNear', 'elbowFar', 'wristFar', 'side forearms'],
  ['wristNear', 'handNear', 'wristFar', 'handFar', 'side hands'],
  ['hipNear', 'kneeNear', 'hipFar', 'kneeFar', 'side thighs'],
  ['kneeNear', 'ankleNear', 'kneeFar', 'ankleFar', 'side shins'],
] as string[][]) if (!close(distance(sideJoints[nearA], sideJoints[nearB]), distance(sideJoints[farA], sideJoints[farB]))) fail(`${label} differ`)
for (const [name, expected] of Object.entries(rig.invariantSegmentLengths as Record<string, number>)) {
  const pairs: Record<string, [string, string]> = { upperArm: ['shoulderRight', 'elbowRight'], forearm: ['elbowRight', 'wristRight'], wristToPalmCentre: ['wristRight', 'handRight'], thigh: ['hipRight', 'kneeRight'], shin: ['kneeRight', 'ankleRight'] }
  if (!close(expected, distance(joints[pairs[name][0]], joints[pairs[name][1]]))) fail(`${name} authority length changed`)
}

const v3 = JSON.parse(fs.readFileSync(path.join(ROOT, register.authorities.historicalSideDesign.register), 'utf8')) as Record<string, any>
if (register.verticalDatums.length !== 15 || rig.verticalDatums.length !== 15) fail('15-point datum register missing')
for (let index = 0; index < 15; index += 1) {
  const source = v3.verticalLandmarks[index]
  const datum = register.verticalDatums[index]
  if (datum.id !== source.id || datum.targetY !== source.frontY || datum.requiredDeltaY !== 0) fail(`datum ${index + 1} no longer uses approved front y`)
}
if (register.verticalDatums.filter((item: any) => item.passesCurrentSide).length !== 5 || register.validation.historicalSidePassCount !== 5 || register.validation.historicalSideBlocked !== true) fail('historical 5/15 side block changed')
if (register.validation.targetLandmarkPassCount !== 15 || register.validation.targetLandmarkTotal !== 15 || register.validation.allTargetDatumsUseApprovedFrontY !== true) fail('target 15/15 contract changed')
if (rig.renderQuality?.smoothHighResolutionMasterRequired !== true || rig.renderQuality?.nearestNeighbourMasterResizeAllowed !== false || rig.renderQuality?.finishedRasterMechanicalStretchAllowed !== false || rig.renderQuality?.roughOuterEdgesAllowed !== false || rig.renderQuality?.jaggedInternalLineworkAllowed !== false) fail('smooth-master contract changed')
if (rig.approvalBoundary?.rigApprovalAllowsSideAuthoring !== true || rig.approvalBoundary?.productionPromotionAllowed !== false || rig.approvalBoundary?.animationAuthoringAllowed !== false) fail('approval boundary changed')
if (register.validation.productionSpritesChanged !== false || register.validation.runtimeManifestChanged !== false || register.validation.animationDraftsChanged !== false) fail('production boundary changed')
for (const [name, evidence] of Object.entries(register.evidence as Record<string, any>)) {
  const file = verify(evidence, `${name} evidence`)
  const image = PNG.sync.read(fs.readFileSync(file))
  if ((name.endsWith('Overlay') || name.endsWith('Composite')) && (image.width !== 256 || image.height !== 320)) fail(`${name} geometry changed`)
}
for (const source of [front, back, historicalSide]) {
  const image = PNG.sync.read(fs.readFileSync(source))
  if (image.width !== 256 || image.height !== 320) fail('authority image geometry changed')
}
if (fs.existsSync(path.join(PACK, 'drafts'))) fail('Rig V1 must not contain generated side artwork')
const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Posable fixed-length lab', 'Arm angle', 'Elbow bend', 'Hip angle', 'Knee bend', '15/15 exact', '5/15', 'widths are projections', 'never mechanically stretched', 'No generated side art is included in Rig V1', 'awaiting rig approval']) if (!html.includes(phrase)) fail(`public review omits ${phrase}`)
console.log('Keeper Prime Rig V1 verified: 24 front/back bones, 24 side-projection bones, exact bilateral long-segment lengths, 15 invariant y-datums, historical side blocked at 5/15, no art promotion.')
