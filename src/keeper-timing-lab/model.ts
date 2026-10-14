export type TimingPhase = 'walk' | 'deceleration' | 'settle' | 'turn' | 'frontHold'

export type TimingProfile = {
  walkFps: number
  decelerationFps: number
  settleMs: number
  turnFps: number
  frontHoldMs: number
}

export type TimingFrame = {
  id: string
  src: string
  phase: TimingPhase
  phaseLabel: string
  pose: string
  dx: number
  x: number
}

export type TimingClip = {
  id: string
  title: string
  description: string
  outfit: string
  status: string
  sourceRegister: string
  sourceRegisterSha256: string
  baseline: TimingProfile
  recommended: TimingProfile
  frames: TimingFrame[]
  distanceHighResolutionPixels: number
  artworkAuthorities: Record<string, { approval: string; approvalSha256: string; acceptedLimitation?: string }>
  endpointContract: Record<string, unknown>
  acceptedVisualLimitation: string
}

export type TimingPreset = { id: string; name: string; description: string; profile: TimingProfile }
export type LoopSection = { id: string; label: string; phases: TimingPhase[] }
export type TimingCatalogue = {
  version: number
  platformId: string
  title: string
  updatedOn: string
  principles: Record<string, string>
  defaults: TimingProfile
  presets: TimingPreset[]
  clips: TimingClip[]
  loopSections: LoopSection[]
}

export type SavedProposal = { id: string; name: string; clipId: string; savedAt: string; profile: TimingProfile }

export const phaseLabels: Record<TimingPhase, string> = {
  walk: 'Walk',
  deceleration: 'Deceleration',
  settle: 'Neutral beat',
  turn: 'Turn',
  frontHold: 'Front hold',
}

export function sectionFrames(frames: TimingFrame[], section: LoopSection) {
  return frames.filter((frame) => section.phases.includes(frame.phase))
}

export function phaseFrameCounts(frames: TimingFrame[]) {
  return frames.reduce<Record<TimingPhase, number>>((counts, frame) => {
    counts[frame.phase] += 1
    return counts
  }, { walk: 0, deceleration: 0, settle: 0, turn: 0, frontHold: 0 })
}

export function frameDurationMs(frame: TimingFrame, profile: TimingProfile, counts: Record<TimingPhase, number>) {
  if (frame.phase === 'walk') return 1000 / profile.walkFps
  if (frame.phase === 'deceleration') return 1000 / profile.decelerationFps
  if (frame.phase === 'turn') return 1000 / profile.turnFps
  if (frame.phase === 'settle') return profile.settleMs / Math.max(1, counts.settle)
  return profile.frontHoldMs / Math.max(1, counts.frontHold)
}

export function profileDurationMs(frames: TimingFrame[], profile: TimingProfile) {
  const counts = phaseFrameCounts(frames)
  return frames.reduce((total, frame) => total + frameDurationMs(frame, profile, counts), 0)
}

export function changedProfileFields(baseline: TimingProfile, candidate: TimingProfile) {
  return (Object.keys(baseline) as (keyof TimingProfile)[]).filter((key) => baseline[key] !== candidate[key])
}

export function clampProfile(profile: TimingProfile): TimingProfile {
  const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value))
  return {
    walkFps: clamp(profile.walkFps, 4, 16),
    decelerationFps: clamp(profile.decelerationFps, 4, 16),
    settleMs: clamp(profile.settleMs, 0, 500),
    turnFps: clamp(profile.turnFps, 4, 16),
    frontHoldMs: clamp(profile.frontHoldMs, 125, 1500),
  }
}
