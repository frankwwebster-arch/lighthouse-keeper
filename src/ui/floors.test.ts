import { describe, expect, it } from 'vitest'
import { BREAKABLE_OBJECTS, OBJECTS } from '../game/config'
import { CORE, DIVING_EXTENSION, PLAYABLE_FLOORS, stripeSpriteAt } from './floors'
import { parseBrokenPreview, visualStateFor } from './objectState'
import { KITCHEN_OBJECT_X, KITCHEN_ROOM, kitchenTowerX } from '../game/kitchenLayout'

describe('playable floor modules', () => {
  it('defines the first three floors in their agreed order on one fixed-width core', () => {
    expect(PLAYABLE_FLOORS.map((floor) => [floor.number, floor.name])).toEqual([
      [1, 'Kitchen'],
      [2, 'Living room'],
      [3, 'Bedroom + en suite'],
    ])
    expect(CORE.width).toBe(440)
    expect(Number.isInteger(CORE.x)).toBe(true)
    expect(Number.isInteger(CORE.bandHeight)).toBe(true)
  })

  it('keeps every listed floor object on the floor that renders it', () => {
    for (const floor of PLAYABLE_FLOORS) {
      for (const id of floor.objects) {
        const object = OBJECTS.find((candidate) => candidate.id === id)
        expect(object?.floor).toBe(floor.id)
        if (floor.id !== 'ground') expect(object!.x % 4).toBe(0)
      }
    }
    expect(PLAYABLE_FLOORS[2].objects).toContain('toilet')
    expect(PLAYABLE_FLOORS[0].objects).not.toContain('toilet')
  })

  it('maps live kitchen interactions onto the approved room coordinate system', () => {
    expect(KITCHEN_ROOM.bodySize).toEqual([84, 74])
    expect(KITCHEN_ROOM.fittedBayOriginsX).toEqual([84, 168, 252, 336, 420, 504])
    expect(KITCHEN_OBJECT_X.cooker).toBe(kitchenTowerX(462))
    expect(KITCHEN_OBJECT_X.fridge).toBe(kitchenTowerX(546))
    expect(KITCHEN_OBJECT_X.broom).toBe(kitchenTowerX(646))
    expect(KITCHEN_OBJECT_X.petbowl).toBe(kitchenTowerX(730))
  })

  it('reserves a completely hidden changing zone between the two diving-room doors', () => {
    expect(DIVING_EXTENSION.parentFloor).toBe('bedroom')
    expect(DIVING_EXTENSION.hiddenZone.visible).toBe(false)
    expect(DIVING_EXTENSION.innerDoor.x).toBeLessThan(DIVING_EXTENSION.hiddenZone.fromX)
    expect(DIVING_EXTENSION.hiddenZone.toX).toBeLessThan(DIVING_EXTENSION.exteriorDoor.x)
    expect(DIVING_EXTENSION.sequence).toEqual([
      'inner-door-close',
      'keeper-hidden',
      'costume-swap-sfx',
      'exterior-door-open',
      'dive-suit-exit',
    ])
  })

  it('chooses shell stripes from world y rather than floor insertion order', () => {
    expect(stripeSpriteAt(0)).toBe('tower_stripe_red')
    expect(stripeSpriteAt(31)).toBe('tower_stripe_red')
    expect(stripeSpriteAt(32)).toBe('tower_stripe_white')
    expect(stripeSpriteAt(64)).toBe('tower_stripe_red')
  })
})

describe('clickable object visual states', () => {
  const ids = OBJECTS.map((object) => object.id)

  it('supports standard, active and broken states with broken taking priority', () => {
    expect(visualStateFor('tv', null, new Set())).toBe('standard')
    expect(visualStateFor('tv', 'tv', new Set())).toBe('on')
    expect(visualStateFor('tv', 'tv', new Set(['tv']))).toBe('broken')
  })

  it('parses the internal browser preview without accepting unknown objects', () => {
    expect([...parseBrokenPreview('tv,cooker,nope', ids)]).toEqual(['tv', 'cooker'])
    expect(parseBrokenPreview('all', ids).size).toBe(ids.length)
  })

  it('allows major outdoor structures to break too', () => {
    expect(BREAKABLE_OBJECTS).toEqual(expect.arrayContaining(['garden', 'jetty']))
    expect(BREAKABLE_OBJECTS).not.toContain('shop')
    expect(parseBrokenPreview('all', BREAKABLE_OBJECTS)).not.toContain('shop')
  })
})
