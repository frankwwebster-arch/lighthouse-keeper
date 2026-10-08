import { afterEach, describe, expect, it } from 'vitest'
import { DEFAULT_RULES, MISSIONS, START_FLOORS } from './config'
import { arrive, completeMission, nextDay, order, setRules, startGame, tick, type Order, type State } from './engine'
import { countEvents, eventsOf, floorCount, freshMissions, goalTarget, goalsOf, insertFloor, objectAvailable, openMissions, rewardOf, started, towerOf } from './missions'
import { read } from './matcher'
import { revive } from './storage'
import { FLOOR_ORDER, FLOOR_Y, LAYOUT, applyLayout, route } from './world'

const fresh = (seed = 7): State => startGame(seed, { name: 'Barnaby', petName: 'Biscuit', petKind: 'cat', personality: { trait: 'cheerful', likes: [], dislikes: [] } })
/** Tell him, walk him there, and let the job finish (a nice day, so nothing gets in the way). */
const doIt = (s: State, o: Order): State => {
  let n = order({ ...s, plan: { ...s.plan, storm: null }, needs: { ...s.needs, bladder: 100 } }, [o])
  n = arrive(n)
  return tick(n, (n.doing?.left ?? 0) + 1)
}
/** Play out the day and wake up the next morning. */
const morning = (s: State): State => nextDay(tick(s, 17 * 60))
const ids = (list: { id: string }[]) => list.map((m) => m.id)

describe('missions', () => {
  it('are all open at once, except the lift, which waits for a taller lighthouse', () => {
    const m = freshMissions()
    expect(ids(openMissions(m, 3))).toEqual(['fishy', 'storm', 'rumble'])
    expect(ids(openMissions(m, 5))).toEqual(['fishy', 'storm', 'rumble', 'puffed'])
    expect(openMissions({ ...m, done: MISSIONS.map((x) => x.id) }, 9)).toEqual([])
  })

  it('counts the right happenings', () => {
    expect(eventsOf({ kind: 'done', id: 'jetty_fish' })).toEqual(['done:jetty_fish'])
    expect(eventsOf({ kind: 'ship', safe: true })).toEqual(['ship_safe'])
    expect(eventsOf({ kind: 'ship', safe: false })).toEqual([])
    expect(eventsOf({ kind: 'quiz', correct: true })).toEqual(['quiz_right'])
    expect(eventsOf({ kind: 'moan' })).toEqual([])
  })

  it('counts towards every open mission at once, and keeps a closed one waiting', () => {
    const m = countEvents(freshMissions(), ['done:scope_look', 'done:jetty_fish', 'quiz_right'], undefined, 3).missions
    expect(m.progress['fishy:0']).toBe(1)
    expect(m.progress['storm:0']).toBe(1)
    expect(m.progress['puffed:0']).toBeUndefined()
  })

  it('finishes whichever missions have every goal met, in any order', () => {
    const r = countEvents(freshMissions(), ['done:scope_look', 'done:scope_look', 'done:scope_look', 'ship_safe', 'ship_safe', 'ship_safe'], undefined, 3)
    expect(ids(r.finished)).toEqual(['storm'])
    expect(r.missions.done).toEqual(['storm'])
  })

  it('keeps a secret mission a mystery until he makes a start', () => {
    const rumble = MISSIONS.find((m) => m.secret)!
    expect(started(rumble, freshMissions())).toBe(false)
    expect(started(rumble, countEvents(freshMissions(), ['done:garden_tend'], undefined, 3).missions)).toBe(true)
  })
})

describe('missions in the game', () => {
  it('pays at once, then builds the floor overnight: it is there in the morning', () => {
    let s = fresh()
    expect(objectAvailable(s, 'tank')).toBe(false)
    for (let i = 0; i < 3; i++) s = doIt(s, { id: 'jetty_fish' })
    expect(s.missions.progress['fishy:0']).toBe(3)
    const credits = s.credits
    s = doIt(s, { id: 'tv_nature' })
    s = doIt(s, { id: 'tv_nature' })
    expect(s.credits).toBe(credits + DEFAULT_RULES.missionReward)
    expect(s.happenings.at(-1)).toMatchObject({ kind: 'mission_done', id: 'fishy', on: true })
    expect(s.unlocked).toEqual([])
    expect(s.arriving).toEqual(['aquarium'])
    s = morning(s)
    expect(s.unlocked).toEqual(['aquarium'])
    expect(s.arriving).toEqual([])
    expect(s.happenings.map((h) => h.kind)).toEqual(['dawn', 'unlocked'])
    expect(objectAvailable(s, 'tank')).toBe(true)
  })

  it('lets floors come in any order', () => {
    let s = completeMission(fresh(), 'storm')
    s = morning(s)
    expect(s.unlocked).toEqual(['weather'])
    s = morning(completeMission(s, 'fishy'))
    expect(s.unlocked).toEqual(['weather', 'aquarium'])
  })

  it('builds one floor a morning, the rest wait their turn', () => {
    let s = completeMission(completeMission(fresh(), 'fishy'), 'rumble')
    expect(s.arriving).toEqual(['aquarium', 'lair'])
    s = morning(s)
    expect(s.unlocked).toEqual(['aquarium'])
    s = morning(s)
    expect(s.unlocked).toEqual(['aquarium', 'lair'])
  })

  it('puts a new floor in a random middle place, keeps the bedroom under the lamp room, and never reshuffles', () => {
    const places = new Set<string>()
    for (let seed = 1; seed <= 30; seed++) {
      let s = morning(completeMission(startGame(seed, { name: 'B', petName: 'P', petKind: 'cat', personality: { trait: 'cheerful', likes: [], dislikes: [] } }), 'fishy'))
      const { stack } = towerOf(s)
      expect(stack[0]).toBe('ground')
      expect(stack.at(-1)).toBe('bedroom')
      places.add(s.middle.join())
      const before = s.middle
      s = morning(morning(s))
      expect(s.middle).toEqual(before)
    }
    expect(places).toEqual(new Set(['aquarium,living', 'living,aquarium']))
  })

  it('opens the lift mission once the tower is tall enough, and fits the lift at once', () => {
    let s = fresh()
    expect(completeMission(s, 'puffed')).toBe(s)
    s = morning(morning(completeMission(completeMission(s, 'fishy'), 'storm')))
    expect(floorCount(s)).toBe(5)
    s = completeMission(s, 'puffed')
    expect(s.unlocked).toContain('lift')
    expect(s.arriving).toEqual([])
  })

  it('will not use things on floors he has not got yet', () => {
    const s = order(fresh(), [{ id: 'tank_watch' }])
    expect(s.doing).toBeNull()
    expect(s.happenings.at(-1)).toMatchObject({ kind: 'refuse', why: 'missing' })
    const later = morning(completeMission(fresh(), 'fishy'))
    expect(order(later, [{ id: 'tank_watch' }]).doing?.id).toBe('tank_watch')
  })

  it('brings old saves up to date, bedroom back on top', () => {
    const old = fresh() as Partial<State>
    delete old.unlocked
    delete old.missions
    delete old.middle
    delete old.arriving
    const s = revive(JSON.parse(JSON.stringify(old)))!
    expect(s.unlocked).toEqual([])
    expect(s.middle).toEqual(['living'])
    expect(s.arriving).toEqual([])
    const grown = { ...fresh(), unlocked: ['weather', 'aquarium', 'lift'] } as Partial<State>
    delete grown.middle
    expect(revive(JSON.parse(JSON.stringify(grown)))!.middle).toEqual(['living', 'aquarium', 'weather'])
  })
})

describe('the tower grows', () => {
  afterEach(() => applyLayout(START_FLOORS, [], false))

  it('starts with three floors and the lamp room on top', () => {
    applyLayout(START_FLOORS, [], false)
    expect(FLOOR_ORDER).toEqual(['ground', 'living', 'bedroom', 'lamp'])
    expect(FLOOR_Y.lamp).toBe(220)
    expect(LAYOUT.top).toBe(0)
  })

  it('stacks the saved order, keeps the lamp room on top, and digs the lair below the ground', () => {
    const t = towerOf({ unlocked: ['aquarium', 'lair'], middle: ['aquarium', 'living'] })
    applyLayout(t.stack, t.below, false)
    expect(FLOOR_ORDER).toEqual(['lair', 'ground', 'aquarium', 'living', 'bedroom', 'lamp'])
    expect(FLOOR_Y.ground).toBe(640)
    expect(FLOOR_Y.bedroom).toBe(220)
    expect(FLOOR_Y.lamp).toBe(80)
    expect(FLOOR_Y.lair).toBe(780)
    expect(LAYOUT.slot).toMatchObject({ lair: -1, ground: 0, aquarium: 1, bedroom: 3 })
    expect(LAYOUT.bottom).toBeGreaterThan(780)
  })

  it('inserts into the middle at the place given', () => {
    expect(insertFloor(['living'], 'aquarium', 0)).toEqual(['aquarium', 'living'])
    expect(insertFloor(['living'], 'aquarium', 1.7)).toEqual(['living', 'aquarium'])
    expect(insertFloor(['living', 'aquarium'], 'aquarium', 0)).toEqual(['living', 'aquarium'])
  })

  it('walks down to the lair by the stairs, and out of the front door', () => {
    applyLayout(START_FLOORS, ['lair'], false)
    const path = route({ x: 400, floor: 'living' }, { x: 300, floor: 'lair' })
    expect(path.map((p) => p.floor)).toEqual(['living', 'ground', 'lair', 'lair'])
    const out = route({ x: 300, floor: 'lair' }, { x: 1040, floor: 'outside' })
    expect(out.at(-1)?.floor).toBe('outside')
  })
})

describe('typing about the new floors', () => {
  const ids = (t: string) => {
    const r = read(t)
    return r.kind === 'do' || r.kind === 'ask' ? r.doing.map((d) => d.id) : []
  }
  it('understands them without stealing the old commands', () => {
    expect(ids('watch the fish')).toEqual(['tank_watch'])
    expect(ids('feed the fish')).toEqual(['tank_feed'])
    expect(ids('check the weather')).toEqual(['weather_check'])
    expect(ids('go fishing')).toEqual(['jetty_fish'])
    expect(ids('fish')).toEqual(['jetty_fish'])
    expect(ids('feed the cat')).toEqual(['pet_feed'])
    expect(ids('watch tv')).toEqual(['tv_watch'])
  })
})

describe('the grown-ups set the size of missions', () => {
  const fishy = MISSIONS[0]
  const lift = MISSIONS[3]

  it('scales every goal at once, then lets one goal or one reward be set by hand', () => {
    const r = { ...DEFAULT_RULES, missionScale: 120 }
    expect(goalTarget(lift, 0, r)).toBe(12)
    expect(goalTarget(fishy, 0, r)).toBe(4)
    expect(goalTarget(fishy, 0, { ...r, missionScale: 25 })).toBe(1)
    const own = { ...r, missionGoals: { 'puffed:1': 3 }, missionReward: 15, missionRewards: { fishy: 25 } }
    expect(goalTarget(lift, 1, own)).toBe(3)
    expect(goalTarget(lift, 0, own)).toBe(12)
    expect(rewardOf(fishy, own)).toBe(25)
    expect(rewardOf(lift, own)).toBe(15)
  })

  it('counts towards the bigger target and pays the chosen reward', () => {
    const r = { ...DEFAULT_RULES, missionScale: 200, missionRewards: { fishy: 30 } }
    let s = setRules(fresh(), r)
    for (let i = 0; i < 4; i++) s = doIt(s, { id: 'tv_nature' })
    for (let i = 0; i < 5; i++) s = doIt(s, { id: 'jetty_fish' })
    expect(s.unlocked).toEqual([])
    expect(goalsOf(fishy, s.missions, s.rules).map((g) => `${g.got}/${g.count}`)).toEqual(['5/6', '4/4'])
    const credits = s.credits
    s = doIt(s, { id: 'jetty_fish' })
    expect(s.arriving).toEqual(['aquarium'])
    expect(s.credits).toBe(credits + 30)
  })

  it('finishes a mission at once if its target is lowered below what he has done', () => {
    let s = fresh()
    for (let i = 0; i < 3; i++) s = doIt(s, { id: 'jetty_fish' })
    s = doIt(s, { id: 'tv_nature' })
    expect(s.unlocked).toEqual([])
    s = setRules(s, { ...s.rules, missionGoals: { 'fishy:1': 1 } })
    expect(s.arriving).toEqual(['aquarium'])
  })

  it('keeps counting past a target, so raising it later loses nothing', () => {
    const m = countEvents(freshMissions(), ['done:jetty_fish', 'done:jetty_fish', 'done:jetty_fish', 'done:jetty_fish'], { missionScale: 200 }, 3).missions
    expect(m.progress['fishy:0']).toBe(4)
  })
})
