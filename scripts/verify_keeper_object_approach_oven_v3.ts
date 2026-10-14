#!/usr/bin/env node
/** Verify Oven Approach V3 floor datum and perspective proposal. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-object-approach-oven-2026-10-14-v3')
const REGISTER = path.join(PACK, 'batch-register.json')
const SPEC_FILE = path.join(PACK, 'room-perspective-v1.json')
const PAGE = path.join(ROOT, 'public/keeper-review/keeper-object-approach-oven-v3/index.html')
const ARCHIVE = path.join(ROOT, 'review-archive/index.json')
const fail = (message: string): never => { throw new Error(`Keeper oven approach V3: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, SPEC_FILE, path.join(PACK, 'HANDOFF.md'), PAGE, ARCHIVE]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const spec = JSON.parse(fs.readFileSync(SPEC_FILE, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-object-approach-oven-2026-10-14-v3' || record.status !== 'draft-perspective-and-placement-awaiting-review') fail('identity/status changed')
if (hash(SPEC_FILE) !== record.spec.sha256 || hash(PAGE) !== record.reviewPage.sha256) fail('registered candidate changed')
for (const authority of Object.values(record.authorities) as Record<string, any>[]) {
  const file = path.join(ROOT, authority.file)
  if (!fs.existsSync(file) || hash(file) !== authority.sha256) fail(`V1 authority changed: ${authority.file}`)
}
if (spec.oven.baseRaiseLp !== 0.5 || JSON.stringify(spec.oven.footprintLp) !== '[30,30]' || spec.oven.interactionCentreLp !== 120) fail('oven correction changed')
const p = spec.perspective
if (p.roomDepthLp !== 42 || p.roomDepthIntervals !== 4 || p.standardAssetDepthLp !== 10.5 || p.assetFrontInteractionPlaneZLp !== 31.5 || p.assetBackPlaneZLp !== 42 || p.projectionDistanceLp !== 1008 || p.horizonYLp !== 20) fail('perspective geometry changed')
const scale = (z: number) => p.projectionDistanceLp / (p.projectionDistanceLp + z)
if (Math.abs(scale(42) - 0.96) > 1e-12 || Math.abs(scale(31.5) - 32 / 33) > 1e-12 || Math.abs(scale(42) / scale(31.5) - 0.99) > 1e-12) fail('perspective scales do not close')
const rearY = p.horizonYLp + (56 - p.horizonYLp) * scale(42)
const interactionY = p.horizonYLp + (56 - p.horizonYLp) * scale(31.5)
if (Math.abs((interactionY - rearY) / scale(31.5) - p.assetBackEdgeRiseLp) > 1e-12) fail('asset rear-edge rise changed')
if (spec.grid.worldPitchLp !== 10.5 || spec.grid.worldPitchKu !== 84 || spec.grid.storedInWorldSpace !== true || spec.grid.keeperScaleAtInteractionPlane !== 1 || spec.grid.runtimeRasterScalingRequired !== false || spec.grid.collisionFootprintsChange !== false) fail('grid boundary changed')
for (const flag of ['ovenRaisedByExactBootGutter', 'v1KeeperFrameUrlsReused', 'worldGridUnchanged', 'keeperInteractionScaleUnchanged']) if (record.validation[flag] !== true) fail(`${flag} changed`)
for (const flag of ['approvedKeeperPixelsChanged', 'runtimeChanged', 'approvalChanged']) if (record.validation[flag] !== false) fail(`${flag} boundary changed`)
const html = fs.readFileSync(PAGE, 'utf8')
for (const phrase of ['Oven approach V3 · corrected floor datum + perspective calibration', 'shared boot / oven base', 'oven.style.bottom=`${.5*scale}px`', 'Perspective calibration · proposed 42-lp room depth', 'Proposed · rear wall 4%; asset 1%', '42 lp', '10.5 lp', 'world space', 'does <strong>not</strong> rescale animation sprites at runtime', 'Loading and decoding every unique approved frame', 'Promise.all(unique.map(preload))']) if (!html.includes(phrase)) fail(`page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review script missing')
new Function(script)
const urls = [...new Set([...html.matchAll(/\/keeper-review\/keeper-prime-walk-stop-turn-back-v2\/assets\/[A-Za-z0-9._-]+\.png/g)].map((m) => m[0]))]
if (urls.length !== 20) fail(`expected 20 exact V1 Keeper URLs, found ${urls.length}`)
const v1 = fs.readFileSync(path.join(ROOT, 'public/keeper-review/keeper-object-approach-oven-v1/index.html'), 'utf8')
const v1Urls = [...new Set([...v1.matchAll(/\/keeper-review\/keeper-prime-walk-stop-turn-back-v2\/assets\/[A-Za-z0-9._-]+\.png/g)].map((m) => m[0]))]
if (JSON.stringify(urls) !== JSON.stringify(v1Urls)) fail('Keeper frame URL sequence differs from V1')
const archive = JSON.parse(fs.readFileSync(ARCHIVE, 'utf8')) as Record<string, any>
for (const url of urls) if (!archive.legacyPaths[url]) fail(`archive does not resolve ${url}`)
console.log('Keeper oven approach V3 verified: exact V1 Keeper frames, +0.5-lp oven base, 42-lp room depth, 1% standard-asset convergence and unchanged world grid.')
