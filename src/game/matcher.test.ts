import { describe, expect, it } from 'vitest'
import { COMMANDS, REACTIONS } from './commands'
import { INTERACTIONS } from './config'
import { distance, isNo, isYes, read, stem } from './matcher'

const ids = (r: ReturnType<typeof read>) => (r.kind === 'do' || r.kind === 'ask' ? r.doing.map((d) => d.react ?? d.id) : [])

describe('the command book', () => {
  it('only points at real interactions and reactions', () => {
    for (const c of COMMANDS) {
      for (const d of c.doing) {
        if (d.id === 'react') expect(REACTIONS.some((r) => r.id === d.react), `${c.id} -> ${d.react}`).toBe(true)
        else expect(INTERACTIONS.some((i) => i.id === d.id), `${c.id} -> ${d.id}`).toBe(true)
      }
    }
  })
  it('has a bucket for every interaction a player can ask for', () => {
    for (const i of INTERACTIONS) {
      expect(COMMANDS.some((c) => c.doing.some((d) => d.id === i.id)), i.id).toBe(true)
    }
  })
  it('uses every reaction', () => {
    const used = new Set(COMMANDS.flatMap((c) => c.doing.map((d) => d.react)))
    // shrug, wave and bow are used by the game itself, not typed.
    for (const r of REACTIONS) if (!['shrug', 'wave', 'bow'].includes(r.id)) expect(used.has(r.id), r.id).toBe(true)
  })
  it('gives the same answer every time', () => {
    for (const phrase of ['do a poo', 'burp', 'go fishing', 'tell a joke']) expect(read(phrase)).toEqual(read(phrase))
  })
})

describe('reading what he types', () => {
  it('sends him to the loo for a poo, however it is put', () => {
    for (const t of ['poo', 'do a poo', 'I need a poo!', 'please go and do a big stinky poo', 'sit on the loo', 'NUMBER TWO']) expect(ids(read(t)), t).toEqual(['loo_poo'])
  })
  it('knows a wee from a poo', () => {
    expect(ids(read('go to the toilet'))).toEqual(['loo_wee'])
    expect(ids(read('wee'))).toEqual(['loo_wee'])
  })
  it('does silly things', () => {
    expect(ids(read('burp'))).toEqual(['burp'])
    expect(ids(read('say bum'))).toEqual(['bum'])
    expect(ids(read('do the robot'))).toEqual(['robot'])
    expect(ids(read('be a chicken'))).toEqual(['chicken'])
  })
  it('does the proper jobs', () => {
    expect(ids(read('go fishing'))).toEqual(['jetty_fish'])
    expect(ids(read('please can you watch TV'))).toEqual(['tv_watch'])
    expect(ids(read('time for bed'))).toEqual(['bed_sleep'])
    expect(ids(read('light the lamp'))).toEqual(['lamp_light'])
    expect(ids(read('play the piano'))).toEqual(['play_piano'])
    expect(ids(read('order a pizza'))).toEqual(['phone_pizza'])
    expect(ids(read('phone a friend'))).toEqual(['phone_call'])
  })
  it('picks the food he names', () => {
    const r = read('cook some pasta')
    expect(r.kind).toBe('do')
    if (r.kind === 'do') expect(r.doing[0]).toEqual({ id: 'cooker_cook', item: 'pasta' })
    const e = read('eat pizza')
    if (e.kind === 'do') expect(e.doing[0].item).toBe('pizza')
  })
  it('chains jobs', () => {
    expect(ids(read('make some toast then play the piano'))).toEqual(['cooker_toast', 'play_piano'])
    expect(ids(read('go fishing and then go to bed'))).toEqual(['jetty_fish', 'bed_sleep'])
  })
  it('forgives a slip in a long word', () => {
    expect(ids(read('go fishhing'))).toEqual(['jetty_fish'])
    expect(ids(read('wath the telly'))[0]).toBeDefined()
    expect(read('play the pianno').kind).toBe('do')
  })
  it('asks "did you mean" for a near miss', () => {
    const r = read('cok')
    expect(['ask', 'shrug']).toContain(r.kind)
    const r2 = read('tidyy')
    expect(r2.kind).not.toBe('shrug')
    const r3 = read('fishig')
    if (r3.kind === 'ask') expect(r3.say).toBe('go fishing')
    expect(r3.kind).not.toBe('shrug')
  })
  it('shrugs at nonsense', () => {
    expect(read('qwertyuiop').kind).toBe('shrug')
    expect(read('zzz xx').kind).toBe('shrug')
    expect(read('   ').kind).toBe('empty')
  })
  it('does not mistake short words for others', () => {
    expect(read('pool').kind).not.toBe('do')
    expect(read('bad').kind).toBe('shrug')
  })
  it('understands yes and no', () => {
    expect(isYes('Yeah!')).toBe(true)
    expect(isYes('no')).toBe(false)
    expect(isNo('nope')).toBe(true)
  })
})

describe('the helpers', () => {
  it('counts slips, including swapped neighbours', () => {
    expect(distance('fish', 'fish')).toBe(0)
    expect(distance('fish', 'fihs')).toBe(1)
    expect(distance('fish', 'dish')).toBe(1)
    expect(distance('cat', 'cart')).toBe(1)
  })
  it('stems endings', () => {
    expect(stem('fishing')).toBe(stem('fish'))
    expect(stem('making')).toBe(stem('make'))
    expect(stem('cooking')).toBe(stem('cook'))
    expect(stem('bed')).toBe('bed')
  })
})
