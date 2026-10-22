import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v8.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Feedback-corrected Animation Review V8',
  description: 'Review ten reversible Prime Keeper animation candidates with an exact torso-to-legs outline join.',
}

export default function PrimeKeeperAnimationDraftsV8Page() {
  return <PrimeKeeperDraftReview batch={batch} />
}
