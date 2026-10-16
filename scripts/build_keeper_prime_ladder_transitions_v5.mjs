#!/usr/bin/env node
/** Build Ladder Transition V5: approved V4 plus a complete upper-door exit. */

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const v4Set = 'keeper-prime-ladder-transitions-v4'
const set = 'keeper-prime-ladder-transitions-v5'
const v4Pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v4')
const pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v5')
const framesDir = path.join(pack, 'drafts/frames')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const v4SpecFile = path.join(v4Pack, 'keeper-prime-ladder-transitions-v4.json')
const v4RegisterFile = path.join(v4Pack, 'batch-register.json')
const v4ApprovalFile = path.join(root, 'docs/review/keeper-prime-ladder-transitions-v4-approval-2026-10-16.json')
const v4PageFile = path.join(root, 'public/keeper-review', v4Set, 'index.html')
const specFile = path.join(pack, 'keeper-prime-ladder-transitions-v5.json')
const pageFile = path.join(publicDir, 'index.html')
const solidPaintFloor = 240
const reachSources = [
  ['partial', 'art/drafts/keeper-prime-stair-transitions-2026-10-15-v1/drafts/frames/keeper_prime_door-reach-right_partial.png'],
  ['full', 'art/drafts/keeper-prime-stair-transitions-2026-10-15-v1/drafts/frames/keeper_prime_door-reach-right_full.png'],
]

const read = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = file => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n') }
for (const file of [v4SpecFile, v4RegisterFile, v4ApprovalFile, v4PageFile]) if (!fs.existsSync(file)) throw new Error(`missing ${file}`)
fs.mkdirSync(framesDir, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const v4Spec = read(v4SpecFile)
const v4Register = read(v4RegisterFile)
const spec = structuredClone(v4Spec)
spec.set = set
spec.status = 'draft-awaiting-upper-door-flow-review'
spec.geometry.upperDoor = {
  orientationToCameraDeg: 90,
  opensOutwardIntoHallway: true,
  occludesKeeperWhenOpen: true,
  frameLeftLp: 150,
  frameWidthLp: 18,
  leafClosedLeftLp: 155.5,
  leafClosedWidthLp: 12.5,
  leafOpenLeftLp: 158.5,
  leafOpenWidthLp: 20,
  handleXLp: 162,
  stopRootXLp: 148.25,
  transferRootXLp: 158.75,
  hiddenRootXLp: 174.5,
}
spec.doorPolicy = {
  opensTowardKeeperIntoHallway: true,
  remainsOpenAfterRoomEntry: true,
  closesOnlyAfterKeeperLaterLeavesRoom: true,
  costumeChangeAllowedOnlyUnderFullDoorOcclusion: true,
  costumeSpecificDoorAnimationRequired: false,
}
spec.delivery = { ...spec.delivery, defaultRoute: 'full', completeUpperDoorInteraction: true, routeEndsWithUpperDoorOpen: true }
spec.timing = { ...spec.timing, doorActionFrameMs: [100, 120, 90, 90, 140, 100, 70], deferredTurnFrameMs: 25, deferredTurnTimingImplemented: false }

const urlMap = new Map()
const publishedAssets = []
for (const entry of v4Register.publishedAssets) {
  const source = path.join(root, entry.draft)
  if (!fs.existsSync(source) || sha(source) !== entry.draftSha256) throw new Error(`V4 authority drift: ${entry.draft}`)
  const draft = path.join(framesDir, path.basename(entry.draft))
  fs.copyFileSync(source, draft)
  const digest = sha(draft)
  const publicName = `${path.basename(draft, '.png')}-${digest.slice(0, 16)}.png`
  const published = path.join(assetsDir, publicName)
  fs.copyFileSync(draft, published)
  const url = `/keeper-review/${set}/assets/${publicName}`
  urlMap.set(entry.url, url)
  publishedAssets.push({ role: 'approved-v4', source: rel(source), sourceSha256: digest, draft: rel(draft), draftSha256: digest, published: rel(published), url, bytes: fs.statSync(published).size, changeScope: 'byte-identical approved V4 artwork' })
}

const reachUrls = {}
for (const [role, relativeSource] of reachSources) {
  const source = path.join(root, relativeSource)
  const input = PNG.sync.read(fs.readFileSync(source))
  const output = new PNG({ width: input.width, height: input.height })
  let hardenedPixels = 0
  let preservedFringePixels = 0
  for (let offset = 0; offset < input.data.length; offset += 4) {
    for (let channel = 0; channel < 4; channel++) output.data[offset + channel] = input.data[offset + channel]
    const alpha = input.data[offset + 3]
    if (alpha >= solidPaintFloor) { output.data[offset + 3] = 255; hardenedPixels += Number(alpha !== 255) }
    else if (alpha > 0) preservedFringePixels++
  }
  const draft = path.join(framesDir, `keeper_prime_door-reach-right_${role}-paint-opaque.png`)
  fs.writeFileSync(draft, PNG.sync.write(output))
  const digest = sha(draft)
  const publicName = `${path.basename(draft, '.png')}-${digest.slice(0, 16)}.png`
  const published = path.join(assetsDir, publicName)
  fs.copyFileSync(draft, published)
  const url = `/keeper-review/${set}/assets/${publicName}`
  reachUrls[role] = url
  publishedAssets.push({ role: `door-reach-${role}`, source: relativeSource, sourceSha256: sha(source), draft: rel(draft), draftSha256: digest, published: rel(published), url, bytes: fs.statSync(published).size, changeScope: `alpha >= ${solidPaintFloor} made opaque; fringe and RGB retained`, hardenedPixels, preservedFringePixels })
}

for (const route of Object.values(spec.routes)) for (const frame of route.frames) {
  const next = urlMap.get(frame.src)
  if (!next) throw new Error(`unmapped V4 URL: ${frame.src}`)
  frame.src = next
}

const findUrl = needle => {
  const entry = publishedAssets.find(asset => asset.role === 'approved-v4' && asset.source.includes(needle))
  if (!entry) throw new Error(`missing role asset: ${needle}`)
  return entry.url
}
const y = 56
const scale = 0.9430570303418159
const frame = (src, xLp, durationMs, phase, label, upperDoorOpen = 0) => ({ src, xLp, rootYLp: y, artScale: scale, durationMs, phase, label, upperDoorOpen })
const approvedPrefix = spec.routes.full.frames.slice(0, 88).map(value => ({ ...value, upperDoorOpen: 0 }))
const stop = 148.25
const doorTail = [
  frame(findUrl('stop-to-walk-right_f4'), 145.375, 70, 'decelerate to upper-door handle', 'approved bridge F4 · +2.375 lp'),
  frame(findUrl('stop-to-walk-right_f3'), 147, 80, 'decelerate to upper-door handle', 'approved bridge F3 · +1.625 lp'),
  frame(findUrl('stop-to-walk-right_f2'), 147.875, 90, 'decelerate to upper-door handle', 'approved bridge F2 · +0.875 lp'),
  frame(findUrl('stop-to-walk-right_f1'), stop, 100, 'decelerate to upper-door handle', 'approved side neutral · +0.375 lp'),
  frame(reachUrls.partial, stop, 100, 'right hand begins reaching for handle', 'approved stair-route door reach · partial'),
  frame(reachUrls.full, stop, 120, 'right hand meets handle', 'approved stair-route door reach · full contact'),
  frame(reachUrls.full, stop, 90, 'right hand pulls; door starts opening', 'door one-third open', 1 / 3),
  frame(reachUrls.full, stop, 90, 'right hand pulls; door continues opening', 'door two-thirds open', 2 / 3),
  frame(reachUrls.full, stop, 140, 'door reaches fully open position', 'door fully open', 1),
  frame(reachUrls.partial, stop, 100, 'right hand retracts from handle', 'door reach retracts', 1),
  frame(findUrl('turn_side-right_to_back_f01'), stop, 70, 'brief exact side neutral before stepping through', 'approved side authority', 1),
  frame(findUrl('stop-to-walk-right_f2'), 148.625, 70, 'accelerate through open doorway', 'approved bridge F2 · +0.375 lp', 1),
  frame(findUrl('stop-to-walk-right_f3'), 149.5, 70, 'accelerate through open doorway', 'approved bridge F3 · +0.875 lp', 1),
  frame(findUrl('stop-to-walk-right_f4'), 151.125, 70, 'accelerate through open doorway', 'approved bridge F4 · +1.625 lp', 1),
  frame(findUrl('walk-right_f1'), 153.5, 62.5, 'accelerate through open doorway', 'approved Walk V6 F1 · +2.375 lp', 1),
]
const exitRoles = ['walk-right_f2', 'walk-right_f3', 'walk-right_f4', 'walk-right_f5', 'walk-right_f6', 'walk-right_f7', 'walk-right_f8', 'walk-right_f1']
for (let index = 0; index < exitRoles.length; index++) {
  const xLp = 156.125 + index * 2.625
  const phase = index === 0 ? 'cross registered open doorway' : 'continue behind opaque open door leaf'
  doorTail.push(frame(findUrl(exitRoles[index]), xLp, 62.5, phase, `approved walk ${exitRoles[index].split('_').at(-1)}`, 1))
}
spec.routes.full = {
  ...spec.routes.full,
  title: '5. Complete room → ladder → next-floor door flow',
  frames: [...approvedPrefix, ...doorTail],
}
spec.routeNotes = {
  v4ApprovedPrefixFrames: 88,
  newTailFrames: doorTail.length,
  upperDoorStopRootLp: stop,
  upperDoorTransferRootLp: 158.75,
  upperDoorHiddenRootLp: 174.5,
  timingNote: 'V4-approved 50-ms turn frames remain unchanged; Frank requested a later separate 25-ms timing-only pass.',
}
writeJson(specFile, spec)

let html = fs.readFileSync(v4PageFile, 'utf8')
html = html.replaceAll('Keeper Prime ladder transitions V4', 'Keeper Prime ladder transitions V5')
html = html.replace(
  'Flicker correction of V3: Keeper interior paint is opaque, the original smooth antialiased fringe is restored, and every decoded frame remains mounted throughout playback. Timing and geometry are unchanged.',
  'Whole-flow extension of approved V4: after the ladder landing the Keeper now completes a measured stop, right-hand door reach, opening and fully obscured exit. V4 artwork and compositor remain exact.',
)
html = html.replace(
  'Four exact mirrored left/right gait cycles close the storey without phase remainder. Turns remain 20 fps and climbing 6.67 fps. The complete ladder is persistent and no playback frame rebuilds the scene.',
  'The approved ladder route now continues through the upper door: one complete post-turn walk cycle, exact reverse bridge stop, right-hand reach/open, brief neutral, restart and full door occlusion. The requested 2× turn timing remains deferred.',
)
html = html.replace(
  '.door{position:absolute;background:#315363;border:2px solid #91aab6;z-index:8}',
  '.door{position:absolute;background:#315363;border:2px solid #91aab6;z-index:8}.doorFrame{position:absolute;background:#142d39;border:2px solid #91aab6;z-index:3}.doorLeaf{position:absolute;background:linear-gradient(90deg,#284756,#426574);border-left:2px solid #a8c0ca;z-index:3;will-change:left,width}.doorKnob{position:absolute;border-radius:50%;background:#f5c842;border:1px solid #5c4611;z-index:4;will-change:left}',
)
html = html.replace(
  '<section class="metrics"><article><b>Opaque paint</b>',
  '<section class="metrics"><article><b>111 frames</b>complete lower-room to upper-room flow</article><article><b>Door remains open</b>it closes only after the later return from the room</article><article><b>Door complete</b>stop · reach · open · restart · disappear</article><article><b>Opaque paint</b>',
)
html = html.replace(
  'Inspect the complete route for any flash or blank repaint: all Keeper frames and the complete ladder are mounted before playback begins. Rungs remain visible through genuine gaps but cannot bleed through solid Keeper paint. Timing, roots, geometry and the accepted hand/foot rung tolerance are unchanged from V2/V3.',
  'Inspect the default complete route from lower-room emergence to full upper-door disappearance. Judge the new F89–F111 door tail: the walk must decelerate naturally, the right hand must meet the handle, the door must open toward him before restart, and the Keeper must finish fully obscured while the door stays open. It closes only after his later return from the room. Approved V4 F1–F88 remain exact.',
)
html = html.replace(/const SPEC=.*?;\nconst routeSelect=/s, `const SPEC=${JSON.stringify(spec)};\nconst routeSelect=`)
html = html.replace("let routeId='gait',index=0", "let routeId='full',index=0")
html = html.replace(
  "for(const [id,route] of Object.entries(SPEC.routes)){const option=document.createElement('option');option.value=id;option.textContent=route.title;routeSelect.append(option)}",
  "for(const [id,route] of Object.entries(SPEC.routes)){const option=document.createElement('option');option.value=id;option.textContent=route.title;routeSelect.append(option)}routeSelect.value=routeId",
)
const oldDoors = "nodes.leftDoor=add(world,'door',8,68,24,48,scale);nodes.rightDoor=add(world,'door',158,8,14,48,scale);"
const newDoors = "nodes.leftDoor=add(world,'door',8,68,24,48,scale);nodes.rightFrame=add(world,'doorFrame',150,8,18,48,scale);nodes.rightDoor=add(world,'doorLeaf',155.5,8,12.5,48,scale);nodes.rightKnob=add(world,'doorKnob',161.3,30.3,1.4,1.4,scale);"
if (!html.includes(oldDoors)) throw new Error('V4 persistent door construction changed')
html = html.replace(oldDoors, newDoors)
const oldDoorRender = "nodes.leftDoor.style.visibility=(routeId==='approach'||routeId==='full')?'visible':'hidden';nodes.rightDoor.style.visibility=(routeId==='exit'||routeId==='full')?'visible':'hidden';const img="
const newDoorRender = "nodes.leftDoor.style.visibility=(routeId==='approach'||routeId==='full')?'visible':'hidden';const showRight=(routeId==='exit'||routeId==='full'),open=frame.upperDoorOpen||0;for(const doorNode of [nodes.rightFrame,nodes.rightDoor,nodes.rightKnob])doorNode.style.visibility=showRight?'visible':'hidden';nodes.rightDoor.style.left=px(155.5+3*open,scale);nodes.rightDoor.style.width=px(12.5+7.5*open,scale);nodes.rightDoor.style.zIndex=open>.8?'8':'3';nodes.rightKnob.style.left=px(161.3+7*open,scale);nodes.rightKnob.style.zIndex=open>.8?'9':'4';const img="
if (!html.includes(oldDoorRender)) throw new Error('V4 persistent door render changed')
html = html.replace(oldDoorRender, newDoorRender)
fs.writeFileSync(pageFile, html)

fs.writeFileSync(path.join(pack, 'HANDOFF.md'), `# Keeper Prime ladder transitions V5

V5 is the first complete lower-room to upper-room ladder flow. Frames 1–88 are exact approved V4 route frames under a fresh asset prefix. Frames 89–111 add an exact reverse-bridge stop, the two already accepted stair-route right-hand door-reach drawings normalized to V4 opaque-paint rules, an animated door, a brief neutral, restart and complete exit occlusion. The outward-opening door remains open after this route. It closes automatically only after the Keeper later returns through it and has fully left the room; costume changes may occur only under its full occlusion, so no costume-specific door-opening animation is required. Approved V4's current 50-ms turn remains unchanged; Frank's requested 25-ms timing-only pass is deferred. Nothing is promoted.

Review: \`/keeper-review/${set}/\`.
`)

const register = {
  schema: 'lighthouse-keeper/review-batch@1', batchId: 'keeper-prime-ladder-transitions-2026-10-16-v5', status: 'draft-awaiting-upper-door-flow-review',
  purpose: 'Complete the approved V4 ladder route through a measured upper-door stop, reach, opening and fully obscured exit.',
  authorities: {
    v4Spec: { file: rel(v4SpecFile), sha256: sha(v4SpecFile) }, v4Register: { file: rel(v4RegisterFile), sha256: sha(v4RegisterFile) },
    v4Approval: { file: rel(v4ApprovalFile), sha256: sha(v4ApprovalFile) }, v4Page: { file: rel(v4PageFile), sha256: sha(v4PageFile) },
  },
  spec: { file: rel(specFile), sha256: sha(specFile) }, reviewPage: { file: rel(pageFile), sha256: sha(pageFile), publicReview: `/keeper-review/${set}/`, preloadsAllUniqueFrames: true, mountsAllUniqueFrames: true, defaultRoute: 'full' },
  publishedAssets,
  changes: { approvedV4PrefixFrames: 88, completeRouteFrames: spec.routes.full.frames.length, newDoorReachDerivatives: 2, persistentCompositor: true, upperDoorOrientationToCameraDeg: 90, upperDoorOpensOutward: true, upperDoorOccludesKeeper: true, upperDoorRemainsOpenAtEnd: true, costumeSpecificDoorAnimationRequired: false, ladderPixelsSuppressed: false, v4TurnTimingChanged: false, deferredTurnFrameMs: 25, finalChanged: false, runtimeChanged: false, productionChanged: false },
  approvalBoundary: { candidateApproved: false, finalLaneEntryAllowed: false, productionPromotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and ${rel(publicDir)}; approved V4 and all earlier provenance remain unchanged.`,
}
writeJson(path.join(pack, 'batch-register.json'), register)
console.log(JSON.stringify({ page: rel(pageFile), completeRouteFrames: spec.routes.full.frames.length, approvedPrefixFrames: 88, uniqueAssets: publishedAssets.length, defaultRoute: 'full' }, null, 2))
