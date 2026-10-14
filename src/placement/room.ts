/**
 * Room, furniture and placement records (plan sections 2 and 3, and Codex's 172 × 56 room-grid
 * handoff agreed by Frank on 14 October). Pure data and arithmetic; no UI. Only the Keeper's
 * interaction anchors snap to the 84 ku lattice; furniture keeps its real dimensions.
 */
import { STEP_KU, assertKu, lpToKu, type Ku } from './units'

/** Standard room geometry. The room origin is the stair-side inside wall; the stair core occupies −304..0 ku. */
export const ROOM_HEIGHT_KU = lpToKu(56)
export const STAIR_CORE_KU = lpToKu(38)
/** No furniture footprint may intrude into the first 368 ku (46 lp) from the stair-side wall. */
export const DOORWAY_EXCLUSION_KU = lpToKu(46)
/** Width tiers: base 172 lp, then each whole-lighthouse expansion adds 21 lp (two lattice intervals). */
export const STANDARD_WIDTHS_KU = [lpToKu(172), lpToKu(193), lpToKu(214)] as const
export type WidthTier = 0 | 1 | 2
/** Anchors snap to 368 + 84n in every standard room, i.e. origin 368 mod 84 = 32 ku. */
export const STANDARD_LATTICE_ORIGIN = DOORWAY_EXCLUSION_KU % STEP_KU

export type Facing = 'left' | 'right'
export type Lane = 'back' | 'front'

/** Half-open [from, to) in room-local ku. */
export interface Interval { from: Ku; to: Ku }

export const overlaps = (a: Interval, b: Interval) => a.from < b.to && b.from < a.to
export const inside = (a: Interval, outer: Interval) => a.from >= outer.from && a.to <= outer.to

/**
 * A doorway, with Codex's four measurements kept separate. A left door sits on the wall at x 0 and a
 * right door on the wall at x width; everything beyond its wall is clipped from view.
 */
export interface Door {
  id: string
  wall: 'left' | 'right'
  /** 1. Clear area: no furniture within this distance of the wall (Frank's 46 lp). */
  clearKu: Ku
  /** 2. Aperture: the visible opening in the wall. */
  aperture: Interval
  /**
   * 3. Occlusion mask: the in-room span drawn in front of him (jamb and open leaf) and its height.
   * Together with the clipped region beyond the wall, it hides any composite lying wholly on the
   * wall side of the mask's inner edge and no taller than topKu.
   */
  occlusion: Interval & { topKu: Ku }
  /** 4. Hidden pocket: root positions beyond this edge (towards the wall, unbounded) where he may start, end or transfer. */
  hiddenPocketEdgeKu: Ku
}

export interface Room {
  id: string
  label: string
  /** Walls at 0 and widthKu. Expansion moves only the far wall. */
  widthKu: Ku
  heightKu: Ku
  /** The active width tier for standard rooms; null for separate geometry (the inset lamp room). */
  widthTier: WidthTier | null
  /** 0–83 ku from the stair-side wall: lattice line n stands at latticeOrigin + 84n. */
  latticeOrigin: Ku
  doors: Door[]
}

export interface Solid { from: Ku; to: Ku; topLp: number }

export interface TierGeometry {
  tier: number
  sprite: string
  label: string
  /** Where the art sits relative to the placement point, in lp. */
  renderAnchor: [number, number]
  /** [left, right] ku around the placement point; left is negative. May be asymmetric and may grow by tier. */
  footprint: [Ku, Ku]
  /** Intervals he may not walk into, relative to the placement point. */
  solid: Solid[]
  /** Seat, surface, handle… heights in lp. Equal for every tier. */
  contacts: Record<string, number>
  effectOrigin?: [number, number]
  bubbleOrigin?: [number, number]
}

/** A zero-root turn or action clip, as rows of one clip. */
export interface ClipRef {
  clip: string
  frames: number
  /** Playback rate; turns use Fast Timing V1 instead. */
  fps?: number
  /** Per-frame root delta in the direction he faces; omitted means zero on every frame. */
  dx?: Ku[]
  approved: boolean
  source?: string
}

/** An action performed at an anchor (Codex's universal action-anchor contract). */
export interface ActionSpec {
  id: string
  /** A zero-root facing turn before the action and its reverse after. */
  face?: 'back' | 'front'
  clips: ClipRef[]
  /** 'anchor': returns to the same neutral at the same anchor. Otherwise a reviewed held-prop or environment endpoint. */
  endpoint: 'anchor' | { reviewed: string; pose: string }
}

export interface KeeperUseAnchor {
  id: string
  /** Whole 84 ku steps from the placement point; 0 by default (Frank: the measured centre). */
  offsetSteps: number
  facing: Facing
  entryPose: string
  exitPose: string
  outfit?: string
  prop?: string
  action?: ActionSpec
}

export interface ObjectType {
  id: string
  label: string
  lane: Lane
  /** Invariant across tiers. */
  anchors: KeeperUseAnchor[]
  tiers: TierGeometry[]
  /** Where the dimensions came from, until Codex measures the art. */
  source: string
}

/** What the save file stores: integer ku, never rounded CSS pixels. */
export interface Placement {
  object: string
  room: string
  /** Room-local x of the selected interaction anchor, on the lattice. */
  xKu: Ku
  /** The selected interaction-anchor id. */
  anchor: string
  tier: number
}

export type Catalogue = Record<string, ObjectType>

export const spotX = (room: Room, spot: number): Ku => assertKu(room.latticeOrigin + STEP_KU * spot, 'spot')
export const spotOf = (room: Room, xKu: Ku): number => (xKu - room.latticeOrigin) / STEP_KU

/** Every lattice line inside the walls, as lattice indices. */
export function spots(room: Room): number[] {
  const out: number[] = []
  for (let n = 0; spotX(room, n) <= room.widthKu; n++) out.push(n)
  return out
}

/** A standard stacked-floor room at a width tier, with its door on the stair-side wall. */
export function standardRoom(id: string, label: string, widthTier: WidthTier, door: Door): Room {
  return { id, label, widthKu: STANDARD_WIDTHS_KU[widthTier], heightKu: ROOM_HEIGHT_KU, widthTier, latticeOrigin: STANDARD_LATTICE_ORIGIN, doors: [door] }
}

/** Expansion moves only the far wall: origin, doorway exclusion and every coordinate stay put. */
export function widenRoom(room: Room, widthTier: WidthTier): Room {
  if (room.widthTier === null) throw new Error(`${room.id} is not a standard room`)
  if (widthTier < room.widthTier) throw new Error('rooms never shrink')
  return { ...room, widthTier, widthKu: STANDARD_WIDTHS_KU[widthTier] }
}

export const onLattice = (room: Room, xKu: Ku) => (((xKu - room.latticeOrigin) % STEP_KU) + STEP_KU) % STEP_KU === 0

export function tierOf(type: ObjectType, tier: number): TierGeometry {
  const t = type.tiers.find((g) => g.tier === tier)
  if (!t) throw new Error(`${type.id} has no tier ${tier}`)
  return t
}

export const footprintAt = (g: TierGeometry, xKu: Ku): Interval => ({ from: xKu + g.footprint[0], to: xKu + g.footprint[1] })
export const solidsAt = (g: TierGeometry, xKu: Ku): Interval[] => g.solid.map((s) => ({ from: xKu + s.from, to: xKu + s.to }))

export interface PlacedAnchor {
  object: string
  anchor: KeeperUseAnchor
  xKu: Ku
}

export const anchorsAt = (type: ObjectType, xKu: Ku): PlacedAnchor[] =>
  type.anchors.map((anchor) => ({ object: type.id, anchor, xKu: xKu + STEP_KU * anchor.offsetSteps }))

export function anchorOf(type: ObjectType, id: string): KeeperUseAnchor {
  const a = type.anchors.find((x) => x.id === id)
  if (!a) throw new Error(`${type.id} has no anchor ${id}`)
  return a
}

/** The object's placement point: the selected anchor's x less its whole-step offset. */
export const placementPoint = (type: ObjectType, p: Placement): Ku => p.xKu - STEP_KU * anchorOf(type, p.anchor).offsetSteps

/** Places an object by its selected anchor's lattice index. */
export const placeAt = (room: Room, object: string, anchor: string, spot: number, tier = 1): Placement => ({ object, room: room.id, xKu: spotX(room, spot), anchor, tier })

/** Door clear area as a room-local interval. */
export const doorClear = (room: Room, d: Door): Interval => (d.wall === 'left' ? { from: 0, to: d.clearKu } : { from: room.widthKu - d.clearKu, to: room.widthKu })

/** x of the door's wall. */
export const doorWallX = (room: Room, d: Door): Ku => (d.wall === 'left' ? 0 : room.widthKu)

export function doorOf(room: Room, id: string): Door {
  const d = room.doors.find((x) => x.id === id)
  if (!d) throw new Error(`${room.id} has no door ${id}`)
  return d
}

/** The direction he walks to come in through a door. */
export const inwardFacing = (d: Door): Facing => (d.wall === 'left' ? 'right' : 'left')
export const dirOf = (f: Facing): 1 | -1 => (f === 'right' ? 1 : -1)
export const opposite = (f: Facing): Facing => (f === 'right' ? 'left' : 'right')

// ── save / load ──

export interface SavedLayout {
  /** The active width tier shared by all standard floors. */
  widthTier: WidthTier
  placements: Placement[]
}

/** Placements in a canonical order with a fixed key order, so identical layouts serialise byte-identically. */
export function canonicalPlacements(ps: readonly Placement[]): Placement[] {
  return [...ps]
    .map((p) => ({ object: p.object, room: p.room, xKu: p.xKu, anchor: p.anchor, tier: p.tier }))
    .sort((a, b) => (a.room < b.room ? -1 : a.room > b.room ? 1 : a.xKu - b.xKu || (a.object < b.object ? -1 : a.object > b.object ? 1 : 0)))
}

export const serializeLayout = (l: SavedLayout): string => JSON.stringify({ widthTier: l.widthTier, placements: canonicalPlacements(l.placements) })

export function parseLayout(text: string): SavedLayout {
  const raw = JSON.parse(text) as { widthTier?: unknown; placements?: unknown }
  if (raw.widthTier !== 0 && raw.widthTier !== 1 && raw.widthTier !== 2) throw new Error('widthTier must be 0, 1 or 2')
  if (!Array.isArray(raw.placements)) throw new Error('placements must be an array')
  const placements = raw.placements.map((r, i) => {
    const o = r as Record<string, unknown>
    if (typeof o.object !== 'string' || typeof o.room !== 'string' || typeof o.anchor !== 'string' || !Number.isInteger(o.xKu) || !Number.isInteger(o.tier)) throw new Error(`placement ${i} is malformed`)
    return { object: o.object, room: o.room, xKu: o.xKu as number, anchor: o.anchor, tier: o.tier as number }
  })
  return { widthTier: raw.widthTier, placements: canonicalPlacements(placements) }
}
