import { describe, expect, it } from 'vitest'
import { DEFAULT_RULES, GAME as G, UPGRADES, maxTier, upgradeTier } from './config'
import { arrive, giftUpgrade, nextDay, nextUpgrade, order, setRules, startGame, tick, tierOf, upgrade, upgradePrice, type State } from './engine'
import { revive } from './storage'
import { spriteNames } from '../ui/art'
import { parseTierPreview } from '../ui/objectState'

const fresh = (credits = 100): State => ({ ...startGame(7, { name: 'Barnaby', petName: 'Biscuit', petKind: 'cat', personality: { trait: 'cheerful', likes: [], dislikes: [] } }), credits })

describe('upgrades', () => {
  it('everything starts at tier 1', () => {
    const s = fresh()
    expect(tierOf(s, 'tv')).toBe(1)
    expect(nextUpgrade(s, 'tv')).toEqual({ tier: 2, name: UPGRADES.tv![0].name, price: UPGRADES.tv![0].cost })
    expect(nextUpgrade(s, 'door')).toBeUndefined()
  })

  it('buying one costs credits, goes up a tier, and stops at the top', () => {
    let s = upgrade(fresh(), 'tv')
    expect(tierOf(s, 'tv')).toBe(2)
    expect(s.credits).toBe(100 - UPGRADES.tv![0].cost)
    expect(s.happenings.at(-1)).toMatchObject({ kind: 'upgraded', id: 'tv', level: 2 })
    s = upgrade(s, 'tv')
    expect(tierOf(s, 'tv')).toBe(maxTier('tv'))
    const before = s.credits
    s = upgrade(s, 'tv')
    expect(tierOf(s, 'tv')).toBe(maxTier('tv'))
    expect(s.credits).toBe(before)
  })

  it('he cannot buy one he cannot afford', () => {
    const s = upgrade(fresh(1), 'bed')
    expect(tierOf(s, 'bed')).toBe(1)
    expect(s.credits).toBe(1)
    expect(s.happenings.at(-1)).toMatchObject({ kind: 'refuse', id: 'upgrade', why: 'broke' })
  })

  it('a new one replaces a broken one', () => {
    const s = upgrade({ ...fresh(), broken: ['tv'] }, 'tv')
    expect(s.broken).not.toContain('tv')
  })

  it('grown-ups set one price for all, then their own per tier', () => {
    const half = { ...DEFAULT_RULES, upgradeScale: 50 }
    expect(upgradePrice(half, 'tv', 2)).toBe(Math.round(UPGRADES.tv![0].cost / 2))
    const own = { ...half, upgradePrices: { 'tv:2': 3 } }
    expect(upgradePrice(own, 'tv', 2)).toBe(3)
    expect(upgradePrice(own, 'tv', 3)).toBe(Math.round(UPGRADES.tv![1].cost / 2))
    const s = setRules(fresh(), own)
    expect(nextUpgrade(s, 'tv')?.price).toBe(3)
  })

  it('a gift is free and says so', () => {
    const s = giftUpgrade(fresh(0), 'bed')
    expect(tierOf(s, 'bed')).toBe(2)
    expect(s.credits).toBe(0)
    expect(s.happenings.at(-1)).toMatchObject({ kind: 'upgraded', id: 'bed', gift: true, amount: 0 })
  })

  it('a better object does more good, quicker', () => {
    const start = (s: State) => arrive(order(s, [{ id: 'tv_watch' }])).doing!
    const plain = start(fresh())
    const big = start(upgrade(fresh(), 'tv'))
    expect(big.total).toBeLessThan(plain.total)
    expect(big.effects.fun!).toBeGreaterThan(plain.effects.fun!)
    // Bad side effects are not made worse.
    expect(big.effects.energy).toBe(plain.effects.energy)
  })

  it('a better bed gives a better night', () => {
    const night = (s: State) => nextDay(tick(s, 17 * 60)).needs.energy
    expect(night(fresh())).toBe(G.upgrades.bedEnergy[0])
    expect(night(giftUpgrade(fresh(), 'bed'))).toBe(G.upgrades.bedEnergy[1])
    expect(night(giftUpgrade(giftUpgrade(fresh(), 'bed'), 'bed'))).toBe(G.upgrades.bedEnergy[2])
  })

  it('old saves without tiers load at tier 1', () => {
    const old = JSON.parse(JSON.stringify(fresh())) as Partial<State>
    delete old.tiers
    const s = revive(old as State)!
    expect(s.tiers).toEqual({})
    expect(s.rules.upgradeScale).toBe(100)
  })

  it('every tier has a name and a price', () => {
    for (const [id, tiers] of Object.entries(UPGRADES)) {
      tiers!.forEach((t, i) => {
        expect(t.name.length).toBeGreaterThan(0)
        expect(t.cost).toBeGreaterThan(0)
        expect(upgradeTier(id as never, i + 2)).toBe(t)
      })
    }
  })
})

describe('tier art', () => {
  it('asks for the tier picture first, then lower tiers, then tier 1', () => {
    expect(spriteNames('tv', 'on', 3)).toEqual(['obj_tv_t3_on', 'obj_tv_t3', 'obj_tv_t2_on', 'obj_tv_t2', 'obj_tv_on', 'obj_tv'])
    expect(spriteNames('tv', 'standard')).toEqual(['obj_tv_standard', 'obj_tv'])
  })
  it('the ?tiers= preview caps at each object’s top tier', () => {
    const all = ['tv', 'piano', 'door'] as const
    expect(parseTierPreview('3', maxTier, all)).toEqual({ tv: 3, piano: 2 })
    expect(parseTierPreview('tv:2,door:3,nope:2', maxTier, all)).toEqual({ tv: 2 })
    expect(parseTierPreview(null, maxTier, all)).toEqual({})
  })
})
