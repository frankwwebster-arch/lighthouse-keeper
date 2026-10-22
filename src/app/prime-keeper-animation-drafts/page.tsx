import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v1.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Morning Animation Drafts V1',
  description: 'Frame-by-frame review and sandbox for versioned, reversible Prime Keeper animation drafts.',
}

export default function PrimeKeeperAnimationDraftsPage() {
  return <PrimeKeeperDraftReview batch={batch} />
}
