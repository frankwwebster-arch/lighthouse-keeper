import { DEFAULT_RULES, foodById } from './config'
import { describe, expect, it } from 'vitest'
import { GAME as G } from './config'
import {
  allowanceFor, annoyanceOf, dayResult, gift, priceOf, setRules, answeredChat, arrive, ask, buy, moodOf, nextDay, order, rightAnswer, rollPersonality, shopOpen, startGame, tick, wrongAnswer,
  type Order, type State,
} from './engine'
import { makeQuiz } from './quiz'
import { CHATS } from './chat'

const fresh = (seed = 7): State => startGame(seed, { name: 'Barnaby', petName: 'Biscuit', petKind: 'cat', personality: { trait: 'cheerful', likes: ['tv_watch', 'read_book'], dislikes: ['garden_tend'] } })
/** Tell him, walk him there, and let the job finish. */
const doIt = (s: State, o: Order | Order[], extra = 0): State => {
  let n = order(s, Array.isArray(o) ? o : [o])
  n = arrive(n)
  return tick(n, (n.doing?.left ?? 0) + extra + 1)
}

describe('starting', () => {
  it('begins at seven in the morning with money in his pocket', () => {
    const s = fresh()
    expect(s.clock).toBe(G.day.start)
    expect(s.credits).toBe(G.credits.first)
    expect(s.items.toast).toBeGreaterThan(0)
    expect(s.phase).toBe('day')
  })
  it('plays the same days from the same seed', () => {
    const a = tick(fresh(3), 300)
    const b = tick(fresh(3), 300)
    expect(a).toEqual(b)
    expect(tick(fresh(4), 300).plan).not.toEqual(a.plan)
  })
  it('gives each keeper tastes', () => {
    const p = rollPersonality(11)
    expect(p.likes).toHaveLength(2)
    expect(p.dislikes).toHaveLength(1)
  })
})

describe('needs', () => {
  it('run down, and a job fills one', () => {
    let s = fresh()
    s = tick(s, 120)
    const hungry = s.needs.hunger
    expect(hungry).toBeLessThan(G.startNeeds.hunger)
    s = doIt(s, { id: 'cooker_toast' })
    expect(s.needs.hunger).toBeGreaterThan(hungry)
  })
  it('looks after himself when left alone', () => {
    let s = fresh()
    s = tick(s, 5 * 60)
    expect(s.happenings.some((h) => h.kind === 'chose' || h.kind === 'done')).toBe(true)
  })
})

describe('the loo', () => {
  it('a poo takes a long time, locks the door, and cannot be interrupted', () => {
    let s = order(fresh(), [{ id: 'loo_poo' }])
    s = arrive(s)
    expect(s.doing?.priv).toBe(true)
    expect(s.doing?.fx).toBe('stench')
    const again = order(s, [{ id: 'tv_watch' }])
    expect(again.doing?.id).toBe('loo_poo')
    expect(again.happenings.some((h) => h.kind === 'locked')).toBe(true)
    s = tick(s, 20)
    expect(s.doing).toBeNull()
    expect(s.needs.bladder).toBeGreaterThan(90)
  })
  it('will do nothing else when bursting', () => {
    let s = fresh()
    s = { ...s, needs: { ...s.needs, bladder: 5 } }
    s = order(s, [{ id: 'tv_watch' }])
    expect(s.happenings.some((h) => h.kind === 'refuse' && h.why === 'bursting')).toBe(true)
    expect(s.doing?.id).toBe('loo_wee')
  })
})

describe('questions', () => {
  it('a quiz holds back the treats but never the basics', () => {
    let s = fresh()
    s = ask(s, { kind: 'quiz', quiz: makeQuiz(() => 0.1), tries: 0, revealed: false })
    expect(s.prompt?.kind).toBe('quiz')
    const tv = order(s, [{ id: 'tv_watch' }])
    expect(tv.happenings.some((h) => h.kind === 'refuse' && h.why === 'quiz')).toBe(true)
    expect(tv.doing).toBeNull()
    const loo = order(s, [{ id: 'loo_wee' }])
    expect(loo.doing?.id).toBe('loo_wee')
    const bed = order(s, [{ id: 'wash_basin' }])
    expect(bed.doing?.id).toBe('wash_basin')
  })
  it('a right answer lets the treats through', () => {
    let s = ask(fresh(), { kind: 'quiz', quiz: makeQuiz(() => 0.1), tries: 0, revealed: false })
    s = rightAnswer(s)
    expect(s.prompt).toBeNull()
    expect(s.tally.quizPoints).toBe(1)
    s = order(s, [{ id: 'tv_watch' }])
    expect(s.doing?.id).toBe('tv_watch')
  })
  it('tells him the answer after a few wrong goes, and then gives no marks', () => {
    let s = ask(fresh(), { kind: 'quiz', quiz: makeQuiz(() => 0.1), tries: 0, revealed: false })
    for (let i = 0; i < G.quiz.triesBeforeAnswer; i++) s = wrongAnswer(s)
    expect(s.prompt?.kind === 'quiz' && s.prompt.revealed).toBe(true)
    s = rightAnswer(s)
    expect(s.tally.quizPoints).toBe(0)
  })
  it('one question at a time', () => {
    let s = ask(fresh(), { kind: 'chat', chat: CHATS[0] })
    const again = ask(s, { kind: 'quiz', quiz: makeQuiz(() => 0.1), tries: 0, revealed: false })
    expect(again.prompt?.kind).toBe('chat')
    s = answeredChat(s, true)
    expect(s.prompt).toBeNull()
  })
})

describe('money and food', () => {
  it('cooking needs real ingredients, and falls back to toast', () => {
    let s = fresh()
    const n = order(s, [{ id: 'cooker_cook' }])
    expect(n.happenings.some((h) => h.kind === 'refuse' && h.why === 'empty')).toBe(true)
    expect(n.doing?.id).toBe('cooker_toast')
    s = { ...s, items: { ...s.items, pasta: 1 } }
    s = doIt(s, { id: 'cooker_cook', item: 'pasta' })
    expect(s.items.pasta).toBe(0)
    expect(s.needs.hunger).toBeGreaterThan(70)
  })
  it('the shop sells things for credits, only while he is there', () => {
    let s = fresh()
    expect(buy(s, 'cake')).toEqual(s)
    s = arrive(order(s, [{ id: 'shop_buy' }]))
    expect(shopOpen(s)).toBe(true)
    s = buy(s, 'cake')
    expect(s.items.cake).toBe(1)
    expect(s.credits).toBe(G.credits.first - 3)
    s = { ...s, credits: 1 }
    const broke = buy(s, 'sausages')
    expect(broke.items.sausages ?? 0).toBe(0)
    expect(broke.credits).toBe(1)
  })
  it('a takeaway pizza costs credits, takes a while, and cannot be bought with none', () => {
    let s = fresh()
    s = doIt(s, { id: 'phone_pizza' })
    expect(s.credits).toBe(G.credits.first - 10)
    expect(s.pizzaAt).not.toBeNull()
    s = tick(s, G.pizzaMinutes + 5)
    expect(s.items.pizza).toBe(1)
    const broke = order({ ...s, credits: 3 }, [{ id: 'phone_pizza' }])
    expect(broke.happenings.some((h) => h.kind === 'refuse' && h.why === 'broke')).toBe(true)
  })
})

describe('the phone', () => {
  it('invites a friend over, then is not available again for a while', () => {
    let s = fresh()
    s = doIt(s, { id: 'phone_call' })
    expect(s.visits.some((v) => v.source === 'friend')).toBe(true)
    const again = order(s, [{ id: 'phone_call' }])
    expect(again.happenings.some((h) => h.kind === 'refuse' && h.why === 'phone_busy')).toBe(true)
  })
  it('will not ring when in a bad mood', () => {
    let s = fresh()
    s = { ...s, needs: { ...s.needs, hunger: 2, fun: 2, social: 2, energy: 5 }, spirits: -25 }
    expect(moodOf(s)).toBeLessThan(G.phone.moodMin)
    const n = order(s, [{ id: 'phone_call' }])
    expect(n.happenings.some((h) => h.kind === 'refuse' && (h.why === 'phone_mood' || h.why === 'grumpy'))).toBe(true)
    expect(n.doing).toBeNull()
  })
  it('a friend who turns up can be let in and joined', () => {
    let s = doIt(fresh(), { id: 'phone_call' })
    s = tick(s, G.visitor.friendArrives + 5)
    expect(s.visits.find((v) => v.state === 'waiting')).toBeDefined()
    s = doIt(s, { id: 'door_greet' })
    expect(s.visits.find((v) => v.state === 'inside')).toBeDefined()
    s = doIt(s, { id: 'with_cards' })
    expect(s.happenings.some((h) => h.kind === 'done' && h.id === 'with_cards')).toBe(true)
  })
  it('nobody to greet means no greeting', () => {
    const n = order(fresh(), [{ id: 'door_greet' }])
    expect(n.happenings.some((h) => h.kind === 'refuse' && h.why === 'nobody')).toBe(true)
  })
})

describe('bedtime and the next day', () => {
  const toEight = (s: State) => tick(s, G.day.bedtime - s.clock)
  it('gets crosser the later it gets', () => {
    expect(annoyanceOf(G.day.bedtime - 1)).toBe(0)
    expect(annoyanceOf(G.day.forced)).toBe(100)
    let s = fresh()
    s = toEight({ ...s, plan: { ...s.plan, storm: null }, visits: [] })
    s = { ...s, doing: null, queue: [] }
    s = tick(s, 60)
    expect(s.happenings.some((h) => h.kind === 'annoyed')).toBe(true)
  })
  it('puts himself to bed if nobody does, with no marks for bedtime', () => {
    let s = fresh()
    s = tick(s, 17 * 60)
    expect(s.phase).toBe('report')
    expect(s.tally.forced).toBe(true)
    expect(s.history[0].parts.find((p) => p.id === 'bedtime')?.got).toBe(0)
  })
  it('a nap, before bedtime, is only a nap', () => {
    const s = order(fresh(), [{ id: 'bed_sleep' }])
    expect(s.doing?.id).toBe('bed_nap')
  })
  it('going to bed on time earns the bedtime marks and ends the day', () => {
    let s = fresh()
    s = tick(s, G.day.bedtime - s.clock - 20)
    s = doIt({ ...s, doing: null, queue: [] }, { id: 'bed_sleep' })
    expect(s.phase).toBe('report')
    expect(s.history).toHaveLength(1)
    const r = s.history[0]
    expect(r.parts.reduce((a, p) => a + p.of, 0)).toBe(100)
    expect(r.parts.find((p) => p.id === 'bedtime')?.got).toBe(G.score.bedtime)
  })
  it("tomorrow's allowance follows how many needs ended green", () => {
    expect(allowanceFor(DEFAULT_RULES, 7)).toBe(DEFAULT_RULES.allowanceBase + DEFAULT_RULES.allowanceBonus)
    expect(allowanceFor(DEFAULT_RULES, 7)).toBeGreaterThan(allowanceFor(DEFAULT_RULES, 3))
    expect(allowanceFor(DEFAULT_RULES, 0)).toBe(DEFAULT_RULES.allowanceBase)
    let s = fresh()
    s = tick(s, 17 * 60)
    expect(s.phase).toBe('report')
    const greens = s.history[0].greens
    const credits = s.credits
    s = nextDay(s)
    expect(s.phase).toBe('day')
    expect(s.day).toBe(2)
    expect(s.clock).toBe(G.day.start)
    expect(s.credits).toBe(Math.min(s.rules.carryCap, credits) + allowanceFor(s.rules, greens))
    expect(s.needs.energy).toBe(G.overnight.energy)
    expect(s.prompt).toBeNull()
  })
  it('a better day gives more money next morning', () => {
    const play = (good: boolean) => {
      let s = fresh(21)
      s = { ...s, plan: { ...s.plan, storm: null } }
      if (good) {
        while (s.phase === 'day' && s.clock < G.day.bedtime - 30) {
          const lowest = Object.entries(s.needs).sort((a, b) => a[1] - b[1])[0][0]
          const fix: Record<string, string> = { hunger: 'cooker_toast', energy: 'tv_nap', fun: 'play_piano', hygiene: 'wash_basin', bladder: 'loo_wee', social: 'pet_play', tidiness: 'desk_tidy' }
          if (s.clock >= G.day.dusk && !s.lampLit && s.plan.ship.state === 'due') s = doIt({ ...s, doing: null }, { id: 'lamp_light' })
          else s = doIt({ ...s, doing: null }, { id: fix[lowest] })
          if (s.pet.hunger < 50) s = doIt(s, { id: 'pet_feed' })
        }
      } else s = tick(s, 17 * 60)
      if (s.phase === 'day') s = doIt({ ...s, doing: null, queue: [] }, { id: 'bed_sleep' })
      return s.history[0]
    }
    expect(play(true).score).toBeGreaterThan(play(false).score)
    expect(play(true).allowance).toBeGreaterThan(play(false).allowance)
  })
  it('one neglected need does not cost the others their green bars', () => {
    let s = fresh()
    s = { ...s, needs: { ...s.needs, tidiness: 0 }, tally: { ...s.tally, minutes: 100, needSums: { hunger: 8000, energy: 8000, fun: 8000, hygiene: 8000, bladder: 8000, social: 8000, tidiness: 0 } } }
    const r = dayResult(s)
    expect(r.greens).toBe(6)
    expect(r.needs.find((n) => n.id === 'tidiness')?.green).toBe(false)
    expect(r.allowance).toBe(allowanceFor(s.rules, 6))
  })
  it('the grown-up can change prices, the allowance, and gift credits', () => {
    let s = fresh()
    const cake = foodById('cake')!
    expect(priceOf(s, cake)).toBe(cake.cost)
    s = setRules(s, { ...s.rules, priceScale: 200 })
    expect(priceOf(s, cake)).toBe(cake.cost * 2)
    s = setRules(s, { ...s.rules, prices: { cake: 1 } })
    expect(priceOf(s, cake)).toBe(1)
    expect(priceOf(s, foodById('toast')!)).toBe(0)
    const before = s.credits
    s = gift(s, 15)
    expect(s.credits).toBe(before + 15)
    expect(s.happenings.some((h) => h.kind === 'credits' && h.amount === 15)).toBe(true)
    s = setRules(s, { ...s.rules, allowanceBase: 30, allowanceBonus: 0 })
    expect(allowanceFor(s.rules, 0)).toBe(30)
  })
  it('a lit lamp saves the ship', () => {
    let s = fresh()
    s = tick(s, 11 * 60)
    s = doIt({ ...s, doing: null }, { id: 'lamp_light' })
    expect(s.lampLit).toBe(true)
    s = tick(s, G.ship.latest - s.clock + 5)
    expect(s.plan.ship.state).toBe('safe')
  })
})

describe('the pet', () => {
  it('goes hungry and can be fed', () => {
    let s = tick(fresh(), 5 * 60)
    const before = s.pet.hunger
    expect(before).toBeLessThan(G.pet.startHunger)
    s = doIt(s, { id: 'pet_feed' })
    expect(s.pet.hunger).toBeGreaterThan(before)
  })
  it('has a mind of its own', () => {
    let seen = false
    for (let seed = 1; seed < 40 && !seen; seed++) {
      const s = tick(fresh(seed), 12 * 60)
      seen = s.happenings.some((h) => h.kind === 'pet') || s.history.length > 0
    }
    expect(seen).toBe(true)
  })
})

describe('silly reactions', () => {
  it('a burp is a short silly job, and the game carries on', () => {
    let s = fresh()
    s = doIt(s, { id: 'react', react: 'burp' })
    expect(s.happenings.some((h) => h.kind === 'react' && h.react === 'burp')).toBe(true)
    expect(s.doing).toBeNull()
  })
})
