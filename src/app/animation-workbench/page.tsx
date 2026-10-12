import type { Metadata } from 'next'
import AnimationWorkbench from '../../animation-workbench/AnimationWorkbench'

export const metadata: Metadata = {
  title: 'Keeper Animation Workbench — Draft & Final',
  description: 'A separate non-destructive Draft and Final review platform for Keeper animation frames, loops and visible transition routes.',
}

export default function AnimationWorkbenchPage() {
  return <AnimationWorkbench />
}
