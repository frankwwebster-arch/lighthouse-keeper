/**
 * The drafted bubble stories and the shared picture library, from
 * data/activity-stories/. Claude adds a story file there and lists it here; a
 * test fails if a file is missing from this list. Frank's edits in the
 * studio are saved separately (as `story-<id>`) and win over these drafts.
 */

import pictures from '../../data/activity-stories/pictures.json'
import gardenBbq from '../../data/activity-stories/stories/garden-bbq.json'
import generalRepair from '../../data/activity-stories/stories/general-repair.json'
import makeSandwich from '../../data/activity-stories/stories/make-sandwich.json'
import washingUp from '../../data/activity-stories/stories/washing-up.json'
import { cleanStory, type Library, type Story } from './format'

export const STORY_FILES = {
  'garden-bbq': gardenBbq,
  'make-sandwich': makeSandwich,
  'washing-up': washingUp,
  'general-repair': generalRepair,
} as const

export const STORY_DRAFTS: Story[] = Object.values(STORY_FILES).map((s) => cleanStory(s)).filter((s): s is Story => !!s)

export const LIBRARY = pictures as unknown as Library
