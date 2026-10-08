/**
 * THE PICTURE'S GEOMETRY. One place says where everything stands, so the
 * scene, the walking and the camera agree. Units are the picture's own
 * (a 1200 × 760 stage); the lighthouse is drawn as a cutaway so every room
 * can be seen at once.
 */

import { OBJECTS, START_FLOORS, objectById, type FloorId, type ObjectId, type RoomFloor } from './config'

export const STAGE = { w: 1200, h: 760 }
/** The tower's left edge, so an object's tower-local x becomes a picture x. */
export const TOWER_X = 240
export const INTERIOR = { left: 70, right: 450 }
/** The ground floor's boards, which never move: floors are added above and below it. */
export const GROUND_Y = 640
/** One floor, boards to boards. */
export const FLOOR_STEP = 140
/** The stairs: where one climbs from each floor (tower-local). The lift, once he has it, runs up behind them. */
export const STAIRS_X = 108

/**
 * THE LAYOUT: which floors he has, stacked. Missions add floors, so this
 * changes during play; `applyLayout` rebuilds it and everything below reads
 * it. Floors he has not got take no space (and are not drawn). The order
 * comes from the save (`towerOf` in missions.ts), never from the floor type.
 */
export const FLOOR_Y: Record<FloorId, number> = { ground: 640, living: 500, bedroom: 360, aquarium: 220, weather: 80, lair: 780, lamp: 220, outside: 640 }
/** Bottom to top, ending with the lamp room. */
export const FLOOR_ORDER: FloorId[] = ['ground', 'living', 'bedroom', 'lamp']
export const LAYOUT = {
  /** The rooms he has, bottom to top. */
  rooms: [...START_FLOORS] as RoomFloor[],
  /** Each room's place counted from the ground (0), so stripes follow the world, not the order floors arrived in. */
  slot: { ground: 0, living: 1, bedroom: 2 } as Partial<Record<RoomFloor, number>>,
  lift: false,
  /** The picture's top and bottom: the roof above the lamp room, the deepest floor below. */
  top: 0,
  bottom: STAGE.h,
  /** Bumped on every change, so the screen can catch up (and move the keeper with his floor). */
  version: 0,
}

/**
 * Rebuild the layout: `stack` is the rooms above ground, bottom to top (the
 * lamp room goes on top of them); `below` the ones underground, nearest the
 * ground first. Cheap; does nothing if unchanged.
 */
export function applyLayout(stack: readonly RoomFloor[], below: readonly RoomFloor[], lift: boolean): void {
  const above = [...new Set(stack)]
  const sorted = [...[...below].reverse(), ...above]
  if (sorted.join() === LAYOUT.rooms.join() && lift === LAYOUT.lift && LAYOUT.version > 0) return
  const slot: Partial<Record<RoomFloor, number>> = {}
  above.forEach((f, i) => (slot[f] = i))
  below.forEach((f, i) => (slot[f] = -(i + 1)))
  for (const f of sorted) FLOOR_Y[f] = GROUND_Y - FLOOR_STEP * slot[f]!
  FLOOR_Y.lamp = GROUND_Y - FLOOR_STEP * above.length
  FLOOR_Y.outside = GROUND_Y
  FLOOR_ORDER.splice(0, FLOOR_ORDER.length, ...sorted, 'lamp')
  LAYOUT.rooms = sorted
  LAYOUT.slot = slot
  LAYOUT.lift = lift
  // The lamp room is 140 tall and the roof 80 more (so 0 for the first day); underground floors hang below the ground.
  LAYOUT.top = Math.min(0, FLOOR_Y.lamp - 220)
  LAYOUT.bottom = Math.max(STAGE.h, ...sorted.map((f) => FLOOR_Y[f] + 40))
  LAYOUT.version++
}
applyLayout(START_FLOORS, [], false)

export const worldX = (id: ObjectId): number => {
  const o = objectById(id)
  if (!o) return TOWER_X + 250
  return o.floor === 'outside' ? o.x : TOWER_X + o.x
}
export const floorOf = (id: ObjectId): FloorId => objectById(id)?.floor ?? 'ground'

export interface Point {
  x: number
  floor: FloorId
}

/** The route from one place to another: along the floor, up or down the stairs, along the next floor. */
export function route(from: Point, to: Point): Point[] {
  const out: Point[] = []
  if (from.floor === to.floor) return [to]
  const stairs = TOWER_X + STAIRS_X // also where the lift is
  const door = TOWER_X + 60
  const a = from.floor
  const b = to.floor
  // Going out of the tower or in at the front door.
  if (a === 'outside' && b !== 'outside') {
    out.push({ x: door, floor: 'ground' })
    return [...out, ...route({ x: door, floor: 'ground' }, to)]
  }
  if (b === 'outside') {
    if (a !== 'ground') return [...route(from, { x: door, floor: 'ground' }), to]
    return [{ x: door, floor: 'ground' }, { x: TOWER_X - 40, floor: 'outside' }, to]
  }
  const ia = FLOOR_ORDER.indexOf(a)
  const ib = FLOOR_ORDER.indexOf(b)
  const step = ia < ib ? 1 : -1
  out.push({ x: stairs, floor: a })
  for (let i = ia + step; i !== ib + step; i += step) out.push({ x: stairs, floor: FLOOR_ORDER[i] })
  out.push(to)
  return out
}

/** Up and down by lift is this much quicker than the stairs. */
export const LIFT_FACTOR = 0.25

/** How long a route takes at a given speed (units a second); stairs count for their height. */
export function routeLength(from: Point, path: Point[]): number {
  let len = 0
  let at = from
  for (const p of path) {
    len += at.floor === p.floor ? Math.abs(p.x - at.x) : Math.abs(FLOOR_Y[p.floor] - FLOOR_Y[at.floor]) * (LAYOUT.lift ? LIFT_FACTOR : 0.9)
    at = p
  }
  return len
}

export const feetY = (floor: FloorId) => FLOOR_Y[floor]

/** The point the camera looks at for an object, and how close it comes. */
export function focusFor(id: ObjectId): { x: number; y: number; zoom: number } {
  const o = objectById(id)
  if (!o) return { x: STAGE.w / 2, y: STAGE.h / 2, zoom: 1 }
  return { x: worldX(id), y: FLOOR_Y[o.floor] - 70, zoom: o.zoom }
}

export const ALL_OBJECT_IDS = OBJECTS.map((o) => o.id)
