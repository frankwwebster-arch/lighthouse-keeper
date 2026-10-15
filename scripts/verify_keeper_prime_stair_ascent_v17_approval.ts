#!/usr/bin/env node
/** Verify Frank's immutable approval of exact Stair Ascent V16. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v17')
const REGISTER = path.join(PACK, 'batch-register.json')
const V16 = path.join(ROOT, 'art/drafts/keeper-prime-stair-ascent-2026-10-15-v16')
const V16_REGISTER = path.join(V16, 'batch-register.json')
const V16_RIG = path.join(V16, 'stair-contact-rig-v16.json')
const V16_PAGE = path.join(ROOT, 'public/keeper-review/keeper-prime-stair-ascent-v16/index.html')
const fail = (message: string): never => { throw new Error(`Keeper Prime stair ascent V17 approval: ${message}`) }
const hash = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
for (const file of [REGISTER, V16_REGISTER, V16_RIG, V16_PAGE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const record = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const v16 = JSON.parse(fs.readFileSync(V16_REGISTER, 'utf8')) as Record<string, any>
const rig = JSON.parse(fs.readFileSync(V16_RIG, 'utf8')) as Record<string, any>
if (record.batchId !== 'keeper-prime-stair-ascent-2026-10-15-v17' || record.status !== 'approved-stair-ascent-v16-artwork-and-full-flight-authority') fail('identity/status changed')
if (record.approval?.approvedBy !== 'Frank' || record.approval?.approvedOn !== '2026-10-15' || record.approval?.wording !== "OK let's say that's done, had enough of refining it.") fail('approval wording changed')
if (record.approvedCandidate.registerSha256 !== hash(V16_REGISTER) || record.approvedCandidate.rigSha256 !== hash(V16_RIG) || record.approvedCandidate.reviewPageSha256 !== hash(V16_PAGE)) fail('V16 authority changed')
if (record.approvedCandidate.frames.length !== 4 || v16.assets.length !== 4) fail('approved four-frame authority changed')
for (const [index, frame] of record.approvedCandidate.frames.entries()) {
  const source = path.join(ROOT, frame.file)
  const authority = v16.assets[index]
  if (frame.role !== authority.role || frame.file !== authority.source || frame.sha256 !== authority.sourceSha256 || hash(source) !== frame.sha256) fail(`approved frame ${frame.role} changed`)
  const png = PNG.sync.read(fs.readFileSync(source))
  if (png.width !== 256 || png.height !== 320) fail(`${frame.role} cell changed`)
}
if (rig.timeline.length !== 27 || rig.timeline.filter((frame: any) => frame.kind === 'contact').length !== 14 || rig.timeline.filter((frame: any) => frame.kind === 'passing').length !== 13 || rig.endpoint.targetTread !== 14 || rig.endpoint.behavior !== 'hold-at-top-no-wrap') fail('approved full-flight mechanics changed')
const scenery = record.staircaseVisualContract
if (scenery.newelPosts !== 2 || scenery.newelPostPositions.join(',') !== 'lower-flight entrance,upper landing' || !scenery.balustrade.includes('foreground') || !scenery.handrail.includes('continuous rail') || !scenery.geometryRule.includes('fourteen-riser, 7-lp-tread, 98-by-60-lp')) fail('future staircase visual contract changed')
for (const flag of ['v16ArtworkApproved', 'twentySevenFrameFullFlightApproved', 'fourteenAlternatingContactsApproved', 'stairGeometryApprovedForThisAnimation', 'finalLaneEntryAllowed']) if (record.approvalBoundary[flag] !== true) fail(`${flag} approval changed`)
for (const flag of ['productionPromotionPerformed', 'runtimeWiringPerformed', 'staircaseSceneryApproved']) if (record.approvalBoundary[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['v16RegisterUnchanged', 'v16RigUnchanged', 'v16PageUnchanged', 'allFourFrameHashesPinned', 'approvalPackDuplicatesNoArtwork']) if (record.validation[flag] !== true) fail(`${flag} validation changed`)
for (const flag of ['priorDraftsChanged', 'finalLaneChanged', 'runtimeSpritesChanged', 'productionChanged']) if (record.validation[flag] !== false) fail(`${flag} boundary changed`)
for (const forbidden of ['drafts', 'sources', 'evidence', 'palette']) if (fs.existsSync(path.join(PACK, forbidden))) fail(`approval pack duplicates artwork in ${forbidden}`)
console.log('Keeper Prime stair ascent V17 approval verified: exact V16 four-drawing/27-frame authority pinned; two-newel foreground balustrade and continuous handrail contract recorded; no artwork duplication or runtime/production promotion.')
