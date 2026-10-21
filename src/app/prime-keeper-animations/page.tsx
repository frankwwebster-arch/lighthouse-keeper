import type { Metadata } from 'next'
import catalogue from '../../../public/prime-keeper-animations/catalogue.json'
import PrimeKeeperAnimationLibrary from '../../prime-keeper-animations/PrimeKeeperAnimationLibrary'
import type { AnimationCatalogue } from '../../prime-keeper-animations/types'

export const metadata: Metadata = {
  title: 'Prime Keeper — Approved Animation Library',
  description: 'Inspect every approved Prime Keeper animation frame by frame and combine clips in a non-destructive sequence sandbox.',
}

export default function PrimeKeeperAnimationsPage() {
  return <PrimeKeeperAnimationLibrary catalogue={catalogue as AnimationCatalogue} />
}

