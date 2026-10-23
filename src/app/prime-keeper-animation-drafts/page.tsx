import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v11.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Complete-arm Choreography Review V11',
  description: 'Review ten reversible Prime Keeper animation candidates, including the exact approved rear body with complete action-arm silhouettes.',
}

export default function PrimeKeeperAnimationDraftsPage() {
  return <PrimeKeeperDraftReview batch={batch} />
}
