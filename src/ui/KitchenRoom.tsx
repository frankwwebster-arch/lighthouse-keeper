import { useId } from 'react'
import { KITCHEN_ROOM, KITCHEN_ROOM_SCALE, type KitchenModule } from '../game/kitchenLayout'
import { TOWER_X } from '../game/world'
import type { ObjectVisualState } from './art'

const PUBLIC_ROOT = '/sprites/kitchen-v4'
const ANIMATION_CELL = [92, 82] as const
const ANIMATION_FRAMES = 40
const ANIMATION_FPS = 4

type KitchenState = 'off' | 'on' | 'broken'

export interface KitchenRuntimeState {
  cooker: ObjectVisualState
  fridge: ObjectVisualState
  cookerTier: number
  fridgeTier: number
}

const runtimeState = (state: ObjectVisualState): KitchenState => state === 'standard' ? 'off' : state

function bodyUrl(name: KitchenModule, state: KitchenState): string {
  return `${PUBLIC_ROOT}/${state}/${name}-${state}-84x74.png`
}

function BrokenLightLayer({ name, originX }: { name: 'dishwasher' | 'oven'; originX: number }) {
  const clipId = `kitchen-light-${useId().replaceAll(':', '')}`
  const x = originX - 4
  const y = KITCHEN_ROOM.bodyY - 4
  const file = name === 'dishwasher'
    ? 'dishwasher-broken-red-lights-f40.png'
    : 'oven-broken-cavity-light-f40.png'
  const values = Array.from({ length: ANIMATION_FRAMES }, (_, frame) => `${-frame * ANIMATION_CELL[0]} 0`).join(';')
  return (
    <g clipPath={`url(#${clipId})`} data-kitchen-light-layer={name}>
      <defs><clipPath id={clipId}><rect x={x} y={y} width={ANIMATION_CELL[0]} height={ANIMATION_CELL[1]} /></clipPath></defs>
      <image
        href={`${PUBLIC_ROOT}/${file}`}
        x={x}
        y={y}
        width={ANIMATION_CELL[0] * ANIMATION_FRAMES}
        height={ANIMATION_CELL[1]}
        preserveAspectRatio="none"
      >
        <animateTransform
          attributeName="transform"
          type="translate"
          values={values}
          dur={`${ANIMATION_FRAMES / ANIMATION_FPS}s`}
          calcMode="discrete"
          repeatCount="indefinite"
        />
      </image>
    </g>
  )
}

/**
 * The approved 772 x 224 room coordinate system, fitted into the unchanged
 * 420-unit runtime floor. Every body remains an exact 84 x 74 source cell;
 * the room receives one uniform presentation transform at the outer boundary.
 */
export function KitchenRoom({ floorY, state }: { floorY: number; state: KitchenRuntimeState }) {
  const states: Record<KitchenModule, KitchenState> = {
    cupboard: 'off',
    drawers: 'off',
    sink: 'off',
    dishwasher: 'off',
    oven: runtimeState(state.cooker),
    fridge: runtimeState(state.fridge),
  }
  const height = KITCHEN_ROOM.sourceSize[1] * KITCHEN_ROOM_SCALE
  const y = floorY - KITCHEN_ROOM.keeperStopTurnY * KITCHEN_ROOM_SCALE

  return (
    <svg
      className="kitchen-runtime-v4"
      x={KITCHEN_ROOM.viewportTowerX + TOWER_X}
      y={y}
      width={KITCHEN_ROOM.viewportWidth}
      height={height}
      viewBox={`0 0 ${KITCHEN_ROOM.sourceSize[0]} ${KITCHEN_ROOM.sourceSize[1]}`}
      preserveAspectRatio="xMinYMin meet"
      overflow="visible"
      aria-hidden="true"
      data-kitchen-runtime="warm-ligne-claire-v4"
    >
      {KITCHEN_ROOM.moduleOrder.map((name, index) => {
        const moduleState = states[name]
        const originX = KITCHEN_ROOM.fittedBayOriginsX[index]
        return (
          <g key={name} data-kitchen-module={name} data-state={moduleState}>
            <image
              href={bodyUrl(name, moduleState)}
              x={originX}
              y={KITCHEN_ROOM.bodyY}
              width={KITCHEN_ROOM.bodySize[0]}
              height={KITCHEN_ROOM.bodySize[1]}
              preserveAspectRatio="none"
            />
            {moduleState === 'broken' && (name === 'dishwasher' || name === 'oven') && <BrokenLightLayer name={name} originX={originX} />}
          </g>
        )
      })}
      {state.cookerTier > 1 && <text x={KITCHEN_ROOM.fittedBayCentresX[4]} y={126} textAnchor="middle" className="floor-label tier-tag">T{state.cookerTier}</text>}
      {state.fridgeTier > 1 && <text x={KITCHEN_ROOM.fittedBayCentresX[5]} y={126} textAnchor="middle" className="floor-label tier-tag">T{state.fridgeTier}</text>}
    </svg>
  )
}
