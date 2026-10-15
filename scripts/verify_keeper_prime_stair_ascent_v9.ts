#!/usr/bin/env node
/** Verify V9's exact Keeper-only back shift and forward-toe clearance. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v9')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v9.json')
const RIG = path.join(PACK, 'stair-contact-rig-v9.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v9/index.html')
const V8_PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v8/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const MANIFEST = path.join(ROOT, 'review-archive/sets/keeper-prime-stair-ascent-v9.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V9: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const near = (a: number, b: number, epsilon = 1e-6) => Math.abs(a - b) <= epsilon
for (const file of [REGISTER, SPEC, RIG, PAGE, V8_PAGE, ARCHIVE, MANIFEST, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const rig = JSON.parse(fs.readFileSync(RIG, 'utf8')) as Record<string, any>
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) as Record<string, any>
const html = fs.readFileSync(PAGE, 'utf8'), v8Html = fs.readFileSync(V8_PAGE, 'utf8')
if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v9' || record.status !== 'draft-v9-forward-toe-clearance-awaiting-review') fail('identity/status changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256 || spec.promoted !== false) fail('registered candidate or boundary changed')
if (rig.geometry.keeperBackShiftFromV8Lp !== 1.5 || rig.geometry.keeperBackShiftSourcePx !== 12 || rig.geometry.minimumOpaqueToeClearanceLp !== 0.25) fail('clearance geometry changed')
const extract = (source: string) => {
  const match = source.match(/const timeline=(\[.*?\]),buttons=/s)
  if (!match) fail('timeline missing')
  return JSON.parse(match[1]) as Record<string, any>[]
}
const v8 = extract(v8Html), v9 = extract(html)
if (v8.length !== 4 || v9.length !== 4) fail('four-contact proof changed')
const prep = JSON.parse(fs.readFileSync(path.join(ROOT, record.authorities.v7SourcePreparation.file), 'utf8')) as Record<string, any>
const prepByLeg = Object.fromEntries(prep.frames.map((frame: any) => [frame.leg, frame])) as Record<string, any>
for (let index = 0; index < 4; index += 1) {
  const before = v8[index], after = v9[index]
  if (!near(after.xLp, before.xLp + 1.5)) fail(`Keeper root is not +1.5 lp at F${index + 1}`)
  for (const key of ['bottomLp', 'supportXLp', 'supportYLp', 'targetXLp', 'targetYLp', 'durationMs', 'step', 'leg', 'supportTread', 'targetTread', 'phase', 'label']) if (after[key] !== before[key]) fail(`${key} changed at F${index + 1}`)
  if (after.src.replace('stair-ascent-v9', 'stair-ascent-v8') !== before.src) fail(`asset alias mismatch at F${index + 1}`)
  const source = prepByLeg[after.leg]
  const png = PNG.sync.read(fs.readFileSync(path.join(ROOT, source.file)))
  let foremost = png.width
  for (let y = 248; y <= 316; y += 1) for (let x = 0; x < 132; x += 1) if (png.data[(y * png.width + x) * 4 + 3] > 0) foremost = Math.min(foremost, x)
  const toeXLp = after.xLp - 16 + foremost / 8
  const nextRiserXLp = after.targetXLp - 3
  const clearance = toeXLp - nextRiserXLp
  if (clearance < 0.25 - 1e-6) fail(`forward toe clearance ${clearance} lp is too small at F${index + 1}`)
}
if (record.originalAndDraft.length !== 2 || record.originalAndDraft.some((entry: any) => entry.sourceSha256 !== entry.candidateSha256)) fail('artwork bytes changed')
if (manifest.set !== 'keeper-prime-stair-ascent-v9' || Object.keys(manifest.entries).length !== 2) fail('archive manifest changed')
for (const url of record.frameUrls) if (!archive.legacyPaths[url] || !manifest.entries[url]) fail(`archive does not resolve ${url}`)
for (const phrase of ['moves the Keeper back 1.5 lp', 'forward toe now has a measured transparent gap', 'two-contact leg test', 'Exact game scale']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
try { fs.lstatSync(path.join(path.dirname(PAGE), 'assets')); fail('public page contains physical binary assets') } catch (error: any) {
  if (error.message?.startsWith('Keeper Prime stair ascent V9:')) throw error
  if (error.code !== 'ENOENT') throw error
}
for (const flag of ['v8ArtworkChanged', 'v8VerticalPositionsChanged', 'v8ContactMarkersChanged', 'v8TimingChanged', 'stairGeometryChanged', 'v1ThroughV8Changed', 'finalChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} changed`)
console.log('Keeper Prime stair ascent V9 verified: Keeper root shifted back 1.5 lp only; every forward toe clears the next riser by at least 0.25 lp; V8 artwork, vertical contacts, markers, timing and stairs unchanged.')
