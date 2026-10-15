#!/usr/bin/env node
/** Verify V15's exact-V14, full-flight stair repetition and stop-at-top contract. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const SET = 'keeper-prime-stair-ascent-v15'
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v15')
const V14 = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v14')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v15.json')
const RIG = path.join(PACK, 'stair-contact-rig-v15.json')
const PAGE = path.join(ROOT, 'public/keeper-review', SET, 'index.html')
const MANIFEST = path.join(ROOT, 'review-archive/sets', `${SET}.json`)
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V15: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const near = (a: number, b: number, epsilon = 1e-6) => Math.abs(a - b) <= epsilon

for (const file of [REGISTER, SPEC, RIG, PAGE, MANIFEST, ARCHIVE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}

const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const rig = JSON.parse(fs.readFileSync(RIG, 'utf8')) as Record<string, any>
const v14Record = JSON.parse(fs.readFileSync(path.join(V14, 'batch-register.json'), 'utf8')) as Record<string, any>
const v14Rig = JSON.parse(fs.readFileSync(path.join(V14, 'stair-contact-rig-v14.json'), 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) as Record<string, any>
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
const html = fs.readFileSync(PAGE, 'utf8')

if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v15' || record.status !== 'draft-v15-full-flight-repetition-awaiting-review' || spec.promoted !== false) fail('identity, status or promotion boundary changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered spec or review page changed')

for (const key of ['floorTopLp', 'stairBaseRightLp', 'floorSupportCentreLp', 'flightRunLp', 'flightRiseLp', 'risers', 'treadRunLp', 'riserRiseLp', 'reservedCoreRunLp', 'frameDurationMs']) {
  if (!near(rig.geometry[key], v14Rig.geometry[key])) fail(`V14 geometry changed at ${key}`)
}
if (rig.geometry.risers !== 14 || !near(rig.geometry.treadRunLp, 7) || !near(rig.geometry.flightRunLp, 98) || !near(rig.geometry.flightRiseLp, 60)) fail('binding stair geometry changed')
if (rig.timeline.length !== 27 || rig.uniqueDrawings !== 4) fail('timeline or unique-drawing count changed')

const contacts = rig.timeline.filter((frame: any) => frame.kind === 'contact')
const passing = rig.timeline.filter((frame: any) => frame.kind === 'passing')
if (contacts.length !== 14 || passing.length !== 13) fail('full-flight contact/passing count changed')
if (contacts.map((frame: any) => frame.targetTread).join(',') !== Array.from({ length: 14 }, (_, index) => index + 1).join(',')) fail('contacts do not land on every tread in order')
if (passing.map((frame: any) => frame.targetTread).join(',') !== Array.from({ length: 13 }, (_, index) => index + 2).join(',')) fail('passing frames do not approach treads 2 through 14 in order')
if (contacts.map((frame: any) => frame.movingLeg).join(',') !== Array.from({ length: 14 }, (_, index) => index % 2 === 0 ? 'left' : 'right').join(',')) fail('contact legs do not alternate 50/50')
if (rig.timeline.map((frame: any) => frame.kind).join(',') !== ['contact', ...Array.from({ length: 13 }, () => ['passing', 'contact']).flat()].join(',')) fail('contact/passing phase order changed')

for (let index = 0; index < rig.timeline.length; index += 1) {
  const frame = rig.timeline[index]
  if (frame.frame !== index + 1 || frame.targetTread !== frame.supportTread + 1) fail(`frame ${frame.frame} identity or tread handover changed`)
  const expectedSupportX = rig.geometry.floorSupportCentreLp - frame.supportTread * rig.geometry.treadRunLp
  const expectedSupportY = rig.geometry.floorTopLp + frame.supportTread * rig.geometry.riserRiseLp
  const expectedTargetX = rig.geometry.floorSupportCentreLp - frame.targetTread * rig.geometry.treadRunLp
  const expectedTargetY = rig.geometry.floorTopLp + frame.targetTread * rig.geometry.riserRiseLp
  if (!near(frame.supportXLp, expectedSupportX) || !near(frame.supportYLp, expectedSupportY) || !near(frame.targetXLp, expectedTargetX) || !near(frame.targetYLp, expectedTargetY)) fail(`frame ${frame.frame} is not registered to its mathematical treads`)
  if (!near(frame.supportClearanceLp, 0)) fail(`frame ${frame.frame} support foot is not locked`)
  if (frame.kind === 'contact' && Math.abs(frame.movingClearanceLp) > 0.05) fail(`frame ${frame.frame} moving foot misses contact tolerance`)
  if (frame.kind === 'passing' && (frame.movingLegPenetratingPixels !== 0 || frame.movingLegMinimumClearanceLp < 0.2)) fail(`frame ${frame.frame} passing boot violates stair clearance`)
  if (index > 0) {
    const previous = rig.timeline[index - 1]
    if (frame.supportXLp > previous.supportXLp + 1e-6 || frame.supportYLp < previous.supportYLp - 1e-6) fail(`frame ${frame.frame} root reverses direction`)
  }
}

if (rig.endpoint.frame !== 27 || rig.endpoint.movingLeg !== 'right' || rig.endpoint.supportTread !== 13 || rig.endpoint.targetTread !== 14 || !near(rig.endpoint.targetY, 80) || rig.endpoint.behavior !== 'hold-at-top-no-wrap') fail('top endpoint contract changed')
if (rig.timeline.at(-1).durationMs !== rig.geometry.finalHoldMs || rig.geometry.finalHoldMs !== 900) fail('final top hold changed')

function edgeAlpha(png: PNG) {
  let total = 0
  for (let x = 0; x < png.width; x += 1) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) total += 1
  for (let y = 1; y < png.height - 1; y += 1) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) total += 1
  return total
}
const v14ByHash = new Map(v14Record.assets.map((entry: any) => [entry.sourceSha256, entry]))
if (record.assets.length !== 4 || record.frameUrls.length !== 4) fail('fresh V15 four-source contract changed')
for (const entry of record.assets) {
  const source = path.join(ROOT, entry.source)
  if (!fs.existsSync(source) || hash(source) !== entry.sourceSha256) fail(`V15 source changed: ${entry.source}`)
  if (!v14ByHash.has(entry.sourceSha256)) fail(`V15 asset is not byte-identical V14 artwork: ${entry.url}`)
  const png = PNG.sync.read(fs.readFileSync(source))
  if (png.width !== 256 || png.height !== 320 || edgeAlpha(png) !== 0) fail(`cell or transparent gutter changed: ${entry.source}`)
}

const match = html.match(/const timeline=(\[.*?\]),buttons=/s)
if (!match || JSON.stringify(JSON.parse(match[1])) !== JSON.stringify(rig.timeline)) fail('page and rig timelines disagree')
for (const phrase of ['Promise.all(unique.map(preload))', 'All four unique drawings decoded', 'It does not loop back to the bottom', 'TOP REACHED', 'Exact game scale', 'nothing promoted']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
if (!html.includes("if(index>=timeline.length-1)return stop()") || /index\s*=\s*\(index\s*\+\s*1\)\s*%/.test(html)) fail('playback does not deterministically stop at the top')
if (manifest.set !== SET || Object.keys(manifest.entries).length !== 4) fail('archive set identity or unique path count changed')
for (const url of record.frameUrls) {
  const entry = manifest.entries[url]
  if (!entry || !archive.legacyPaths[url] || entry.sha256 !== archive.legacyPaths[url].sha256) fail(`archive does not resolve ${url}`)
}
try {
  fs.lstatSync(path.join(path.dirname(PAGE), 'assets'))
  fail('public page contains physical review binaries')
} catch (error: any) {
  if (error.message?.startsWith('Keeper Prime stair ascent V15:')) throw error
  if (error.code !== 'ENOENT') throw error
}
if (record.validation.timelineFrames !== 27 || record.validation.contactFrames !== 14 || record.validation.passingFrames !== 13 || record.validation.finalTargetTread !== 14 || !near(record.validation.finalTargetYLp, 80) || record.validation.wrapToBottom !== false || record.validation.v14ArtworkByteIdentical !== true) fail('registered full-flight summary changed')
for (const flag of ['finalChanged', 'runtimeSpritesChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} changed`)

console.log('Keeper Prime stair ascent V15 verified: 27 ordered frames, 14 alternating contacts, 13 clear passing poses, exact V14 pixels and geometry, mathematical tread locks through tread 14, and a deterministic stop-and-hold at the top.')
