#!/usr/bin/env node
/** Verify Ladder Transition V5: approved V4 plus the complete side-on upper-door exit. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const v4Pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v4')
const pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v5')
const v4SpecFile = path.join(v4Pack, 'keeper-prime-ladder-transitions-v4.json')
const v4RegisterFile = path.join(v4Pack, 'batch-register.json')
const v4ApprovalFile = path.join(root, 'docs/review/keeper-prime-ladder-transitions-v4-approval-2026-10-16.json')
const v4PageFile = path.join(root, 'public/keeper-review/keeper-prime-ladder-transitions-v4/index.html')
const specFile = path.join(pack, 'keeper-prime-ladder-transitions-v5.json')
const registerFile = path.join(pack, 'batch-register.json')
const pageFile = path.join(root, 'public/keeper-review/keeper-prime-ladder-transitions-v5/index.html')
const read = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message: string): never => { throw new Error(`[keeper-prime-ladder-transitions-v5] ${message}`) }

for (const file of [v4SpecFile, v4RegisterFile, v4ApprovalFile, v4PageFile, specFile, registerFile, pageFile]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(root, file)}`)
}
const v4 = read(v4SpecFile)
const v4Register = read(v4RegisterFile)
const spec = read(specFile)
const register = read(registerFile)

if (spec.set !== 'keeper-prime-ladder-transitions-v5' || spec.status !== 'draft-awaiting-upper-door-flow-review') fail('candidate identity changed')
if (register.batchId !== 'keeper-prime-ladder-transitions-2026-10-16-v5' || register.status !== spec.status) fail('register identity changed')
for (const [key, authority] of Object.entries<any>(register.authorities)) {
  const file = path.join(root, authority.file)
  if (!fs.existsSync(file) || sha(file) !== authority.sha256) fail(`${key} authority changed`)
}
if (register.authorities.v4Spec.sha256 !== sha(v4SpecFile) || register.authorities.v4Register.sha256 !== sha(v4RegisterFile) || register.authorities.v4Approval.sha256 !== sha(v4ApprovalFile) || register.authorities.v4Page.sha256 !== sha(v4PageFile)) fail('V4 authority pin changed')

const door = spec.geometry.upperDoor
if (door.orientationToCameraDeg !== 90 || !door.opensOutwardIntoHallway || !door.occludesKeeperWhenOpen) fail('dollhouse door orientation contract changed')
if (door.frameLeftLp !== 150 || door.frameWidthLp !== 18 || door.leafClosedLeftLp !== 155.5 || door.leafClosedWidthLp !== 12.5 || door.leafOpenLeftLp !== 158.5 || door.leafOpenWidthLp !== 20 || door.handleXLp !== 162) fail('upper-door geometry changed')
if (door.stopRootXLp !== 148.25 || door.transferRootXLp !== 158.75 || door.hiddenRootXLp !== 174.5) fail('upper-door route anchors changed')
if (door.leafOpenLeftLp > door.hiddenRootXLp - 16 || door.leafOpenLeftLp + door.leafOpenWidthLp < 172) fail('open door does not cover the final visible Keeper cell')
if (!spec.doorPolicy.opensTowardKeeperIntoHallway || !spec.doorPolicy.remainsOpenAfterRoomEntry || !spec.doorPolicy.closesOnlyAfterKeeperLaterLeavesRoom || !spec.doorPolicy.costumeChangeAllowedOnlyUnderFullDoorOcclusion || spec.doorPolicy.costumeSpecificDoorAnimationRequired) fail('persistent room-door policy changed')
if (!spec.delivery.allUniqueFramesDecodedBeforePlayback || !spec.delivery.allUniqueFramesMountedBeforePlayback || spec.delivery.architectureRebuiltDuringPlayback || spec.delivery.defaultRoute !== 'full' || !spec.delivery.completeUpperDoorInteraction || !spec.delivery.routeEndsWithUpperDoorOpen) fail('delivery contract changed')

const full = spec.routes.full.frames
if (full.length !== 111 || spec.routeNotes.v4ApprovedPrefixFrames !== 88 || spec.routeNotes.newTailFrames !== 23) fail('complete route frame count changed')
const clean = (value: any) => { const frame = { ...value }; delete frame.src; delete frame.upperDoorOpen; return frame }
for (let index = 0; index < 88; index++) {
  const frame = full[index]
  const approved = v4.routes.full.frames[index]
  if (JSON.stringify(clean(frame)) !== JSON.stringify(clean(approved))) fail(`approved V4 prefix metadata changed at F${index + 1}`)
  if (frame.upperDoorOpen !== 0) fail(`approved V4 prefix door state changed at F${index + 1}`)
  if (!frame.src.startsWith('/keeper-review/keeper-prime-ladder-transitions-v5/assets/')) fail(`stale asset prefix at F${index + 1}`)
}
const tail = full.slice(88)
const expectedRoots = [145.375, 147, 147.875, 148.25, 148.25, 148.25, 148.25, 148.25, 148.25, 148.25, 148.25, 148.625, 149.5, 151.125, 153.5, 156.125, 158.75, 161.375, 164, 166.625, 169.25, 171.875, 174.5]
const expectedDoorStates = [0, 0, 0, 0, 0, 0, 1 / 3, 2 / 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
if (JSON.stringify(tail.map((frame: any) => frame.xLp)) !== JSON.stringify(expectedRoots)) fail('door-tail root table changed')
if (JSON.stringify(tail.map((frame: any) => frame.upperDoorOpen)) !== JSON.stringify(expectedDoorStates)) fail('door-tail opening table changed')
if (!tail[4].phase.includes('right hand begins') || !tail[5].phase.includes('right hand meets') || !tail[10].phase.includes('brief exact side neutral') || !tail[15].phase.includes('cross registered') || !tail.at(-1).phase.includes('opaque open door leaf')) fail('door-tail semantic sequence changed')
if (spec.routeNotes.upperDoorStopRootLp !== door.stopRootXLp || spec.routeNotes.upperDoorTransferRootLp !== door.transferRootXLp || spec.routeNotes.upperDoorHiddenRootLp !== door.hiddenRootXLp) fail('route-note anchors disagree with geometry')

const turnFrames = Object.values<any>(spec.routes).flatMap((route: any) => route.frames).filter((frame: any) => frame.phase?.includes('turn'))
if (!turnFrames.length || turnFrames.some((frame: any) => frame.durationMs !== 50)) fail('approved V4 turn timing changed')
if (spec.timing.deferredTurnFrameMs !== 25 || spec.timing.deferredTurnTimingImplemented !== false || register.changes.v4TurnTimingChanged !== false) fail('deferred turn timing contract changed')

const approvedAssets = register.publishedAssets.filter((asset: any) => asset.role === 'approved-v4')
const reachAssets = register.publishedAssets.filter((asset: any) => asset.role.startsWith('door-reach-'))
if (approvedAssets.length !== 29 || reachAssets.length !== 2 || register.publishedAssets.length !== 31) fail('asset inventory changed')
for (const asset of approvedAssets) {
  const v4Asset = v4Register.publishedAssets.find((entry: any) => entry.draft === asset.source)
  const source = path.join(root, asset.source)
  const draft = path.join(root, asset.draft)
  const published = path.join(root, asset.published)
  if (!v4Asset || v4Asset.draftSha256 !== asset.sourceSha256) fail(`approved V4 asset not pinned: ${asset.source}`)
  if (!fs.existsSync(source) || sha(source) !== asset.sourceSha256 || !fs.existsSync(draft) || sha(draft) !== asset.draftSha256 || asset.sourceSha256 !== asset.draftSha256) fail(`approved V4 bytes changed: ${asset.draft}`)
  if (!fs.existsSync(published) || sha(published) !== asset.draftSha256) fail(`published/draft mismatch: ${asset.published}`)
}
for (const asset of reachAssets) {
  const sourceFile = path.join(root, asset.source)
  const draftFile = path.join(root, asset.draft)
  const publishedFile = path.join(root, asset.published)
  if (!fs.existsSync(sourceFile) || sha(sourceFile) !== asset.sourceSha256 || !fs.existsSync(draftFile) || sha(draftFile) !== asset.draftSha256 || !fs.existsSync(publishedFile) || sha(publishedFile) !== asset.draftSha256) fail(`door-reach provenance changed: ${asset.role}`)
  const source = PNG.sync.read(fs.readFileSync(sourceFile))
  const draft = PNG.sync.read(fs.readFileSync(draftFile))
  if (source.width !== draft.width || source.height !== draft.height) fail(`door-reach cell geometry changed: ${asset.role}`)
  let hardened = 0
  let fringe = 0
  let edgeAlpha = 0
  for (let offset = 0; offset < draft.data.length; offset += 4) {
    const alpha = source.data[offset + 3]
    const expectedAlpha = alpha >= 240 ? 255 : alpha
    if (draft.data[offset + 3] !== expectedAlpha) fail(`wrong alpha transform: ${asset.role}`)
    for (let channel = 0; channel < 3; channel++) if (draft.data[offset + channel] !== source.data[offset + channel]) fail(`RGB changed: ${asset.role}`)
    hardened += Number(alpha >= 240 && alpha !== 255)
    fringe += Number(alpha > 0 && alpha < 240)
  }
  for (let x = 0; x < draft.width; x++) edgeAlpha += Number(draft.data[x * 4 + 3] > 0) + Number(draft.data[((draft.height - 1) * draft.width + x) * 4 + 3] > 0)
  for (let y = 1; y < draft.height - 1; y++) edgeAlpha += Number(draft.data[y * draft.width * 4 + 3] > 0) + Number(draft.data[(y * draft.width + draft.width - 1) * 4 + 3] > 0)
  if (hardened !== asset.hardenedPixels || fringe !== asset.preservedFringePixels || edgeAlpha !== 0) fail(`door-reach alpha/gutter audit changed: ${asset.role}`)
}

if (!register.changes.persistentCompositor || !register.changes.upperDoorOpensOutward || !register.changes.upperDoorOccludesKeeper || !register.changes.upperDoorRemainsOpenAtEnd || register.changes.costumeSpecificDoorAnimationRequired || register.changes.upperDoorOrientationToCameraDeg !== 90 || register.changes.ladderPixelsSuppressed || register.changes.finalChanged || register.changes.runtimeChanged || register.changes.productionChanged) fail('change boundary widened or door contract missing')
if (register.approvalBoundary.candidateApproved || register.approvalBoundary.finalLaneEntryAllowed || register.approvalBoundary.productionPromotionAllowed) fail('unapproved candidate promoted')

const html = fs.readFileSync(pageFile, 'utf8')
for (const required of ['Keeper Prime ladder transitions V5', "let routeId='full'", 'routeSelect.value=routeId', '111 frames', 'Door remains open', 'closes only after his later return from the room', 'Door complete', 'prepareStage(stage)', 'decoded.get(src).cloneNode()', "nodes.rightDoor.style.zIndex=open>.8?'8':'3'", '155.5+3*open', '12.5+7.5*open', '← Frame', 'Frame →']) {
  if (!html.includes(required)) fail(`review contract missing: ${required}`)
}
const renderStart = html.indexOf('function renderStage(stage)')
const renderEnd = html.indexOf('function render()', renderStart)
if (renderStart < 0 || renderEnd < 0) fail('persistent compositor functions missing')
const renderBody = html.slice(renderStart, renderEnd)
for (const forbidden of ['createElement', 'append(', 'appendChild', 'replaceChildren', '.src=']) if (renderBody.includes(forbidden)) fail(`playback mutates DOM/assets: ${forbidden}`)
const urls = new Set(Object.values<any>(spec.routes).flatMap((route: any) => route.frames.map((frame: any) => frame.src)))
if (urls.size !== 31) fail(`unexpected unique frame count: ${urls.size}`)

console.log(JSON.stringify({
  ok: true,
  completeRouteFrames: full.length,
  approvedV4PrefixFrames: 88,
  newDoorTailFrames: tail.length,
  uniqueFrames: urls.size,
  doorOrientationToCameraDeg: 90,
  doorOpensOutward: true,
  doorRemainsOpenAfterRoomEntry: true,
  costumeSpecificDoorAnimationRequired: false,
  finalVisibleCellFullyOccluded: true,
  v4TurnTimingChanged: false,
  productionChanged: false,
}, null, 2))
