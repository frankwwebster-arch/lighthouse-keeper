import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const authorityRoot = path.join(root, 'art/drafts/kitchen-warm-ligne-claire-family-2026-10-24-v4')
const authorityManifest = JSON.parse(fs.readFileSync(path.join(authorityRoot, 'manifest.json'), 'utf8'))
const draftRoot = path.join(root, 'art/drafts/kitchen-runtime-promotion-2026-10-24-v1')
const rawRoot = path.join(root, 'art/raw/kitchen-warm-ligne-claire-runtime-v1')
const publicRoot = path.join(root, 'public/sprites/kitchen-v4')
const promotionPath = path.join(root, 'data/kitchen_runtime_promotion_v1.json')
const check = process.argv.includes('--check')
const modules = ['cupboard', 'drawers', 'sink', 'dishwasher', 'oven', 'fridge']
const states = ['off', 'on', 'broken']

const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const relative = file => path.relative(root, file)

const definitions = []
for (const state of states) {
  for (const name of modules) {
    definitions.push({
      id: `${name}-${state}`,
      source: path.join(authorityRoot, 'candidates', state, `${name}-${state}-84x74.png`),
      delivery: path.join(state, `${name}-${state}-84x74.png`),
      size: [84, 74],
      role: 'fitted-body',
    })
  }
}
definitions.push(
  {
    id: 'dishwasher-broken-red-lights',
    source: path.join(authorityRoot, 'candidates/dishwasher-broken-red-lights-f40.png'),
    delivery: 'dishwasher-broken-red-lights-f40.png',
    size: [92 * 40, 82],
    role: 'light-only-animation',
    frames: 40,
    fps: 4,
    cell: [92, 82],
  },
  {
    id: 'oven-broken-cavity-light',
    source: path.join(authorityRoot, 'candidates/oven-broken-cavity-light-f40.png'),
    delivery: 'oven-broken-cavity-light-f40.png',
    size: [92 * 40, 82],
    role: 'light-only-animation',
    frames: 40,
    fps: 4,
    cell: [92, 82],
  },
)

const expected = new Map()
const assets = definitions.map(definition => {
  const bytes = fs.readFileSync(definition.source)
  const image = PNG.sync.read(bytes)
  assert.deepEqual([image.width, image.height], definition.size, `${definition.id} geometry drift`)
  const hash = sha256(bytes)
  if (definition.role === 'fitted-body') {
    const [name, state] = definition.id.split('-')
    assert.equal(hash, authorityManifest.states[state][name], `${definition.id} authority hash drift`)
  } else {
    const record = definition.id.startsWith('dishwasher') ? authorityManifest.animation.dishwasher : authorityManifest.animation.oven
    assert.equal(hash, record.sha256, `${definition.id} authority hash drift`)
    for (let frame = 0; frame < definition.frames; frame += 1) {
      const x0 = frame * definition.cell[0]
      for (let x = 0; x < definition.cell[0]; x += 1) {
        assert.equal(image.data[((0 * image.width) + x0 + x) * 4 + 3], 0, `${definition.id} frame ${frame} touches top edge`)
        assert.equal(image.data[(((definition.cell[1] - 1) * image.width) + x0 + x) * 4 + 3], 0, `${definition.id} frame ${frame} touches bottom edge`)
      }
      for (let y = 0; y < definition.cell[1]; y += 1) {
        assert.equal(image.data[(y * image.width + x0) * 4 + 3], 0, `${definition.id} frame ${frame} touches left edge`)
        assert.equal(image.data[(y * image.width + x0 + definition.cell[0] - 1) * 4 + 3], 0, `${definition.id} frame ${frame} touches right edge`)
      }
    }
  }
  const draft = path.join(draftRoot, 'assets', definition.delivery)
  const raw = path.join(rawRoot, definition.delivery)
  const publicFile = path.join(publicRoot, definition.delivery)
  expected.set(draft, bytes)
  expected.set(raw, bytes)
  expected.set(publicFile, bytes)
  return {
    id: definition.id,
    role: definition.role,
    state: definition.role === 'fitted-body' ? definition.id.split('-').at(-1) : 'broken',
    dimensions: definition.size,
    ...(definition.frames ? { frames: definition.frames, fps: definition.fps, cell: definition.cell } : {}),
    authority: relative(definition.source),
    authoritySha256: hash,
    draft: relative(draft),
    draftSha256: hash,
    productionSource: relative(raw),
    productionSourceSha256: hash,
    publicSprite: relative(publicFile),
    publicSpriteSha256: hash,
  }
})

const legacyRoom = path.join(root, 'public/sprites/room_kitchen.png')
const legacyRoomHash = sha256(fs.readFileSync(legacyRoom))
const promotion = {
  schema: 'lighthouse-keeper/kitchen-runtime-promotion@1',
  version: 1,
  promotedOn: '2026-10-24',
  status: 'production',
  authority: 'kitchen-warm-ligne-claire-family-2026-10-24-v4',
  approval: 'Frank approved Warm Ligne-Claire Family V4 and explicitly requested runtime wiring.',
  roomRegistration: {
    approvedCoordinateSystem: [772, 224],
    fittedBodySize: [84, 74],
    fittedBayOriginsX: [84, 168, 252, 336, 420, 504],
    fittedBayCentresX: [126, 210, 294, 378, 462, 546],
    bodyY: 134,
    floorSupportY: 208,
    keeperStopTurnY: 218,
    runtimeViewport: { towerLocalX: 48, width: 420, uniformScale: 420 / 772 },
    policy: 'The complete approved coordinate system receives one uniform outer presentation transform; individual 84 x 74 bodies are never resized, cropped, reordered or independently transformed.',
  },
  liveBindings: {
    component: 'src/ui/KitchenRoom.tsx',
    cooker: { module: 'oven', standard: 'off', active: 'on', broken: 'broken' },
    fridge: { module: 'fridge', standard: 'off', active: 'on', broken: 'broken' },
    staticModules: { cupboard: 'off', drawers: 'off', sink: 'off', dishwasher: 'off' },
    brokenAnimations: { dishwasher: 'three independent red lenses only', oven: 'internal cavity light only' },
    gameplayPolicy: 'Existing object IDs, commands, need effects, timings, fault/repair state, saves, tiers and hit-area behavior are unchanged.',
  },
  rollback: {
    retainedLegacyRoom: relative(legacyRoom),
    retainedLegacyRoomSha256: legacyRoomHash,
    boundary: 'Remove the KitchenRoom binding and this named V1 draft/raw/public family to return to the retained room_kitchen plate; the approved V4 authority and every unrelated sprite remain untouched.',
  },
  assets,
}
const promotionBytes = Buffer.from(`${JSON.stringify(promotion, null, 2)}\n`)
const registerBytes = Buffer.from(`${JSON.stringify({
  schema: 'lighthouse-keeper/kitchen-runtime-promotion-register@1',
  version: 1,
  generatedOn: '2026-10-24',
  sourceAuthority: relative(authorityRoot),
  reversibleDraft: relative(draftRoot),
  productionSource: relative(rawRoot),
  publicDelivery: relative(publicRoot),
  legacyRoom: { path: relative(legacyRoom), sha256: legacyRoomHash, overwritten: false },
  canonicalPolicy: promotion.rollback.boundary,
  assets: assets.map(asset => ({ id: asset.id, authority: asset.authority, authoritySha256: asset.authoritySha256, draft: asset.draft, draftSha256: asset.draftSha256, productionSource: asset.productionSource, productionSourceSha256: asset.productionSourceSha256, publicSprite: asset.publicSprite, publicSpriteSha256: asset.publicSpriteSha256 })),
}, null, 2)}\n`)
expected.set(promotionPath, promotionBytes)
expected.set(path.join(draftRoot, 'batch-register.json'), registerBytes)

if (check) {
  for (const [file, bytes] of expected) {
    assert.ok(fs.existsSync(file), `Kitchen runtime file missing: ${relative(file)}`)
    assert.ok(fs.readFileSync(file).equals(bytes), `Kitchen runtime file stale: ${relative(file)}`)
  }
  const contract = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_asset_contract_v1.json'), 'utf8'))
  assert.equal(contract.packaging.runtimePromoted, true, 'authority contract does not record runtime promotion')
  assert.equal(contract.packaging.runtimePromotion, 'data/kitchen_runtime_promotion_v1.json')
  const roomSource = fs.readFileSync(path.join(root, 'src/ui/KitchenRoom.tsx'), 'utf8')
  assert.match(roomSource, /data-kitchen-runtime="warm-ligne-claire-v4"/)
  assert.match(roomSource, /moduleState === 'broken'/)
  const sceneSource = fs.readFileSync(path.join(root, 'src/ui/Scene.tsx'), 'utf8')
  assert.match(sceneSource, /o\.id === 'fridge' \|\| o\.id === 'cooker'/)
  console.log(`Kitchen runtime V1 verified: ${assets.length} byte-identical assets, exact 84x74 grid, reversible legacy boundary.`)
} else {
  for (const [file, bytes] of expected) {
    fs.mkdirSync(path.dirname(file), { recursive: true })
    fs.writeFileSync(file, bytes)
  }
  console.log(`Kitchen runtime V1 built: ${assets.length} byte-identical assets.`)
}
