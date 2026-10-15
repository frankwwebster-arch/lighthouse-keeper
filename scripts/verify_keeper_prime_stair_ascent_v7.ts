#!/usr/bin/env node
/** Verify the deliberately minimal RIGHT/LEFT/RIGHT/LEFT Stair Ascent V7 proof. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v7')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC = path.join(PACK, 'keeper-prime-stair-ascent-v7.json')
const PREP = path.join(PACK, 'source-preparation-v7.json')
const RIG = path.join(PACK, 'stair-contact-rig-v7.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v7/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const MANIFEST = path.join(ROOT, 'review-archive/sets/keeper-prime-stair-ascent-v7.json')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V7: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const near = (a: number, b: number, epsilon = 1e-6) => Math.abs(a - b) <= epsilon
for (const file of [REGISTER, SPEC, PREP, RIG, PAGE, ARCHIVE, MANIFEST, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC, 'utf8')) as Record<string, any>
const prep = JSON.parse(fs.readFileSync(PREP, 'utf8')) as Record<string, any>
const rig = JSON.parse(fs.readFileSync(RIG, 'utf8')) as Record<string, any>
const html = fs.readFileSync(PAGE, 'utf8')
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v7' || record.status !== 'draft-v7-two-contact-leg-test-awaiting-review') fail('identity/status changed')
for (const entry of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, entry.file)
  if (!fs.existsSync(file) || hash(file) !== entry.sha256) fail(`authority changed: ${entry.file}`)
}
if (hash(SPEC) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered candidate changed')
if (spec.scope !== 'Four-contact RIGHT/LEFT/RIGHT/LEFT diagnostic only; not a complete transition.' || spec.promoted !== false) fail('scope/promotion boundary changed')
if (rig.geometry.shownContacts !== 4 || !near(rig.geometry.treadRunLp, 6) || !near(rig.geometry.riserRiseLp, 60 / 14)) fail('proof geometry changed')
const expectedOrder = ['right', 'left', 'right', 'left']
if (JSON.stringify(rig.contactOrder) !== JSON.stringify(expectedOrder) || rig.contract.some((line: string) => /swing|high-pass|transfer frames/.test(line) && !/no intervening|not a complete/.test(line))) fail('two-contact contract changed')

const timelineMatch = html.match(/const timeline=(\[.*?\]),buttons=/s)
if (!timelineMatch) fail('timeline missing')
const timeline = JSON.parse(timelineMatch[1]) as Record<string, any>[]
if (timeline.length !== 4 || new Set(timeline.map(frame => frame.src)).size !== 2) fail('must contain four shown contacts using two unique drawings')
const prepByLeg = Object.fromEntries(prep.frames.map((frame: any) => [frame.leg, frame])) as Record<string, any>
for (let index = 0; index < timeline.length; index += 1) {
  const frame = timeline[index], leg = expectedOrder[index], source = prepByLeg[leg]
  if (frame.step !== index + 1 || frame.leg !== leg || frame.label !== `${leg.toUpperCase()} leg forward and up`) fail(`contact order mismatch at F${index + 1}`)
  if (frame.supportTread !== index || frame.targetTread !== index + 1 || frame.durationMs !== 320) fail(`contact metadata mismatch at F${index + 1}`)
  const expectedSupportX = rig.geometry.baseX - (index + 0.5) * 6
  const expectedTargetX = expectedSupportX - 6
  const expectedSupportY = 20 + index * (60 / 14)
  const expectedTargetY = 20 + (index + 1) * (60 / 14)
  if (!near(frame.supportXLp, expectedSupportX) || !near(frame.targetXLp, expectedTargetX) || !near(frame.supportYLp, expectedSupportY) || !near(frame.targetYLp, expectedTargetY)) fail(`tread registration mismatch at F${index + 1}`)
  const cellLeft = frame.xLp - 16
  const renderedSupportX = cellLeft + source.supportSole.centreX / 8
  const renderedMovingX = cellLeft + source.movingSole.centreX / 8
  const renderedSupportY = frame.bottomLp + (320 - source.supportSole.y) / 8
  const renderedMovingY = frame.bottomLp + (320 - source.movingSole.y) / 8
  if (!near(renderedSupportX, expectedSupportX) || Math.abs(renderedMovingX - expectedTargetX) > 0.07) fail(`horizontal sole/tread mismatch at F${index + 1}`)
  if (!near(renderedSupportY, expectedSupportY) || Math.abs(renderedMovingY - expectedTargetY) > 0.04) fail(`vertical sole/tread mismatch at F${index + 1}`)
}

if (prep.frames.length !== 2 || prep.correction.unchangedUpperBodyThroughY !== 219) fail('prepared two-drawing contract changed')
for (const frame of prep.frames) {
  const file = path.join(ROOT, frame.file), sourceFile = path.join(ROOT, frame.source.file)
  if (!fs.existsSync(file) || hash(file) !== frame.sha256 || !fs.existsSync(sourceFile) || hash(sourceFile) !== frame.source.sha256) fail(`${frame.leg} source or result changed`)
  const png = PNG.sync.read(fs.readFileSync(file)), source = PNG.sync.read(fs.readFileSync(sourceFile))
  if (png.width !== 256 || png.height !== 320 || frame.edgeAlpha !== 0 || frame.supportSole.y !== 316 || frame.movingSole.y !== 282) fail(`${frame.leg} cell/contact geometry changed`)
  if (Math.abs(frame.localSeparation.xLp - 6) > 0.07 || !near(frame.localSeparation.yLp, 4.25)) fail(`${frame.leg} is not one adjacent tread apart`)
  for (let y = 0; y <= 219; y += 1) for (let x = 0; x < png.width; x += 1) {
    const offset = (y * png.width + x) * 4
    for (let channel = 0; channel < 4; channel += 1) if (png.data[offset + channel] !== source.data[offset + channel]) fail(`${frame.leg} upper body changed at ${x},${y}`)
  }
  let edgeAlpha = 0
  for (let x = 0; x < png.width; x += 1) for (const y of [0, png.height - 1]) if (png.data[(y * png.width + x) * 4 + 3]) edgeAlpha += 1
  for (let y = 1; y < png.height - 1; y += 1) for (const x of [0, png.width - 1]) if (png.data[(y * png.width + x) * 4 + 3]) edgeAlpha += 1
  if (edgeAlpha) fail(`${frame.leg} touches a cell edge`)
}

if (manifest.set !== 'keeper-prime-stair-ascent-v7' || Object.keys(manifest.entries).length !== 2) fail('archive manifest changed')
for (const url of record.frameUrls) if (!archive.legacyPaths[url] || !manifest.entries[url]) fail(`archive does not resolve ${url}`)
for (const phrase of ['two-contact leg test', 'RIGHT leg forward/up → LEFT leg forward/up → repeat', 'There are no swing, high-pass or transfer frames', 'The only two drawings used', 'Exact game scale']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
try { fs.lstatSync(path.join(path.dirname(PAGE), 'assets')); fail('public page contains physical binary assets') } catch (error: any) {
  if (error.message?.startsWith('Keeper Prime stair ascent V7:')) throw error
  if (error.code !== 'ENOENT') throw error
}
for (const flag of ['v1ThroughV6Changed', 'finalChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} changed`)
console.log('Keeper Prime stair ascent V7 verified: exactly two unique planted contacts, RIGHT/LEFT/RIGHT/LEFT only, one adjacent tread per contact, safe cells, stable upper body and no production change.')
