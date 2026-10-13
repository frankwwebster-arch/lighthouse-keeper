#!/usr/bin/env node
/** Verify the separate Draft/Final Keeper animation workbench contract. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const DATA = path.join(ROOT, 'data/keeper_animation_workbench.json')
const PUBLIC = path.join(ROOT, 'public/keeper-animation-workbench/catalog.json')
const PAGE = path.join(ROOT, 'src/app/animation-workbench/page.tsx')
const UI = path.join(ROOT, 'src/animation-workbench/AnimationWorkbench.tsx')
const MODEL = path.join(ROOT, 'src/animation-workbench/model.ts')
const CSS = path.join(ROOT, 'src/animation-workbench/workbench.module.css')
const CORE_V2_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-core-transitions-2026-10-12-v2/batch-register.json')
const PRIME_MASTER_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-master-2026-10-12-v1/master-pack-register.json')
const PRIME_ORTHOGRAPHIC_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/batch-register.json')
const PRIME_RIG_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v1/batch-register.json')
const PRIME_RIG_MOTION_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v2/batch-register.json')
const EXPECTED_FINALS: string[] = []
const EXPECTED_DRAFTS: string[] = []
const fail = (message: string): never => { throw new Error(`keeper animation workbench: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [DATA, PUBLIC, PAGE, UI, MODEL, CSS, CORE_V2_REGISTER, PRIME_MASTER_REGISTER, PRIME_ORTHOGRAPHIC_REGISTER, PRIME_RIG_REGISTER, PRIME_RIG_MOTION_REGISTER]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
if (!fs.readFileSync(DATA).equals(fs.readFileSync(PUBLIC))) fail('data and public catalogues differ')

const catalogue = JSON.parse(fs.readFileSync(DATA, 'utf8')) as Record<string, any>
if (catalogue.version !== 1 || catalogue.platformId !== 'keeper-animation-workbench') fail('catalogue identity changed')
if (catalogue.separateFrom !== '/keeper-review/') fail('new workbench is not explicitly separated from the existing reviewer')
if (catalogue.provenance?.productionSpritesChanged !== false || catalogue.provenance?.runtimeManifestChanged !== false) fail('production mutation guard changed')
if (catalogue.featureContract?.walkExtension?.owner !== 'game-engine' || catalogue.featureContract?.walkExtension?.startVisibility !== 'hidden-behind-door' || catalogue.featureContract?.walkExtension?.firstVisibleState !== 'walking-mid-stride') fail('door-hidden runtime walk-lead-in contract changed')
if (JSON.stringify(catalogue.lanes?.final?.map((item: Record<string, any>) => item.id)) !== JSON.stringify(EXPECTED_FINALS)) fail('Final library scope changed')
if (JSON.stringify(catalogue.lanes?.draft?.map((item: Record<string, any>) => item.id)) !== JSON.stringify(EXPECTED_DRAFTS)) fail('Draft library must remain empty until Prime orthographic endpoint approval')
if (!catalogue.principles?.final?.startsWith('Currently empty') || !catalogue.principles?.draft?.startsWith('Currently empty')) fail('empty-library approval gate changed')

const assets = new Map<string, Record<string, any>>(catalogue.assets.map((asset: Record<string, any>) => [asset.id, asset]))
for (const asset of catalogue.assets as Record<string, any>[]) {
  if (asset.id.startsWith('draft:') ? asset.immutable !== false : asset.immutable !== true) fail(`${asset.id} mutability flag changed`)
  const local = asset.file.startsWith('/sprites/')
    ? path.join(ROOT, 'public', asset.file)
    : path.join(ROOT, 'public', asset.file)
  if (!fs.existsSync(local)) fail(`${asset.id} is missing ${path.relative(ROOT, local)}`)
  if (sha256(local) !== asset.sha256) fail(`${asset.id} hash changed`)
  const png = PNG.sync.read(fs.readFileSync(local))
  if (png.width !== asset.w * asset.density * asset.frames || png.height !== asset.h * asset.density) fail(`${asset.id} strip geometry disagrees with metadata`)
  if (asset.id.startsWith('draft:')) {
    const sidecar = JSON.parse(fs.readFileSync(path.join(ROOT, asset.sourceSidecar), 'utf8'))
    if (sha256(path.join(ROOT, asset.sourceSidecar)) !== asset.sourceSidecarSha256) fail(`${asset.id} sidecar hash changed`)
    for (const key of ['w', 'h', 'frames', 'fps', 'density', 'startPose', 'endPose']) if (asset[key] !== sidecar[key]) fail(`${asset.id} strip/sidecar ${key} disagrees`)
    for (let frame = 0; frame < asset.frames; frame += 1) {
      let opaque = 0
      for (let y = 0; y < png.height; y += 1) for (let x = 0; x < asset.w * asset.density; x += 1) {
        const alpha = png.data[((y * png.width) + frame * asset.w * asset.density + x) * 4 + 3]
        if (alpha !== 0 && alpha !== 255) fail(`${asset.id} frame ${frame + 1} alpha is not binary`)
        if (alpha > 0) opaque += 1
        if (alpha > 0 && (x === 0 || x === asset.w * asset.density - 1 || y === 0 || y === png.height - 1)) fail(`${asset.id} frame ${frame + 1} touches a cell edge`)
      }
      if (!opaque) fail(`${asset.id} frame ${frame + 1} is empty`)
    }
  }
}

for (const item of catalogue.lanes.final as Record<string, any>[]) {
  if (item.lane !== 'final') fail(`${item.id} has the wrong Final lane`)
  if (!item.approval?.scope?.includes('runtime promotion remains a separate decision')) fail(`${item.id} approval scope could imply production promotion`)
  if (item.timeline?.length !== 6 || item.timeline.map((entry: Record<string, any>) => entry.frame).join(',') !== '0,1,2,3,4,5') fail(`${item.id} Final timeline changed`)
  if (item.sectionLoops?.length || item.overallLoop !== false) fail(`${item.id} Final recipe was mutated`)
  if (item.transitionPolicy !== 'required') fail(`${item.id} lost its visible-transition gate`)
  if (item.transitionRoute.filter((segment: Record<string, any>) => segment.id === item.timelineSegmentId).length !== 1) fail(`${item.id} does not declare exactly one editable timeline route segment`)
  const roles = item.transitionRoute.map((segment: Record<string, any>) => segment.role)
  if (JSON.stringify(roles) !== '["walk","stop","action"]' && JSON.stringify(roles) !== '["walk","stop","turn","action"]') fail(`${item.id} ingress is not walk → stop → optional turn → action`)
  if (item.transitionRoute[0]?.distanceMode !== 'runtime-placement' || item.transitionRoute[0]?.repeats !== 1) fail(`${item.id} walk extension is not delegated to deterministic runtime placement`)
  const expectedDoor = item.name === 'keeper_turn_left_front' ? 'door-right' : 'door-left'
  if (item.transitionRoute[0]?.entryOcclusion !== expectedDoor) fail(`${item.id} does not begin walking behind the correct door`)
  if (item.transitionRoute.at(-1)?.assetId !== item.assetId) fail(`${item.id} ingress does not end by beginning the selected action`)
  const currentAsset = assets.get(item.assetId)
  if (!currentAsset || currentAsset.source !== `${item.sourceDraft}/drafts/${item.name}/${item.name}_f6.png`) fail(`${item.id} does not resolve to its approved V2 source`)
  let priorEnd: string | undefined
  for (const segment of item.transitionRoute as Record<string, any>[]) {
    const asset = assets.get(segment.assetId)
    if (!asset) fail(`${item.id} route references missing ${segment.assetId}`)
    if (segment.frames.some((frame: number) => frame < 0 || frame >= asset.frames)) fail(`${item.id} route references an out-of-range frame`)
    const mirrored = (pose: string | undefined) => !segment.mirror || !pose ? pose : pose.replace('side-right', 'SIDE').replace('side-left', 'side-right').replace('SIDE', 'side-left')
    const start = mirrored(asset.startPose)
    const end = mirrored(asset.endPose)
    if (priorEnd && start && priorEnd !== start) fail(`${item.id} metadata seam jumps from ${priorEnd} to ${start}`)
    priorEnd = end
  }

  const finalFile = path.join(ROOT, 'public', currentAsset.file)
  const png = PNG.sync.read(fs.readFileSync(finalFile))
  const cellWidth = currentAsset.w * currentAsset.density
  const cellHeight = currentAsset.h * currentAsset.density
  for (let frame = 0; frame < currentAsset.frames; frame += 1) {
    let opaque = 0
    for (let y = 0; y < cellHeight; y += 1) for (let x = 0; x < cellWidth; x += 1) {
      const alpha = png.data[((y * png.width) + (frame * cellWidth) + x) * 4 + 3]
      if (alpha > 0) opaque += 1
      if (alpha > 0 && (x === 0 || x === cellWidth - 1 || y === 0 || y === cellHeight - 1)) fail(`${item.id} frame ${frame + 1} touches a cell edge`)
    }
    if (!opaque) fail(`${item.id} frame ${frame + 1} is empty`)
  }
}

for (const item of catalogue.lanes.draft as Record<string, any>[]) {
  if (item.lane !== 'draft' || item.approval) fail(`${item.id} is not an unapproved Draft`)
  if (item.transitionPolicy !== 'required' || !item.sourceDraft?.includes('keeper-prime-core-transitions')) fail(`${item.id} lost the Keeper Prime Draft boundary`)
  const timelineSegments = item.transitionRoute.filter((segment: Record<string, any>) => segment.id === item.timelineSegmentId)
  if (timelineSegments.length !== 1 || timelineSegments[0].assetId !== item.assetId) fail(`${item.id} does not declare exactly one matching editable timeline route segment`)
  for (const segment of item.transitionRoute as Record<string, any>[]) {
    const asset = assets.get(segment.assetId)
    if (!asset) fail(`${item.id} route references missing ${segment.assetId}`)
    if (segment.frames.some((frame: number) => frame < 0 || frame >= asset.frames)) fail(`${item.id} route references an out-of-range frame`)
    if (segment.motion && segment.motion.length !== segment.frames.length) fail(`${item.id} ${segment.id} motion/frame counts disagree`)
  }
}

const frameBytes = (assetId: string, frame: number) => {
  const asset = assets.get(assetId)
  if (!asset) fail(`missing endpoint asset ${assetId}`)
  const png = PNG.sync.read(fs.readFileSync(path.join(ROOT, 'public', asset.file)))
  const width = asset.w * asset.density
  const bytes = Buffer.alloc(width * png.height * 4)
  for (let y = 0; y < png.height; y += 1) {
    const start = ((y * png.width) + frame * width) * 4
    png.data.copy(bytes, y * width * 4, start, start + width * 4)
  }
  return bytes
}
const walkId = 'draft:keeper_prime_walk_cycle:kp-v2'
const stopId = 'draft:keeper_prime_walk_stop:kp-v2'
const frontId = 'draft:keeper_prime_turn_front:kp-v2'
const backId = 'draft:keeper_prime_turn_back:kp-v2'
const sitId = 'draft:keeper_prime_sit_side:kp-v2'
const standId = 'draft:keeper_prime_stand_side:kp-v2'
const backNeutralId = 'draft:keeper_prime_neutral_standing-back:kp-v2'
for (const historicalId of [walkId, stopId, frontId, backId, sitId, standId, backNeutralId].map((id) => id.replace(':kp-v2', ':kp-v1'))) {
  if (!assets.has(historicalId)) fail(`missing addressable historical V1 asset ${historicalId}`)
}
const sideState = frameBytes(stopId, 3)
for (const [assetId, frame] of [[walkId, 0], [walkId, 4], [walkId, 8], [frontId, 0], [backId, 0], [sitId, 0], [standId, 5]] as [string, number][]) {
  if (!sideState.equals(frameBytes(assetId, frame))) fail(`${assetId} F${frame + 1} does not equal the shared Keeper Prime side stop`)
}
if (!frameBytes(backId, 5).equals(frameBytes(backNeutralId, 0))) fail('back turn does not end on the exact registered back neutral')
for (let frame = 0; frame < 6; frame += 1) if (!frameBytes(sitId, frame).equals(frameBytes(standId, 5 - frame))) fail(`stand F${6 - frame} is not the exact reverse of sit F${frame + 1}`)
const primeFront = PNG.sync.read(fs.readFileSync(path.join(ROOT, 'art/raw/keeper-first-batch/keeper_neutral_standing-front_f1.png')))
if (!frameBytes(frontId, 5).equals(primeFront.data)) fail('front turn does not end on byte-identical Keeper Prime pixels')
const coreV2 = JSON.parse(fs.readFileSync(CORE_V2_REGISTER, 'utf8')) as Record<string, any>
if (coreV2.batchId !== 'keeper-prime-core-transitions-2026-10-12-v2' || coreV2.productionChanged !== false) fail('V2 register identity or production guard changed')
if (!coreV2.deterministicChecks?.walkStopOutOfScopePixelsUnchanged || !coreV2.deterministicChecks?.singleGeneratedSourcePerMovingAction) fail('V2 unchanged-scope/render-family checks are missing')
for (const [name, seam] of Object.entries(coreV2.criticalSeamChecks ?? {}) as [string, Record<string, number>][]) {
  if (Math.abs(seam.widthDelta) > 8 || Math.abs(seam.heightDelta) > 8 || seam.opaqueAreaRatio < 0.82 || seam.opaqueAreaRatio > 1.18 || seam.baselineDelta !== 0) fail(`${name} violates the V2 route-step continuity bounds`)
}
const primeMaster = JSON.parse(fs.readFileSync(PRIME_MASTER_REGISTER, 'utf8')) as Record<string, any>
if (primeMaster.status !== 'approved-permanent-identity-authority' || primeMaster.approval?.wording !== 'Approved. Make sure this is NEVER forgotten.' || primeMaster.validation?.finalAnimations !== 0 || primeMaster.candidate?.productionPromotionAllowed !== false) fail('permanent Prime Master approval gate changed')
if (catalogue.provenance?.primeMasterRegisterSha256 !== sha256(PRIME_MASTER_REGISTER)) fail('workbench does not pin the Prime Master register')
if (catalogue.provenance?.primeOrthographicRegisterSha256 !== sha256(PRIME_ORTHOGRAPHIC_REGISTER)) fail('workbench does not pin the orthographic register')
if (catalogue.provenance?.primeRigRegisterSha256 !== sha256(PRIME_RIG_REGISTER)) fail('workbench does not pin the construction rig register')
if (catalogue.provenance?.primeRigMotionRegisterSha256 !== sha256(PRIME_RIG_MOTION_REGISTER)) fail('workbench does not pin the rig motion register')

const ui = fs.readFileSync(UI, 'utf8')
for (const label of ['Final', 'Draft', 'Copy to Draft', 'Copy frame', 'Remove frame', 'Move left', 'Move right', 'Repeat section', 'Transition preview', 'Required for every action', 'begins hidden behind', 'cycles set by game placement', 'Export Draft JSON', 'Import Draft JSON', 'Final is empty', 'No animations are currently Final', 'Prime Master V1', 'historical side remains blocked at 5/15', 'KP Rig V1 is approved', 'Keeper Prime Rig Motion V2 review']) {
  if (!ui.includes(label)) fail(`UI omits ${label}`)
}
for (const functionName of ['copyTimelineEntry', 'removeTimelineEntry', 'moveTimelineEntry', 'expandTimeline', 'transitionPlayback', 'transitionWarnings', 'reconcileDraftLibrary']) {
  if (!fs.readFileSync(MODEL, 'utf8').includes(`function ${functionName}`)) fail(`model omits ${functionName}`)
}

console.log('Verified Keeper Animation Workbench reset: 0 Final, 0 active Draft, permanent Prime Master authority and orthographic approval gate intact')
