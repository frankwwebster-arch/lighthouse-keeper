export type PrimeFacing = 'side-right' | 'front' | 'back'

export interface PrimeActionPlan {
  facing: PrimeFacing
  entry: readonly { clip: string; seconds: number }[]
  hold: string
  exit: readonly { clip: string; seconds: number }[]
}

const TURN_FRONT_SECONDS = 8 / 16
const TURN_BACK_SECONDS = 9 / 16
const SIT_SECONDS = 6 / 8

const sideSeat: PrimeActionPlan = {
  facing: 'side-right',
  entry: [{ clip: 'keeper_prime_sit_side-right', seconds: SIT_SECONDS }],
  hold: 'keeper_prime_neutral_sitting-side-right',
  exit: [{ clip: 'keeper_prime_stand_side-right', seconds: SIT_SECONDS }],
}

const frontSeat: PrimeActionPlan = {
  facing: 'front',
  entry: [
    { clip: 'keeper_prime_turn_side-right_to_front', seconds: TURN_FRONT_SECONDS },
    { clip: 'keeper_prime_sit_front', seconds: SIT_SECONDS },
  ],
  hold: 'keeper_prime_neutral_sitting-front',
  exit: [
    { clip: 'keeper_prime_stand_front', seconds: SIT_SECONDS },
    { clip: 'keeper_prime_turn_front_to_side-right', seconds: TURN_FRONT_SECONDS },
  ],
}

const backSeat: PrimeActionPlan = {
  facing: 'back',
  entry: [
    { clip: 'keeper_prime_turn_side-right_to_back', seconds: TURN_BACK_SECONDS },
    { clip: 'keeper_prime_sit_back', seconds: SIT_SECONDS },
  ],
  hold: 'keeper_prime_neutral_sitting-back',
  exit: [
    { clip: 'keeper_prime_stand_back', seconds: SIT_SECONDS },
    { clip: 'keeper_prime_turn_back_to_side-right', seconds: TURN_BACK_SECONDS },
  ],
}

const rearWork: PrimeActionPlan = {
  facing: 'back',
  entry: [{ clip: 'keeper_prime_turn_side-right_to_back', seconds: TURN_BACK_SECONDS }],
  hold: 'keeper_prime_rear_work',
  exit: [{ clip: 'keeper_prime_turn_back_to_side-right', seconds: TURN_BACK_SECONDS }],
}

const sideDarts: PrimeActionPlan = {
  facing: 'side-right',
  entry: [],
  hold: 'keeper_prime_darts_throw',
  exit: [],
}

const SIDE_SEATED = new Set(['tv_watch', 'tv_nature', 'tv_nap', 'read_book', 'play_piano'])
const BACK_SEATED = new Set(['desk_diary'])
const FRONT_SEATED = new Set<string>()
const REAR_WORK = new Set(['cooker_cook', 'cooker_toast', 'wash_basin', 'brush_teeth', 'lamp_light', 'lamp_polish'])
const DARTS = new Set(['darts_throw', 'play_darts'])

export function primeActionPlanFor(action?: string): PrimeActionPlan | null {
  if (!action) return null
  if (SIDE_SEATED.has(action)) return sideSeat
  if (BACK_SEATED.has(action)) return backSeat
  if (FRONT_SEATED.has(action)) return frontSeat
  if (REAR_WORK.has(action)) return rearWork
  if (DARTS.has(action)) return sideDarts
  return null
}

/**
 * Resolve an installed Prime clip for a job without cutting an entry or exit
 * short. Entry is measured from action start; exit is measured backwards from
 * action completion. When a very short job cannot fit both, entry wins.
 */
export function primeActionClipFor(action: string | undefined, elapsedSeconds: number, remainingSeconds: number): string | null {
  const plan = primeActionPlanFor(action)
  if (!plan) return null
  let cursor = 0
  for (const phase of plan.entry) {
    cursor += phase.seconds
    if (elapsedSeconds < cursor) return phase.clip
  }
  const exitSeconds = plan.exit.reduce((sum, phase) => sum + phase.seconds, 0)
  if (remainingSeconds < exitSeconds) {
    let fromEnd = remainingSeconds
    for (let index = plan.exit.length - 1; index >= 0; index -= 1) {
      const phase = plan.exit[index]
      if (fromEnd < phase.seconds) return phase.clip
      fromEnd -= phase.seconds
    }
  }
  return plan.hold
}

export const primeVerticalClipFor = (mode: 'stairs-up' | 'stairs-down' | 'ladder-up' | 'lift') => ({
  'stairs-up': 'keeper_prime_stairs_up',
  'stairs-down': 'keeper_prime_stairs_down',
  'ladder-up': 'keeper_prime_ladder_climb',
  lift: null,
})[mode]

