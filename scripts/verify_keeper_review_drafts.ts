#!/usr/bin/env node
/** Verify reversible review drafts without treating them as production art. */
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const REGISTRY = path.join(ROOT, 'data/keeper_review_drafts.json')
const fail = (message: string): never => { throw new Error(`keeper review drafts: ${message}`) }
const absolute = (relative: string) => path.join(ROOT, relative)
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const readJson = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8')) as Record<string, any>

if (!fs.existsSync(REGISTRY)) fail('registry is missing')
const registry = readJson(REGISTRY)
if (registry.version !== 1 || !Array.isArray(registry.drafts)) fail('registry schema is invalid')
const active = registry.drafts.filter((item: Record<string, any>) => item.status === 'active-review-draft')
if (active.length !== 1 || active[0].name !== 'keeper_darts') fail('expected one exact-name keeper_darts review draft')

const record = readJson(absolute(active[0].register))
if (record.animation !== active[0].name || record.label !== active[0].label) fail('draft registry detached from its exact animation name')
for (const sectionName of ['canonical', 'draft']) {
  const section = record[sectionName]
  for (const key of sectionName === 'canonical' ? ['strip', 'runtime', 'sidecar'] : ['source', 'strip', 'sidecar']) {
    const file = absolute(section[key])
    if (!fs.existsSync(file)) fail(`${sectionName} ${key} is missing`)
    if (section[`${key}Sha256`] !== sha256(file)) fail(`${sectionName} ${key} SHA-256 is stale`)
  }
}
if (record.canonical.stripSha256 === record.draft.stripSha256) fail('draft is byte-identical to canonical')
if (record.draft.sourceSha256 !== 'ed8fd9e733c4468541f20b4976e75111838f76194c592951ecf6b27211aefa48') fail('draft source is not Frank’s selected image')

const sidecar = readJson(absolute(record.draft.sidecar))
if (sidecar.frames !== 14 || sidecar.w !== 56 || sidecar.h !== 40 || sidecar.density !== 4) fail('draft sidecar geometry changed')
if (sidecar.reviewDraft?.draftId !== record.draftId || sidecar.reviewDraft?.canonicalPromotion !== false) fail('draft reversibility metadata is missing')
const image = PNG.sync.read(fs.readFileSync(absolute(record.draft.strip)))
if (image.width !== sidecar.frames * sidecar.w * sidecar.density || image.height !== sidecar.h * sidecar.density) fail('draft strip geometry does not match sidecar')
const frameWidth = sidecar.w * sidecar.density
for (let frame = 0; frame < sidecar.frames; frame += 1) {
  let opaque = 0
  for (let y = 0; y < image.height; y += 1) for (let x = 0; x < frameWidth; x += 1) {
    const absoluteX = frame * frameWidth + x
    const alpha = image.data[((y * image.width) + absoluteX) * 4 + 3]
    if (alpha > 0) opaque += 1
    if (alpha > 0 && (x === 0 || x === frameWidth - 1 || y === 0 || y === image.height - 1)) fail(`frame ${frame + 1} lost its transparent safety gutter`)
  }
  if (!opaque) fail(`frame ${frame + 1} is empty`)
}
if (!Array.isArray(record.draft.frameEvidence) || record.draft.frameEvidence.length !== 14) fail('frame ownership evidence is incomplete')
if (!record.draft.frameEvidence.some((frame: Record<string, any>) => frame.detachedComponentCount > 0)) fail('detached dart ownership was not recorded')
for (const evidence of record.draft.evidence as string[]) if (!fs.existsSync(absolute(evidence))) fail(`evidence is missing: ${evidence}`)

const publicDraft = path.join(ROOT, 'public/keeper-review/drafts', path.basename(record.draft.strip))
if (!fs.existsSync(publicDraft) || sha256(publicDraft) !== record.draft.stripSha256) fail('published reviewer draft is missing or stale')
const reviewHtml = fs.readFileSync(path.join(ROOT, 'public/keeper-review/index.html'), 'utf8')
const payload = JSON.parse(reviewHtml.split('const DATA=', 2)[1].split(';\nconst $=', 1)[0]) as Record<string, any>
const darts = payload.assets.find((asset: Record<string, any>) => asset.name === 'keeper_darts')
if (!darts?.draftVariant || darts.draftVariant.source !== record.draft.strip) fail('review page did not attach the draft by exact animation name')
if (darts.draftVariant.sha256 !== record.draft.stripSha256 || darts.draftVariant.canonicalSha256 !== record.canonical.stripSha256) fail('review page hashes are stale')
if (darts.draftVariant.label !== 'Frank-selected draft') fail('review page does not identify the selected draft')

console.log('Verified one reversible keeper_darts review draft: 14 isolated frames; canonical raw/runtime sprites unchanged')
