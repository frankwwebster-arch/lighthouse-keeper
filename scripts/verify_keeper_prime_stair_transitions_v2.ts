import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { PNG } from 'pngjs'

const root = process.cwd()
const pack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-15-v2')
const specFile = path.join(pack, 'keeper-prime-stair-transitions-v2.json')
const registerFile = path.join(pack, 'batch-register.json')
const pageFile = path.join(root, 'public/keeper-review/keeper-prime-stair-transitions-v2/index.html')
const sha = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message: string): never => { throw new Error(`[keeper-prime-stair-transitions-v2] ${message}`) }
const read = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8'))

for (const file of [specFile, registerFile, pageFile]) if (!fs.existsSync(file)) fail(`missing ${path.relative(root, file)}`)
const spec = read(specFile)
const register = read(registerFile)
const lower = spec.routes.lowerJoin.frames
const seam = spec.routes.seamReview.frames
const upper = spec.routes.upperExit.frames
const full = spec.routes.fullFlow.frames

if (spec.schema !== 'lighthouse-keeper/stair-transitions@2') fail('schema changed')
if (seam.length !== 9 || lower.length !== 24 || upper.length !== 92 || full.length !== 131) fail('route length changed')
const expectedOrder = [8, 1, 2, 3, 4, 5, 6, 7]
for (let index = 0; index < 16; index++) {
  const expected = expectedOrder[index % 8]
  if (lower[index].sourceFrame !== `walk:${expected}`) fail(`walk phase ${index + 1} changed`)
  const expectedRoot = 161.5 - ((index + 1) * 2.625)
  if (Math.abs(lower[index].xLp - expectedRoot) > 1e-9) fail(`walk root ${index + 1} changed`)
}
if (lower[15].sourceFrame !== 'walk:7' || lower[16].sourceFrame !== 'stair-mount:left-passing' || lower[17].sourceFrame !== 'stair:1') fail('corrected seam changed')
if (JSON.stringify(seam) !== JSON.stringify(lower.slice(12, 21))) fail('focused seam route changed')
if (!(lower[15].xLp > lower[16].xLp && lower[16].xLp > lower[17].xLp)) fail('corrected seam does not advance')
if (lower[15].bottomLp !== 19.5 || lower[16].bottomLp !== 19.5 || lower[17].bottomLp !== 19.5) fail('corrected seam baseline changed')
for (let index = 0; index < 24; index++) {
  for (const key of ['src', 'sourceFrame', 'xLp', 'bottomLp', 'flipX']) {
    if (full[index][key] !== lower[index][key]) fail(`full route lower seam disagrees at frame ${index + 1} ${key}`)
  }
}

const old = read(path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-15-v1/batch-register.json'))
const oldHashes = new Map(old.publishedAssets.map((asset: any) => [asset.source, asset.sourceSha256]))
for (const asset of register.publishedAssets) {
  const source = path.join(root, asset.source)
  if (!fs.existsSync(source) || sha(source) !== asset.sourceSha256) fail(`source hash mismatch ${asset.source}`)
  if (oldHashes.get(asset.source) !== asset.sourceSha256) fail(`asset differs from immutable V1 authority ${asset.source}`)
  const png = PNG.sync.read(fs.readFileSync(source))
  if (png.width !== 256 || png.height !== 320) fail(`cell geometry changed ${asset.source}`)
  let edgeAlpha = 0
  for (let x = 0; x < png.width; x++) edgeAlpha += Number(png.data[(x * 4) + 3] > 0) + Number(png.data[(((png.height - 1) * png.width + x) * 4) + 3] > 0)
  for (let y = 1; y < png.height - 1; y++) edgeAlpha += Number(png.data[(y * png.width * 4) + 3] > 0) + Number(png.data[((y * png.width + png.width - 1) * 4) + 3] > 0)
  if (edgeAlpha) fail(`transparent gutter failed ${asset.source}`)
}

const html = fs.readFileSync(pageFile, 'utf8')
if (!html.includes('Promise.all(unique.map(preload))') || !html.includes("textContent='All '+unique.length")) fail('preload/decode contract changed')
if (html.includes('/keeper-review/keeper-prime-stair-transitions-v1/assets/')) fail('V1 asset path leaked into V2')
if (!html.includes('Compact Walk F7 → compact passing bridge → V16 F1')) fail('review seam explanation missing')
if (!html.includes("let routeId='seam'")) fail('focused seam is not the default route')
if (register.validation.approvedPixelBytesChanged !== false || register.validation.runtimeChanged !== false || register.validation.productionChanged !== false) fail('approval boundary changed')

console.log(JSON.stringify({ ok: true, routes: { seam: seam.length, lower: lower.length, upper: upper.length, full: full.length }, verifiedAssets: register.publishedAssets.length }, null, 2))
