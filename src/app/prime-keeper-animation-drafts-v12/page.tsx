import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v12.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Intact Rear-work Review V12',
  description: 'Review the corrected Prime Keeper rear-task choreography built from complete, intact cooking poses.',
}

export default function PrimeKeeperAnimationDraftsV12Page() {
  return <PrimeKeeperDraftReview batch={batch} />
}
