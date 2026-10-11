import { readFileSync, readdirSync } from 'node:fs'
import { describe, expect, it } from 'vitest'
import { CATEGORIES, CATEGORY_FILES, DRAFTS, DRAFT_FILES } from './drafts'
import { DOOR, DOOR_CLEAR, KEEPER_HALF, bridgesFor, checkSolids, flipPose, isOrdinaryPose, joinsOf, cleanCategory, cleanRecipe, compile, everyVariant, resolveRecipe, frameFrom, hashOf, mainOf, moveStep, newCue, placeX, shotAt, soundsUsed, walkFor, type BoundsLookup, type ClipInfo, type ClipLookup, type Recipe, type StageObject } from './recipe'

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
    const cats = readdirSync('data/studio/categories').filter((f) => f.endsWith('.json')).map((f) => `categories/${f.replace(/\.json$/, '')}`)
    expect(Object.keys(CATEGORY_FILES).sort()).toEqual(cats.sort())
    expect(Object.keys(CATEGORIES)).toHaveLength(cats.length)
    const files = ['macros', 'recipes'].flatMap((dir) => readdirSync(`data/studio/${dir}`).filter((f) => f.endsWith('.json')).map((f) => `${dir}/${f.replace(/\.json$/, '')}`))
    expect(Object.keys(DRAFT_FILES).sort()).toEqual(files.sort())
  })

  it('are all valid, with unique ids', () => {
    expect(DRAFTS).toHaveLength(Object.keys(DRAFT_FILES).length)
    expect(new Set(DRAFTS.map((d) => d.id)).size).toBe(DRAFTS.length)
  })

  it('compile with no problems, and every clip they use is in the sprites', () => {
    for (const raw of recipes) {
      const { recipe: r, problems } = resolveRecipe(raw, CATEGORIES)
      expect(problems, raw.id).toEqual([])
      const tl = compile(r, macros, fromManifest)
      expect(tl.problems, r.id).toEqual([])
      for (const s of tl.segments) if (s.clip) expect(manifest[s.clip], `${r.id}: ${s.clip}`).toBeTruthy()
      expect(mainOf(tl), r.id).toBeTruthy()
    }
  })

  it('never walk into anything solid or get covered by anything in front of him, with every variant of every object', () => {
    for (const raw of recipes) {
      for (const { variant, recipe } of [{ variant: { id: 'as drafted' }, recipe: raw }, ...everyVariant(raw, CATEGORIES)]) {
        const r = resolveRecipe(recipe, CATEGORIES).recipe
        expect(checkSolids(r, compile(r, macros, fromManifest)), `${raw.id} with ${variant.id}`).toEqual([])
      }
    }
  })

  it('come in by the door and leave by it, ending at the stairs in standard clothes', () => {
    for (const raw of recipes) {
      const r = resolveRecipe(raw, CATEGORIES).recipe
      const tl = compile(r, macros, fromManifest)
      const doorways = new Set(tl.segments.filter((s) => s.kind === 'hide').map((s) => `${s.stepId}/${s.innerId}`))
      expect(doorways.size, r.id).toBe(2)
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
    // Whole strides: the nearest whole number of 2 s rounds (8 frames at 4 fps) to the distance at 20 px/s.
    expect(walk.end).toBeCloseTo(Math.max(1, Math.round((60 - placeX(r, 'stairs')) / 20 / 2)) * 2)
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
    // 4 frames at 2 fps is a 2 s round: stopped at 3 s, he finishes the round he is in.
    const cut = compile(r, {}, tiny, { mainSeconds: 3 })
    expect(cut.segments[0].end).toBe(4)
    expect(cut.segments[1].start).toBe(4)
    expect(cut.duration).toBeCloseTo(4 + 6 / 4)
    expect(compile(r, {}, tiny, { mainSeconds: 0.1 }).segments[0].end).toBe(2)
  })

  it('walks him straight through the doorway, changing his outfit behind the open door', () => {
    const enter: Recipe = cleanRecipe({ id: 'enter', kind: 'macro', steps: [{ id: 'w', kind: 'walk', to: 'doorOut' }, { id: 'o', kind: 'play', clip: 'door', doorAfter: 'open' }, { id: 'h', kind: 'hide', through: 'door', swapTo: '$swapTo' }] })!
    const r = base([{ id: 'm', kind: 'macro', macro: 'enter', params: { swapTo: 'light-blue-pyjamas' } }, { id: 'g', kind: 'walk', to: 'action' }])
    const tl = compile(r, { enter }, tiny)
    const [before, after] = tl.segments.filter((s) => s.kind === 'hide')
    expect(before.visible).toBe(true) // seen walking up to and behind the door, never popping in
    expect(before.covered).toBe(true)
    expect(before.door).toBe(true)
    expect(before.x0).toBeLessThan(0)
    expect(before.x1).toBe(DOOR.leaf / 2) // the costume changes where the open door covers all of him
    expect(after.changes).toBe('light-blue-pyjamas')
    expect(after.clip).toBe('keeper_pyjamas_walk')
    expect(after.start).toBeCloseTo(before.end)
    expect(after.x1).toBe(placeX(r, 'doorIn'))
    expect(after.stepId).toBe('m') // macro steps belong to the recipe's macro step
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
    const shelf = { id: 'shelf', label: 'Bookshelf', x: 70, w: 30, h: 40, layer: 'back' }
    const r = room([shelf, chair], [{ id: 'a', kind: 'walk', to: 'action' }])
    expect(checkSolids(r, compile(r, {}, tiny))).toEqual([])
  })

  it('never lets him walk through a wall: only a hidden doorway step crosses one', () => {
    const r = room([chair], [{ id: 'a', kind: 'walk', to: 'stairs' }])
    expect(checkSolids(r, compile(r, {}, tiny)).map((i) => i.text)).toContain('walks into the wall by the door')
    const ok = room([chair], [{ id: 'a', kind: 'walk', to: 'doorIn' }, { id: 'o', kind: 'wait', seconds: 0.5, doorAfter: 'open' }, { id: 'h', kind: 'hide', through: 'door' }, { id: 'b', kind: 'walk', to: 'stairs' }])
    expect(compile(ok, {}, tiny).problems).toEqual([])
    expect(checkSolids(ok, compile(ok, {}, tiny))).toEqual([])
    // Through a closed door is a problem.
    const shut = room([chair], [{ id: 'a', kind: 'walk', to: 'doorIn' }, { id: 'h', kind: 'hide', through: 'door' }])
    expect(compile(shut, {}, tiny).problems[0]).toMatch(/closed door/)
  })

  it('flags anything in front of him that would cover him, using the frame’s own pixels', () => {
    const plant = { id: 'plant', label: 'Tall plant', x: 60, w: 10, h: 30, layer: 'front' }
    const r = room([plant, chair], [{ id: 'a', kind: 'wait', clip: 'keeper_walk', seconds: 1 }])
    const at = (x: number) => ({ ...r, startAt: x })
    expect(checkSolids(at(50), compile(at(50), {}, tiny))).toHaveLength(1) // body 39–61 reaches the plant at 55
    expect(checkSolids(at(40), compile(at(40), {}, tiny))).toEqual([]) // body 29–51 is clear
    // A narrow frame (arms tucked in) can stand closer than the plain body width.
    const narrow: BoundsLookup = () => ({ left: -4, right: 4, bottom: 0, top: 38 })
    expect(checkSolids(at(50), compile(at(50), {}, tiny), narrow)).toEqual([])
    // Mirrored, a frame that reaches out to its right reaches to his left.
    const reach: BoundsLookup = () => ({ left: -4, right: 14, bottom: 0, top: 38 })
    const facingLeft = { ...at(72), facing: 'left' as const }
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

describe('whole strides and clean joins', () => {
  it('finishes every walk on a whole stride, landing on the standing frame', () => {
    const closed: ClipLookup = (n) => (n === 'keeper_walk' ? { ...clip(9, 8), closed: true, startPose: 'standing-side-right', endPose: 'standing-side-right' } : tiny(n))
    const r = { ...base([{ id: 'a', kind: 'walk', to: 70 }, { id: 'b', kind: 'play', clip: 'sit' }]), startAt: 10 as const }
    const tl = compile(r, {}, closed)
    const walk = tl.segments[0]
    expect(((walk.end - walk.start) * 8) % 8).toBeCloseTo(0) // whole rounds of 8 frames
    expect(frameFrom(walk, walk.end - walk.start + 1e-6)).toBe(0) // the next frame would be the standing frame
    expect(shotAt(tl, walk.end - 1e-6, r).x).toBe(70) // and he is on his spot
    // A closed cycle never shows its repeated last frame mid-walk.
    for (let s = 0; s < walk.end; s += 0.125) expect(frameFrom(walk, s)).toBeLessThan(8)
  })

  it('lists each handover with the poses either side, and suggests bridges', () => {
    const posed: ClipLookup = (n) => ({ keeper_walk: { ...clip(9, 8), closed: true, startPose: 'standing-side-right', endPose: 'standing-side-right' }, back: { ...clip(4, 4, null), startPose: 'standing-back', endPose: 'standing-back' }, turn: { ...clip(6, 8), startPose: 'standing-side-right', endPose: 'standing-back' } } as Record<string, ClipInfo>)[n]
    const r = { ...base([{ id: 'a', kind: 'walk', to: 70 }, { id: 'b', kind: 'loop', clip: 'back', seconds: 1 }]), startAt: 10 as const }
    const joins = joinsOf(compile(r, {}, posed))
    expect(joins).toHaveLength(1)
    expect(joins[0]).toMatchObject({ aPose: 'standing-side-right', bPose: 'standing-back', aFrame: 0, bFrame: 0 })
    expect(bridgesFor(joins[0], [{ name: 'turn', info: posed('turn')! }, { name: 'back', info: posed('back')! }])[0]).toEqual([{ name: 'turn', reverse: false, mirror: false }])
  })

  it('knows a flipped clip faces the other way, and turns him round with two clips', () => {
    expect(flipPose('standing-side-right', true)).toBe('standing-side-left')
    expect(flipPose('sitting-rear-left', true)).toBe('sitting-rear-right')
    expect(flipPose('standing-front', true)).toBe('standing-front')
    const posed: ClipLookup = (n) => ({ keeper_walk: { ...clip(9, 8), closed: true, startPose: 'standing-side-right', endPose: 'standing-side-right' }, toFront: { ...clip(4, 8), startPose: 'standing-side-right', endPose: 'standing-front' } } as Record<string, ClipInfo>)[n]
    // Walks right, then walks back left: an instant about-turn.
    const r = { ...base([{ id: 'a', kind: 'walk', to: 70 }, { id: 'b', kind: 'walk', to: 20 }]), startAt: 10 as const }
    const [j] = joinsOf(compile(r, {}, posed))
    expect([j.aPose, j.bPose]).toEqual(['standing-side-right', 'standing-side-left'])
    expect(bridgesFor(j, [{ name: 'toFront', info: posed('toFront')! }])).toEqual([[{ name: 'toFront', reverse: false, mirror: false }, { name: 'toFront', reverse: true, mirror: true }]])
    // Never through a special state, however the poses line up.
    const chute = { ...clip(9, 8), startPose: 'standing-side-right', endPose: 'parachute-open', mirrorSafe: true }
    expect(bridgesFor(j, [{ name: 'chute', info: chute }])).toEqual([])
    expect(isOrdinaryPose('sitting-rear-left')).toBe(true)
    expect(isOrdinaryPose('scuba-swim-right')).toBe(false)
    // Only clips in the outfit he is wearing.
    expect(bridgesFor(j, [{ name: 'partyToFront', info: { ...posed('toFront')!, outfit: 'party-hat' } }])).toEqual([])
  })

  it('holds the standing frame while he stands still', () => {
    const r = base([{ id: 'w', kind: 'wait', clip: 'keeper_walk', seconds: 3 }])
    const seg = compile(r, {}, tiny).segments[0]
    expect([0, 1.3, 2.9].map((s) => frameFrom(seg, s))).toEqual([0, 0, 0])
  })

  it('flags a costume change where part of him would still be seen', () => {
    const enter = cleanRecipe({ id: 'enter', kind: 'macro', steps: [{ id: 'o', kind: 'wait', seconds: 0.2, doorAfter: 'open' }, { id: 'h', kind: 'hide', through: 'door', swapTo: 'light-blue-pyjamas' }] })!
    const r = { ...base([{ id: 'm', kind: 'macro', macro: 'enter' }]), startAt: 'doorOut' as const }
    const tl = compile(r, { enter }, tiny)
    expect(checkSolids(r, tl)).toEqual([]) // a 22 px body behind a 24 px door
    const wide: BoundsLookup = () => ({ left: -14, right: 14, bottom: 0, top: 38 })
    expect(checkSolids(r, tl, wide).map((i) => i.kind)).toEqual(['swap'])
  })
})

describe('the door’s clear area', () => {
  it('keeps every door’s clear area free of objects, and checks the inner door too', () => {
    const r = cleanRecipe({ id: 'clear', objects: [{ id: 'box', label: 'Toy box', x: 40, w: 16, h: 10 }], action: { object: 'box', dx: 0, facing: 'right' }, steps: [] })!
    expect(checkSolids(r, compile(r, {}, tiny)).map((i) => i.kind)).toEqual(['place'])
    const moved = { ...r, objects: [{ ...r.objects[0], x: DOOR_CLEAR + 8 }] }
    expect(checkSolids(moved, compile(moved, {}, tiny))).toEqual([])
    const inner = { ...moved, room: { name: 'Room', inner: true }, objects: [{ ...r.objects[0], x: 100 }] }
    expect(checkSolids(inner, compile(inner, {}, tiny)).map((i) => i.text)).toEqual([expect.stringContaining('the inner door')])
  })
})

describe('object types and variants', () => {
  const oven = cleanCategory({ id: 'oven', label: 'Oven', layer: 'back', solid: true, spots: [{ id: 'use', label: 'Use' }], variants: [{ id: 'small', label: 'Small', w: 20, h: 20, spots: { use: { dx: 0, facing: 'right' } } }, { id: 'big', label: 'Big', w: 50, h: 24, spots: { use: { dx: -12, facing: 'left' } } }] })!
  const table: StageObject = { id: 'table', label: 'Table', x: 100, w: 20, h: 19, layer: 'back', solid: true }
  const r = cleanRecipe({ id: 'cook', startAt: 20, objects: [{ id: 'o', label: '', x: 60, w: 1, h: 1, category: 'oven', variant: 'small' }, table], action: { object: 'o', spot: 'use', dx: 1, facing: 'right' }, steps: [{ id: 'a', kind: 'walk', to: 'action' }, { id: 'b', kind: 'walk', to: '@table' }] })!

  it('takes size, label and standing spot from the variant, with the recipe’s nudge on top', () => {
    const small = resolveRecipe(r, { oven }).recipe
    expect(small.objects[0]).toMatchObject({ w: 20, h: 20, label: 'Oven', solid: true })
    expect(placeX(small, 'action')).toBe(61)
    const big = resolveRecipe({ ...r, objects: [{ ...r.objects[0], variant: 'big' }, table] }, { oven }).recipe
    expect(big.objects[0].w).toBe(50)
    expect(placeX(big, 'action')).toBe(60 - 12 + 1)
    expect(big.action.facing).toBe('left')
  })

  it('stops just clear of an object he walks to, so the route stretches when it changes size', () => {
    const res = resolveRecipe(r, { oven }).recipe
    const tl = compile(res, {}, tiny)
    expect(tl.segments[1].x1).toBe(100 - 10 - KEEPER_HALF - 1)
    const wide = { ...res, objects: [res.objects[0], { ...table, w: 40 }] }
    expect(compile(wide, {}, tiny).segments[1].x1).toBe(100 - 20 - KEEPER_HALF - 1)
  })

  it('lists the recipe with each variant in turn, and reports an unknown type or spot', () => {
    expect(everyVariant(r, { oven }).map((v) => v.variant.id)).toEqual(['small', 'big'])
    expect(resolveRecipe(r, {}).problems).toHaveLength(2)
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
    expect(walkFor('standard', has)).toBe('keeper_walk_cycle')
    expect(walkFor('light-blue-pyjamas', has)).toBe('keeper_pyjamas_walk_cycle')
    expect(walkFor('knight', has)).toBe('keeper_knight_walk_side_cycle')
    expect(walkFor('no-such-outfit', has)).toBe('keeper_walk_cycle')
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
