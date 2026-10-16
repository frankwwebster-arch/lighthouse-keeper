#!/usr/bin/env node
/** Build Ladder Transition V6: approved V5 animation with a flat two-way door. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const v5Set = 'keeper-prime-ladder-transitions-v5'
const set = 'keeper-prime-ladder-transitions-v6'
const v5Pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v5')
const pack = path.join(root, 'art/drafts/keeper-prime-ladder-transitions-2026-10-16-v6')
const framesDir = path.join(pack, 'drafts/frames')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const v5SpecFile = path.join(v5Pack, 'keeper-prime-ladder-transitions-v5.json')
const v5RegisterFile = path.join(v5Pack, 'batch-register.json')
const v5ApprovalFile = path.join(root, 'docs/review/keeper-prime-ladder-transitions-v5-animation-approval-2026-10-16.json')
const doorContractFile = path.join(root, 'docs/review/keeper-two-way-door-contract-2026-10-16.json')
const v5PageFile = path.join(root, 'public/keeper-review', v5Set, 'index.html')
const specFile = path.join(pack, 'keeper-prime-ladder-transitions-v6.json')
const pageFile = path.join(publicDir, 'index.html')
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const rel = file => path.relative(root, file).split(path.sep).join('/')
const writeJson = (file, value) => { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n') }

for (const file of [v5SpecFile, v5RegisterFile, v5ApprovalFile, doorContractFile, v5PageFile]) if (!fs.existsSync(file)) throw new Error(`missing ${file}`)
fs.mkdirSync(framesDir, { recursive: true })
fs.mkdirSync(assetsDir, { recursive: true })

const v5Spec = read(v5SpecFile)
const v5Register = read(v5RegisterFile)
const approval = read(v5ApprovalFile)
const doorContract = read(doorContractFile)
const spec = structuredClone(v5Spec)
spec.set = set
spec.status = 'draft-awaiting-two-way-door-review'
spec.geometry.upperDoor = {
  orientationToHallwayDeg: 90,
  projection: 'flat-orthographic-rectangle',
  perspectiveWideningAllowed: false,
  gradientDepthAllowed: false,
  onlyProtrudingComponent: 'handle',
  hingeSideAsViewed: 'right',
  swingDirection: 'away-from-approaching-keeper',
  jambXLp: 158,
  jambWidthLp: 0.5,
  leafXLp: 158.5,
  leafWidthLp: 20,
  leafHeightLp: 48,
  visibleStageRightXLp: 172,
  hingeXLp: 178.5,
  handleXLp: 161.3,
  handleWidthLp: 1.4,
  handleHeightLp: 1.4,
  stopRootXLp: 148.25,
  transferRootXLp: 158.75,
  hiddenRootXLp: 174.5,
}
spec.doorPolicy = {
  twoWaySwing: true,
  opensAwayFromApproachingKeeper: true,
  hingeSideAsViewed: 'right',
  occlusionMethod: 'opaque-open-door-leaf',
  autoCloseTrigger: 'keeper-fully-cleared-doorway',
  autoCloseRequiresKeeperAnimation: false,
  remainsOpenAfterRoomEntry: false,
  costumeSpecificDoorAnimationRequired: false,
}
spec.presentationCorrection = {
  v5KeeperAnimationApproved: true,
  keeperFramesChanged: false,
  rootsChanged: false,
  timingChanged: false,
  choreographyChanged: false,
  presentationPhaseLabelsChangedOnly: false,
  v5PerspectiveDoorRejected: true,
  flatTwoWayDoorOnly: true,
}

const urlMap = new Map()
const publishedAssets = []
for (const entry of v5Register.publishedAssets) {
  const source = path.join(root, entry.draft)
  if (!fs.existsSync(source) || sha(source) !== entry.draftSha256) throw new Error(`V5 authority drift: ${entry.draft}`)
  const draft = path.join(framesDir, path.basename(entry.draft))
  fs.copyFileSync(source, draft)
  const digest = sha(draft)
  const publicName = `${path.basename(draft, '.png')}-${digest.slice(0, 16)}.png`
  const published = path.join(assetsDir, publicName)
  fs.copyFileSync(draft, published)
  const url = `/keeper-review/${set}/assets/${publicName}`
  urlMap.set(entry.url, url)
  publishedAssets.push({
    role: entry.role,
    source: rel(source),
    sourceSha256: digest,
    draft: rel(draft),
    draftSha256: digest,
    published: rel(published),
    url,
    bytes: fs.statSync(published).size,
    changeScope: 'byte-identical approved V5 Keeper animation artwork',
  })
}
for (const route of Object.values(spec.routes)) for (const frame of route.frames) {
  const next = urlMap.get(frame.src)
  if (!next) throw new Error(`unmapped V5 URL: ${frame.src}`)
  frame.src = next
}
writeJson(specFile, spec)

let html = fs.readFileSync(v5PageFile, 'utf8')
html = html.replaceAll('Keeper Prime ladder transitions V5', 'Keeper Prime ladder transitions V6')
html = html.replace(
  'Whole-flow extension of approved V4: after the ladder landing the Keeper now completes a measured stop, right-hand door reach, opening and fully obscured exit. V4 artwork and compositor remain exact.',
  'Door-only correction of approved V5 animation: every Keeper frame, root, timing and transition remains exact. The right-hinged two-way door is a flat rectangular leaf which always opens away from the approaching Keeper.',
)
html = html.replace(
  'The approved ladder route now continues through the upper door: one complete post-turn walk cycle, exact reverse bridge stop, right-hand reach/open, brief neutral, restart and full door occlusion. The requested 2× turn timing remains deferred.',
  'All 111 approved V5 animation frames remain exact. The rejected perspective panel is replaced by a constant-size, flat orthographic rectangle. The opaque open leaf—not the room boundary—hides the Keeper while he crosses.',
)
html = html.replace(
  '.doorFrame{position:absolute;background:#142d39;border:2px solid #91aab6;z-index:3}.doorLeaf{position:absolute;background:linear-gradient(90deg,#284756,#426574);border-left:2px solid #a8c0ca;z-index:3;will-change:left,width}.doorKnob{position:absolute;border-radius:50%;background:#f5c842;border:1px solid #5c4611;z-index:4;will-change:left}',
  '.doorFrame{position:absolute;background:#91aab6;z-index:3}.doorLeaf{position:absolute;background:#426574;border:0;z-index:8}.doorKnob{position:absolute;border-radius:999px;background:#f5c842;border:1px solid #5c4611;z-index:9;will-change:left,width}',
)
html = html.replace(
  '<section class="metrics"><article><b>111 frames</b>complete lower-room to upper-room flow</article><article><b>Door remains open</b>',
  '<section class="metrics"><article><b>Animation approved</b>111 V5 frames, roots and timing remain exact</article><article><b>Two-way door</b>opens away · closes after full clearance</article><article><b>Flat leaf</b>20 × 48 lp · zero widening · zero gradient</article><article><b>111 frames</b>complete lower-room to upper-room flow</article><article><b>Door remains open</b>',
)
html = html.replace(
  '<article><b>Door remains open</b>it closes only after the later return from the room</article>',
  '<article><b>Automatic close</b>fires only after the Keeper fully clears the doorway</article>',
)
html = html.replace(
  '<article><b>Door complete</b>stop · reach · open · restart · disappear</article>',
  '<article><b>No costume variant</b>the door controller owns the closing action</article>',
)
html = html.replace(
  'Inspect the default complete route from lower-room emergence to full upper-door disappearance. Judge the new F89–F111 door tail: the walk must decelerate naturally, the right hand must meet the handle, the door must open toward him before restart, and the Keeper must finish fully obscured while the door stays open. It closes only after his later return from the room. Approved V4 F1–F88 remain exact.',
  'The Keeper animation is approved and must not be rejudged here. Inspect only the corrected upper door: a full, flat, right-hinged rectangular leaf with no perspective widening or gradient. It always opens away from the approaching Keeper, genuinely hides him during crossing, and the game closes it automatically only after he has fully cleared the doorway. Only the handle protrudes.',
)
html = html.replace(/const SPEC=.*?;\nconst routeSelect=/s, `const SPEC=${JSON.stringify(spec)};\nconst routeSelect=`)
const oldDoors = "nodes.leftDoor=add(world,'door',8,68,24,48,scale);nodes.rightFrame=add(world,'doorFrame',150,8,18,48,scale);nodes.rightDoor=add(world,'doorLeaf',155.5,8,12.5,48,scale);nodes.rightKnob=add(world,'doorKnob',161.3,30.3,1.4,1.4,scale);"
const newDoors = "nodes.leftDoor=add(world,'door',8,68,24,48,scale);nodes.rightFrame=add(world,'doorFrame',158,8,.5,48,scale);nodes.rightDoor=add(world,'doorLeaf',158.5,8,20,48,scale);nodes.rightKnob=add(world,'doorKnob',161.3,30.3,1.4,1.4,scale);"
if (!html.includes(oldDoors)) throw new Error('V5 door construction changed')
html = html.replace(oldDoors, newDoors)
const oldRender = "nodes.leftDoor.style.visibility=(routeId==='approach'||routeId==='full')?'visible':'hidden';const showRight=(routeId==='exit'||routeId==='full'),open=frame.upperDoorOpen||0;for(const doorNode of [nodes.rightFrame,nodes.rightDoor,nodes.rightKnob])doorNode.style.visibility=showRight?'visible':'hidden';nodes.rightDoor.style.left=px(155.5+3*open,scale);nodes.rightDoor.style.width=px(12.5+7.5*open,scale);nodes.rightDoor.style.zIndex=open>.8?'8':'3';nodes.rightKnob.style.left=px(161.3+7*open,scale);nodes.rightKnob.style.zIndex=open>.8?'9':'4';const img="
const newRender = "nodes.leftDoor.style.visibility=(routeId==='approach'||routeId==='full')?'visible':'hidden';const showRight=(routeId==='exit'||routeId==='full'),open=frame.upperDoorOpen||0;for(const doorNode of [nodes.rightFrame,nodes.rightDoor,nodes.rightKnob])doorNode.style.visibility=showRight?'visible':'hidden';nodes.rightDoor.style.left=px(158.5,scale);nodes.rightDoor.style.width=px(20,scale);nodes.rightDoor.style.zIndex=open>.8?'8':'3';nodes.rightKnob.style.left=px(161.3,scale);nodes.rightKnob.style.width=px(1.4,scale);nodes.rightKnob.style.zIndex=open>.8?'9':'4';const img="
if (!html.includes(oldRender)) throw new Error('V5 door render changed')
html = html.replace(oldRender, newRender)
fs.writeFileSync(pageFile, html)

fs.writeFileSync(path.join(pack, 'HANDOFF.md'), `# Keeper Prime ladder transitions V6

V6 changes only the rejected V5 door presentation. All 111 V5 Keeper frames, artwork hashes, route roots, timing and choreography are exact. The door is a full 20 × 48-lp flat rectangle, right-hinged as viewed, with no gradient, perspective widening or false depth. Only the handle protrudes. It is a two-way swing door which always opens away from the approaching Keeper; the opaque leaf itself hides him during crossing. The game closes it automatically only after his bounds have fully cleared the doorway, without any costume-specific Keeper animation. Nothing is promoted.

Review: \`/keeper-review/${set}/\`.
`)

const register = {
  schema: 'lighthouse-keeper/review-batch@1',
  batchId: 'keeper-prime-ladder-transitions-2026-10-16-v6',
  status: spec.status,
  purpose: 'Preserve the approved V5 Keeper animation exactly while replacing the rejected perspective door with a flat, opaque, two-way door leaf.',
  authorities: {
    v5Spec: { file: rel(v5SpecFile), sha256: sha(v5SpecFile) },
    v5Register: { file: rel(v5RegisterFile), sha256: sha(v5RegisterFile) },
    v5AnimationApproval: { file: rel(v5ApprovalFile), sha256: sha(v5ApprovalFile) },
    twoWayDoorContract: { file: rel(doorContractFile), sha256: sha(doorContractFile) },
    v5Page: { file: rel(v5PageFile), sha256: sha(v5PageFile) },
  },
  spec: { file: rel(specFile), sha256: sha(specFile) },
  reviewPage: { file: rel(pageFile), sha256: sha(pageFile), publicReview: `/keeper-review/${set}/`, preloadsAllUniqueFrames: true, mountsAllUniqueFrames: true, defaultRoute: 'full' },
  publishedAssets,
  changes: {
    keeperAnimationApproved: true,
    keeperAssetsChanged: false,
    routeRootsChanged: false,
    routeTimingChanged: false,
    routeChoreographyChanged: false,
    presentationPhaseLabelsChangedOnly: false,
    v5PerspectiveDoorRejected: true,
    flatTwoWayDoorOnly: true,
    doorLeafWidthLp: 20,
    doorLeafHeightLp: 48,
    hingeSideAsViewed: 'right',
    opensAwayFromApproachingKeeper: true,
    perspectiveWideningAllowed: false,
    gradientDepthAllowed: false,
    onlyProtrudingComponent: 'handle',
    occlusionMethod: 'opaque-open-door-leaf',
    autoCloseTrigger: 'keeper-fully-cleared-doorway',
    autoCloseRequiresKeeperAnimation: false,
    finalVisibleKeeperCellFullyCoveredByDoorLeaf: true,
    finalChanged: false,
    runtimeChanged: false,
    productionChanged: false,
  },
  approvalBoundary: { candidateApproved: false, keeperAnimationAlreadyApproved: true, doorPresentationApproved: false, finalLaneEntryAllowed: false, productionPromotionAllowed: false },
  rollback: `Delete only ${rel(pack)} and ${rel(publicDir)}; approved V5 animation and every earlier candidate remain unchanged.`,
}
writeJson(path.join(pack, 'batch-register.json'), register)
console.log(JSON.stringify({ page: rel(pageFile), frames: spec.routes.full.frames.length, uniqueAssets: publishedAssets.length, keeperAnimationChanged: false, doorLeafSizeLp: [20, 48], twoWaySwing: true }, null, 2))
