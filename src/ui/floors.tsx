import type { ObjectId, RoomFloor } from '../game/config'
import { FLOOR_Y, LAYOUT, TOWER_X } from '../game/world'
import { Sprite } from './Sprite'

export const CORE = {
  x: TOWER_X + 40,
  width: 440,
  interiorX: TOWER_X + 48,
  interiorWidth: 420,
  bandHeight: 140,
  beamHeight: 12,
} as const

export interface FloorModuleSpec {
  id: RoomFloor
  number: number
  name: string
  roomSprite: string
  wall: string
  objects: readonly ObjectId[]
  zones: readonly { id: string; fromX: number; toX: number }[]
  partitionX?: number
}

export const PLAYABLE_FLOORS: readonly FloorModuleSpec[] = [
  {
    id: 'ground',
    number: 1,
    name: 'Kitchen',
    roomSprite: 'room_kitchen',
    wall: '#f2e6c9',
    objects: ['door', 'fridge', 'cooker', 'broom', 'petbowl'],
    zones: [{ id: 'kitchen', fromX: 52, toX: 468 }],
  },
  {
    id: 'living',
    number: 2,
    name: 'Living room',
    roomSprite: 'room_living',
    wall: '#cfe3d3',
    objects: ['tv', 'bookshelf', 'piano'],
    zones: [{ id: 'living', fromX: 52, toX: 468 }],
  },
  {
    id: 'bedroom',
    number: 3,
    name: 'Bedroom + en suite',
    roomSprite: 'room_bedroom',
    wall: '#e5d4ea',
    objects: ['bed', 'phone', 'desk', 'basin', 'toilet'],
    zones: [
      { id: 'bedroom', fromX: 52, toX: 348 },
      { id: 'ensuite', fromX: 348, toX: 468 },
    ],
    partitionX: 348,
  },
] as const

/**
 * Floors that missions unlock (wiring by Claude; looks are Codex's). They
 * arrive furnished: their objects are in config.ts. Plain stand-in walls
 * until their room art is in.
 */
export const UNLOCKABLE_FLOORS: readonly FloorModuleSpec[] = [
  { id: 'aquarium', number: 4, name: 'Aquarium', roomSprite: 'room_aquarium', wall: '#c9d2d6', objects: ['tank', 'fishfood'], zones: [{ id: 'aquarium', fromX: 52, toX: 468 }] },
  { id: 'weather', number: 5, name: 'Weather station', roomSprite: 'room_weather', wall: '#c9d2d6', objects: ['barometer', 'radio'], zones: [{ id: 'weather', fromX: 52, toX: 468 }] },
  { id: 'lair', number: -1, name: 'Hidden lair', roomSprite: 'room_lair', wall: '#b9bec2', objects: ['console', 'gadgets'], zones: [{ id: 'lair', fromX: 52, toX: 468 }] },
]

/** The floors he has, bottom to top, as the layout stacks them. */
export function floorsOnShow(): FloorModuleSpec[] {
  const all = [...PLAYABLE_FLOORS, ...UNLOCKABLE_FLOORS]
  return LAYOUT.rooms.map((id) => all.find((f) => f.id === id)!).filter(Boolean)
}

/** Reserved geometry for the later diving-board changing-room bay. It belongs to the bedroom, so it rises with it as the tower grows (heights read the live layout). */
export const DIVING_EXTENSION = {
  parentFloor: 'bedroom' as const,
  side: 'right' as const,
  innerDoor: { x: 468, get floorY() { return FLOOR_Y.bedroom }, get keeperUsePoint() { return { x: 452, y: FLOOR_Y.bedroom } } },
  hiddenZone: { fromX: 469, toX: 523, visible: false },
  exteriorDoor: { x: 524, get floorY() { return FLOOR_Y.bedroom }, get exitPoint() { return { x: 540, y: FLOOR_Y.bedroom } } },
  sequence: ['inner-door-close', 'keeper-hidden', 'costume-swap-sfx', 'exterior-door-open', 'dive-suit-exit'] as const,
} as const

export function stripeSpriteAt(runtimeY: number): 'tower_stripe_red' | 'tower_stripe_white' {
  const stripeIndex = Math.floor(runtimeY / 32)
  return stripeIndex % 2 === 0 ? 'tower_stripe_red' : 'tower_stripe_white'
}

function StripeBands({ floor }: { floor: FloorModuleSpec }) {
  const y = FLOOR_Y[floor.id] - CORE.bandHeight
  return (
    <g aria-hidden="true" clipPath={`url(#floor-band-${floor.id})`}>
      <defs><clipPath id={`floor-band-${floor.id}`}><rect x={CORE.x} y={y} width={CORE.width} height={CORE.bandHeight} /></clipPath></defs>
      {Array.from({ length: 5 }, (_, index) => {
        const stripeY = y + index * 32
        const name = stripeSpriteAt(stripeY)
        const fallback = name === 'tower_stripe_red' ? '#c8463c' : '#f3e7cc'
        return (
          <Sprite key={stripeY} name={name} x={CORE.x + CORE.width / 2} y={stripeY + 32} w={CORE.width} h={32}>
            <rect x={CORE.x} y={stripeY} width={CORE.width} height={32} fill={fallback} />
          </Sprite>
        )
      })}
    </g>
  )
}

function LivingFurniture() {
  return (
    <g aria-hidden="true" transform={`translate(${TOWER_X + 188} ${FLOOR_Y.living})`}>
      <path d="M-46-30h92v30h-92z" fill="#9e543b" stroke="#542b25" strokeWidth={4} />
      <path d="M-38-46h76v28h-76z" fill="#bd6b4e" stroke="#542b25" strokeWidth={4} />
      <path d="M-48-38h14v34h-14zM34-38h14v34h-14z" fill="#87442f" />
    </g>
  )
}

export function FloorModule({ floor }: { floor: FloorModuleSpec }) {
  const y = FLOOR_Y[floor.id] - CORE.bandHeight
  return (
    <g className={`floor-module floor-${floor.id}`} data-floor={floor.number}>
      <StripeBands floor={floor} />
      <Sprite name={floor.roomSprite} x={CORE.interiorX + CORE.interiorWidth / 2} y={FLOOR_Y[floor.id]} w={CORE.interiorWidth} h={CORE.bandHeight}>
        <>
          <rect x={CORE.interiorX} y={y} width={CORE.interiorWidth} height={CORE.bandHeight} fill={floor.wall} />
          <rect x={CORE.x} y={FLOOR_Y[floor.id] - 8} width={CORE.width} height={12} fill="#725336" stroke="#14243a" strokeWidth={4} />
        </>
      </Sprite>
      {floor.id === 'living' && <LivingFurniture />}
    </g>
  )
}
