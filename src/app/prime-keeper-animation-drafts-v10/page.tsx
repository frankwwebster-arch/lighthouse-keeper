import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v10.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Approved-body Arm Choreography Review V10',
  description: 'Review the rear-task animation with the exact approved Prime body and action-only arm substitutions.',
}

export default function PrimeKeeperAnimationDraftsV10Page() {
  return <PrimeKeeperDraftReview batch={batch} />
}
