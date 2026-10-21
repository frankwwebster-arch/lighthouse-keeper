import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const oldSetName = 'kitchen-built-in-state-ligne-claire-v4'
const newSetName = 'kitchen-built-in-state-ligne-claire-v4-delivery-v2'
const read = relative => fs.readFileSync(path.join(root, relative))
const text = relative => read(relative).toString('utf8')
const json = relative => JSON.parse(text(relative))
const sha = relative => crypto.createHash('sha256').update(read(relative)).digest('hex')

const oldPage = `public/keeper-review/${oldSetName}/index.html`
const newPage = `public/keeper-review/${newSetName}/index.html`
const oldManifest = json(`review-archive/sets/${oldSetName}.json`)
const newManifest = json(`review-archive/sets/${newSetName}.json`)
const page = text(newPage)

assert.equal(sha(oldPage), '27732340d908aa60e094dae5444ebde2b2eee88f53e1f0b94b5393acd929fcae', 'immutable V4 page changed')
assert.equal(newManifest.page.sha256, sha(newPage), 'delivery-v2 page hash drifted')
assert.equal(newManifest.set, newSetName)
assert.equal(fs.existsSync(path.join(root, `public/keeper-review/${newSetName}/assets`)), false, 'review media returned to public payload')

const evidence = {
  'evidence--on-broken-healing-current-vs-candidate.png': 'on-broken-healing-current-vs-candidate.png',
  'evidence--oven-on-broken-current-vs-candidate.png': 'oven-on-broken-current-vs-candidate.png',
  'evidence--dishwasher-on-broken-current-vs-candidate.png': 'dishwasher-on-broken-current-vs-candidate.png',
  'evidence--oven-broken-animation-sampler-current-vs-candidate.png': 'oven-broken-animation-sampler-current-vs-candidate.png',
}

assert.equal(Object.keys(newManifest.entries).length, Object.keys(evidence).length)
for (const [publishedName, draftName] of Object.entries(evidence)) {
  const oldPath = `/keeper-review/${oldSetName}/assets/${publishedName}`
  const newPath = `/keeper-review/${newSetName}/assets/${publishedName}`
  const oldEntry = oldManifest.entries[oldPath]
  const newEntry = newManifest.entries[newPath]
  assert.ok(oldEntry && newEntry, `${publishedName} archive mapping missing`)
  assert.deepEqual(newEntry, oldEntry, `${publishedName} delivery bytes changed`)
  assert.equal(
    sha(`art/drafts/kitchen-built-in-state-ligne-claire-2026-10-21-v4/evidence/${draftName}`),
    newEntry.sha256,
    `${publishedName} no longer matches immutable V4 evidence`,
  )
  assert.match(page, new RegExp(`assets/${publishedName.replaceAll('.', '\\.')}`))
}

assert.match(page, /Promise\.all\(images\.map\(image=>image\.decode\(\)\)\)/, 'decode gate missing')
assert.match(page, /slot x − 4, 104/, 'sink datum not stated')
assert.match(page, /no artwork, geometry or behaviour changed/i)

const route = text('src/app/keeper-review/[set]/assets/[asset]/route.ts')
const proxy = text('src/lib/reviewArchiveProxy.ts')
assert.match(route, new RegExp(newSetName))
assert.match(route, /proxyReviewArchiveEntry\(entry\)/)
assert.match(proxy, /createHash\('sha256'\)/)
assert.match(proxy, /digest !== entry\.sha256/)
assert.match(proxy, /max-age=31536000, immutable/)
assert.match(proxy, /Cross-Origin-Resource-Policy': 'same-origin'/)

console.log(JSON.stringify({
  set: newSetName,
  immutableV4PagePreserved: true,
  exactEvidenceObjectsReused: Object.keys(evidence).length,
  sameOriginDelivery: true,
  sinkDatum: '(slot x - 4, 104)',
  runtimeAssetsChanged: false,
  status: 'verified',
}, null, 2))
