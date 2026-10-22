import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v6.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Feedback-corrected Animation Review V6',
  description: 'Review ten reversible Prime Keeper animation candidates with a tapered rear-task root and clean authority lower body.',
}

export default function PrimeKeeperAnimationDraftsPage() {
  return <PrimeKeeperDraftReview batch={batch} />
}
