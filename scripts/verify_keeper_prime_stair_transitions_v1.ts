#!/usr/bin/env node
/** Deterministic contract for the reversible Keeper Prime stair-transition review. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const SET = 'keeper-prime-stair-transitions-v1'
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-transitions-2026-10-15-v1')
const SPEC_FILE = path.join(PACK, 'keeper-prime-stair-transitions-v1.json')
const REGISTER_FILE = path.join(PACK, 'batch-register.json')
const PAGE_FILE = path.join(ROOT, 'public/keeper-review', SET, 'index.html')
const STAIR_RIG_FILE = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16/stair-contact-rig-v16.json')
const REJECTED = [
  path.join(PACK, 'sources/rejected/keeper-prime-top-landing-pass-too-wide.png'),
  path.join(PACK, 'sources/rejected/keeper-prime-top-landing-pass-rejected-three-arms.png'),
]
const fail = (message: string): never => { throw new Error(`Keeper Prime stair transitions V1: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const close = (actual: number, expected: number, label: string) => {
  if (Math.abs(actual - expected) > 1e-9) fail(`${label}: expected ${expected}, got ${actual}`)
}

for (const file of [SPEC_FILE, REGISTER_FILE, PAGE_FILE, STAIR_RIG_FILE, ...REJECTED, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}

const spec = JSON.parse(fs.readFileSync(SPEC_FILE, 'utf8')) as Record<string, any>
const record = JSON.parse(fs.readFileSync(REGISTER_FILE, 'utf8')) as Record<string, any>
const stairRig = JSON.parse(fs.readFileSync(STAIR_RIG_FILE, 'utf8')) as Record<string, any>
const page = fs.readFileSync(PAGE_FILE, 'utf8')
const lower = spec.routes.lowerJoin.frames as Array<Record<string, any>>
const upper = spec.routes.upperExit.frames as Array<Record<string, any>>
const full = spec.routes.fullFlow.frames as Array<Record<string, any>>

if (spec.schema !== 'lighthouse-keeper/stair-transitions@1' || record.batchId !== 'keeper-prime-stair-transitions-2026-10-15-v1') fail('identity changed')
if (record.status !== 'draft-two-route-transition-review-awaiting-frank' || spec.status !== record.status) fail('draft approval status changed')
if (record.spec.sha256 !== hash(SPEC_FILE) || record.reviewPage.sha256 !== hash(PAGE_FILE)) fail('spec/page hash disagreement')
for (const authority of Object.values(record.authorities) as Array<Record<string, string>>) {
  const file = path.join(ROOT, authority.file)
  if (!fs.existsSync(file) || hash(file) !== authority.sha256) fail(`authority changed: ${authority.file}`)
}

if (record.publishedAssets.length !== 27 || record.validation.uniquePublishedFrames !== 27) fail('expected 27 unique authority/candidate frames')
const publishedHashes = new Set<string>()
const publishedUrls = new Set<string>()
for (const asset of record.publishedAssets as Array<Record<string, string>>) {
  const source = path.join(ROOT, asset.source)
  const publicFile = path.join(ROOT, 'public', asset.url.replace(/^\//, ''))
  if (!asset.url.startsWith(`/keeper-review/${SET}/assets/frame-`) || !asset.url.endsWith('.png')) fail(`bad published URL ${asset.url}`)
  if (!fs.existsSync(source) || hash(source) !== asset.sourceSha256) fail(`source hash changed: ${asset.source}`)
  if (!fs.existsSync(publicFile) || hash(publicFile) !== asset.sourceSha256) fail(`published bytes disagree: ${asset.url}`)
  const png = PNG.sync.read(fs.readFileSync(publicFile))
  if (png.width !== 256 || png.height !== 320) fail(`cell geometry changed: ${asset.url}`)
  let edgeAlpha = 0
  for (let x = 0; x < png.width; x++) edgeAlpha += png.data[(x * 4) + 3] + png.data[(((png.height - 1) * png.width + x) * 4) + 3]
  for (let y = 1; y < png.height - 1; y++) edgeAlpha += png.data[(y * png.width * 4) + 3] + png.data[((y * png.width + png.width - 1) * 4) + 3]
  if (edgeAlpha !== 0) fail(`non-transparent cell safety edge: ${asset.url}`)
  if (publishedHashes.has(asset.sourceSha256) || publishedUrls.has(asset.url)) fail('published frame deduplication changed')
  publishedHashes.add(asset.sourceSha256)
  publishedUrls.add(asset.url)
}
for (const rejected of REJECTED) {
  if (publishedHashes.has(hash(rejected))) fail(`rejected study was published: ${path.basename(rejected)}`)
  if (page.includes(path.basename(rejected))) fail(`rejected study was loaded by page: ${path.basename(rejected)}`)
}
const routeUrls = new Set([...lower, ...upper, ...full].map((frame) => frame.src))
if (routeUrls.size !== 27 || [...routeUrls].some((url) => !publishedUrls.has(url))) fail('route/public frame set disagreement')

if (lower.length !== 23 || upper.length !== 92 || full.length !== 130) fail('route frame counts changed')
if (spec.units.kuPerLp !== 8 || spec.units.walkDeltaKu !== 21 || spec.units.walkDeltaLp !== 2.625) fail('walk units changed')
if (spec.geometry.stair.risers !== 14 || spec.geometry.stair.treadRunLp !== 7 || spec.geometry.stair.flightRunLp !== 98 || spec.geometry.stair.flightRiseLp !== 60) fail('stair geometry changed')
close(spec.geometry.transferDoorXLp, 140.5, 'door axis')
close(spec.geometry.hiddenRootXLp, 161.5, 'hidden root')
close(spec.geometry.lowerStairRootLp, 119.5, 'lower stair root')
close(spec.geometry.upperLandingRootLp, 14.5, 'upper landing root')
close(spec.geometry.upperDoorStopRootLp, 130, 'upper door stop root')
close(spec.geometry.upperDoorHandleXLp, 144, 'upper door handle')
close(spec.geometry.lowerDoorToStairLp, 21, 'lower door-to-stair distance')
close(spec.geometry.upperLandingToDoorLp, 126, 'landing-to-door distance')
close(spec.geometry.doorToHiddenLp, 21, 'door-to-hidden distance')

for (let index = 0; index < 16; index++) {
  const frame = lower[index]
  if (frame.sourceFrame !== `walk:${(index % 8) + 1}` || frame.flipX !== true) fail(`lower walk frame ${index + 1} identity changed`)
  close(frame.xLp, 161.5 - ((index + 1) * 2.625), `lower walk frame ${index + 1} root`)
  if (index > 0 && frame.xLp === lower[index - 1].xLp) fail(`lower walk frame ${index + 1} walks on spot`)
}
close(lower[15].xLp, 119.5, 'last lower walk root')
if (lower[15].sourceFrame !== 'walk:8' || lower[16].sourceFrame !== 'stair:1' || lower[16].xLp === lower[15].xLp) fail('walk-to-stair moving join changed')
for (let index = 0; index < 7; index++) {
  const actual = lower[16 + index]
  const expected = stairRig.timeline[index]
  if (actual.sourceFrame !== `stair:${expected.frame}`) fail(`lower stair frame ${index + 1} identity changed`)
  close(actual.xLp, expected.xLp, `lower stair frame ${index + 1} x`)
  close(actual.bottomLp, expected.bottomLp, `lower stair frame ${index + 1} bottom`)
}

const lastFive = stairRig.timeline.slice(-5)
for (let index = 0; index < 5; index++) {
  const frame = upper[index]
  if (frame.sourceFrame !== `stair:${lastFive[index].frame}`) fail(`upper approach frame ${index + 1} changed`)
  close(frame.xLp, lastFive[index].xLp, `upper approach frame ${index + 1} x`)
  close(frame.bottomLp, lastFive[index].bottomLp, `upper approach frame ${index + 1} bottom`)
}
if (upper[5].sourceFrame !== 'walk:3' || upper[5].flipX !== true) fail('compact landing pass changed')
close(upper[5].xLp, 20.5, 'landing pass root')
if (upper[6].sourceFrame !== 'side-back:1' || upper[6].flipX !== true) fail('landing settle authority changed')
close(upper[6].xLp, 14.5, 'landing settle root')
const expectedTurnSources = ['side-back:2', 'side-back:3', 'side-back:4', 'side-back:5', 'side-back:6', 'side-back:7', 'side-back:8', 'side-back:9', 'side-back:8', 'side-back:7', 'side-back:6', 'side-back:5', 'side-back:4', 'side-back:3', 'side-back:2', 'side-back:1']
for (let index = 0; index < expectedTurnSources.length; index++) {
  const frame = upper[7 + index]
  if (frame.sourceFrame !== expectedTurnSources[index]) fail(`turn frame ${index + 1} order changed`)
  if (frame.flipX !== (index < 8)) fail(`turn frame ${index + 1} mirroring changed`)
  close(frame.xLp, 14.5, `turn frame ${index + 1} root`)
}
if (!spec.rootMotion.turnParityRule.includes('bottom-right→top-left') || !spec.rootMotion.turnParityRule.includes('side-left→back→side-right') || !spec.rootMotion.turnParityRule.includes('side-right→front→side-left')) fail('clockwise turn parity rule changed')

const acceleration = upper.slice(23, 27)
const expectedDeltas = [3, 7, 13, 19]
let rootLp = 14.5
for (let index = 0; index < acceleration.length; index++) {
  const frame = acceleration[index]
  rootLp += expectedDeltas[index] / 8
  if (frame.sourceFrame !== `bridge:${index + 2}` || frame.deltaKu !== expectedDeltas[index]) fail(`acceleration frame ${index + 1} changed`)
  close(frame.xLp, rootLp, `acceleration frame ${index + 1} root`)
}
close(rootLp, 19.75, 'candidate-42 endpoint')
if (spec.rootMotion.upperAccelerationCandidate.id !== 'candidate-42' || spec.rootMotion.upperAccelerationCandidate.approved === true || record.approvalBoundary.candidate42RootMotionApproved !== false) fail('candidate-42 approval boundary changed')

const hallway = upper.slice(27, 67)
if (hallway.length !== 40) fail('hallway approach frame count changed')
for (let index = 0; index < hallway.length; index++) {
  const frame = hallway[index]
  close(frame.xLp, 19.75 + ((index + 1) * 2.625), `hallway frame ${index + 1} root`)
  if (index > 0 && frame.xLp === hallway[index - 1].xLp) fail(`hallway frame ${index + 1} walks on spot`)
}
close(hallway[39].xLp, 124.75, 'door approach steady endpoint')
if (hallway[39].sourceFrame !== 'walk:1') fail('door approach no longer ends on Walk F1')
const deceleration = upper.slice(67, 71)
const decelDeltas = [19, 13, 7, 3]
rootLp = 124.75
for (let index = 0; index < deceleration.length; index++) {
  const frame = deceleration[index]
  rootLp += decelDeltas[index] / 8
  if (frame.sourceFrame !== `bridge:${4 - index}` || frame.deltaKu !== decelDeltas[index]) fail(`door deceleration frame ${index + 1} changed`)
  close(frame.xLp, rootLp, `door deceleration frame ${index + 1} root`)
}
close(rootLp, 130, 'door stop root')

const doorAction = upper.slice(71, 78)
const doorSources = ['door-reach:partial', 'door-reach:full', 'door-reach:full', 'door-reach:full', 'door-reach:full', 'door-reach:partial', 'side-back:1']
const doorOpen = [0, 0, 1 / 3, 2 / 3, 1, 1, 1]
for (let index = 0; index < doorAction.length; index++) {
  const frame = doorAction[index]
  if (frame.sourceFrame !== doorSources[index]) fail(`door action frame ${index + 1} identity changed`)
  close(frame.xLp, 130, `door action frame ${index + 1} root`)
  close(frame.upperDoorOpen, doorOpen[index], `door action frame ${index + 1} opening`)
}
const doorAcceleration = upper.slice(78, 82)
rootLp = 130
for (let index = 0; index < doorAcceleration.length; index++) {
  rootLp += expectedDeltas[index] / 8
  if (doorAcceleration[index].sourceFrame !== `bridge:${index + 2}`) fail(`door restart frame ${index + 1} changed`)
  close(doorAcceleration[index].xLp, rootLp, `door restart frame ${index + 1} root`)
}
close(rootLp, 135.25, 'door restart endpoint')
const doorWalk = upper.slice(82)
if (doorWalk.length !== 10) fail('door exit walk count changed')
for (let index = 0; index < doorWalk.length; index++) close(doorWalk[index].xLp, 135.25 + ((index + 1) * 2.625), `door exit frame ${index + 1} root`)
close(doorWalk[1].xLp, 140.5, 'open-door crossing frame')
close(doorWalk[9].xLp, 161.5, 'fully hidden endpoint')
if (record.validation.upperDoorCrossingAfterRestartFrame !== 2 || record.validation.walkingOnSpotFrames !== 0 || record.validation.clockwiseLandingTurnViaBack !== true || record.validation.doorReachCandidateFrames !== 2) fail('door/turn validation changed')

const reachCandidates = record.generation.doorReachCandidates as Array<Record<string, any>>
if (reachCandidates.length !== 2 || record.approvalBoundary.doorReachArtworkApproved !== false) fail('door-reach candidate boundary changed')
const maskRecord = record.generation.doorReachMask as Record<string, any>
const maskFile = path.join(ROOT, maskRecord.file)
const neutralFile = path.join(ROOT, maskRecord.outsideMaskAuthority)
if (!fs.existsSync(maskFile) || hash(maskFile) !== maskRecord.sha256 || hash(neutralFile) !== maskRecord.outsideMaskAuthoritySha256) fail('door-reach mask/neutral authority changed')
const mask = PNG.sync.read(fs.readFileSync(maskFile))
const neutral = PNG.sync.read(fs.readFileSync(neutralFile))
if (mask.width !== 256 || mask.height !== 320 || neutral.width !== 256 || neutral.height !== 320) fail('door-reach mask/authority geometry changed')
for (const candidate of reachCandidates) {
  for (const item of [candidate.source, candidate.registeredSource, candidate.maskedDraft]) {
    const file = path.join(ROOT, item.file)
    if (!fs.existsSync(file) || hash(file) !== item.sha256) fail(`door-reach provenance changed: ${item.file}`)
  }
  const draft = PNG.sync.read(fs.readFileSync(path.join(ROOT, candidate.maskedDraft.file)))
  if (draft.width !== 256 || draft.height !== 320) fail(`door-reach candidate cell changed: ${candidate.role}`)
  for (let offset = 0; offset < draft.data.length; offset += 4) {
    if (mask.data[offset] !== 0) continue
    for (let channel = 0; channel < 4; channel++) if (draft.data[offset + channel] !== neutral.data[offset + channel]) fail(`out-of-mask pixel changed in ${candidate.role}`)
  }
  if (!publishedHashes.has(candidate.maskedDraft.sha256)) fail(`door-reach candidate not published: ${candidate.role}`)
}

const fullStair = full.slice(16, 43)
if (fullStair.length !== 27) fail('full flow no longer contains complete approved stair flight')
for (let index = 0; index < fullStair.length; index++) {
  if (fullStair[index].sourceFrame !== `stair:${stairRig.timeline[index].frame}`) fail(`full-flow stair frame ${index + 1} changed`)
  close(fullStair[index].xLp, stairRig.timeline[index].xLp, `full-flow stair frame ${index + 1} x`)
  close(fullStair[index].bottomLp, stairRig.timeline[index].bottomLp, `full-flow stair frame ${index + 1} bottom`)
}

for (const token of ['Previous frame', 'Next frame', 'Exact game scale', '1 CSS px = 1 logical px.', 'Root guide', 'Door occlusion', 'Promise.all(unique.map(preload))', 'im.decode', 'clockwise turn via the back view', 'reaches with his right hand', 'three-armed result', 'doorKnob']) {
  if (!page.includes(token)) fail(`review control/evidence missing: ${token}`)
}
if ([...routeUrls].some((url) => !page.includes(url))) fail('review page/spec URL disagreement')
if (spec.boundaries.newKeeperDoorReachArtworkPresent !== true) fail('door-reach candidate presence changed')
for (const flag of ['approvedSourcePixelsChanged', 'newKeeperArtworkAccepted', 'rejectedGeneratedStudyUsed', 'finalChanged', 'runtimeChanged', 'productionChanged']) if (spec.boundaries[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['reviewCandidateApproved', 'candidate42RootMotionApproved', 'doorReachArtworkApproved', 'finalLaneEntryAllowed', 'productionPromotionAllowed']) if (record.approvalBoundary[flag] !== false) fail(`${flag} approval changed`)

console.log('Keeper Prime stair transitions V1 verified: 27 deduplicated authority/candidate frames; transparent 256×320 cells; rejected studies excluded; clockwise landing turn; exact stop/restart roots; masked two-frame right-hand door reach; animated opening and full occlusion all agree.')
