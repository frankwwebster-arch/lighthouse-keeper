#!/usr/bin/env node
/** Verify Frank's immutable approval of exact Turn V9. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v10')
const REGISTER = path.join(PACK, 'batch-register.json')
const V9_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/batch-register.json')
const V8_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v8/batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-turn-side-back-v10')
const ROUTE = '/keeper-review/keeper-prime-turn-side-back-v10'
const fail = (message: string): never => { throw new Error(`Keeper Prime Turn V10 approval: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, V9_REGISTER, V8_REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const v9 = JSON.parse(fs.readFileSync(V9_REGISTER, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-turn-side-back-2026-10-13-v10' || record.status !== 'approved-side-back-turn-v9-artwork-authority') fail('identity/status changed')
if (record.approval?.approvedBy !== 'Frank' || record.approval?.approvedOn !== '2026-10-13' || record.approval?.wording !== 'approved') fail('approval wording changed')
if (record.approvedCandidate?.registerSha256 !== hash(V9_REGISTER) || record.rejectedV8?.registerSha256 !== hash(V8_REGISTER)) fail('V9/V8 provenance changed')
if (record.rejectedV8?.feedback !== "It's now significantly more jerky, so that's not an improvement") fail('V8 rejection changed')
const frames = record.approvedCandidate.frames as Record<string, any>[]
if (frames.length !== 9 || record.approvedCandidate.fps !== 9 || record.approvedCandidate.durationSeconds !== 1) fail('approved cadence changed')
for (const [index, frame] of frames.entries()) {
  const source = path.join(ROOT, frame.file)
  if (frame.file !== v9.frames[index].file || frame.sha256 !== v9.frames[index].sha256 || hash(source) !== frame.sha256) fail(`approved F${index + 1} changed`)
  const png = PNG.sync.read(fs.readFileSync(source))
  if (png.width !== 256 || png.height !== 320) fail(`approved F${index + 1} cell changed`)
  const asset = fs.readdirSync(path.join(PUBLIC, 'assets')).find(name => name.startsWith(`frame${index + 1}-`))
  if (!asset || hash(path.join(PUBLIC, 'assets', asset)) !== frame.sha256) fail(`public F${index + 1} differs from V9`)
}
if (record.approvedCandidate.midpoint?.sourceSha256 !== v9.midpoint.sourceSha256 || hash(path.join(ROOT, record.approvedCandidate.midpoint.source)) !== v9.midpoint.sourceSha256) fail('approved midpoint changed')
if (JSON.stringify(record.approvedCandidate.earOcclusion?.farLeftEarSkinPixels) !== '[0,18,181]') fail('approved ear sequence changed')
for (const key of ['forwardStrip', 'reverseStrip'] as const) {
  const approved = record.approvedCandidate[key]
  const original = v9.animation[key === 'forwardStrip' ? 'forward' : 'reverse']
  if (approved.sha256 !== original.sha256 || approved.sidecarSha256 !== original.sidecarSha256 || hash(path.join(ROOT, approved.file)) !== approved.sha256 || hash(path.join(ROOT, approved.sidecar)) !== approved.sidecarSha256) fail(`${key} changed`)
}
for (const asset of record.reviewSurface.publicAssets as Record<string, any>[]) if (hash(path.join(ROOT, asset.file)) !== asset.sha256) fail(`public asset changed: ${asset.file}`)
const pagePath = path.join(ROOT, record.reviewSurface.publicPage)
if (hash(pagePath) !== record.reviewSurface.publicPageSha256) fail('approval page changed')
const html = fs.readFileSync(pagePath, 'utf8')
for (const phrase of ['Approved artwork authority · 13 October 2026', 'Frank approved exact Turn V9 with ‘approved’', 'V8 remains rejected provenance', 'does not alter Final, production sprites or the runtime manifest', 'id="previous"', 'id="next"', 'id="largePlayer"', 'id="gamePlayer"', 'id="oldPlayer"', 'id="comparePlayer"']) if (!html.includes(phrase)) fail(`approval page omits ${phrase}`)
if (html.includes('/keeper-review/keeper-prime-turn-side-back-v9/assets/')) fail('approval page still references V9 route')
for (let index = 1; index <= 9; index += 1) {
  const asset = fs.readdirSync(path.join(PUBLIC, 'assets')).find(name => name.startsWith(`frame${index}-`))
  if (!asset || !html.includes(`${ROUTE}/assets/${asset}`)) fail(`approval page omits routed F${index}`)
}
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('playback script missing')
new Function(script)
for (const flag of ['v9RegisterUnchanged', 'allNineFrameHashesPinned', 'publicFramesByteIdenticalToV9', 'stripsAndSidecarsPinned', 'approvalPackDuplicatesNoArtwork']) if (record.validation?.[flag] !== true) fail(`${flag} changed`)
for (const flag of ['artPixelsChangedByV10', 'productionSpritesChanged', 'runtimeManifestChanged', 'finalLaneChanged', 'priorDraftsChanged']) if (record.validation?.[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['sideBackTurnV9Approved', 'singleIntermediateApproved', 'nineFpsOneSecondCadenceApproved', 'coreTurnArtworkAuthority', 'finalLaneEntryAllowed']) if (record.approvalBoundary?.[flag] !== true) fail(`${flag} approval changed`)
if (record.approvalBoundary?.productionPromotionAllowed !== false) fail('production promotion changed')
for (const forbidden of ['drafts', 'sources', 'evidence', 'palette']) if (fs.existsSync(path.join(PACK, forbidden))) fail(`approval pack duplicates art in ${forbidden}`)
console.log('Keeper Prime Turn V10 approval verified: exact V9 nine-frame/9-fps authority pinned; V8 rejected; approval page exact; Final and production unchanged.')
