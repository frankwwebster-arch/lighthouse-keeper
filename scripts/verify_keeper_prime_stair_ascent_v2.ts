#!/usr/bin/env node
/** Verify Stair Ascent V2 without weakening or rewriting V1. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v2')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v2.json')
const PREP = path.join(PACK, 'source-preparation-v2.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v2/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V2: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const mirror = (source: PNG) => {
  const output = new PNG({ width: source.width, height: source.height })
  for (let y = 0; y < source.height; y++) for (let x = 0; x < source.width; x++) {
    const from = (y * source.width + x) * 4
    const to = (y * source.width + source.width - 1 - x) * 4
    for (let channel = 0; channel < 4; channel++) output.data[to + channel] = source.data[from + channel]
  }
  return output
}
const edgeAlpha = (png: PNG) => {
  let count = 0
  for (let x = 0; x < png.width; x++) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count++
  for (let y = 1; y < png.height - 1; y++) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) count++
  return count
}
const differingLowerPixels = (a: PNG, b: PNG) => {
  let count = 0
  for (let y = 160; y < a.height; y++) for (let x = 0; x < a.width; x++) {
    const offset = (y * a.width + x) * 4
    if ([0, 1, 2, 3].some((channel) => a.data[offset + channel] !== b.data[offset + channel])) count++
  }
  return count
}

for (const file of [REGISTER, SPEC, PREP, PAGE, ARCHIVE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const prep = JSON.parse(fs.readFileSync(PREP, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v2' || record.status !== 'draft-v2-forward-exit-alternating-leg-climb-awaiting-review') fail('identity/status changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered candidate changed')
if (!spec.unchanged.v1 || !spec.unchanged.approvedWalkSourcePixels || !spec.unchanged.runtimeGeometry || !spec.unchanged.finalLane || !spec.unchanged.production) fail('unchanged boundary weakened')
if (spec.route.walkDistanceLp !== 21 || spec.route.pauseFramesAtJoin !== 0 || spec.route.flightRunKu !== 672 || spec.route.flightRiseKu !== 480) fail('route closure changed')
if (prep.frames.length !== 8 || prep.walkFrames.length !== 8 || prep.targetCell.join('x') !== '256x320' || prep.headTopY !== 18) fail('prepared frame contract changed')

const climbPngs: PNG[] = []
for (const frame of prep.frames) {
  for (const [fileKey, hashKey] of [['rightFile', 'rightSha256'], ['leftFile', 'leftSha256']] as const) {
    const file = path.join(ROOT, frame[fileKey])
    if (!fs.existsSync(file) || hash(file) !== frame[hashKey]) fail(`climb frame changed: ${frame[fileKey]}`)
    const png = PNG.sync.read(fs.readFileSync(file))
    if (edgeAlpha(png)) fail(`shared-edge alpha in ${frame[fileKey]}`)
    if (fileKey === 'leftFile') climbPngs.push(png)
  }
}
for (let frame = 0; frame < 4; frame++) if (differingLowerPixels(climbPngs[frame], climbPngs[frame + 4]) < 12000) fail(`opposite-leg phase ${frame + 1}/${frame + 5} is insufficiently distinct`)
for (const frame of prep.walkFrames) {
  const authority = PNG.sync.read(fs.readFileSync(path.join(ROOT, frame.rightAuthority)))
  const leftFile = path.join(ROOT, frame.leftFile)
  if (hash(path.join(ROOT, frame.rightAuthority)) !== frame.rightSha256 || hash(leftFile) !== frame.leftSha256) fail(`walk frame ${frame.frame} changed`)
  const actual = PNG.sync.read(fs.readFileSync(leftFile))
  if (!mirror(authority).data.equals(actual.data)) fail(`walk frame ${frame.frame} is not an exact horizontal mirror`)
  if (edgeAlpha(actual)) fail(`shared-edge alpha in mirrored walk frame ${frame.frame}`)
}

const html = fs.readFileSync(PAGE, 'utf8')
for (const phrase of ['forward exit + alternating legs', 'emerge from the doorway face-first', 'F1–F4 / F5–F8', 'facing '+"'"+'+f.facing+'+"'"+' ←', 'Promise.all(unique.map(preload))']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
const timelineMatch = html.match(/const timeline=(\[.*?\]),buttons=/s)
if (!timelineMatch) fail('timeline missing')
const timeline = JSON.parse(timelineMatch[1]) as Record<string, any>[]
if (timeline.length !== 72 || timeline.some((frame) => frame.facing !== 'left')) fail('timeline direction changed')
if (timeline.slice(0, 8).some((frame) => frame.phase !== 'forward walk from door') || timeline.slice(8).some((frame) => frame.phase !== 'alternating stair climb')) fail('timeline phases changed')
if (timeline[0].xKu >= 924 || timeline[7].xKu !== 756 || timeline[8].xKu >= timeline[7].xKu || timeline[8].yKu <= timeline[7].yKu) fail('forward walk or advancing join changed')
if (timeline.at(-1)?.xKu !== 84 || timeline.at(-1)?.yKu !== 640) fail('upper landing endpoint changed')
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
for (const url of record.frameUrls) if (!archive.legacyPaths[url]) fail(`archive does not resolve ${url}`)
for (const flag of ['spriteFacesRootMotion', 'approvedWalkMirroredOnly', 'oppositeLegHalfCyclesDeclared', 'walkClosesAtBase', 'firstClimbFrameAdvances', 'climbCycleCloses84x60Ku', 'flightCloses672x480Ku']) if (record.validation[flag] !== true) fail(`${flag} changed`)
for (const flag of ['v1Changed', 'approvedWalkChanged', 'runtimeChanged', 'finalChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} boundary changed`)
console.log('Keeper Prime stair ascent V2 verified: forward-facing door exit, exact mirrored walk, alternating-leg climb, safe gutters and unchanged route closure.')
