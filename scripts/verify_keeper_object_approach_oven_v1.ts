#!/usr/bin/env node
/** Verify the reversible oven-context walk/stop/turn-away review. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-object-approach-oven-2026-10-14-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-object-approach-oven-v1/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper oven approach V1: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, path.join(PACK, 'HANDOFF.md'), PAGE, ARCHIVE]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-object-approach-oven-2026-10-14-v1' || record.status !== 'draft-asset-context-root-motion-awaiting-review') fail('identity/status changed')
for (const authority of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, authority.file)
  if (!fs.existsSync(file) || hash(file) !== authority.sha256) fail(`authority changed: ${authority.file}`)
}
if (hash(PAGE) !== record.reviewPage.sha256) fail('review page changed')
if (record.asset.kind !== 'opaque-placeholder' || JSON.stringify(record.asset.footprintLp) !== '[30,30]' || record.asset.centreLp !== 120 || record.asset.artAuthority !== false) fail('oven placeholder contract changed')
const route = record.route
if (route.startRootKu !== 708 || route.targetRootKu !== 960 || route.candidateDistanceKu !== 252 || route.currentDistanceKu !== 244 || route.currentMissKu !== 8 || route.frameCount !== 25) fail('route geometry changed')
if (route.candidateDeltasKu.reduce((a: number, b: number) => a + b, 0) !== 252 || route.approvedDeltasKu.reduce((a: number, b: number) => a + b, 0) !== 244) fail('root totals do not agree')
for (const flag of ['candidateClosesThreeLatticeIntervals', 'candidateEndsAtAssetAnchor', 'currentStopsOneLogicalPixelShort', 'turnRootMotionZero']) if (record.validation[flag] !== true) fail(`${flag} changed`)
for (const flag of ['canonicalArtworkChanged', 'productionSpritesChanged', 'runtimeManifestChanged', 'approvalChanged']) if (record.validation[flag] !== false) fail(`${flag} boundary changed`)

const html = fs.readFileSync(PAGE, 'utf8')
for (const phrase of ['Oven approach V1', 'walk → stop → turn fully away', 'OVEN PLACEHOLDER', 'Full 172 × 56 lp room · exact 4× authoring ruler', 'Large 8× inspection', 'Grid-perfect candidate · lands exactly', 'Current approved distance · 1 lp short', 'Loop for inspection (restarts from origin)', 'Loading and decoding every unique approved frame', 'Promise.all(unique.map(preload))', 'image.decode', 'Previous frame', 'Next frame']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
if (html.includes('id="loop" type="checkbox" checked')) fail('route must not loop by default because the reset is not a transition')
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
const urls = [...new Set([...html.matchAll(/\/keeper-review\/keeper-prime-walk-stop-turn-back-v2\/assets\/[A-Za-z0-9._-]+\.png/g)].map((m) => m[0]))]
if (urls.length !== 20) fail(`expected 20 unique approved asset URLs, found ${urls.length}`)
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
for (const url of urls) if (!archive.legacyPaths[url]) fail(`archive does not resolve ${url}`)
console.log('Keeper oven approach V1 verified: exact approved frame URLs, 252-ku candidate closure, 1-lp current miss, opaque placeholder and no promotion.')
