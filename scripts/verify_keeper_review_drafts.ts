#!/usr/bin/env node
/** Verify reversible exact-name keeper review drafts and promoted replacements. */
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const REGISTRY = path.join(ROOT, 'data/keeper_review_drafts.json')
const fail = (message: string): never => { throw new Error(`keeper review drafts: ${message}`) }
const absolute = (relative: string) => path.join(ROOT, relative)
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const pixelSha256 = (file: string) => {
  const image = PNG.sync.read(fs.readFileSync(file))
  return crypto.createHash('sha256').update(`${image.width}x${image.height}:`).update(image.data).digest('hex')
}
const readJson = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8')) as Record<string, any>

const selectedSources: Record<string, string> = {
  keeper_darts: 'ed8fd9e733c4468541f20b4976e75111838f76194c592951ecf6b27211aefa48',
  keeper_guitar_pickup_flying_v_1967: '183e9ad3b1f7288c327a7109a2f1e3f507f909e1f67482b6e33be763d842dc69',
  keeper_guitar_pickup_gretsch: '62319e80e21c9d093178f18521580b926ffcc2ed785c5946321959d42b09fae6',
  keeper_guitar_pickup_acoustic: '97220284e11ed3bd664c5d65be655b63fe3284f800a2f86c93912dbcad3b6893',
  keeper_fish_standing: '9ecf2af163e9290499be1379e61580c459685d966e6a82d2db0312aca7f87124',
  keeper_fish_seated: '8dedc0f4473fcdc49d8d67e2ff494f0e99e17391ca8e5a7462bbb592c2c06580',
  keeper_clear_snow: 'c4eea3f639873f14d91736a10c7f411d6da4423ac158fb6346fe79a3cb3c87a6',
  keeper_meal_place_side: '46b5157591944ac624118f759a4c6bf6949501e391b3e7e06a1fa442788302e4',
  keeper_parachute_drift: '5f461731f05c2eeb7c2e7e911e5a5760e70a127337f2be81b6b4399f8612a39f',
  keeper_parachute_landing: '6a0b199f02897906e20207bd4badbbe79687daaea36472322f1681129e861976',
  keeper_machete_side: 'df6209ee8d6a0b5abb7133881721164846b9065bcfd189ce03d5b60c1eac7fc0',
}
const acceptedArtistDraftStrips: Record<string, string> = {
  keeper_artist_smock_sit_front: 'ab7bdc63c78dbebdbdf8010fda7593cb42ae805b5e2d2a2e10fccaea6e7f4788',
  keeper_artist_smock_turn_back: '67dfa4b1cf64b3fa60dd67e4161ec1b73a887f92ba3a86666049f65c9c4068dd',
  keeper_artist_smock_turn_front: 'cf1f5f6af7eaad6e19368497de3c019df57a9fd245be37c6f62456964c4af911',
  keeper_artist_smock_walk: 'aab1c99a9f5d97edf6937437d744085aecf162a839bf23d9581683956b4f7af3',
  keeper_paint_back: '0395c4db55062516df1eaf752dfe81e093f2186886e6e191eb1730b658659e85',
  keeper_paint_side: '3cf424326da7394357c12845c7e10ce21af0efc09777cade72c1672357be610f',
  keeper_pottery_front: '2fac8fb3c10b92df68efa0c365cdba0e83736caed14903246bd5babd8a288c95',
}
const acceptedSnookerDraftStrips: Record<string, string> = {
  keeper_snooker: '01bb338512f37561efd86ceb4256c855e4f7b3e250a49b1b5e275d528a25eab0',
}
if (!fs.existsSync(REGISTRY)) fail('registry is missing')
const registry = readJson(REGISTRY)
if (registry.version !== 1 || !Array.isArray(registry.drafts)) fail('registry schema is invalid')
const registers = registry.drafts.map((item: Record<string, any>) => item.register)
if (new Set(registers).size !== registers.length) fail('registry contains a duplicate draft register')

const reviewHtml = fs.readFileSync(path.join(ROOT, 'public/keeper-review/index.html'), 'utf8')
const payload = JSON.parse(reviewHtml.split('const DATA=', 2)[1].split(';\nconst $=', 1)[0]) as Record<string, any>
const pageAssets = new Map(payload.assets.map((asset: Record<string, any>) => [asset.name, asset]))

for (const item of registry.drafts as Record<string, any>[]) {
  const name = item.name as string
  const expectedStatus = item.status as string
  if (!['promoted-review-draft', 'active-review-draft'].includes(expectedStatus)) fail(`${name} has unsupported registry status ${expectedStatus}`)
  if (item.status !== expectedStatus) fail(`${name} has unexpected status ${item.status}`)
  const record = readJson(absolute(item.register))
  if (record.animation !== name) fail(`${name} register detached from its exact animation name`)
  if (record.status !== expectedStatus) fail(`${name} register status is stale`)

  for (const sectionName of ['canonical', 'draft'] as const) {
    const section = record[sectionName]
    const keys = sectionName === 'canonical' ? ['strip', 'runtime', 'sidecar'] : ['source', 'strip', 'sidecar']
    for (const key of keys) {
      const file = absolute(section[key])
      if (!fs.existsSync(file)) fail(`${name} ${sectionName} ${key} is missing`)
      if (section[`${key}Sha256`] !== sha256(file)) fail(`${name} ${sectionName} ${key} SHA-256 is stale`)
    }
  }
  if (record.canonical.stripSha256 === record.draft.stripSha256 && !record.qualification?.match(/metadata|accepted art|unchanged/i)) fail(`${name} replacement is byte-identical without a metadata-only qualification`)
  if (record.draft.workingSource) {
    const working = absolute(record.draft.workingSource)
    if (!fs.existsSync(working) || sha256(working) !== record.draft.workingSourceSha256) fail(`${name} isolated working source is stale`)
    if (!record.qualification) fail(`${name} does not explain why an isolated working source was required`)
  }

  const sidecar = readJson(absolute(record.draft.sidecar))
  const image = PNG.sync.read(fs.readFileSync(absolute(record.draft.strip)))
  const frameWidth = sidecar.w * sidecar.density
  if (image.width !== sidecar.frames * frameWidth || image.height !== sidecar.h * sidecar.density) fail(`${name} draft geometry does not match its sidecar`)
  for (let frame = 0; frame < sidecar.frames; frame += 1) {
    let opaque = 0
    for (let y = 0; y < image.height; y += 1) for (let x = 0; x < frameWidth; x += 1) {
      const alpha = image.data[((y * image.width) + frame * frameWidth + x) * 4 + 3]
      if (alpha > 0) opaque += 1
      if (alpha > 0 && (x === 0 || x === frameWidth - 1 || y === 0 || y === image.height - 1)) fail(`${name} frame ${frame + 1} lost its transparent safety gutter`)
    }
    if (!opaque) fail(`${name} frame ${frame + 1} is empty`)
  }
  if (!Array.isArray(record.draft.frameEvidence) || record.draft.frameEvidence.length !== sidecar.frames) fail(`${name} frame ownership evidence is incomplete`)
  for (const evidence of record.draft.evidence ?? []) if (!fs.existsSync(absolute(evidence))) fail(`${name} evidence is missing: ${evidence}`)

  const page = pageAssets.get(name) as Record<string, any> | undefined
  const variants = page?.draftVariants ?? (page?.draftVariant ? [page.draftVariant] : [])
  if (!variants.length) fail(`${name} has no side-by-side reviewer variant`)
  const expectedLabel = expectedStatus === 'active-review-draft' ? item.label : 'Previous version'
  const expectedComparison = expectedStatus === 'active-review-draft' ? record.draft : record.canonical
  const pageVariant = variants.find((variant: Record<string, any>) => variant.label === expectedLabel && variant.source === expectedComparison.strip && variant.sha256 === expectedComparison.stripSha256)
  if (!pageVariant) fail(`${name} has no correctly-labelled reviewer variant`)
  if (expectedStatus === 'active-review-draft') {
    if (pageVariant.source !== record.draft.strip || pageVariant.sha256 !== record.draft.stripSha256) fail(`${name} active draft is stale in the reviewer`)
    if (pageVariant.canonicalSha256 !== record.canonical.stripSha256) fail(`${name} canonical reviewer hash is stale`)
  } else {
    for (const key of ['strip', 'runtime', 'sidecar']) {
      const file = absolute(record.promotion[key])
      if (!fs.existsSync(file) || sha256(file) !== record.promotion[`${key}Sha256`]) fail(`${name} promoted ${key} is stale`)
    }
    if (record.promotion.stripSha256 !== record.draft.stripSha256 || pixelSha256(absolute(record.promotion.runtime)) !== pixelSha256(absolute(record.draft.strip))) fail(`${name} promoted pixels differ from its inspected draft`)
    if (pageVariant.source !== record.canonical.strip) fail(`${name} previous version is not visible beside production`)
    if (pageVariant.sha256 !== record.canonical.stripSha256 || pageVariant.canonicalSha256 !== record.promotion.stripSha256) fail(`${name} promoted reviewer hashes are stale`)
  }
  const comparison = expectedStatus === 'active-review-draft' ? record.draft : record.canonical
  const published = path.join(ROOT, 'public/keeper-review/drafts', `${comparison.stripSha256}.png`)
  if (!fs.existsSync(published) || sha256(published) !== comparison.stripSha256) fail(`${name} published comparison is missing or stale`)
}

const turnRegister = readJson(path.join(ROOT, 'art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/registers/keeper_artist_smock_turn_front.json'))
const sitRegister = readJson(path.join(ROOT, 'art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/registers/keeper_artist_smock_sit_front.json'))
const turnImage = PNG.sync.read(fs.readFileSync(absolute(turnRegister.draft.strip)))
const sitImage = PNG.sync.read(fs.readFileSync(absolute(sitRegister.draft.strip)))
const seamWidth = 128
const seamHeight = 160
const turnLast = Buffer.alloc(seamWidth * seamHeight * 4)
const sitFirst = Buffer.alloc(seamWidth * seamHeight * 4)
for (let y = 0; y < seamHeight; y += 1) for (let x = 0; x < seamWidth; x += 1) {
  const target = (y * seamWidth + x) * 4
  const turnSource = (y * turnImage.width + (5 * seamWidth + x)) * 4
  const sitSource = (y * sitImage.width + x) * 4
  turnImage.data.copy(turnLast, target, turnSource, turnSource + 4)
  sitImage.data.copy(sitFirst, target, sitSource, sitSource + 4)
}
if (!turnLast.equals(sitFirst)) fail('accepted V11 front transition seam is no longer complete-frame identical')

const superseded = readJson(path.join(ROOT, 'art/drafts/keeper-user-selected-batch-2026-10-10-v1/superseded-sources.json'))
const oldSnow = superseded.keeper_clear_snow
if (oldSnow.sha256 !== 'b34b7c40710d9110ef93eb5d7aecf6b4b3d6a69df54534c45ffdcebb8ebe26d6' || sha256(absolute(oldSnow.stored)) !== oldSnow.sha256) fail('superseded overlapping snow source is not preserved byte-for-byte')
if (!oldSnow.reason.includes('frame ownership')) fail('superseded snow qualification is missing')

const promotedCount = registry.drafts.filter((item: Record<string, any>) => item.status === 'promoted-review-draft').length
const activeCount = registry.drafts.filter((item: Record<string, any>) => item.status === 'active-review-draft').length
console.log(`Verified ${promotedCount} promoted comparisons and ${activeCount} active review drafts; every registered variant remains hash-pinned, published and frame-isolated`)
