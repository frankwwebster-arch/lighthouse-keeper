import fs from 'node:fs'
import path from 'node:path'
import { describe, expect, it } from 'vitest'
import { compileStory, type FrameItem } from './compile'
import { STORY_DRAFTS, STORY_FILES, LIBRARY } from './drafts'
import { cleanStory, groupPictures, OTHER_GROUP, playsText, type Library } from './format'

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

      it('reduced motion ends on pictures from the full-motion ending', () => {
        const end = (frames: typeof c.full) => objects(frames[c.storyFrames - 1].items).map((i) => i.id)
        const full = end(c.full)
        for (const id of end(c.reduced)) expect(full).toContain(id)
        expect(end(c.reduced).length).toBeGreaterThan(0)
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
    grill.versions.push({ ...grill.versions[0], v: 2, url: '/activity-stories/pictures/bbq-grill-v2.png' })
    grill.current = 2
    const story = STORY_DRAFTS.find((s) => s.id === 'garden-bbq')!
    const urlOf = (s: typeof story) => compileStory(s, lib).full.flatMap((f) => f.items).find((i) => i.id === 'grill')?.url
    expect(urlOf(story)).toBe('/activity-stories/pictures/bbq-grill-v2.png')
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
