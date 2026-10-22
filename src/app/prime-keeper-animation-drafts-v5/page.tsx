import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v5.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Feedback-corrected Animation Review V5',
  description: 'Review ten reversible Prime Keeper animation candidates with the moving rear-task hem and clean authority-trouser correction.',
}

export default function PrimeKeeperAnimationDraftsV5Page() {
  return <PrimeKeeperDraftReview batch={batch} />
}
