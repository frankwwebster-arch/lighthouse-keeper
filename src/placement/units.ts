/**
 * One coordinate contract (docs/architecture/FURNITURE_PLACEMENT_AND_LOCOMOTION.md, section 1).
 * Every model quantity is an integer in Keeper units (ku): one pixel of the 256 × 320
 * density-8 Keeper cell. 1 lp = 8 ku, 1 su = 2 ku. Conversion happens only at the boundaries below.
 */

/** An integer number of Keeper units. */
export type Ku = number

export const KU_PER_LP = 8
export const KU_PER_SU = 2
/** One step, Walk F1 → F5, and the anchor lattice pitch: 10.5 lp. */
export const STEP_KU = 84
/** Fast Timing V1 frame rates all divide 240 (10, 12 and 16 fps), so time is held in integer ticks. */
export const TICKS_PER_SECOND = 240

export class UnitError extends Error {}

/** Throws unless n is an integer: a non-integer model quantity is a contract failure. */
export function assertKu(n: number, label = 'value'): Ku {
  if (!Number.isInteger(n)) throw new UnitError(`${label} must be a whole number of ku, got ${n}`)
  return n
}

/** Import boundary: logical pixels (halves allowed) to ku. */
export const lpToKu = (lp: number): Ku => assertKu(lp * KU_PER_LP, `${lp} lp`)

export const kuToLp = (ku: Ku): number => ku / KU_PER_LP

/**
 * Render boundary: room-local ku to stage units. Halves of a stage unit are kept, so density-8 art
 * is never re-snapped to whole lp (Sprite.tsx rounds legacy art; the Keeper must bypass that).
 */
export const kuToStageSu = (roomLeftSu: number, xKu: Ku): number => roomLeftSu + xKu / KU_PER_SU

/** Legacy migration boundary: game stage units (config.ts) to room-local ku, once. */
export const stageSuToKu = (roomLeftSu: number, su: number): Ku => assertKu((su - roomLeftSu) * KU_PER_SU, `${su} su`)

export const ticksForFps = (fps: number): number => {
  const t = TICKS_PER_SECOND / fps
  if (!Number.isInteger(t)) throw new UnitError(`${fps} fps does not divide ${TICKS_PER_SECOND} ticks per second`)
  return t
}
