import { renderToStaticMarkup } from 'react-dom/server'
import { describe, expect, it } from 'vitest'
import { KITCHEN_ROOM } from '../game/kitchenLayout'
import { KitchenRoom, type KitchenRuntimeState } from './KitchenRoom'

const base: KitchenRuntimeState = { cooker: 'standard', fridge: 'standard', cookerTier: 1, fridgeTier: 1 }

describe('approved kitchen runtime room', () => {
  it('renders the six exact fitted cells in binding order', () => {
    const html = renderToStaticMarkup(<KitchenRoom floorY={640} state={base} />)
    expect(html).toContain('data-kitchen-runtime="warm-ligne-claire-v4"')
    expect(html).toContain('viewBox="0 0 772 224"')
    expect((html.match(/data-kitchen-module=/g) ?? []).length).toBe(6)
    for (const [index, name] of KITCHEN_ROOM.moduleOrder.entries()) {
      expect(html).toContain(`data-kitchen-module="${name}"`)
      expect(html).toContain(`href="/sprites/kitchen-v4/off/${name}-off-84x74.png"`)
      expect(html).toContain(`x="${KITCHEN_ROOM.fittedBayOriginsX[index]}"`)
    }
    expect((html.match(/width="84" height="74"/g) ?? []).length).toBe(6)
  })

  it('binds cooker state only to the oven and uses the approved light-only strip', () => {
    const html = renderToStaticMarkup(<KitchenRoom floorY={640} state={{ ...base, cooker: 'broken' }} />)
    expect(html).toContain('/sprites/kitchen-v4/broken/oven-broken-84x74.png')
    expect(html).not.toContain('/sprites/kitchen-v4/dishwasher-broken-red-lights-f40.png')
    expect(html).toContain('/sprites/kitchen-v4/oven-broken-cavity-light-f40.png')
    expect(html).toContain('dur="10s"')
  })

  it('binds fridge states without inventing a fridge animation', () => {
    const html = renderToStaticMarkup(<KitchenRoom floorY={640} state={{ ...base, fridge: 'broken' }} />)
    expect(html).toContain('/sprites/kitchen-v4/broken/fridge-broken-84x74.png')
    expect(html).not.toContain('data-kitchen-light-layer="fridge"')
    expect(html).not.toContain('oven-broken-cavity-light-f40.png')
  })
})
