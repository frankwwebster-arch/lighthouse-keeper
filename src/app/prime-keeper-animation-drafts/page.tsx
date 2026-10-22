import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v2.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Expanded Animation Review V2',
  description: 'Review ten reversible Prime Keeper animation and choreography candidates frame by frame.',
}

export default function PrimeKeeperAnimationDraftsPage() {
  return <PrimeKeeperDraftReview batch={batch} />
}
