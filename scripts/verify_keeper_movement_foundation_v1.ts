#!/usr/bin/env node
/** Verify the reversible root-motion and vertical-circulation construction batch. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-movement-foundation-2026-10-14-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const GATE = path.join(ROOT, 'public/keeper-review/keeper-root-motion-gate-v1/index.html')
const CIRCULATION = path.join(ROOT, 'public/keeper-review/keeper-vertical-circulation-v1/index.html')
const fail = (message: string): never => { throw new Error(`Keeper movement foundation V1: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), GATE, CIRCULATION]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-movement-foundation-2026-10-14-v1' || record.status !== 'draft-root-motion-and-vertical-circulation-awaiting-review') fail('identity/status changed')

for (const authority of Object.values(record.authorities) as Record<string, any>[]) if (!fs.existsSync(path.join(ROOT, authority.file)) || hash(path.join(ROOT, authority.file)) !== authority.sha256) fail(`authority changed: ${authority.file}`)
for (const asset of record.publishedAssets as Record<string, any>[]) {
  const source = path.join(ROOT, asset.source)
  const published = path.join(ROOT, asset.public)
  if (hash(source) !== asset.sourceSha256 || hash(published) !== asset.publicSha256 || asset.sourceSha256 !== asset.publicSha256 || asset.byteIdentical !== true) fail(`published asset differs: ${asset.key}`)
  const png = PNG.sync.read(fs.readFileSync(published))
  if (png.width !== 256 || png.height !== 320) fail(`${asset.key} cell geometry changed`)
  for (let x = 0; x < png.width; x += 1) if (png.data[x * 4 + 3] || png.data[((png.height - 1) * png.width + x) * 4 + 3]) fail(`${asset.key} touches horizontal cell edge`)
  for (let y = 1; y < png.height - 1; y += 1) if (png.data[(y * png.width) * 4 + 3] || png.data[(y * png.width + png.width - 1) * 4 + 3]) fail(`${asset.key} touches vertical cell edge`)
}

if (hash(GATE) !== record.rootMotionGate.pageSha256 || hash(CIRCULATION) !== record.verticalCirculation.pageSha256) fail('review page changed')
const geometryFile = path.join(ROOT, record.verticalCirculation.geometry)
if (hash(geometryFile) !== record.verticalCirculation.geometrySha256) fail('geometry contract changed')
const g = JSON.parse(fs.readFileSync(geometryFile, 'utf8')) as Record<string, any>
if (g.floor.clearHeightLogicalPixels !== 56 || g.floor.sharedDeckLogicalPixels !== 4 || g.floor.finishedFloorPitchKu !== 480) fail('floor module changed')
if (g.stair.risersPerFlight !== 16 || g.stair.riserKu !== 30 || g.stair.treadKu !== 42 || g.stair.flightRunKu !== 672 || g.stair.coreWidthKu !== 840) fail('stair geometry changed')
if (g.stair.risersPerFlight * g.stair.riserKu !== g.floor.finishedFloorPitchKu) fail('stair does not close floor rise')
if (g.stair.risersPerFlight * g.stair.treadKu !== g.stair.flightRunKu || g.stair.flightRunKu !== 8 * g.units.walkingPitchKu) fail('stair does not close eight walk intervals')
if (g.ladder.intervalsPerFloor * g.ladder.rungPitchKu !== g.floor.finishedFloorPitchKu || g.lift.verticalStopPitchKu !== g.floor.finishedFloorPitchKu) fail('ladder/lift pitch disagrees with floor')
if (Math.abs(g.stair.treadLogicalPixels / g.keeper.bootLengthLogicalPixels - g.stair.supportedBootFraction) > 1e-9) fail('boot support calculation changed')

if (JSON.stringify(record.rootMotionGate.approvedDeltasKu) !== '[2,6,12,18,18,12,6,2]' || record.rootMotionGate.approvedDistanceKu !== 76) fail('approved root profile changed')
if (JSON.stringify(record.rootMotionGate.candidateDeltasKu) !== '[3,7,13,19,19,13,7,3]' || record.rootMotionGate.candidateDistanceKu !== 84) fail('candidate root profile changed')
if (record.rootMotionGate.candidateDeltasKu.reduce((a: number, b: number) => a + b, 0) !== g.units.walkingPitchKu) fail('candidate does not close one lattice interval')

const gateHtml = fs.readFileSync(GATE, 'utf8')
const circulationHtml = fs.readFileSync(CIRCULATION, 'utf8')
for (const phrase of ['Root-motion Gate 1', 'exact approved pixels', 'Exact proposed game scale', 'Loading and decoding all five unique Keeper frames', 'Promise.all(unique.map(preloadFrame))', 'image.decode', 'Previous frame', 'Next frame']) if (!gateHtml.includes(phrase)) fail(`root gate omits ${phrase}`)
for (const phrase of ['Vertical circulation V1', '56 lp clear room + 4 lp shared structural deck', 'Stairs · climb and continue higher', 'Stairs · far landing to room door', 'Stairs · near landing to room door', 'Ladder · climb and continue higher', 'Ladder · climb, dismount and walk', 'Lift · walk, stop, turn and enter', 'Lift · exit, turn and walk', 'Exact game scale · 4 CSS px per logical px', 'Previous frame', 'Next frame']) if (!circulationHtml.includes(phrase)) fail(`circulation page omits ${phrase}`)
for (const html of [gateHtml, circulationHtml]) {
  const script = html.split('<script>')[1]?.split('</script>')[0]
  if (!script) fail('review script missing')
  new Function(script)
}

for (const flag of ['stairRiseMatchesFinishedFloorPitch', 'stairRunMatchesEightWalkIntervals', 'treadAndRiserIntegralKu', 'ladderRiseMatchesFinishedFloorPitch', 'liftPitchMatchesFinishedFloorPitch']) if (record.validation?.[flag] !== true) fail(`${flag} changed`)
for (const flag of ['canonicalArtworkChanged', 'productionSpritesChanged', 'runtimeManifestChanged', 'workbenchFinalChanged']) if (record.validation?.[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['geometryApproved', 'rootMotionCandidateApproved', 'constructionMotionApproved', 'finishedArtworkApproved', 'productionPromotionAllowed']) if (record.approvalBoundary?.[flag] !== false) fail(`${flag} approval boundary changed`)
console.log('Keeper movement foundation V1 verified: exact root pixels, 84-ku candidate closure, 60-lp vertical module, stair/ladder/lift routes, safe gutters and no promotion.')
