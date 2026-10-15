#!/usr/bin/env node
/** Verify Stair Ascent V8's geometry-only one-tread horizontal correction. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v8')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v8.json')
const RIG = path.join(PACK, 'stair-contact-rig-v8.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v8/index.html')
const V7_PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v7/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const MANIFEST = path.join(ROOT, 'review-archive/sets/keeper-prime-stair-ascent-v8.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V8: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const near = (a: number, b: number, epsilon = 1e-6) => Math.abs(a - b) <= epsilon
for (const file of [REGISTER, SPEC, RIG, PAGE, V7_PAGE, ARCHIVE, MANIFEST, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const rig = JSON.parse(fs.readFileSync(RIG, 'utf8')) as Record<string, any>
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) as Record<string, any>
const html = fs.readFileSync(PAGE, 'utf8'), v7Html = fs.readFileSync(V7_PAGE, 'utf8')
if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v8' || record.status !== 'draft-v8-first-step-horizontal-registration-awaiting-review') fail('identity/status changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256 || spec.promoted !== false) fail('registered candidate or boundary changed')
if (rig.geometry.horizontalCorrectionFromV7Lp !== 6 || rig.geometry.firstFloorSupportCentreXLp !== 103.5 || rig.geometry.firstTreadCentreXLp !== 97.5) fail('first-step geometry changed')
const extract = (source: string) => {
  const match = source.match(/const timeline=(\[.*?\]),buttons=/s)
  if (!match) fail('timeline missing')
  return JSON.parse(match[1]) as Record<string, any>[]
}
const v7 = extract(v7Html), v8 = extract(html)
if (v7.length !== 4 || v8.length !== 4) fail('four-contact proof changed')
for (let index = 0; index < 4; index += 1) {
  const before = v7[index], after = v8[index]
  for (const key of ['xLp', 'supportXLp', 'targetXLp']) if (!near(after[key], before[key] + 6)) fail(`${key} is not +6 lp at F${index + 1}`)
  for (const key of ['bottomLp', 'supportYLp', 'targetYLp', 'durationMs', 'step', 'leg', 'supportTread', 'targetTread', 'phase', 'label']) if (after[key] !== before[key]) fail(`${key} changed at F${index + 1}`)
  if (after.src.replace('stair-ascent-v8', 'stair-ascent-v7') !== before.src) fail(`asset alias mismatch at F${index + 1}`)
  const expectedSupportX = 103.5 - index * 6
  const expectedTargetX = 97.5 - index * 6
  if (!near(after.supportXLp, expectedSupportX) || !near(after.targetXLp, expectedTargetX)) fail(`foot contact is not on floor/tread pair at F${index + 1}`)
}
if (v8[0].supportTread !== 0 || v8[0].targetTread !== 1 || !near(v8[0].supportXLp, 103.5) || !near(v8[0].targetXLp, 97.5)) fail('first step does not begin on floor and land on tread 1')
if (record.originalAndDraft.length !== 2 || record.originalAndDraft.some((entry: any) => entry.v7Sha256 !== entry.v8Sha256)) fail('V7 artwork bytes changed')
if (manifest.set !== 'keeper-prime-stair-ascent-v8' || Object.keys(manifest.entries).length !== 2) fail('archive manifest changed')
for (const url of record.frameUrls) if (!archive.legacyPaths[url] || !manifest.entries[url]) fail(`archive does not resolve ${url}`)
for (const phrase of ['V8 fixes V7’s one-tread horizontal offset', 'frame 1 starts from the floor and lands on tread 1', 'two-contact leg test', 'Exact game scale']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
try { fs.lstatSync(path.join(path.dirname(PAGE), 'assets')); fail('public page contains physical binary assets') } catch (error: any) {
  if (error.message?.startsWith('Keeper Prime stair ascent V8:')) throw error
  if (error.code !== 'ENOENT') throw error
}
for (const flag of ['v7ArtworkChanged', 'v7VerticalPositionsChanged', 'v7TimingChanged', 'stairGeometryChanged', 'v1ThroughV7Changed', 'finalChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} changed`)
console.log('Keeper Prime stair ascent V8 verified: complete character and contact guides shifted exactly one 6-lp tread right; frame 1 supports on the floor and lands on tread 1; V7 artwork, vertical geometry and timing unchanged.')
