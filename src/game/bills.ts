/**
 * Bills: what it costs to run the lighthouse each night, paid from his credits before the
 * morning's allowance arrives. Frank's rules (15 Oct, answers b1–b4): a small bill every night,
 * shown in the day's recap; power and heating only; some upgrades cost more to run (the huge TV)
 * and some cost less (the fridge-freezer). Overdrafts are gentle: a red balance, a worried
 * keeper, and nothing to spend until he is back above zero.
 */
import { DEFAULT_RULES, type ObjectId, type Rules } from './config'
import { objectAvailable } from './missions'
import type { State } from './engine'

export type BillId = 'power' | 'heating'
export const BILLS: readonly BillId[] = ['power', 'heating']
export const BILL_LABEL: Record<BillId, string> = { power: 'Power', heating: 'Heating' }

/**
 * Credits a night for each object at tiers 1, 2 and 3 (halves allowed; each bill is rounded once at the end).
 * A negative number saves money, for things like a wind turbine once they are in the game.
 */
export const RUNNING_COSTS: Partial<Record<ObjectId, Partial<Record<BillId, readonly [number, number, number]>>>> = {
  fridge: { power: [1, 0.5, 0.5] },
  cooker: { power: [1, 1, 1.5] },
  tv: { power: [0.5, 1, 2] },
  lamp: { power: [1, 1, 0.5] },
  broom: { power: [0, 0.5, 0.5] },
  phone: { power: [0, 0.5, 0.5] },
  door: { power: [0, 0, 0.5] },
  petbowl: { power: [0, 0, 0.5] },
  radio: { power: [0, 0.5, 1] },
  barometer: { power: [0, 0, 0.5] },
  console: { power: [0.5, 1, 2] },
  gadgets: { power: [0.5, 1, 1.5] },
  tank: { power: [0.5, 1, 1.5] },
  toilet: { power: [0, 0, 0.5] },
  basin: { heating: [0.5, 1, 1.5] },
  garden: { heating: [0, 0, 1] },
}

/** The lighthouse itself, whatever is in it. */
export const STANDING_CHARGE: Record<BillId, number> = { power: 0, heating: 2 }
/** A stormy day makes the heating bill this much bigger. */
export const STORM_HEATING = 1.5
/** Spirits lost each morning he wakes up overdrawn. */
export const OVERDRAWN_WORRY = 6

export interface BillLine {
  id: BillId
  amount: number
}

export interface DayBill {
  lines: BillLine[]
  total: number
  stormy: boolean
}

const rulesOf = (s: Pick<State, 'rules'>): Rules => ({ ...DEFAULT_RULES, ...s.rules })

/** Tonight's bill for how the lighthouse is now. Zero lines when the grown-ups have switched bills off. */
export function billFor(s: Pick<State, 'rules' | 'tiers' | 'unlocked' | 'plan'>): DayBill {
  const rules = rulesOf(s)
  const stormy = !!s.plan.storm
  if (!rules.billsOn) return { lines: [], total: 0, stormy }
  const raw: Record<BillId, number> = { ...STANDING_CHARGE }
  for (const [id, costs] of Object.entries(RUNNING_COSTS) as [ObjectId, Partial<Record<BillId, readonly number[]>>][]) {
    if (!objectAvailable(s, id)) continue
    const tier = Math.min(3, Math.max(1, s.tiers?.[id] ?? 1))
    for (const bill of BILLS) raw[bill] += costs[bill]?.[tier - 1] ?? 0
  }
  if (stormy) raw.heating *= STORM_HEATING
  const lines = BILLS.map((id) => ({ id, amount: Math.max(0, Math.round((raw[id] * rules.billScale) / 100)) }))
  return { lines, total: lines.reduce((sum, l) => sum + l.amount, 0), stormy }
}

/** What one upgrade would do to tonight's bill: positive costs more, negative saves. */
export function billChange(s: Pick<State, 'rules' | 'tiers' | 'unlocked' | 'plan'>, id: ObjectId, tier: number): number {
  return billFor({ ...s, tiers: { ...s.tiers, [id]: tier } }).total - billFor(s).total
}

/**
 * Overnight money: the bill is paid from what is left in his purse first, then from the allowance
 * he earned. Savings above the carry cap are lost as before; an overdraft never goes below the
 * grown-ups' limit (anything beyond it is let off).
 */
export function payOvernight(credits: number, allowance: number, bill: number, rules: Rules): number {
  const r = { ...DEFAULT_RULES, ...rules }
  const left = credits - bill
  if (left >= 0) return Math.min(r.carryCap, left) + allowance
  return Math.max(-r.overdraftLimit, left + allowance)
}

export const overdrawn = (s: Pick<State, 'credits'>) => s.credits < 0
