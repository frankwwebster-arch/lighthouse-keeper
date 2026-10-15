#!/usr/bin/env node
/** Verify V14 restrained arms, synchronous phases and boot/stair clearance. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v14')
const V12 = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v12')
const V13 = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v13')
const REGISTER = path.join(PACK, 'batch-register.json')
const PREP = path.join(PACK, 'source-preparation-v14.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v14.json')
const RIG = path.join(PACK, 'stair-contact-rig-v14.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v14/index.html')
const MANIFEST = path.join(ROOT, 'review-archive/sets/keeper-prime-stair-ascent-v14.json')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V14: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const near = (a: number, b: number, epsilon = 1e-6) => Math.abs(a - b) <= epsilon
for (const file of [REGISTER, PREP, SPEC, RIG, PAGE, MANIFEST, ARCHIVE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const prep = JSON.parse(fs.readFileSync(PREP, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const rig = JSON.parse(fs.readFileSync(RIG, 'utf8')) as Record<string, any>
const v12Prep = JSON.parse(fs.readFileSync(path.join(V12, 'source-preparation-v12.json'), 'utf8')) as Record<string, any>
const v13Prep = JSON.parse(fs.readFileSync(path.join(V13, 'source-preparation-v13.json'), 'utf8')) as Record<string, any>
const v13Rig = JSON.parse(fs.readFileSync(path.join(V13, 'stair-contact-rig-v13.json'), 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) as Record<string, any>
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
const html = fs.readFileSync(PAGE, 'utf8')

if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v14' || record.status !== 'draft-v14-restrained-synchronised-arms-and-compact-passing-boots-awaiting-review' || spec.promoted !== false) fail('identity, status or promotion boundary changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) { const file = path.join(ROOT, entry.file); if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`) }
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered spec or page changed')
if (prep.contacts.length !== 2 || prep.passing.length !== 2 || rig.timeline.length !== 5) fail('source or timeline frame count changed')
if (rig.timeline.map((f: any) => f.kind).join(',') !== 'contact,passing,contact,passing,contact') fail('synchronized contact/passing cadence changed')
if (rig.sequence.join(',') !== 'LEFT contact,RIGHT compact passing,RIGHT contact,LEFT compact passing,LEFT contact') fail('phase order changed')
for (const key of ['floorTopLp', 'stairBaseRightLp', 'floorSupportCentreLp', 'flightRunLp', 'flightRiseLp', 'risers', 'treadRunLp', 'riserRiseLp', 'reservedCoreRunLp']) if (!near(rig.geometry[key], v13Rig.geometry[key])) fail(`accepted geometry changed at ${key}`)
if (rig.geometry.risers !== 14 || !near(rig.geometry.treadRunLp, 7) || !near(rig.geometry.flightRunLp, 98) || !near(rig.geometry.flightRiseLp, 60)) fail('binding stair geometry changed')

function edgeAlpha(png: PNG) {
  let total = 0
  for (let x = 0; x < png.width; x += 1) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) total += 1
  for (let y = 1; y < png.height - 1; y += 1) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) total += 1
  return total
}
function changedOutsideMask(base: PNG, candidate: PNG, mask: PNG) {
  let changed = 0
  for (let i = 0; i < base.width * base.height; i += 1) {
    if (mask.data[i * 4] !== 0) continue
    if ([0, 1, 2, 3].some((channel) => base.data[i * 4 + channel] !== candidate.data[i * 4 + channel])) changed += 1
  }
  return changed
}
const assetByUrl = Object.fromEntries(record.assets.map((entry: any) => [entry.url, entry])) as Record<string, any>
for (const entry of record.assets) {
  const file = path.join(ROOT, entry.source)
  if (!fs.existsSync(file) || hash(file) !== entry.sourceSha256) fail(`asset source changed: ${entry.source}`)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 256 || png.height !== 320 || edgeAlpha(png)) fail(`${entry.source} cell or gutter changed`)
}
for (const frame of prep.contacts) {
  const candidateFile = path.join(ROOT, frame.draft.file), maskFile = path.join(ROOT, frame.mask.file)
  const old = v12Prep.frames.find((entry: any) => entry.leg === frame.leg)
  if (!old) fail(`missing V12 ${frame.leg} authority`)
  const base = PNG.sync.read(fs.readFileSync(path.join(ROOT, old.draft.file)))
  const candidate = PNG.sync.read(fs.readFileSync(candidateFile))
  const mask = PNG.sync.read(fs.readFileSync(maskFile))
  if (hash(candidateFile) !== frame.draft.sha256 || hash(maskFile) !== frame.mask.sha256) fail(`${frame.leg} contact hash changed`)
  if (changedOutsideMask(base, candidate, mask) !== 0 || frame.outsideMaskChangedPixels !== 0) fail(`${frame.leg} contact changed outside arm mask`)
  const offset = frame.nearHand.offsetFromPlumbX137Px
  if (Math.abs(offset) < 10 || Math.abs(offset) > 16) fail(`${frame.leg} near-arm swing is not restrained (${offset}px)`)
  if ((frame.leg === 'right' && offset >= 0) || (frame.leg === 'left' && offset <= 0)) fail(`${frame.leg} arm direction no longer opposes the other contact`)
  if (frame.farHandVisibleSkinSamples > 100) fail(`${frame.leg} far/right arm is too visible (${frame.farHandVisibleSkinSamples} samples)`)
  const legSource = PNG.sync.read(fs.readFileSync(path.join(ROOT, frame.baseLegSource.file)))
  for (let y = 0; y <= 127; y += 1) for (let x = 0; x < 256; x += 1) { const i = (y * 256 + x) * 4; for (let c = 0; c < 4; c += 1) if (candidate.data[i + c] !== legSource.data[i + c]) fail(`${frame.leg} changed Prime identity above arm boundary`) }
}

function stairSurface(x: number) {
  const g = rig.geometry
  if (x >= g.stairBaseRightLp) return g.floorTopLp
  if (x < g.stairBaseRightLp - g.flightRunLp) return g.floorTopLp + g.flightRiseLp
  return g.floorTopLp + (Math.floor((g.stairBaseRightLp - x - 1e-9) / g.treadRunLp) + 1) * g.riserRiseLp
}
for (const frame of prep.passing) {
  const candidateFile = path.join(ROOT, frame.draft.file), baseFile = path.join(ROOT, frame.base.file), maskFile = path.join(ROOT, frame.mask.file)
  const candidate = PNG.sync.read(fs.readFileSync(candidateFile)), base = PNG.sync.read(fs.readFileSync(baseFile)), mask = PNG.sync.read(fs.readFileSync(maskFile))
  if (hash(candidateFile) !== frame.draft.sha256 || hash(baseFile) !== frame.base.sha256 || hash(maskFile) !== frame.mask.sha256) fail(`${frame.movingLeg} passing hash changed`)
  if (changedOutsideMask(base, candidate, mask) !== 0 || frame.outsideMaskChangedPixels !== 0) fail(`${frame.movingLeg} passing changed outside moving-leg mask`)
  const supportTread = frame.stairClearance.supportTread
  const supportX = rig.geometry.floorSupportCentreLp - supportTread * rig.geometry.treadRunLp
  const supportY = rig.geometry.floorTopLp + supportTread * rig.geometry.riserRiseLp
  const xLp = supportX - frame.supportSole.centreX / 8 + 16
  const bottomLp = supportY - (320 - frame.supportSole.y) / 8
  let minimum = Number.POSITIVE_INFINITY, penetrating = 0
  for (let y = 205; y < 310; y += 1) for (let x = 0; x < 256; x += 1) {
    const i = y * 256 + x
    if (mask.data[i * 4] !== 255 || candidate.data[i * 4 + 3] <= 8) continue
    const worldX = xLp - 16 + x / 8, worldY = bottomLp + (320 - y) / 8
    const clearance = worldY - stairSurface(worldX)
    minimum = Math.min(minimum, clearance)
    if (clearance < -0.05) penetrating += 1
  }
  if (penetrating !== 0 || frame.stairClearance.penetratingPixels !== 0) fail(`${frame.movingLeg} passing boot penetrates stair (${penetrating} pixels)`)
  if (!near(minimum, frame.stairClearance.minimumLp)) fail(`${frame.movingLeg} clearance sidecar mismatch`)
  if (frame.movingLeg === 'right' && minimum < 0.2) fail(`F2 clearance below 0.2 lp (${minimum})`)
  if (frame.movingLeg === 'left' && minimum < 1.5) fail(`F4 clearance below 1.5 lp (${minimum})`)
  const v13 = v13Prep.frames.find((entry: any) => entry.movingLeg === frame.movingLeg)
  if (!v13 || frame.base.sha256 !== v13.draft.sha256) fail(`${frame.movingLeg} passing base is not exact V13`)
}

for (const frame of rig.timeline) {
  if (!assetByUrl[frame.src] || !near(frame.supportClearanceLp, 0)) fail(`frame ${frame.frame} asset or support lock changed`)
  const expectedX = rig.geometry.floorSupportCentreLp - frame.supportTread * rig.geometry.treadRunLp
  const expectedY = rig.geometry.floorTopLp + frame.supportTread * rig.geometry.riserRiseLp
  if (!near(frame.supportXLp, expectedX) || !near(frame.supportYLp, expectedY) || frame.targetTread !== frame.supportTread + 1) fail(`frame ${frame.frame} tread registration changed`)
}
const match = html.match(/const timeline=(\[.*?\]),buttons=/s)
if (!match || JSON.stringify(JSON.parse(match[1])) !== JSON.stringify(rig.timeline)) fail('page and sidecar timelines disagree')
if (!html.includes('Promise.all(unique.map(preload))') || !html.includes('All four unique drawings decoded')) fail('decode-before-play gate changed')
for (const phrase of ['far/right arm should be almost hidden', 'F4', 'does not extend into a tread or riser', 'Exact game scale', 'nothing promoted']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
if (record.frameUrls.length !== 4 || manifest.set !== 'keeper-prime-stair-ascent-v14') fail('archive identity or four-drawing contract changed')
for (const url of record.frameUrls) if (!manifest.entries[url] || !archive.legacyPaths[url]) fail(`archive does not resolve ${url}`)
try { fs.lstatSync(path.join(path.dirname(PAGE), 'assets')); fail('public page contains physical review binaries') } catch (error: any) { if (error.message?.startsWith('Keeper Prime stair ascent V14:')) throw error; if (error.code !== 'ENOENT') throw error }
if (record.validation.passingPenetratingPixels !== 0 || record.validation.outsideMaskChanges !== 0 || record.validation.maximumNearHandOffsetPx > 16 || record.validation.f4MinimumClearanceLp < 1.5) fail('registered validation summary changed')
for (const flag of ['finalChanged', 'runtimeSpritesChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} changed`)
console.log(`Keeper Prime stair ascent V14 verified: synchronized five-frame cadence, restrained ±${record.validation.maximumNearHandOffsetPx.toFixed(2)}px near-arm travel, mostly occluded far arms, F4 ${record.validation.f4MinimumClearanceLp.toFixed(2)}-lp clearance, zero passing-boot penetration, exact out-of-mask pixels and unchanged Final/runtime/production boundaries.`)
