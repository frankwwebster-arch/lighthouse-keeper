import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const cataloguePath = path.join(root, 'public/prime-keeper-animations/catalogue.json')
const draftRoot = path.join(root, 'art/drafts/keeper-prime-runtime-promotion-2026-10-22-v1')
const draftAssetRoot = path.join(draftRoot, 'runtime')
const rawRoot = path.join(root, 'art/raw/keeper-prime-runtime-v1')
const bankPath = path.join(root, 'data/keeper_prime_runtime_bank.json')
const publicRoot = path.join(root, 'public/sprites')
const manifestPath = path.join(publicRoot, 'manifest.json')
const check = process.argv.includes('--check')

const catalogue = JSON.parse(fs.readFileSync(cataloguePath, 'utf8'))
const clipMap = new Map(catalogue.clips.map((clip) => [clip.id, clip]))
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')

function frameRange(from, to) {
  return Array.from({ length: to - from + 1 }, (_, index) => from + index)
}

const definitions = [
  { id: 'neutral-side-right', sprite: 'keeper_prime_neutral_standing-side-right', clip: 'stop-walk-stop-v2', indices: [0], fps: 0, loop: false, startPose: 'standing-side-right', endPose: 'standing-side-right', facing: 'right', mirrorSafe: true, role: 'neutral' },
  { id: 'neutral-front', sprite: 'keeper_prime_neutral_standing-front', clip: 'turn-front-side-v1', indices: [0], fps: 0, loop: false, startPose: 'standing-front', endPose: 'standing-front', facing: 'front', mirrorSafe: false, role: 'neutral' },
  { id: 'neutral-back', sprite: 'keeper_prime_neutral_standing-back', clip: 'turn-side-back-v10', indices: [8], fps: 0, loop: false, startPose: 'standing-back', endPose: 'standing-back', facing: 'back', mirrorSafe: false, role: 'neutral' },
  { id: 'walk-side-cycle', sprite: 'keeper_prime_walk_side_cycle', clip: 'walk-v7', indices: frameRange(0, 7), fps: 10, loop: true, startPose: 'walking-side-right', endPose: 'walking-side-right', facing: 'right', mirrorSafe: true, role: 'clip' },
  { id: 'walk-side-start', sprite: 'keeper_prime_walk_side_start', clip: 'stop-walk-stop-v2', indices: frameRange(3, 7), fps: 10, loop: false, startPose: 'standing-side-right', endPose: 'walking-side-right', facing: 'right', mirrorSafe: true, role: 'bridge' },
  { id: 'walk-side-stop', sprite: 'keeper_prime_walk_side_stop', clip: 'stop-walk-stop-v2', indices: frameRange(23, 27), fps: 12, loop: false, startPose: 'walking-side-right', endPose: 'standing-side-right', facing: 'right', mirrorSafe: true, role: 'bridge' },
  { id: 'turn-front-to-side-right', sprite: 'keeper_prime_turn_front_to_side-right', clip: 'turn-front-side-v1', indices: frameRange(0, 7), fps: 16, loop: false, startPose: 'standing-front', endPose: 'standing-side-right', facing: 'turning-right', mirrorSafe: true, role: 'bridge' },
  { id: 'turn-side-right-to-front', sprite: 'keeper_prime_turn_side-right_to_front', clip: 'turn-front-side-v1', indices: frameRange(0, 7).reverse(), fps: 16, loop: false, startPose: 'standing-side-right', endPose: 'standing-front', facing: 'turning-front', mirrorSafe: true, role: 'bridge' },
  { id: 'turn-side-right-to-back', sprite: 'keeper_prime_turn_side-right_to_back', clip: 'turn-side-back-v10', indices: frameRange(0, 8), fps: 16, loop: false, startPose: 'standing-side-right', endPose: 'standing-back', facing: 'turning-back', mirrorSafe: true, role: 'bridge' },
  { id: 'turn-back-to-side-right', sprite: 'keeper_prime_turn_back_to_side-right', clip: 'turn-side-back-v10', indices: frameRange(0, 8).reverse(), fps: 16, loop: false, startPose: 'standing-back', endPose: 'standing-side-right', facing: 'turning-right', mirrorSafe: true, role: 'bridge' },
  { id: 'stairs-up', sprite: 'keeper_prime_stairs_up', clip: 'stair-ascent-v16', indices: frameRange(0, 26), fps: 1000 / 110, loop: false, startPose: 'stair-lower-contact', endPose: 'stair-upper-contact', facing: 'right-up', mirrorSafe: false, role: 'clip' },
  { id: 'stairs-down', sprite: 'keeper_prime_stairs_down', clip: 'stair-descent-v2', indices: frameRange(16, 42), fps: 1000 / 110, loop: false, startPose: 'stair-upper-contact', endPose: 'stair-lower-contact', facing: 'right-down', mirrorSafe: false, role: 'clip' },
  { id: 'ladder-climb', sprite: 'keeper_prime_ladder_climb', clip: 'ladder-route-v5', select: (frame) => frame.phase?.startsWith('climb one exact floor') || frame.phase === 'right boot clears the ladder opening', fps: 1000 / 150, loop: false, startPose: 'climbing-back-lower', endPose: 'climbing-back-upper', facing: 'back', mirrorSafe: false, role: 'clip' },
  { id: 'sit-side-right', sprite: 'keeper_prime_sit_side-right', clip: 'sit-side-right-v6', indices: frameRange(0, 5), fps: 8, loop: false, startPose: 'standing-side-right', endPose: 'sitting-side-right', facing: 'right', mirrorSafe: false, role: 'bridge' },
  { id: 'stand-side-right', sprite: 'keeper_prime_stand_side-right', clip: 'sit-side-right-v6', indices: frameRange(0, 5).reverse(), fps: 8, loop: false, startPose: 'sitting-side-right', endPose: 'standing-side-right', facing: 'right', mirrorSafe: false, role: 'bridge' },
  { id: 'sit-side-left', sprite: 'keeper_prime_sit_side-left', clip: 'sit-side-left-v1', indices: frameRange(0, 5), fps: 8, loop: false, startPose: 'standing-side-left', endPose: 'sitting-side-left', facing: 'left', mirrorSafe: false, role: 'bridge' },
  { id: 'stand-side-left', sprite: 'keeper_prime_stand_side-left', clip: 'sit-side-left-v1', indices: frameRange(0, 5).reverse(), fps: 8, loop: false, startPose: 'sitting-side-left', endPose: 'standing-side-left', facing: 'left', mirrorSafe: false, role: 'bridge' },
  { id: 'sit-front', sprite: 'keeper_prime_sit_front', clip: 'sit-front-v4', indices: frameRange(0, 5), fps: 8, loop: false, startPose: 'standing-front', endPose: 'sitting-front', facing: 'front', mirrorSafe: false, role: 'bridge' },
  { id: 'stand-front', sprite: 'keeper_prime_stand_front', clip: 'sit-front-v4', indices: frameRange(0, 5).reverse(), fps: 8, loop: false, startPose: 'sitting-front', endPose: 'standing-front', facing: 'front', mirrorSafe: false, role: 'bridge' },
  { id: 'sit-back', sprite: 'keeper_prime_sit_back', clip: 'sit-back-v2', indices: frameRange(0, 5), fps: 8, loop: false, startPose: 'standing-back', endPose: 'sitting-back', facing: 'back', mirrorSafe: false, role: 'bridge' },
  { id: 'stand-back', sprite: 'keeper_prime_stand_back', clip: 'sit-back-v2', indices: frameRange(0, 5).reverse(), fps: 8, loop: false, startPose: 'sitting-back', endPose: 'standing-back', facing: 'back', mirrorSafe: false, role: 'bridge' },
  { id: 'neutral-sitting-side-right', sprite: 'keeper_prime_neutral_sitting-side-right', clip: 'sit-side-right-v6', indices: [5], fps: 0, loop: false, startPose: 'sitting-side-right', endPose: 'sitting-side-right', facing: 'right', mirrorSafe: false, role: 'neutral' },
  { id: 'neutral-sitting-side-left', sprite: 'keeper_prime_neutral_sitting-side-left', clip: 'sit-side-left-v1', indices: [5], fps: 0, loop: false, startPose: 'sitting-side-left', endPose: 'sitting-side-left', facing: 'left', mirrorSafe: false, role: 'neutral' },
  { id: 'neutral-sitting-front', sprite: 'keeper_prime_neutral_sitting-front', clip: 'sit-front-v4', indices: [5], fps: 0, loop: false, startPose: 'sitting-front', endPose: 'sitting-front', facing: 'front', mirrorSafe: false, role: 'neutral' },
  { id: 'neutral-sitting-back', sprite: 'keeper_prime_neutral_sitting-back', clip: 'sit-back-v2', indices: [5], fps: 0, loop: false, startPose: 'sitting-back', endPose: 'sitting-back', facing: 'back', mirrorSafe: false, role: 'neutral' },
  { id: 'darts-throw', sprite: 'keeper_prime_darts_throw', clip: 'darts-context-v8', select: (frame) => frame.phase?.startsWith('set 1 · dart 1'), w: 56, fps: 14 / 2.245, loop: true, startPose: 'standing-side-right', endPose: 'standing-side-right', facing: 'right', mirrorSafe: false, role: 'clip' },
  { id: 'rear-work', sprite: 'keeper_prime_rear_work', clip: 'rear-action-v1', select: (frame) => frame.phase === 'Prime rear-work action', fps: 4, loop: true, startPose: 'standing-back', endPose: 'standing-back', facing: 'back', mirrorSafe: false, role: 'clip' },
]

function resolveFrame(src) {
  if (!src.startsWith('/keeper-review/')) throw new Error(`Unsupported frame URL: ${src}`)
  const parts = src.split('/').filter(Boolean)
  const set = parts[1]
  const publicPath = path.join(root, 'public', ...parts)
  if (fs.existsSync(publicPath)) return { path: publicPath, sha256: sha256(fs.readFileSync(publicPath)) }
  const manifestPath = path.join(root, 'review-archive/sets', `${set}.json`)
  if (!fs.existsSync(manifestPath)) throw new Error(`No archive manifest for ${src}`)
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'))
  const entry = manifest.entries[src]
  if (!entry) throw new Error(`No archive entry for ${src}`)
  return { path: path.join(root, entry.object), sha256: entry.sha256 }
}

function flipHorizontal(image) {
  const out = new PNG({ width: image.width, height: image.height })
  for (let y = 0; y < image.height; y += 1) {
    for (let x = 0; x < image.width; x += 1) {
      const source = (y * image.width + (image.width - 1 - x)) * 4
      const target = (y * image.width + x) * 4
      image.data.copy(out.data, target, source, source + 4)
    }
  }
  return out
}

function downsampleHalf(image, logicalWidth) {
  const sourceWidth = logicalWidth * 8
  const outputWidth = logicalWidth * 4
  if (image.width !== sourceWidth || image.height !== 320) throw new Error(`Expected a ${sourceWidth}x320 registered Prime frame, got ${image.width}x${image.height}`)
  const out = new PNG({ width: outputWidth, height: 160 })
  for (let y = 0; y < out.height; y += 1) {
    for (let x = 0; x < out.width; x += 1) {
      let alpha = 0
      let red = 0
      let green = 0
      let blue = 0
      for (let oy = 0; oy < 2; oy += 1) {
        for (let ox = 0; ox < 2; ox += 1) {
          const source = (((y * 2) + oy) * image.width + (x * 2) + ox) * 4
          const a = image.data[source + 3]
          alpha += a
          red += image.data[source] * a
          green += image.data[source + 1] * a
          blue += image.data[source + 2] * a
        }
      }
      const target = (y * out.width + x) * 4
      out.data[target + 3] = Math.round(alpha / 4)
      if (alpha > 0) {
        out.data[target] = Math.round(red / alpha)
        out.data[target + 1] = Math.round(green / alpha)
        out.data[target + 2] = Math.round(blue / alpha)
      }
    }
  }
  return out
}

function compose(frames, logicalWidth) {
  const cellWidth = logicalWidth * 4
  const strip = new PNG({ width: cellWidth * frames.length, height: 160 })
  frames.forEach((frame, index) => {
    const decoded = PNG.sync.read(fs.readFileSync(frame.local.path))
    const oriented = frame.flipX ? flipHorizontal(decoded) : decoded
    const rendered = downsampleHalf(oriented, logicalWidth)
    PNG.bitblt(rendered, strip, 0, 0, rendered.width, rendered.height, index * rendered.width, 0)
  })
  return PNG.sync.write(strip)
}

function hardAlpha(bytes) {
  const image = PNG.sync.read(bytes)
  for (let index = 0; index < image.data.length; index += 4) {
    if (image.data[index + 3] >= 128) image.data[index + 3] = 255
    else image.data.fill(0, index, index + 4)
  }
  return PNG.sync.write(image)
}

function selectedFrames(definition) {
  const source = clipMap.get(definition.clip)
  if (!source) throw new Error(`Unknown approved clip: ${definition.clip}`)
  const selected = definition.indices
    ? definition.indices.map((index) => source.frames[index])
    : source.frames.filter(definition.select)
  if (!selected.length || selected.some((frame) => !frame)) throw new Error(`${definition.id} selected no valid frames`)
  return selected.map((frame) => ({ ...frame, local: resolveFrame(frame.src) }))
}

function countSharedEdgeAlpha(image) {
  let count = 0
  for (let y = 0; y < image.height; y += 1) {
    if (image.data[(y * image.width) * 4 + 3] !== 0) count += 1
    if (image.data[(y * image.width + image.width - 1) * 4 + 3] !== 0) count += 1
  }
  return count
}

const outputs = []
for (const definition of definitions) {
  const selected = selectedFrames(definition)
  const file = `${definition.sprite}_f${selected.length}.png`
  const sidecarFile = file.replace(/\.png$/, '.json')
  const logicalWidth = definition.w ?? 32
  const cellWidth = logicalWidth * 4
  const bytes = compose(selected, logicalWidth)
  const decoded = PNG.sync.read(bytes)
  let sharedEdgeAlpha = 0
  for (let frame = 0; frame < selected.length; frame += 1) {
    const cell = new PNG({ width: cellWidth, height: 160 })
    PNG.bitblt(decoded, cell, frame * cellWidth, 0, cellWidth, 160, 0, 0)
    sharedEdgeAlpha += countSharedEdgeAlpha(cell)
  }
  if (sharedEdgeAlpha !== 0) throw new Error(`${definition.id} has ${sharedEdgeAlpha} opaque cell-edge pixels`)
  const outputHash = sha256(bytes)
  const publicBytes = hardAlpha(bytes)
  const publicHash = sha256(publicBytes)
  const sidecar = {
    schema: 'lighthouse-keeper/prime-runtime-sprite@1',
    name: definition.sprite,
    w: logicalWidth,
    h: 40,
    density: 4,
    frames: selected.length,
    fps: definition.fps,
    anchor: [16, 40],
    startPose: definition.startPose,
    endPose: definition.endPose,
    assetRole: definition.role,
    outfit: 'standard',
    loop: definition.loop,
    mirrorSafe: definition.mirrorSafe,
    facing: definition.facing,
    productionPromotionApprovedOn: '2026-10-22',
    derivation: 'deterministic 2x premultiplied-alpha box reduction from exact approved 256x320 review frames; frame order is unchanged except for declared reversible clips',
    approvedClipId: definition.clip,
    sourceFrames: selected.map((frame) => ({ url: frame.src, sha256: frame.local.sha256, flipX: Boolean(frame.flipX) })),
    sha256: outputHash,
  }
  const sidecarBytes = Buffer.from(`${JSON.stringify(sidecar, null, 2)}\n`)
  outputs.push({ ...definition, logicalWidth, selected, file, sidecarFile, publicFile: `${definition.sprite}.png`, bytes, publicBytes, sidecarBytes, sha256: outputHash, publicSha256: publicHash, sharedEdgeAlpha })
}

const bank = {
  schema: 'lighthouse-keeper/prime-runtime-animation-bank@1',
  version: 1,
  generatedOn: '2026-10-22',
  status: 'production',
  approval: 'Frank: “go ahead” after the runtime-promotion boundary was explained',
  deliveryScale: { density: 4, standardLogicalCell: [32, 40], standardPixelCell: [128, 160], transform: '2x premultiplied-alpha box reduction from approved 8px-per-logical-pixel frames' },
  activeBindings: {
    idle: 'keeper_prime_neutral_standing-side-right',
    walkStart: 'keeper_prime_walk_side_start',
    walk: 'keeper_prime_walk_side_cycle',
    walkStop: 'keeper_prime_walk_side_stop',
    stairsUp: 'keeper_prime_stairs_up',
    stairsDown: 'keeper_prime_stairs_down',
    rearWork: 'keeper_prime_rear_work',
  },
  installedButAwaitingAConsumer: outputs.filter((entry) => !['neutral-side-right', 'walk-side-start', 'walk-side-cycle', 'walk-side-stop', 'stairs-up', 'stairs-down', 'rear-work'].includes(entry.id)).map((entry) => entry.sprite),
  assets: outputs.map((entry) => ({
    id: entry.id,
    sprite: entry.sprite,
    file: entry.file,
    publicFile: entry.publicFile,
    w: entry.logicalWidth,
    h: 40,
    frames: entry.selected.length,
    fps: entry.fps,
    loop: entry.loop,
    startPose: entry.startPose,
    endPose: entry.endPose,
    approvedClipId: entry.clip,
    sourceStripSha256: entry.sha256,
    publicSha256: entry.publicSha256,
    sourceFrameSha256: entry.selected.map((frame) => frame.local.sha256),
    transparentCellEdges: entry.sharedEdgeAlpha === 0,
  })),
}

const register = {
  schema: 'lighthouse-keeper/prime-runtime-promotion-register@1',
  version: 1,
  generatedOn: '2026-10-22',
  reversibleDraft: path.relative(root, draftRoot),
  productionSource: path.relative(root, rawRoot),
  canonicalPolicy: 'Existing approved review frames and legacy runtime sheets are not overwritten. Rejecting this promotion removes only the named V1 draft/raw files, their generated public sprites, bank record and bindings.',
  assets: outputs.map((entry) => ({
    id: entry.id,
    originalFrameSha256: entry.selected.map((frame) => frame.local.sha256),
    draft: `runtime/${entry.file}`,
    draftSha256: entry.sha256,
    productionSource: `art/raw/keeper-prime-runtime-v1/${entry.file}`,
    productionSourceSha256: entry.sha256,
    publicSprite: `public/sprites/${entry.publicFile}`,
    publicSpriteSha256: entry.publicSha256,
    transparentCellEdges: entry.sharedEdgeAlpha === 0,
  })),
}

const expected = new Map()
for (const entry of outputs) {
  expected.set(path.join(draftAssetRoot, entry.file), entry.bytes)
  expected.set(path.join(draftAssetRoot, entry.sidecarFile), entry.sidecarBytes)
  expected.set(path.join(rawRoot, entry.file), entry.bytes)
  expected.set(path.join(rawRoot, entry.sidecarFile), entry.sidecarBytes)
  expected.set(path.join(publicRoot, entry.publicFile), entry.publicBytes)
}
expected.set(bankPath, Buffer.from(`${JSON.stringify(bank, null, 2)}\n`))
expected.set(path.join(draftRoot, 'batch-register.json'), Buffer.from(`${JSON.stringify(register, null, 2)}\n`))

if (check) {
  for (const [file, bytes] of expected) {
    if (!fs.existsSync(file) || !fs.readFileSync(file).equals(bytes)) {
      console.error(`Prime runtime promotion is stale: ${path.relative(root, file)}`)
      process.exit(1)
    }
  }
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'))
  for (const entry of outputs) {
    const expectedEntry = {
      file: entry.publicFile,
      w: entry.logicalWidth,
      h: 40,
      frames: entry.selected.length,
      ...(entry.fps > 0 ? { fps: entry.fps } : {}),
      density: 4,
      anchor: [16, 40],
      startPose: entry.startPose,
      endPose: entry.endPose,
      assetRole: entry.role,
      outfit: 'standard',
      loop: entry.loop,
      mirrorSafe: entry.mirrorSafe,
      facing: entry.facing,
      z: 50,
    }
    if (JSON.stringify(manifest[entry.sprite]) !== JSON.stringify(expectedEntry)) {
      console.error(`Prime runtime manifest entry is stale: ${entry.sprite}`)
      process.exit(1)
    }
  }
  console.log(`Prime runtime V1 verified: ${outputs.length} sprites, ${outputs.reduce((sum, entry) => sum + entry.selected.length, 0)} registered frames, zero shared-edge alpha.`)
} else {
  fs.mkdirSync(draftAssetRoot, { recursive: true })
  fs.mkdirSync(rawRoot, { recursive: true })
  for (const [file, bytes] of expected) {
    fs.mkdirSync(path.dirname(file), { recursive: true })
    fs.writeFileSync(file, bytes)
  }
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'))
  for (const entry of outputs) {
    manifest[entry.sprite] = {
      file: entry.publicFile,
      w: entry.logicalWidth,
      h: 40,
      frames: entry.selected.length,
      ...(entry.fps > 0 ? { fps: entry.fps } : {}),
      density: 4,
      anchor: [16, 40],
      startPose: entry.startPose,
      endPose: entry.endPose,
      assetRole: entry.role,
      outfit: 'standard',
      loop: entry.loop,
      mirrorSafe: entry.mirrorSafe,
      facing: entry.facing,
      z: 50,
    }
  }
  fs.writeFileSync(manifestPath, `${JSON.stringify(Object.fromEntries(Object.entries(manifest).sort(([left], [right]) => left.localeCompare(right))), null, 1)}\n`)
  console.log(`Wrote Prime runtime V1: ${outputs.length} sprites, ${outputs.reduce((sum, entry) => sum + entry.selected.length, 0)} registered frames.`)
}
