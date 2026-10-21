import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const sourceSetName = 'kitchen-built-in-state-ligne-claire-v4'
const failedSetName = 'kitchen-built-in-state-ligne-claire-v4-delivery-v2'
const setName = 'kitchen-built-in-state-ligne-claire-v4-delivery-v3'
const read = relative => fs.readFileSync(path.join(root, relative))
const text = relative => read(relative).toString('utf8')
const json = relative => JSON.parse(text(relative))
const sha = relative => crypto.createHash('sha256').update(read(relative)).digest('hex')

const sourceManifest = json(`review-archive/sets/${sourceSetName}.json`)
const manifest = json(`review-archive/sets/${setName}.json`)
const pagePath = `public/keeper-review/${setName}/index.html`
const page = text(pagePath)

assert.equal(
  sha(`public/keeper-review/${failedSetName}/index.html`),
  'a484fc99ad9b6a1dfa71708471cef21424ffed6eab4ba7d61bf723a8798b6de9',
  'failed Delivery V2 page changed instead of being preserved',
)
assert.equal(manifest.page.sha256, sha(pagePath), 'Delivery V3 page hash drifted')
assert.equal(manifest.set, setName)
assert.equal(fs.existsSync(path.join(root, `public/keeper-review/${setName}/assets`)), false, 'review media returned to public payload')

const evidence = {
  'evidence--on-broken-healing-current-vs-candidate.png': 'on-broken-healing-current-vs-candidate.png',
  'evidence--oven-on-broken-current-vs-candidate.png': 'oven-on-broken-current-vs-candidate.png',
  'evidence--dishwasher-on-broken-current-vs-candidate.png': 'dishwasher-on-broken-current-vs-candidate.png',
  'evidence--oven-broken-animation-sampler-current-vs-candidate.png': 'oven-broken-animation-sampler-current-vs-candidate.png',
}

assert.equal(Object.keys(manifest.entries).length, Object.keys(evidence).length)
for (const [publishedName, draftName] of Object.entries(evidence)) {
  const sourcePath = `/keeper-review/${sourceSetName}/assets/${publishedName}`
  const publishedPath = `/keeper-review/${setName}/assets/${publishedName}`
  const sourceEntry = sourceManifest.entries[sourcePath]
  const entry = manifest.entries[publishedPath]
  assert.ok(sourceEntry && entry, `${publishedName} archive mapping missing`)
  assert.deepEqual(entry, sourceEntry, `${publishedName} delivery bytes changed`)
  assert.equal(
    sha(`art/drafts/kitchen-built-in-state-ligne-claire-2026-10-21-v4/evidence/${draftName}`),
    entry.sha256,
    `${publishedName} no longer matches immutable V4 evidence`,
  )
  const escapedPath = publishedPath.replaceAll('.', '\\.')
  assert.match(page, new RegExp(`href="${escapedPath}"`), `${publishedName} link is not root-absolute`)
  assert.match(page, new RegExp(`src="${escapedPath}"`), `${publishedName} image is not root-absolute`)
}

assert.doesNotMatch(page, /(?:href|src)="assets\//, 'relative asset URL would break after Vercel slash canonicalization')
assert.match(page, /Promise\.all\(images\.map\(image=>image\.decode\(\)\)\)/, 'decode gate missing')
assert.match(page, /slot x − 4, 104/, 'sink datum not stated')
assert.match(page, /no artwork, geometry or behaviour changed/i)

const route = text('src/app/keeper-review/[set]/assets/[asset]/route.ts')
const deploy = text('scripts/deploy.mjs')
const archive = text('scripts/archive_keeper_review_media.mjs')
const archiveVerifier = text('scripts/verify_review_archive.mjs')
const vercelGate = text('scripts/vercel-ignore-build.mjs')
const githubDeploy = text('.github/workflows/deploy.yml')
assert.match(route, new RegExp(setName))
assert.match(route, /proxyReviewArchiveEntry\(entry\)/)
for (const [name, source] of Object.entries({ deploy, archive, archiveVerifier })) {
  assert.match(source, /verifyRootAbsoluteReviewUrls/, `${name} does not enforce root-absolute review URLs`)
}
assert.match(vercelGate, /verifyRootAbsoluteReviewUrls/, 'Vercel build gate does not enforce root-absolute review URLs')
assert.match(githubDeploy, /node scripts\/review_page_url_policy\.mjs/, 'GitHub deployment does not enforce root-absolute review URLs')

console.log(JSON.stringify({
  set: setName,
  failedDeliveryV2Preserved: true,
  exactEvidenceObjectsReused: Object.keys(evidence).length,
  rootAbsoluteSameOriginDelivery: true,
  sinkDatum: '(slot x - 4, 104)',
  runtimeAssetsChanged: false,
  status: 'verified',
}, null, 2))
