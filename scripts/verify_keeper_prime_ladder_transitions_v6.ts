#!/usr/bin/env node
/** Verify Ladder Transition V6: approved V5 animation, flat two-way door only. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const v5Pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v5')
const pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v6')
const v5SpecFile = path.join(v5Pack, 'keeper-prime-ladder-transitions-v5.json')
const v5RegisterFile = path.join(v5Pack, 'batch-register.json')
const approvalFile = path.join(root, 'docs/review/keeper-prime-ladder-transitions-v5-animation-approval-2026-10-16.json')
const doorContractFile = path.join(root, 'docs/review/keeper-two-way-door-contract-2026-10-16.json')
const v5PageFile = path.join(root, 'public/keeper-review/keeper-prime-ladder-transitions-v5/index.html')
const specFile = path.join(pack, 'keeper-prime-ladder-transitions-v6.json')
const registerFile = path.join(pack, 'batch-register.json')
const pageFile = path.join(root, 'public/keeper-review/keeper-prime-ladder-transitions-v6/index.html')
const read = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message: string): never => { throw new Error(`[keeper-prime-ladder-transitions-v6] ${message}`) }

for (const file of [v5SpecFile, v5RegisterFile, approvalFile, doorContractFile, v5PageFile, specFile, registerFile, pageFile]) if (!fs.existsSync(file)) fail(`missing ${path.relative(root, file)}`)
const v5 = read(v5SpecFile)
const v5Register = read(v5RegisterFile)
const approval = read(approvalFile)
const doorContract = read(doorContractFile)
const spec = read(specFile)
const register = read(registerFile)

if (approval.candidate !== 'keeper-prime-ladder-transitions-v5' || !approval.approvalBoundary.keeperAnimationApproved || !approval.approvalBoundary.all111RouteFramesApproved || approval.approvalBoundary.v5DoorPresentationApproved || !approval.approvalBoundary.v5DoorPerspectiveRejected || !approval.approvalBoundary.v6DoorOnlyCorrectionAuthorized) fail('V5 partial approval boundary changed')
for (const key of ['candidateRegister', 'candidateSpec', 'reviewPage']) {
  const authority = approval[key]
  const file = path.join(root, authority.file)
  if (!fs.existsSync(file) || sha(file) !== authority.sha256) fail(`V5 approval authority changed: ${key}`)
}
if (!doorContract.contract.twoWaySwing || !doorContract.contract.opensAwayFromApproachingKeeper || doorContract.contract.screenHingeSide !== 'right' || !doorContract.contract.doorLeafProvidesCrossingOcclusion || doorContract.contract.roomBoundaryProvidesCrossingOcclusion || !doorContract.contract.autoCloseOnlyAfterKeeperFullyClearsDoorway || doorContract.contract.autoCloseRequiresKeeperAnimation || doorContract.contract.costumeSpecificDoorAnimationRequired) fail('two-way door contract changed')
if (spec.set !== 'keeper-prime-ladder-transitions-v6' || spec.status !== 'draft-awaiting-two-way-door-review') fail('candidate identity changed')
for (const [key, authority] of Object.entries<any>(register.authorities)) {
  const file = path.join(root, authority.file)
  if (!fs.existsSync(file) || sha(file) !== authority.sha256) fail(`${key} authority changed`)
}

const door = spec.geometry.upperDoor
if (door.orientationToHallwayDeg !== 90 || door.projection !== 'flat-orthographic-rectangle' || door.perspectiveWideningAllowed || door.gradientDepthAllowed || door.onlyProtrudingComponent !== 'handle' || door.hingeSideAsViewed !== 'right' || door.swingDirection !== 'away-from-approaching-keeper') fail('flat two-way door contract changed')
if (door.jambXLp !== 158 || door.jambWidthLp !== 0.5 || door.leafXLp !== 158.5 || door.leafWidthLp !== 20 || door.leafHeightLp !== 48 || door.visibleStageRightXLp !== 172 || door.hingeXLp !== 178.5 || door.handleXLp !== 161.3 || door.handleWidthLp !== 1.4 || door.handleHeightLp !== 1.4) fail('flat door geometry changed')
if (door.leafXLp > door.hiddenRootXLp - 16 || door.leafXLp + door.leafWidthLp < door.visibleStageRightXLp) fail('opaque door leaf does not cover the final visible Keeper cell')
if (!spec.doorPolicy.twoWaySwing || !spec.doorPolicy.opensAwayFromApproachingKeeper || spec.doorPolicy.hingeSideAsViewed !== 'right' || spec.doorPolicy.occlusionMethod !== 'opaque-open-door-leaf' || spec.doorPolicy.autoCloseTrigger !== 'keeper-fully-cleared-doorway' || spec.doorPolicy.autoCloseRequiresKeeperAnimation || spec.doorPolicy.remainsOpenAfterRoomEntry || spec.doorPolicy.costumeSpecificDoorAnimationRequired) fail('door policy changed')
if (!spec.presentationCorrection.v5KeeperAnimationApproved || spec.presentationCorrection.keeperFramesChanged || spec.presentationCorrection.rootsChanged || spec.presentationCorrection.timingChanged || spec.presentationCorrection.choreographyChanged || spec.presentationCorrection.presentationPhaseLabelsChangedOnly || !spec.presentationCorrection.v5PerspectiveDoorRejected || !spec.presentationCorrection.flatTwoWayDoorOnly) fail('door-only correction boundary changed')

const clean = (frame: any) => { const value = { ...frame }; delete value.src; return value }
for (const [routeId, route] of Object.entries<any>(spec.routes)) {
  const prior = v5.routes[routeId]
  if (!prior || route.frames.length !== prior.frames.length) fail(`${routeId} frame count changed`)
  for (let index = 0; index < route.frames.length; index++) {
    if (JSON.stringify(clean(route.frames[index])) !== JSON.stringify(clean(prior.frames[index]))) fail(`${routeId} F${index + 1} root/timing/choreography changed`)
    if (!route.frames[index].src.startsWith('/keeper-review/keeper-prime-ladder-transitions-v6/assets/')) fail(`${routeId} F${index + 1} stale prefix`)
  }
}
if (spec.routes.full.frames.length !== 111 || spec.routes.full.frames.at(-1).upperDoorOpen !== 1) fail('approved complete route changed')

if (register.publishedAssets.length !== 31 || v5Register.publishedAssets.length !== 31) fail('asset inventory changed')
for (const asset of register.publishedAssets) {
  const prior = v5Register.publishedAssets.find((entry: any) => path.basename(entry.draft) === path.basename(asset.draft))
  const source = path.join(root, asset.source)
  const draft = path.join(root, asset.draft)
  const published = path.join(root, asset.published)
  if (!prior || prior.draftSha256 !== asset.sourceSha256 || asset.sourceSha256 !== asset.draftSha256) fail(`V5 Keeper asset bytes changed: ${asset.draft}`)
  if (!fs.existsSync(source) || sha(source) !== asset.sourceSha256 || !fs.existsSync(draft) || sha(draft) !== asset.draftSha256 || !fs.existsSync(published) || sha(published) !== asset.draftSha256) fail(`asset provenance mismatch: ${asset.draft}`)
  const image = PNG.sync.read(fs.readFileSync(draft))
  let edgeAlpha = 0
  for (let x = 0; x < image.width; x++) edgeAlpha += Number(image.data[x * 4 + 3] > 0) + Number(image.data[((image.height - 1) * image.width + x) * 4 + 3] > 0)
  for (let y = 1; y < image.height - 1; y++) edgeAlpha += Number(image.data[y * image.width * 4 + 3] > 0) + Number(image.data[(y * image.width + image.width - 1) * 4 + 3] > 0)
  if (edgeAlpha) fail(`opaque cell edge: ${asset.draft}`)
}

if (!register.changes.keeperAnimationApproved || register.changes.keeperAssetsChanged || register.changes.routeRootsChanged || register.changes.routeTimingChanged || register.changes.routeChoreographyChanged || register.changes.presentationPhaseLabelsChangedOnly || !register.changes.v5PerspectiveDoorRejected || !register.changes.flatTwoWayDoorOnly || register.changes.doorLeafWidthLp !== 20 || register.changes.doorLeafHeightLp !== 48 || register.changes.hingeSideAsViewed !== 'right' || !register.changes.opensAwayFromApproachingKeeper || register.changes.perspectiveWideningAllowed || register.changes.gradientDepthAllowed || register.changes.onlyProtrudingComponent !== 'handle' || register.changes.occlusionMethod !== 'opaque-open-door-leaf' || register.changes.autoCloseTrigger !== 'keeper-fully-cleared-doorway' || register.changes.autoCloseRequiresKeeperAnimation || !register.changes.finalVisibleKeeperCellFullyCoveredByDoorLeaf) fail('registered change scope widened')
if (register.changes.finalChanged || register.changes.runtimeChanged || register.changes.productionChanged || register.approvalBoundary.candidateApproved || register.approvalBoundary.doorPresentationApproved || register.approvalBoundary.finalLaneEntryAllowed || register.approvalBoundary.productionPromotionAllowed) fail('unapproved door candidate promoted')

const html = fs.readFileSync(pageFile, 'utf8')
for (const required of ['Keeper Prime ladder transitions V6', 'Animation approved', 'Two-way door', 'Flat leaf', 'opens away', 'closes after full clearance', 'Automatic close', 'Keeper fully clears the doorway', 'No costume variant', 'door controller owns the closing action', "background:#426574;border:0", "nodes.rightDoor.style.width=px(20,scale)", "nodes.rightKnob.style.width=px(1.4,scale)", "nodes.rightDoor.style.zIndex=open>.8?'8':'3'", 'opaque open leaf—not the room boundary']) if (!html.includes(required)) fail(`review contract missing: ${required}`)
for (const forbidden of ['Door remains open', 'closes only after the later return', 'img.style.clipPath=', 'const clipRight=', 'side-wall boundary—not a broad door face', '1.5 lp flat edge', "nodes.rightDoor.style.width=px(1.5,scale)", 'linear-gradient(90deg,#284756,#426574)', '12.5+7.5*open', '155.5+3*open', "add(world,'doorFrame',150,8,18,48", "add(world,'doorLeaf',155.5,8,12.5,48"]) if (html.includes(forbidden)) fail(`rejected door treatment remains: ${forbidden}`)
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(match => match[1])
if (scripts.length !== 1) fail('unexpected inline script count')
try { new Function(scripts[0]) } catch (error) { fail(`review script does not compile: ${String(error)}`) }
const urls = new Set(Object.values<any>(spec.routes).flatMap((route: any) => route.frames.map((frame: any) => frame.src)))
if (urls.size !== 31) fail(`unexpected unique frame count: ${urls.size}`)

console.log(JSON.stringify({
  ok: true,
  approvedAnimationFrames: 111,
  uniqueKeeperAssets: 31,
  keeperAnimationChanged: false,
  doorProjection: 'flat-orthographic-rectangle',
  doorLeafSizeLp: [20, 48],
  twoWaySwing: true,
  opensAwayFromApproachingKeeper: true,
  perspectiveWideningAllowed: false,
  onlyProtrudingComponent: 'handle',
  occlusionMethod: 'opaque-open-door-leaf',
  autoCloseTrigger: 'keeper-fully-cleared-doorway',
  finalVisibleKeeperCellFullyCoveredByDoorLeaf: true,
  productionChanged: false,
}, null, 2))
