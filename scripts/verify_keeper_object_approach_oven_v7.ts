#!/usr/bin/env node
/** Verify Oven Approach V7 restrained visible-floor placement. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-object-approach-oven-2026-10-14-v7')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC_FILE = path.join(PACK, 'oven-restrained-floor-placement-v1.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-object-approach-oven-v7/index.html')
const V6_PAGE = path.join(ROOT, 'public/keeper-review/keeper-object-approach-oven-v6/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper oven approach V7: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, SPEC_FILE, path.join(PACK, 'HANDOFF.md'), PAGE, V6_PAGE, ARCHIVE]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC_FILE, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-object-approach-oven-2026-10-14-v7' || record.status !== 'draft-placement-and-perspective-awaiting-review') fail('identity/status changed')
if (hash(SPEC_FILE) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered candidate changed')
for (const authority of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, authority.file)
  if (!fs.existsSync(file) || hash(file) !== authority.sha256) fail(`authority changed: ${authority.file}`)
}
const room = spec.room
const oven = spec.oven
if (room.heightLp !== 56 || room.frontFloorLipLp !== 2 || room.visibleFloorSurfaceDepthOnElevationLp !== 5 || room.rearWallFloorJunctionLpAboveStageBottom !== 7 || room.wallHeightPercent !== 87.5) fail('restrained floor geometry changed')
if (room.frontFloorLipLp + room.visibleFloorSurfaceDepthOnElevationLp !== room.rearWallFloorJunctionLpAboveStageBottom) fail('floor arithmetic is inconsistent')
if (oven.ovenBaseLpAboveStageBottom !== room.rearWallFloorJunctionLpAboveStageBottom) fail('oven does not sit at rear floor junction')
if (JSON.stringify(oven.footprintLp) !== '[30,30]' || oven.interactionCentreLp !== 120) fail('oven footprint/anchor changed')
for (const flag of ['ovenBaseEqualsRearFloorJunction', 'visibleFloorSurfaceIsExact', 'v6KeeperFramesRoutesAndPerspectivePreserved']) if (record.validation[flag] !== true) fail(`${flag} changed`)
for (const flag of ['approvedKeeperPixelsChanged', 'runtimeChanged', 'approvalChanged']) if (record.validation[flag] !== false) fail(`${flag} boundary changed`)
const html = fs.readFileSync(PAGE, 'utf8')
for (const phrase of ['Oven approach V7 · restrained floor plane + perspective calibration', 'restrained 5-lp floor surface', '7 lp above the stage bottom', '5 lp of visible floor', '87.5%', 'oven.style.bottom=`${7*scale}px`', 'floorSurface.style.height=`${5*scale}px`', 'Perspective calibration · proposed 42-lp room depth', 'Promise.all(unique.map(preload))']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
if ((html.match(/rear wall \/ oven base/g) ?? []).length !== 2) fail('both panes must identify the rear-wall datum')
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
const urlsOf = (text: string) => [...new Set([...text.matchAll(/\/keeper-review\/keeper-prime-walk-stop-turn-back-v2\/assets\/[A-Za-z0-9._-]+\.png/g)].map((m) => m[0]))]
const urls = urlsOf(html)
const v6Urls = urlsOf(fs.readFileSync(V6_PAGE, 'utf8'))
if (urls.length !== 20 || JSON.stringify(urls) !== JSON.stringify(v6Urls)) fail('Keeper frame URLs differ from V6')
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
for (const url of urls) if (!archive.legacyPaths[url]) fail(`archive does not resolve ${url}`)
console.log('Keeper oven approach V7 verified: 5-lp visible floor, 2-lp lip, 7-lp oven base, unchanged Keeper frames/routes/perspective.')
