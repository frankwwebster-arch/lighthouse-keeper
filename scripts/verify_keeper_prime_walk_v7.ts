#!/usr/bin/env node
/** Verify Frank's immutable approval of exact Keeper Prime Walk V6. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-14-v7')
const REGISTER = path.join(PACK, 'batch-register.json')
const V6_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-14-v6/batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-walk-v7')
const ROUTE = '/keeper-review/keeper-prime-walk-v7'
const fail = (message: string): never => { throw new Error(`Keeper Prime Walk V7 approval: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, V6_REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const v6 = JSON.parse(fs.readFileSync(V6_REGISTER, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-walk-2026-10-14-v7' || record.status !== 'approved-walk-v6-locomotion-artwork-authority') fail('identity/status changed')
if (record.approval?.approvedBy !== 'Frank' || record.approval?.approvedOn !== '2026-10-14' || record.approval?.wording !== 'Approved') fail('approval wording changed')
if (record.approvedCandidate?.registerSha256 !== hash(V6_REGISTER)) fail('V6 register provenance changed')
if (record.approvedCandidate?.fps !== 8 || record.approvedCandidate?.frames?.length !== 8) fail('approved cadence changed')

for (const [index, frame] of (record.approvedCandidate.frames as Record<string, any>[]).entries()) {
  const source = path.join(ROOT, frame.file)
  if (frame.file !== v6.frames[index].file || frame.sha256 !== v6.frames[index].sha256 || hash(source) !== frame.sha256) fail(`approved F${index + 1} changed`)
  const png = PNG.sync.read(fs.readFileSync(source))
  if (png.width !== 256 || png.height !== 320) fail(`approved F${index + 1} cell changed`)
  const asset = fs.readdirSync(path.join(PUBLIC, 'assets')).find(name => name.startsWith(`frame${index + 1}-`))
  if (!asset || hash(path.join(PUBLIC, 'assets', asset)) !== frame.sha256) fail(`public F${index + 1} differs from V6`)
}
const strip = record.approvedCandidate.strip
if (strip.sha256 !== v6.animation.strip.sha256 || strip.sidecarSha256 !== v6.animation.strip.sidecarSha256 || hash(path.join(ROOT, strip.file)) !== strip.sha256 || hash(path.join(ROOT, strip.sidecar)) !== strip.sidecarSha256) fail('approved strip/sidecar changed')
for (const asset of record.reviewSurface.publicAssets as Record<string, any>[]) if (hash(path.join(ROOT, asset.file)) !== asset.sha256) fail(`public asset changed: ${asset.file}`)
const page = path.join(ROOT, record.reviewSurface.publicPage)
if (hash(page) !== record.reviewSurface.publicPageSha256) fail('approval page changed')
const html = fs.readFileSync(page, 'utf8')
for (const phrase of ['approved locomotion authority', 'Approved locomotion artwork authority · 14 October 2026', 'Frank approved exact Walk V6', 'Final and production remain unchanged']) if (!html.includes(phrase)) fail(`approval page omits ${phrase}`)
if (html.includes('/keeper-review/keeper-prime-walk-v6/assets/')) fail('approval page still references V6 route')
for (let index = 1; index <= 8; index += 1) {
  const asset = fs.readdirSync(path.join(PUBLIC, 'assets')).find(name => name.startsWith(`frame${index}-`))
  if (!asset || !html.includes(`${ROUTE}/assets/${asset}`)) fail(`approval page omits routed F${index}`)
}
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('playback script missing')
new Function(script)
for (const flag of ['v6RegisterUnchanged', 'allEightFrameHashesPinned', 'publicAssetsByteIdenticalToV6', 'approvalPackDuplicatesNoArtwork']) if (record.validation?.[flag] !== true) fail(`${flag} changed`)
for (const flag of ['artPixelsChangedByV7', 'productionSpritesChanged', 'runtimeManifestChanged', 'finalLaneChanged', 'priorDraftsChanged']) if (record.validation?.[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['walkV6Approved', 'coreRightFacingLocomotionAuthority', 'finalLaneEntryAllowed']) if (record.approvalBoundary?.[flag] !== true) fail(`${flag} approval changed`)
for (const flag of ['stopToWalkApproved', 'walkToStopApproved', 'productionPromotionAllowed']) if (record.approvalBoundary?.[flag] !== false) fail(`${flag} approval changed`)
for (const forbidden of ['drafts', 'sources', 'evidence', 'palette']) if (fs.existsSync(path.join(PACK, forbidden))) fail(`approval pack duplicates art in ${forbidden}`)
console.log('Keeper Prime Walk V7 approval verified: exact Walk V6 eight-frame/8-fps authority pinned; no artwork, Final or production changes.')
