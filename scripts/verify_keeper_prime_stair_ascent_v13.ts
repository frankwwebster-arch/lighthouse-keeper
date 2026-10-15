#!/usr/bin/env node
/** Verify V13: exact V12 contacts plus one raised passing frame per leg. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v13')
const V12 = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v12')
const REGISTER = path.join(PACK, 'batch-register.json')
const PREP = path.join(PACK, 'source-preparation-v13.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v13.json')
const RIG = path.join(PACK, 'stair-contact-rig-v13.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v13/index.html')
const MANIFEST = path.join(ROOT, 'review-archive/sets/keeper-prime-stair-ascent-v13.json')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V13: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const near = (a: number, b: number, epsilon = 1e-6) => Math.abs(a - b) <= epsilon
for (const file of [REGISTER, PREP, SPEC, RIG, PAGE, MANIFEST, ARCHIVE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}

const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const prep = JSON.parse(fs.readFileSync(PREP, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const rig = JSON.parse(fs.readFileSync(RIG, 'utf8')) as Record<string, any>
const v12Prep = JSON.parse(fs.readFileSync(path.join(V12, 'source-preparation-v12.json'), 'utf8')) as Record<string, any>
const v12Rig = JSON.parse(fs.readFileSync(path.join(V12, 'stair-contact-rig-v12.json'), 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) as Record<string, any>
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
const html = fs.readFileSync(PAGE, 'utf8')

if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v13' || record.status !== 'draft-v13-one-passing-frame-per-leg-awaiting-review' || spec.promoted !== false) fail('identity, status or promotion boundary changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered spec or review page changed')
if (prep.frames.length !== 2 || rig.timeline.length !== 5 || rig.sequence.join(',') !== 'LEFT contact,RIGHT mid-swing,RIGHT contact,LEFT mid-swing,LEFT contact') fail('five-frame alternating sequence changed')
if (rig.timeline.map((frame: any) => frame.kind).join(',') !== 'contact,mid-swing,contact,mid-swing,contact') fail('contact/passing cadence changed')
for (const key of ['floorTopLp', 'stairBaseRightLp', 'floorSupportCentreLp', 'flightRunLp', 'flightRiseLp', 'risers', 'treadRunLp', 'riserRiseLp', 'reservedCoreRunLp']) {
  if (!near(rig.geometry[key], v12Rig.geometry[key])) fail(`V12 geometry changed at ${key}`)
}
if (!near(rig.geometry.flightRunLp, 98) || !near(rig.geometry.flightRiseLp, 60) || rig.geometry.risers !== 14 || !near(rig.geometry.treadRunLp, 7) || !near(rig.geometry.reservedCoreRunLp, 105) || rig.geometry.framesPerStep !== 2) fail('binding stair or cadence geometry changed')

const assetByUrl = Object.fromEntries(record.assets.map((entry: any) => [entry.url, entry])) as Record<string, any>
for (const entry of record.assets) {
  const file = path.join(ROOT, entry.source)
  if (!fs.existsSync(file) || hash(file) !== entry.sourceSha256) fail(`registered source changed: ${entry.source}`)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 256 || png.height !== 320) fail(`${entry.source} cell geometry changed`)
  let edgeAlpha = 0
  for (let x = 0; x < 256; x += 1) for (const y of [0, 319]) if (png.data[(y * 256 + x) * 4 + 3]) edgeAlpha += 1
  for (let y = 1; y < 319; y += 1) for (const x of [0, 255]) if (png.data[(y * 256 + x) * 4 + 3]) edgeAlpha += 1
  if (edgeAlpha) fail(`${entry.source} touches a cell edge`)
}

for (const mid of prep.frames) {
  if (!mid.byteIdenticalToLegSource || !mid.protected.entireFrameExactV6PassingPose) fail(`${mid.movingLeg} passing provenance changed`)
  const source = path.join(ROOT, mid.legSource.file)
  const draft = path.join(ROOT, mid.draft.file)
  if (hash(source) !== mid.legSource.sha256 || hash(draft) !== mid.draft.sha256 || hash(source) !== hash(draft)) fail(`${mid.movingLeg} passing frame is not exact V6 pose 3`)
  if (!mid.legSource.file.endsWith('_f03.png')) fail(`${mid.movingLeg} passing frame is no longer the raised pose 3`)
  if (mid.supportSole.y !== 316 || mid.edgeAlpha !== 0) fail(`${mid.movingLeg} support datum or gutter changed`)
  for (const generated of [mid.rejectedArmStudy, mid.registeredRejectedArmStudy]) {
    const file = path.join(ROOT, generated.file)
    if (!fs.existsSync(file) || hash(file) !== generated.sha256) fail(`rejected provenance changed: ${generated.file}`)
  }
}
for (const generated of prep.rejectedArmSources) if (!generated.reason.includes('endpoint-like arm extreme')) fail('rejected arm-study reason changed')

for (const frame of rig.timeline) {
  if (!assetByUrl[frame.src]) fail(`frame ${frame.frame} URL is not registered`)
  if (!near(frame.supportClearanceLp, 0)) fail(`frame ${frame.frame} support sole is not planted`)
  const expectedX = rig.geometry.floorSupportCentreLp - frame.supportTread * rig.geometry.treadRunLp
  const expectedY = rig.geometry.floorTopLp + frame.supportTread * rig.geometry.riserRiseLp
  if (!near(frame.supportXLp, expectedX) || !near(frame.supportYLp, expectedY)) fail(`frame ${frame.frame} support is not on the declared tread`)
  if (frame.targetTread !== frame.supportTread + 1) fail(`frame ${frame.frame} target tread changed`)
  if (frame.kind === 'contact') {
    const source = v12Prep.frames.find((entry: any) => entry.leg === frame.leg)
    if (!source || assetByUrl[frame.src].sourceSha256 !== source.draft.sha256) fail(`frame ${frame.frame} is not an exact V12 contact`)
    if (Math.abs(frame.movingClearanceLp) > 0.05) fail(`frame ${frame.frame} upper sole misses target by ${frame.movingClearanceLp} lp`)
  } else {
    const source = prep.frames.find((entry: any) => entry.movingLeg === frame.movingLeg)
    if (!source || assetByUrl[frame.src].sourceSha256 !== source.draft.sha256) fail(`frame ${frame.frame} is not the registered raised passing pose`)
  }
}
for (const [from, mid, to] of [[rig.timeline[0], rig.timeline[1], rig.timeline[2]], [rig.timeline[2], rig.timeline[3], rig.timeline[4]]]) {
  if (mid.supportTread !== from.targetTread || to.supportTread !== mid.supportTread) fail(`support transfer ${from.frame}→${mid.frame}→${to.frame} changed`)
  if (!near(mid.supportXLp, to.supportXLp) || !near(mid.supportYLp, to.supportYLp)) fail(`passing frame ${mid.frame} does not lock to the following contact's support tread`)
}

const match = html.match(/const timeline=(\[.*?\]),buttons=/s)
if (!match) fail('review timeline missing')
const pageTimeline = JSON.parse(match[1]) as Record<string, any>[]
if (JSON.stringify(pageTimeline) !== JSON.stringify(rig.timeline)) fail('page and sidecar timelines disagree')
if (!html.includes('Promise.all(unique.map(preload))') || !html.includes('All four unique drawings decoded')) fail('decode-before-play gate changed')
for (const phrase of ['LEFT contact → RIGHT foot passes → RIGHT contact', 'planted boot stays on its tread', 'Exact game scale', 'nothing promoted']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
if (manifest.set !== 'keeper-prime-stair-ascent-v13' || record.frameUrls.length !== 4) fail('archive identity or current four-drawing contract changed')
for (const url of record.frameUrls) if (!manifest.entries[url] || !archive.legacyPaths[url]) fail(`archive does not resolve ${url}`)
try { fs.lstatSync(path.join(path.dirname(PAGE), 'assets')); fail('public page contains physical review binaries') } catch (error: any) {
  if (error.message?.startsWith('Keeper Prime stair ascent V13:')) throw error
  if (error.code !== 'ENOENT') throw error
}
for (const flag of ['finalChanged', 'runtimeSpritesChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} changed`)
console.log('Keeper Prime stair ascent V13 verified: exact V12 contacts, exact raised V6 passing pose per leg, contact→passing→contact cadence, planted support locks, 14 × 7-lp stair geometry, transparent gutters, archive agreement and unchanged Final/runtime/production boundaries.')
