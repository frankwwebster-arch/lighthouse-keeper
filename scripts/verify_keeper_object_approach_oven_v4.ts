#!/usr/bin/env node
/** Verify Oven Approach V4 floor-surface placement. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-object-approach-oven-2026-10-14-v4')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC_FILE = path.join(PACK, 'oven-floor-surface-placement-v1.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-object-approach-oven-v4/index.html')
const V3_PAGE = path.join(ROOT, 'public/keeper-review/keeper-object-approach-oven-v3/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper oven approach V4: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, SPEC_FILE, path.join(PACK, 'HANDOFF.md'), PAGE, V3_PAGE, ARCHIVE]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC_FILE, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-object-approach-oven-2026-10-14-v4' || record.status !== 'draft-placement-and-perspective-awaiting-review') fail('identity/status changed')
if (hash(SPEC_FILE) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered candidate changed')
for (const authority of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, authority.file)
  if (!fs.existsSync(file) || hash(file) !== authority.sha256) fail(`V3 authority changed: ${authority.file}`)
}
const oven = spec.oven
if (oven.floorBandThicknessLp !== 2 || oven.floorTopSurfaceLpAboveStageBottom !== 2 || oven.ovenBaseLpAboveStageBottom !== 2) fail('oven does not sit on floor top')
if (oven.v3BaseLpAboveStageBottom !== 0.5 || oven.additionalRaiseFromV3Lp !== 1.5 || oven.ovenBaseLpAboveStageBottom - oven.v3BaseLpAboveStageBottom !== oven.additionalRaiseFromV3Lp) fail('V3-to-V4 raise changed')
if (JSON.stringify(oven.footprintLp) !== '[30,30]' || oven.interactionCentreLp !== 120) fail('oven footprint/anchor changed')
for (const flag of ['ovenBaseEqualsFloorTop', 'additionalRaiseFromV3IsExact', 'v3KeeperFrameUrlsReused', 'v3PerspectiveCalibrationPreserved']) if (record.validation[flag] !== true) fail(`${flag} changed`)
for (const flag of ['approvedKeeperPixelsChanged', 'runtimeChanged', 'approvalChanged']) if (record.validation[flag] !== false) fail(`${flag} boundary changed`)
const html = fs.readFileSync(PAGE, 'utf8')
for (const phrase of ['Oven approach V4 · oven on the floor surface + perspective calibration', 'floor top / oven base', 'oven.style.bottom=`${2*scale}px`', 'top of the 2-lp structural floor band', '1.5 lp higher than V3', 'Perspective calibration · proposed 42-lp room depth', 'Proposed · rear wall 4%; asset 1%', 'Promise.all(unique.map(preload))']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
const urlsOf = (text: string) => [...new Set([...text.matchAll(/\/keeper-review\/keeper-prime-walk-stop-turn-back-v2\/assets\/[A-Za-z0-9._-]+\.png/g)].map((m) => m[0]))]
const urls = urlsOf(html)
const v3Urls = urlsOf(fs.readFileSync(V3_PAGE, 'utf8'))
if (urls.length !== 20 || JSON.stringify(urls) !== JSON.stringify(v3Urls)) fail('Keeper frame URLs differ from V3')
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
for (const url of urls) if (!archive.legacyPaths[url]) fail(`archive does not resolve ${url}`)
console.log('Keeper oven approach V4 verified: oven base equals 2-lp floor top, exact +1.5-lp raise from V3, and Keeper frames/perspective remain unchanged.')
