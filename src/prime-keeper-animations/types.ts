export type AnimationFrame = {
  src: string
  durationMs: number
  label: string
  phase?: string
  flipX?: boolean
}

export type AnimationClip = {
  id: string
  title: string
  version: string
  category: string
  approvedBy: string
  approvedOn: string
  scope: string
  productionState: string
  startPose: string
  endPose: string
  loop: boolean
  reviewUrl: string
  frames: AnimationFrame[]
}

export type AnimationCatalogue = {
  schema: string
  generatedOn: string
  title: string
  summary: {
    approvedPlayableClips: number
    uniqueFrameImages: number
    runtimePromotions: number
    experimentalApprovedProofsExcluded: number
  }
  excludedProofs: Array<{ id: string; title: string; reason: string; reviewUrl: string }>
  clips: AnimationClip[]
}

export type PlayerCommand = { type: 'play' | 'pause' | 'previous' | 'next' | 'restart'; nonce: number }

