/**
 * THE RULES. Pure functions that take the game and give back the next game:
 * no screen, no clock of their own, and luck from a seed, so the same seed and
 * the same orders always play the same days.
 *
 * The screen calls `tick` as time passes, `order` when he is told something,
 * and `arrive` when he has walked to where the job is. Everything that happens
 * is added to `happenings`, which the screen turns into his diary, his remarks
 * and the pictures.
 *
 * Evolved from the Keeper mini game in Stranded Studio: the needs, mood,
 * "left alone he looks after himself", callers, ship and day marks all carry
 * over. New here: credits and a shop, a loo, a phone he can refuse to use,
 * bedtime, a pet with its own needs and mischief, and multi-day progress.
 *
 * No number lives here: they are all in `config.ts`.
 */

import { REACTIONS, reactionById, type DoOrder } from './commands'
import {
  GAME as G,
  BREAKABLE_OBJECTS,
  BREAKDOWN_SFX,
  INTERACTIONS,
  NEEDS,
  TASTE_POOL,
  TRAITS,
  VISITORS,
  foodById,
  maxTier,
  upgradeKey,
  upgradeTier,
  DEFAULT_RULES,
  type FoodDef,
  type Rules,
  interactionById,
  type AnimKey,
  type FxKey,
  type InteractionDef,
  type NeedId,
  type ObjectId,
  START_MIDDLE,
  type PetKind,
  type RoomFloor,
  type TraitId,
  type UnlockId,
} from './config'
import type { Quiz } from './quiz'
import { countEvents, eventsOf, floorCount, freshMissions, goalTarget, insertFloor, isMiddleFloor, objectAvailable, openMissions, rewardOf, type MissionState } from './missions'
import type { ChatQ } from './chat'

// ─── What a game is ──────────────────────────────────────────────────────────

export interface Personality {
  trait: TraitId
  likes: string[]
  dislikes: string[]
}

export interface Setup {
  name: string
  petName: string
  petKind: PetKind
  personality: Personality
}

/** One job. `id` is an interaction, or 'react' for a silly reaction. */
export type Order = DoOrder

export interface Doing {
  id: string
  react?: string
  object: ObjectId
  anim: AnimKey
  fx?: FxKey
  /** A shut door: the room is out of sight (the loo). */
  priv: boolean
  by: 'player' | 'self'
  sulky: boolean
  phase: 'going' | 'doing'
  /** What it does to his needs by the time it is finished. */
  effects: Partial<Record<NeedId, number>>
  left: number
  total: number
  going: number
  /** The food, if it is one. */
  item?: string
  /** Different for every job, so the screen can tell a new one from the old. */
  n: number
}

export interface Visit {
  who: string
  /** `due`: not here yet. `waiting`: at the door. `inside`: in the house. `gone`. */
  state: 'due' | 'waiting' | 'inside' | 'gone'
  /** When they arrive (or arrived). */
  at: number
  /** When they leave. */
  until: number
  source: 'caller' | 'friend'
  met: boolean
}

export interface DayPlan {
  ship: { at: number; state: 'due' | 'safe' | 'close' }
  storm: { from: number; to: number } | null
  /** When the phone rings with a call for him. */
  rings: number[]
}

export type HKind =
  | 'dawn' | 'chose' | 'done' | 'refuse' | 'moan' | 'caller' | 'caller_met' | 'caller_gone' | 'visitor_left'
  | 'horn' | 'ship' | 'storm' | 'thunder' | 'dusk' | 'lamp_lit' | 'lamp_out' | 'spotted' | 'bed' | 'annoyed'
  | 'ring' | 'friend_coming' | 'pizza_ordered' | 'pizza_arrived' | 'pet' | 'bought' | 'locked' | 'react' | 'quiz' | 'chat'
  | 'credits' | 'breakdown' | 'repaired' | 'upgraded' | 'mission_done' | 'unlocked'

export type RefuseWhy = 'missing' | 'storm' | 'nobody' | 'early' | 'quiz' | 'bursting' | 'grumpy' | 'phone_busy' | 'phone_mood' | 'phone_none' | 'empty' | 'broke' | 'broken' | 'notready' | 'pizza_pending' | 'stuck'

export interface Happening {
  n: number
  at: number
  kind: HKind
  id?: string
  react?: string
  who?: string
  need?: NeedId
  why?: RefuseWhy
  by?: 'player' | 'self'
  sulky?: boolean
  liked?: boolean
  disliked?: boolean
  item?: string
  safe?: boolean
  on?: boolean
  level?: number
  what?: 'caller' | 'ship' | 'storm' | 'nothing'
  inMinutes?: number
  petDid?: 'steal' | 'gift' | 'knock' | 'purr'
  correct?: boolean
  amount?: number
  text?: string
  /** A present from the grown-ups (an upgrade they gave). */
  gift?: boolean
}
type Loose = Omit<Happening, 'n' | 'at'>

export interface DayResult {
  day: number
  score: number
  rating: (typeof G.ratings)[number]['id']
  parts: { id: 'mood' | 'ship' | 'friends' | 'pet' | 'house' | 'brain' | 'bedtime'; got: number; of: number }[]
  mood: number
  /** Each need's average over the day, and whether it ended up green. */
  needs: { id: NeedId; avg: number; green: boolean }[]
  greens: number
  shipSafe: boolean
  /** What the next morning's allowance will be. */
  allowance: number
}

/** A question waiting for an answer. */
export type Prompt =
  | { kind: 'quiz'; quiz: Quiz; tries: number; revealed: boolean }
  | { kind: 'chat'; chat: ChatQ }

export interface State {
  v: 1
  seed: number
  rng: number
  name: string
  petName: string
  petKind: PetKind
  personality: Personality
  day: number
  /** Minutes after midnight. */
  clock: number
  needs: Record<NeedId, number>
  spirits: number
  doing: Doing | null
  queue: Order[]
  queueSulky: boolean
  idle: number
  moaned: NeedId[]
  lampLit: boolean
  lampLeft: number
  shine: number
  /** Objects waiting for repair. */
  broken: ObjectId[]
  /** Upgraded objects and the tier they are at (missing = tier 1). */
  tiers: Partial<Record<ObjectId, number>>
  /** Floors (and the lift) that missions have unlocked. */
  unlocked: UnlockId[]
  /** The middle of the tower, bottom to top (between the kitchen and the bedroom). New floors take a random place here and keep it. */
  middle: RoomFloor[]
  /** Floors earned but not built yet: one arrives each morning, in this order. */
  arriving: UnlockId[]
  missions: MissionState
  plan: DayPlan
  visits: Visit[]
  thunderAt: number
  /** The pet, who has needs and a mind of its own. */
  pet: { hunger: number; fun: number; fright: number }
  petClock: number
  /** Money. */
  credits: number
  /** The grown-up's dials. */
  rules: Rules
  /** What is in the fridge and larder (food id → count). */
  items: Record<string, number>
  garden: { ready: number; watered: boolean }
  /** The phone: when he will next be willing to ring someone, and a ring he has not yet answered. */
  phoneReadyAt: number
  ringing: { until: number } | null
  /** A pizza on its way: when it arrives. */
  pizzaAt: number | null
  /** How annoyed he is about not being in bed (0–3). */
  annoyedLevel: number
  /** A question waiting for Ralph. */
  prompt: Prompt | null
  happenings: Happening[]
  nextN: number
  tally: { needSums: Record<NeedId, number>; moodSum: number; minutes: number; emptied: boolean; bedAt: number | null; forced: boolean; asked: number; quizAsked: number; quizPoints: number; petFed: boolean }
  history: DayResult[]
  phase: 'day' | 'report'
}

// ─── Luck ────────────────────────────────────────────────────────────────────

function roll(rng: number): [number, number] {
  const next = (rng + 0x6d2b79f5) | 0
  let t = next
  t = Math.imul(t ^ (t >>> 15), t | 1)
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
  return [((t ^ (t >>> 14)) >>> 0) / 4294967296, next]
}

function dice(rng: number) {
  let at = rng
  const next = () => {
    const [v, n] = roll(at)
    at = n
    return v
  }
  return {
    next,
    between: (lo: number, hi: number) => Math.round(lo + next() * (hi - lo)),
    pick: <T>(list: readonly T[]): T => list[Math.min(list.length - 1, Math.floor(next() * list.length))],
    get rng() {
      return at
    },
  }
}

const clamp = (v: number, lo = 0, hi = 100) => Math.min(hi, Math.max(lo, v))

// ─── Starting ────────────────────────────────────────────────────────────────

export function rollPersonality(seed: number): Personality {
  const d = dice(seed | 0)
  const trait = d.pick(TRAITS)
  const pool = [...TASTE_POOL] as string[]
  const take = () => pool.splice(Math.min(pool.length - 1, Math.floor(d.next() * pool.length)), 1)[0]
  return { trait, likes: [take(), take()], dislikes: [take()] }
}

/** What a day brings: surprise callers, the ship, a storm, phone calls. */
export function planDay(rng: number): { plan: DayPlan; visits: Visit[]; rng: number } {
  const d = dice(rng)
  const V = G.visitor
  const count = d.between(V.min, V.max)
  const pool = VISITORS.filter((v) => !v.friend).map((v) => v.id)
  const visits: Visit[] = []
  for (let i = 0; i < count; i++) {
    const who = pool.splice(Math.min(pool.length - 1, Math.floor(d.next() * pool.length)), 1)[0]
    const at = d.between(V.earliest + i * 180, V.latest)
    visits.push({ who, state: 'due', at, until: at + V.waits, source: 'caller', met: false })
  }
  const ship = { at: d.between(G.ship.earliest, G.ship.latest), state: 'due' as const }
  const stormy = d.next() < G.storm.chance
  const from = d.between(G.storm.earliest, G.storm.latest)
  const rings: number[] = []
  const nRings = d.between(G.phone.ringsMin, G.phone.ringsMax)
  for (let i = 0; i < nRings; i++) rings.push(d.between(10 * 60 + i * 180, 17 * 60))
  rings.sort((a, b) => a - b)
  return { plan: { ship, storm: stormy ? { from, to: from + G.storm.lasts } : null, rings }, visits, rng: d.rng }
}

export function startGame(seed: number, setup: Setup, rules: Rules = DEFAULT_RULES): State {
  const { plan, visits, rng } = planDay(seed | 0)
  const s: State = {
    v: 1,
    seed: seed | 0,
    rng,
    name: setup.name,
    petName: setup.petName,
    petKind: setup.petKind,
    personality: setup.personality,
    day: 1,
    clock: G.day.start,
    needs: { ...G.startNeeds },
    spirits: 0,
    doing: null,
    queue: [],
    queueSulky: false,
    idle: 0,
    moaned: [],
    lampLit: false,
    lampLeft: 0,
    shine: G.lamp.startShine,
    broken: [],
    tiers: {},
    unlocked: [],
    middle: [...START_MIDDLE],
    arriving: [],
    missions: freshMissions(),
    plan,
    visits,
    thunderAt: plan.storm ? plan.storm.from + 5 : Infinity,
    pet: { hunger: G.pet.startHunger, fun: G.pet.startFun, fright: 0 },
    petClock: 0,
    credits: rules.firstDay,
    rules,
    items: { toast: 99, ...G.credits.startItems },
    garden: { ready: 0, watered: false },
    phoneReadyAt: 0,
    ringing: null,
    pizzaAt: null,
    annoyedLevel: 0,
    prompt: null,
    happenings: [],
    nextN: 1,
    tally: freshTally(),
    history: [],
    phase: 'day',
  }
  return note(s, { kind: 'dawn' })
}

function freshTally(): State['tally'] {
  return { needSums: Object.fromEntries(NEEDS.map((n) => [n, 0])) as Record<NeedId, number>, moodSum: 0, minutes: 0, emptied: false, bedAt: null, forced: false, asked: 0, quizAsked: 0, quizPoints: 0, petFed: false }
}

// ─── Reading the game ────────────────────────────────────────────────────────

/** How cross he is about still being up: 0 before bedtime, rising to 100 when he is about to put himself to bed. */
export const annoyanceOf = (clock: number) => (clock < G.day.bedtime ? 0 : clamp(((clock - G.day.bedtime) / (G.day.forced - G.day.bedtime)) * 100))

/** His mood, 0 to 100: mostly the average of his needs, dragged by the worst, moved by his spirits, spoiled by being up too late. */
export function moodOf(s: Pick<State, 'needs' | 'spirits' | 'clock' | 'doing'>): number {
  const values = NEEDS.map((n) => s.needs[n])
  const mean = values.reduce((a, b) => a + b, 0) / values.length
  const late = s.doing?.id === 'bed_sleep' ? 0 : annoyanceOf(s.clock) * 0.25
  return clamp(mean * G.mood.averageShare + Math.min(...values) * G.mood.worstShare + s.spirits - late)
}

export type MoodWord = 'chipper' | 'content' | 'soso' | 'grumpy' | 'miserable'
export function moodWord(mood: number): MoodWord {
  const W = G.mood.moodWords
  return mood >= W.chipper ? 'chipper' : mood >= W.content ? 'content' : mood >= W.soso ? 'soso' : mood >= W.grumpy ? 'grumpy' : 'miserable'
}

export const stormNow = (s: State) => s.plan.storm !== null && s.clock >= s.plan.storm.from && s.clock < s.plan.storm.to
export const darkness = (clock: number) => clamp(((clock - G.day.dusk) / (G.day.dark - G.day.dusk)) * 1, 0, 1)
export const waitingVisit = (s: State): Visit | undefined => s.visits.find((v) => v.state === 'waiting')
export const insideVisit = (s: State): Visit | undefined => s.visits.find((v) => v.state === 'inside')
export const lampWillLast = (s: State) => s.lampLit && s.clock + s.lampLeft >= s.plan.ship.at
export const shopOpen = (s: State) => s.doing?.id === 'shop_buy' && s.doing.phase === 'doing'
export const quizBlocking = (s: State) => s.prompt?.kind === 'quiz'
export const isNight = (s: State) => s.phase === 'report'

/** What's he able to eat right now: the larder's food, by kind. */
export const owned = (s: State, kind: 'snack' | 'cook' | 'takeaway' | 'staple'): string[] => Object.keys(s.items).filter((id) => (s.items[id] ?? 0) > 0 && foodById(id)?.kind === kind)

/** Sending him to bed now would lose something. */
export function bedWarning(s: State): 'lamp' | 'caller' | null {
  if (s.clock < G.day.bedFrom) return null
  if (s.plan.ship.state === 'due' && !lampWillLast(s)) return 'lamp'
  if (waitingVisit(s)) return 'caller'
  return null
}

/** The effects of one go at an action, as he is now: more of what he likes, less in a sulk. */
export function effectsOf(s: Pick<State, 'personality'>, def: { id: string; effects: Partial<Record<NeedId, number>> }, sulky = false): Partial<Record<NeedId, number>> {
  const liked = s.personality.likes.includes(def.id)
  const out: Partial<Record<NeedId, number>> = {}
  for (const need of NEEDS) {
    const base = def.effects[need]
    if (!base) continue
    out[need] = base > 0 ? Math.round(base * (liked ? 1 + G.mood.likedBonus : 1) * (sulky ? G.mood.sulkyShare : 1)) : base
  }
  return out
}

/** What allowance tomorrow's score earns. */
/** Tomorrow's allowance: the base, plus a share of the bonus for each need that finished the day green. */
export const allowanceFor = (rules: Rules, greens: number) => Math.round(rules.allowanceBase + (rules.allowanceBonus * greens) / NEEDS.length)

/** What a food costs today (the grown-up's own price, or the normal one scaled). */
export const priceOf = (s: Pick<State, 'rules'>, food: Pick<FoodDef, 'id' | 'cost'>): number => {
  if (food.cost <= 0) return 0
  const own = s.rules.prices[food.id]
  return own !== undefined ? Math.max(0, Math.round(own)) : Math.max(1, Math.round((food.cost * s.rules.priceScale) / 100))
}

/** A surprise from a grown-up. */
export function gift(s: State, credits: number): State {
  const n = Math.max(0, Math.round(credits))
  return n ? note({ ...s, credits: s.credits + n }, { kind: 'credits', amount: n }) : s
}

/** Changed dials take effect at once (a mission target lowered below what he has done finishes it). */
export const setRules = (s: State, rules: Rules): State => missionEvents({ ...s, rules }, [])

// ─── Upgrades ────────────────────────────────────────────────────────────────

/** The tier an object is at (1 until it is upgraded). */
export const tierOf = (s: Pick<State, 'tiers'>, id: ObjectId) => s.tiers?.[id] ?? 1

/** What one upgrade costs today: the grown-up's own price, or the normal one scaled. */
export function upgradePrice(rules: Pick<Rules, 'upgradeScale' | 'upgradePrices'>, id: ObjectId, tier: number): number {
  const def = upgradeTier(id, tier)
  if (!def) return 0
  const own = rules.upgradePrices?.[upgradeKey(id, tier)]
  return own !== undefined ? Math.max(0, Math.round(own)) : Math.max(1, Math.round((def.cost * (rules.upgradeScale ?? 100)) / 100))
}

/** The next upgrade for an object, if there is one. */
export function nextUpgrade(s: Pick<State, 'tiers' | 'rules'>, id: ObjectId): { tier: number; name: string; price: number } | undefined {
  const tier = tierOf(s, id) + 1
  const def = upgradeTier(id, tier)
  return def && tier <= maxTier(id) ? { tier, name: def.name, price: upgradePrice(s.rules, id, tier) } : undefined
}

/** Fit the next tier: the new one replaces the old, so a broken one is broken no more. */
function fitUpgrade(s: State, id: ObjectId, price: number, isGift: boolean): State {
  const up = nextUpgrade(s, id)!
  const next = { ...s, credits: s.credits - price, tiers: { ...s.tiers, [id]: up.tier }, broken: s.broken.filter((b) => b !== id) }
  return note(next, { kind: 'upgraded', id, level: up.tier, amount: price, gift: isGift || undefined })
}

/** He buys the next tier for an object (or says he cannot afford it). */
export function upgrade(s: State, id: ObjectId): State {
  const up = nextUpgrade(s, id)
  if (!up || !objectAvailable(s, id)) return s
  if (s.credits < up.price) return note(s, { kind: 'refuse', id: 'upgrade', why: 'broke', item: id })
  return fitUpgrade(s, id, up.price, false)
}

/** For the grown-ups: give him the next tier for free. */
export function giftUpgrade(s: State, id: ObjectId): State {
  return nextUpgrade(s, id) && objectAvailable(s, id) ? fitUpgrade(s, id, 0, true) : s
}

/** A job on a better object does more good, and quicker. */
function withTier(s: State, object: ObjectId, minutes: number, effects: Partial<Record<NeedId, number>>) {
  const i = Math.min(tierOf(s, object), G.upgrades.boost.length) - 1
  if (i <= 0) return { minutes, effects }
  const boosted: Partial<Record<NeedId, number>> = {}
  for (const need of NEEDS) {
    const v = effects[need]
    if (v !== undefined) boosted[need] = v > 0 ? Math.round(v * (1 + G.upgrades.boost[i] / 100)) : v
  }
  return { minutes: Math.max(1, Math.round(minutes * (1 - G.upgrades.quicker[i] / 100))), effects: boosted }
}

// ─── Changing the game ───────────────────────────────────────────────────────

function note(s: State, h: Loose): State {
  const entry = { ...h, n: s.nextN, at: s.clock } as Happening
  const next = { ...s, happenings: [...s.happenings, entry].slice(-G.diaryLimit), nextN: s.nextN + 1 }
  return missionEvents(next, eventsOf(entry))
}

/**
 * Count what happened towards the missions. A finished one pays its reward;
 * the lift goes in at once, and a floor is built overnight (it arrives the
 * next morning, one floor a morning).
 */
function missionEvents(s: State, events: Parameters<typeof countEvents>[1]): State {
  const { missions, finished } = countEvents(s.missions, events, s.rules, floorCount(s))
  if (!finished.length) return missions === s.missions ? s : { ...s, missions }
  let next: State = { ...s, missions }
  for (const m of finished) {
    const reward = rewardOf(m, next.rules)
    const now = m.unlocks === 'lift'
    next = note({ ...next, credits: next.credits + reward }, { kind: 'mission_done', id: m.id, amount: reward, on: !now })
    if (now) next = note({ ...next, unlocked: [...new Set([...next.unlocked, m.unlocks])] }, { kind: 'unlocked', id: m.unlocks })
    else if (!next.arriving.includes(m.unlocks) && !next.unlocked.includes(m.unlocks)) next = { ...next, arriving: [...next.arriving, m.unlocks] }
  }
  return next
}

/** For the grown-ups: finish an open mission now (its floor still arrives in the morning). */
export function completeMission(s: State, id: string): State {
  const m = openMissions(s.missions, floorCount(s)).find((x) => x.id === id)
  if (!m) return s
  const events = m.goals.flatMap((g, i) => Array.from({ length: goalTarget(m, i, s.rules) }, () => g.event))
  return missionEvents(s, events)
}

/** Overnight, the lighthouse builds the next floor he has earned: a middle floor takes a random place and keeps it for good. */
function buildOvernight(s: State): State {
  const [floor, ...rest] = s.arriving
  if (!floor) return s
  const d = dice(s.rng)
  const middle = isMiddleFloor(floor) ? insertFloor(s.middle, floor, d.next() * (s.middle.length + 1)) : s.middle
  return note({ ...s, rng: d.rng, arriving: rest, middle, unlocked: [...new Set([...s.unlocked, floor])] }, { kind: 'unlocked', id: floor })
}

const lift = (s: State, by: number): State => ({ ...s, spirits: clamp(s.spirits + by, -G.mood.spiritsLimit, G.mood.spiritsLimit) })

/** What an order is, as a definition: an interaction, or a silly reaction made to look like one. */
export function defOf(o: Order): InteractionDef | undefined {
  if (o.id === 'repair' && o.object) {
    return { id: 'repair', object: o.object, label: 'Repair it', did: `repaired the ${o.object}`, minutes: G.breakdown.repairMinutes, effects: { fun: 4, tidiness: -2 }, anim: 'busy', fx: 'sparkles', self: false, gated: false, keywords: ['repair', 'fix', 'mend'], example: 'repair it' }
  }
  if (o.id === 'react') {
    const r = o.react ? reactionById(o.react) : undefined
    if (!r) return undefined
    return { id: 'react', object: 'here', label: r.id, did: 'did something silly', minutes: r.minutes, effects: r.effects ?? {}, anim: r.anim, fx: r.fx, self: false, gated: false, keywords: [], example: '' }
  }
  return interactionById(o.id)
}

/** What he is able to do with what is in the house: the food this job would use. */
function foodFor(s: State, id: string, wanted?: string): string | null {
  const kinds = id === 'fridge_snack' ? (['snack', 'takeaway', 'staple'] as const) : id === 'cooker_cook' ? (['cook'] as const) : ([] as const)
  if (!kinds.length) return null
  if (wanted && (s.items[wanted] ?? 0) > 0 && kinds.some((k) => foodById(wanted)?.kind === k)) return wanted
  // He picks the thing he has most of that does most for him, other than toast: that is only if nothing else is left.
  const have = kinds.flatMap((k) => owned(s, k)).filter((f) => foodById(f)?.kind !== 'staple')
  if (!have.length) return null
  return have.sort((a, b) => (foodById(b)?.hunger ?? 0) - (foodById(a)?.hunger ?? 0))[0]
}

/** Start on a job (or say why not). */
function begin(s: State, o: Order, by: 'player' | 'self', sulky: boolean): State {
  let id = o.id
  let item = o.item
  const def0 = defOf(o)
  if (!def0) return startNext(s)
  const refuse = (why: RefuseWhy, then?: Order): State => {
    const next = note(s, { kind: 'refuse', id, why, react: o.react })
    return then ? begin(next, then, 'self', false) : startNext(next)
  }
  const bursting = s.needs.bladder < G.bursting
  if (!objectAvailable(s, def0.object)) return refuse('missing')
  if (id === 'repair' && !s.broken.includes(def0.object)) return refuse('notready')
  // A broken bed must never trap the simulation at forced bedtime: he can still
  // sleep in it (badly), while naps and every other broken-object action wait
  // for a repair.
  const canUseBrokenBed = id === 'bed_sleep' && s.clock >= G.day.bedFrom
  if (id !== 'repair' && s.broken.includes(def0.object) && !canUseBrokenBed) return refuse('broken')
  if (by === 'player') {
    // He has got to go, and will not do anything else.
    if (id !== 'repair' && bursting && !def0.private && s.doing?.priv !== true) return refuse('bursting', { id: 'loo_wee' })
    if (def0.gated && quizBlocking(s)) return refuse('quiz')
    if (def0.gated && moodOf(s) < G.refuseMoodBelow) {
      const d = dice(s.rng)
      const grump = d.next() < 0.5
      s = { ...s, rng: d.rng }
      if (grump) return refuse('grumpy')
    }
  }
  if (id === 'jetty_fish' && stormNow(s)) return refuse('storm')
  if ((id === 'door_greet') && !waitingVisit(s)) return refuse('nobody')
  if (['with_chat', 'with_cards', 'with_tv'].includes(id) && !insideVisit(s)) return refuse('nobody')
  if (id === 'phone_answer' && !s.ringing) return refuse('nobody')
  let next = s
  if (id === 'bed_sleep' && s.clock < G.day.bedFrom) {
    // Too early for bed: he has a nap instead, and says so.
    next = note(s, { kind: 'refuse', id, why: 'early' })
    id = 'bed_nap'
  }
  if (id === 'phone_call') {
    if (s.clock < s.phoneReadyAt) return refuse('phone_busy')
    if (moodOf(s) < G.phone.moodMin) return refuse('phone_mood')
    if (!VISITORS.some((v) => v.friend && !s.visits.some((x) => x.who === v.id && x.state !== 'gone'))) return refuse('phone_none')
  }
  if (id === 'phone_pizza') {
    if (s.pizzaAt !== null) return refuse('pizza_pending')
    if (s.credits < priceOf(s, foodById('pizza')!)) return refuse('broke')
  }
  if (id === 'garden_pick' && s.garden.ready <= 0) return refuse('notready')
  if (id === 'fridge_snack' || id === 'cooker_cook') {
    // Toast is always in the larder; the cooker takes only cooking food.
    const found = foodFor(next, id, item)
    if (!found) {
      if (id === 'cooker_cook') return refuse('empty', { id: 'cooker_toast' })
      return refuse('empty')
    }
    item = found
  }
  const def = id === o.id ? def0 : (interactionById(id) ?? def0)
  let minutes = def.minutes
  let effects: Partial<Record<NeedId, number>> = { ...def.effects }
  if (item) {
    const food = foodById(item)!
    minutes = food.minutes
    effects.hunger = (effects.hunger ?? 0) + food.hunger
    if (food.fun) effects.fun = (effects.fun ?? 0) + food.fun
  }
  if (def.id !== 'repair' && def.object !== 'here') ({ minutes, effects } = withTier(next, def.object, minutes, effects))
  const withTaste = effectsOf(next, { id: def.id, effects }, sulky)
  const here = def.object === 'here' || o.id === 'react'
  const doing: Doing = {
    id: def.id,
    react: o.react,
    object: def.object,
    anim: def.anim,
    fx: def.fx,
    priv: def.private === true,
    by,
    sulky,
    phase: here ? 'doing' : 'going',
    effects: withTaste,
    left: minutes,
    total: minutes,
    going: 0,
    item,
    n: next.nextN,
  }
  return { ...next, doing, idle: 0, nextN: next.nextN + 1 }
}

function startNext(s: State): State {
  if (!s.queue.length) return { ...s, doing: null }
  const [first, ...rest] = s.queue
  return begin({ ...s, queue: rest, doing: null }, first, 'player', s.queueSulky)
}

/**
 * He is told what to do. `moodDelta` is how he took being asked: -2 (rude) to
 * 2 (very nicely). What he was doing is dropped, and the new jobs are done in
 * order. A night's sleep, and the loo, once he is in, are not interrupted.
 */
export function order(s: State, orders: readonly Order[], moodDelta = 0): State {
  if (s.phase !== 'day') return s
  const delta = Math.max(-2, Math.min(2, Math.round(moodDelta)))
  let next = lift(s, delta * 4)
  next = { ...next, tally: { ...next.tally, asked: next.tally.asked + 1 } }
  const wanted = orders.filter((o) => defOf(o)).slice(0, G.queueLimit)
  if (!wanted.length) return next
  if (next.doing?.id === 'bed_sleep' && next.doing.phase === 'doing') return next
  if (next.doing?.priv && next.doing.phase === 'doing') return note(next, { kind: 'locked' })
  const [first, ...rest] = wanted
  return begin({ ...next, queue: rest, queueSulky: delta < 0, doing: null }, first, 'player', delta < 0)
}

/** Stop what he is doing (leaving the shop, say) and go on to whatever is next. */
export function stopDoing(s: State): State {
  if (!s.doing || s.doing.priv) return s
  return startNext({ ...s, doing: null })
}

/** He has walked to where the job is. */
export function arrive(s: State): State {
  const d = s.doing
  if (!d || d.phase !== 'going') return s
  let next: State = { ...s, doing: { ...d, phase: 'doing' } }
  if (d.id === 'bed_sleep') next = { ...next, tally: { ...next.tally, bedAt: next.clock } }
  return d.total <= 0 ? finish(next) : next
}

/** A job is done: what it leaves behind. */
function finish(s: State): State {
  const d = s.doing!
  const liked = s.personality.likes.includes(d.id)
  const disliked = s.personality.dislikes.includes(d.id)
  let next: State = { ...s, doing: null }
  if (liked) next = lift(next, G.mood.taste)
  if (disliked && d.by === 'player') next = lift(next, d.sulky ? -G.mood.taste : -G.mood.taste / 2)
  if (d.id === 'react') {
    const r = d.react ? reactionById(d.react) : undefined
    if (r?.spirits) next = lift(next, r.spirits)
    next = note(next, { kind: 'react', react: d.react, id: 'react' })
    if (d.react === 'fart' || d.react === 'stinky') next = { ...next, pet: { ...next.pet, fright: 1 } }
    return startNext(next)
  }
  if (d.id === 'repair') {
    next = note({ ...next, broken: next.broken.filter((id) => id !== d.object) }, { kind: 'repaired', id: d.object })
    return startNext(next)
  }
  next = note(next, { kind: 'done', id: d.id, by: d.by, sulky: d.sulky, liked, disliked, item: d.item })

  if (d.item) {
    const left = Math.max(0, (next.items[d.item] ?? 0) - 1)
    next = { ...next, items: { ...next.items, [d.item]: left } }
    // Toast is never used up.
    if (foodById(d.item)?.kind === 'staple') next = { ...next, items: { ...next.items, [d.item]: 99 } }
  }
  switch (d.id) {
    case 'lamp_light':
      next = note({ ...next, lampLit: true, lampLeft: G.lamp.burnMinutes }, { kind: 'lamp_lit' })
      break
    case 'lamp_polish':
      next = { ...next, shine: clamp(next.shine + G.lamp.polish) }
      break
    case 'scope_look':
    case 'weather_check':
      next = note(next, spotted(next))
      break
    case 'pet_feed':
      next = { ...next, pet: { ...next.pet, hunger: clamp(next.pet.hunger + G.pet.feedGain) }, tally: { ...next.tally, petFed: true } }
      break
    case 'pet_play':
      next = { ...next, pet: { ...next.pet, fun: clamp(next.pet.fun + G.pet.playGain) } }
      break
    case 'garden_tend':
      next = { ...next, garden: { ready: Math.min(3, next.garden.ready + 1), watered: true } }
      break
    case 'garden_pick':
      next = { ...next, garden: { ...next.garden, ready: Math.max(0, next.garden.ready - 1) } }
      break
    case 'door_greet': {
      const v = waitingVisit(next)
      if (v) {
        const def = VISITORS.find((x) => x.id === v.who)!
        const needs = { ...next.needs }
        for (const need of NEEDS) needs[need] = clamp(needs[need] + ((def.gift as Partial<Record<NeedId, number>>)[need] ?? 0))
        const stays = v.source === 'friend' ? G.visitor.stays : 60
        next = note({ ...next, needs, credits: next.credits + (def.credits ?? 0), visits: next.visits.map((x) => (x === v ? { ...x, state: 'inside' as const, met: true, until: next.clock + stays } : x)) }, { kind: 'caller_met', who: v.who, amount: def.credits })
      }
      break
    }
    case 'phone_call': {
      const free = VISITORS.filter((x) => x.friend && !next.visits.some((y) => y.who === x.id && y.state !== 'gone'))
      if (free.length) {
        const dd = dice(next.rng)
        const who = dd.pick(free).id
        const at = next.clock + G.visitor.friendArrives
        next = note({ ...next, rng: dd.rng, phoneReadyAt: next.clock + G.phone.cooldownMinutes, visits: [...next.visits, { who, state: 'due' as const, at, until: at + G.visitor.waits, source: 'friend' as const, met: false }] }, { kind: 'friend_coming', who })
      }
      break
    }
    case 'phone_answer': {
      next = { ...next, ringing: null }
      const free = VISITORS.filter((x) => x.friend && !next.visits.some((y) => y.who === x.id && y.state !== 'gone'))
      if (free.length && next.clock < G.day.dusk) {
        const dd = dice(next.rng)
        const who = dd.pick(free).id
        const at = next.clock + G.visitor.friendArrives
        next = note({ ...next, rng: dd.rng, visits: [...next.visits, { who, state: 'due' as const, at, until: at + G.visitor.waits, source: 'friend' as const, met: false }] }, { kind: 'friend_coming', who })
      }
      break
    }
    case 'phone_pizza': {
      const cost = priceOf(next, foodById('pizza')!)
      if (next.credits >= cost) next = note({ ...next, credits: next.credits - cost, pizzaAt: next.clock + G.pizzaMinutes }, { kind: 'pizza_ordered', amount: cost })
      break
    }
    case 'bed_sleep':
      return endDay(note(next, { kind: 'bed', by: d.by }))
    default:
      break
  }
  return startNext(next)
}

/** What the telescope shows is on its way. */
function spotted(s: State): Loose {
  const caller = s.visits.find((c) => c.state === 'due')
  if (s.plan.storm && s.clock < s.plan.storm.from && (!caller || s.plan.storm.from < caller.at)) return { kind: 'spotted', what: 'storm', inMinutes: Math.round(s.plan.storm.from - s.clock) }
  if (caller) return { kind: 'spotted', what: 'caller', who: caller.who, inMinutes: Math.round(caller.at - s.clock) }
  if (s.plan.ship.state === 'due') return { kind: 'spotted', what: 'ship', inMinutes: Math.round(s.plan.ship.at - s.clock) }
  return { kind: 'spotted', what: 'nothing' }
}

/** Fix whatever he needs most, in order of what he would do about it. */
const FIX: Record<NeedId, readonly string[]> = {
  bladder: ['loo_wee'],
  hunger: ['fridge_snack', 'cooker_cook', 'cooker_toast'],
  energy: ['tv_nap', 'bed_nap'],
  hygiene: ['wash_basin'],
  social: ['pet_play', 'desk_diary'],
  fun: ['read_book', 'play_piano', 'tv_watch', 'scope_look'],
  tidiness: ['desk_tidy'],
}

/** Left alone with nothing to do, he chooses for himself: a need that is low, or something he fancies, or something with a visitor, or nothing. */
function chooseForHimself(s: State): State {
  const d = dice(s.rng)
  const lowest = [...NEEDS].sort((a, b) => s.needs[a] - s.needs[b])[0]
  let choice: Order | undefined
  if (s.needs[lowest] < G.self.needBelow) {
    const options = FIX[lowest].filter((id) => !(id === 'cooker_cook' && !foodFor(s, 'cooker_cook')) && !(id === 'fridge_snack' && !foodFor(s, 'fridge_snack')))
    const pick = options.find((id) => !s.personality.dislikes.includes(id)) ?? options[0]
    if (pick) choice = { id: pick }
  } else if (insideVisit(s) && d.next() < 0.7) {
    choice = { id: d.pick(['with_chat', 'with_cards', 'with_tv']) }
  } else if (d.next() < G.self.quirkChance) {
    const fancies = [...s.personality.likes, 'pet_play', 'play_piano', 'scope_look'].filter((f) => !(f === 'jetty_fish' && stormNow(s)))
    choice = { id: d.pick(fancies) }
    if (d.next() < 0.3) choice = { id: 'react', react: d.pick(['dance', 'sing', 'whistle', 'jump', 'laugh', 'bum', 'burp']) }
  }
  const next = { ...s, rng: d.rng, idle: 0 }
  if (!choice) return next
  return begin(note(next, { kind: 'chose', id: choice.id === 'react' ? 'react' : choice.id, react: choice.react }), choice, 'self', false)
}

/** The pet has a mind of its own: now and then it does something about the house. */
function petMind(s: State, dt: number): State {
  const d = dice(s.rng)
  const chance = (dt / 60) * 0.35
  if (d.next() >= chance) return { ...s, rng: d.rng }
  let next: State = { ...s, rng: d.rng }
  if (s.pet.hunger < 40) {
    // A hungry pet steals a snack if there is one, and otherwise yowls.
    const snacks = owned(s, 'snack')
    if (snacks.length) {
      const stolen = snacks[0]
      return note({ ...next, items: { ...next.items, [stolen]: (next.items[stolen] ?? 1) - 1 }, pet: { ...next.pet, hunger: clamp(next.pet.hunger + 18) } }, { kind: 'pet', petDid: 'steal', item: stolen })
    }
    return note(next, { kind: 'pet', petDid: 'knock' })
  }
  const roll2 = d.next()
  next = { ...next, rng: d.rng }
  if (roll2 < 0.4) return note({ ...next, needs: { ...next.needs, tidiness: clamp(next.needs.tidiness - 8) } }, { kind: 'pet', petDid: 'knock' })
  if (roll2 < 0.75) return note({ ...next, needs: { ...next.needs, fun: clamp(next.needs.fun + 4), social: clamp(next.needs.social + 4) } }, { kind: 'pet', petDid: 'purr' })
  return note({ ...next, needs: { ...next.needs, fun: clamp(next.needs.fun + 8) } }, { kind: 'pet', petDid: 'gift' })
}

/** Random faults use the same seeded luck as the rest of the day. */
function maybeBreak(s: State, dt: number): State {
  const every = s.rules.breakdownMinutes
  const limit = s.rules.maxBreakdowns
  if (every <= 0 || limit <= 0 || s.broken.length >= limit) return s
  const d = dice(s.rng)
  if (d.next() >= Math.min(1, dt / every)) return { ...s, rng: d.rng }
  const candidates = BREAKABLE_OBJECTS.filter((id) => !s.broken.includes(id) && s.doing?.object !== id && objectAvailable(s, id))
  if (!candidates.length) return { ...s, rng: d.rng }
  const id = d.pick(candidates)
  return note({ ...s, rng: d.rng, broken: [...s.broken, id] }, { kind: 'breakdown', id, text: BREAKDOWN_SFX[id] ?? 'mechanical-clunk' })
}

/** One step of time, no longer than a few minutes, so nothing is stepped over. */
function step(s0: State, dt: number): State {
  let s: State = { ...s0, clock: s0.clock + dt }
  const before = s0.clock
  const passed = (t: number) => before < t && s.clock >= t

  // His needs run down; in a storm, cooped up, his fun runs down faster.
  const needs = { ...s.needs }
  for (const need of NEEDS) needs[need] = clamp(needs[need] - (G.drift[need] * (need === 'fun' && stormNow(s) ? G.storm.funDrift : 1) * dt) / 60)
  const fade = (G.mood.spiritsFade * dt) / 60
  s = { ...s, needs, spirits: Math.abs(s.spirits) <= fade ? 0 : s.spirits - Math.sign(s.spirits) * fade }
  // The pet's own needs.
  s = { ...s, pet: { hunger: clamp(s.pet.hunger - (G.pet.hungerDrift * dt) / 60), fun: clamp(s.pet.fun - (G.pet.funDrift * dt) / 60), fright: Math.max(0, s.pet.fright - dt / 20) } }

  // Callers and friends.
  for (const c of s.visits) {
    if (c.state === 'due' && s.clock >= c.at) s = note({ ...s, visits: s.visits.map((x) => (x === c ? { ...x, state: 'waiting' as const } : x)) }, { kind: 'caller', who: c.who })
    else if (c.state === 'waiting' && s.clock >= c.at + G.visitor.waits && s.doing?.id !== 'door_greet') {
      s = note(lift({ ...s, visits: s.visits.map((x) => (x === c ? { ...x, state: 'gone' as const } : x)) }, -G.visitor.missed), { kind: 'caller_gone', who: c.who })
    } else if (c.state === 'inside' && s.clock >= c.until) s = note({ ...s, visits: s.visits.map((x) => (x === c ? { ...x, state: 'gone' as const } : x)) }, { kind: 'visitor_left', who: c.who })
  }
  const storm = s.plan.storm
  if (storm) {
    if (passed(storm.from)) s = note(s, { kind: 'storm', on: true })
    if (passed(storm.to)) s = note(s, { kind: 'storm', on: false })
    if (stormNow(s) && s.clock >= s.thunderAt) s = note({ ...s, thunderAt: s.thunderAt + G.storm.thunderEvery, pet: { ...s.pet, fright: 1 } }, { kind: 'thunder' })
  }
  if (passed(G.day.dusk)) s = note(s, { kind: 'dusk' })
  if (passed(s.plan.ship.at - G.ship.hornBefore)) s = note(s, { kind: 'horn' })
  if (s.lampLit) {
    const left = s.lampLeft - dt
    s = left <= 0 ? note({ ...s, lampLit: false, lampLeft: 0 }, { kind: 'lamp_out' }) : { ...s, lampLeft: left }
  }
  if (s.plan.ship.state === 'due' && s.clock >= s.plan.ship.at) s = note({ ...s, plan: { ...s.plan, ship: { ...s.plan.ship, state: s.lampLit ? 'safe' : 'close' } } }, { kind: 'ship', safe: s.lampLit })

  // The phone rings; the pizza comes.
  for (const t of s.plan.rings) if (passed(t) && !s.ringing) s = note({ ...s, ringing: { until: t + 30 } }, { kind: 'ring' })
  if (s.ringing && s.clock >= s.ringing.until) s = { ...s, ringing: null }
  if (s.pizzaAt !== null && s.clock >= s.pizzaAt) s = note({ ...s, pizzaAt: null, items: { ...s.items, pizza: (s.items.pizza ?? 0) + 1 } }, { kind: 'pizza_arrived' })

  s = maybeBreak(s, dt)

  // The pet's mischief.
  s = petMind(s, dt)

  // The job in hand.
  const d = s.doing
  if (d?.phase === 'going') {
    const going = d.going + dt
    s = going >= G.travelLimit ? arrive({ ...s, doing: { ...d, going } }) : { ...s, doing: { ...d, going } }
  } else if (d) {
    const share = d.total > 0 ? Math.min(dt, d.left) / d.total : 0
    const now = { ...s.needs }
    for (const need of NEEDS) now[need] = clamp(now[need] + (d.effects[need] ?? 0) * share)
    const left = d.left - dt
    s = { ...s, needs: now, doing: { ...d, left } }
    if (left <= 0) s = finish(s)
  }
  if (s.phase !== 'day') return s

  // Bedtime: he gets cross, and then he puts himself to bed.
  if (s.clock >= G.day.bedtime && s.doing?.id !== 'bed_sleep') {
    const level = annoyanceOf(s.clock) >= 85 ? 3 : annoyanceOf(s.clock) >= 55 ? 2 : annoyanceOf(s.clock) >= 15 ? 1 : 0
    if (level > s.annoyedLevel) s = note({ ...s, annoyedLevel: level }, { kind: 'annoyed', level })
  }
  const busyInLoo = s.doing?.priv === true
  if (s.clock >= G.day.forced && s.doing?.id !== 'bed_sleep' && !busyInLoo) {
    s = begin({ ...s, queue: [], doing: null, tally: { ...s.tally, forced: true } }, { id: 'bed_sleep' }, 'self', false)
  } else if (!s.doing) {
    // Nothing to do: he says what is wrong, and after a while sees to himself.
    s = { ...s, idle: s.idle + dt }
    const low = NEEDS.find((need) => s.needs[need] < G.self.moanBelow && !s.moaned.includes(need))
    if (low) s = note({ ...s, moaned: [...s.moaned, low] }, { kind: 'moan', need: low })
    // A bursting bladder cannot wait.
    if (s.needs.bladder < G.bursting) s = begin(s, { id: 'loo_wee' }, 'self', false)
    else if (s.idle >= G.self.idleMinutes) s = chooseForHimself(s)
  } else if (s.needs.bladder <= 0 && s.doing.by === 'self') {
    // He is already busy with his own business.
  }
  if (s.moaned.length) s = { ...s, moaned: s.moaned.filter((need) => s.needs[need] < G.self.moanBelow + 10) }

  const t = s.tally
  const needSums = { ...t.needSums }
  for (const need of NEEDS) needSums[need] += s.needs[need] * dt
  return { ...s, tally: { ...t, needSums, moodSum: t.moodSum + moodOf(s) * dt, minutes: t.minutes + dt, emptied: t.emptied || NEEDS.some((need) => s.needs[need] <= 0) } }
}

/** Time passes: `minutes` of his day. */
export function tick(s: State, minutes: number): State {
  let next = s
  for (let left = minutes; left > 1e-9 && next.phase === 'day'; left -= 4) next = step(next, Math.min(4, left))
  return next
}

// ─── Buying ──────────────────────────────────────────────────────────────────

/** Buy one thing in the shop (he must be at it). */
export function buy(s: State, foodId: string): State {
  const food = foodById(foodId)
  if (!food || food.cost <= 0 || food.kind === 'takeaway' || !shopOpen(s)) return s
  const cost = priceOf(s, food)
  if (s.credits < cost) return note(s, { kind: 'refuse', id: 'shop_buy', why: 'broke', item: foodId })
  return note({ ...s, credits: s.credits - cost, items: { ...s.items, [foodId]: (s.items[foodId] ?? 0) + 1 } }, { kind: 'bought', item: foodId, amount: cost })
}

// ─── Questions ───────────────────────────────────────────────────────────────

/** The keeper asks Ralph something. */
export function ask(s: State, prompt: Prompt): State {
  if (s.phase !== 'day' || s.prompt) return s
  return note({ ...s, prompt, tally: { ...s.tally, quizAsked: s.tally.quizAsked + (prompt.kind === 'quiz' ? 1 : 0) } }, { kind: prompt.kind === 'quiz' ? 'quiz' : 'chat', text: prompt.kind === 'quiz' ? prompt.quiz.text : prompt.chat.text })
}

/** A wrong go at a quiz. After enough, he says the answer, and Ralph must type it in. */
export function wrongAnswer(s: State): State {
  const p = s.prompt
  if (!p || p.kind !== 'quiz') return s
  const tries = p.tries + 1
  return { ...s, prompt: { ...p, tries, revealed: p.revealed || tries >= G.quiz.triesBeforeAnswer } }
}

/** A right answer: it clears. First time earns a full point; later, half; copied once he told the answer, none. */
export function rightAnswer(s: State): State {
  const p = s.prompt
  if (!p || p.kind !== 'quiz') return s
  const points = p.revealed ? 0 : p.tries === 0 ? 1 : 0.5
  const next = lift({ ...s, prompt: null, tally: { ...s.tally, quizPoints: s.tally.quizPoints + points }, needs: { ...s.needs, fun: clamp(s.needs.fun + 4) } }, 2)
  return note(next, { kind: 'quiz', correct: true })
}

/** Ralph has answered a chat question (the reply itself is worked out by `chat.ts`). */
export function answeredChat(s: State, good: boolean): State {
  if (!s.prompt || s.prompt.kind !== 'chat') return s
  const next = lift({ ...s, prompt: null, needs: { ...s.needs, social: clamp(s.needs.social + G.chat.socialGain) } }, good ? G.chat.spirits : 0)
  return note(next, { kind: 'chat', correct: good })
}

/** He lets a chat question go (a quiz never can). */
export function dropChat(s: State): State {
  return s.prompt?.kind === 'chat' ? { ...s, prompt: null } : s
}

// ─── The end of a day ────────────────────────────────────────────────────────

function endDay(s: State): State {
  let next = s
  if (next.plan.ship.state === 'due') {
    const safe = lampWillLast(next)
    next = note({ ...next, plan: { ...next.plan, ship: { ...next.plan.ship, state: safe ? 'safe' : 'close' } } }, { kind: 'ship', safe })
  }
  next = { ...next, visits: next.visits.map((c) => (c.state === 'waiting' || c.state === 'due' || c.state === 'inside' ? { ...c, state: 'gone' as const } : c)), doing: null, queue: [], prompt: null, phase: 'report' }
  const result = dayResult(next)
  next = { ...next, history: [...next.history, result] }
  return result.score >= G.missions.goodDay ? missionEvents(next, ['good_day']) : next
}

/** The marks for the day so far. */
export function dayResult(s: State): DayResult {
  const S = G.score
  const mood = s.tally.minutes > 0 ? s.tally.moodSum / s.tally.minutes : moodOf(s)
  const callers = s.visits
  const met = callers.filter((c) => c.met).length
  const social = s.needs.social
  const friends = callers.length ? Math.round((S.friends * met) / callers.length) : Math.round((S.friends * Math.min(100, social + 20)) / 100)
  const petOk = [s.pet.hunger >= S.petAt, s.pet.fun >= S.petAt].filter(Boolean).length
  const houseOk = [s.needs.tidiness >= S.houseAt, s.needs.hygiene >= S.houseAt].filter(Boolean).length
  const asked = s.tally.quizAsked
  const brain = asked === 0 ? S.brain : Math.round(S.brain * Math.min(1, s.tally.quizPoints / Math.min(asked, G.quiz.fullMarksAt)))
  const inTime = s.tally.bedAt !== null && s.tally.bedAt <= G.day.bedtime + S.bedWindow
  const bedtime = s.tally.forced ? 0 : inTime ? S.bedtime : Math.round(S.bedtime / 2)
  const shipSafe = s.plan.ship.state === 'safe'
  const parts: DayResult['parts'] = [
    { id: 'mood', got: Math.round((mood / 100) * S.mood), of: S.mood },
    { id: 'ship', got: shipSafe ? S.ship : 0, of: S.ship },
    { id: 'friends', got: friends, of: S.friends },
    { id: 'pet', got: Math.round((S.pet * petOk) / 2), of: S.pet },
    { id: 'house', got: Math.round((S.house * houseOk) / 2), of: S.house },
    { id: 'brain', got: brain, of: S.brain },
    { id: 'bedtime', got: bedtime, of: S.bedtime },
  ]
  const score = parts.reduce((sum, p) => sum + p.got, 0)
  const minutes = s.tally.minutes
  const needs = NEEDS.map((id) => {
    const avg = minutes > 0 ? s.tally.needSums[id] / minutes : s.needs[id]
    return { id, avg: Math.round(avg), green: avg >= s.rules.greenAt }
  })
  const greens = needs.filter((n) => n.green).length
  return { day: s.day, score, rating: G.ratings.find((r) => score >= r.from)!.id, parts, mood: Math.round(mood), needs, greens, shipSafe, allowance: allowanceFor(s.rules, greens) }
}

/** The next morning. Yesterday's score sets today's allowance. */
export function nextDay(s: State): State {
  if (s.phase !== 'report') return s
  const last = s.history[s.history.length - 1]
  const { plan, visits, rng } = planDay(s.rng)
  const O = G.overnight
  const allowance = last?.allowance ?? s.rules.allowanceBase
  const saved = Math.min(s.rules.carryCap, s.credits)
  const gardenGrows = s.garden.watered ? Math.min(3, s.garden.ready + 1) : s.garden.ready
  const next: State = {
    ...s,
    rng,
    day: s.day + 1,
    clock: G.day.start,
    needs: { ...s.needs, energy: G.upgrades.bedEnergy[Math.min(tierOf(s, 'bed'), G.upgrades.bedEnergy.length) - 1], hunger: Math.max(O.hungerFloor, s.needs.hunger - O.hungerLoss), bladder: Math.min(s.needs.bladder, O.bladder), hygiene: clamp(s.needs.hygiene - O.hygieneLoss) },
    spirits: s.spirits / 2,
    doing: null,
    queue: [],
    idle: 0,
    moaned: [],
    lampLit: false,
    lampLeft: 0,
    shine: clamp(s.shine - G.lamp.dullsOvernight),
    plan,
    visits,
    thunderAt: plan.storm ? plan.storm.from + 5 : Infinity,
    pet: { hunger: Math.max(35, s.pet.hunger - 20), fun: Math.max(35, s.pet.fun - 10), fright: 0 },
    credits: saved + allowance,
    garden: { ready: gardenGrows, watered: false },
    phoneReadyAt: 0,
    ringing: null,
    pizzaAt: null,
    annoyedLevel: 0,
    prompt: null,
    happenings: [],
    tally: freshTally(),
    phase: 'day',
  }
  return buildOvernight(note(next, { kind: 'dawn', amount: allowance }))
}

// Keep these exports used (the screen reads them).
export { INTERACTIONS, REACTIONS }
