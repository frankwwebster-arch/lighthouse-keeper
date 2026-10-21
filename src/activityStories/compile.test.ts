import fs from 'node:fs'
import path from 'node:path'
import { describe, expect, it } from 'vitest'
import { compileStory, type FrameItem } from './compile'
import { STORY_DRAFTS, STORY_FILES, LIBRARY, STYLE_REVIEW } from './drafts'
import { canPlace, styleOf, cleanStory, groupPictures, OTHER_GROUP, placePicture, playsText, swapPicture, type Library, type Story } from './format'

const objects = <T extends { kind: string }>(items: T[]) => items.filter((i) => i.kind === 'object')

describe('bubble story drafts', () => {
  it('lists every story file in data/activity-stories/stories', () => {
    const files = fs.readdirSync(path.resolve(__dirname, '../../data/activity-stories/stories')).map((f) => f.replace(/\.json$/, ''))
    expect(Object.keys(STORY_FILES).sort()).toEqual(files.sort())
    expect(STORY_DRAFTS).toHaveLength(files.length)
  })

  for (const story of STORY_DRAFTS) {
    describe(story.label, () => {
      const c = compileStory(story, LIBRARY)

      it('compiles with no errors and never rushes (at least 5 seconds)', () => {
        expect(c.issues.filter((i) => i.level === 'error')).toEqual([])
        expect(c.seconds).toBeGreaterThanOrEqual(5)
      })

      it('shows every cast member at some point', () => {
        for (const as of Object.keys(story.cast)) expect(c.full.some((f) => f.items.some((i) => i.id === as))).toBe(true)
      })

      it('fires every touch mark when the two pictures actually touch', () => {
        expect(c.contacts.length).toBeGreaterThan(0)
        for (const t of c.contacts) expect(t.gap, `${t.actor} → ${t.target} at frame ${t.frame}`).toBeLessThanOrEqual(4)
      })

      it('keeps the quiet ending completely still, with no marks (circling props carry on)', () => {
        const q = c.full.slice(c.quiet[0], c.quiet[1] + 1)
        const story = (items: (typeof q)[0]['items']) => items.filter((i) => !i.id.startsWith('prop-'))
        expect(q.length).toBeGreaterThanOrEqual(5)
        for (const f of q) {
          expect(f.items.filter((i) => i.kind === 'mark')).toEqual([])
          expect(story(f.items)).toEqual(story(q[0].items))
        }
      })

      it('draws motion trails beneath every object', () => {
        for (const f of c.full) {
          const lowest = Math.min(...objects(f.items).filter((i) => !i.id.startsWith('prop-')).map((i) => i.z))
          for (const t of f.items.filter((i) => i.id.startsWith('trail-'))) expect(t.z).toBeLessThan(lowest)
        }
      })

      it('reduced motion: at most two objects and one mark, nothing travels within a step, same frame count', () => {
        expect(c.reduced).toHaveLength(c.full.length)
        for (const f of c.reduced) {
          expect(objects(f.items).length).toBeLessThanOrEqual(2)
          expect(f.items.filter((i) => i.kind === 'mark').length).toBeLessThanOrEqual(1)
        }
        for (const w of c.windows) {
          const frames = c.reduced.slice(w.start, w.end)
          for (const f of frames) for (const i of f.items) {
            const first = frames[0].items.find((j) => j.id === i.id) ?? i
            expect([i.x, i.y, i.rotation]).toEqual([first.x, first.y, first.rotation])
          }
        }
      })

      it('reduced motion ends on pictures from the full-motion ending (an empty bubble if everything was served)', () => {
        const end = (frames: typeof c.full) => objects(frames[c.storyFrames - 1].items).filter((i) => !i.id.startsWith('prop-')).map((i) => i.id)
        const full = end(c.full)
        for (const id of end(c.reduced)) expect(full).toContain(id)
        expect(end(c.reduced).length > 0).toBe(full.length > 0)
      })

      it('loops cleanly: clears after the quiet moment, or flows straight back to its retelling step', () => {
        if (c.loopStart > 0) {
          // The end must look exactly like the moment before the retelling starts (the hot BBQ alone).
          const shown = (f: number) => objects(c.full[f].items).filter((i) => !i.id.startsWith('prop-')).map((i) => [i.id, i.x, i.y, i.scale])
          expect(c.full.length).toBe(c.storyFrames)
          expect(shown(c.full.length - 1)).toEqual(shown(c.loopStart - 1))
        } else {
          expect(c.full.length).toBe(c.storyFrames + 3)
          const left = objects(c.full.at(-1)!.items).filter((i) => !i.id.startsWith('prop-'))
          expect(left.every((i) => i.opacity < 0.05)).toBe(true)
        }
      })
    })
  }
})

describe('picture library', () => {
  it('a new current version reaches every story, and a pinned cast member keeps the old one', () => {
    const lib = structuredClone(LIBRARY) as Library
    const grill = lib.pictures['bbq-grill']
    const next = Math.max(...grill.versions.map((version) => version.v)) + 1
    const replacement = `/activity-stories/pictures/bbq-grill-v${next}.png`
    grill.versions.push({ ...grill.versions[0], v: next, url: replacement })
    grill.current = next
    const story = STORY_DRAFTS.find((s) => s.id === 'garden-bbq')!
    const urlOf = (s: typeof story) => compileStory(s, lib).full.flatMap((f) => f.items).find((i) => i.id === 'grill')?.url
    expect(urlOf(story)).toBe(replacement)
    const pinned = { ...story, cast: { ...story.cast, grill: { ...story.cast.grill, version: 1 } } }
    expect(urlOf(pinned)).toBe(grill.versions[0].url)
  })

  it('reports a picture the library does not have', () => {
    const story = cleanStory({ ...STORY_DRAFTS[0], cast: { ...STORY_DRAFTS[0].cast, grill: { picture: 'no-such-thing', role: 'hero' } } })!
    expect(compileStory(story, LIBRARY).issues.some((i) => i.level === 'error' && i.text.includes('no-such-thing'))).toBe(true)
  })

  it('reports a step that acts on something not yet on show', () => {
    const s = STORY_DRAFTS[0]
    const story = { ...s, steps: [s.steps[0], { do: 'flip' as const, who: 'sausages', onto: 'burgers' }, ...s.steps.slice(1)] }
    expect(compileStory(story, LIBRARY).issues.some((i) => i.level === 'error' && i.text.includes('burgers'))).toBe(true)
  })
})

describe('library checker', () => {
  it('npm run verify:activity-stories passes', async () => {
    const { execFileSync } = await import('node:child_process')
    expect(execFileSync('node', [path.resolve(__dirname, '../../scripts/verify_activity_stories.mjs')], { encoding: 'utf8' })).toContain('check out')
  })
})

describe('Garden BBQ reads left to right', () => {
  const story = STORY_DRAFTS.find((s) => s.id === 'garden-bbq')!
  const c = compileStory(story, LIBRARY)
  const at = (f: number, id: string) => c.full[f].items.find((i) => i.id === id)

  it('brings every ingredient in from the left', () => {
    for (const id of ['charcoal', 'sausages', 'patties', 'tomato', 'lettuce', 'cheese', 'steak']) {
      const first = c.full.findIndex((f) => f.items.some((i) => i.id === id))
      expect(at(first, id)!.x, id).toBeLessThan(-60)
    }
  })

  it('serves each finished dish off to the right, leaving the hot BBQ alone for a beat', () => {
    for (const id of ['hotdogs', 'burgers', 'meal']) {
      const seen = c.full.map((f, k) => [k, f.items.find((i) => i.id === id)] as const).filter(([, i]) => i)
      const lastSeen = seen.at(-1)!
      expect(lastSeen[1]!.x, id).toBeGreaterThan(100)
      // Just after it has gone, only the grill (and props/marks) remain.
      expect(objects(c.full[lastSeen[0] + 1].items).filter((i) => !i.id.startsWith('prop-')).map((i) => i.id), id).toEqual(['grill'])
    }
  })

  it('retells from the hot BBQ, so the cold grill and charcoal only play the first time', () => {
    expect(c.loopStart).toBe(c.windows[3].start)
    for (let f = c.loopStart; f < c.full.length; f++) for (const id of ['cold', 'charcoal']) expect(at(f, id)).toBeUndefined()
    expect(c.tellings[1]).toBeGreaterThanOrEqual(1)
  })
})

describe('a result that takes a stacked picture’s place', () => {
  it('stays on the grill: fillings go onto raw burgers, the finished burgers replace them on the grill, then a steak replaces the burgers', () => {
    // Stand-in pictures until Codex's uncooked burgers, cheese and steak arrive.
    const story = cleanStory({
      id: 'bbq-long-test',
      cast: {
        grill: { picture: 'bbq-grill', role: 'hero' },
        raw: { picture: 'bbq-sausages', role: 'support' },
        tomato: { picture: 'sandwich-tomato', role: 'support' },
        lettuce: { picture: 'sandwich-lettuce', role: 'support' },
        burgers: { picture: 'bbq-burgers', role: 'result' },
        steak: { picture: 'repair-boat-hull-patch', role: 'support' },
      },
      steps: [
        { do: 'arrive', who: 'grill' },
        { do: 'flip', who: 'raw', onto: 'grill', speed: 'quick' },
        { do: 'land-on', who: 'tomato', onto: 'raw', speed: 'quick' },
        { do: 'land-on', who: 'lettuce', onto: 'raw', speed: 'quick' },
        { do: 'reveal', who: 'burgers', onto: 'raw', replace: true, speed: 'quick' },
        { do: 'flip', who: 'steak', onto: 'grill', replace: true, speed: 'quick' },
        { do: 'settle' },
      ],
    })!
    const c = compileStory(story, LIBRARY)
    expect(c.issues.filter((i) => i.level === 'error')).toEqual([])
    const burgerStep = c.windows[4]
    const at = (f: number, id: string) => c.full[f].items.find((i) => i.id === id)
    const rawPos = at(burgerStep.start - 1, 'raw')!
    const burgers = at(burgerStep.end - 1, 'burgers')!
    // The finished burgers sit where the raw ones were (on the grill), not in the middle of the bubble.
    expect(Math.abs(burgers.y - rawPos.y)).toBeLessThan(25)
    expect(at(burgerStep.end - 1, 'tomato')).toBeUndefined()
    // The steak then replaces the burgers on the grill, and the ending is just the grill and the steak.
    expect(objects(c.full[c.storyFrames - 1].items).map((i) => i.id).sort()).toEqual(['grill', 'steak'])
  })
})

describe('the bubble opens once and then stays', () => {
  const c = compileStory(STORY_DRAFTS.find((s) => s.id === 'garden-bbq')!, LIBRARY)

  it('opens from his head: the rings appear first, then the bubble swells to full size', () => {
    expect(c.intro.length).toBeGreaterThanOrEqual(6)
    expect(c.intro[0].bubble.opacity).toBe(0)
    expect(c.intro[0].bubble.rings![1]).toBeGreaterThan(0)
    expect(c.intro.at(-1)!.bubble).toEqual({ opacity: 1, scale: 1, rings: [1, 1] })
    for (const f of c.intro) expect(f.items).toEqual([])
  })

  it('keeps the bubble fully up through every story frame, so retellings never lose it', () => {
    for (const f of c.full) expect(f.bubble).toEqual({ opacity: 1, scale: 1 })
  })
})

describe('BBQ ephemera', () => {
  const c = compileStory(STORY_DRAFTS.find((s) => s.id === 'garden-bbq')!, LIBRARY)
  const props = c.full.flatMap((f) => f.items.filter((i) => i.id.startsWith('prop-')))

  it('circles inside the bubble all the way round, beneath everything, turning gently, never fading at the bottom', () => {
    expect(props.length).toBeGreaterThan(0)
    for (const p of props) {
      // Its centre plus its half-size stays within the (grown) rim: centre y −5, radii 162 × 100 in bubble-local terms.
      const half = (140 * p.scale) / 2
      expect(((Math.abs(p.x) + half * 0.6) / 162) ** 2 + ((Math.abs(p.y + 5) + half * 0.5) / 100) ** 2).toBeLessThan(1)
      expect(p.scale).toBeCloseTo(0.39, 2)
      expect(p.z).toBe(1)
    }
    // Fully visible at the bottom of the orbit too (only the start and end of the run fade).
    const bottom = props.filter((p) => p.y > 55)
    expect(bottom.length).toBeGreaterThan(0)
    expect(Math.max(...bottom.map((p) => p.opacity))).toBe(1)
    // They turn: the same prop changes angle from frame to frame, slowly.
    const one = c.full.map((f) => f.items.find((i) => i.id === 'prop-0')).filter(Boolean)
    const step = Math.abs(one[10]!.rotation - one[9]!.rotation)
    expect(step).toBeGreaterThan(0.5)
    expect(step).toBeLessThan(10)
  })

  it('persists when the story retells: fully up through the quiet moment and straight on into the retelling (Frank, 21 Oct)', () => {
    const ids = (f: number) => c.full[f].items.filter((i) => i.id.startsWith('prop-'))
    // Every frame of the retold part shows all six, fully visible: nothing blinks out at the restart.
    for (let f = c.loopStart; f < c.full.length; f++) {
      expect(ids(f), `frame ${f}`).toHaveLength(6)
      for (const p of ids(f)) expect(p.opacity, `${p.id} at frame ${f}`).toBe(1)
    }
    // The jump from the last frame back to the retelling step is one ordinary step along the orbit.
    const pos = (f: number, id: string) => c.full[f].items.find((i) => i.id === id)!
    const stride = (a: FrameItem, b: FrameItem) => Math.hypot(a.x - b.x, a.y - b.y)
    for (const p of ids(c.loopStart)) {
      const normal = stride(pos(c.loopStart, p.id), pos(c.loopStart + 1, p.id))
      const jump = stride(pos(c.full.length - 1, p.id), pos(c.loopStart, p.id))
      expect(jump).toBeLessThan(normal * 1.6 + 0.5)
    }
    // On the very first telling they fade in just before they are needed, not with a pop.
    const first = c.full.findIndex((f) => f.items.some((i) => i.id.startsWith('prop-')))
    expect(ids(first)[0].opacity).toBeLessThan(1)
  })
})

describe('the bubble outline', () => {
  it('is a loose, slowly drifting shape around the bubble oval, growing from the bottom for the opening', async () => {
    const { bubbleOutline } = await import('./compile')
    const pts = (d: string) => [...d.matchAll(/[ML](-?[\d.]+) (-?[\d.]+)/g)].map((m) => [Number(m[1]), Number(m[2])])
    const a = pts(bubbleOutline(0)), b = pts(bubbleOutline(40))
    expect(a).toHaveLength(72)
    const radii = a.map(([x, y]) => Math.hypot((x - 180) / 162, (y - 110) / 100))
    // The loose edge stays inside the 360 × 230 drawing box, so nothing is clipped.
    for (const [x, y] of a) expect(x >= 0 && x <= 360 && y >= 0 && y <= 230).toBe(true)
    expect(Math.min(...radii)).toBeGreaterThan(0.92)
    expect(Math.max(...radii)).toBeLessThan(1.08)
    expect(Math.max(...radii) - Math.min(...radii)).toBeGreaterThan(0.04)
    expect(a).not.toEqual(b)
    const small = pts(bubbleOutline(0, 0.3))
    expect(Math.max(...small.map(([, y]) => y))).toBeGreaterThan(200)
  })
})

describe('the picture library in the studio', () => {
  it('puts every picture in exactly one named group, so none is hidden under Other', () => {
    const groups = groupPictures(LIBRARY)
    expect(groups.map((g) => g.label)).not.toContain(OTHER_GROUP)
    expect(groups.flatMap((g) => g.pictures.map(([id]) => id)).sort()).toEqual(Object.keys(LIBRARY.pictures).sort())
  })

  it('offers only objects in object menus', () => {
    for (const g of groupPictures(LIBRARY, 'object')) for (const [, p] of g.pictures) expect(p.kind).toBe('object')
  })

  it('says how often a story plays in plain words', () => {
    expect(playsText([1, 1])).toBe('plays once')
    expect(playsText([2, 2])).toBe('plays twice')
    expect(playsText([1, 2])).toBe('plays once or twice')
    expect(playsText([2, 4])).toBe('plays 2–4 times')
    expect(playsText([0, 1])).toBe('plays once at most')
    expect(playsText([0, 0])).toBe('is longer than the activity')
  })
})

describe('dropping a picture from the library onto a story', () => {
  const bbq = STORY_DRAFTS.find((s) => s.id === 'garden-bbq')!

  it('adds an object to the cast as a helper, or swaps the picture of the member it lands on', () => {
    const added = placePicture(bbq, LIBRARY, 'consumable-cellulose-sponge', { to: 'cast' })!
    expect(added.cast.sponge).toEqual({ picture: 'consumable-cellulose-sponge', role: 'support' })
    const again = placePicture(added, LIBRARY, 'washing-sponge', { to: 'cast' })!
    expect(again.cast['sponge-2'].picture).toBe('washing-sponge')
    const swapped = placePicture(bbq, LIBRARY, 'bbq-hotdogs', { to: 'cast', as: 'sausages' })!
    expect(swapped.cast.sausages).toEqual({ picture: 'bbq-hotdogs', role: bbq.cast.sausages.role })
    expect(placePicture(bbq, LIBRARY, 'symbol-impact-star', { to: 'cast' })).toBeNull()
  })

  it('makes an object the actor of a step (joining the cast if needed) and a mark its touch mark', () => {
    const i = bbq.steps.findIndex((s) => s.do === 'land-on')
    const acted = placePicture(bbq, LIBRARY, 'condiment-honey-pot', { to: 'step', index: i })!
    expect(acted.steps[i].who).toBe('honey')
    expect(acted.cast.honey.picture).toBe('condiment-honey-pot')
    const reused = placePicture(bbq, LIBRARY, bbq.cast.charcoal.picture, { to: 'step', index: i })!
    expect(reused.steps[i].who).toBe('charcoal')
    expect(Object.keys(reused.cast)).toEqual(Object.keys(bbq.cast))
    expect(placePicture(bbq, LIBRARY, 'symbol-soap-bubbles', { to: 'step', index: i })!.steps[i].mark).toBe('symbol-soap-bubbles')
    // A quiet moment has no actor and no touches.
    expect(canPlace(bbq, 'object', { to: 'step', index: bbq.steps.length - 1 })).toBe(false)
  })

  it('adds a circling prop for the retold part of the story, and a mark riding on the main picture', () => {
    const withProp = placePicture(bbq, LIBRARY, 'bbq-heatproof-mitt', { to: 'props' })!
    expect(withProp.props.at(-1)).toEqual({ picture: 'bbq-heatproof-mitt', at: 'orbit', fromStep: bbq.loopFrom ?? 1, toStep: bbq.steps.length - 1 })
    expect(compileStory(withProp, LIBRARY).issues.filter((x) => x.level === 'error')).toEqual([])
    const withMark = placePicture(bbq, LIBRARY, 'symbol-heat-shimmer', { to: 'marks' })!
    const hero = Object.entries(bbq.cast).find(([, m]) => m.role === 'hero')![0]
    expect(withMark.ambient.at(-1)).toMatchObject({ picture: 'symbol-heat-shimmer', on: hero })
    expect(placePicture(bbq, LIBRARY, 'tool-broom', { to: 'marks' })).toBeNull()
  })
})

describe('the ligne-claire style review', () => {
  it('names only pictures that exist, and goes stale when Codex adds a newer version', () => {
    for (const id of Object.keys(STYLE_REVIEW.pictures)) expect(LIBRARY.pictures[id], id).toBeDefined()
    const id = Object.keys(STYLE_REVIEW.pictures)[0]
    expect(styleOf(STYLE_REVIEW, LIBRARY, id)).toBeDefined()
    const lib = structuredClone(LIBRARY) as Library
    lib.pictures[id].current = 99
    expect(styleOf(STYLE_REVIEW, lib, id)).toBeUndefined()
  })
})

/** One demo story per working action (data/activity-stories/demos): the target arrives, the tool does its job slowly, a pause. */
const DEMO_DIR = path.resolve(__dirname, '../../data/activity-stories/demos')
const demo = (name: string) => cleanStory(JSON.parse(fs.readFileSync(path.join(DEMO_DIR, `${name}.json`), 'utf8')))!

describe('the ten working actions (Frank’s a1 answer, 21 Oct)', () => {
  const VERBS10 = ['saw', 'chop', 'stir', 'shake', 'spray', 'wipe', 'sweep', 'dig', 'brush', 'iron'] as const
  /** The tool's frames while it works: after it pops up (2) and swings in (6, slow), for 12 frames. */
  const working = (name: string) => {
    const c = compileStory(demo(name), LIBRARY)
    const w = c.windows[1]
    const frames = c.full.slice(w.start + 8, w.start + 20)
    return {
      c,
      tool: frames.map((f) => f.items.find((i) => i.id === 'tool')!),
      target: frames.map((f) => f.items.find((i) => i.id === 'target')!),
      marks: c.full.slice(w.start, w.end).flatMap((f) => f.items.filter((i) => i.kind === 'mark' && !i.id.startsWith('trail-'))),
    }
  }
  const turns = (v: number[]) => v.slice(2).filter((x, i) => Math.sign(x - v[i + 1]) !== 0 && Math.sign(v[i + 1] - v[i]) !== 0 && Math.sign(x - v[i + 1]) !== Math.sign(v[i + 1] - v[i])).length
  const range = (v: number[]) => Math.max(...v) - Math.min(...v)

  for (const verb of VERBS10)
    it(`${verb}: plays cleanly, touches where it says, then leaves`, () => {
      const { c, tool } = working(verb)
      expect(c.issues.filter((i) => i.level === 'error'), verb).toEqual([])
      expect(tool.every(Boolean), `${verb} on show while it works`).toBe(true)
      for (const t of c.contacts) expect(t.gap, `${verb} at frame ${t.frame}`).toBeLessThanOrEqual(4)
      expect(c.full[c.windows[2].start].items.some((i) => i.id === 'tool')).toBe(false)
      // No motion trails while it works in place: they would bury the action.
      const w = c.windows[1]
      for (const f of c.full.slice(w.start + 8, w.start + 20)) expect(f.items.some((i) => i.id === 'trail-tool'), verb).toBe(false)
    })

  it('saw: back and forth across the top, sinking a little, sawdust falling', () => {
    const { tool, target, marks } = working('saw')
    expect(turns(tool.map((t) => t.x))).toBeGreaterThanOrEqual(4)
    expect(tool.at(-1)!.y).toBeGreaterThan(tool[0].y)
    expect(range(tool.map((t) => t.y))).toBeLessThan(8)
    expect(tool.every((t, i) => t.y < target[i].y)).toBe(true)
    expect(marks.filter((m) => m.id.startsWith('drift-')).length).toBeGreaterThanOrEqual(3)
  })

  it('chop: quick downward strokes, stepping along', () => {
    const { tool, marks } = working('chop')
    expect(turns(tool.map((t) => t.y))).toBeGreaterThanOrEqual(4)
    expect(Math.abs(tool.at(-1)!.x - tool[0].x)).toBeGreaterThan(10)
    expect(new Set(marks.filter((m) => m.id.startsWith('contact-')).map((m) => m.id)).size).toBeGreaterThanOrEqual(4)
  })

  it('stir: round and round, behind the rim of what it stirs', () => {
    const { tool, target } = working('stir')
    expect(tool.every((t, i) => t.z < target[i].z)).toBe(true)
    expect(turns(tool.map((t) => t.x))).toBeGreaterThanOrEqual(2)
    expect(turns(tool.map((t) => t.y))).toBeGreaterThanOrEqual(2)
  })

  it('shake: turned over above it, shaken, bits falling onto it', () => {
    const { tool, target, marks } = working('shake')
    expect(tool.every((t) => Math.abs(t.rotation) > 150)).toBe(true)
    expect(tool.every((t, i) => t.y < target[i].y)).toBe(true)
    expect(turns(tool.map((t) => t.y))).toBeGreaterThanOrEqual(4)
    const bits = marks.filter((m) => m.id.startsWith('drift-'))
    expect(bits.length).toBeGreaterThanOrEqual(4)
  })

  it('spray: stands clear beside it and puffs a mist across', () => {
    const { tool, target, marks, c } = working('spray')
    expect(tool.every((t, i) => Math.abs(t.x - target[i].x) > 40)).toBe(true)
    expect(c.contacts.filter((t) => t.step === 2)).toEqual([])
    const puffs = new Set(marks.filter((m) => m.id.startsWith('drift-')).map((m) => m.id))
    expect(puffs.size).toBeGreaterThanOrEqual(3)
  })

  it('wipe: small circles over it, a gleam after each', () => {
    const { tool, target, marks } = working('wipe')
    expect(range(tool.map((t) => t.y))).toBeLessThanOrEqual(12)
    expect(turns(tool.map((t) => t.x))).toBeGreaterThanOrEqual(2)
    expect(tool.every((t, i) => Math.abs(t.y - target[i].y) < 30)).toBe(true)
    expect(new Set(marks.filter((m) => m.picture === 'symbol-clean-glint').map((m) => m.id)).size).toBeGreaterThanOrEqual(3)
  })

  it('sweep: wide swings along its bottom edge', () => {
    const { tool, target } = working('sweep')
    expect(tool.every((t, i) => t.y > target[i].y)).toBe(true)
    expect(range(tool.map((t) => t.x))).toBeGreaterThan(range(working('wipe').tool.map((t) => t.x)))
    expect(turns(tool.map((t) => t.x))).toBeGreaterThanOrEqual(1)
  })

  it('dig: down into it, then flicked up and out', () => {
    const { tool, target, marks } = working('dig')
    expect(new Set(tool.map((t) => t.rotation)).size).toBeGreaterThanOrEqual(3)
    expect(Math.max(...tool.map((t) => t.y))).toBeGreaterThan(Math.min(...tool.map((t) => t.y)) + 20)
    expect(tool.some((t, i) => Math.abs(t.x - target[i].x) < 2)).toBe(true)
    expect(marks.some((m) => m.id.startsWith('drift-'))).toBe(true)
  })

  it('brush: long strokes the same way, each a little lower', () => {
    const { tool } = working('brush')
    const strokes = [0, 4, 8].map((k) => tool.slice(k, k + 4))
    for (const st of strokes) expect(Math.sign(st[3].x - st[1].x)).toBe(Math.sign(strokes[0][3].x - strokes[0][1].x))
    expect(Math.abs(strokes[0][3].x - strokes[0][1].x)).toBeGreaterThan(20)
    expect(strokes[2][2].y).toBeGreaterThan(strokes[0][2].y)
  })

  it('iron: glides flat across and back, steam rising', () => {
    const { tool, marks } = working('iron')
    expect(tool.every((t) => t.rotation === 0)).toBe(true)
    expect(range(tool.map((t) => t.y))).toBe(0)
    expect(range(tool.map((t) => t.x))).toBeGreaterThan(25)
    const steam = marks.filter((m) => m.id.startsWith('drift-'))
    expect(steam.length).toBeGreaterThanOrEqual(3)
  })

  it('each action moves differently from every other', () => {
    const sig = (v: string) => working(v).tool.map((t) => `${Math.round(t.x)},${Math.round(t.y)},${Math.round(t.rotation)}`).join(' ')
    expect(new Set(VERBS10.map(sig)).size).toBe(VERBS10.length)
  })
})

describe('a mark as a picture appears (Frank’s a2 answer, 21 Oct)', () => {
  const story = demo('appear')
  const c = compileStory(story, LIBRARY)
  const bursts = (id: string) => c.full.map((f, k) => [k, f.items.find((i) => i.id.startsWith(`appear-${id}`))] as const).filter(([, i]) => i)

  it('bursts once, for about a second, as the picture appears, then is gone', () => {
    expect(c.issues.filter((i) => i.level === 'error')).toEqual([])
    for (const id of ['hotdogs', 'plate']) {
      const seen = bursts(id)
      const first = c.full.findIndex((f) => f.items.some((i) => i.id === id))
      expect(seen[0][0], id).toBe(first)
      expect(seen.length, id).toBeGreaterThanOrEqual(6)
      expect(seen.length, id).toBeLessThanOrEqual(8)
      expect(seen.at(-1)![0] - seen[0][0], id).toBe(seen.length - 1)
      // It sits above the picture it belongs to.
      const [k, mark] = seen[2]
      expect(mark!.y).toBeLessThan(c.full[k].items.find((i) => i.id === id)!.y)
    }
    expect(bursts('grill')).toEqual([])
  })

  it('never runs into the quiet moment, and reduced motion shows it still', () => {
    for (const f of c.full.slice(c.quiet[0])) expect(f.items.filter((i) => i.kind === 'mark')).toEqual([])
    const r = c.reduced.filter((f) => f.items.some((i) => i.id.startsWith('appear-')))
    expect(r.length).toBeGreaterThan(0)
    for (const f of c.reduced) expect(f.items.filter((i) => i.kind === 'mark').length).toBeLessThanOrEqual(1)
  })

  it('is dropped from the library onto a cast member’s slot, and kept when its picture is swapped', () => {
    const bbq = STORY_DRAFTS.find((s) => s.id === 'garden-bbq')!
    expect(canPlace(bbq, 'mark', { to: 'appear', as: 'hotdogs' })).toBe(true)
    expect(canPlace(bbq, 'object', { to: 'appear', as: 'hotdogs' })).toBe(false)
    expect(canPlace(bbq, 'mark', { to: 'appear', as: 'nobody' })).toBe(false)
    const withMark = placePicture(bbq, LIBRARY, 'symbol-pleasant-aroma', { to: 'appear', as: 'hotdogs' })!
    expect(withMark.cast.hotdogs.appear).toBe('symbol-pleasant-aroma')
    const swapped = placePicture(withMark, LIBRARY, 'bbq-burgers', { to: 'cast', as: 'hotdogs' })!
    expect(swapped.cast.hotdogs).toEqual({ picture: 'bbq-burgers', role: bbq.cast.hotdogs.role, appear: 'symbol-pleasant-aroma' })
    expect(swapPicture({ picture: 'a', role: 'hero', version: 2 }, 'b')).toEqual({ picture: 'b', role: 'hero' })
    // It survives a save and reload, and a non-mark is reported.
    expect(cleanStory(JSON.parse(JSON.stringify(withMark)))!.cast.hotdogs.appear).toBe('symbol-pleasant-aroma')
    const wrong: Story = { ...bbq, cast: { ...bbq.cast, hotdogs: { ...bbq.cast.hotdogs, appear: 'tool-broom' } } }
    expect(compileStory(wrong, LIBRARY).issues.some((i) => i.level === 'error' && i.text.includes('tool-broom'))).toBe(true)
  })
})
