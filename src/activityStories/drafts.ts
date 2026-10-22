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
import bakeCake from '../../data/activity-stories/stories/bake-cake.json'
import collectEggs from '../../data/activity-stories/stories/collect-eggs.json'
import cookDinner from '../../data/activity-stories/stories/cook-dinner.json'
import fryUp from '../../data/activity-stories/stories/fry-up.json'
import lunch from '../../data/activity-stories/stories/lunch.json'
import makeTea from '../../data/activity-stories/stories/make-tea.json'
import woodwork from '../../data/activity-stories/stories/woodwork.json'
import toast from '../../data/activity-stories/stories/toast.json'
import sweep from '../../data/activity-stories/stories/sweep.json'
import cleanLoo from '../../data/activity-stories/stories/clean-loo.json'
import harvest from '../../data/activity-stories/stories/harvest.json'
import styleReview from '../../data/activity-stories/style-review.json'
import { cleanStory, type Library, type Story, type StyleReview } from './format'

export const STORY_FILES = {
  'garden-bbq': gardenBbq,
  'make-sandwich': makeSandwich,
  'washing-up': washingUp,
  'general-repair': generalRepair,
  'make-tea': makeTea,
  'cook-dinner': cookDinner,
  'fry-up': fryUp,
  lunch,
  'bake-cake': bakeCake,
  'collect-eggs': collectEggs,
  woodwork,
  toast,
  sweep,
  'clean-loo': cleanLoo,
  harvest,
} as const

export const STORY_DRAFTS: Story[] = Object.values(STORY_FILES).map((s) => cleanStory(s)).filter((s): s is Story => !!s)

export const LIBRARY = pictures as unknown as Library
/** Claude's ligne-claire review of each picture's current version. */
export const STYLE_REVIEW = styleReview as unknown as StyleReview
