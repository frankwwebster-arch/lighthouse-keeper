/**
 * Starting room and furniture records. Widths are the best measurements available today: the studio
 * categories (data/studio/categories) where they exist, otherwise the floor-asset catalogue frame widths
 * (art/source/floor-asset-catalogue/spaces.json). Codex refits them as object art lands. Anchors sit at
 * each item's measured centre (Frank, 14 October), so offsetSteps is 0 throughout.
 */
import { standardRoom, type Catalogue, type Door, type ObjectType, type Placement, type Room, type TierGeometry } from './room'
import { lpToKu } from './units'

/**
 * The studio's placeholder door until door art exists (src/studio/recipe.ts DOOR): a 4 lp jamb and a
 * 24 lp open leaf, 44 lp tall, drawn in front of him, with everything beyond the wall clipped.
 */
export function leftDoor(id = 'door'): Door {
  return {
    id,
    wall: 'left',
    clearKu: lpToKu(46),
    aperture: { from: -lpToKu(4), to: 0 },
    occlusion: { from: -lpToKu(4), to: lpToKu(24), topKu: lpToKu(44) },
    hiddenPocketEdgeKu: -lpToKu(4),
  }
}

const box = (tier: number, label: string, sprite: string, wLp: number, hLp: number, solid: boolean, contacts: Record<string, number> = {}): TierGeometry => {
  const half = lpToKu(wLp / 2)
  return { tier, label, sprite, renderAnchor: [-wLp / 2, 0], footprint: [-half, half], solid: solid ? [{ from: -half, to: half, topLp: hLp }] : [], contacts }
}

const CATALOGUE_SRC = 'art/source/floor-asset-catalogue/spaces.json (catalogue frame width)'

export const CATALOGUE: Catalogue = {
  tv: {
    id: 'tv', label: 'TV', lane: 'back', source: CATALOGUE_SRC,
    anchors: [{ id: 'use', offsetSteps: 0, facing: 'right', entryPose: 'standing-side-right', exitPose: 'standing-side-right', action: { id: 'switch-on', clips: [], endpoint: 'anchor' } }],
    tiers: [box(1, 'TV', 'obj_tv', 28, 23, false)],
  },
  bookshelf: {
    id: 'bookshelf', label: 'Bookshelf', lane: 'back', source: CATALOGUE_SRC,
    // A back-facing action: turn to the back with the approved Turn V9, browse, turn back.
    anchors: [{ id: 'browse', offsetSteps: 0, facing: 'right', entryPose: 'standing-side-right', exitPose: 'standing-side-right', action: { id: 'browse-books', face: 'back', clips: [], endpoint: 'anchor' } }],
    tiers: [box(1, 'Bookshelf', 'obj_bookshelf', 20, 28, false)],
  },
  piano: {
    id: 'piano', label: 'Piano', lane: 'back', source: CATALOGUE_SRC,
    anchors: [{ id: 'play', offsetSteps: 0, facing: 'right', entryPose: 'standing-side-right', exitPose: 'standing-side-right', action: { id: 'play-piano', clips: [], endpoint: 'anchor' } }],
    tiers: [box(1, 'Piano', 'obj_piano', 25, 18, false)],
  },
  armchair: {
    id: 'armchair', label: 'Armchair', lane: 'back', source: 'data/studio/categories/armchair.json (side-on in the walking lane, so solid; seat 11 lp on every tier)',
    // The seated action: the sit bridge owns the move to the seat contact and the stand bridge returns exactly.
    anchors: [{ id: 'seat', offsetSteps: 0, facing: 'right', entryPose: 'standing-side-right', exitPose: 'standing-side-right', action: { id: 'sit', clips: [], endpoint: 'anchor' } }],
    tiers: [
      box(1, 'Basic armchair', 'obj_armchair', 26, 24, true, { seat: 11 }),
      box(2, 'Rocking chair', 'obj_armchair_t2', 30, 27, true, { seat: 11 }),
      box(3, 'Lazyboy-style recliner', 'obj_armchair_t3', 36, 26, true, { seat: 11 }),
    ],
  },
  fridge: { id: 'fridge', label: 'Fridge', lane: 'back', source: CATALOGUE_SRC, anchors: [{ id: 'use', offsetSteps: 0, facing: 'right', entryPose: 'standing-side-right', exitPose: 'standing-side-right' }], tiers: [box(1, 'Fridge', 'obj_fridge', 12, 24, false)] },
  cooker: {
    id: 'cooker', label: 'Cooker', lane: 'back', source: 'data/studio/categories/cooker.json (tier widths; anchors at the measured centre, not the studio dx)',
    anchors: [{ id: 'use', offsetSteps: 0, facing: 'right', entryPose: 'standing-side-right', exitPose: 'standing-side-right' }],
    tiers: [box(1, 'Basic oven', 'obj_cooker', 28, 22, false), box(2, 'Two-oven range', 'obj_cooker_t2', 42, 24, false), box(3, 'Fancy professional kitchen', 'obj_cooker_t3', 46, 28, false)],
  },
  broom: { id: 'broom', label: 'Broom', lane: 'back', source: CATALOGUE_SRC, anchors: [{ id: 'use', offsetSteps: 0, facing: 'right', entryPose: 'standing-side-right', exitPose: 'standing-side-right' }], tiers: [box(1, 'Broom', 'obj_broom', 8, 23, false)] },
  petbowl: { id: 'petbowl', label: 'Pet bowl', lane: 'back', source: CATALOGUE_SRC, anchors: [{ id: 'use', offsetSteps: 0, facing: 'right', entryPose: 'standing-side-right', exitPose: 'standing-side-right' }], tiers: [box(1, 'Pet bowl', 'obj_petbowl', 10, 5, false)] },
}

export const objectType = (id: string): ObjectType => CATALOGUE[id]

/**
 * The real room for Codex's gate-5 proof at the base width. packRoom over every order: bookshelf, TV,
 * piano, then the solid armchair at the far end (so it blocks no route) is the only order that fits
 * every armchair tier. 1208 ku is the last line he can stop on: stopping, his boot reaches 89 ku past
 * the anchor, more than the 84 ku left by the next line.
 */
export const LIVING_ROOM: Room = standardRoom('living', 'Living room', 0, leftDoor())

export const LIVING_PLACEMENTS: Placement[] = [
  { object: 'bookshelf', room: 'living', xKu: 452, anchor: 'browse', tier: 1 },
  { object: 'tv', room: 'living', xKu: 704, anchor: 'use', tier: 1 },
  { object: 'piano', room: 'living', xKu: 956, anchor: 'play', tier: 1 },
  { object: 'armchair', room: 'living', xKu: 1208, anchor: 'seat', tier: 1 },
]

/** A compact starting kitchen for shuffle and upgrade tests; every cooker tier fits where it stands. */
export const KITCHEN: Room = standardRoom('kitchen', 'Kitchen', 0, leftDoor())

export const KITCHEN_PLACEMENTS: Placement[] = [
  { object: 'fridge', room: 'kitchen', xKu: 452, anchor: 'use', tier: 1 },
  { object: 'broom', room: 'kitchen', xKu: 536, anchor: 'use', tier: 1 },
  { object: 'petbowl', room: 'kitchen', xKu: 620, anchor: 'use', tier: 1 },
  { object: 'cooker', room: 'kitchen', xKu: 872, anchor: 'use', tier: 1 },
]
