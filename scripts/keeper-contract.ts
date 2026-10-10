/**
 * Build and validate the keeper neutral/bridge contract.
 *
 * The authored keeper sheets remain the visual source of truth. This pass adds
 * exact stills and reusable bridges from those approved pixels, fills the pose
 * and sound fields on every full-body clip, and writes the endpoint audit used
 * by npm test. Run it before scripts/sprites.ts.
 */

import { existsSync, readFileSync, readdirSync, unlinkSync, writeFileSync } from 'node:fs'
import { basename, join } from 'node:path'
import { PNG } from 'pngjs'

const ROOT = process.cwd()
const RAW = join(ROOT, 'art/raw/keeper-first-batch')
const AUDIT_JSON = join(ROOT, 'data/keeper_endpoint_audit.json')
const AUDIT_MD = join(ROOT, 'docs/KEEPER_NEUTRAL_ENDPOINT_AUDIT.md')
const EXCEPTIONS_JSON = join(ROOT, 'data/keeper_endpoint_exceptions.json')
const CHECK = process.argv.includes('--check')

interface Registry { poses: string[]; outfitOrder: string[] }
interface Cue { frame: number; cue: string }
interface Sidecar {
  w: number
  h: number
  frames: number
  fps: number
  density: number
  anchor: [number, number]
  loop?: boolean
  outfit?: string
  facing?: string
  interaction?: string
  seatPoint?: [number, number]
  movementVector?: [number, number]
  startPose?: string
  endPose?: string
  reverseFor?: string
  propHandoffFrame?: number
  sfxCues?: Cue[]
  assetRole?: 'clip' | 'component' | 'reference' | 'neutral' | 'bridge'
  pose?: string
  [key: string]: unknown
}
interface Asset {
  name: string
  jsonPath: string
  pngPath: string
  sidecar: Sidecar
  image: PNG
}
interface NeutralSource { outfit: string; pose: string; clip: string; frame: number; canvas?: { w: number; h: number; anchor: [number, number] } }
interface Metric {
  exact: boolean
  mismatchPercent: number
  canvasAnchorDelta: [number, number]
  landmarkMaxDelta: number
}
interface AuditRow {
  outfit: string
  clip: string
  end: 'start' | 'end'
  pose: string
  neutral: string
  status: 'pass' | 'fail' | 'missing-neutral'
  mismatchPercent: number | null
  canvasAnchorDelta: [number, number] | null
  landmarkMaxDelta: number | null
  remedy: 'none' | 'fix endpoint frame' | 'add bridge' | 'add neutral and bridge'
}

const registry = JSON.parse(readFileSync(join(ROOT, 'data/keeper_pose_registry.json'), 'utf8')) as Registry
const poseSet = new Set(registry.poses)
const COMPONENT = /^keeper_(?:front|back)_(?:torso|arm_[lr]|leg_[lr]|head(?:_[a-z]+)?)$/
const GENERATED = new Set([
  'keeper_walk_cycle', 'keeper_walk_start', 'keeper_walk_stop', 'keeper_pyjamas_walk_cycle',
  'keeper_turn_left_front', 'keeper_turn_left_back',
  'keeper_crouch_back', 'keeper_reach_high', 'keeper_reach_low', 'keeper_pick_up_low',
  'keeper_sitting_turn_back_to_rear',
])

const assetName = (file: string) => basename(file, '.json').replace(/_f\d+$/, '')
const outfitOf = (s: Sidecar) => s.outfit ?? 'standard'
const neutralName = (outfit: string, pose: string) => outfit === 'standard' ? `keeper_neutral_${pose}` : `keeper_${outfit}_neutral_${pose}`

function readAssets(): Map<string, Asset> {
  const out = new Map<string, Asset>()
  for (const file of readdirSync(RAW).filter((f) => /^keeper_.*_f\d+\.json$/.test(f)).sort()) {
    const jsonPath = join(RAW, file)
    const pngPath = jsonPath.replace(/\.json$/, '.png')
    if (!existsSync(pngPath)) throw new Error(`Missing PNG for ${file}`)
    const sidecar = JSON.parse(readFileSync(jsonPath, 'utf8')) as Sidecar
    const image = PNG.sync.read(readFileSync(pngPath))
    const name = assetName(file)
    out.set(name, { name, jsonPath, pngPath, sidecar, image })
  }
  return out
}

function blank(w: number, h: number): PNG {
  const p = new PNG({ width: w, height: h })
  p.data.fill(0)
  return p
}

function frameOf(a: Asset, index: number): PNG {
  const d = a.sidecar.density
  const fw = a.sidecar.w * d
  const h = a.sidecar.h * d
  const i = Math.max(0, Math.min(a.sidecar.frames - 1, index))
  const out = blank(fw, h)
  PNG.bitblt(a.image, out, i * fw, 0, fw, h, 0, 0)
  return out
}

function mirrorFrame(source: PNG): PNG {
  const out = blank(source.width, source.height)
  for (let y = 0; y < source.height; y++) for (let x = 0; x < source.width; x++) {
    const from = (y * source.width + x) * 4
    const to = (y * source.width + source.width - 1 - x) * 4
    source.data.copy(out.data, to, from, from + 4)
  }
  return out
}

function blitAligned(source: PNG, sourceMeta: Sidecar, target: PNG, targetMeta: Sidecar): void {
  const d = targetMeta.density
  if (sourceMeta.density !== d) throw new Error('Mixed keeper density is unsupported')
  const dx = Math.round((targetMeta.anchor[0] - sourceMeta.anchor[0]) * d)
  const dy = Math.round((targetMeta.anchor[1] - sourceMeta.anchor[1]) * d)
  const sx = Math.max(0, -dx), sy = Math.max(0, -dy)
  const tx = Math.max(0, dx), ty = Math.max(0, dy)
  const w = Math.min(source.width - sx, target.width - tx)
  const h = Math.min(source.height - sy, target.height - ty)
  if (w > 0 && h > 0) PNG.bitblt(source, target, sx, sy, w, h, tx, ty)
}

function alignedFrame(source: Asset, index: number, targetMeta: Sidecar): PNG {
  const target = blank(targetMeta.w * targetMeta.density, targetMeta.h * targetMeta.density)
  blitAligned(frameOf(source, index), source.sidecar, target, targetMeta)
  return target
}

function writeAsset(name: string, frames: PNG[], sidecar: Sidecar): Asset {
  if (!frames.length) throw new Error(`No frames for ${name}`)
  const strip = blank(frames[0].width * frames.length, frames[0].height)
  frames.forEach((frame, index) => PNG.bitblt(frame, strip, 0, 0, frame.width, frame.height, index * frame.width, 0))
  for (const old of readdirSync(RAW).filter((f) => f.startsWith(`${name}_f`) && /\.(?:png|json)$/.test(f))) unlinkSync(join(RAW, old))
  const stem = join(RAW, `${name}_f${frames.length}`)
  const full = { ...sidecar, frames: frames.length, fps: frames.length === 1 ? 0 : sidecar.fps }
  writeFileSync(`${stem}.png`, PNG.sync.write(strip))
  writeFileSync(`${stem}.json`, JSON.stringify(full, null, 2) + '\n')
  return { name, pngPath: `${stem}.png`, jsonPath: `${stem}.json`, sidecar: full, image: strip }
}

function poseForFacing(facing = ''): string {
  if (facing === 'front') return 'standing-front'
  if (facing === 'back' || facing === 'up') return 'standing-back'
  if (facing.includes('rear') || facing.includes('three-quarter') || facing.includes('front-right')) return 'standing-rear-right'
  return 'standing-side-right'
}

function seatedPose(facing = ''): string {
  if (facing === 'front') return 'sitting-front'
  if (facing === 'back') return 'sitting-back'
  if (facing.includes('rear')) return 'sitting-rear-right'
  return 'sitting-side-right'
}

function inferPoses(name: string, s: Sidecar): [string, string] {
  const explicit: Record<string, [string, string]> = {
    keeper_turn_back: ['standing-side-right', 'standing-back'],
    keeper_turn_front: ['standing-side-right', 'standing-front'],
    keeper_turn_left_back: ['standing-side-left', 'standing-back'],
    keeper_turn_left_front: ['standing-side-left', 'standing-front'],
    keeper_sit_side: ['standing-side-right', 'sitting-side-right'],
    keeper_sit_front: ['standing-front', 'sitting-front'],
    keeper_sit_back: ['standing-back', 'sitting-back'],
    keeper_sitting_turn_back_to_rear: ['sitting-back', 'sitting-rear-right'],
    keeper_get_into_bed: ['standing-side-right', 'lying-side-right'],
    keeper_pyjamas_turn_back: ['standing-front', 'standing-back'],
    keeper_party_turn_back: ['standing-front', 'standing-back'],
    keeper_walk_into_lift: ['standing-back', 'standing-front'],
    keeper_parachute_jump: ['standing-side-right', 'parachute-open'],
    keeper_parachute_drift: ['parachute-open', 'parachute-open'],
    keeper_parachute_landing: ['parachute-open', 'standing-side-right'],
    keeper_scuba_jetty_dive: ['scuba-standing-side-right', 'scuba-swim-right'],
    keeper_boat_enter: ['standing-side-right', 'sitting-side-right'],
    keeper_boat_exit: ['sitting-side-right', 'standing-side-right'],
    keeper_bath_enter: ['standing-side-right', 'sitting-front'],
    keeper_bath_exit: ['sitting-front', 'standing-side-right'],
    keeper_shower_enter: ['standing-rear-right', 'standing-back'],
    keeper_shower_exit: ['standing-back', 'standing-rear-right'],
    keeper_shower_enter_bathrobe: ['standing-rear-right', 'standing-back'],
    keeper_artist_smock_turn_back: ['standing-side-right', 'standing-back'],
    keeper_artist_smock_turn_front: ['standing-side-right', 'standing-front'],
    keeper_artist_smock_sit_front: ['standing-front', 'sitting-front'],
    keeper_crouch_back: ['standing-back', 'crouching-back'],
    keeper_reach_high: ['standing-side-right', 'standing-side-right'],
    keeper_reach_low: ['standing-side-right', 'standing-side-right'],
    keeper_pick_up_low: ['standing-side-right', 'holding-small-object-side-right'],
  }
  if (explicit[name]) return explicit[name]
  if (s.startPose && s.endPose && poseSet.has(s.startPose) && poseSet.has(s.endPose)) return [s.startPose, s.endPose]
  if (/swim_(?:horizontal|costume_horizontal)/.test(name)) return ['swimming-side-right', 'swimming-side-right']
  if (/swim_(?:up|costume_up)/.test(name)) return ['swimming-back', 'swimming-back']
  if (/swim_(?:down|costume_down)/.test(name)) return ['swimming-front', 'swimming-front']
  if (name.includes('pressups')) return ['prone-side-right', 'prone-side-right']
  if (name.includes('anti_gravity')) return ['floating-prone-right', 'floating-prone-right']
  if (name.includes('pyjamas_snore')) return ['lying-side-right', 'lying-side-right']
  if (/crouch|search_boxes|collect_eggs/.test(name)) return ['crouching-back', 'crouching-back']
  if (name.includes('ladder')) return ['climbing-back', 'climbing-back']
  if (name.includes('guitar_pickup_')) {
    const kind = name.replace('keeper_guitar_pickup_', '')
    return ['standing-side-right', `play-guitar-${kind}`]
  }
  if (name.includes('play_guitar_flying_v')) return ['play-guitar-flying-v-1967', 'play-guitar-flying-v-1967']
  if (name.includes('play_guitar_gretsch')) return ['play-guitar-gretsch', 'play-guitar-gretsch']
  if (name === 'keeper_play_guitar') return ['play-guitar-acoustic', 'play-guitar-acoustic']
  if (name.includes('turn_back')) {
    if (s.facing?.startsWith('front')) return ['standing-front', 'standing-back']
    return ['standing-side-right', 'standing-back']
  }
  if (name.includes('turn_front')) return ['standing-side-right', 'standing-front']
  if (s.seatPoint) {
    const pose = seatedPose(s.facing)
    return [pose, pose]
  }
  const pose = poseForFacing(s.facing)
  return [pose, pose]
}

function enrich(a: Asset): void {
  const s = a.sidecar
  if (COMPONENT.test(a.name)) {
    s.assetRole = 'component'
    delete s.startPose; delete s.endPose
    return
  }
  if (a.name === 'keeper_reference') {
    s.assetRole = 'reference'
    delete s.startPose; delete s.endPose
    return
  }
  if (a.name.includes('_neutral_')) s.assetRole = 'neutral'
  else if (GENERATED.has(a.name) || /walk.*_(?:cycle|start|stop)$/.test(a.name) || a.name === 'keeper_turn_front') s.assetRole = 'bridge'
  else s.assetRole = 'clip'
  const [start, end] = inferPoses(a.name, s)
  s.startPose = start; s.endPose = end
  // Keep the accepted right-to-back source sidecar stable; its cardinal route
  // is expressed by startPose/endPose, while derived left bridges carry facing.
  if (a.name === 'keeper_turn_back') {
    delete s.facing
    delete s.interaction
  }
  if (/walk/.test(a.name) && s.frames > 1 && !a.name.includes('walk_into_lift') && !s.sfxCues?.length) {
    const second = Math.min(s.frames - 1, Math.floor(s.frames / 2))
    s.sfxCues = [{ frame: 0, cue: 'footstep' }, { frame: second, cue: 'footstep' }]
  }
  if (a.name === 'keeper_pick_vegetable' || a.name === 'keeper_pick_fruit') s.propHandoffFrame ??= 5
  if (a.name === 'keeper_hot_drink_pickup') s.propHandoffFrame ??= 5
  if (a.name === 'keeper_hot_drink_put_down') s.propHandoffFrame ??= 5
}

const neutralSources: NeutralSource[] = [
  { outfit: 'standard', pose: 'standing-side-right', clip: 'keeper_walk', frame: 2 },
  { outfit: 'standard', pose: 'standing-front', clip: 'keeper_sit_front', frame: 0 },
  { outfit: 'standard', pose: 'standing-back', clip: 'keeper_turn_back', frame: 5 },
  { outfit: 'standard', pose: 'sitting-side-right', clip: 'keeper_sit_side', frame: 5 },
  { outfit: 'standard', pose: 'sitting-front', clip: 'keeper_sit_front', frame: 5 },
  { outfit: 'standard', pose: 'sitting-back', clip: 'keeper_sit_back', frame: 5 },
  { outfit: 'standard', pose: 'sitting-rear-right', clip: 'keeper_watch_tv', frame: 0, canvas: { w: 34, h: 40, anchor: [17, 40] } },
  { outfit: 'standard', pose: 'crouching-back', clip: 'keeper_crouch_work_back', frame: 3 },
  { outfit: 'standard', pose: 'holding-small-object-side-right', clip: 'keeper_pick_vegetable', frame: 7 },
  { outfit: 'artist-smock', pose: 'standing-side-right', clip: 'keeper_artist_smock_walk', frame: 2 },
  { outfit: 'artist-smock', pose: 'standing-front', clip: 'keeper_artist_smock_turn_front', frame: 5 },
  { outfit: 'artist-smock', pose: 'standing-back', clip: 'keeper_artist_smock_turn_back', frame: 5 },
  { outfit: 'artist-smock', pose: 'sitting-front', clip: 'keeper_artist_smock_sit_front', frame: 5 },
  { outfit: 'light-blue-pyjamas', pose: 'standing-side-right', clip: 'keeper_pyjamas_walk', frame: 2 },
  { outfit: 'light-blue-pyjamas', pose: 'standing-front', clip: 'keeper_pyjamas_turn_back', frame: 0 },
  { outfit: 'light-blue-pyjamas', pose: 'standing-back', clip: 'keeper_pyjamas_turn_back', frame: 5 },
  { outfit: 'light-blue-pyjamas', pose: 'lying-side-right', clip: 'keeper_get_into_bed', frame: 7 },
  { outfit: 'cream-bathrobe', pose: 'standing-side-right', clip: 'keeper_bathrobe_walk', frame: 2 },
  { outfit: 'cream-bathrobe', pose: 'standing-rear-right', clip: 'keeper_shower_door_open_bathrobe', frame: 0 },
  { outfit: 'cream-bathrobe', pose: 'standing-back', clip: 'keeper_shower_enter_bathrobe', frame: 7 },
  { outfit: 'party-hat', pose: 'standing-side-right', clip: 'keeper_party_walk', frame: 2 },
  { outfit: 'party-hat', pose: 'standing-front', clip: 'keeper_party_idle', frame: 0 },
  { outfit: 'party-hat', pose: 'standing-back', clip: 'keeper_party_turn_back', frame: 5 },
  { outfit: 'party-hat', pose: 'sitting-side-right', clip: 'keeper_party_eat_cake', frame: 0 },
  { outfit: 'mechanic', pose: 'standing-side-right', clip: 'keeper_mechanic_walk_side', frame: 2 },
  { outfit: 'mechanic', pose: 'standing-front', clip: 'keeper_mechanic_walk_front', frame: 2 },
  { outfit: 'mechanic', pose: 'standing-back', clip: 'keeper_mechanic_walk_back', frame: 2 },
  { outfit: 'old-school-workout-kit', pose: 'standing-front', clip: 'keeper_trampoline_front', frame: 0 },
  { outfit: 'old-school-workout-kit', pose: 'standing-back', clip: 'keeper_lift_weights_back', frame: 0 },
  { outfit: 'old-school-workout-kit', pose: 'prone-side-right', clip: 'keeper_pressups_side', frame: 0 },
  { outfit: 'striped-swimming-costume', pose: 'swimming-side-right', clip: 'keeper_swim_costume_horizontal', frame: 0 },
  { outfit: 'striped-swimming-costume', pose: 'swimming-back', clip: 'keeper_swim_costume_up', frame: 0 },
  { outfit: 'striped-swimming-costume', pose: 'swimming-front', clip: 'keeper_swim_costume_down', frame: 0 },
  { outfit: 'scuba', pose: 'scuba-standing-side-right', clip: 'keeper_scuba_walk_side', frame: 0 },
  { outfit: 'scuba', pose: 'scuba-swim-right', clip: 'keeper_scuba_swim_horizontal', frame: 0 },
  { outfit: 'scuba', pose: 'swimming-back', clip: 'keeper_scuba_swim_up', frame: 0 },
  { outfit: 'scuba', pose: 'swimming-front', clip: 'keeper_scuba_swim_down', frame: 0 },
  { outfit: 'souwester', pose: 'standing-side-right', clip: 'keeper_souwester_walk_side', frame: 2 },
  { outfit: 'souwester', pose: 'standing-front', clip: 'keeper_souwester_walk_front', frame: 2 },
  { outfit: 'souwester', pose: 'standing-back', clip: 'keeper_souwester_walk_back', frame: 2 },
  ...['knight', 'pirate', 'spaceman', 'halloween', 'tarzan'].flatMap((outfit): NeutralSource[] => [
    { outfit, pose: 'standing-side-right', clip: `keeper_${outfit}_walk_side`, frame: 2 },
    { outfit, pose: 'standing-front', clip: `keeper_${outfit}_walk_front`, frame: 2 },
    { outfit, pose: 'standing-back', clip: `keeper_${outfit}_walk_back`, frame: 2 },
  ]),
  { outfit: 'towel-privacy', pose: 'standing-side-right', clip: 'keeper_bath_enter', frame: 0 },
  { outfit: 'towel-privacy', pose: 'standing-rear-right', clip: 'keeper_shower_enter', frame: 0 },
  { outfit: 'mosaic-privacy', pose: 'sitting-front', clip: 'keeper_bath_wash', frame: 0 },
  { outfit: 'mosaic-privacy', pose: 'standing-back', clip: 'keeper_shower_wash', frame: 0 },
  { outfit: 'privacy-foam', pose: 'sitting-front', clip: 'keeper_hot_tub', frame: 0 },
]

function buildNeutrals(assets: Map<string, Asset>): void {
  for (const n of neutralSources) {
    if (!poseSet.has(n.pose)) throw new Error(`Neutral uses unregistered pose ${n.pose}`)
    const source = assets.get(n.clip)
    if (!source) throw new Error(`Neutral source is missing: ${n.clip}`)
    const name = neutralName(n.outfit, n.pose)
    const feetAnchored = source.sidecar.anchor[1] >= source.sidecar.h - 1
    const neutralW = n.canvas?.w ?? (feetAnchored ? Math.max(1, Math.round(source.sidecar.anchor[0] * 2)) : source.sidecar.w)
    const neutralH = n.canvas?.h ?? (feetAnchored ? Math.max(1, Math.round(source.sidecar.anchor[1])) : source.sidecar.h)
    const sidecar: Sidecar = {
      w: neutralW, h: neutralH, frames: 1, fps: 0,
      density: source.sidecar.density, anchor: n.canvas?.anchor ?? source.sidecar.anchor, z: source.sidecar.z ?? 50,
      loop: false, ...(n.outfit === 'standard' ? {} : { outfit: n.outfit }),
      startPose: n.pose, endPose: n.pose, pose: n.pose, assetRole: 'neutral',
      ...(source.sidecar.facing ? { facing: source.sidecar.facing } : {}),
      ...(source.sidecar.mirrorSafe ? { mirrorSafe: true } : {}),
    }
    assets.set(name, writeAsset(name, [alignedFrame(source, n.frame, sidecar)], sidecar))
  }
  const leftPose = 'standing-side-left'
  if (!poseSet.has(leftPose)) throw new Error(`Neutral uses unregistered pose ${leftPose}`)
  for (const outfit of [...new Set(neutralSources.filter((n) => n.pose === 'standing-side-right').map((n) => n.outfit))]) {
    const right = neutralFor(assets, outfit, 'standing-side-right')
    if (!right) throw new Error(`Right-facing neutral is missing for ${outfit}`)
    const sidecar: Sidecar = {
      ...right.sidecar,
      anchor: [right.sidecar.w - right.sidecar.anchor[0], right.sidecar.anchor[1]],
      facing: 'left', startPose: leftPose, endPose: leftPose, pose: leftPose,
      assetRole: 'neutral', mirrorSafe: true,
    }
    const name = neutralName(outfit, leftPose)
    assets.set(name, writeAsset(name, [mirrorFrame(frameOf(right, 0))], sidecar))
  }
}

function neutralFor(assets: Map<string, Asset>, outfit: string, pose: string): Asset | undefined {
  return assets.get(neutralName(outfit, pose))
}

function replaceEnd(assets: Map<string, Asset>, clip: string, end: 'start' | 'end', outfit: string, pose: string): void {
  const a = assets.get(clip), neutral = neutralFor(assets, outfit, pose)
  if (!a || !neutral) throw new Error(`Cannot repair ${clip} ${end}: ${outfit}/${pose}`)
  const targetIndex = end === 'start' ? 0 : a.sidecar.frames - 1
  const fw = a.sidecar.w * a.sidecar.density, fh = a.sidecar.h * a.sidecar.density
  a.image.data.fill(0, targetIndex * fw * 4, targetIndex * fw * 4) // no-op; rows are not contiguous by frame
  const clean = blank(fw, fh)
  blitAligned(frameOf(neutral, 0), neutral.sidecar, clean, a.sidecar)
  for (let y = 0; y < fh; y++) {
    const start = (y * a.image.width + targetIndex * fw) * 4
    a.image.data.fill(0, start, start + fw * 4)
  }
  PNG.bitblt(clean, a.image, 0, 0, fw, fh, targetIndex * fw, 0)
  writeFileSync(a.pngPath, PNG.sync.write(a.image))
  if (end === 'start') a.sidecar.startPose = pose
  else a.sidecar.endPose = pose
  writeFileSync(a.jsonPath, JSON.stringify(a.sidecar, null, 2) + '\n')
}

function buildBridges(assets: Map<string, Asset>): void {
  for (const name of ['keeper_watch_tv', 'keeper_sitting_turn_back_to_rear']) {
    const source = assets.get(name)
    if (!source) continue
    const meta: Sidecar = { ...source.sidecar, w: 34, h: 40, anchor: [17, 40] }
    const reframed = Array.from({ length: source.sidecar.frames }, (_, i) => alignedFrame(source, i, meta))
    assets.set(name, writeAsset(name, reframed, meta))
  }
  for (const [sourceName, name, endPose, facing, interaction, reverseFor] of [
    ['keeper_turn_front', 'keeper_turn_left_front', 'standing-front', 'left-to-front', 'turn-front', 'turn_left_from_front'],
    ['keeper_turn_back', 'keeper_turn_left_back', 'standing-back', 'left-to-back', 'turn-back', 'turn_left_from_back'],
  ] as const) {
    const source = assets.get(sourceName)
    if (!source) throw new Error(`Turn source is missing: ${sourceName}`)
    const meta: Sidecar = {
      ...source.sidecar,
      anchor: [source.sidecar.w - source.sidecar.anchor[0], source.sidecar.anchor[1]],
      facing, interaction, reverseFor, startPose: 'standing-side-left', endPose,
      assetRole: 'bridge', mirrorSafe: false,
    }
    const frames = Array.from({ length: source.sidecar.frames }, (_, i) => mirrorFrame(frameOf(source, i)))
    const bridge = writeAsset(name, frames, meta)
    assets.set(name, bridge)
  }
  const walk = assets.get('keeper_walk')!, side = neutralFor(assets, 'standard', 'standing-side-right')!
  const n = frameOf(side, 0)
  const bridgeBase: Sidecar = { w: 32, h: 40, frames: 5, fps: 8, density: 4, anchor: [16, 40], z: 50, loop: false, mirrorSafe: true, facing: 'right', startPose: 'standing-side-right', endPose: 'standing-side-right', assetRole: 'bridge' }
  const start = writeAsset('keeper_walk_start', [n, frameOf(walk, 3), frameOf(walk, 4), frameOf(walk, 5), n], { ...bridgeBase, interaction: 'walk-start', reverseFor: 'walk_stop', sfxCues: [{ frame: 2, cue: 'footstep' }] })
  const stop = writeAsset('keeper_walk_stop', [n, frameOf(walk, 7), frameOf(walk, 0), frameOf(walk, 1), n], { ...bridgeBase, interaction: 'walk-stop', reverseFor: 'walk_start', sfxCues: [{ frame: 2, cue: 'footstep' }] })
  const cycle = writeAsset('keeper_walk_cycle', [n, frameOf(walk, 3), frameOf(walk, 4), frameOf(walk, 5), frameOf(walk, 6), frameOf(walk, 7), frameOf(walk, 0), frameOf(walk, 1), n], { ...bridgeBase, frames: 9, fps: 8, loop: true, interaction: 'walk', sfxCues: [{ frame: 2, cue: 'footstep' }, { frame: 6, cue: 'footstep' }] })
  assets.set(start.name, start); assets.set(stop.name, stop); assets.set(cycle.name, cycle)

  const outfitWalks: Array<[string, string, string, boolean]> = [
    ['keeper_artist_smock_walk', 'artist-smock', 'footstep', true],
    ['keeper_pyjamas_walk', 'light-blue-pyjamas', 'slipper_step', true],
    ['keeper_bathrobe_walk', 'cream-bathrobe', 'slipper_step', true],
    ['keeper_party_walk', 'party-hat', 'footstep', true],
    ['keeper_mechanic_walk_side', 'mechanic', 'boot_step', true],
    ['keeper_mechanic_walk_front', 'mechanic', 'boot_step', false],
    ['keeper_mechanic_walk_back', 'mechanic', 'boot_step', false],
    ['keeper_scuba_walk_side', 'scuba', 'boot_step', true],
    ['keeper_souwester_walk_side', 'souwester', 'boot_step', true],
    ['keeper_souwester_walk_front', 'souwester', 'boot_step', false],
    ['keeper_souwester_walk_back', 'souwester', 'boot_step', false],
    ...['knight', 'pirate', 'spaceman', 'halloween', 'tarzan'].flatMap((outfit): Array<[string, string, string, boolean]> => [
      [`keeper_${outfit}_walk_side`, outfit, 'footstep', true],
      [`keeper_${outfit}_walk_front`, outfit, 'footstep', false],
      [`keeper_${outfit}_walk_back`, outfit, 'footstep', false],
    ]),
  ]
  for (const [sourceName, outfit, cue, makeStartStop] of outfitWalks) {
    const source = assets.get(sourceName)
    if (!source) continue
    const pose = source.sidecar.startPose!
    const neutral = neutralFor(assets, outfit, pose)
    if (!neutral || source.sidecar.frames < 8) continue
    const meta: Sidecar = {
      w: neutral.sidecar.w, h: neutral.sidecar.h, frames: 9, fps: source.sidecar.fps || 8,
      density: source.sidecar.density, anchor: neutral.sidecar.anchor, z: source.sidecar.z ?? 50,
      loop: true, outfit, mirrorSafe: source.sidecar.mirrorSafe, facing: source.sidecar.facing,
      interaction: source.sidecar.interaction, movementVector: source.sidecar.movementVector,
      startPose: pose, endPose: pose, assetRole: 'bridge',
      sfxCues: [{ frame: 2, cue }, { frame: 6, cue }],
    }
    const still = alignedFrame(neutral, 0, meta)
    const cycleName = `${sourceName}_cycle`
    const outfitCycle = writeAsset(cycleName, [still, ...[3, 4, 5, 6, 7, 0, 1].map((frame) => alignedFrame(source, frame, meta)), still], meta)
    assets.set(cycleName, outfitCycle)
    if (!makeStartStop) continue
    for (const [suffix, indices, reverseFor] of [
      ['start', [3, 4, 5], 'walk_stop'],
      ['stop', [7, 0, 1], 'walk_start'],
    ] as const) {
      const name = `${sourceName}_${suffix}`
      const bridge = writeAsset(name, [still, ...indices.map((frame) => alignedFrame(source, frame, meta)), still], {
        ...meta, frames: 5, loop: false, reverseFor, interaction: `${source.sidecar.interaction ?? 'walk'}-${suffix}`,
        sfxCues: [{ frame: 2, cue }],
      })
      assets.set(name, bridge)
    }
  }

  const back = neutralFor(assets, 'standard', 'standing-back')!, crouch = neutralFor(assets, 'standard', 'crouching-back')!, crouchWork = assets.get('keeper_crouch_work_back')!
  const crouchMeta: Sidecar = { w: crouchWork.sidecar.w, h: crouchWork.sidecar.h, frames: 4, fps: 6, density: 4, anchor: crouchWork.sidecar.anchor, z: 50, loop: false, facing: 'back', interaction: 'crouch',
    startPose: 'standing-back', endPose: 'crouching-back', reverseFor: 'stand_back_from_crouch', assetRole: 'bridge',
  }
  const crouchBridge = writeAsset('keeper_crouch_back', [alignedFrame(back, 0, crouchMeta), alignedFrame(crouchWork, 1, crouchMeta), alignedFrame(crouchWork, 2, crouchMeta), alignedFrame(crouch, 0, crouchMeta)], crouchMeta)
  assets.set(crouchBridge.name, crouchBridge)

  const highSource = assets.get('keeper_pick_fruit')!, lowSource = assets.get('keeper_pick_vegetable')!
  const centred = (source: Asset) => {
    const half = Math.max(source.sidecar.anchor[0], source.sidecar.w - source.sidecar.anchor[0])
    return { w: Math.ceil(half * 2), h: Math.round(source.sidecar.anchor[1]), anchor: [Math.ceil(half), Math.round(source.sidecar.anchor[1])] as [number, number] }
  }
  const highCanvas = centred(highSource), lowCanvas = centred(lowSource)
  const highMeta: Sidecar = { ...bridgeBase, ...highCanvas, interaction: 'reach-high', reverseFor: 'withdraw_high' }
  const lowMeta: Sidecar = { ...bridgeBase, ...lowCanvas, interaction: 'reach-low', reverseFor: 'withdraw_low' }
  const high = writeAsset('keeper_reach_high', [alignedFrame(side, 0, highMeta), alignedFrame(highSource, 1, highMeta), alignedFrame(highSource, 2, highMeta), alignedFrame(highSource, 3, highMeta), alignedFrame(side, 0, highMeta)], highMeta)
  const low = writeAsset('keeper_reach_low', [alignedFrame(side, 0, lowMeta), alignedFrame(lowSource, 1, lowMeta), alignedFrame(lowSource, 2, lowMeta), alignedFrame(lowSource, 3, lowMeta), alignedFrame(side, 0, lowMeta)], lowMeta)
  const pickupMeta: Sidecar = {
    ...lowCanvas, frames: lowSource.sidecar.frames, fps: 5, density: 4, z: 50, loop: false,
    mirrorSafe: true, facing: 'right', interaction: 'pick-up-low', startPose: 'standing-side-right', endPose: 'holding-small-object-side-right', reverseFor: 'put_down_low',
    propHandoffFrame: 5, assetRole: 'bridge',
  }
  const pickupFrames = Array.from({ length: lowSource.sidecar.frames }, (_, i) => alignedFrame(lowSource, i, pickupMeta))
  pickupFrames[0] = alignedFrame(side, 0, pickupMeta)
  const pickup = writeAsset('keeper_pick_up_low', pickupFrames, {
    ...pickupMeta, frames: pickupFrames.length,
  })
  for (const a of [high, low, pickup]) assets.set(a.name, a)
}

function bbox(a: Asset, frame: PNG): [number, number, number, number] | null {
  let x0 = Infinity, y0 = Infinity, x1 = -1, y1 = -1
  for (let y = 0; y < frame.height; y++) for (let x = 0; x < frame.width; x++) {
    if (frame.data[(y * frame.width + x) * 4 + 3] < 128) continue
    if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y
  }
  if (x1 < 0) return null
  const d = a.sidecar.density, [ax, ay] = a.sidecar.anchor
  return [x0 / d - ax, y0 / d - ay, (x1 + 1) / d - ax, (y1 + 1) / d - ay]
}

function pixels(a: Asset, frame: PNG): Map<string, number> {
  const out = new Map<string, number>(), d = a.sidecar.density, [ax, ay] = a.sidecar.anchor
  const ox = Math.round(ax * d), oy = Math.round(ay * d)
  for (let y = 0; y < frame.height; y++) for (let x = 0; x < frame.width; x++) {
    const i = (y * frame.width + x) * 4
    if (frame.data[i + 3] < 128) continue
    const colour = (frame.data[i] << 24) | (frame.data[i + 1] << 16) | (frame.data[i + 2] << 8) | 255
    out.set(`${x - ox},${y - oy}`, colour)
  }
  return out
}

function metric(a: Asset, index: number, neutral: Asset): Metric {
  const af = frameOf(a, index), nf = frameOf(neutral, 0), ap = pixels(a, af), np = pixels(neutral, nf)
  const keys = new Set([...ap.keys(), ...np.keys()])
  let mismatch = 0
  for (const k of keys) if (ap.get(k) !== np.get(k)) mismatch++
  const ab = bbox(a, af), nb = bbox(neutral, nf)
  const landmarkMaxDelta = ab && nb ? Math.max(...ab.map((v, i) => Math.abs(v - nb[i]))) : 999
  const anchorA: [number, number] = [a.sidecar.anchor[0] - a.sidecar.w / 2, a.sidecar.anchor[1] - a.sidecar.h]
  const anchorN: [number, number] = [neutral.sidecar.anchor[0] - neutral.sidecar.w / 2, neutral.sidecar.anchor[1] - neutral.sidecar.h]
  const canvasAnchorDelta: [number, number] = [Number((anchorA[0] - anchorN[0]).toFixed(2)), Number((anchorA[1] - anchorN[1]).toFixed(2))]
  return {
    exact: mismatch === 0 && Math.abs(canvasAnchorDelta[0]) <= 0.5 && Math.abs(canvasAnchorDelta[1]) <= 0.5 && landmarkMaxDelta <= 0.5,
    mismatchPercent: keys.size ? Number(((mismatch / keys.size) * 100).toFixed(2)) : 0,
    canvasAnchorDelta,
    landmarkMaxDelta: Number(landmarkMaxDelta.toFixed(2)),
  }
}

function remedyFor(a: Asset, m: Metric | null): AuditRow['remedy'] {
  if (!m) return 'add neutral and bridge'
  if (m.exact) return 'none'
  if (a.sidecar.loop) return 'add bridge'
  if (m.landmarkMaxDelta <= 2 && m.mismatchPercent <= 35 && !a.sidecar.propHandoffFrame) return 'fix endpoint frame'
  return 'add bridge'
}

function buildAudit(assets: Map<string, Asset>): { rows: AuditRow[]; actionClips: number } {
  const rows: AuditRow[] = []
  let actionClips = 0
  for (const a of [...assets.values()].sort((a, b) => a.name.localeCompare(b.name))) {
    if (a.sidecar.assetRole === 'component' || a.sidecar.assetRole === 'reference' || a.sidecar.assetRole === 'neutral') continue
    actionClips++
    const outfit = outfitOf(a.sidecar)
    for (const end of ['start', 'end'] as const) {
      const pose = end === 'start' ? a.sidecar.startPose! : a.sidecar.endPose!
      const nn = neutralName(outfit, pose)
      const neutral = assets.get(nn)
      if (!neutral) {
        rows.push({ outfit, clip: a.name, end, pose, neutral: nn, status: 'missing-neutral', mismatchPercent: null, canvasAnchorDelta: null, landmarkMaxDelta: null, remedy: 'add neutral and bridge' })
        continue
      }
      const m = metric(a, end === 'start' ? 0 : a.sidecar.frames - 1, neutral)
      rows.push({ outfit, clip: a.name, end, pose, neutral: nn, status: m.exact ? 'pass' : 'fail', mismatchPercent: m.mismatchPercent, canvasAnchorDelta: m.canvasAnchorDelta, landmarkMaxDelta: m.landmarkMaxDelta, remedy: remedyFor(a, m) })
    }
  }
  return { rows, actionClips }
}

function writeAudit(audit: ReturnType<typeof buildAudit>): void {
  const failed = audit.rows.filter((r) => r.status !== 'pass')
  writeFileSync(AUDIT_JSON, JSON.stringify({
    schemaVersion: 1,
    measuredAt: '2026-10-10',
    actionClips: audit.actionClips,
    endpointChecks: audit.rows.length,
    passingEndpoints: audit.rows.length - failed.length,
    failingEndpoints: failed.length,
    rows: audit.rows,
  }, null, 2) + '\n')
  const lines = [
    '# Keeper neutral endpoint audit', '',
    'Audit date: 10 October 2026. Generated by `node scripts/keeper-contract.ts` from the density-4 source strips. The report compares real RGBA pixels in anchor-relative coordinates; it does not use canvas rectangles as a proxy for the body.', '',
    `Coverage: ${audit.actionClips} full-body action/bridge clips, ${audit.rows.length} endpoint checks, ${audit.rows.length - failed.length} exact passes and ${failed.length} endpoints still requiring the recorded remedy. The 18 modular/reference sheets are not action clips.`, '',
    'Metrics: `pixels` is the percentage of opaque anchor-relative pixels whose colour/presence differs; `anchor` is the canvas-centre/baseline anchor delta in logical pixels; `landmarks` is the maximum delta across the silhouette left/top/right/bottom landmarks. Exact means zero pixel mismatch, anchor delta no more than 0.5 px and landmark delta no more than 0.5 px.', '',
    'Migration guard: the current legacy failures are frozen in `data/keeper_endpoint_exceptions.json`. `npm test` recomputes the real-pixel audit and fails on a new failure, a regression, a stale audit row or a stale exception. New sheets must pass; do not extend the exception file to make them green.', '',
  ]
  const order = new Map(registry.outfitOrder.map((x, i) => [x, i]))
  const outfits = [...new Set(failed.map((r) => r.outfit))].sort((a, b) => (order.get(a) ?? 999) - (order.get(b) ?? 999) || a.localeCompare(b))
  for (const outfit of outfits) {
    lines.push(`## ${outfit}`, '', '| Clip | Failing end | Expected pose | Delta | Remedy |', '|---|---|---|---|---|')
    for (const r of failed.filter((x) => x.outfit === outfit)) {
      const delta = r.status === 'missing-neutral' ? 'neutral missing' : `pixels ${r.mismatchPercent}%; anchor (${r.canvasAnchorDelta![0]}, ${r.canvasAnchorDelta![1]}); landmarks ${r.landmarkMaxDelta}px`
      lines.push(`| \`${r.clip}\` | ${r.end} | \`${r.pose}\` | ${delta} | ${r.remedy} |`)
    }
    lines.push('')
  }
  lines.push('## Exact endpoints', '', 'Exact passes are retained in the machine-readable `data/keeper_endpoint_audit.json`; they are omitted from the failure tables above so the repair queue stays usable.', '')
  writeFileSync(AUDIT_MD, lines.join('\n'))
}

function validate(assets: Map<string, Asset>): void {
  const errors: string[] = []
  const storedAudit = existsSync(AUDIT_JSON) ? JSON.parse(readFileSync(AUDIT_JSON, 'utf8')) as { rows?: AuditRow[] } : null
  const currentAudit = buildAudit(assets)
  const audited = new Set((storedAudit?.rows ?? []).map((r) => `${r.clip}:${r.end}`))
  const currentRows = new Map(currentAudit.rows.map((r) => [`${r.clip}:${r.end}`, r]))
  for (const row of currentAudit.rows) {
    const stored = (storedAudit?.rows ?? []).find((candidate) => candidate.clip === row.clip && candidate.end === row.end)
    if (!stored || JSON.stringify(stored) !== JSON.stringify(row)) errors.push(`${row.clip}: ${row.end} endpoint audit is stale`)
  }
  const exceptions = existsSync(EXCEPTIONS_JSON)
    ? JSON.parse(readFileSync(EXCEPTIONS_JSON, 'utf8')) as { exceptions?: Array<Pick<AuditRow, 'clip' | 'end' | 'pose' | 'remedy'>> }
    : null
  const exceptionKeys = new Set((exceptions?.exceptions ?? []).map((r) => `${r.clip}:${r.end}`))
  for (const row of currentAudit.rows.filter((r) => r.status !== 'pass')) {
    if (!exceptionKeys.has(`${row.clip}:${row.end}`)) errors.push(`${row.clip}: ${row.end} is a new unapproved endpoint failure`)
  }
  for (const exception of exceptions?.exceptions ?? []) {
    const row = currentRows.get(`${exception.clip}:${exception.end}`)
    if (!row || row.status === 'pass') errors.push(`${exception.clip}: ${exception.end} endpoint exception is stale`)
    else if (row.pose !== exception.pose || row.remedy !== exception.remedy) errors.push(`${exception.clip}: ${exception.end} endpoint exception no longer matches the audit`)
  }
  for (const a of assets.values()) {
    const s = a.sidecar
    if (s.assetRole !== 'component' && s.assetRole !== 'reference') {
      if (!s.startPose || !poseSet.has(s.startPose)) errors.push(`${a.name}: invalid/missing startPose`)
      if (!s.endPose || !poseSet.has(s.endPose)) errors.push(`${a.name}: invalid/missing endPose`)
      if (s.assetRole !== 'neutral') for (const end of ['start', 'end']) if (!audited.has(`${a.name}:${end}`)) errors.push(`${a.name}: ${end} is absent from endpoint audit`)
    }
    for (const cue of s.sfxCues ?? []) {
      if (!Number.isInteger(cue.frame) || cue.frame < 0 || cue.frame >= s.frames) errors.push(`${a.name}: sfx frame ${cue.frame} is outside 0..${s.frames - 1}`)
      if (!/^[a-z0-9_-]+$/.test(cue.cue)) errors.push(`${a.name}: invalid cue ${cue.cue}`)
    }
    if (s.propHandoffFrame !== undefined && (!Number.isInteger(s.propHandoffFrame) || s.propHandoffFrame < 1 || s.propHandoffFrame > s.frames)) errors.push(`${a.name}: invalid propHandoffFrame`)
  }
  for (const outfit of [...new Set(neutralSources.filter((n) => n.pose === 'standing-side-right').map((n) => n.outfit))]) {
    const right = neutralFor(assets, outfit, 'standing-side-right')
    const left = neutralFor(assets, outfit, 'standing-side-left')
    if (!right || !left) {
      errors.push(`${outfit}: missing right/left standing neutral pair`)
      continue
    }
    const expected = mirrorFrame(frameOf(right, 0)), actual = frameOf(left, 0)
    if (expected.width !== actual.width || expected.height !== actual.height || !expected.data.equals(actual.data)) errors.push(`${outfit}: left standing neutral is not an exact mirror of right`)
    const expectedAnchor: [number, number] = [right.sidecar.w - right.sidecar.anchor[0], right.sidecar.anchor[1]]
    if (left.sidecar.anchor[0] !== expectedAnchor[0] || left.sidecar.anchor[1] !== expectedAnchor[1]) errors.push(`${outfit}: left standing neutral anchor is not mirrored exactly`)
  }
  for (const [clip, outfit, start, end] of [
    ['keeper_walk_cycle', 'standard', 'standing-side-right', 'standing-side-right'],
    ['keeper_turn_back', 'standard', 'standing-side-right', 'standing-back'],
    ['keeper_turn_front', 'standard', 'standing-side-right', 'standing-front'],
    ['keeper_turn_left_back', 'standard', 'standing-side-left', 'standing-back'],
    ['keeper_turn_left_front', 'standard', 'standing-side-left', 'standing-front'],
    ['keeper_sit_side', 'standard', 'standing-side-right', 'sitting-side-right'],
    ['keeper_sit_back', 'standard', 'standing-back', 'sitting-back'],
    ['keeper_sitting_turn_back_to_rear', 'standard', 'sitting-back', 'sitting-rear-right'],
    ['keeper_watch_tv', 'standard', 'sitting-rear-right', 'sitting-rear-right'],
    ['keeper_get_into_bed', 'light-blue-pyjamas', 'standing-side-right', 'lying-side-right'],
    ['keeper_pyjamas_walk_cycle', 'light-blue-pyjamas', 'standing-side-right', 'standing-side-right'],
  ] as const) {
    const a = assets.get(clip)
    if (!a) { errors.push(`${clip}: missing priority clip`); continue }
    for (const [which, pose, index] of [['start', start, 0], ['end', end, a.sidecar.frames - 1]] as const) {
      const n = neutralFor(assets, outfit, pose)
      if (!n || !metric(a, index, n).exact) errors.push(`${clip}: ${which} is not the exact ${outfit}/${pose} neutral`)
    }
  }
  if (errors.length) throw new Error(`Keeper contract failed:\n- ${errors.join('\n- ')}`)
}

let assets = readAssets()
if (CHECK) {
  validate(assets)
  console.log(`Keeper contract valid: ${assets.size} keeper sheets`)
} else {
  for (const a of assets.values()) enrich(a)
  for (const a of assets.values()) writeFileSync(a.jsonPath, JSON.stringify(a.sidecar, null, 2) + '\n')
  buildNeutrals(assets)
  assets = readAssets()
  for (const a of assets.values()) enrich(a)
  buildBridges(assets)
  assets = readAssets()
  for (const a of assets.values()) enrich(a)
  for (const [clip, end, outfit, pose] of [
    ['keeper_turn_back', 'start', 'standard', 'standing-side-right'], ['keeper_turn_back', 'end', 'standard', 'standing-back'],
    ['keeper_turn_front', 'start', 'standard', 'standing-side-right'], ['keeper_turn_front', 'end', 'standard', 'standing-front'],
    ['keeper_turn_left_back', 'start', 'standard', 'standing-side-left'], ['keeper_turn_left_back', 'end', 'standard', 'standing-back'],
    ['keeper_turn_left_front', 'start', 'standard', 'standing-side-left'], ['keeper_turn_left_front', 'end', 'standard', 'standing-front'],
    ['keeper_sit_side', 'start', 'standard', 'standing-side-right'], ['keeper_sit_side', 'end', 'standard', 'sitting-side-right'],
    ['keeper_sit_front', 'start', 'standard', 'standing-front'], ['keeper_sit_front', 'end', 'standard', 'sitting-front'],
    ['keeper_sit_back', 'start', 'standard', 'standing-back'], ['keeper_sit_back', 'end', 'standard', 'sitting-back'],
    ['keeper_idle', 'start', 'standard', 'standing-front'], ['keeper_idle', 'end', 'standard', 'standing-front'],
    ['keeper_work_back', 'start', 'standard', 'standing-back'], ['keeper_work_back', 'end', 'standard', 'standing-back'],
    ['keeper_cook_back', 'start', 'standard', 'standing-back'], ['keeper_cook_back', 'end', 'standard', 'standing-back'],
    ['keeper_wash_back', 'start', 'standard', 'standing-back'], ['keeper_wash_back', 'end', 'standard', 'standing-back'],
    ['keeper_brush_teeth_back', 'start', 'standard', 'standing-back'], ['keeper_brush_teeth_back', 'end', 'standard', 'standing-back'],
    ['keeper_nap_seated', 'start', 'standard', 'sitting-side-right'], ['keeper_nap_seated', 'end', 'standard', 'sitting-side-right'],
    ['keeper_sitting_turn_back_to_rear', 'start', 'standard', 'sitting-back'], ['keeper_sitting_turn_back_to_rear', 'end', 'standard', 'sitting-rear-right'],
    ['keeper_watch_tv', 'start', 'standard', 'sitting-rear-right'], ['keeper_watch_tv', 'end', 'standard', 'sitting-rear-right'],
    ['keeper_pyjamas_turn_back', 'start', 'light-blue-pyjamas', 'standing-front'], ['keeper_pyjamas_turn_back', 'end', 'light-blue-pyjamas', 'standing-back'],
    ['keeper_get_into_bed', 'start', 'light-blue-pyjamas', 'standing-side-right'], ['keeper_get_into_bed', 'end', 'light-blue-pyjamas', 'lying-side-right'],
    ['keeper_pyjamas_snore', 'start', 'light-blue-pyjamas', 'lying-side-right'], ['keeper_pyjamas_snore', 'end', 'light-blue-pyjamas', 'lying-side-right'],
  ] as const) replaceEnd(assets, clip, end, outfit, pose)
  assets = readAssets()
  for (const a of assets.values()) { enrich(a); writeFileSync(a.jsonPath, JSON.stringify(a.sidecar, null, 2) + '\n') }
  writeAudit(buildAudit(assets))
  validate(assets)
  console.log(`Keeper contract built: ${assets.size} sheets; audit written to docs/KEEPER_NEUTRAL_ENDPOINT_AUDIT.md`)
}
