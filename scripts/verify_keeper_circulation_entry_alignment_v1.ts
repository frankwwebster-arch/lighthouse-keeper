#!/usr/bin/env node
/** Verify the shared door-to-stair/lift construction study. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-circulation-entry-alignment-2026-10-14-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC_FILE = path.join(PACK, 'circulation-entry-alignment-v1.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-circulation-entry-alignment-v1/index.html')
const fail = (message: string): never => { throw new Error(`Keeper circulation entry alignment V1: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, SPEC_FILE, path.join(PACK, 'HANDOFF.md'), PAGE]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC_FILE, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-circulation-entry-alignment-2026-10-14-v1' || record.status !== 'draft-construction-choreography-awaiting-review') fail('identity/status changed')
if (hash(SPEC_FILE) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered candidate changed')
for (const group of ['authorities', 'preservedEvidence']) for (const authority of Object.values(record[group]) as Record<string, any>[]) {
  const file = path.join(ROOT, authority.file)
  if (!fs.existsSync(file) || hash(file) !== authority.sha256) fail(`${group} changed: ${authority.file}`)
}
const u = spec.units, shared = spec.sharedGeometry, stair = spec.stair, lift = spec.lift
if (shared.circulationCoreWidthLp !== 105 || shared.transferDoorCentreLp !== 115.5 || shared.landingRootMarginLp !== 10.5) fail('shared geometry changed')
if (stair.baseRootLp !== shared.circulationCoreWidthLp - shared.landingRootMarginLp || shared.transferDoorCentreLp - stair.baseRootLp !== stair.doorToBaseLp) fail('stair base/door relation changed')
if (stair.doorToBaseLp !== 21 || stair.doorToBaseKu !== 168 || stair.doorToBaseLp !== u.fullStrideLp || stair.walkStepIntervals !== 2 || stair.fullWalkCycles !== 1 || stair.visibleWalkFrames !== 8) fail('stair whole-cycle closure changed')
if (stair.pauseFramesAtJoin !== 0 || stair.firstClimbFrameAdvances !== true) fail('walk-to-climb pause introduced')
if (stair.flightEndRootLp !== 10.5 || stair.baseRootLp - stair.flightEndRootLp !== 84 || stair.flightRunLp !== 84 || stair.flightRiseLp !== 60 || stair.risers * stair.riserLp !== stair.flightRiseLp || stair.risers * stair.treadLp !== stair.flightRunLp) fail('stair flight geometry changed')
if (shared.transferDoorCentreLp - lift.thresholdRootLp !== lift.doorToThresholdLp || lift.doorToThresholdLp !== 84 || lift.doorToThresholdKu !== 672 || lift.walkStepIntervals !== 8 || lift.fullWalkCycles !== 4) fail('lift route closure changed')
if (lift.openingLeftLp !== 9.5 || lift.openingWidthLp !== 44 || JSON.stringify(lift.buttonLp) !== '[42,43.5]' || lift.f5StopDependency !== 'not-drawn-not-approved') fail('lift geometry/dependency changed')
for (const flag of ['sharedDoorAnchor', 'stairWholeWalkCycle', 'stairJoinHasZeroPauseFrames', 'firstClimbFrameAdvances', 'liftWholeStrideClosure']) if (record.validation[flag] !== true) fail(`${flag} changed`)
for (const flag of ['approvedPixelsChanged', 'runtimeChanged', 'approvalChanged']) if (record.validation[flag] !== false) fail(`${flag} boundary changed`)
const html = fs.readFileSync(PAGE, 'utf8')
for (const phrase of ['Circulation entry alignment V1 · door → stairs or lift', 'one complete eight-frame walk cycle', '0 pause frames', 'climb frame 1 · already advancing', '21 lp · 2 steps · 1 walk cycle', '84 lp · 8 steps · 4 full strides', 'Walk F5 → neutral', 'Previous frame', 'Next frame →', 'Promise.all(REVIEW_MEDIA.map(preload))']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
if (!html.includes('const REVIEW_MEDIA=[]') || /<img\b/i.test(html)) fail('unexpected external moving media contract')
if (html.includes('id="loop" type="checkbox" checked')) fail('route reset must not be shown as a continuous transition')
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
console.log('Keeper circulation entry alignment V1 verified: shared x=115.5 door, one-cycle 21-lp stair approach, zero-pause advancing climb join, and 84-lp lift route.')
