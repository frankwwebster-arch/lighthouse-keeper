import type { Metadata } from 'next'
import TimingLab from '../../keeper-timing-lab/TimingLab'

export const metadata: Metadata = {
  title: 'Keeper Timing Lab',
  description: 'Tune Keeper animation timing independently from immutable approved artwork.',
}

export default function KeeperTimingLabPage() {
  return <TimingLab />
}
