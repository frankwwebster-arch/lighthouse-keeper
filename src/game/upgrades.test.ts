import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { DEFAULT_RULES, GAME as G, OBJECTS, UPGRADES, baseTierName, maxTier, midSentence, upgradeTier } from './config'
import { parseCsv, upgradeRows } from './csv'
import { UPGRADE_ROWS } from './upgrades.data'
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
    expect(nextUpgrade(s, 'shop')).toBeUndefined()
    expect(nextUpgrade(s, 'fishfood')).toBeUndefined()
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
    const all = ['tv', 'piano', 'shop'] as const
    expect(parseTierPreview('9', maxTier, all)).toEqual({ tv: 3, piano: 3 })
    expect(parseTierPreview('tv:2,shop:3,nope:2', maxTier, all)).toEqual({ tv: 2 })
    expect(parseTierPreview(null, maxTier, all)).toEqual({})
  })
})

describe('the upgrade list (data/upgrades.csv)', () => {
  const csv = readFileSync('data/upgrades.csv', 'utf8')
  it('the game has the latest copy (run `npm run upgrades` if not)', () => {
    expect(UPGRADE_ROWS).toEqual(upgradeRows(csv))
  })
  it('every row names a real tier and its sprite follows the naming rule', () => {
    const ids = new Set(OBJECTS.map((o) => o.id as string))
    for (const r of parseCsv(csv)) {
      expect(['1', '2', '3']).toContain(r.tier)
      expect(r.sprite).toBe(r.tier === '1' ? `obj_${r.object}` : `obj_${r.object}_t${r.tier}`)
      for (const state of ['normal', 'working', 'broken']) expect(['todo', 'done', 'n/a']).toContain(r[state])
      // Objects not in the game yet (the boat) are allowed: they wait for their code.
      if (!ids.has(r.object)) expect(['boat']).toContain(r.object)
    }
  })
  it('reads quoted cells with commas', () => {
    expect(parseCsv('a,b\n"x, y","say ""hi"""\n')).toEqual([{ a: 'x, y', b: 'say "hi"' }])
  })
  it('tier 1 has a name of its own, and names read well mid-sentence', () => {
    expect(baseTierName('cooker')).toBe('Basic oven')
    expect(midSentence('Big flat-screen TV')).toBe('big flat-screen TV')
    expect(midSentence('American-style fridge')).toBe('American-style fridge')
  })
})
