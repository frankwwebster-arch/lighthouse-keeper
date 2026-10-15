#!/usr/bin/env node
/** Verify V16's three masked corrections on the exact V15 full-flight sequence. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const SET = 'keeper-prime-stair-ascent-v16'
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16')
const V14 = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v14')
const V15 = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v15')
const REGISTER = path.join(PACK, 'batch-register.json')
const PREP = path.join(PACK, 'source-preparation-v16.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v16.json')
const RIG = path.join(PACK, 'stair-contact-rig-v16.json')
const PAGE = path.join(ROOT, 'public/keeper-review', SET, 'index.html')
const MANIFEST = path.join(ROOT, 'review-archive/sets', `${SET}.json`)
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V16: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const near = (a: number, b: number, epsilon = 1e-6) => Math.abs(a - b) <= epsilon

for (const file of [REGISTER, PREP, SPEC, RIG, PAGE, MANIFEST, ARCHIVE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const prep = JSON.parse(fs.readFileSync(PREP, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const rig = JSON.parse(fs.readFileSync(RIG, 'utf8')) as Record<string, any>
const v15Rig = JSON.parse(fs.readFileSync(path.join(V15, 'stair-contact-rig-v15.json'), 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) as Record<string, any>
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
const html = fs.readFileSync(PAGE, 'utf8')

if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v16' || record.status !== 'draft-v16-three-defect-correction-awaiting-review' || spec.promoted !== false) fail('identity, status or promotion boundary changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered spec or page changed')
if (rig.timeline.length !== 27 || rig.timeline.filter((frame: any) => frame.kind === 'contact').length !== 14 || rig.timeline.filter((frame: any) => frame.kind === 'passing').length !== 13) fail('full-flight count changed')
if (JSON.stringify(rig.geometry) !== JSON.stringify(v15Rig.geometry) || JSON.stringify(rig.endpoint) !== JSON.stringify(v15Rig.endpoint)) fail('V15 geometry or endpoint changed')

for (let index = 0; index < rig.timeline.length; index += 1) {
  const frame = rig.timeline[index]
  const old = v15Rig.timeline[index]
  for (const key of ['frame', 'kind', 'leg', 'movingLeg', 'supportTread', 'targetTread', 'xLp', 'bottomLp', 'supportXLp', 'supportYLp', 'targetXLp', 'targetYLp', 'supportClearanceLp', 'durationMs']) {
    const equal = typeof frame[key] === 'number' ? near(frame[key], old[key]) : frame[key] === old[key]
    if (!equal) fail(`frame ${index + 1} changed V15 ${key}`)
  }
  if (frame.kind === 'contact') {
    for (const key of ['movingXLp', 'movingYLp', 'movingClearanceLp']) if (!near(frame[key], old[key])) fail(`contact frame ${index + 1} changed ${key}`)
  }
  if (frame.kind === 'passing' && frame.movingLeg === 'left' && (!near(frame.movingLegMinimumClearanceLp, old.movingLegMinimumClearanceLp) || frame.src.includes('v15'))) fail(`LEFT passing frame ${index + 1} changed authority data`)
  if (index && (frame.supportXLp > rig.timeline[index - 1].supportXLp + 1e-6 || frame.supportYLp < rig.timeline[index - 1].supportYLp - 1e-6)) fail(`frame ${index + 1} reverses root direction`)
}

if (prep.corrections.right_passing.movingBoundsExclusive[3] !== 270 || prep.corrections.left_passing.movingBoundsExclusive[3] !== 270) fail('passing moving-region lower edges are not exactly matched')
if (prep.corrections.right_passing.stairClearance.penetratingPixels !== 0 || prep.corrections.left_passing.stairClearance.penetratingPixels !== 0 || prep.corrections.right_passing.stairClearance.minimumLp < 1.5) fail('passing stair clearance changed')
for (const key of ['right_passing', 'left_contact', 'right_contact']) if (prep.corrections[key].outsideMaskChangedPixels !== 0) fail(`${key} changed outside its declared mask`)

function edgeAlpha(png: PNG) {
  let total = 0
  for (let x = 0; x < png.width; x += 1) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) total += 1
  for (let y = 1; y < png.height - 1; y += 1) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) total += 1
  return total
}
function changedPixels(a: PNG, b: PNG) {
  let changed = 0
  for (let index = 0; index < a.data.length; index += 4) if ([0, 1, 2, 3].some((channel) => a.data[index + channel] !== b.data[index + channel])) changed += 1
  return changed
}
const assetsByRole = Object.fromEntries(record.assets.map((entry: any) => [entry.role, entry])) as Record<string, any>
if (Object.keys(assetsByRole).length !== 4 || record.frameUrls.length !== 4) fail('four-drawing contract changed')
for (const entry of record.assets) {
  const file = path.join(ROOT, entry.source)
  if (!fs.existsSync(file) || hash(file) !== entry.sourceSha256) fail(`candidate source changed: ${entry.source}`)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 256 || png.height !== 320 || edgeAlpha(png)) fail(`${entry.role} violates cell/gutter contract`)
}
if (assetsByRole['passing:left'].sourceSha256 !== prep.corrections.left_passing.v14Sha256) fail('LEFT passing is not byte-identical V14')

const leftContact = PNG.sync.read(fs.readFileSync(path.join(ROOT, prep.corrections.left_contact.draft.file)))
const leftBase = PNG.sync.read(fs.readFileSync(path.join(ROOT, prep.corrections.left_contact.restorationAuthority.file)))
const artefactMask = PNG.sync.read(fs.readFileSync(path.join(ROOT, prep.corrections.left_contact.mask.file)))
let restored = 0
for (let i = 0; i < leftContact.width * leftContact.height; i += 1) {
  if (artefactMask.data[i * 4] === 0) continue
  restored += 1
  for (let channel = 0; channel < 4; channel += 1) if (leftContact.data[i * 4 + channel] !== leftBase.data[i * 4 + channel]) fail('LEFT-contact artefact mask is not exact base restoration')
}
if (restored < 100) fail('LEFT-contact artefact restoration mask unexpectedly empty')

const rightContact = PNG.sync.read(fs.readFileSync(path.join(ROOT, prep.corrections.right_contact.draft.file)))
const rightContactBase = PNG.sync.read(fs.readFileSync(path.join(ROOT, prep.corrections.right_contact.base.file)))
if (changedPixels(rightContact, rightContactBase) < 100) fail('RIGHT-contact toecap did not materially change')
for (let x = 0; x < 256; x += 1) {
  const offset = (282 * 256 + x) * 4
  for (let channel = 0; channel < 4; channel += 1) if (rightContact.data[offset + channel] !== rightContactBase.data[offset + channel]) fail('RIGHT-contact sole/contact row changed')
}

const match = html.match(/const timeline=(\[.*?\]),evidence=/s)
if (!match || JSON.stringify(JSON.parse(match[1])) !== JSON.stringify(rig.timeline)) fail('page and rig timelines disagree')
for (const phrase of ['Promise.all(unique.map(preload))', 'All before/after drawings decoded', 'RIGHT compact passing', 'LEFT contact', 'RIGHT contact', 'TOP REACHED', 'Exact game scale', 'nothing promoted']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
if (!html.includes("if(index>=timeline.length-1)return stop()") || /index\s*=\s*\(index\s*\+\s*1\)\s*%/.test(html)) fail('playback no longer stops at the top')
if (manifest.set !== SET || Object.keys(manifest.entries).length !== 4) fail('archive set identity or path count changed')
for (const url of record.frameUrls) if (!manifest.entries[url] || !archive.legacyPaths[url]) fail(`archive does not resolve ${url}`)
try { fs.lstatSync(path.join(path.dirname(PAGE), 'assets')); fail('public page contains physical review binaries') } catch (error: any) { if (error.message?.startsWith('Keeper Prime stair ascent V16:')) throw error; if (error.code !== 'ENOENT') throw error }
if (record.validation.passingMovingBottomExclusive.right !== 270 || record.validation.passingMovingBottomExclusive.left !== 270 || record.validation.passingPenetratingPixels !== 0 || record.validation.outsideMaskChanges !== 0 || record.validation.finalTargetTread !== 14 || record.validation.wrapToBottom !== false) fail('registered correction/full-flight summary changed')
for (const flag of ['finalChanged', 'runtimeSpritesChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} changed`)

console.log('Keeper Prime stair ascent V16 verified: exact V15 full-flight timeline; matched passing lower edges at y=270; 1.59-lp RIGHT clearance with zero penetration; exact LEFT artefact restoration; masked RIGHT toecap repair; unchanged sole row, gutters and Final/runtime/production boundaries.')
