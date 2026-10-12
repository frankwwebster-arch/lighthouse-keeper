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
const EXPECTED_FINALS = ['keeper_turn_front-v2-final', 'keeper_turn_left_front-v2-final']
const APPROVAL = 'I am very happy with your V2.'
const fail = (message: string): never => { throw new Error(`keeper animation workbench: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [DATA, PUBLIC, PAGE, UI, MODEL, CSS]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
if (!fs.readFileSync(DATA).equals(fs.readFileSync(PUBLIC))) fail('data and public catalogues differ')

const catalogue = JSON.parse(fs.readFileSync(DATA, 'utf8')) as Record<string, any>
if (catalogue.version !== 1 || catalogue.platformId !== 'keeper-animation-workbench') fail('catalogue identity changed')
if (catalogue.separateFrom !== '/keeper-review/') fail('new workbench is not explicitly separated from the existing reviewer')
if (catalogue.provenance?.productionSpritesChanged !== false || catalogue.provenance?.runtimeManifestChanged !== false) fail('production mutation guard changed')
if (catalogue.featureContract?.walkExtension?.owner !== 'game-engine' || catalogue.featureContract?.walkExtension?.startVisibility !== 'hidden-behind-door' || catalogue.featureContract?.walkExtension?.firstVisibleState !== 'walking-mid-stride') fail('door-hidden runtime walk-lead-in contract changed')
if (catalogue.lanes?.draft?.length !== 0) fail('repository catalogue must not ship mutable Draft records')
if (JSON.stringify(catalogue.lanes?.final?.map((item: Record<string, any>) => item.id)) !== JSON.stringify(EXPECTED_FINALS)) fail('Final library scope changed')

const assets = new Map<string, Record<string, any>>(catalogue.assets.map((asset: Record<string, any>) => [asset.id, asset]))
for (const asset of catalogue.assets as Record<string, any>[]) {
  if (!asset.immutable) fail(`${asset.id} is not immutable`)
  const local = asset.file.startsWith('/sprites/')
    ? path.join(ROOT, 'public', asset.file)
    : path.join(ROOT, 'public', asset.file)
  if (!fs.existsSync(local)) fail(`${asset.id} is missing ${path.relative(ROOT, local)}`)
  if (sha256(local) !== asset.sha256) fail(`${asset.id} hash changed`)
  const png = PNG.sync.read(fs.readFileSync(local))
  if (png.width !== asset.w * asset.density * asset.frames || png.height !== asset.h * asset.density) fail(`${asset.id} strip geometry disagrees with metadata`)
}

for (const item of catalogue.lanes.final as Record<string, any>[]) {
  if (item.lane !== 'final' || item.approval?.wording !== APPROVAL) fail(`${item.id} is missing exact Final approval evidence`)
  if (!item.approval?.scope?.includes('runtime promotion remains a separate decision')) fail(`${item.id} approval scope could imply production promotion`)
  if (item.timeline?.length !== 6 || item.timeline.map((entry: Record<string, any>) => entry.frame).join(',') !== '0,1,2,3,4,5') fail(`${item.id} Final timeline changed`)
  if (item.sectionLoops?.length || item.overallLoop !== false) fail(`${item.id} Final recipe was mutated`)
  if (item.transitionPolicy !== 'required') fail(`${item.id} lost its visible-transition gate`)
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

const ui = fs.readFileSync(UI, 'utf8')
for (const label of ['Final', 'Draft', 'Copy to Draft', 'Copy frame', 'Remove frame', 'Move left', 'Move right', 'Repeat section', 'Ingress preview', 'Required for every action', 'begins hidden behind', 'cycles set by game placement', 'Export Draft JSON', 'Import Draft JSON']) {
  if (!ui.includes(label)) fail(`UI omits ${label}`)
}
for (const functionName of ['copyTimelineEntry', 'removeTimelineEntry', 'moveTimelineEntry', 'expandTimeline', 'transitionPlayback', 'transitionWarnings']) {
  if (!fs.readFileSync(MODEL, 'utf8').includes(`function ${functionName}`)) fail(`model omits ${functionName}`)
}

console.log('Verified Keeper Animation Workbench: immutable Final, non-destructive Draft editing, and door-hidden walk → stop → optional turn → action ingress with runtime-owned walk length')
