import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v12.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Intact Rear-work Review V12',
  description: 'Review ten reversible Prime Keeper animation candidates, including the rear task rebuilt from complete cooking poses.',
}

export default function PrimeKeeperAnimationDraftsPage() {
  return <PrimeKeeperDraftReview batch={batch} />
}
