import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v11.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Complete-arm Choreography Review V11',
  description: 'Review the corrected Prime Keeper rear-task choreography with full arm silhouettes and the exact approved body.',
}

export default function PrimeKeeperAnimationDraftsV11Page() {
  return <PrimeKeeperDraftReview batch={batch} />
}
