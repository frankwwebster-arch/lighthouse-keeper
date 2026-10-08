import { afterEach, describe, expect, it } from 'vitest'
import { GAME as G, MISSIONS, START_FLOORS } from './config'
import { arrive, completeMission, order, startGame, tick, type Order, type State } from './engine'
import { activeMission, countEvents, eventsOf, freshMissions, goalsOf, objectAvailable, roomFloors } from './missions'
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

describe('missions', () => {
  it('runs one at a time, in order, starting with the aquarium', () => {
    const m = freshMissions()
    expect(activeMission(m)?.unlocks).toBe('aquarium')
    expect(activeMission({ ...m, done: ['fishy'] })?.unlocks).toBe('weather')
    expect(activeMission({ ...m, done: MISSIONS.map((x) => x.id) })).toBeUndefined()
  })

  it('counts the right happenings', () => {
    expect(eventsOf({ kind: 'done', id: 'jetty_fish' })).toEqual(['done:jetty_fish'])
    expect(eventsOf({ kind: 'ship', safe: true })).toEqual(['ship_safe'])
    expect(eventsOf({ kind: 'ship', safe: false })).toEqual([])
    expect(eventsOf({ kind: 'quiz', correct: true })).toEqual(['quiz_right'])
    expect(eventsOf({ kind: 'moan' })).toEqual([])
  })

  it('only counts towards the mission on the go, and never past the goal', () => {
    let m = countEvents(freshMissions(), ['done:scope_look', 'done:jetty_fish']).missions
    m = countEvents(m, ['done:jetty_fish', 'done:jetty_fish', 'done:jetty_fish']).missions
    const goals = goalsOf(activeMission(m)!, m)
    expect(goals.map((g) => g.got)).toEqual([3, 0])
    expect(m.progress['storm:0']).toBeUndefined()
  })

  it('finishes when every goal is met', () => {
    const r = countEvents(freshMissions(), ['done:jetty_fish', 'done:jetty_fish', 'done:jetty_fish', 'done:tv_nature', 'done:tv_nature'])
    expect(r.finished?.id).toBe('fishy')
    expect(r.missions.done).toEqual(['fishy'])
  })
})

describe('missions in the game', () => {
  it('counts his jobs, then unlocks a furnished floor and pays a reward', () => {
    let s = fresh()
    expect(objectAvailable(s, 'tank')).toBe(false)
    for (let i = 0; i < 3; i++) s = doIt(s, { id: 'jetty_fish' })
    expect(s.missions.progress['fishy:0']).toBe(3)
    const credits = s.credits
    s = doIt(s, { id: 'tv_nature' })
    s = doIt(s, { id: 'tv_nature' })
    expect(s.unlocked).toEqual(['aquarium'])
    expect(s.credits).toBe(credits + G.missions.reward)
    expect(s.happenings.map((h) => h.kind)).toEqual(expect.arrayContaining(['mission_done', 'unlocked']))
    expect(objectAvailable(s, 'tank')).toBe(true)
    expect(activeMission(s.missions)?.id).toBe('storm')
  })

  it('will not use things on floors he has not got yet', () => {
    const s = order(fresh(), [{ id: 'tank_watch' }])
    expect(s.doing).toBeNull()
    expect(s.happenings.at(-1)).toMatchObject({ kind: 'refuse', why: 'missing' })
    const later = completeMission(fresh())
    expect(order(later, [{ id: 'tank_watch' }]).doing?.id).toBe('tank_watch')
  })

  it('lets the grown-ups finish the current mission', () => {
    let s = fresh()
    for (const m of MISSIONS) {
      expect(activeMission(s.missions)?.id).toBe(m.id)
      s = completeMission(s)
    }
    expect(s.unlocked).toEqual(['aquarium', 'weather', 'lair', 'lift'])
    expect(completeMission(s)).toBe(s)
  })

  it('brings old saves up to date', () => {
    const old = fresh() as Partial<State>
    delete old.unlocked
    delete old.missions
    const s = revive(JSON.parse(JSON.stringify(old)))!
    expect(s.unlocked).toEqual([])
    expect(activeMission(s.missions)?.id).toBe('fishy')
  })
})

describe('the tower grows', () => {
  afterEach(() => applyLayout(START_FLOORS, false))

  it('starts with three floors and the lamp room on top', () => {
    applyLayout(START_FLOORS, false)
    expect(FLOOR_ORDER).toEqual(['ground', 'living', 'bedroom', 'lamp'])
    expect(FLOOR_Y.lamp).toBe(220)
    expect(LAYOUT.top).toBe(0)
  })

  it('stacks new floors above, keeps the lamp room on top, and digs the lair below the ground', () => {
    applyLayout(roomFloors(['aquarium', 'lair']), false)
    expect(FLOOR_ORDER).toEqual(['lair', 'ground', 'living', 'bedroom', 'aquarium', 'lamp'])
    expect(FLOOR_Y.ground).toBe(640)
    expect(FLOOR_Y.aquarium).toBe(220)
    expect(FLOOR_Y.lamp).toBe(80)
    expect(FLOOR_Y.lair).toBe(780)
    expect(LAYOUT.slot).toMatchObject({ lair: -1, ground: 0, aquarium: 3 })
    expect(LAYOUT.bottom).toBeGreaterThan(780)
  })

  it('walks down to the lair by the stairs, and out of the front door', () => {
    applyLayout(roomFloors(['lair']), false)
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
