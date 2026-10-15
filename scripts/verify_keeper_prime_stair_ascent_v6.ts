#!/usr/bin/env node
/** Verify Stair Ascent V6 geometry, media isolation, archive and immutable boundaries. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v6')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v6.json')
const PREP = path.join(PACK, 'source-preparation-v6.json')
const RIG = path.join(PACK, 'stair-contact-rig-v6.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v6/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const MANIFEST = path.join(ROOT, 'review-archive/sets/keeper-prime-stair-ascent-v6.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V6: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const near = (a: number, b: number, epsilon = 1e-9) => Math.abs(a - b) <= epsilon
for (const file of [REGISTER, SPEC, PREP, RIG, PAGE, ARCHIVE, MANIFEST, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const prep = JSON.parse(fs.readFileSync(PREP, 'utf8')) as Record<string, any>
const rig = JSON.parse(fs.readFileSync(RIG, 'utf8')) as Record<string, any>
const html = fs.readFileSync(PAGE, 'utf8')
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v6' || record.status !== 'draft-v6-equal-leg-fourteen-contact-ascent-awaiting-review') fail('identity/status changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered V6 candidate changed')
if (spec.correction.risers !== 14 || spec.correction.leftContacts !== 7 || spec.correction.rightContacts !== 7) fail('50/50 contact geometry changed')
if (!near(spec.correction.treadRunLp, 6) || !near(spec.correction.riserRiseLp, 60 / 14)) fail('tread dimensions changed')
if (rig.cadence.framesPerStep !== 6 || rig.cadence.millisecondsPerStep !== 360 || rig.cadence.priorV5MillisecondsPerStep !== 368) fail('cadence contract changed')

const timelineMatch = html.match(/const timeline=(\[.*?\]),buttons=/s)
if (!timelineMatch) fail('timeline missing')
const timeline = JSON.parse(timelineMatch[1]) as Record<string, any>[]
if (timeline.length !== 92) fail('timeline must contain 8 walk + 84 climb frames')
const climb = timeline.slice(8)
let left = 0, right = 0
for (let step = 0; step < 14; step += 1) {
  const frames = climb.slice(step * 6, step * 6 + 6)
  const expectedLeg = step % 2 === 0 ? 'left' : 'right'
  if (expectedLeg === 'left') left += 1; else right += 1
  for (let pose = 0; pose < 6; pose += 1) {
    const frame = frames[pose]
    if (frame.step !== step + 1 || frame.leg !== expectedLeg || frame.pose !== pose + 1) fail(`leg/pose mismatch at step ${step + 1} pose ${pose + 1}`)
    const expectedX = 94.5 - step * 6 - rig.rootRunLp[pose]
    const expectedBottom = 19.5 + step * (60 / 14) + rig.rootRiseFactor[pose] * (60 / 14)
    if (!near(frame.xLp, expectedX) || !near(frame.bottomLp, expectedBottom)) fail(`root mismatch at step ${step + 1} pose ${pose + 1}`)
    if (pose > 0 && frame.xLp > frames[pose - 1].xLp) fail(`backward root slide at step ${step + 1}`)
    if (frame.durationMs !== 60) fail(`climb timing changed at step ${step + 1} pose ${pose + 1}`)
    if (frame.supportTread !== (pose === 5 ? step + 1 : step)) fail(`support tread mismatch at step ${step + 1} pose ${pose + 1}`)
  }
}
if (left !== 7 || right !== 7 || record.validation.leftContacts !== 7 || record.validation.rightContacts !== 7) fail('leg work is not exactly 50/50')
if (!near(climb.at(-1)?.xLp, 10.5) || !near(climb.at(-1)?.bottomLp, 79.5) || climb.at(-1)?.supportTread !== 14) fail('flight does not close exactly')

if (prep.frames.length !== 12 || prep.target.width !== 256 || prep.target.height !== 320 || prep.target.safetyGutter !== 3) fail('prepared frame contract changed')
const authority = PNG.sync.read(fs.readFileSync(path.join(ROOT, prep.upperBodyLock.authority)))
for (const frame of prep.frames) {
  for (const direction of ['right', 'left']) {
    const file = path.join(ROOT, frame[`${direction}File`])
    if (!fs.existsSync(file) || hash(file) !== frame[`${direction}Sha256`]) fail(`${direction} frame changed: ${frame.leg} F${frame.pose}`)
    const png = PNG.sync.read(fs.readFileSync(file))
    if (png.width !== 256 || png.height !== 320) fail(`cell geometry changed: ${frame.leg} F${frame.pose}`)
    let edge = 0
    for (let x = 0; x < png.width; x += 1) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) edge += 1
    for (let y = 1; y < png.height - 1; y += 1) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) edge += 1
    if (edge !== 0) fail(`edge alpha at ${frame.leg} F${frame.pose} ${direction}`)
  }
  const right = PNG.sync.read(fs.readFileSync(path.join(ROOT, frame.rightFile)))
  for (let y = 0; y <= prep.upperBodyLock.exactThroughY; y += 1) for (let x = 0; x < right.width; x += 1) {
    const offset = (y * right.width + x) * 4
    for (let channel = 0; channel < 4; channel += 1) if (right.data[offset + channel] !== authority.data[offset + channel]) fail(`upper body drift at ${frame.leg} F${frame.pose}`)
  }
  if (frame.alphaBounds.minY !== 31 || frame.alphaBounds.maxY !== 316 || frame.edgeAlpha !== 0) fail(`registered bounds changed at ${frame.leg} F${frame.pose}`)
  if (frame.pose === 4) {
    const leftFacing = PNG.sync.read(fs.readFileSync(path.join(ROOT, frame.leftFile)))
    const maxY = (fromX: number, toX: number) => {
      let result = -1
      for (let y = 230; y < leftFacing.height; y += 1) for (let x = fromX; x < toX; x += 1) if (leftFacing.data[(y * leftFacing.width + x) * 4 + 3] > 32) result = Math.max(result, y)
      return result
    }
    const movingSoleY = maxY(0, 108)
    const supportSoleY = maxY(108, 256)
    const separation = supportSoleY - movingSoleY
    if (supportSoleY < 315 || movingSoleY < 274 || movingSoleY > 284 || separation < 32 || separation > 42) fail(`${frame.leg} F4 is not one-riser contact geometry`)
  }
}

if (manifest.set !== 'keeper-prime-stair-ascent-v6' || Object.keys(manifest.entries).length < 22) fail('archive manifest changed')
for (const url of record.frameUrls) if (!archive.legacyPaths[url] || !manifest.entries[url]) fail(`archive does not resolve ${url}`)
for (const phrase of ['exact 50/50 alternating contacts', '7 LEFT + 7 RIGHT', '6 frames per step', '6 lp × 4.286 lp', '84 × 60 lp', 'Loop one LEFT + RIGHT pair', 'Exact game scale']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
try {
  fs.lstatSync(path.join(path.dirname(PAGE), 'assets'))
  fail('public page contains physical binary assets')
} catch (error: any) {
  if (error.message?.startsWith('Keeper Prime stair ascent V6:')) throw error
  if (error.code !== 'ENOENT') throw error
}
for (const flag of ['v1ThroughV5Changed', 'finalChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} changed`)
console.log('Keeper Prime stair ascent V6 verified: 7 left + 7 right adjacent-tread contacts, six frames per step at preserved cadence, stable upper body, safe cells and exact 84 × 60 lp closure.')
