#!/usr/bin/env node
/** Verify Stair Ascent V5 root phasing, archive reuse and immutable boundaries. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v5')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v5.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v5/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const MANIFEST = path.join(ROOT, 'review-archive/sets/keeper-prime-stair-ascent-v5.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V5: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
for (const file of [REGISTER, SPEC, PAGE, ARCHIVE, MANIFEST, path.join(PACK, 'HANDOFF.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const html = fs.readFileSync(PAGE, 'utf8')
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v5' || record.status !== 'draft-v5-independent-leg-root-phasing-awaiting-review') fail('identity/status changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered V5 candidate changed')
for (const flag of ['v3CharacterMediaBytes', 'frameDurations', 'staircaseGeometry', 'walkApproach', 'finalLane', 'production']) if (spec.unchanged[flag] !== true) fail(`${flag} boundary weakened`)
const timelineMatch = html.match(/const timeline=(\[.*?\]),buttons=/s)
if (!timelineMatch) fail('timeline missing')
const timeline = JSON.parse(timelineMatch[1]) as Record<string, any>[]
if (timeline.length !== 72) fail('timeline must contain 8 walk + 64 climb frames')
const climb = timeline.slice(8)
const expectedRoot = [[0,0],[1,0],[2,0],[5.25,3.75],[5.25,3.75],[6.25,3.75],[7.25,3.75],[10.5,7.5]]
for (let cycle = 0; cycle < 8; cycle += 1) {
  const frames = climb.slice(cycle * 8, cycle * 8 + 8)
  for (let index = 0; index < 8; index += 1) {
    const frame = frames[index]
    const [rootX, rootY] = expectedRoot[index]
    const expectedX = 94.5 - cycle * 10.5 - rootX
    const expectedBottom = 19.5 + cycle * 7.5 + rootY
    const expectedTread = cycle * 2 + (index >= 7 ? 2 : index >= 3 ? 1 : 0)
    if (frame.xLp !== expectedX || frame.bottomLp !== expectedBottom || frame.supportTread !== expectedTread) fail(`root/contact mismatch at cycle ${cycle + 1} pose ${index + 1}`)
    if (index > 0 && frame.xLp > frames[index - 1].xLp) fail(`backward slide at cycle ${cycle + 1} pose ${index + 1}`)
  }
  if (frames[3].bottomLp - frames[2].bottomLp !== 3.75 || frames[7].bottomLp - frames[6].bottomLp !== 3.75) fail(`landing rise changed in cycle ${cycle + 1}`)
}
if (climb.at(-1)?.xLp !== 10.5 || climb.at(-1)?.bottomLp !== 79.5 || climb.at(-1)?.supportTread !== 16) fail('flight does not close at upper landing')
if (manifest.set !== 'keeper-prime-stair-ascent-v5' || Object.keys(manifest.entries).length !== 17) fail('archive manifest changed')
for (let index = 0; index < record.frameUrls.length; index += 1) {
  const v5Url = record.frameUrls[index]
  const v3Url = record.generation.sourceFrameUrls[index]
  if (!archive.legacyPaths[v5Url] || !manifest.entries[v5Url]) fail(`archive does not resolve ${v5Url}`)
  if (archive.legacyPaths[v5Url].sha256 !== archive.legacyPaths[v3Url].sha256) fail(`V5/V3 media bytes differ at ${v5Url}`)
}
for (const phrase of ['independent left/right steps', 'Translucent bannister', 'id="opacity"', 'value="55"', 'near leg lands +1 riser', 'far leg lands +1 riser', 'Monotonic root', '16 single steps']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
if (!html.includes('.game .world{left:0;bottom:0;top:auto;right:auto;')) fail('exact logical-scale world is not bottom-left aligned')
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
try {
  fs.lstatSync(path.join(path.dirname(PAGE), 'assets'))
  fail('public page contains physical binary assets')
} catch (error: any) {
  if (error.message?.startsWith('Keeper Prime stair ascent V5:')) throw error
  if (error.code !== 'ENOENT') throw error
}
for (const flag of ['rootMonotonic', 'risesOnlyOnF4AndF8', 'oneRiserPerLegLanding', 'sixteenSingleSteps']) if (record.validation[flag] !== true) fail(`${flag} validation weakened`)
for (const flag of ['v3MediaBytesChanged', 'frameDurationsChanged', 'stairGeometryChanged', 'finalChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} changed`)
console.log('Keeper Prime stair ascent V5 verified: separate four-frame near/far leg steps, one-riser F4/F8 landings, monotonic root, exact 84 × 60 lp closure and unchanged V3 media.')
