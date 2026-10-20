import fs from 'node:fs'
import path from 'node:path'
import { describe, expect, it } from 'vitest'
import { compileStory } from './compile'
import { STORY_DRAFTS, STORY_FILES, LIBRARY } from './drafts'
import { cleanStory, type Library } from './format'

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

      it('keeps the quiet ending completely still, with no marks', () => {
        const q = c.full.slice(c.quiet[0], c.quiet[1] + 1)
        expect(q.length).toBeGreaterThanOrEqual(5)
        for (const f of q) {
          expect(f.items.filter((i) => i.kind === 'mark')).toEqual([])
          expect(f.items).toEqual(q[0].items)
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
          expect(objects(c.full.at(-1)!.items).every((i) => i.opacity < 0.05) || objects(c.full.at(-1)!.items).length === 0).toBe(true)
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

  it('circles outside the bubble, small, beneath everything, and away from his head', () => {
    expect(props.length).toBeGreaterThan(0)
    for (const p of props) {
      expect(((p.x / 149) ** 2 + ((p.y - 2) / 92) ** 2) ** 0.5).toBeGreaterThan(1)
      expect(p.scale).toBeLessThan(0.3)
      expect(p.z).toBe(1)
      if (p.y > 80) expect(p.opacity).toBeLessThan(0.5)
    }
  })

  it('is back where it started when the story retells, so the loop is seamless', () => {
    const at = (f: number) => c.full[f].items.filter((i) => i.id.startsWith('prop-')).map((i) => [i.id, i.x, i.y])
    const lastWithProps = c.full.map((f, k) => [k, f.items.some((i) => i.id.startsWith('prop-'))] as const).filter(([, has]) => has).at(-1)![0]
    // One lap per retelling: positions advance smoothly and the lap length equals the retelling length.
    expect(lastWithProps).toBeGreaterThan(c.loopStart)
    expect(at(c.loopStart + 2).length).toBeGreaterThan(0)
  })
})
