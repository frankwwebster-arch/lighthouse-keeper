/**
 * The drafted recipes and macros, from data/studio/. Claude and Codex add a
 * JSON file there and list it here; a test fails if a file is missing from
 * this list. Frank's edits in the recipe studio are saved separately and win
 * over these drafts (docs/RECIPES.md).
 */

import enterRoom from '../../data/studio/macros/enter_room.json'
import leaveRoom from '../../data/studio/macros/leave_room.json'
import armchairNap from '../../data/studio/recipes/armchair_nap.json'
import brushTeeth from '../../data/studio/recipes/brush_teeth.json'
import goToBed from '../../data/studio/recipes/go_to_bed.json'
import makeTea from '../../data/studio/recipes/make_tea.json'
import watchTv from '../../data/studio/recipes/watch_tv.json'
import { cleanRecipe, type Recipe } from './recipe'

export const DRAFT_FILES = {
  'macros/enter_room': enterRoom,
  'macros/leave_room': leaveRoom,
  'recipes/armchair_nap': armchairNap,
  'recipes/brush_teeth': brushTeeth,
  'recipes/go_to_bed': goToBed,
  'recipes/make_tea': makeTea,
  'recipes/watch_tv': watchTv,
} as const

export const DRAFTS: Recipe[] = Object.values(DRAFT_FILES).map((d) => cleanRecipe(d)).filter((d): d is Recipe => !!d)
