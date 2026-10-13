#!/usr/bin/env node
/** Verify the Walk V2 routing wrapper and its byte-identical Walk V1 art. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const ROOT = path.resolve(import.meta.dirname, '..')
const V1_PACK = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-13-v1')
const V1_PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-walk-v1')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-13-v2')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-walk-v2')
const PREFIX = '/keeper-review/keeper-prime-walk-v2/assets/'
const fail = (message: string): never => { throw new Error(`Keeper Prime Walk V2: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

const registerPath = path.join(PACK, 'batch-register.json')
for (const file of [registerPath, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const register = JSON.parse(fs.readFileSync(registerPath, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-walk-2026-10-13-v2' || register.status !== 'technical-review-wrapper-awaiting-walk-v1-visual-approval') fail('batch identity/status changed')

const v1Register = path.join(V1_PACK, 'batch-register.json')
const v1Page = path.join(V1_PUBLIC, 'index.html')
if (sha256(v1Register) !== register.source?.walkV1Register?.sha256 || sha256(v1Page) !== register.source?.walkV1ReviewPage?.sha256) fail('Walk V1 provenance changed')
if (register.source?.walkV1Status !== 'draft-finished-art-walk-v1-awaiting-visual-approval') fail('Walk V1 approval state changed')

const assets = register.publishedAssets as Record<string, any>[]
if (!Array.isArray(assets) || assets.length !== 13) fail('published asset inventory changed')
for (const asset of assets) {
  const source = path.join(ROOT, asset.v1File)
  const target = path.join(ROOT, asset.v2File)
  if (!fs.existsSync(source) || !fs.existsSync(target)) fail(`missing copied asset ${asset.name}`)
  const sourceHash = sha256(source)
  const targetHash = sha256(target)
  if (sourceHash !== asset.v1Sha256 || targetHash !== asset.v2Sha256 || sourceHash !== targetHash || asset.byteIdentical !== true) fail(`asset bytes differ: ${asset.name}`)
}

const pagePath = path.join(PUBLIC, 'index.html')
if (sha256(pagePath) !== register.reviewPage?.sha256 || register.reviewPage?.assetPrefix !== PREFIX || register.reviewPage?.relativeAssetUrls !== false || register.reviewPage?.artworkChanged !== false) fail('review page record changed')
const html = fs.readFileSync(pagePath, 'utf8')
for (const forbidden of ['src="assets/', 'const frames=["assets/', 'href="assets/']) if (html.includes(forbidden)) fail(`relative asset path remains: ${forbidden}`)
for (const asset of assets) if (!html.includes(`${PREFIX}${asset.name}`) && !['side-a172a8a01a387a21.png'].includes(asset.name)) fail(`review page omits ${asset.name}`)
for (const phrase of ['Keeper Prime Walk V2 · right-facing', 'Walk V1 artwork · fixed review routing · awaiting visual approval', 'absolute review asset addresses', 'Nothing has entered Final or production']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('public playback script missing')
new Function(script)

for (const flag of ['allWalkV1AssetsCopiedByteIdentically']) if (register.validation?.[flag] !== true) fail(`${flag} changed`)
for (const flag of ['walkV1FilesChanged', 'productionSpritesChanged', 'runtimeManifestChanged', 'workbenchFinalChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['walkV1ArtworkApproved', 'walkStopApproved', 'finalLaneEntryAllowed', 'productionPromotionAllowed']) if (register.approvalBoundary?.[flag] !== false) fail(`${flag} approval boundary changed`)

console.log('Keeper Prime Walk V2 verified: 13 Walk V1 assets are byte-identical, all review URLs are absolute, playback compiles and no approval or production boundary changed.')
