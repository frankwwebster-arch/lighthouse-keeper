#!/usr/bin/env node
/** Verify V11's same-family alternating stair intermediates. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v11')
const REGISTER = path.join(PACK, 'batch-register.json')
const PREP = path.join(PACK, 'source-preparation-v11.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v11.json')
const RIG = path.join(PACK, 'stair-contact-rig-v11.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v11/index.html')
const MANIFEST = path.join(ROOT, 'review-archive/sets/keeper-prime-stair-ascent-v11.json')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V11: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const near = (a: number, b: number, epsilon = 1e-6) => Math.abs(a - b) <= epsilon
for (const file of [REGISTER, PREP, SPEC, RIG, PAGE, MANIFEST, ARCHIVE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const prep = JSON.parse(fs.readFileSync(PREP, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const rig = JSON.parse(fs.readFileSync(RIG, 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) as Record<string, any>
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
const html = fs.readFileSync(PAGE, 'utf8')
if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v11' || record.status !== 'draft-v11-alternating-intermediates-awaiting-review' || spec.promoted !== false) fail('identity, status or promotion boundary changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered spec or page changed')
if (prep.frames.length !== 8 || record.originalAndDraft.length !== 6 || rig.geometry.framesPerStep !== 3) fail('pose count changed')

function assertUnchangedOutsideArm(source: PNG, draft: PNG, label: string) {
  if (source.width !== 256 || source.height !== 320 || draft.width !== 256 || draft.height !== 320) fail(`${label} cell geometry changed`)
  for (let y = 0; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
    const insideArmWarp = x >= 96 && x <= 184 && y >= 128 && y <= 246
    if (insideArmWarp) continue
    const offset = (y * 256 + x) * 4
    for (let channel = 0; channel < 4; channel += 1) if (source.data[offset + channel] !== draft.data[offset + channel]) fail(`${label} changed outside arm warp at ${x},${y}`)
  }
  let edgeAlpha = 0
  for (let x = 0; x < 256; x += 1) for (const y of [0, 319]) if (draft.data[(y * 256 + x) * 4 + 3]) edgeAlpha += 1
  for (let y = 1; y < 319; y += 1) for (const x of [0, 255]) if (draft.data[(y * 256 + x) * 4 + 3]) edgeAlpha += 1
  if (edgeAlpha) fail(`${label} touches a cell edge`)
}
for (const frame of prep.frames) {
  const sourceFile = path.join(ROOT, frame.sourceFile), draftFile = path.join(ROOT, frame.file)
  if (hash(sourceFile) !== frame.sourceSha256 || hash(draftFile) !== frame.sha256) fail(`${frame.leg} F${frame.pose} hash changed`)
  assertUnchangedOutsideArm(PNG.sync.read(fs.readFileSync(sourceFile)), PNG.sync.read(fs.readFileSync(draftFile)), `${frame.leg} F${frame.pose}`)
}
if (Math.max(...prep.frames.filter((frame: any) => frame.leg === 'right').map((frame: any) => frame.armForwardPixels)) !== 3) fail('right-step modest arm amplitude changed')
if (Math.max(...prep.frames.filter((frame: any) => frame.leg === 'left').map((frame: any) => frame.armForwardPixels)) !== 7) fail('left-step stronger arm amplitude changed')

const match = html.match(/const timeline=(\[.*?\]),buttons=/s)
if (!match) fail('timeline missing')
const timeline = JSON.parse(match[1]) as Record<string, any>[]
if (timeline.length !== 12 || new Set(timeline.map((frame) => frame.src)).size !== 6) fail('four-step/six-drawing review sequence changed')
const pattern = ['right', 'left', 'right', 'left']
const selectedPoses = [1, 3, 4]
const sourceByKey = Object.fromEntries(prep.frames.map((frame: any) => [`${frame.leg}:${frame.pose}`, frame])) as Record<string, any>
const rise = 60 / 14
const surface = (x: number) => x >= 100.5 ? 20 : 20 + (Math.floor((100.5 - x - 1e-6) / 6) + 1) * rise
for (let step = 0; step < 4; step += 1) {
  const frames = timeline.slice(step * 3, step * 3 + 3)
  if (frames.some((frame, index) => frame.step !== step + 1 || frame.leg !== pattern[step] || frame.pose !== selectedPoses[index])) fail(`step ${step + 1} order changed`)
  if (!near(frames[0].xLp, 109.875 - step * 6) || !near(frames[2].xLp, frames[0].xLp - 6)) fail(`step ${step + 1} does not advance exactly one tread`)
  if (!frames.every((frame) => near(frame.bottomLp, 19.5 + step * rise))) fail(`step ${step + 1} support height changed`)
  for (const frame of frames) {
    const source = sourceByKey[`${frame.leg}:${frame.pose}`]
    const png = PNG.sync.read(fs.readFileSync(path.join(ROOT, source.file)))
    let minimumClearance = Number.POSITIVE_INFINITY
    for (let y = 210; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
      if (png.data[(y * 256 + x) * 4 + 3] <= 32) continue
      const worldX = frame.xLp - 16 + x / 8
      const worldY = frame.bottomLp + (320 - y) / 8
      minimumClearance = Math.min(minimumClearance, worldY - surface(worldX))
    }
    if (minimumClearance < -0.2) fail(`${frame.leg} F${frame.pose} penetrates stair by ${-minimumClearance} lp`)
  }
}
for (let step = 0; step < 3; step += 1) if (!near(timeline[step * 3 + 2].xLp, timeline[(step + 1) * 3].xLp)) fail(`horizontal root jumps between steps ${step + 1} and ${step + 2}`)
if (!html.includes('Promise.all(unique.map(preload))') || !html.includes("All '+unique.length+' unique drawings decoded")) fail('decode-before-play gate changed')
for (const phrase of ['RIGHT leg + LEFT arm', 'LEFT leg + RIGHT arm', 'Exact game scale', 'nothing promoted']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
if (manifest.set !== 'keeper-prime-stair-ascent-v11' || Object.keys(manifest.entries).length !== 6) fail('archive manifest changed')
for (const url of record.frameUrls) if (!manifest.entries[url] || !archive.legacyPaths[url]) fail(`archive does not resolve ${url}`)
try { fs.lstatSync(path.join(path.dirname(PAGE), 'assets')); fail('public page contains physical review binaries') } catch (error: any) {
  if (error.message?.startsWith('Keeper Prime stair ascent V11:')) throw error
  if (error.code !== 'ENOENT') throw error
}
for (const flag of ['v1ThroughV10Changed', 'finalChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} changed`)
console.log('Keeper Prime stair ascent V11 verified: four alternating adjacent steps, six same-family drawings, asymmetric contralateral arm motion, no tread penetration beyond 0.2 lp, transparent gutters and unchanged Final/production boundaries.')
