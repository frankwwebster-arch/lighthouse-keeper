import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const set = 'kitchen-complete-room-layout-2026-10-22-v3'
const route = '/keeper-review/kitchen-complete-room-layout-v3'
const draft = path.join(root, 'art/drafts', set)
const pagePath = path.join(root, 'public/keeper-review/kitchen-complete-room-layout-v3/index.html')
const publicManifestPath = path.join(root, 'public/keeper-review/kitchen-complete-room-layout-v3/manifest.json')
const archivePath = path.join(root, 'review-archive/sets/kitchen-complete-room-layout-v3.json')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

const manifest = JSON.parse(fs.readFileSync(path.join(draft, 'manifest.json'), 'utf8'))
assert.equal(manifest.schema, 'lighthouse-keeper/kitchen-complete-room-layout@3')
assert.equal(manifest.deliveryPredecessor.manifestSha256, 'a3a4bbef753700b168a8341c2ff1dfd6b4eecab9436e550e51ec85849ab87b33')
assert.equal(manifest.deliveryPredecessor.drawingPixelsChanged, false)
assert.equal(manifest.deliveryPredecessor.roomGeometryChanged, false)
assert.equal(manifest.deliveryPredecessor.interactionChanged, false)
assert.equal(manifest.atlas.drawingCount, 19)
assert.equal(manifest.atlas.uniqueImageRequests, 1)
assert.equal(manifest.atlas.lossless, true)

const atlasPath = path.join(draft, 'assets', manifest.atlas.file)
assert.equal(sha(atlasPath), manifest.atlas.sha256)
assert.equal(sha(publicManifestPath), sha(path.join(draft, 'manifest.json')))
const [atlasWidth, atlasHeight] = manifest.atlas.pixels
const records = [...Object.values(manifest.assets), ...Object.values(manifest.looseAssets)]
assert.equal(new Set(records.map(record => record.file)).size, 1)
for (const record of records) {
  const [x, y, width, height] = record.atlasRect
  assert.ok(x >= 0 && y >= 0 && width > 0 && height > 0)
  assert.ok(x + width <= atlasWidth && y + height <= atlasHeight)
  assert.deepEqual([width, height], record.pixels)
}
for (let a = 0; a < records.length; a += 1) for (let b = a + 1; b < records.length; b += 1) {
  const [ax, ay, aw, ah] = records[a].atlasRect
  const [bx, by, bw, bh] = records[b].atlasRect
  assert.ok(ax + aw <= bx || bx + bw <= ax || ay + ah <= by || by + bh <= ay, `atlas overlap ${a}/${b}`)
}

const page = fs.readFileSync(pagePath, 'utf8')
assert.ok(page.includes("const ROUTE='/keeper-review/kitchen-complete-room-layout-v3'"))
assert.ok(page.includes("1 ATLAS READY • 19 DRAWINGS"))
assert.ok(page.includes("atlas timed out after 30 seconds"))
assert.equal(page.includes('loadImage('), false)
assert.equal(page.includes('kitchen-complete-room-layout-v2'), false)

assert.ok(fs.existsSync(archivePath), 'run npm run maintain:keeper-review before verification')
const archive = JSON.parse(fs.readFileSync(archivePath, 'utf8'))
const entry = archive.entries[`${route}/assets/${manifest.atlas.file}`]
assert.ok(entry)
assert.equal(entry.sha256, manifest.atlas.sha256)
assert.equal(sha(path.join(root, entry.object)), manifest.atlas.sha256)
assert.equal(Object.keys(archive.entries).length, 1)
assert.equal(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-complete-room-layout-v3/assets')), false)

const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.ok(nextConfig.includes("source: '/keeper-review/kitchen-complete-room-layout-v3'"))
assert.ok(nextConfig.includes("destination: '/keeper-review/kitchen-complete-room-layout-v3/index.html'"))
console.log('Kitchen Complete Room Layout V3 verification passed (one lossless atlas, 19 unchanged drawings, immutable V2).')
