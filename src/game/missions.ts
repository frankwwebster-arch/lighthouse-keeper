/**
 * MISSIONS. One at a time, in the order of `MISSIONS` (config.ts). Each has a
 * few goals counted from what happens in the game; finishing one unlocks a
 * floor (it arrives furnished) or the lift.
 *
 * Pure: the engine feeds in what happened and applies what comes back.
 */

import { DEFAULT_RULES, FLOOR_LEVELS, MISSIONS, OBJECTS, START_FLOORS, type MissionDef, type MissionEvent, type ObjectId, type RoomFloor, type Rules, type UnlockId } from './config'
import type { Happening, State } from './engine'

export interface MissionState {
  done: string[]
  /** `<mission>:<goal index>` → how many so far. */
  progress: Record<string, number>
}

export const freshMissions = (): MissionState => ({ done: [], progress: {} })

/** The mission being worked on now (undefined when they are all done). */
export function activeMission(m: MissionState): MissionDef | undefined {
  return MISSIONS.find((x) => !m.done.includes(x.id) && (!x.after || m.done.includes(x.after)))
}

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
 * Count events towards the active mission. Returns the new state and the
 * mission it finished, if it did. With no events it just checks: a target the
 * grown-ups have lowered may already be met.
 */
export function countEvents(ms: MissionState, events: readonly MissionEvent[], dials?: MissionDials): { missions: MissionState; finished?: MissionDef } {
  const m = activeMission(ms)
  if (!m) return { missions: ms }
  let progress = ms.progress
  m.goals.forEach((g, i) => {
    const n = events.filter((e) => e === g.event).length
    if (!n) return
    const k = goalKey(m, i)
    // Kept uncapped (to a point), so raising a target later still counts what he has done.
    progress = { ...progress, [k]: Math.min(999, (progress[k] ?? 0) + n) }
  })
  const next = progress === ms.progress ? ms : { ...ms, progress }
  if (goalsOf(m, next, dials).every((g) => g.met)) return { missions: { ...next, done: [...next.done, m.id] }, finished: m }
  return { missions: next }
}

/** The floors with rooms that he has, bottom to top. */
export function roomFloors(unlocked: readonly UnlockId[]): RoomFloor[] {
  const have = new Set<string>([...START_FLOORS, ...unlocked])
  return (Object.keys(FLOOR_LEVELS) as RoomFloor[]).filter((f) => have.has(f)).sort((a, b) => FLOOR_LEVELS[a] - FLOOR_LEVELS[b])
}

const isRoomFloor = (f: string): f is RoomFloor => f in FLOOR_LEVELS

/** Is this thing in his lighthouse yet? (Objects on locked floors are not.) */
export function objectAvailable(s: Pick<State, 'unlocked'>, id: ObjectId): boolean {
  if (id === 'here') return true
  const o = OBJECTS.find((x) => x.id === id)
  if (!o) return false
  return !isRoomFloor(o.floor) || START_FLOORS.includes(o.floor) || s.unlocked.includes(o.floor as UnlockId)
}
