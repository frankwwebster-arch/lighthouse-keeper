/**
 * Locomotion data: Keeper Prime poses, root-motion tables and transition timing, as recorded in
 * Codex's registers. Nothing here is authored by Claude: approved values are copied from the
 * approval registers (tests re-read the registers and PNGs to prove they still agree), and the
 * candidate values are Codex's proposal in docs/CODEX_TO_CLAUDE_DIRECT_OBJECT_LOCOMOTION_2026-10-14.md.
 */
import type { Ku } from './units'

/** The 256 × 320 density-8 registration cell. The root sits at x 128; y 320 is the anchor row. */
export const CELL = { width: 256, height: 320, anchorX: 128, anchorY: 320 } as const

export type PoseId =
  | 'neutral'
  | 'bridge15' | 'bridge50' | 'bridge75'
  | 'walkF1' | 'walkF2' | 'walkF3' | 'walkF4' | 'walkF5' | 'walkF6' | 'walkF7' | 'walkF8'
  | 'f5stopA' | 'f5stopB' | 'f5stopC'

export interface Pose {
  id: PoseId
  label: string
  clip: string
  frame: number
  /** Repository path of the exact approved PNG, or null while the pose is not drawn. */
  file: string | null
  sha256: string | null
  /** Strict (alpha > 0) bounds in the cell, [x0, y0, x1, y1), measured from the PNG; null while not drawn. Used for door hiding. */
  alphaBounds: readonly [number, number, number, number] | null
  /** The register's opaqueBoundsExclusive (significant alpha). Used for wall and furniture clearance. */
  opaqueBounds: readonly [number, number, number, number] | null
  /** Codex: "the same rule works in reverse and for mirrored left travel". */
  mirrorSafe: boolean
  /** Walk V6 frame number, for phase-aware stops. */
  gaitFrame?: number
}

const BRIDGE = 'art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v1/drafts/frames/keeper_prime_stop-to-walk-right_f'
const WALK = 'art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames/keeper_prime_walk-right_f'

const walk = (n: number, sha256: string, alphaBounds: Pose['alphaBounds'], opaqueBounds: Pose['opaqueBounds']): Pose => ({
  id: `walkF${n}` as PoseId, label: `Walk V6 F${n}`, clip: 'keeper_prime_walk-right', frame: n, file: `${WALK}${n}.png`, sha256, alphaBounds, opaqueBounds, mirrorSafe: true, gaitFrame: n,
})

export const POSES: Record<PoseId, Pose> = {
  neutral: { id: 'neutral', label: 'Exact side-right neutral', clip: 'keeper_prime_master-neutral-standing-side-right', frame: 1, file: 'art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png', sha256: 'a172a8a01a387a21d14c092d2a9eb53b938a44574279108a5776e2cc67f2fff3', alphaBounds: [77, 18, 179, 316], opaqueBounds: [77, 18, 179, 316], mirrorSafe: true },
  bridge15: { id: 'bridge15', label: 'Stop ↔ walk bridge 15%', clip: 'keeper_prime_stop-to-walk-right', frame: 2, file: `${BRIDGE}2.png`, sha256: 'e54546ba14b4e5f7f042677f7c5babc83df99943d1bc0a8f482f7188d0c96930', alphaBounds: [53, 14, 221, 318], opaqueBounds: [80, 17, 219, 316], mirrorSafe: true },
  bridge50: { id: 'bridge50', label: 'Stop ↔ walk bridge 50%', clip: 'keeper_prime_stop-to-walk-right', frame: 3, file: `${BRIDGE}3.png`, sha256: '0169b3642905389dfe1846b054ce463653708d971aef7a588f834dcbf8c9714c', alphaBounds: [51, 15, 225, 317], opaqueBounds: [63, 17, 223, 315], mirrorSafe: true },
  bridge75: { id: 'bridge75', label: 'Stop ↔ walk bridge 75%', clip: 'keeper_prime_stop-to-walk-right', frame: 4, file: `${BRIDGE}4.png`, sha256: '9f4192beb8fecbc80de4530725a9431a4df8ad9adc3b86df66ad7159728c2b29', alphaBounds: [28, 15, 242, 319], opaqueBounds: [42, 17, 230, 317], mirrorSafe: true },
  walkF1: walk(1, '0e80ea65610452c93a1ebe48424dddcc5709a77340b4bc1e93dddff38809e656', [41, 18, 233, 316], [41, 18, 233, 316]),
  walkF2: walk(2, '2b8e91de747b527dc3f1d6e5aa6e95753c4f360b9d542534a286b819eace15bf', [34, 16, 212, 316], [61, 16, 210, 316]),
  walkF3: walk(3, 'b376254e9c29da38c80973c09a4242ddfc29b2ff3a70b724e97510cc90ac91d4', [82, 17, 203, 316], [84, 17, 203, 316]),
  walkF4: walk(4, '982646b0b0e6f3f986fc42ef8f9d1abd542ac417e2e2061c9f3aec9fd4e3fa2b', [43, 17, 232, 316], [46, 17, 232, 316]),
  walkF5: walk(5, '545e7338151e6e5a5bb66cd236955cc497229f317b982ba0e8469e5ed4104549', [47, 23, 234, 316], [47, 23, 234, 316]),
  walkF6: walk(6, '17d007eee75c2e86d8f02c05ae6d30740abcab4ec59c1ad9603c41383e9ffc52', [61, 22, 194, 316], [63, 22, 194, 316]),
  walkF7: walk(7, 'dbf5b3849624cec7244322d630841895c733b6a1143c891a790a15a8fb57a0df', [57, 23, 200, 316], [77, 23, 200, 316]),
  walkF8: walk(8, 'cf8c53e7ffa703a5947a0f4b81a89526cae64f494a8cf37303877fe683689b61', [40, 23, 229, 316], [66, 23, 229, 316]),
  // Codex's requested Walk F5 → neutral bridge: three poses, not drawn yet (gate 3).
  f5stopA: { id: 'f5stopA', label: 'F5 stop bridge pose 1 (not drawn)', clip: 'keeper_prime_walk-f5-to-stop-right', frame: 1, file: null, sha256: null, alphaBounds: null, opaqueBounds: null, mirrorSafe: true },
  f5stopB: { id: 'f5stopB', label: 'F5 stop bridge pose 2 (not drawn)', clip: 'keeper_prime_walk-f5-to-stop-right', frame: 2, file: null, sha256: null, alphaBounds: null, opaqueBounds: null, mirrorSafe: true },
  f5stopC: { id: 'f5stopC', label: 'F5 stop bridge pose 3 (not drawn)', clip: 'keeper_prime_walk-f5-to-stop-right', frame: 3, file: null, sha256: null, alphaBounds: null, opaqueBounds: null, mirrorSafe: true },
}

export const WALK_CYCLE: readonly PoseId[] = ['walkF1', 'walkF2', 'walkF3', 'walkF4', 'walkF5', 'walkF6', 'walkF7', 'walkF8']

export interface Bridge {
  /** Row poses in play order; a start ends on Walk F1, a stop ends on the neutral. */
  poses: readonly PoseId[]
  /** Root delta applied on each row, in the direction of travel. */
  dx: readonly Ku[]
}

export type StopPhase = 'F1' | 'F5'

export interface RootProfile {
  id: 'approved-v1' | 'candidate-42' | 'candidate-42-f5'
  label: string
  status: 'approved' | 'candidate'
  /** Frank's review gates still needed before this profile may be the default. */
  awaiting: readonly string[]
  source: { register: string | null; registerSha256: string | null; note: string }
  start: Bridge
  walkDx: Ku
  /** Stops by the gait frame they leave from. null: that stop does not exist in this profile. */
  stops: Record<StopPhase, Bridge | null>
}

const START_POSES: readonly PoseId[] = ['bridge15', 'bridge50', 'bridge75', 'walkF1']
const F1_STOP_POSES: readonly PoseId[] = ['bridge75', 'bridge50', 'bridge15', 'neutral']
const F5_STOP_POSES: readonly PoseId[] = ['f5stopA', 'f5stopB', 'f5stopC', 'neutral']

export const APPROVED_STOP_WALK_STOP_REGISTER = 'art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v2/batch-register.json'
export const APPROVED_STOP_WALK_STOP_REGISTER_SHA256 = '3cbdc5ea7f7467ea18a353d5abc8581c1d6afd088316570c629241612bc2542c'
export const APPROVED_WALK_REGISTER = 'art/drafts/keeper-prime-walk-2026-10-14-v7/batch-register.json'
export const APPROVED_WALK_REGISTER_SHA256 = 'ad788fb923009c6dd97840d3c4ae91c6e8084ef699ab6637bb2738b9532cb342'
export const DIRECT_LOCOMOTION_NOTE = 'docs/CODEX_TO_CLAUDE_DIRECT_OBJECT_LOCOMOTION_2026-10-14.md'

/** Approved by Frank on 14 October 2026: exact stop → walk → stop V1 (route V2 is its approval record). */
export const APPROVED_PROFILE: RootProfile = {
  id: 'approved-v1',
  label: 'Approved stop → walk → stop V1 (2, 6, 12, 18 / 18, 12, 6, 2; stop from F1 only)',
  status: 'approved',
  awaiting: [],
  source: { register: APPROVED_STOP_WALK_STOP_REGISTER, registerSha256: APPROVED_STOP_WALK_STOP_REGISTER_SHA256, note: 'approvedCandidate.rootMotion' },
  start: { poses: START_POSES, dx: [2, 6, 12, 18] },
  walkDx: 21,
  stops: { F1: { poses: F1_STOP_POSES, dx: [18, 12, 6, 2] }, F5: null },
}

/** Codex's gate-1 candidate: the same pixels, re-timed 42 ku bridges. Not approved. */
export const CANDIDATE_PROFILE: RootProfile = {
  id: 'candidate-42',
  label: 'Candidate 42 ku bridges (3, 7, 13, 19 / 19, 13, 7, 3; stop from F1 only)',
  status: 'candidate',
  awaiting: ['Gates 1–2: Frank reviews the re-timed 42 ku root-motion candidate'],
  source: { register: null, registerSha256: null, note: `${DIRECT_LOCOMOTION_NOTE}, "Recommended resolution"; no candidate register exists yet` },
  start: { poses: START_POSES, dx: [3, 7, 13, 19] },
  walkDx: 21,
  stops: { F1: { poses: F1_STOP_POSES, dx: [19, 13, 7, 3] }, F5: null },
}

/** The candidate plus Codex's proposed Walk F5 → neutral stop (gate 3). Not drawn, not approved. */
export const CANDIDATE_F5_PROFILE: RootProfile = {
  ...CANDIDATE_PROFILE,
  id: 'candidate-42-f5',
  label: 'Candidate 42 ku bridges plus the proposed Walk F5 stop',
  awaiting: [...CANDIDATE_PROFILE.awaiting, 'Gate 3: Codex draws the Walk F5 → neutral bridge and Frank approves it'],
  source: { ...CANDIDATE_PROFILE.source, note: `${DIRECT_LOCOMOTION_NOTE}, "The required opposite-foot stop"; not drawn yet` },
  stops: { F1: CANDIDATE_PROFILE.stops.F1, F5: { poses: F5_STOP_POSES, dx: [19, 13, 7, 3] } },
}

export const PROFILES: readonly RootProfile[] = [APPROVED_PROFILE, CANDIDATE_PROFILE, CANDIDATE_F5_PROFILE]

/**
 * What Frank has approved, recorded from the repository on 14 October 2026 (main at b042bde): no
 * root-motion candidate register and no F5 bridge exist yet, so neither is approved.
 */
export const APPROVALS = { rootCandidate: false, f5Stop: false, recordedOn: '2026-10-14', evidence: 'main at b042bde: no candidate register, no F5 bridge draft' } as const

export function profileFor(approvals: { rootCandidate: boolean; f5Stop: boolean }): RootProfile {
  if (!approvals.rootCandidate) return APPROVED_PROFILE
  return approvals.f5Stop ? CANDIDATE_F5_PROFILE : CANDIDATE_PROFILE
}

/** The only profile anything may present as the default: what Frank has approved. */
export const DEFAULT_PROFILE = profileFor(APPROVALS)

export const sum = (xs: readonly number[]): number => xs.reduce((a, b) => a + b, 0)

/** Fast Timing V1 (data/keeper_timing_policy.json), approved 14 October 2026. Acceleration plays at the walk rate. */
export const FAST_TIMING_V1 = { walkFps: 10, decelerationFps: 12, settleMs: 0, turnFps: 16, frontHoldMs: 625 } as const
export type TransitionTiming = typeof FAST_TIMING_V1

/** Reads the root-motion schedule from a stop → walk → stop register (the approval record or a candidate). */
export function rootTableFromRegister(register: unknown): { start: Ku[]; walk: Ku; stop: Ku[] } {
  const r = register as { approvedCandidate?: { rootMotion?: unknown }; rootMotion?: unknown }
  const rm = (r.approvedCandidate?.rootMotion ?? r.rootMotion) as Record<string, unknown> | undefined
  if (!rm) throw new Error('register has no rootMotion')
  const nums = (v: unknown) => (Array.isArray(v) && v.every(Number.isInteger) ? (v as number[]) : null)
  const start = nums(rm.accelerationDeltasHighResolutionPixels)
  const stop = nums(rm.decelerationDeltasHighResolutionPixels)
  const walk = rm.walkDeltaHighResolutionPixels
  if (!start || !stop || !Number.isInteger(walk)) throw new Error('register rootMotion is incomplete')
  return { start, walk: walk as number, stop }
}
