import { describe, expect, it } from 'vitest'
import { APPROVED_PROFILE, CANDIDATE_F5_PROFILE } from './locomotion'
import {
  DOORWAY_EXCLUSION_KU, STANDARD_LATTICE_ORIGIN, STANDARD_WIDTHS_KU, anchorsAt, parseLayout, placeAt, placementPoint, serializeLayout, spots, spotX, widenRoom,
  type Catalogue, type ObjectType, type Placement,
} from './room'
import { CATALOGUE, KITCHEN, KITCHEN_PLACEMENTS, LIVING_PLACEMENTS, LIVING_ROOM } from './rooms.data'
import { DROP_VARIANTS, packRoom, planDrop, planUpgrade, roomHoldsFullyUpgraded, shuffleAround, snapX } from './shuffle'
import { STEP_KU, lpToKu } from './units'
import { errorsOf, keeperEnvelope, validateRoom, validateType, validateWithGrowth, type LayoutInput } from './validator'

const living = (placements: Placement[] = LIVING_PLACEMENTS, extra: Partial<LayoutInput> = {}): LayoutInput => ({ room: LIVING_ROOM, placements, catalogue: CATALOGUE, ...extra })
const kitchen = (placements: Placement[] = KITCHEN_PLACEMENTS, extra: Partial<LayoutInput> = {}): LayoutInput => ({ room: KITCHEN, placements, catalogue: CATALOGUE, ...extra })
const rules = (input: LayoutInput) => errorsOf(validateRoom(input)).map((i) => i.rule)
const move = (ps: Placement[], object: string, xKu: number) => ps.map((p) => (p.object === object ? { ...p, xKu } : p))

const frontCrate: ObjectType = {
  id: 'crate', label: 'Crate', lane: 'front', source: 'test fixture',
  anchors: [{ id: 'use', offsetSteps: 0, facing: 'right', entryPose: 'standing-side-right', exitPose: 'standing-side-right' }],
  tiers: [{ tier: 1, label: 'Crate', sprite: 'x', renderAnchor: [0, 0], footprint: [-40, 40], solid: [{ from: -40, to: 40, topLp: 8 }], contacts: {} }],
}
const withCrate: Catalogue = { ...CATALOGUE, crate: frontCrate }

describe('the 172 × 56 room grid', () => {
  it('matches Codex\'s agreed dimensions', () => {
    expect(STANDARD_WIDTHS_KU).toEqual([1376, 1544, 1712])
    expect(LIVING_ROOM.heightKu).toBe(448)
    expect(DOORWAY_EXCLUSION_KU).toBe(368)
    expect(STANDARD_LATTICE_ORIGIN).toBe(32)
    // candidate x = 368 + 84n: the doorway edge is a lattice line and the usable field holds 12 intervals.
    expect(spots(LIVING_ROOM).map((n) => spotX(LIVING_ROOM, n))).toContain(368)
    expect((STANDARD_WIDTHS_KU[0] - DOORWAY_EXCLUSION_KU) / STEP_KU).toBe(12)
    // Each expansion adds exactly two intervals.
    expect(STANDARD_WIDTHS_KU[1] - STANDARD_WIDTHS_KU[0]).toBe(2 * STEP_KU)
  })

  it('expansion moves only the far wall; a valid layout stays valid with every coordinate unchanged', () => {
    for (const tier of [1, 2] as const) {
      const wide = widenRoom(LIVING_ROOM, tier)
      expect({ ...wide, widthKu: 0, widthTier: 0 }).toEqual({ ...LIVING_ROOM, widthKu: 0, widthTier: 0 })
      expect(errorsOf(validateRoom({ ...living(), room: wide, variants: 'all' }))).toEqual([])
    }
    expect(() => widenRoom(widenRoom(LIVING_ROOM, 2), 1)).toThrow()
  })

  it('stopping, his boot reaches 89 ku past the anchor, so the line 84 ku from the far wall is not a stance', () => {
    expect(keeperEnvelope(APPROVED_PROFILE, 0, 'left').extent.to).toBe(89)
    expect(keeperEnvelope(CANDIDATE_F5_PROFILE, 0, 'left').extent.to).toBe(88)
    expect(keeperEnvelope(CANDIDATE_F5_PROFILE, 0, 'right').extent.from).toBe(-88)
    const solo = (x: number) => rules(living([{ object: 'piano', room: 'living', xKu: x, anchor: 'play', tier: 1 }]))
    expect(solo(1292)).toContain(7)
    expect(solo(1208)).toEqual([])
  })
})

describe('validator (test 12)', () => {
  it('accepts the real living room with every armchair tier, and the starting kitchen', () => {
    expect(errorsOf(validateRoom(living(LIVING_PLACEMENTS, { variants: 'all' })))).toEqual([])
    expect(errorsOf(validateRoom(kitchen()))).toEqual([])
  })

  it('rejects a split step', () => {
    expect(rules(living(move(LIVING_PLACEMENTS, 'tv', 704 + 4)))).toContain(1)
  })

  it('rejects poking through the far wall', () => {
    expect(rules(living([{ object: 'tv', room: 'living', xKu: 1376, anchor: 'use', tier: 1 }]))).toContain(2)
  })

  it('rejects the doorway exclusion', () => {
    expect(rules(living([{ object: 'tv', room: 'living', xKu: 452, anchor: 'use', tier: 1 }]))).toContain(3)
  })

  it('rejects overlaps in a lane', () => {
    expect(rules(living(move(LIVING_PLACEMENTS, 'tv', 536)))).toContain(4)
  })

  it('rejects an anchor he can\'t reach past something solid', () => {
    // Armchair (solid) between the door and the piano.
    const ps: Placement[] = [{ object: 'armchair', room: 'living', xKu: 536, anchor: 'seat', tier: 1 }, { object: 'piano', room: 'living', xKu: 872, anchor: 'play', tier: 1 }]
    const issues = errorsOf(validateRoom(living(ps)))
    expect(issues.some((i) => i.rule === 5 && i.object === 'piano' && i.other === 'armchair')).toBe(true)
  })

  it('rejects a foreground item that would hide him', () => {
    const ps: Placement[] = [{ object: 'crate', room: 'living', xKu: 704, anchor: 'use', tier: 1 }, { object: 'tv', room: 'living', xKu: 788, anchor: 'use', tier: 1 }]
    const issues = errorsOf(validateRoom({ room: LIVING_ROOM, placements: ps, catalogue: withCrate }))
    expect(issues.some((i) => (i.rule === 6 || i.rule === 5) && i.other === 'crate')).toBe(true)
  })

  it('checks every variant when asked (the drag contract)', () => {
    // At 788 the professional oven would hit the pet bowl, though today's oven fits.
    const ps = move(KITCHEN_PLACEMENTS, 'cooker', 788)
    expect(rules(kitchen(ps))).toEqual([])
    const all = errorsOf(validateRoom(kitchen(ps, { variants: 'all' })))
    expect(all.some((i) => i.object === 'cooker' || i.other === 'cooker')).toBe(true)
    expect(all.every((i) => i.text.includes('(as the'))).toBe(true)
  })

  it('warns when there is no room to grow', () => {
    expect(validateWithGrowth(kitchen()).filter((i) => i.severity === 'warning')).toEqual([])
    const issues = validateWithGrowth(kitchen(move(KITCHEN_PLACEMENTS, 'cooker', 788)))
    expect(issues.filter((i) => i.severity === 'warning').map((i) => [i.rule, i.object])).toEqual([['grow', 'cooker']])
  })

  it('child-readable reasons', () => {
    const [issue] = errorsOf(validateRoom(living([{ object: 'tv', room: 'living', xKu: 452, anchor: 'use', tier: 1 }])))
    expect(issue.text).toBe('TV is too close to the door.')
  })
})

describe('tiers (test 13)', () => {
  it('tier changes never move an anchor or a contact datum', () => {
    for (const type of Object.values(CATALOGUE)) {
      expect(validateType(type)).toEqual([])
      const p = LIVING_PLACEMENTS.find((q) => q.object === type.id)
      if (!p) continue
      for (const t of type.tiers) expect(anchorsAt(type, placementPoint(type, { ...p, tier: t.tier }))).toEqual(anchorsAt(type, placementPoint(type, p)))
    }
  })

  it('a tier that moves a contact is rejected', () => {
    const bad: ObjectType = { ...CATALOGUE.armchair, tiers: [CATALOGUE.armchair.tiers[0], { ...CATALOGUE.armchair.tiers[1], contacts: { seat: 12 } }] }
    expect(validateType(bad).map((i) => i.rule)).toEqual(['catalogue'])
  })

  it('a split-step anchor offset is rejected', () => {
    const bad: ObjectType = { ...CATALOGUE.tv, anchors: [{ ...CATALOGUE.tv.anchors[0], offsetSteps: 0.5 }] }
    expect(validateType(bad).map((i) => i.rule)).toEqual([1])
  })

  it('a footprint that grows re-runs validation (upgrade guidance)', () => {
    const fits = planUpgrade(living(), 'armchair', 3)
    expect(fits.verdict).toBe('fits')
    expect(planUpgrade(kitchen(), 'cooker', 3).verdict).toBe('fits')
    const shuffled = planUpgrade(kitchen(move(KITCHEN_PLACEMENTS, 'cooker', 788)), 'cooker', 3)
    expect(shuffled.verdict).toBe('shuffle')
    expect(shuffled.moved.map((m) => m.object)).toEqual(['petbowl'])
    expect(errorsOf(validateRoom(kitchen(shuffled.placements)))).toEqual([])
    expect(shuffled.placements.find((p) => p.object === 'cooker')).toMatchObject({ xKu: 788, tier: 3 })
  })

  it('when nothing works, the shop says what to move', () => {
    const tight = { ...KITCHEN, widthKu: lpToKu(120) }
    const ps: Placement[] = [{ object: 'fridge', room: 'kitchen', xKu: 452, anchor: 'use', tier: 1 }, { object: 'cooker', room: 'kitchen', xKu: 620, anchor: 'use', tier: 1 }]
    expect(errorsOf(validateRoom({ room: tight, placements: ps, catalogue: CATALOGUE }))).toEqual([])
    const plan = planUpgrade({ room: tight, placements: ps, catalogue: CATALOGUE }, 'cooker', 3)
    expect(plan.verdict).toBe('cannot')
    expect(plan.reasons.length).toBeGreaterThan(0)
    expect(plan.whatToMove).toEqual(['fridge'])
  })
})

describe('shuffle and drop (test 14)', () => {
  const order = (ps: Placement[], room = 'kitchen') => ps.filter((p) => p.room === room).sort((a, b) => a.xKu - b.xKu).map((p) => p.object)

  it('dropping onto a neighbour slides others aside, keeping their order, never into the doorway or through a wall', () => {
    const plan = planDrop(kitchen(), 'petbowl', 1124)
    expect(plan.verdict).toBe('fits')
    const onto = planDrop(kitchen(), 'broom', 620)
    expect(onto.verdict).toBe('shuffle')
    expect(errorsOf(validateRoom(kitchen(onto.placements)))).toEqual([])
    const others = (ps: Placement[]) => order(ps).filter((o) => o !== 'broom')
    expect(others(onto.placements)).toEqual(others(KITCHEN_PLACEMENTS))
    expect(onto.placements.find((p) => p.object === 'broom')!.xKu).toBe(620)
    for (const p of onto.placements) expect(p.xKu).toBeGreaterThan(DOORWAY_EXCLUSION_KU)
  })

  it('is deterministic, minimal and never changes room', () => {
    const elsewhere: Placement = { object: 'tv', room: 'living', xKu: 704, anchor: 'use', tier: 1 }
    const input = kitchen([...KITCHEN_PLACEMENTS, elsewhere])
    const a = planDrop(input, 'broom', 620)
    const b = planDrop(input, 'broom', 620)
    expect(JSON.stringify(a)).toBe(JSON.stringify(b))
    expect(a.placements).toContainEqual(elsewhere)
    expect(a.moved.every((m) => Math.abs(m.toKu - m.fromKu) % STEP_KU === 0)).toBe(true)
  })

  it('an impossible drop stays grey, gives a reason and suggests the nearest fitting spot', () => {
    const plan = planDrop(kitchen(), 'cooker', 368)
    expect(plan.verdict).toBe('cannot')
    expect(plan.reasons[0].text).toBe('Cooker is too close to the door.')
    expect(plan.placements).toEqual(kitchen().placements.slice().sort((x, y) => x.xKu - y.xKu))
    expect(plan.nearest).toBeDefined()
  })

  it('snaps a dragged anchor to the nearest lattice line', () => {
    expect(snapX(LIVING_ROOM, 700)).toBe(704)
    expect(snapX(LIVING_ROOM, 662)).toBe(704)
    expect(snapX(LIVING_ROOM, 661)).toBe(620)
    expect(snapX(LIVING_ROOM, 5000)).toBe(1376)
  })

  it('shuffleAround keeps the fixed item and returns only valid layouts', () => {
    const fixed = placeAt(KITCHEN, 'cooker', 'use', 6, 2)
    const r = shuffleAround(kitchen(KITCHEN_PLACEMENTS.filter((p) => p.object !== 'cooker')), fixed)
    expect(r).not.toBeNull()
    expect(r!.placements).toContainEqual(fixed)
    expect(errorsOf(validateRoom(kitchen(r!.placements)))).toEqual([])
  })

  it('packRoom reproduces the recorded living room', () => {
    const r = packRoom({ room: LIVING_ROOM, catalogue: CATALOGUE, variants: 'all' }, LIVING_PLACEMENTS.map((p) => ({ object: p.object, anchor: p.anchor, tier: 1 })))
    expect(r?.placements).toEqual(LIVING_PLACEMENTS)
  })
})

describe('Frank\'s answers of 14 October (questions 1–3)', () => {
  it('a drop checks only the tier he has now; a bigger upgrade shuffles later', () => {
    expect(DROP_VARIANTS).toBe('current')
    const ps = move(KITCHEN_PLACEMENTS, 'cooker', 788)
    expect(planDrop(kitchen(ps), 'cooker', 788).verdict).toBe('fits')
    expect(planDrop(kitchen(ps, { variants: 'all' }), 'cooker', 788).verdict).not.toBe('fits')
  })

  it('every room must hold every item fully upgraded', () => {
    const items = (ps: Placement[]) => ps.map((p) => ({ object: p.object, anchor: p.anchor }))
    const living = roomHoldsFullyUpgraded({ room: LIVING_ROOM, catalogue: CATALOGUE }, items(LIVING_PLACEMENTS))
    expect(living?.placements.find((p) => p.object === 'armchair')?.tier).toBe(3)
    expect(roomHoldsFullyUpgraded({ room: KITCHEN, catalogue: CATALOGUE }, items(KITCHEN_PLACEMENTS))).not.toBeNull()
    expect(roomHoldsFullyUpgraded({ room: { ...KITCHEN, widthKu: lpToKu(100) }, catalogue: CATALOGUE }, items(KITCHEN_PLACEMENTS))).toBeNull()
  })

  it('a far-wall cupboard whose open door hides him makes the last line usable', () => {
    const anchor = { id: 'use', offsetSteps: 0, facing: 'right' as const, entryPose: 'standing-side-right', exitPose: 'standing-side-right' }
    const cupboard = (concealed: boolean): ObjectType => ({
      id: 'cupboard', label: 'Cupboard', lane: 'back', source: 'test fixture',
      anchors: [{ ...anchor, ...(concealed ? { concealedBy: { label: 'cupboard door', span: [-60, 120] as [number, number] } } : {}) }],
      tiers: [{ tier: 1, label: 'Cupboard', sprite: 'x', renderAnchor: [0, 0], footprint: [-42, 84], solid: [], contacts: {} }],
    })
    const at = (concealed: boolean) => rules({ room: LIVING_ROOM, catalogue: { ...CATALOGUE, cupboard: cupboard(concealed) }, placements: [{ object: 'cupboard', room: 'living', xKu: 1292, anchor: 'use', tier: 1 }] })
    expect(at(false)).toContain(7)
    expect(at(true)).toEqual([])
  })
})

describe('save and load (test 15)', () => {
  it('round-trips exactly, as integer ku with the width tier and anchor id', () => {
    const layout = { widthTier: 0 as const, placements: [...KITCHEN_PLACEMENTS].reverse() }
    const text = serializeLayout(layout)
    expect(serializeLayout(parseLayout(text))).toBe(text)
    expect(JSON.parse(text).placements[0]).toEqual({ object: 'fridge', room: 'kitchen', xKu: 452, anchor: 'use', tier: 1 })
    expect(() => parseLayout('{"widthTier":0,"placements":[{"object":"x","room":"y","xKu":1.5,"anchor":"use","tier":1}]}')).toThrow()
    expect(() => parseLayout('{"widthTier":3,"placements":[]}')).toThrow()
  })
})
