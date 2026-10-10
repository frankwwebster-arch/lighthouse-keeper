import { readFileSync, readdirSync } from 'node:fs'
import { describe, expect, it } from 'vitest'
import { DRAFTS, DRAFT_FILES } from './drafts'
import { checkSolids, cleanRecipe, compile, frameFrom, hashOf, mainOf, moveStep, newCue, placeX, shotAt, soundsUsed, walkFor, type BoundsLookup, type ClipInfo, type ClipLookup, type Recipe } from './recipe'

const manifest = JSON.parse(readFileSync('public/sprites/manifest.json', 'utf8')) as Record<string, { w: number; h: number; frames: number; fps?: number; anchor?: [number, number]; facing?: string; mirrorSafe?: boolean }>
const fromManifest: ClipLookup = (name) => {
  const e = manifest[name]
  if (!e) return undefined
  return { w: e.w, h: e.h, frames: e.frames, fps: e.fps ?? 4, anchor: e.anchor ?? [e.w / 2, e.h], native: e.facing?.includes('left') ? 'left' : e.facing?.includes('right') ? 'right' : null, mirrorSafe: !!e.mirrorSafe }
}
const macros = Object.fromEntries(DRAFTS.filter((d) => d.kind === 'macro').map((d) => [d.id, d]))
const recipes = DRAFTS.filter((d) => d.kind === 'recipe')

// A tiny made-up world for exact sums.
const clip = (frames: number, fps: number, native: ClipInfo['native'] = 'right'): ClipInfo => ({ w: 32, h: 40, frames, fps, anchor: [16, 40], native, mirrorSafe: native !== null })
const tiny: ClipLookup = (n) => ({ keeper_walk: clip(8, 4), keeper_pyjamas_walk: clip(8, 4), sit: clip(6, 4), nap: clip(4, 2), back: clip(4, 4, null), door: clip(4, 4) })[n]
const base = (steps: Recipe['steps']): Recipe =>
  cleanRecipe({ id: 'test', title: 'Test', startAt: 'stairs', objects: [{ id: 'chair', label: 'Chair', x: 60, w: 20, h: 20 }], action: { object: 'chair', dx: 0, facing: 'left' }, walkSpeed: 20, steps })!

describe('the drafts', () => {
  it('lists every JSON file in data/studio', () => {
    const files = ['macros', 'recipes'].flatMap((dir) => readdirSync(`data/studio/${dir}`).filter((f) => f.endsWith('.json')).map((f) => `${dir}/${f.replace(/\.json$/, '')}`))
    expect(Object.keys(DRAFT_FILES).sort()).toEqual(files.sort())
  })

  it('are all valid, with unique ids', () => {
    expect(DRAFTS).toHaveLength(Object.keys(DRAFT_FILES).length)
    expect(new Set(DRAFTS.map((d) => d.id)).size).toBe(DRAFTS.length)
  })

  it('compile with no problems, and every clip they use is in the sprites', () => {
    for (const r of recipes) {
      const tl = compile(r, macros, fromManifest)
      expect(tl.problems, r.id).toEqual([])
      for (const s of tl.segments) if (s.clip) expect(manifest[s.clip], `${r.id}: ${s.clip}`).toBeTruthy()
      expect(mainOf(tl), r.id).toBeTruthy()
    }
  })

  it('never walk into anything solid or get covered by anything in front of him', () => {
    for (const r of recipes) expect(checkSolids(r, compile(r, macros, fromManifest)), r.id).toEqual([])
  })

  it('come in by the door and leave by it, ending at the stairs in standard clothes', () => {
    for (const r of recipes) {
      const tl = compile(r, macros, fromManifest)
      const hides = tl.segments.filter((s) => s.kind === 'hide')
      expect(hides.length, r.id).toBe(2)
      const end = shotAt(tl, tl.duration, r)
      expect(end.x, r.id).toBe(placeX(r, 'stairs'))
      expect(tl.segments[tl.segments.length - 1].outfit, r.id).toBe('standard')
    }
  })
})

describe('compiling a recipe', () => {
  it('walks at the set speed, faces the way it walks, and arrives facing the action', () => {
    const r = base([{ id: 'a', kind: 'walk', to: 'action' }])
    const tl = compile(r, {}, tiny)
    const walk = tl.segments[0]
    expect(walk.x0).toBe(placeX(r, 'stairs'))
    expect(walk.x1).toBe(60)
    expect(walk.end).toBeCloseTo((60 - placeX(r, 'stairs')) / 20)
    expect(walk.mirror).toBe(false) // walking right, drawn facing right
    const r2 = { ...r, steps: [...r.steps, { id: 'b', kind: 'play' as const, clip: 'sit' }] }
    expect(compile(r2, {}, tiny).segments[1].mirror).toBe(true) // arrived facing left (the action's facing)
  })

  it('never mirrors a clip with no direction (a rear view)', () => {
    const r = base([{ id: 'a', kind: 'walk', to: 'action' }, { id: 'b', kind: 'loop', clip: 'back', seconds: 1 }])
    expect(compile(r, {}, tiny).segments[1].mirror).toBe(false)
  })

  it('plays a one-shot for its own length and holds its last frame; reverse runs it backwards', () => {
    const r = base([{ id: 'a', kind: 'play', clip: 'sit' }, { id: 'b', kind: 'play', clip: 'sit', reverse: true }])
    const tl = compile(r, {}, tiny)
    expect(tl.segments[0].end).toBeCloseTo(6 / 4)
    expect(frameFrom(tl.segments[0], 0)).toBe(0)
    expect(frameFrom(tl.segments[0], 99)).toBe(5)
    expect(frameFrom(tl.segments[1], 0)).toBe(5)
    expect(frameFrom(tl.segments[1], 99)).toBe(0)
  })

  it('loops a loop, and the player can stop the main step early', () => {
    const r = base([{ id: 'a', kind: 'loop', clip: 'nap', seconds: 10, main: true }, { id: 'b', kind: 'play', clip: 'sit', reverse: true }])
    const tl = compile(r, {}, tiny)
    expect(frameFrom(tl.segments[0], 2.5)).toBe(1) // 4 frames at 2 fps: frame 5 wraps to 1
    const cut = compile(r, {}, tiny, { mainSeconds: 3 })
    expect(cut.segments[0].end).toBe(3)
    expect(cut.segments[1].start).toBe(3)
    expect(cut.duration).toBeCloseTo(3 + 6 / 4)
  })

  it('hides him in the doorway, swaps the outfit there, and opens or closes the door', () => {
    const enter: Recipe = cleanRecipe({ id: 'enter', kind: 'macro', steps: [{ id: 'w', kind: 'walk', to: 'doorOut' }, { id: 'o', kind: 'play', clip: 'door', doorAfter: 'open' }, { id: 'h', kind: 'hide', through: 'door', seconds: 0.5, swapTo: '$swapTo' }] })!
    const r = base([{ id: 'm', kind: 'macro', macro: 'enter', params: { swapTo: 'light-blue-pyjamas' } }, { id: 'g', kind: 'walk', to: 'action' }])
    const tl = compile(r, { enter }, tiny)
    const hide = tl.segments.find((s) => s.kind === 'hide')!
    expect(hide.visible).toBe(false)
    expect(hide.door).toBe(true)
    expect(hide.x0).toBeLessThan(0)
    expect(hide.x1).toBeGreaterThan(0)
    expect(hide.stepId).toBe('m') // macro steps belong to the recipe's macro step
    const walkIn = tl.segments[tl.segments.length - 1]
    expect(walkIn.outfit).toBe('light-blue-pyjamas')
    expect(walkIn.clip).toBe('keeper_pyjamas_walk')
    // Without the parameter he keeps his outfit.
    const plain = compile(base([{ id: 'm', kind: 'macro', macro: 'enter' }, { id: 'g', kind: 'walk', to: 'action' }]), { enter }, tiny)
    expect(plain.segments[plain.segments.length - 1].outfit).toBe('standard')
  })

  it('times cues from their step, and a looped cue runs to the step’s end', () => {
    const r = base([{ id: 'a', kind: 'play', clip: 'sit' }, { id: 'b', kind: 'loop', clip: 'nap', seconds: 4, cues: [{ ...newCue('snore', 0.5), loop: true }, newCue('yawn', 1)] }])
    const tl = compile(r, {}, tiny)
    const snore = tl.cues.find((c) => c.sound === 'snore')!
    expect(snore.time).toBeCloseTo(1.5 + 0.5)
    expect(snore.until).toBeCloseTo(1.5 + 4)
    expect(tl.cues.find((c) => c.sound === 'yawn')!.until).toBeNull()
  })

  it('says where each of the recipe’s own steps starts and ends', () => {
    const enter: Recipe = cleanRecipe({ id: 'enter', kind: 'macro', steps: [{ id: 'w', kind: 'walk', to: 'doorOut' }, { id: 'h', kind: 'hide', seconds: 0.5 }] })!
    const r = base([{ id: 'm', kind: 'macro', macro: 'enter' }, { id: 'p', kind: 'play', clip: 'sit' }])
    const tl = compile(r, { enter }, tiny)
    expect(tl.steps.map((s) => s.id)).toEqual(['m', 'p'])
    expect(tl.steps[0].start).toBe(0)
    expect(tl.steps[0].end).toBeCloseTo(tl.steps[1].start)
    expect(tl.steps[1].end).toBeCloseTo(tl.duration)
  })

  it('plays the sounds marked on a clip’s own sheet, every time that frame comes round', () => {
    const steps: ClipLookup = (n) => (n === 'walky' ? { ...clip(4, 4), sfxCues: [{ frame: 1, cue: 'footstep' }, { frame: 3, cue: 'footstep' }] } : tiny(n))
    const r = base([{ id: 'a', kind: 'walk', to: 40, clip: 'walky', speed: 40 / 3 + 0.0001 }])
    const walk = { ...r, startAt: 0 as const }
    const tl = compile(walk, {}, steps)
    // 3 s of a 1 s loop: footsteps at 0.25 and 0.75 each second
    expect(tl.cues.map((c) => Math.round(c.time * 100) / 100)).toEqual([0.25, 0.75, 1.25, 1.75, 2.25, 2.75])
    expect(tl.cues.every((c) => c.fromClip === 'walky')).toBe(true)
    const back = compile(base([{ id: 'p', kind: 'play', clip: 'walky', reverse: true }]), {}, steps)
    expect(back.cues.map((c) => c.time)).toEqual([0, 0.5]) // backwards, frame 3 shows first and frame 1 third
  })

  it('reports problems instead of failing', () => {
    const r = base([{ id: 'a', kind: 'macro', macro: 'nope' }, { id: 'b', kind: 'play', clip: 'missing_clip' }])
    expect(compile(r, {}, tiny).problems).toHaveLength(2)
  })

  it('keeps positions on whole pixels', () => {
    const r = base([{ id: 'a', kind: 'walk', to: 'action' }])
    const tl = compile(r, {}, tiny)
    for (let t = 0; t < tl.duration; t += 0.037) expect(Number.isInteger(shotAt(tl, t, r).x)).toBe(true)
  })
})

describe('solid things', () => {
  const room = (objects: unknown[], steps: Recipe['steps']) => cleanRecipe({ id: 'solid', startAt: 20, objects, action: { object: 'chair', dx: 0, facing: 'right' }, walkSpeed: 20, steps })!
  const chair = { id: 'chair', label: 'Armchair', x: 90, w: 20, h: 20, layer: 'back', solid: true }

  it('stops a walk through a solid object, but lets him reach the one he is using', () => {
    const box = { id: 'box', label: 'Toy box', x: 60, w: 16, h: 12, layer: 'back', solid: true }
    const r = room([box, chair], [{ id: 'a', kind: 'walk', to: 'action' }])
    const issues = checkSolids(r, compile(r, {}, tiny))
    expect(issues.map((i) => i.text)).toEqual(['walks into Toy box'])
    expect(checkSolids(room([chair], r.steps), compile(room([chair], r.steps), {}, tiny))).toEqual([])
  })

  it('lets him walk in front of things against the back wall', () => {
    const shelf = { id: 'shelf', label: 'Bookshelf', x: 60, w: 30, h: 40, layer: 'back' }
    const r = room([shelf, chair], [{ id: 'a', kind: 'walk', to: 'action' }])
    expect(checkSolids(r, compile(r, {}, tiny))).toEqual([])
  })

  it('never lets him walk through a wall: only a hidden doorway step crosses one', () => {
    const r = room([chair], [{ id: 'a', kind: 'walk', to: 'stairs' }])
    expect(checkSolids(r, compile(r, {}, tiny)).map((i) => i.text)).toContain('walks into the wall by the door')
    const ok = room([chair], [{ id: 'a', kind: 'walk', to: 'doorIn' }, { id: 'h', kind: 'hide', through: 'door' }, { id: 'b', kind: 'walk', to: 'stairs' }])
    expect(checkSolids(ok, compile(ok, {}, tiny))).toEqual([])
  })

  it('flags anything in front of him that would cover him, using the frame’s own pixels', () => {
    const plant = { id: 'plant', label: 'Tall plant', x: 50, w: 10, h: 30, layer: 'front' }
    const r = room([plant, chair], [{ id: 'a', kind: 'wait', clip: 'keeper_walk', seconds: 1 }])
    const at = (x: number) => ({ ...r, startAt: x })
    expect(checkSolids(at(40), compile(at(40), {}, tiny))).toHaveLength(1) // body 29–51 reaches the plant at 45
    expect(checkSolids(at(30), compile(at(30), {}, tiny))).toEqual([]) // body 19–41 is clear
    // A narrow frame (arms tucked in) can stand closer than the plain body width.
    const narrow: BoundsLookup = () => ({ left: -4, right: 4, bottom: 0, top: 38 })
    expect(checkSolids(at(40), compile(at(40), {}, tiny), narrow)).toEqual([])
    // Mirrored, a frame that reaches out to its right reaches to his left.
    const reach: BoundsLookup = () => ({ left: -4, right: 14, bottom: 0, top: 38 })
    const facingLeft = { ...at(62), facing: 'left' as const }
    expect(checkSolids(facingLeft, compile(facingLeft, {}, tiny), reach)).toHaveLength(1)
  })

  it('lets his hand touch the door while he opens or closes it', () => {
    const reach: BoundsLookup = () => ({ left: -11, right: 20, bottom: 0, top: 38 })
    const r = room([chair], [{ id: 'o', kind: 'play', clip: 'door', facing: 'right', doorAfter: 'open' }, { id: 'w', kind: 'wait', clip: 'door', facing: 'right', seconds: 0.5 }])
    const at = { ...r, startAt: 'doorOut' as const }
    const issues = checkSolids(at, compile(at, {}, tiny), reach)
    expect([...new Set(issues.map((i) => i.stepId))]).toEqual(['w']) // opening is fine; standing there reaching into it afterwards is not
  })

  it('treats the open door leaf as in front of him, so he stands clear of it', () => {
    const r = room([chair], [{ id: 'o', kind: 'wait', seconds: 0.5, doorAfter: 'open' }, { id: 'a', kind: 'wait', clip: 'keeper_walk', seconds: 0.5 }])
    const near = { ...r, startAt: 15 }
    expect(checkSolids(near, compile(near, {}, tiny)).map((i) => i.text.split(' (')[0])).toEqual(['the open door covers part of him'])
    const clear = { ...r, startAt: placeX(r, 'doorIn') }
    expect(checkSolids(clear, compile(clear, {}, tiny))).toEqual([])
  })
})

describe('editing helpers', () => {
  it('moves steps, lists sounds, and fingerprints drafts', () => {
    const r = base([{ id: 'a', kind: 'wait' }, { id: 'b', kind: 'wait', cues: [newCue('tick', 0)] }])
    expect(moveStep(r, 'b', -1).steps.map((s) => s.id)).toEqual(['b', 'a'])
    expect(moveStep(r, 'a', -1)).toBe(r)
    expect(soundsUsed([r])).toEqual(['tick'])
    expect(hashOf(r)).toBe(hashOf(JSON.parse(JSON.stringify(r))))
    expect(hashOf(r)).not.toBe(hashOf(moveStep(r, 'b', -1)))
  })

  it('finds each outfit’s walk', () => {
    const has = (n: string) => !!manifest[n]
    expect(walkFor('standard', has)).toBe('keeper_walk')
    expect(walkFor('light-blue-pyjamas', has)).toBe('keeper_pyjamas_walk')
    expect(walkFor('knight', has)).toBe('keeper_knight_walk_side')
    expect(walkFor('no-such-outfit', has)).toBe('keeper_walk')
  })

  it('refuses junk and fills gaps when reading a saved recipe', () => {
    expect(cleanRecipe(null)).toBeNull()
    expect(cleanRecipe({ id: 'Bad Id!' })).toBeNull()
    const r = cleanRecipe({ id: 'ok' })!
    expect(r.steps).toEqual([])
    expect(r.walkSpeed).toBe(20)
    expect(r.status).toBe('draft')
  })
})
