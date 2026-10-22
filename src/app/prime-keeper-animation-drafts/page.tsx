import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v4.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Feedback-corrected Animation Review V4',
  description: 'Review ten reversible Prime Keeper animation candidates with the continuous rear-task jumper hem correction.',
}

export default function PrimeKeeperAnimationDraftsPage() {
  return <PrimeKeeperDraftReview batch={batch} />
}
