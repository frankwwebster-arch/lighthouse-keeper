import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v6.json'
import corrections from '../../../art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v9/corrections.json'
import RearTaskAlignmentWorkbench from '../../prime-keeper-drafts/RearTaskAlignmentWorkbench'

export const metadata: Metadata = {
  title: 'Prime Keeper — Manual rear-task alignment',
  description: 'Manually align the exact Prime Keeper rear-task torso and approved legs, one frame at a time.',
}

const sequence = batch.sequences.find((item) => item.id === 'rear-work-turn-return-v1')
if (!sequence) throw new Error('Rear-task sequence is missing')

const correctionByPosition = new Map(corrections.frames.map((item) => [item.position, item]))
const frames = sequence.frames.slice(10, 31).map((frame, offset) => {
  const position = offset + 11
  return {
    position,
    label: frame.label,
    torsoSrc: frame.src,
    torsoSha256: frame.sha256,
    defaultLegsX: correctionByPosition.get(position)?.rootDx ?? 0,
  }
})

export default function PrimeKeeperRearTaskAlignmentPage() {
  return <RearTaskAlignmentWorkbench
    frames={frames}
    legsSrc="/keeper-review/keeper-prime-morning-drafts-v6/assets/frame-31dbac4efc00089f.png"
    legsSha256="31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35"
  />
}
