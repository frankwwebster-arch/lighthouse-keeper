import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const alpha = (image, x, y) => image.data[(y * image.width + x) * 4 + 3]
const specs = {
  kettle: { version: 33, dir: 'kitchen-kettle-states-2026-10-18-v33', source: 'kettle-three-state-source-v1.png', sourceSha: 'f935e112d0d5fc43536762fb528fbff0fd3121733434aea2936d5b4e428b4b54', states: ['standard', 'on', 'broken'], cell: [84, 68], effects: ['small_steam'], sfx: ['kitchen_kettle_heating_hiss_loop', 'kitchen_kettle_broken_handle_rattle'], requirements: { smallSteamFromSpout: true, steamSeparate: true, brokenHandleMountFailed: true, brokenHandleAttached: true, visibleElectricalEffects: false } },
  toaster: { version: 34, dir: 'kitchen-toaster-states-2026-10-18-v34', source: 'toaster-three-state-source-v1.png', sourceSha: '72c4336829f4bb6da2ff71283e2c0a4c4b9f026692b3e6e2df5bec6af307402b', states: ['standard', 'on', 'broken'], cell: [84, 68], effects: ['restrained_heat'], sfx: ['kitchen_toaster_heating_hum_loop', 'kitchen_toaster_jammed_click'], requirements: { onBreadTopsVisible: true, heatSeparate: true, brokenBreadJammed: true, visibleFlames: false, visibleElectricalEffects: false } },
  oven: { version: 35, dir: 'kitchen-oven-states-2026-10-18-v35', source: 'oven-three-state-source-v1.png', sourceSha: '6468b44c8a3e3aa5e8a87c2c97020bc2cded221de40bf9bb00bf65a75ee2bfaf', states: ['standard', 'on', 'broken'], cell: [92, 96], effects: ['billowing_smoke', 'hob_flames'], sfx: ['kitchen_oven_on_fan_loop', 'kitchen_oven_broken_smoke_hiss_loop', 'kitchen_oven_hob_flame_loop'], requirements: { standardInteriorLight: false, onInteriorLight: true, onDialsTurned: true, onRedIndicator: true, onRoastingTin: true, brokenDoorAskew: true, smokeSeparate: true, hobFlamesSeparate: true } },
  'mixing-bowl': { version: 36, dir: 'kitchen-mixing-bowl-states-2026-10-18-v36', source: 'mixing-bowl-two-state-source-v1.png', sourceSha: '700f66771ef1ce63c5ef293066e9512d32db338f5932a2a0966be1129514e6e6', states: ['standard', 'broken'], cell: [84, 68], effects: [], sfx: ['kitchen_mixing_bowl_ceramic_break'], requirements: { animationRequired: false, brokenLargeCeramicPieces: true, intactTableauBeneathBroken: false } },
  basin: { version: 37, dir: 'kitchen-basin-states-2026-10-18-v37', source: 'basin-three-state-source-v1.png', sourceSha: '9518bc62fcd36704d59b3993d5d1719c984d07f43a8e64b019638adff0cedacc', states: ['standard', 'on', 'broken'], cell: [92, 112], effects: ['gentle_flow', 'upward_spray'], sfx: ['kitchen_basin_gentle_flow_loop', 'kitchen_basin_broken_spray_loop'], requirements: { standardWaterRunning: false, onGentleFlow: true, onFlowSeparate: true, brokenTapCracked: true, brokenUpwardSpraySeparate: true } },
  table: { version: 38, dir: 'kitchen-table-states-2026-10-18-v38', source: 'table-two-state-source-v1.png', sourceSha: 'd5d34dd002c9f14f6d0585026ff9f2c61baecb639a6c9325cf8b543e7ec8872f', states: ['standard', 'broken'], cell: [104, 96], effects: [], sfx: ['kitchen_table_broken_creak'], requirements: { animationRequired: false, brokenLegPartlyAttached: true, brokenFootFloorContact: true, intactTableBeneathBroken: false } },
}

const assertGutter = (image, label, x0 = 0, width = image.width) => {
  for (let x = 0; x < width; x++) {
    assert.equal(alpha(image, x0 + x, 0), 0, `${label} touches top edge`)
    assert.equal(alpha(image, x0 + x, image.height - 1), 0, `${label} touches bottom edge`)
  }
  for (let y = 0; y < image.height; y++) {
    assert.equal(alpha(image, x0, y), 0, `${label} touches left edge`)
    assert.equal(alpha(image, x0 + width - 1, y), 0, `${label} touches right edge`)
  }
}

for (const [asset, spec] of Object.entries(specs)) {
  const source = path.join(root, 'art/source', spec.dir, 'generated', spec.source)
  const rawDir = path.join(root, 'art/raw', spec.dir)
  const draftDir = path.join(root, 'art/drafts', spec.dir)
  const route = `kitchen-${asset}-states-v${spec.version}`
  const pageFile = path.join(root, 'public/keeper-review', route, 'index.html')
  assert.equal(sha(source), spec.sourceSha, `${asset} coordinated source changed`)
  const catalogue = JSON.parse(fs.readFileSync(path.join(draftDir, 'candidate-catalogue.json'), 'utf8'))
  const register = JSON.parse(fs.readFileSync(path.join(draftDir, 'batch-register.json'), 'utf8'))
  assert.equal(catalogue.version, spec.version)
  assert.equal(catalogue.asset, asset)
  assert.equal(catalogue.status, 'awaiting-visual-review')
  assert.deepEqual(catalogue.states, spec.states)
  assert.deepEqual(catalogue.cellPixels, spec.cell)
  assert.deepEqual(catalogue.roomPixels, [772, 224])
  assert.deepEqual(catalogue.requirements, spec.requirements)
  assert.deepEqual(catalogue.sfxCues, spec.sfx)
  assert.deepEqual(catalogue.construction, { coordinatedFamily: true, sameSourceSheet: true, objectAnimation: false })
  assert.deepEqual(catalogue.boundaries, { approved: false, promoted: false, runtimeChanged: false, finalChanged: false, v5AndV20OnwardChanged: false })
  assert.equal(register.version, spec.version)
  assert.equal(register.asset, asset)

  const stateHashes = new Set()
  const roomHashes = new Set()
  for (const state of spec.states) {
    const stateFile = path.join(rawDir, `${asset}-${state}.png`)
    const image = png(stateFile)
    assert.deepEqual([image.width, image.height], spec.cell, `${asset} ${state} cell changed`)
    assert.equal(sha(stateFile), catalogue.outputs[`${asset}-${state}.png`].sha256)
    assertGutter(image, `${asset} ${state}`)
    for (let i = 3; i < image.data.length; i += 4) assert.ok(image.data[i] === 0 || image.data[i] === 255, `${asset} ${state} has partial alpha`)
    stateHashes.add(sha(stateFile))
    const roomFile = path.join(rawDir, `kitchen-${asset}-${state}-in-situ.png`)
    const room = png(roomFile)
    assert.deepEqual([room.width, room.height], [772, 224], `${asset} ${state} room is not native size`)
    assert.equal(sha(roomFile), catalogue.outputs[`kitchen-${asset}-${state}-in-situ.png`].sha256)
    roomHashes.add(sha(roomFile))
  }
  assert.equal(stateHashes.size, spec.states.length, `${asset} state art is not independently drawn`)
  assert.equal(roomHashes.size, spec.states.length, `${asset} room proofs are not state-specific`)

  for (const kind of spec.effects) {
    const effect = catalogue.effects[kind]
    assert.deepEqual(effect, { file: `fx-${asset}-${kind}-f40.png`, frames: 40, fps: 4, durationSeconds: 10, reusable: true, cellPixels: spec.cell, objectPixelsChanged: false })
    const file = path.join(rawDir, effect.file)
    const strip = png(file)
    assert.deepEqual([strip.width, strip.height], [spec.cell[0] * 40, spec.cell[1]])
    assert.equal(sha(file), catalogue.outputs[effect.file].sha256)
    const frameHashes = new Set()
    for (let frame = 0; frame < 40; frame++) {
      const x0 = frame * spec.cell[0]
      assertGutter(strip, `${asset} ${kind} frame ${frame}`, x0, spec.cell[0])
      const bytes = Buffer.alloc(spec.cell[0] * spec.cell[1] * 4)
      let opaque = 0
      for (let y = 0; y < spec.cell[1]; y++) {
        strip.data.copy(bytes, y * spec.cell[0] * 4, (y * strip.width + x0) * 4, (y * strip.width + x0 + spec.cell[0]) * 4)
        for (let x = 0; x < spec.cell[0]; x++) if (alpha(strip, x0 + x, y)) opaque++
      }
      assert.ok(opaque > 0, `${asset} ${kind} frame ${frame} is empty`)
      frameHashes.add(crypto.createHash('sha256').update(bytes).digest('hex'))
    }
    assert.ok(frameHashes.size >= 20, `${asset} ${kind} lacks a sedate full-loop pose range`)
  }

  const page = fs.readFileSync(pageFile, 'utf8')
  assert.match(page, new RegExp(`Kitchen V${spec.version} · coordinated ${asset}`))
  assert.match(page, /Canonical reference beside the new standard/)
  assert.match(page, /exact 772 × 224 game pixels/)
  assert.match(page, /new Set\(/)
  assert.match(page, /Promise\.all\(unique\.map\(preload\)\)/)
  assert.match(page, /Playback unlocked/)
  for (const cue of spec.sfx) assert.ok(page.includes(cue), `${asset} page omits ${cue}`)
  if (spec.effects.length) {
    assert.match(page, /data-strip data-frames="40" data-fps="4"/)
    assert.match(page, /40f \/ 4fps \/ 10s/)
  }
  const manifest = path.join(root, 'review-archive/sets', `${route}.json`)
  if (fs.existsSync(manifest)) {
    const archive = JSON.parse(fs.readFileSync(manifest, 'utf8'))
    for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
  }
}

const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
for (const [asset, spec] of Object.entries(specs)) assert.ok(nextConfig.includes(`/keeper-review/kitchen-${asset}-states-v${spec.version}`), `${asset} review redirect missing`)
console.log('Kitchen V33-V38 verified: six coordinated families, native-size room proofs, isolated 40-frame effects, transparent gutters, reversible boundaries and named SFX')
