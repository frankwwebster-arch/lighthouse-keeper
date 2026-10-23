import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v10.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Approved-body Arm Choreography Review V10',
  description: 'Review ten reversible Prime Keeper animation candidates, including the exact approved rear body with action-only arm substitutions.',
}

export default function PrimeKeeperAnimationDraftsPage() {
  return <PrimeKeeperDraftReview batch={batch} />
}
