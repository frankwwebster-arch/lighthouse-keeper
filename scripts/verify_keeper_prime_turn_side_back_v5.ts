#!/usr/bin/env node
/** Verify immutable V4 approval plus synchronized large/game-scale review controls. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v5')
const REGISTER = path.join(PACK, 'batch-register.json')
const V4_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v4/batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-turn-side-back-v5')
const PUBLIC_ROUTE = '/keeper-review/keeper-prime-turn-side-back-v5'
const fail = (message: string): never => { throw new Error(`Keeper Prime side ↔ back Turn V5 approval: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, V4_REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const v4 = JSON.parse(fs.readFileSync(V4_REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-turn-side-back-2026-10-13-v5' || register.status !== 'approved-side-back-turn-artwork-authority') fail('batch identity/status changed')
if (register.approval?.approvedBy !== 'Frank' || register.approval?.approvedOn !== '2026-10-13' || register.approval?.wording !== 'Approved.') fail('approval wording changed')
if (register.approvedCandidate?.registerSha256 !== sha256(V4_REGISTER)) fail('approved V4 register changed')

const expectedFrameHashes = [
  'a172a8a01a387a21d14c092d2a9eb53b938a44574279108a5776e2cc67f2fff3',
  'e1dc020aabfe8f3ba519630c85885bf8f4db31e439232d017ec7e38c8a3ad4d5',
  '34028d8821a7272a37d35724d687c17d75f5cd1d7acf1ed216a1bd7c239e3859',
  '0d278363a0e7e4f1e6bf92ca44199df822451aa012fd1b086b6e3fdc5bb0e655',
  'f827ac61f45aaaa495546777f470cbb62818530dceea5e2251649d47ca0bd7dc',
  'fe06522abd0cd55cf70f40378c7c52bdb08c9911022b3dd6daa7fbf1bbca291c',
  'ba4a9ee3bf122e226e2cda411b724374c7b04749aa7f398e449d7ee42071c77b',
  '89192561909568824a5b9dd6e30200a0ca9421b955201d3d2aeb865b388f51d8',
]
const approvedFrames = register.approvedCandidate.frames as Record<string, any>[]
if (approvedFrames.length !== 8 || JSON.stringify(approvedFrames.map((item) => item.sha256)) !== JSON.stringify(expectedFrameHashes)) fail('approved frame hashes changed')
for (const [index, item] of approvedFrames.entries()) {
  const source = path.join(ROOT, item.file)
  if (sha256(source) !== item.sha256 || item.file !== v4.frames[index].file || item.sha256 !== v4.frames[index].sha256) fail(`approved frame ${index + 1} no longer matches V4`)
  const png = PNG.sync.read(fs.readFileSync(source))
  if (png.width !== 256 || png.height !== 320) fail(`approved frame ${index + 1} source cell changed`)
  const publicName = fs.readdirSync(path.join(PUBLIC, 'assets')).find((name) => name.startsWith(`frame${index + 1}-`))
  if (!publicName || sha256(path.join(PUBLIC, 'assets', publicName)) !== item.sha256) fail(`public frame ${index + 1} is not byte-identical to V4`)
}
for (const [key, expected] of [['forwardStrip', 'bff5fb2428c23f26b9618a4ce5b46e543b3ee4f1636a823e248a36d84cd62f9f'], ['reverseStrip', '13ce475c350fa6a55f5bad7847a05f7ab89c24de03e035c6deab26f1830eedc7']] as const) {
  const record = register.approvedCandidate[key]
  if (record.sha256 !== expected || sha256(path.join(ROOT, record.file)) !== expected || sha256(path.join(ROOT, record.sidecar)) !== record.sidecarSha256) fail(`${key} provenance changed`)
}
if (sha256(path.join(ROOT, register.approvedCandidate.palette.file)) !== register.approvedCandidate.palette.sha256) fail('approved standard-uniform palette provenance changed')
if (sha256(path.join(ROOT, register.approvedCandidate.rearBootChangedMask)) !== register.approvedCandidate.rearBootChangedMaskSha256) fail('approved rear-boot mask provenance changed')

const display = register.displayContract
if (JSON.stringify(display.logicalCell) !== '[32,40]' || JSON.stringify(display.sourceCell) !== '[256,320]' || display.sourceDensity !== 8 || display.gamePixelsPerLogicalPixel !== 4 || JSON.stringify(display.gameCssDisplay) !== '[128,160]') fail('game display geometry changed')
const assetContractPath = path.join(ROOT, display.assetContract)
const rendererPath = path.join(ROOT, display.spriteRenderer)
if (sha256(assetContractPath) !== display.assetContractSha256 || sha256(rendererPath) !== display.spriteRendererSha256) fail('game display authority changed')
const assetContract = JSON.parse(fs.readFileSync(assetContractPath, 'utf8')) as Record<string, any>
if (JSON.stringify(assetContract.canvas?.standard) !== JSON.stringify({ width: 32, height: 40, density: 4, anchor: [16, 40] })) fail('standard game canvas contract changed')
const renderer = fs.readFileSync(rendererPath, 'utf8')
for (const phrase of ['export const PX = 4', 'w = entry.w * PX', 'h = entry.h * PX']) if (!renderer.includes(phrase)) fail(`sprite renderer omits ${phrase}`)

const pagePath = path.join(ROOT, register.reviewSurface.publicPage)
if (sha256(pagePath) !== register.reviewSurface.publicPageSha256) fail('review page hash changed')
const html = fs.readFileSync(pagePath, 'utf8')
for (const phrase of [
  'Approved artwork authority · 13 October 2026', 'every animation frame remains byte-identical to V4',
  'id="previous"', 'id="next"', '← Previous frame', 'Next frame →',
  'id="largePlayer"', 'id="gamePlayer"', 'width:128px;height:160px',
  '32 × 40 logical pixels', '128 × 160 CSS-pixel box', 'large.src=frames[index];game.src=frames[index]',
  "document.getElementById('previous').onclick=()=>step(-1)", "document.getElementById('next').onclick=()=>step(1)",
  'index=(i+frames.length)%frames.length',
  'This page does not alter Final, production sprites or the runtime manifest',
]) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (html.includes('src="assets/') || html.includes('"assets/')) fail('review page uses trailing-slash-dependent asset URLs')
for (let index = 0; index < 8; index += 1) {
  const publicName = fs.readdirSync(path.join(PUBLIC, 'assets')).find((name) => name.startsWith(`frame${index + 1}-`))
  if (!publicName || !html.includes(`${PUBLIC_ROUTE}/assets/${publicName}`)) fail(`review page does not route frame ${index + 1} correctly`)
  if (!html.includes(`data-frame="${index}"`)) fail(`direct selector missing for frame ${index + 1}`)
}
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review playback script missing')
new Function(script)
if (JSON.stringify(register.reviewSurface.controls) !== JSON.stringify(['previous-frame', 'next-frame', 'play-forward', 'play-reverse', 'loop-both', 'pause', 'frame-time', 'direct-frame-selection']) || register.reviewSurface.viewsFrameSynchronized !== true) fail('review control contract changed')

for (const flag of ['v4RegisterUnchanged', 'allApprovedFrameHashesPinned', 'publicFramesByteIdenticalToV4', 'largeAndGameViewsUseSameFrameUrls']) if (register.validation?.[flag] !== true) fail(`${flag} validation changed`)
for (const flag of ['artPixelsChangedByV5', 'productionSpritesChanged', 'runtimeManifestChanged', 'finalLaneChanged', 'priorDraftsChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
const boundary = register.approvalBoundary
for (const flag of ['sideBackTurnV4Approved', 'rearBootEndpointApproved', 'standardOutfitPaletteApproved', 'coreTurnArtworkAuthority', 'finalLaneEntryAllowed']) if (boundary?.[flag] !== true) fail(`${flag} approval boundary changed`)
if (boundary?.productionPromotionAllowed !== false) fail('production promotion boundary changed')
for (const forbidden of ['drafts', 'evidence', 'sources', 'palette']) if (fs.existsSync(path.join(PACK, forbidden))) fail(`approval pack must not duplicate artwork in ${forbidden}`)

console.log('Keeper Prime side ↔ back Turn V5 approval verified: exact V4 artwork pinned; previous/next controls; synchronized large and 128×160 game-scale views; no production change.')
