/**
 * MISSIONS. Every mission is open at once and counts in parallel, so the
 * floors arrive in whatever order he finishes them (some wait for the tower to
 * be tall enough: `needsFloors`). Each has a few goals counted from what
 * happens in the game; finishing one brings a floor (it arrives furnished,
 * the next morning) or the lift.
 *
 * Also here: how the tower stacks, from the save's own middle order.
 *
 * Pure: the engine feeds in what happened and applies what comes back.
 */

import { ALL_ROOM_FLOORS, BASE_FLOOR, DEFAULT_RULES, MISSIONS, OBJECTS, START_FLOORS, TOP_FLOOR, UNDERGROUND, type MissionDef, type MissionEvent, type ObjectId, type RoomFloor, type Rules, type UnlockId } from './config'
import type { Happening, State } from './engine'

export interface MissionState {
  done: string[]
  /** `<mission>:<goal index>` → how many so far. */
  progress: Record<string, number>
}

export const freshMissions = (): MissionState => ({ done: [], progress: {} })

/** The missions he can work on now: not done, and the tower is tall enough. */
export function openMissions(m: MissionState, floors: number): MissionDef[] {
  return MISSIONS.filter((x) => !m.done.includes(x.id) && floors >= (x.needsFloors ?? 0))
}

/** Has he made a start on it (a secret mission stays a mystery until then)? */
export const started = (m: MissionDef, ms: MissionState) => m.goals.some((_, i) => (ms.progress[goalKey(m, i)] ?? 0) > 0)

/** What a happening counts as. */
export function eventsOf(h: Pick<Happening, 'kind' | 'id' | 'safe' | 'correct'>): MissionEvent[] {
  switch (h.kind) {
    case 'done':
      return h.id ? [`done:${h.id}`] : []
    case 'ship':
      return h.safe ? ['ship_safe'] : []
    case 'caller_met':
      return ['caller_met']
    case 'repaired':
      return ['repaired']
    case 'upgraded':
      return ['upgraded']
    case 'quiz':
      return h.correct ? ['quiz_right'] : []
    default:
      return []
  }
}

export const goalKey = (m: MissionDef, i: number) => `${m.id}:${i}`

/**
 * The grown-ups' dials: first for every mission at once (a size percentage and
 * a reward), then, where set, for one goal or one mission, which wins.
 */
type MissionDials = Partial<Pick<Rules, 'missionScale' | 'missionReward' | 'missionGoals' | 'missionRewards'>>
/** A goal's target from the overall size dial alone. */
export const scaledTarget = (m: MissionDef, i: number, dials?: MissionDials) => Math.max(1, Math.round((m.goals[i].count * (dials?.missionScale ?? 100)) / 100))
export const goalTarget = (m: MissionDef, i: number, dials?: MissionDials) => Math.max(1, dials?.missionGoals?.[goalKey(m, i)] ?? scaledTarget(m, i, dials))
export const rewardOf = (m: MissionDef, dials?: MissionDials) => dials?.missionRewards?.[m.id] ?? dials?.missionReward ?? DEFAULT_RULES.missionReward

/** How far along a mission's goals are. */
export function goalsOf(m: MissionDef, ms: MissionState, dials?: MissionDials) {
  return m.goals.map((g, i) => {
    const count = goalTarget(m, i, dials)
    const got = Math.min(count, ms.progress[goalKey(m, i)] ?? 0)
    return { ...g, count, got, met: got >= count }
  })
}

/**
 * Count events towards every open mission. Returns the new state and the
 * missions it finished (often none). With no events it just checks: a target
 * the grown-ups have lowered may already be met.
 */
export function countEvents(ms: MissionState, events: readonly MissionEvent[], dials: MissionDials | undefined, floors: number): { missions: MissionState; finished: MissionDef[] } {
  const open = openMissions(ms, floors)
  let progress = ms.progress
  for (const m of open) {
    m.goals.forEach((g, i) => {
      const n = events.filter((e) => e === g.event).length
      if (!n) return
      const k = goalKey(m, i)
      // Kept uncapped (to a point), so raising a target later still counts what he has done.
      progress = { ...progress, [k]: Math.min(999, (progress[k] ?? 0) + n) }
    })
  }
  const next = progress === ms.progress ? ms : { ...ms, progress }
  const finished = open.filter((m) => goalsOf(m, next, dials).every((g) => g.met))
  return finished.length ? { missions: { ...next, done: [...next.done, ...finished.map((m) => m.id)] }, finished } : { missions: next, finished }
}

// ─── The tower ───────────────────────────────────────────────────────────────

const isUnderground = (f: RoomFloor) => UNDERGROUND.includes(f)
const isRoomFloor = (f: string): f is RoomFloor => ALL_ROOM_FLOORS.includes(f as RoomFloor)

/** A floor a mission brings that goes into the middle of the tower (not the lift, not underground). */
export const isMiddleFloor = (u: UnlockId): u is UnlockId & RoomFloor => u !== 'lift' && !isUnderground(u as RoomFloor)

/** The tower he has: rooms bottom to top above ground (kitchen first, bedroom last), and any below ground. */
export function towerOf(s: Pick<State, 'unlocked' | 'middle'>): { stack: RoomFloor[]; below: RoomFloor[] } {
  return {
    stack: [BASE_FLOOR, ...s.middle, TOP_FLOOR],
    below: UNDERGROUND.filter((f) => s.unlocked.includes(f as UnlockId)),
  }
}

/** Floors above ground (what `needsFloors` counts). */
export const floorCount = (s: Pick<State, 'unlocked' | 'middle'>) => towerOf(s).stack.length

/** Put a new floor in the middle at the place `at` (0 is just above the kitchen). */
export function insertFloor(middle: readonly RoomFloor[], floor: RoomFloor, at: number): RoomFloor[] {
  if (middle.includes(floor)) return [...middle]
  const i = Math.max(0, Math.min(middle.length, Math.floor(at)))
  return [...middle.slice(0, i), floor, ...middle.slice(i)]
}

/** Is this thing in his lighthouse yet? (Objects on floors he has not got are not.) */
export function objectAvailable(s: Pick<State, 'unlocked'>, id: ObjectId): boolean {
  if (id === 'here') return true
  const o = OBJECTS.find((x) => x.id === id)
  if (!o) return false
  return !isRoomFloor(o.floor) || START_FLOORS.includes(o.floor) || s.unlocked.includes(o.floor as UnlockId)
}
