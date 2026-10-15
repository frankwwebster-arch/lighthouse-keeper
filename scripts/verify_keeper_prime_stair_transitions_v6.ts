import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { PNG } from 'pngjs'

const root = process.cwd()
const pack = path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-16-v6')
const specFile = path.join(pack, 'keeper-prime-stair-transitions-v6.json')
const registerFile = path.join(pack, 'batch-register.json')
const pageFile = path.join(root, 'public/keeper-review/keeper-prime-stair-transitions-v6/index.html')
const read = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const fail = (message: string): never => { throw new Error(`[keeper-prime-stair-transitions-v6] ${message}`) }
const near = (a: number, b: number, epsilon = 1e-9) => Math.abs(a - b) <= epsilon

for (const file of [specFile, registerFile, pageFile]) if (!fs.existsSync(file)) fail(`missing ${path.relative(root, file)}`)
const spec = read(specFile)
const register = read(registerFile)
const previousSpec = read(path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-16-v5/keeper-prime-stair-transitions-v5.json'))
const previousRegister = read(path.join(root, 'art/drafts/keeper-prime-stair-transitions-2026-10-16-v5/batch-register.json'))

if (spec.schema !== 'lighthouse-keeper/stair-transitions@6' || spec.status !== 'door-hidden-circulation-scale-handoff-awaiting-review') fail('identity changed')
const expectedScale = Math.sqrt(24299 / 27322)
if (!near(spec.sizeRegistration.circulationArtScale, expectedScale) || !near(spec.sizeRegistration.registeredWalkEquivalentOpaquePixels, 24299)) fail('circulation scale changed')
if (!spec.sizeRegistration.departureHandoff.includes('fully behind') || !spec.sizeRegistration.arrivalHandoff.includes('fully behind')) fail('door-hidden handoff contract changed')

const isStair = (frame: any) => frame.sourceFrame?.startsWith('stair:') || frame.sourceFrame?.startsWith('stair-mount:')
let stairFrames = 0
let circulationFrames = 0
for (const key of ['seamReview', 'lowerJoin', 'upperExit', 'fullFlow']) {
  const current = spec.routes[key].frames
  const previous = previousSpec.routes[key].frames
  if (current.length !== previous.length) fail(`${key} length changed`)
  for (let index = 0; index < current.length; index++) {
    const frame = current[index]
    const normalized = { ...frame, src: frame.src.replace('/keeper-review/keeper-prime-stair-transitions-v6/', '/keeper-review/keeper-prime-stair-transitions-v5/') }
    normalized.artScale = previous[index].artScale
    if (JSON.stringify(normalized) !== JSON.stringify(previous[index])) fail(`${key} frame ${index + 1} changed beyond scale registration`)
    if (isStair(frame)) { stairFrames++; if (frame.artScale !== undefined) fail(`${key} stair frame ${index + 1} is not native scale`) }
    else { circulationFrames++; if (!near(frame.artScale, expectedScale)) fail(`${key} circulation frame ${index + 1} lacks common scale`) }
  }
}
if (stairFrames < 40 || circulationFrames < 150) fail('route scale coverage changed')

const lower = spec.routes.lowerJoin.frames
const full = spec.routes.fullFlow.frames
const upper = spec.routes.upperExit.frames
if (lower[0].lowerDoorOpen !== 1 || lower[0].xLp < 158 || full[0].lowerDoorOpen !== 1) fail('departure no longer begins under door occlusion')
if (upper.at(-1).upperDoorOpen !== 1 || upper.at(-1).xLp < 161 || full.at(-1).upperDoorOpen !== 1) fail('arrival no longer ends under door occlusion')

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
for (const required of ['transform-origin:50% 98.75%', 'hidden handoff', 'Normal scale changes behind the door', 'data-scale="4"', 'Promise.all(unique.map(preload))']) if (!html.includes(required)) fail(`page contract missing ${required}`)
if (html.includes('/keeper-review/keeper-prime-stair-transitions-v5/assets/')) fail('stale V5 asset prefix leaked')
if (register.correction.visibleScaleChanges !== 0 || !register.correction.departureScaleHandoffFullyDoorHidden || !register.correction.arrivalScaleHandoffFullyDoorHidden) fail('hidden scale boundary changed')
if (register.validation.finalChanged !== false || register.validation.runtimeChanged !== false || register.validation.productionChanged !== false) fail('promotion boundary changed')

console.log(JSON.stringify({ ok: true, circulationArtScale: expectedScale, stairArtScale: 1, equivalentOpaquePixels: 24299, stairFrames, circulationFrames, sourceAssets: register.publishedAssets.length }, null, 2))
