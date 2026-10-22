import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v7.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Feedback-corrected Animation Review V7',
  description: 'Review ten reversible Prime Keeper animation candidates with a single authority-owned rear jumper hem.',
}

export default function PrimeKeeperAnimationDraftsV7Page() {
  return <PrimeKeeperDraftReview batch={batch} />
}
