/**
 * RECIPES. One activity written as data: the room, its objects, the action
 * point, the outfit he starts in, and the steps he goes through (walk to the
 * door, open it, step through and change, walk to the armchair, sit, nap,
 * stand, leave). Reusable steps live in MACROS (enter a room, leave a room),
 * which recipes use by name, so improving a macro improves every recipe.
 *
 * `compile` turns a recipe into a timeline: who is where, showing which frame
 * of which clip, at every moment, plus the sound cues. The recipe studio plays
 * it; later the game will too. Pure: no screen, no clock. Units are the art's
 * logical pixels (x along the floor, 0 = the room's left wall, the stairway to
 * the left of it) and real seconds. docs/RECIPES.md describes the format.
 */

// ─── The format ──────────────────────────────────────────────────────────────

export type Facing = 'left' | 'right'
/**
 * Where a walk goes: a named place in the room, an object (`@table`, or
 * `@cooker:use` for one of its type's standing spots), or an x. Walking to an
 * object without a spot stops him just clear of its nearer edge, so the route
 * stretches when the object is moved, swapped or upgraded.
 */
export type Target = 'stairs' | 'doorOut' | 'doorIn' | 'innerIn' | 'innerOut' | 'action' | `@${string}` | number

export interface Cue {
  id: string
  /** A sound in the library, by name. A name with no file yet plays a placeholder blip. */
  sound: string
  /** Seconds after its step starts. */
  at: number
  /** Where in the sound file to start and stop (seconds; null = its end). */
  trimStart: number
  trimEnd: number | null
  volume: number
  /** Repeat it until the step ends (a tap running, a snore). */
  loop: boolean
}

export type StepKind = 'walk' | 'play' | 'loop' | 'hide' | 'wait' | 'macro'

export interface Step {
  id: string
  kind: StepKind
  label?: string
  /** walk: where to. */
  to?: Target
  /** walk: picture units a second (default: the recipe's walk speed). */
  speed?: number
  /** The clip, if not the outfit's own walk (walk) or standing pose (wait). */
  clip?: string
  /** play: run the clip backwards (standing up is sitting down reversed). */
  reverse?: boolean
  /** Which way he faces; 'auto' keeps the way he was facing (or walking). */
  facing?: Facing | 'auto'
  /** Nudges from where he stands, in logical pixels (dy up). */
  dx?: number
  dy?: number
  /** loop, wait, hide: how long (seconds). */
  seconds?: number
  /** The step the activity is: the player can stop it at any moment, and its length is the activity's. */
  main?: boolean
  /** In the game it runs until another order; here `seconds` is how long the preview runs. */
  untilStopped?: boolean
  /** hide: the doorway he passes through, and the outfit he comes out in ('' keeps it). */
  through?: 'door' | 'inner'
  swapTo?: string
  /** play or hide: what the door does when the step ends. */
  doorAfter?: 'open' | 'close'
  /** macro: which, and the outfit it changes into ('' = none). */
  macro?: string
  params?: { swapTo?: string }
  cues?: Cue[]
}

export interface StageObject {
  id: string
  label: string
  /** Bottom-centre, logical pixels from the room's left wall. */
  x: number
  w: number
  h: number
  /** A sprite to show instead of the placeholder box, when it exists. */
  sprite?: string
  /** Contact heights to mark (seat 11, worktop 19 …), from docs/KEEPER_OBJECT_DIMENSIONS.md. */
  marks?: { label: string; y: number }[]
  /**
   * 'back': against the back wall, drawn behind him (he can pass in front of it).
   * 'front': on a side wall or nearer the camera, drawn in front of him and
   * opaque, so it must never cover him while he is meant to be seen.
   */
  layer?: 'back' | 'front'
  /** He can never walk into or through it (except the object he is using: he sits on the armchair). Front objects are always solid. */
  solid?: boolean
  /**
   * Its type (the game's object id, e.g. `cooker`) and which variant (usually
   * the upgrade tier). With a type, its size, art, contact marks and standing
   * spots come from that variant, so one recipe serves every oven.
   */
  category?: string
  variant?: string
  /** Filled in from its variant when the recipe is resolved. */
  spots?: Record<string, Spot>
}

// ─── Object types: one recipe for every variant ──────────────────────────────

/** Where he stands to use one variant: from its bottom-centre, and the way he faces. */
export interface Spot {
  dx: number
  facing: Facing
}

export interface Variant {
  id: string
  label: string
  /** The upgrade tier it is, if it is one. */
  tier?: number
  /** The sprite's base name (`obj_cooker_t2`); a placeholder box until it exists. */
  sprite?: string
  w: number
  h: number
  marks?: { label: string; y: number }[]
  /** Each of the type's spots, for this variant. */
  spots: Record<string, Spot>
}

/** A type of object (an oven), its standing spots, and its variants (the three ovens). */
export interface Category {
  id: string
  kind: 'category'
  label: string
  notes: string
  layer?: 'back' | 'front'
  solid?: boolean
  spots: { id: string; label: string }[]
  variants: Variant[]
}

export const variantOf = (c: Category | undefined, id: string | undefined) => (c ? c.variants.find((v) => v.id === id) ?? c.variants[0] : undefined)

export interface Recipe {
  id: string
  kind: 'recipe' | 'macro'
  title: string
  notes: string
  status: 'draft' | 'needs-work' | 'approved'
  /** The game interaction it is for, if any (config.ts INTERACTIONS). */
  activity?: string
  outfit: string
  startAt: Target
  facing: Facing
  room: { name: string; inner: boolean }
  objects: StageObject[]
  /**
   * Where he stands to do it. With `spot`, the object's type says where (and
   * which way he faces) for whichever variant is in the room, and `dx` is a
   * nudge on top; without one, `dx` is from the object's bottom-centre.
   */
  action: { object: string; spot?: string; dx: number; facing: Facing }
  walkSpeed: number
  steps: Step[]
}

/** What the timeline needs to know about a clip (from the sprite manifest). */
export interface ClipInfo {
  w: number
  h: number
  frames: number
  fps: number
  anchor: [number, number]
  /** The way it was drawn facing, if it has one (a rear view does not). */
  native: Facing | null
  /** May be flipped for the other direction. */
  mirrorSafe: boolean
  /** Sounds marked on the sheet itself (Codex's sidecar `sfxCues`): every recipe using the clip gets them. */
  sfxCues?: { frame: number; cue: string }[]
}
export type ClipLookup = (name: string) => ClipInfo | undefined

// ─── The stage ───────────────────────────────────────────────────────────────

/** The room is 110 wide and 56 tall (docs/DOORS_STAIRS_AND_COSTUMES.md); the stairway runs alongside on the left. */
export const STAGE = { roomW: 110, roomH: 56, stairW: 38, wall: 0, ladderX: -27 } as const
/**
 * Half his body width when standing (the 22 px silhouette), for checks made
 * without the sprite's own pixels. The studio uses each frame's real pixels.
 */
export const KEEPER_HALF = 11
/**
 * A doorway, until Codex's door art fixes the numbers: the jamb on the
 * stairway side, and the open door leaf on the room side. Both are opaque and
 * in front of him; the leaf is what hides him as he passes. He stands clear of
 * both before and after.
 */
export const DOOR = { jamb: 4, leaf: 12, height: 44 } as const
/** Each side of a doorway he stands, and the doorways themselves. */
const PLACES = {
  stairs: STAGE.ladderX,
  doorOut: -(DOOR.jamb + KEEPER_HALF),
  doorIn: DOOR.leaf + KEEPER_HALF,
  innerIn: STAGE.roomW - DOOR.leaf - KEEPER_HALF,
  innerOut: STAGE.roomW + DOOR.jamb + KEEPER_HALF,
} as const
export const DOORWAY = { door: 0, inner: STAGE.roomW } as const

export const placeX = (r: Recipe, t: Target, from?: number): number => {
  if (typeof t === 'number') return Math.round(t)
  if (t === 'action') {
    const o = r.objects.find((x) => x.id === r.action.object)
    return Math.round((o?.x ?? STAGE.roomW / 2) + r.action.dx)
  }
  if (t.startsWith('@')) {
    const [id, spot] = t.slice(1).split(':')
    const o = r.objects.find((x) => x.id === id)
    if (!o) return from ?? STAGE.roomW / 2
    const s = spot ? o.spots?.[spot] : undefined
    if (s) return Math.round(o.x + s.dx)
    // Just clear of the nearer edge.
    const side = (from ?? 0) <= o.x ? -1 : 1
    return Math.round(o.x + side * (o.w / 2 + KEEPER_HALF + 1))
  }
  return PLACES[t as keyof typeof PLACES]
}

/** Which way he faces on arriving at an object target. */
const facingAt = (r: Recipe, t: Target, x: number): Facing | null => {
  if (typeof t !== 'string' || !t.startsWith('@')) return null
  const [id, spot] = t.slice(1).split(':')
  const o = r.objects.find((y) => y.id === id)
  if (!o) return null
  return (spot && o.spots?.[spot]?.facing) || (o.x >= x ? 'right' : 'left')
}

/**
 * A recipe with every typed object filled in from its variant (size, art,
 * marks, spots) and the action point worked out from its spot. Compiling and
 * checking always use this; editing changes the recipe itself.
 */
export function resolveRecipe(r: Recipe, cats: Record<string, Category>): { recipe: Recipe; problems: string[] } {
  const problems: string[] = []
  const objects = r.objects.map((o) => {
    if (!o.category) return o
    const c = cats[o.category]
    const v = variantOf(c, o.variant)
    if (!c || !v) {
      problems.push(`${o.label} is a ${o.category}, but there is no such object type`)
      return o
    }
    return { ...o, label: o.label || c.label, w: v.w, h: v.h, sprite: v.sprite ?? o.sprite, marks: v.marks ?? o.marks, layer: c.layer ?? o.layer, solid: c.solid ?? o.solid, variant: v.id, spots: v.spots }
  })
  let action = r.action
  if (r.action.spot) {
    const o = objects.find((x) => x.id === r.action.object)
    const s = o?.spots?.[r.action.spot]
    if (s) action = { ...r.action, dx: s.dx + r.action.dx, facing: s.facing }
    else problems.push(`${o?.label ?? r.action.object} has no “${r.action.spot}” spot`)
  }
  return { recipe: { ...r, objects, action }, problems }
}

/** The same recipe with each variant of each typed object in turn (the others as they are). */
export function everyVariant(r: Recipe, cats: Record<string, Category>): { object: StageObject; variant: Variant; recipe: Recipe }[] {
  return r.objects.flatMap((o) => {
    const c = o.category ? cats[o.category] : undefined
    return (c?.variants ?? []).map((v) => ({ object: o, variant: v, recipe: { ...r, objects: r.objects.map((x) => (x.id === o.id ? { ...x, variant: v.id } : x)) } }))
  })
}

/** An object type from saved or drafted JSON (anything missing gets a safe default). */
export function cleanCategory(raw: unknown): Category | null {
  if (!raw || typeof raw !== 'object') return null
  const d = raw as Partial<Category>
  if (typeof d.id !== 'string' || !/^[a-z0-9_-]{1,60}$/.test(d.id)) return null
  const spots = Array.isArray(d.spots) ? d.spots.filter((s) => s && typeof s.id === 'string').map((s) => ({ id: s.id, label: typeof s.label === 'string' ? s.label : s.id })) : []
  const variants = (Array.isArray(d.variants) ? d.variants : [])
    .filter((v) => v && typeof v.id === 'string')
    .map((v) => ({
      id: v.id,
      label: typeof v.label === 'string' ? v.label : v.id,
      tier: typeof v.tier === 'number' ? v.tier : undefined,
      sprite: typeof v.sprite === 'string' && v.sprite ? v.sprite : undefined,
      w: typeof v.w === 'number' && v.w > 0 ? v.w : 20,
      h: typeof v.h === 'number' && v.h > 0 ? v.h : 20,
      marks: Array.isArray(v.marks) ? v.marks : undefined,
      spots: Object.fromEntries(spots.map((s) => [s.id, { dx: Number(v.spots?.[s.id]?.dx) || 0, facing: v.spots?.[s.id]?.facing === 'left' ? 'left' : 'right' } as Spot])),
    }))
  if (!variants.length) return null
  return { id: d.id, kind: 'category', label: typeof d.label === 'string' ? d.label : d.id, notes: typeof d.notes === 'string' ? d.notes : '', layer: d.layer === 'front' ? 'front' : d.layer === 'back' ? 'back' : undefined, solid: typeof d.solid === 'boolean' ? d.solid : undefined, spots, variants }
}

/** The neutral-ended walk cycle for each outfit, falling back to its approved walk. */
export const walkFor = (outfit: string, has: (name: string) => boolean): string => {
  if (outfit === 'standard') return has('keeper_walk_cycle') ? 'keeper_walk_cycle' : 'keeper_walk'
  const short = { 'light-blue-pyjamas': 'pyjamas', 'cream-bathrobe': 'bathrobe', 'party-hat': 'party', souwester: 'souwester', 'artist-smock': 'artist_smock' }[outfit] ?? outfit
  const base = [`keeper_${short}_walk`, `keeper_${short}_walk_side`].find(has)
  return (base && has(`${base}_cycle`) ? `${base}_cycle` : base) ?? (has('keeper_walk_cycle') ? 'keeper_walk_cycle' : 'keeper_walk')
}

// ─── The timeline ────────────────────────────────────────────────────────────

export interface Segment {
  /** The top-level step it came from (a macro's steps all carry the macro step's id). */
  stepId: string
  /** The step itself (inside a macro, the macro's own step). */
  innerId: string
  fromMacro?: string
  kind: Exclude<StepKind, 'macro'>
  label: string
  start: number
  end: number
  clip: string | null
  info: ClipInfo | null
  reverse: boolean
  /** Hold the last frame (a play-once clip). */
  once: boolean
  x0: number
  x1: number
  dx: number
  dy: number
  mirror: boolean
  visible: boolean
  outfit: string
  door: boolean
  inner: boolean
  main: boolean
  untilStopped: boolean
  /** He works this doorway's door in this step (opens or closes it), so his hand may touch it. */
  touches: 'door' | 'inner' | null
}

export interface TimedCue extends Cue {
  stepId: string
  fromMacro?: string
  /** Marked on this clip's sheet rather than in a recipe. */
  fromClip?: string
  time: number
  /** When it must stop (a looped cue runs to its step's end). */
  until: number | null
}

export interface Timeline {
  segments: Segment[]
  cues: TimedCue[]
  /** When each of the recipe's own steps starts and ends (a macro step spans all of its steps). */
  steps: { id: string; start: number; end: number }[]
  duration: number
  problems: string[]
}

export interface CompileOptions {
  /** Cut the main step short here (the player stopped it): seconds into that step. */
  mainSeconds?: number
}

const directional = (c: ClipInfo | null) => !!c && (c.native !== null || c.mirrorSafe)
const mirrorFor = (c: ClipInfo | null, facing: Facing) => directional(c) && c!.mirrorSafe !== false && facing !== (c!.native ?? 'right')

/** Turn a recipe (and the macros it uses) into a timeline. */
export function compile(r: Recipe, macros: Record<string, Recipe>, clips: ClipLookup, opts: CompileOptions = {}): Timeline {
  const segments: Segment[] = []
  const cues: TimedCue[] = []
  const problems: string[] = []
  const spans: Timeline['steps'] = []
  const has = (n: string) => !!clips(n)
  let t = 0
  let x = placeX(r, r.startAt)
  let facing: Facing = r.facing
  let outfit = r.outfit
  let door = false
  let inner = false

  const run = (steps: readonly Step[], top: Step | null, params: Step['params'], depth: number, macroId?: string) => {
    for (const s of steps) {
      const stepId = top?.id ?? s.id
      const at0 = t
      if (s.kind === 'macro') {
        const m = s.macro ? macros[s.macro] : undefined
        if (!m) problems.push(`Step “${s.label ?? s.id}” uses a macro that does not exist: ${s.macro ?? '(none)'}`)
        else if (depth > 3) problems.push(`Macro ${m.id} is nested too deeply`)
        else run(m.steps, top ?? s, { ...params, ...s.params }, depth + 1, m.id)
        addCues(s, stepId, at0, t, top ? macroId : undefined)
        if (!top) spans.push({ id: s.id, start: at0, end: t })
        continue
      }
      const swap = s.swapTo === '$swapTo' ? (params?.swapTo ?? '') : (s.swapTo ?? '')
      const base: Omit<Segment, 'kind' | 'start' | 'end' | 'clip' | 'info' | 'x0' | 'x1' | 'mirror' | 'once' | 'visible'> = {
        stepId,
        innerId: s.id,
        fromMacro: macroId,
        label: s.label ?? s.kind,
        reverse: !!s.reverse,
        dx: Math.round(s.dx ?? 0),
        dy: Math.round(s.dy ?? 0),
        outfit,
        door,
        inner,
        main: !!s.main,
        untilStopped: !!s.untilStopped,
        touches: s.doorAfter && s.kind !== 'hide' ? (s.through ?? 'door') : null,
      }
      if (s.kind === 'walk') {
        const to = placeX(r, s.to ?? 'action', x)
        const clip = s.clip || walkFor(outfit, has)
        const info = clips(clip) ?? null
        if (!info) problems.push(`No walk clip ${clip}`)
        const speed = Math.max(1, s.speed ?? r.walkSpeed)
        const dist = Math.abs(to - x)
        if (to !== x) facing = to > x ? 'right' : 'left'
        if (s.facing && s.facing !== 'auto' && dist === 0) facing = s.facing
        const dur = dist / speed
        if (dur > 0) segments.push({ ...base, kind: 'walk', start: t, end: t + dur, clip, info, x0: x, x1: to, mirror: mirrorFor(info, facing), once: false, visible: true })
        t += dur
        x = to
        if (s.facing && s.facing !== 'auto') facing = s.facing
        else if ((s.to ?? 'action') === 'action') facing = r.action.facing
        else facing = facingAt(r, s.to!, x) ?? facing
      } else if (s.kind === 'play' || s.kind === 'loop' || s.kind === 'wait') {
        if (s.facing && s.facing !== 'auto') facing = s.facing
        const clip = s.clip || (s.kind === 'wait' ? walkFor(outfit, has) : '')
        const info = clip ? clips(clip) ?? null : null
        if (s.kind !== 'wait' && !info) problems.push(`Step “${s.label ?? s.id}” needs a clip${clip ? ` (${clip} is not in the sprites)` : ''}`)
        let dur = s.kind === 'play' ? (info ? info.frames / info.fps : 1) : Math.max(0, s.seconds ?? 2)
        if (s.main && opts.mainSeconds !== undefined) dur = Math.max(0, Math.min(dur, opts.mainSeconds))
        segments.push({ ...base, kind: s.kind, start: t, end: t + dur, clip: clip || null, info, x0: x, x1: x, mirror: mirrorFor(info, facing), once: s.kind === 'play' || s.kind === 'wait', visible: true })
        t += dur
      } else if (s.kind === 'hide') {
        const way = s.through ?? 'door'
        const wall = DOORWAY[way]
        const to = way === 'door' ? (x < wall ? PLACES.doorIn : PLACES.doorOut) : x < wall ? PLACES.innerOut : PLACES.innerIn
        facing = to > x ? 'right' : 'left'
        const dur = Math.max(0.1, s.seconds ?? 0.6)
        segments.push({ ...base, kind: 'hide', start: t, end: t + dur, clip: null, info: null, x0: x, x1: to, mirror: false, once: false, visible: false })
        t += dur
        x = to
        if (swap) outfit = swap
      }
      if (s.doorAfter) {
        const open = s.doorAfter === 'open'
        if ((s.through ?? 'door') === 'inner') inner = open
        else door = open
      }
      addCues(s, stepId, at0, t, macroId)
      if (!top) spans.push({ id: s.id, start: at0, end: t })
    }
  }
  // A sheet's own cues, each time its frame comes round (backwards too).
  const clipCues = (seg: Segment) => {
    const info = seg.info
    if (!info?.sfxCues?.length || !seg.clip) return
    const dur = seg.end - seg.start
    const rounds = seg.once ? 1 : Math.ceil((dur * info.fps) / info.frames)
    for (const c of info.sfxCues) {
      if (c.frame < 0 || c.frame >= info.frames) continue
      const shown = seg.reverse ? info.frames - 1 - c.frame : c.frame
      for (let k = 0; k < rounds; k++) {
        const time = seg.start + (k * info.frames + shown) / info.fps
        if (time >= seg.end - 1e-9) break
        cues.push({ id: `clip-${seg.clip}-${c.frame}`, sound: c.cue, at: time - seg.start, trimStart: 0, trimEnd: null, volume: 1, loop: false, stepId: seg.stepId, fromMacro: seg.fromMacro, fromClip: seg.clip, time, until: null })
      }
    }
  }
  const addCues = (s: Step, stepId: string, start: number, end: number, fromMacro?: string) => {
    for (const c of s.cues ?? []) cues.push({ ...c, stepId, fromMacro, time: start + Math.max(0, c.at), until: c.loop ? end : null })
  }

  run(r.steps, null, {}, 0)
  for (const seg of segments) clipCues(seg)
  return { segments, cues: cues.sort((a, b) => a.time - b.time), steps: spans, duration: t, problems }
}

// ─── Reading the timeline ────────────────────────────────────────────────────

export interface Shot {
  segment: Segment | null
  clip: string | null
  info: ClipInfo | null
  frame: number
  /** Feet position, whole logical pixels. */
  x: number
  y: number
  mirror: boolean
  visible: boolean
  outfit: string
  door: boolean
  inner: boolean
}

/** Which frame he shows at a moment. Positions are whole pixels so the art stays crisp. */
export function frameFrom(seg: Segment, local: number): number {
  const info = seg.info
  if (!info) return 0
  const n = Math.floor(Math.max(0, local) * info.fps + 1e-9)
  const i = seg.once ? Math.min(info.frames - 1, n) : n % info.frames
  return seg.reverse ? info.frames - 1 - i : i
}

export function shotAt(tl: Timeline, time: number, r: Pick<Recipe, 'startAt' | 'outfit'> & Partial<Recipe>): Shot {
  const segs = tl.segments
  const seg = segs.find((s) => time >= s.start && time < s.end) ?? (time >= tl.duration ? segs[segs.length - 1] : segs[0]) ?? null
  if (!seg) return { segment: null, clip: null, info: null, frame: 0, x: typeof r.startAt === 'number' ? r.startAt : 0, y: 0, mirror: false, visible: true, outfit: r.outfit, door: false, inner: false }
  const local = Math.min(seg.end - seg.start, Math.max(0, time - seg.start))
  const k = seg.end > seg.start ? local / (seg.end - seg.start) : 1
  const end = time >= seg.end
  return {
    segment: seg,
    clip: seg.clip,
    info: seg.info,
    frame: end && seg.info ? frameFrom(seg, seg.end - seg.start - 1e-6) : frameFrom(seg, local),
    x: Math.round(seg.x0 + (seg.x1 - seg.x0) * k) + seg.dx,
    y: seg.dy,
    mirror: seg.mirror,
    visible: seg.visible,
    outfit: seg.outfit,
    door: seg.door,
    inner: seg.inner,
  }
}

// ─── Solid things ────────────────────────────────────────────────────────────

/** Something he must not walk into, or be covered by, along the floor (logical px). */
export interface Zone {
  id: string
  label: string
  x0: number
  x1: number
  top: number
  /** Drawn in front of him and opaque. */
  front: boolean
  /** He cannot walk through it. */
  solid: boolean
  kind: 'wall' | 'door' | 'object'
}

export const isFront = (o: StageObject) => o.layer === 'front'
export const isSolid = (o: StageObject) => isFront(o) || !!o.solid

/** The walls, the doors (their leaves only while open) and the solid or front objects. */
export function zonesOf(r: Recipe, door: boolean, inner: boolean): Zone[] {
  const H = STAGE.roomH
  const z: Zone[] = [
    { id: 'wall', label: 'the wall by the door', x0: -DOOR.jamb, x1: 0, top: H, front: true, solid: true, kind: 'wall' },
    { id: 'wall-far', label: r.room.inner ? 'the wall by the inner door' : 'the far wall', x0: STAGE.roomW, x1: STAGE.roomW + DOOR.jamb, top: H, front: true, solid: true, kind: 'wall' },
  ]
  if (door) z.push({ id: 'door', label: 'the open door', x0: 0, x1: DOOR.leaf, top: DOOR.height, front: true, solid: true, kind: 'door' })
  if (r.room.inner && inner) z.push({ id: 'inner', label: 'the open inner door', x0: STAGE.roomW - DOOR.leaf, x1: STAGE.roomW, top: DOOR.height, front: true, solid: true, kind: 'door' })
  for (const o of r.objects) if (isSolid(o)) z.push({ id: o.id, label: o.label, x0: o.x - o.w / 2, x1: o.x + o.w / 2, top: o.h, front: isFront(o), solid: true, kind: 'object' })
  return z
}

/** Where a frame's opaque pixels are, from his feet: x as drawn facing its own way, y up from the floor. */
export interface Bounds {
  left: number
  right: number
  bottom: number
  top: number
}
export type BoundsLookup = (clip: string, frame: number) => Bounds | null

const bodyBounds: Bounds = { left: -KEEPER_HALF, right: KEEPER_HALF, bottom: 0, top: 38 }

export interface Issue {
  time: number
  stepId: string
  kind: 'walk' | 'cover'
  text: string
}

/**
 * Check the rules about solid things. He may never walk through a wall (only
 * a hidden doorway step crosses one) or through a solid object (the one he is
 * using is allowed: he stops at it, or sits on it). And while he can be seen,
 * nothing drawn in front of him may cover any of his pixels; being covered is
 * only allowed while he is hidden in a doorway.
 */
export function checkSolids(r: Recipe, tl: Timeline, boundsOf: BoundsLookup = () => null): Issue[] {
  const out: Issue[] = []
  const seen = new Set<string>()
  // One report per thing per step: the first frame it happens.
  const add = (i: Issue, what: string) => {
    const key = `${i.kind}:${i.stepId}:${what}`
    if (!seen.has(key)) {
      seen.add(key)
      out.push(i)
    }
  }
  const actionX = placeX(r, 'action')
  for (const seg of tl.segments) {
    const zones = zonesOf(r, seg.door, seg.inner)
    if (seg.kind === 'walk') {
      const lo = Math.min(seg.x0, seg.x1) - KEEPER_HALF
      const hi = Math.max(seg.x0, seg.x1) + KEEPER_HALF
      const usingIt = seg.x0 === actionX || seg.x1 === actionX
      for (const z of zones) {
        if (!z.solid || hi <= z.x0 || lo >= z.x1) continue
        if (z.kind === 'door') continue // the open leaf is checked as a cover: he walks up to it, not into it
        if (z.kind === 'object' && z.id === r.action.object && usingIt) continue
        add({ time: seg.start, stepId: seg.stepId, kind: 'walk', text: `walks into ${z.label}` }, z.id)
      }
    }
    if (!seg.visible || !seg.info) continue
    // Every frame he shows in this step (a long loop repeats, so one round is enough).
    const frames = Math.min(seg.info.frames * 2, Math.ceil((seg.end - seg.start) * seg.info.fps) + 1)
    for (let k = 0; k < frames; k++) {
      const local = Math.min(seg.end - seg.start - 1e-6, k / seg.info.fps)
      const frame = frameFrom(seg, local)
      const x = Math.round(seg.x0 + (seg.x1 - seg.x0) * (seg.end > seg.start ? local / (seg.end - seg.start) : 1)) + seg.dx
      const b = boundsOf(seg.clip!, frame) ?? bodyBounds
      const left = seg.mirror ? x - b.right : x + b.left
      const right = seg.mirror ? x - b.left : x + b.right
      for (const z of zones) {
        if (seg.touches === 'door' && (z.id === 'wall' || z.id === 'door')) continue // his hand is on the door
        if (seg.touches === 'inner' && (z.id === 'wall-far' || z.id === 'inner')) continue
        if (!z.front || right <= z.x0 || left >= z.x1 || b.bottom + seg.dy >= z.top) continue
        add({ time: seg.start + local, stepId: seg.stepId, kind: 'cover', text: `${z.label} covers part of him (${seg.clip}, frame ${frame + 1})` }, z.id)
      }
    }
  }
  return out.sort((a, b) => a.time - b.time)
}

/** The main step's segment, if the recipe has one. */
export const mainOf = (tl: Timeline) => tl.segments.find((s) => s.main)

// ─── Editing helpers ─────────────────────────────────────────────────────────

let n = 0
export const newId = (prefix: string) => `${prefix}-${Date.now().toString(36)}${(n++).toString(36)}`

export const newCue = (sound: string, at: number): Cue => ({ id: newId('cue'), sound, at: Math.max(0, Math.round(at * 100) / 100), trimStart: 0, trimEnd: null, volume: 1, loop: false })

/** Swap one step for an edited copy, wherever it is. */
export const withStep = (r: Recipe, id: string, f: (s: Step) => Step): Recipe => ({ ...r, steps: r.steps.map((s) => (s.id === id ? f(s) : s)) })

export const moveStep = (r: Recipe, id: string, by: -1 | 1): Recipe => {
  const i = r.steps.findIndex((s) => s.id === id)
  const j = i + by
  if (i < 0 || j < 0 || j >= r.steps.length) return r
  const steps = [...r.steps]
  ;[steps[i], steps[j]] = [steps[j], steps[i]]
  return { ...r, steps }
}

/** Every sound a recipe or macro names (the placeholders still to fill are the ones with no file). */
export const soundsUsed = (docs: readonly Recipe[]) => [...new Set(docs.flatMap((d) => d.steps.flatMap((s) => (s.cues ?? []).map((c) => c.sound))))].sort()

/** A short stable fingerprint, to tell when a draft changed under a saved edit. */
export function hashOf(value: unknown): string {
  const s = JSON.stringify(value)
  let h = 2166136261
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619)
  return (h >>> 0).toString(36)
}

/** A recipe from saved or drafted JSON, with every field present (anything missing gets a safe default). */
export function cleanRecipe(raw: unknown): Recipe | null {
  if (!raw || typeof raw !== 'object') return null
  const d = raw as Partial<Recipe>
  if (typeof d.id !== 'string' || !/^[a-z0-9_-]{1,60}$/.test(d.id)) return null
  return {
    id: d.id,
    kind: d.kind === 'macro' ? 'macro' : 'recipe',
    title: typeof d.title === 'string' ? d.title : d.id,
    notes: typeof d.notes === 'string' ? d.notes : '',
    status: d.status === 'approved' || d.status === 'needs-work' ? d.status : 'draft',
    activity: typeof d.activity === 'string' ? d.activity : undefined,
    outfit: typeof d.outfit === 'string' ? d.outfit : 'standard',
    startAt: d.startAt ?? 'stairs',
    facing: d.facing === 'left' ? 'left' : 'right',
    room: { name: d.room?.name ?? 'Room', inner: !!d.room?.inner },
    objects: Array.isArray(d.objects) ? d.objects.filter((o) => o && typeof o.id === 'string') : [],
    action: { object: d.action?.object ?? '', spot: typeof d.action?.spot === 'string' ? d.action.spot : undefined, dx: d.action?.dx ?? 0, facing: d.action?.facing === 'left' ? 'left' : 'right' },
    walkSpeed: typeof d.walkSpeed === 'number' && d.walkSpeed > 0 ? d.walkSpeed : 20,
    steps: Array.isArray(d.steps) ? d.steps.filter((s) => s && typeof s.id === 'string' && typeof s.kind === 'string') : [],
  }
}
