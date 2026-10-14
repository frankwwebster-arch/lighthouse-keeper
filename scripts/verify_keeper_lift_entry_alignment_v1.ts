#!/usr/bin/env node
/** Verify the reversible lift placement/choreography study. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-lift-entry-alignment-2026-10-14-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC_FILE = path.join(PACK, 'lift-entry-alignment-v1.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-lift-entry-alignment-v1/index.html')
const fail = (message: string): never => { throw new Error(`Keeper lift entry alignment V1: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, SPEC_FILE, path.join(PACK, 'HANDOFF.md'), PAGE]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC_FILE, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-lift-entry-alignment-2026-10-14-v1' || record.status !== 'draft-construction-choreography-awaiting-review') fail('identity/status changed')
if (hash(SPEC_FILE) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered candidate file changed')
for (const group of ['authorities', 'preservedEvidence']) for (const authority of Object.values(record[group]) as Record<string, any>[]) {
  const file = path.join(ROOT, authority.file)
  if (!fs.existsSync(file) || hash(file) !== authority.sha256) fail(`${group} changed: ${authority.file}`)
}
const g = spec.geometry
if (g.roomDoorCentreLp !== 126 || g.liftThresholdCentreLp !== 42 || g.distanceLp !== 84 || g.distanceKu !== 672) fail('door/lift geometry changed')
if (g.roomDoorCentreLp - g.liftThresholdCentreLp !== g.distanceLp) fail('distance does not close')
if (g.stepIntervals !== 8 || g.fullStrides !== 4 || g.distanceLp !== g.stepIntervals * spec.units.stepLp || g.distanceLp !== g.fullStrides * spec.units.fullStrideLp) fail('step/stride closure changed')
if (g.liftOpeningLeftLp !== 20 || g.liftOpeningWidthLp !== 44 || JSON.stringify(g.liftButtonLp) !== '[52.5,43.5]') fail('lift opening/button geometry changed')
if (spec.timeline.length !== 8 || spec.timeline[2].root !== '42 lp' || spec.timeline.slice(2).some((p: any) => p.root !== '42 lp')) fail('action root is not fixed')
if (spec.artDependency.id !== 'walk-f5-to-neutral-stop' || spec.artDependency.status !== 'not-drawn-not-approved') fail('F5 dependency hidden or changed')
for (const flag of ['wholeStrideClosure', 'fixedActionRoot', 'rightHandReachIncluded', 'depthOnlyEntry', 'f5StopDependencyDeclared']) if (record.validation[flag] !== true) fail(`${flag} changed`)
for (const flag of ['approvedPixelsChanged', 'runtimeChanged', 'approvalChanged']) if (record.validation[flag] !== false) fail(`${flag} boundary changed`)

const html = fs.readFileSync(PAGE, 'utf8')
for (const phrase of ['Lift entry alignment V1 · no sideways slide', 'right hand', '84 lp · 8 steps · 4 full strides', 'x = 42 lp', '44 lp', 'Walk F5 → neutral', 'enter in depth only', 'Previous frame', 'Next frame', 'Promise.all(REVIEW_MEDIA.map(preload))', 'Construction vectors ready · no external frame media required']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
if (!html.includes('const REVIEW_MEDIA=[]') || /<img\b/i.test(html)) fail('unexpected external moving media contract')
if (html.includes('id="loop" type="checkbox" checked')) fail('route reset must not masquerade as a continuous transition')
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
console.log('Keeper lift entry alignment V1 verified: 84-lp whole-stride route, fixed x=42 action root, right-hand press, depth-only entry and explicit F5 dependency.')
