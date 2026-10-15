import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { PNG } from 'pngjs'

const root = process.cwd()
const pack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-16-v3')
const specFile = path.join(pack, 'keeper-prime-stair-transitions-v3.json')
const registerFile = path.join(pack, 'batch-register.json')
const pageFile = path.join(root, 'public/keeper-review/keeper-prime-stair-transitions-v3/index.html')
const read = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message: string): never => { throw new Error(`[keeper-prime-stair-transitions-v3] ${message}`) }

for (const file of [specFile, registerFile, pageFile]) if (!fs.existsSync(file)) fail(`missing ${path.relative(root, file)}`)
const spec = read(specFile)
const register = read(registerFile)
const previousSpec = read(path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-15-v2/keeper-prime-stair-transitions-v2.json'))
const previousRegister = read(path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-15-v2/batch-register.json'))

if (spec.schema !== 'lighthouse-keeper/stair-transitions@3') fail('schema changed')
if (spec.reviewPresentation.defaultGameScale !== 4 || !spec.reviewPresentation.stableReadoutHeight || !spec.reviewPresentation.stackedViews) fail('review presentation contract changed')
for (const key of ['seamReview', 'lowerJoin', 'upperExit', 'fullFlow']) {
  const current = spec.routes[key].frames
  const previous = previousSpec.routes[key].frames
  if (current.length !== previous.length) fail(`${key} length changed`)
  for (let index = 0; index < current.length; index++) {
    const normalized = { ...current[index], src: current[index].src.replace('/keeper-review/keeper-prime-stair-transitions-v3/', '/keeper-review/keeper-prime-stair-transitions-v2/') }
    if (JSON.stringify(normalized) !== JSON.stringify(previous[index])) fail(`${key} frame ${index + 1} differs from V2`)
  }
}

const previousHashes = new Map(previousRegister.publishedAssets.map((asset: any) => [asset.source, asset.sourceSha256]))
for (const asset of register.publishedAssets) {
  const source = path.join(root, asset.source)
  if (!fs.existsSync(source) || sha(source) !== asset.sourceSha256 || previousHashes.get(asset.source) !== asset.sourceSha256) fail(`source changed ${asset.source}`)
  const png = PNG.sync.read(fs.readFileSync(source))
  if (png.width !== 256 || png.height !== 320) fail(`cell changed ${asset.source}`)
  let edgeAlpha = 0
  for (let x = 0; x < png.width; x++) edgeAlpha += Number(png.data[x * 4 + 3] > 0) + Number(png.data[((png.height - 1) * png.width + x) * 4 + 3] > 0)
  for (let y = 1; y < png.height - 1; y++) edgeAlpha += Number(png.data[y * png.width * 4 + 3] > 0) + Number(png.data[(y * png.width + png.width - 1) * 4 + 3] > 0)
  if (edgeAlpha) fail(`gutter changed ${asset.source}`)
}

const html = fs.readFileSync(pageFile, 'utf8')
for (const required of ['#readout{height:3.1em;overflow:auto', '.stage.game{width:640px;height:500px}', 'data-scale="4"', 'Studio 4×', 'grid-template-columns:1fr', 'Promise.all(unique.map(preload))']) if (!html.includes(required)) fail(`page contract missing ${required}`)
if (html.includes('1 CSS px = 1 logical px.') || html.includes('/keeper-review/keeper-prime-stair-transitions-v2/assets/')) fail('stale V2 presentation leaked')
if (register.validation.approvedPixelBytesChanged !== false || register.validation.runtimeChanged !== false || register.validation.productionChanged !== false) fail('approval boundary changed')

console.log(JSON.stringify({ ok: true, defaultGameScale: 4, stableReadout: true, stackedViews: true, verifiedAssets: register.publishedAssets.length }, null, 2))
