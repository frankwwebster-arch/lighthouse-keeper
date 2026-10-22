import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v3.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Feedback-corrected Animation Review V3',
  description: 'Review ten reversible Prime Keeper animation candidates with the passive-colour and rear-work corrections.',
}

export default function PrimeKeeperAnimationDraftsV3Page() {
  return <PrimeKeeperDraftReview batch={batch} />
}
