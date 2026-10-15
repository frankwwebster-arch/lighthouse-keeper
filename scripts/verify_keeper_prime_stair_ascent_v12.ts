#!/usr/bin/env node
/** Verify V12's deeper-tread binding contacts and readable arm alternation. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v12')
const REGISTER = path.join(PACK, 'batch-register.json')
const PREP = path.join(PACK, 'source-preparation-v12.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v12.json')
const RIG = path.join(PACK, 'stair-contact-rig-v12.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v12/index.html')
const MANIFEST = path.join(ROOT, 'review-archive/sets/keeper-prime-stair-ascent-v12.json')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V12: ${message}`) }
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

if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v12' || record.status !== 'draft-v12-deeper-tread-contact-and-arm-gate-awaiting-review' || spec.promoted !== false) fail('identity, status or promotion boundary changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered spec or review page changed')
if (prep.frames.length !== 2 || rig.timeline.length !== 4 || rig.contactOrder.join(',') !== 'right,left,right,left') fail('contact frame count or order changed')
if (!near(rig.geometry.flightRunLp, 98) || !near(rig.geometry.flightRiseLp, 60) || rig.geometry.risers !== 14 || !near(rig.geometry.treadRunLp, 7) || !near(rig.geometry.reservedCoreRunLp, 105)) fail('deeper-tread geometry changed')

let prior: Record<string, any> | null = null
for (const frame of rig.timeline) {
  const source = prep.frames.find((entry: any) => entry.leg === frame.leg)
  if (!source) fail(`missing ${frame.leg} preparation`)
  const file = path.join(ROOT, source.draft.file)
  if (hash(file) !== source.draft.sha256) fail(`${frame.leg} draft changed`)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 256 || png.height !== 320) fail(`${frame.leg} cell geometry changed`)
  let edgeAlpha = 0
  for (let x = 0; x < 256; x += 1) for (const y of [0, 319]) if (png.data[(y * 256 + x) * 4 + 3]) edgeAlpha += 1
  for (let y = 1; y < 319; y += 1) for (const x of [0, 255]) if (png.data[(y * 256 + x) * 4 + 3]) edgeAlpha += 1
  if (edgeAlpha) fail(`${frame.leg} touches a cell edge`)
  if (!near(frame.supportClearanceLp, 0)) fail(`frame ${frame.frame} support sole is not on its tread`)
  if (Math.abs(frame.movingClearanceLp) > 0.05) fail(`frame ${frame.frame} upper sole misses target tread by ${frame.movingClearanceLp} lp`)
  const legSource = PNG.sync.read(fs.readFileSync(path.join(ROOT, source.legSource.file)))
  for (let y = 0; y <= 127; y += 1) for (let x = 0; x < 256; x += 1) {
    const offset = (y * 256 + x) * 4
    for (let channel = 0; channel < 4; channel += 1) if (png.data[offset + channel] !== legSource.data[offset + channel]) fail(`${frame.leg} changed Prime head above arm boundary at ${x},${y}`)
  }
  if (prior) {
    if (Math.abs(frame.supportXLp - prior.movingXLp) > 0.07 || Math.abs(frame.supportYLp - prior.movingYLp) > 0.04) fail(`frame ${prior.frame}→${frame.frame} does not transfer the upper foot continuously`)
  }
  prior = frame
}

const right = PNG.sync.read(fs.readFileSync(path.join(ROOT, prep.frames.find((entry: any) => entry.leg === 'right').draft.file)))
const left = PNG.sync.read(fs.readFileSync(path.join(ROOT, prep.frames.find((entry: any) => entry.leg === 'left').draft.file)))
let armRegionDifference = 0
for (let y = 128; y <= 270; y += 1) for (let x = 20; x <= 215; x += 1) {
  const offset = (y * 256 + x) * 4
  if ([0, 1, 2, 3].some((channel) => Math.abs(right.data[offset + channel] - left.data[offset + channel]) > 12)) armRegionDifference += 1
}
if (armRegionDifference < 1800) fail(`opposite arm silhouettes are not visually distinct enough (${armRegionDifference} changed pixels)`)

const match = html.match(/const timeline=(\[.*?\]),buttons=/s)
if (!match) fail('review timeline missing')
const pageTimeline = JSON.parse(match[1]) as Record<string, any>[]
if (JSON.stringify(pageTimeline) !== JSON.stringify(rig.timeline)) fail('page and sidecar timelines disagree')
if (!html.includes('Promise.all(unique.map(preload))') || !html.includes('Both contact drawings decoded')) fail('decode-before-play gate changed')
for (const phrase of ['exactly one 4.286-lp riser', 'RIGHT leg + LEFT arm', 'LEFT leg + RIGHT arm', 'Exact game scale', 'nothing promoted']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
if (manifest.set !== 'keeper-prime-stair-ascent-v12' || Object.keys(manifest.entries).length !== 2) fail('archive manifest changed')
for (const url of record.frameUrls) if (!manifest.entries[url] || !archive.legacyPaths[url]) fail(`archive does not resolve ${url}`)
try { fs.lstatSync(path.join(path.dirname(PAGE), 'assets')); fail('public page contains physical review binaries') } catch (error: any) {
  if (error.message?.startsWith('Keeper Prime stair ascent V12:')) throw error
  if (error.code !== 'ENOENT') throw error
}
for (const flag of ['v1ThroughV11Changed', 'finalChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} changed`)
console.log(`Keeper Prime stair ascent V12 verified: 14 deeper 7-lp treads over 98 × 60 lp, four supported contacts, ≤0.07-lp foot handovers, ${armRegionDifference} opposite-arm pixels, transparent gutters and unchanged Final/production boundaries.`)
