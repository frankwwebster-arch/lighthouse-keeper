import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const reviewSet = 'keeper-prime-morning-drafts-v1'
const reviewRoot = path.join(root, 'public/keeper-review', reviewSet)
const assetRoot = path.join(reviewRoot, 'assets')
const check = process.argv.includes('--check')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')

const authorities = {
  front: {
    path: 'art/drafts/keeper-prime-master-2026-10-12-v1/drafts/keeper_prime_master-neutral-front_f1.png',
    sha256: 'a9a5c37fe72221992ec499fa3096fdd0581977b4ac03ff7788da2af411107a2e',
  },
  back: {
    path: 'art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/drafts/keeper_prime_master-neutral-standing-back_f1.png',
    sha256: 'd1d409f098a18883f419633def910b4f2fef108337b6b9aff49ac356704ebf86',
  },
  sideRight: {
    path: 'art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png',
    sha256: 'a172a8a01a387a21d14c092d2a9eb53b938a44574279108a5776e2cc67f2fff3',
  },
}

const definitions = [
  {
    id: 'lift-enter-exit-v1',
    title: 'Lift entry, ride handoff and exit',
    source: 'art/drafts/keeper-prime-lift-enter-2026-10-22-v1/source/generated-sheet.png',
    draftRoot: 'art/drafts/keeper-prime-lift-enter-2026-10-22-v1',
    expectedFrames: 8,
    fps: 8,
    startPose: 'walking-back',
    endPose: 'standing-front',
    authorityOverrides: { 4: 'back', 7: 'front' },
    labels: [
      'rear approach', 'rear three-quarter step', 'threshold contact', 'cross threshold',
      'ride-neutral handoff', 'turn to side', 'side exit', 'front exit endpoint',
    ],
  },
  {
    id: 'front-door-open-v1',
    title: 'Front-door approach, open and pass through',
    source: 'art/drafts/keeper-prime-front-door-2026-10-22-v1/source/generated-sheet.png',
    draftRoot: 'art/drafts/keeper-prime-front-door-2026-10-22-v1',
    expectedFrames: 6,
    fps: 8,
    startPose: 'standing-side-right',
    endPose: 'walking-side-right',
    authorityOverrides: { 0: 'sideRight' },
    labels: ['standing endpoint', 'reach', 'handle contact', 'draw door', 'leading step', 'walk handoff'],
  },
  {
    id: 'cook-counter-v1',
    title: 'Cook at counter',
    source: 'art/drafts/keeper-prime-cook-2026-10-22-v1/source/generated-sheet.png',
    draftRoot: 'art/drafts/keeper-prime-cook-2026-10-22-v1',
    expectedFrames: 8,
    fps: 8,
    startPose: 'standing-back',
    endPose: 'standing-back',
    authorityOverrides: { 0: 'back', 7: 'back' },
    labels: ['rear endpoint', 'lift right hand', 'two-hand work', 'stir inward', 'stir outward', 'steady pan', 'release', 'rear endpoint'],
  },
  {
    id: 'brush-teeth-v1',
    title: 'Brush teeth at basin',
    source: 'art/drafts/keeper-prime-brush-teeth-2026-10-22-v1/source/generated-sheet.png',
    draftRoot: 'art/drafts/keeper-prime-brush-teeth-2026-10-22-v1',
    expectedFrames: 8,
    fps: 8,
    startPose: 'standing-back',
    endPose: 'standing-back',
    authorityOverrides: { 0: 'back', 7: 'back' },
    labels: ['rear endpoint', 'raise toothbrush', 'mouth contact', 'brush inward', 'brush outward', 'repeat stroke', 'lower toothbrush', 'rear endpoint'],
  },
  {
    id: 'wave-front-v1',
    title: 'Friendly wave to camera',
    source: 'art/drafts/keeper-prime-wave-2026-10-22-v2/source/generated-sheet.png',
    draftRoot: 'art/drafts/keeper-prime-wave-2026-10-22-v2',
    expectedFrames: 6,
    fps: 8,
    startPose: 'standing-front',
    endPose: 'standing-front',
    authorityOverrides: { 0: 'front', 5: 'front' },
    labels: ['front endpoint', 'raise arm', 'present palm', 'wave inward', 'lower arm', 'front endpoint'],
  },
]

const quarantinedSources = [
  { id: 'fridge-snack-v1', title: 'Take and eat a fridge snack', path: 'art/drafts/keeper-prime-fridge-snack-2026-10-22-v1/source/generated-sheet.png', sha256: '5eff6cdc6af9db4f61dde41c4a32c1e65c1735632c5bd4b57f0a9e7ad933d304', reason: 'Adjacent source poses share opaque pixels; no frame crop or review export is permitted.' },
  { id: 'bed-day-nap-v1', title: 'Get onto bed for a daytime nap', path: 'art/drafts/keeper-prime-bed-nap-2026-10-22-v1/source/generated-sheet.png', sha256: '31b4f11616ea493592098098b63c75448c33c0ac1fe305e5054d436a9f77a08a', reason: 'The seated-to-lying source poses overlap; rerender individual poses before review.' },
  { id: 'sweep-broom-v1', title: 'Sweep with broom', path: 'art/drafts/keeper-prime-sweep-2026-10-22-v1/source/generated-sheet.png', sha256: '6bdbe8ea311f27c48c6d67935f2f5a35db0c7d460101ec49b387ab05027aee1d', reason: 'Broom/body ownership crosses source frame gaps; source is quarantined.' },
  { id: 'wave-front-v0', title: 'Friendly wave first render', path: 'art/drafts/keeper-prime-wave-2026-10-22-v1/source/generated-sheet.png', sha256: '6fbdc77b40fa395b9dd6d53063631c83cbbdb93f00d9c04f3ce1bf29f4be03c1', reason: 'Two arm poses touched; superseded by isolated six-frame V1 candidate.' },
]

function activeXRanges(image) {
  const active = Array(image.width).fill(false)
  for (let x = 0; x < image.width; x += 1) {
    for (let y = 0; y < image.height; y += 1) {
      if (image.data[(y * image.width + x) * 4 + 3] > 8) { active[x] = true; break }
    }
  }
  const ranges = []
  for (let x = 0; x < image.width; x += 1) {
    if (!active[x]) continue
    const start = x
    while (x + 1 < image.width && active[x + 1]) x += 1
    if (x - start + 1 > 8) ranges.push([start, x])
  }
  return ranges
}

function alphaBounds(image, fromX, toX) {
  let left = toX
  let right = fromX
  let top = image.height
  let bottom = -1
  for (let y = 0; y < image.height; y += 1) {
    for (let x = fromX; x <= toX; x += 1) {
      if (image.data[(y * image.width + x) * 4 + 3] <= 8) continue
      left = Math.min(left, x); right = Math.max(right, x); top = Math.min(top, y); bottom = Math.max(bottom, y)
    }
  }
  return { left, right, top, bottom, width: right - left + 1, height: bottom - top + 1 }
}

function primeColourLock(r, g, b) {
  // Preserve shading while translating the generated blue families toward the
  // measured Prime medians. Near-black contour remains black.
  if (b > 125 && b > r * 1.8 && b > g * 1.25) return [r, Math.min(255, Math.round(g * 1.27)), Math.min(255, Math.round(b * 1.16))]
  if (r > 14 && r < 105 && g > r && b > g * 1.12 && b < 155) return [Math.min(255, Math.round(r * 1.55)), Math.min(255, Math.round(g * 1.55)), Math.min(255, Math.round(b * 1.27))]
  if (r > 180 && g > 168 && b > 145 && Math.max(r, g, b) - Math.min(r, g, b) < 110) return [Math.min(255, r + 3), g, Math.max(0, b - 2)]
  return [r, g, b]
}

function samplePremultiplied(source, x, y) {
  const x0 = Math.max(0, Math.min(source.width - 1, Math.floor(x)))
  const y0 = Math.max(0, Math.min(source.height - 1, Math.floor(y)))
  const x1 = Math.min(source.width - 1, x0 + 1)
  const y1 = Math.min(source.height - 1, y0 + 1)
  const tx = x - x0
  const ty = y - y0
  const weights = [[x0, y0, (1 - tx) * (1 - ty)], [x1, y0, tx * (1 - ty)], [x0, y1, (1 - tx) * ty], [x1, y1, tx * ty]]
  let alpha = 0; let red = 0; let green = 0; let blue = 0
  for (const [sx, sy, weight] of weights) {
    const index = (sy * source.width + sx) * 4
    const a = source.data[index + 3] / 255
    alpha += a * weight
    red += source.data[index] * a * weight
    green += source.data[index + 1] * a * weight
    blue += source.data[index + 2] * a * weight
  }
  if (alpha <= 0) return [0, 0, 0, 0]
  const locked = primeColourLock(Math.round(red / alpha), Math.round(green / alpha), Math.round(blue / alpha))
  return [...locked, Math.round(alpha * 255)]
}

function normaliseFrame(source, bounds, scale) {
  const frame = new PNG({ width: 256, height: 320 })
  const targetHeight = Math.round(bounds.height * scale)
  const targetWidth = Math.round(bounds.width * scale)
  const targetLeft = Math.round((256 - targetWidth) / 2)
  const targetTop = 316 - targetHeight
  for (let y = 0; y < targetHeight; y += 1) {
    for (let x = 0; x < targetWidth; x += 1) {
      const sx = bounds.left + ((x + 0.5) / targetWidth) * bounds.width - 0.5
      const sy = bounds.top + ((y + 0.5) / targetHeight) * bounds.height - 0.5
      const rgba = samplePremultiplied(source, sx, sy)
      const target = ((targetTop + y) * frame.width + targetLeft + x) * 4
      frame.data[target] = rgba[0]; frame.data[target + 1] = rgba[1]; frame.data[target + 2] = rgba[2]; frame.data[target + 3] = rgba[3]
    }
  }
  return frame
}

function edgeAlpha(image) {
  let count = 0
  for (let x = 0; x < image.width; x += 1) {
    if (image.data[x * 4 + 3]) count += 1
    if (image.data[((image.height - 1) * image.width + x) * 4 + 3]) count += 1
  }
  for (let y = 0; y < image.height; y += 1) {
    if (image.data[(y * image.width) * 4 + 3]) count += 1
    if (image.data[(y * image.width + image.width - 1) * 4 + 3]) count += 1
  }
  return count
}

function writeOrCheck(file, bytes) {
  if (check) {
    let existing = fs.existsSync(file) ? fs.readFileSync(file) : null
    if (!existing && file.startsWith(reviewRoot)) {
      const setManifestPath = path.join(root, 'review-archive/sets', `${reviewSet}.json`)
      if (fs.existsSync(setManifestPath)) {
        const setManifest = JSON.parse(fs.readFileSync(setManifestPath, 'utf8'))
        const url = `/keeper-review/${reviewSet}/${path.relative(reviewRoot, file).split(path.sep).join('/')}`
        const archived = setManifest.entries?.[url]
        if (archived) existing = fs.readFileSync(path.join(root, archived.object))
      }
    }
    if (!existing || !existing.equals(bytes)) throw new Error(`Stale or missing generated file: ${path.relative(root, file)}`)
    return
  }
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, bytes)
}

for (const authority of Object.values(authorities)) {
  const bytes = fs.readFileSync(path.join(root, authority.path))
  if (sha256(bytes) !== authority.sha256) throw new Error(`Prime authority changed: ${authority.path}`)
}

const sequences = []
if (!check && fs.existsSync(assetRoot)) {
  for (const file of fs.readdirSync(assetRoot)) if (file.endsWith('.png')) fs.unlinkSync(path.join(assetRoot, file))
}
for (const definition of definitions) {
  const sourceBytes = fs.readFileSync(path.join(root, definition.source))
  const source = PNG.sync.read(sourceBytes)
  const ranges = activeXRanges(source)
  if (ranges.length !== definition.expectedFrames) throw new Error(`${definition.id}: expected ${definition.expectedFrames} isolated figures, found ${ranges.length}`)
  const boundsList = ranges.map((range) => alphaBounds(source, range[0], range[1]))
  const scale = Math.min(298 / boundsList[0].height, 224 / Math.max(...boundsList.map((bounds) => bounds.width)))
  if (!check) {
    const framesRoot = path.join(root, definition.draftRoot, 'frames')
    if (fs.existsSync(framesRoot)) for (const file of fs.readdirSync(framesRoot)) if (file.endsWith('.png')) fs.unlinkSync(path.join(framesRoot, file))
    const draftDirectory = path.join(root, definition.draftRoot)
    for (const file of fs.readdirSync(draftDirectory)) if (file.startsWith(`${definition.id}-`) && file.endsWith('.png')) fs.unlinkSync(path.join(draftDirectory, file))
  }
  const frames = []
  const strip = new PNG({ width: 256 * ranges.length, height: 320 })
  for (let index = 0; index < ranges.length; index += 1) {
    const bounds = boundsList[index]
    const authorityName = definition.authorityOverrides?.[index]
    const frame = authorityName
      ? PNG.sync.read(fs.readFileSync(path.join(root, authorities[authorityName].path)))
      : normaliseFrame(source, bounds, scale)
    if (edgeAlpha(frame)) throw new Error(`${definition.id} frame ${index + 1}: opaque cell edge`)
    const bytes = PNG.sync.write(frame)
    const hash = sha256(bytes)
    const fileName = `${definition.id}-frame-${String(index + 1).padStart(2, '0')}-${hash.slice(0, 16)}.png`
    writeOrCheck(path.join(root, definition.draftRoot, 'frames', fileName), bytes)
    writeOrCheck(path.join(assetRoot, fileName), bytes)
    PNG.bitblt(frame, strip, 0, 0, 256, 320, index * 256, 0)
    frames.push({
      id: `${definition.id}-f${String(index + 1).padStart(2, '0')}`,
      label: definition.labels[index],
      src: `/keeper-review/${reviewSet}/assets/${fileName}`,
      sha256: hash,
      durationMs: Math.round(1000 / definition.fps),
      cell: [256, 320],
      anchor: [128, 320],
      redraftSlot: `${definition.id}/frame-${String(index + 1).padStart(2, '0')}`,
      authorityOverride: authorityName ?? null,
    })
  }
  const stripBytes = PNG.sync.write(strip)
  const stripHash = sha256(stripBytes)
  writeOrCheck(path.join(root, definition.draftRoot, `${definition.id}-${stripHash.slice(0, 16)}.png`), stripBytes)
  sequences.push({
    id: definition.id,
    title: definition.title,
    status: 'unapproved-versioned-draft',
    source: { path: definition.source, sha256: sha256(sourceBytes) },
    draftStrip: { path: `${definition.draftRoot}/${definition.id}-${stripHash.slice(0, 16)}.png`, sha256: stripHash },
    fps: definition.fps,
    startPose: definition.startPose,
    endPose: definition.endPose,
    frames,
  })
}

const manifest = {
  schema: 'lighthouse-keeper/prime-animation-draft-batch@1',
  version: 1,
  generatedOn: '2026-10-22',
  status: 'review-only-unapproved',
  note: 'Canonical Prime and prior approved animation sources are immutable. Rejecting any candidate requires deleting only its named versioned draft directory; every frame can be regenerated independently through its stable redraft slot.',
  dimensions: { logicalCell: [32, 40], authoringCell: [256, 320], scale: 8, anchor: [128, 320], capTop: 18, floorOpaqueY: 316 },
  colourLock: { jumperBlue: [0, 108, 230], jumperCream: [251, 232, 206], trousers: [63, 75, 112], boots: [63, 74, 111] },
  canonicalAuthorities: authorities,
  quarantinedSources,
  sequences,
}
const manifestBytes = Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`)
writeOrCheck(path.join(reviewRoot, 'batch.json'), manifestBytes)
writeOrCheck(path.join(root, 'data/keeper_prime_animation_drafts_v1.json'), manifestBytes)

console.log(`${check ? 'Verified' : 'Wrote'} Prime morning draft V1: ${sequences.length} sequences, ${sequences.reduce((sum, item) => sum + item.frames.length, 0)} isolated redraftable frames.`)
