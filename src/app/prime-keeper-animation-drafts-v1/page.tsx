import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v1.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Morning Animation Drafts V1',
  description: 'Immutable first Prime Keeper morning animation review batch.',
}

export default function PrimeKeeperAnimationDraftsV1Page() {
  return <PrimeKeeperDraftReview batch={batch} />
}
