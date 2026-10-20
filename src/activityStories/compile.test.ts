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

      it('plays at least twice in a 30-second activity', () => {
        expect(c.tellings[1]).toBeGreaterThanOrEqual(2)
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
          const lowest = Math.min(...objects(f.items).map((i) => i.z))
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

      it('loops by clearing after the quiet moment', () => {
        expect(c.full.length).toBe(c.storyFrames + 3)
        expect(objects(c.full.at(-1)!.items).every((i) => i.opacity < 0.05) || objects(c.full.at(-1)!.items).length === 0).toBe(true)
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

describe('replacing what is on top', () => {
  it('Garden BBQ: the raw sausages sink into the grill as the hot dogs land, and never sit under them', () => {
    const story = STORY_DRAFTS.find((s) => s.id === 'garden-bbq')!
    const c = compileStory(story, LIBRARY)
    const hotdogStep = c.windows[story.steps.findIndex((s) => s.who === 'hotdogs')]
    const landed = c.contacts.find((t) => t.actor === 'hotdogs')!.frame
    const grillAt = (f: number) => c.full[f].items.find((i) => i.id === 'grill')!
    // Sausages are on show until the hot dogs touch down, then shrink towards the grill and are gone within three frames.
    expect(c.full[landed - 1].items.some((i) => i.id === 'sausages' && i.opacity === 1)).toBe(true)
    const sinking = c.full[landed + 1].items.find((i) => i.id === 'sausages')
    if (sinking) expect(Math.abs(sinking.y - grillAt(landed + 1).y)).toBeLessThan(Math.abs(c.full[landed - 1].items.find((i) => i.id === 'sausages')!.y - grillAt(landed - 1).y))
    for (let f = landed + 3; f < c.storyFrames; f++) expect(c.full[f].items.some((i) => i.id === 'sausages')).toBe(false)
    expect(hotdogStep.end).toBeLessThanOrEqual(c.quiet[0])
    // The ending is the plated meal alone.
    expect(objects(c.full[c.storyFrames - 1].items).map((i) => i.id).sort()).toEqual(['meal'])
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
