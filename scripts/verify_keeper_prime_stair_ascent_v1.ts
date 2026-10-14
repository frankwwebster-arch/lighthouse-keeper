#!/usr/bin/env node
/** Verify the reversible Keeper Prime walk-to-stair-ascent V1 review. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-14-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v1.json')
const PREP = path.join(PACK, 'source-preparation-v1.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v1/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V1: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, SPEC, PREP, PAGE, ARCHIVE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const prep = JSON.parse(fs.readFileSync(PREP, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-14-v1' || record.status !== 'draft-finished-art-walk-to-continuous-ascent-awaiting-review') fail('identity/status changed')
for (const entry of [...Object.values(record.authorities), ...Object.values(record.generation)] as Record<string, any>[]) {
  if (!entry.file) continue
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`registered source changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered candidate changed')
if (spec.route.transferDoorRootLp !== 115.5 || spec.route.stairBaseRootLp !== 94.5 || spec.route.walkDistanceLp !== 21 || spec.route.pauseFramesAtJoin !== 0) fail('door-to-stair join changed')
if (spec.route.climbCycles !== 8 || spec.route.climbFrames !== 64 || spec.route.cycleRunKu !== 84 || spec.route.cycleRiseKu !== 60 || spec.route.flightRunKu !== 672 || spec.route.flightRiseKu !== 480 || spec.route.upperLandingRootLp !== 10.5) fail('flight closure changed')
if (spec.climbRootDeltasKu.xTowardLeft.reduce((a: number, b: number) => a + b, 0) !== 84 || spec.climbRootDeltasKu.yUp.reduce((a: number, b: number) => a + b, 0) !== 60) fail('cycle deltas do not close')
if (prep.frames.length !== 8 || prep.targetCell.join('x') !== '256x320' || prep.headTopY !== 18) fail('prepared frame contract changed')
const edgeAlpha = (file: string) => {
  const png = PNG.sync.read(fs.readFileSync(file))
  let count = 0
  for (let x = 0; x < png.width; x++) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count++
  for (let y = 1; y < png.height - 1; y++) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count++
  return count
}
for (const frame of prep.frames) for (const [fileKey, hashKey] of [['rightFile', 'rightSha256'], ['leftFile', 'leftSha256']] as const) {
  const file = path.join(ROOT, frame[fileKey])
  if (!fs.existsSync(file) || hash(file) !== frame[hashKey]) fail(`prepared frame changed: ${frame[fileKey]}`)
  if (edgeAlpha(file) !== 0) fail(`shared-edge alpha in ${frame[fileKey]}`)
}
const html = fs.readFileSync(PAGE, 'utf8')
for (const phrase of ['walk directly into continuous climb', '0 pause frames', '16 risers', '84 lp run', '60 lp rise', 'Compact pacing preview', 'not a runtime-size claim', 'Promise.all(unique.map(preload))']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
const timelineMatch = html.match(/const timeline=(\[.*?\]),buttons=/s)
if (!timelineMatch) fail('timeline missing')
const timeline = JSON.parse(timelineMatch[1]) as Record<string, any>[]
if (timeline.length !== 72 || timeline.slice(0, 8).some((frame) => frame.phase !== 'walk') || timeline.slice(8).some((frame) => frame.phase !== 'climb')) fail('timeline phases changed')
if (timeline[7].xKu !== 756 || timeline[7].yKu !== 160 || timeline[8].xKu >= timeline[7].xKu || timeline[8].yKu <= timeline[7].yKu) fail('walk-to-climb join is not immediately advancing')
if (timeline.at(-1)?.xKu !== 84 || timeline.at(-1)?.yKu !== 640) fail('upper landing endpoint changed')
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
for (const url of record.frameUrls) if (!archive.legacyPaths[url]) fail(`archive does not resolve ${url}`)
for (const flag of ['walkClosesAtBase', 'firstClimbFrameAdvances', 'climbCycleCloses84x60Ku', 'flightCloses672x480Ku']) if (record.validation[flag] !== true) fail(`${flag} changed`)
for (const flag of ['approvedWalkPixelsChanged', 'runtimeChanged', 'finalChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} boundary changed`)
console.log('Keeper Prime stair ascent V1 verified: eight isolated poses, zero-pause walk join, 84×60-ku cycle and exact 672×480-ku flight closure.')
