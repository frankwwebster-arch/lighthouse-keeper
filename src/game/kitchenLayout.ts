/**
 * Runtime registration for the approved Kitchen Warm Ligne-Claire V4 room.
 *
 * The approved art keeps its native 772 x 224 coordinate system and exact
 * 84 x 74 fitted bodies. The current fixed-width floor presents that complete
 * coordinate system through one uniform scale, so no bay is independently
 * stretched or repositioned.
 */
export const KITCHEN_ROOM = {
  sourceSize: [772, 224],
  bodySize: [84, 74],
  bodyY: 134,
  floorSupportY: 208,
  keeperStopTurnY: 218,
  fittedBayOriginsX: [84, 168, 252, 336, 420, 504],
  fittedBayCentresX: [126, 210, 294, 378, 462, 546],
  moduleOrder: ['cupboard', 'drawers', 'sink', 'dishwasher', 'oven', 'fridge'],
  viewportTowerX: 48,
  viewportWidth: 420,
} as const

export type KitchenModule = (typeof KITCHEN_ROOM.moduleOrder)[number]

export const KITCHEN_ROOM_SCALE = KITCHEN_ROOM.viewportWidth / KITCHEN_ROOM.sourceSize[0]

/** Convert an approved-room x coordinate to the existing tower-local world. */
export function kitchenTowerX(roomX: number): number {
  return KITCHEN_ROOM.viewportTowerX + roomX * KITCHEN_ROOM_SCALE
}

export const KITCHEN_OBJECT_X = {
  door: kitchenTowerX(42),
  cooker: kitchenTowerX(KITCHEN_ROOM.fittedBayCentresX[4]),
  fridge: kitchenTowerX(KITCHEN_ROOM.fittedBayCentresX[5]),
  broom: kitchenTowerX(646),
  petbowl: kitchenTowerX(730),
} as const
