/**
 * THE PICTURE'S GEOMETRY. One place says where everything stands, so the
 * scene, the walking and the camera agree. Units are the picture's own
 * (a 1200 × 760 stage); the lighthouse is drawn as a cutaway so every room
 * can be seen at once.
 */

import { OBJECTS, objectById, type FloorId, type ObjectId } from './config'

export const STAGE = { w: 1200, h: 760 }
/** The tower's left edge, so an object's tower-local x becomes a picture x. */
export const TOWER_X = 240
export const INTERIOR = { left: 70, right: 450 }
/** Where each floor's boards are (the keeper's feet). */
export const FLOOR_Y: Record<FloorId, number> = { ground: 640, living: 500, bedroom: 360, lamp: 220, outside: 640 }
export const FLOOR_ORDER: FloorId[] = ['ground', 'living', 'bedroom', 'lamp']
/** The stairs: where one climbs from each floor (tower-local). */
export const STAIRS_X = 108

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
  const stairs = TOWER_X + STAIRS_X
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

/** How long a route takes at a given speed (units a second); stairs count for their height. */
export function routeLength(from: Point, path: Point[]): number {
  let len = 0
  let at = from
  for (const p of path) {
    len += at.floor === p.floor ? Math.abs(p.x - at.x) : Math.abs(FLOOR_Y[p.floor] - FLOOR_Y[at.floor]) * 0.9
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
