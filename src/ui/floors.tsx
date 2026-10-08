import type { FloorId, ObjectId } from '../game/config'
import { FLOOR_Y, TOWER_X } from '../game/world'

export const CORE = {
  x: TOWER_X + 40,
  width: 440,
  interiorX: TOWER_X + 48,
  interiorWidth: 420,
  bandHeight: 140,
  beamHeight: 12,
} as const

export interface FloorModuleSpec {
  id: Extract<FloorId, 'ground' | 'living' | 'bedroom'>
  number: 1 | 2 | 3
  name: string
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
    wall: '#f2e6c9',
    objects: ['door', 'fridge', 'cooker', 'broom', 'petbowl'],
    zones: [{ id: 'kitchen', fromX: 52, toX: 468 }],
  },
  {
    id: 'living',
    number: 2,
    name: 'Living room',
    wall: '#cfe3d3',
    objects: ['tv', 'bookshelf', 'piano'],
    zones: [{ id: 'living', fromX: 52, toX: 468 }],
  },
  {
    id: 'bedroom',
    number: 3,
    name: 'Bedroom + en suite',
    wall: '#e5d4ea',
    objects: ['bed', 'phone', 'desk', 'basin', 'toilet'],
    zones: [
      { id: 'bedroom', fromX: 52, toX: 348 },
      { id: 'ensuite', fromX: 348, toX: 468 },
    ],
    partitionX: 348,
  },
] as const

/** Reserved geometry for the later Floor 3 diving-board changing-room bay. */
export const DIVING_EXTENSION = {
  parentFloor: 'bedroom' as const,
  side: 'right' as const,
  innerDoor: { x: 468, floorY: FLOOR_Y.bedroom, keeperUsePoint: { x: 452, y: FLOOR_Y.bedroom } },
  hiddenZone: { fromX: 469, toX: 523, visible: false },
  exteriorDoor: { x: 524, floorY: FLOOR_Y.bedroom, exitPoint: { x: 540, y: FLOOR_Y.bedroom } },
  sequence: ['inner-door-close', 'keeper-hidden', 'costume-swap-sfx', 'exterior-door-open', 'dive-suit-exit'] as const,
} as const

function StripePiers({ floor }: { floor: FloorModuleSpec }) {
  const y = FLOOR_Y[floor.id] - CORE.bandHeight
  const stripe = floor.number % 2 === 1 ? '#c8463c' : '#f3e7cc'
  return (
    <g aria-hidden="true">
      <rect x={CORE.x} y={y} width={12} height={CORE.bandHeight} fill={stripe} />
      <rect x={CORE.x + CORE.width - 12} y={y} width={12} height={CORE.bandHeight} fill={stripe} />
      <path d={`M${CORE.x} ${y}h12v${CORE.bandHeight}h-12M${CORE.x + CORE.width} ${y}h-12v${CORE.bandHeight}h12`} fill="none" stroke="#14243a" strokeWidth={4} />
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

function BedroomDetails() {
  return (
    <g aria-hidden="true">
      <rect x={TOWER_X + 352} y={FLOOR_Y.bedroom - 136} width={116} height={132} fill="#c9e3df" />
      <path d={`M${TOWER_X + 348} ${FLOOR_Y.bedroom - 140}v140`} stroke="#14243a" strokeWidth={4} />
      <path d={`M${TOWER_X + 348} ${FLOOR_Y.bedroom - 76}v76h36`} fill="none" stroke="#e9f3ef" strokeWidth={8} />
      <rect x={TOWER_X + 358} y={FLOOR_Y.bedroom - 128} width={98} height={16} fill="#7fb7af" opacity={0.55} />
    </g>
  )
}

export function FloorModule({ floor }: { floor: FloorModuleSpec }) {
  const y = FLOOR_Y[floor.id] - CORE.bandHeight
  return (
    <g className={`floor-module floor-${floor.id}`} data-floor={floor.number}>
      <rect x={CORE.interiorX} y={y} width={CORE.interiorWidth} height={CORE.bandHeight} fill={floor.wall} />
      <StripePiers floor={floor} />
      <rect x={CORE.x} y={FLOOR_Y[floor.id] - 8} width={CORE.width} height={12} fill="#725336" stroke="#14243a" strokeWidth={4} />
      <text x={CORE.x + 22} y={y + 22} className="floor-label">{floor.number} · {floor.name}</text>
      {floor.id === 'living' && <LivingFurniture />}
      {floor.id === 'bedroom' && <BedroomDetails />}
    </g>
  )
}
