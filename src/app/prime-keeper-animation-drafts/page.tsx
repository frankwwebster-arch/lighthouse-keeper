import type { Metadata } from 'next'
import batch from '../../../data/keeper_prime_animation_drafts_v9.json'
import PrimeKeeperDraftReview from '../../prime-keeper-drafts/PrimeKeeperDraftReview'

export const metadata: Metadata = {
  title: 'Prime Keeper — Feedback-corrected Animation Review V9',
  description: 'Review ten reversible Prime Keeper animation candidates with one continuous moving rear jumper hem.',
}

export default function PrimeKeeperAnimationDraftsPage() {
  return <PrimeKeeperDraftReview batch={batch} manualAlignmentHref="/prime-keeper-rear-task-alignment" />
}
