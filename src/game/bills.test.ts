import { describe, expect, it } from 'vitest'
import { DEFAULT_RULES } from './config'
import { OVERDRAWN_WORRY, billChange, billFor, payOvernight } from './bills'
import { buy, giftUpgrade, nextDay, startGame, tick, upgrade, type State } from './engine'

const fresh = (seed = 7): State => {
  const s = startGame(seed, { name: 'Barnaby', petName: 'Biscuit', petKind: 'cat', personality: { trait: 'cheerful', likes: [], dislikes: [] } })
  return { ...s, plan: { ...s.plan, storm: null } }
}
const lines = (s: State) => Object.fromEntries(billFor(s).lines.map((l) => [l.id, l.amount]))
/** Sleep through the day to the report. */
const toReport = (s: State) => tick(s, 17 * 60)

describe('bills', () => {
  it('the first night costs about a quarter of a good day', () => {
    const s = fresh()
    expect(lines(s)).toEqual({ power: 4, heating: 3 })
    const good = DEFAULT_RULES.allowanceBase + DEFAULT_RULES.allowanceBonus
    expect(billFor(s).total).toBe(Math.round(good / 4))
  })

  it('floors he has not got cost nothing', () => {
    const s = fresh()
    expect(billFor({ ...s, tiers: { console: 3, tank: 3 } }).total).toBe(billFor(s).total)
    expect(billFor({ ...s, unlocked: ['lair'], tiers: {} }).total).toBeGreaterThan(billFor(s).total)
  })

  it('some upgrades cost more to run and some save', () => {
    const s = fresh()
    expect(billChange(s, 'tv', 3)).toBeGreaterThan(0)
    expect(billChange(s, 'fridge', 2)).toBeLessThan(0)
    expect(billChange(s, 'bookshelf', 3)).toBe(0)
  })

  it('a stormy day puts the heating up', () => {
    const s = fresh()
    const stormy = { ...s, plan: { ...s.plan, storm: { from: 600, to: 700 } } }
    expect(lines(stormy).heating).toBeGreaterThan(lines(s).heating)
    expect(billFor(stormy).stormy).toBe(true)
  })

  it('grown-ups can scale bills or switch them off', () => {
    const s = fresh()
    expect(billFor({ ...s, rules: { ...s.rules, billsOn: false } }).total).toBe(0)
    expect(billFor({ ...s, rules: { ...s.rules, billScale: 200 } }).total).toBe(12)
    // Saves from before bills have no bill dials: bills are on at normal size.
    const { billsOn, billScale, overdraftLimit, ...old } = s.rules
    expect(billFor({ ...s, rules: old as State['rules'] }).total).toBe(7)
  })

  it('overnight: bills come out of the purse first, then the allowance', () => {
    const r = DEFAULT_RULES
    expect(payOvernight(30, 10, 7, r)).toBe(23 + 10)
    expect(payOvernight(60, 10, 7, r)).toBe(r.carryCap + 10)
    expect(payOvernight(3, 10, 7, r)).toBe(6)
    expect(payOvernight(0, 8, 12, r)).toBe(-4)
    expect(payOvernight(-18, 8, 15, r)).toBe(-r.overdraftLimit)
    expect(payOvernight(-10, 28, 7, r)).toBe(11)
  })

  it('the day report carries the bill and the morning pays it', () => {
    let s = toReport(fresh())
    const r = s.history[0]
    expect(r.bills?.total).toBe(7)
    const before = s.credits
    s = nextDay(s)
    expect(s.credits).toBe(Math.min(s.rules.carryCap, before - 7) + r.allowance)
    expect(s.happenings.some((h) => h.kind === 'bills' && h.amount === 7)).toBe(true)
  })

  it('a poor day after spending everything leaves him overdrawn and worried', () => {
    let s = fresh()
    s = { ...s, credits: 0, tiers: { tv: 3, cooker: 3, basin: 3 } }
    s = toReport(s)
    const r = { ...s.history[0], allowance: DEFAULT_RULES.allowanceBase }
    s = { ...s, history: [r] }
    expect(r.bills!.total).toBeGreaterThan(r.allowance)
    const calm = nextDay({ ...s, credits: 50 })
    s = nextDay(s)
    expect(s.credits).toBeLessThan(0)
    expect(s.spirits).toBe(calm.spirits - OVERDRAWN_WORRY)
    expect(s.happenings.some((h) => h.kind === 'overdrawn')).toBe(true)
  })

  it('overdrawn: no upgrades or shopping, but presents from the grown-ups still arrive', () => {
    const s = { ...fresh(), credits: -5 }
    const tried = upgrade(s, 'tv')
    expect(tried.tiers.tv).toBeUndefined()
    expect(tried.happenings.at(-1)).toMatchObject({ kind: 'refuse', why: 'overdrawn' })
    const shopping = { ...s, doing: { id: 'shop_buy', phase: 'doing' } as State['doing'] }
    expect(buy(shopping, 'cheese').happenings.at(-1)).toMatchObject({ kind: 'refuse', why: 'overdrawn' })
    expect(giftUpgrade(s, 'tv').tiers.tv).toBe(2)
  })

  it('a week of ordinary days never runs away', () => {
    // Worst case: every day earns only the guaranteed allowance and he spends nothing.
    const poor = (s: State): State => ({ ...s, rules: { ...s.rules, allowanceBonus: 0 } })
    let s = poor(fresh())
    for (let d = 0; d < 7; d++) s = nextDay(toReport(s))
    expect(s.credits).toBeGreaterThanOrEqual(0)
    // With power-hungry upgrades the same week sinks, but never past the overdraft limit.
    let t: State = { ...poor(fresh()), tiers: { tv: 3, cooker: 3, basin: 3, lamp: 2, broom: 3, phone: 3, door: 3, toilet: 3, garden: 3 } }
    for (let d = 0; d < 14; d++) t = nextDay(toReport(t))
    expect(t.credits).toBe(-DEFAULT_RULES.overdraftLimit)
  })
})
