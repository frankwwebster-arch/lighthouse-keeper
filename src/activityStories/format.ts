/**
 * The shared bubble-story formats (docs: data/activity-stories/README.md).
 *
 * A story is an ordered list of steps (“the sausages flip onto the grill”).
 * It names pictures only by id; the picture library says which version of
 * each picture is current. Claude drafts stories, Frank adjusts them in the
 * recipe studio, and Codex adds or replaces pictures in the library.
 */

export const STORY_SCHEMA = 'lighthouse-keeper/activity-story@1'
export const LIBRARY_SCHEMA = 'lighthouse-keeper/activity-picture-library@1'

export type Speed = 'quick' | 'normal' | 'slow'
export type AfterStory = 'loop' | 'hold' | 'hide'
export type CastRole = 'hero' | 'support' | 'result'

/** What a step does. Each verb has one fixed motion; see VERBS. */
export type Verb =
  | 'arrive' | 'present' | 'land-on' | 'flip' | 'drop-in' | 'strike' | 'scrub' | 'pour' | 'tighten' | 'reveal' | 'serve' | 'pause' | 'settle'
  // Frank's a1 answer (21 Oct): ten working actions, each with its own movement.
  | 'saw' | 'chop' | 'stir' | 'shake' | 'spray' | 'wipe' | 'sweep' | 'dig' | 'brush' | 'iron'
/** `around`: supports come in from both sides. `left-to-right`: everything enters from the left and finished things leave to the right. */
export type Flow = 'around' | 'left-to-right'
/** A corner of the bubble, or `orbit`: small and circling slowly just outside the bubble, clear of the action. */
export type PropSlot = 'orbit' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right'

export interface CastMember {
  picture: string
  role: CastRole
  /** Pin an older picture version (Frank's one-tap undo). Absent = follow the library's current version. */
  version?: number
  /** A mark that bursts once as this picture appears, for about a second (Frank's a2 answer, 21 Oct): sparkles on the clean plate, steam on the hot dogs. */
  appear?: string
}

export interface Step {
  do: Verb
  /** The cast member that acts. Not used by settle. */
  who?: string
  /** The cast member it acts on. */
  onto?: string
  speed?: Speed
  /** A mark picture shown at each touch, instead of the verb's default. */
  mark?: string
  /**
   * reveal: the result takes the target's place instead of sitting on it.
   * land-on / flip: whatever is already on the target sinks into it as this one lands.
   */
  replace?: boolean
}

export interface Ambient {
  picture: string
  on: string
  /** First and last step (1-based) it shows during. */
  fromStep: number
  toStep: number
}

/** Scene-setting pictures (tongs, ketchup) that stay at the bubble's edge for a range of steps, bobbing gently. */
export interface Prop {
  picture: string
  at: PropSlot
  fromStep: number
  toStep: number
}

export interface StorySfx {
  step: number
  at: 'start' | 'contact' | 'end'
  cue: string
  owner: string
  kind: 'asset-state' | 'activity-beat' | 'completion'
}

export interface Story {
  schema: typeof STORY_SCHEMA
  id: string
  label: string
  appliesTo: { assetId: string; label: string }
  bodyCompatibility: 'rear-work-with-context' | 'dedicated-pose-required'
  afterStory: AfterStory
  /** Overall speed: 1 is normal, 1.25 is a quarter faster. */
  pace: number
  flow: Flow
  /** When it retells, start again from this step (1-based), so setting-up steps play only the first time. */
  loopFrom?: number
  cast: Record<string, CastMember>
  steps: Step[]
  ambient: Ambient[]
  props: Prop[]
  sfx: StorySfx[]
  notes?: string
}

export interface PictureVersion {
  v: number
  /** An archived /keeper-review/… URL or a /activity-stories/… file in public/. */
  url: string
  sha256: string
  cell: [number, number]
  /** Alpha > 8 bounds in the cell: [x0, y0, x1, y1]. */
  bounds: [number, number, number, number]
  added: string
  source: string
  by: 'codex' | 'claude' | 'frank'
  note?: string
}

export interface Picture {
  kind: 'object' | 'mark'
  family: string
  label: string
  current: number
  versions: PictureVersion[]
  review?: { status: 'rework-requested' | 'approved'; note: string }
}

export interface Library {
  schema: typeof LIBRARY_SCHEMA
  keeper: { rearWork: { url: string; sha256: string; ms: number }[] }
  pictures: Record<string, Picture>
}

export const VERBS: Record<Verb, { label: string; needs: ('who' | 'onto')[]; hint: string }> = {
  arrive: { label: 'arrives', needs: ['who'], hint: 'Pops out of his head and takes the middle.' },
  present: { label: 'takes the middle', needs: ['who'], hint: 'Moves to the middle; whatever was there steps aside.' },
  'land-on': { label: 'lands on', needs: ['who', 'onto'], hint: 'Swings in and stays stacked on top (or, with “replaces”, sends what was there down into it).' },
  flip: { label: 'flips onto', needs: ['who', 'onto'], hint: 'Somersaults in and stays on top (or, with “replaces”, sends what was there down into it).' },
  'drop-in': { label: 'drops into', needs: ['who', 'onto'], hint: 'Falls in and disappears inside.' },
  strike: { label: 'strikes', needs: ['who', 'onto'], hint: 'Hits it two or three times, then leaves.' },
  scrub: { label: 'scrubs', needs: ['who', 'onto'], hint: 'Rubs back and forth across it, then leaves.' },
  pour: { label: 'pours onto', needs: ['who', 'onto'], hint: 'Tips over it so drops fall, then leaves.' },
  tighten: { label: 'tightens', needs: ['who', 'onto'], hint: 'Turns in place on its edge, then leaves.' },
  saw: { label: 'saws', needs: ['who', 'onto'], hint: 'Saws back and forth across its top, cutting a little deeper, sawdust falling. Then leaves.' },
  chop: { label: 'chops', needs: ['who', 'onto'], hint: 'Quick downward strokes, moving along it like slicing. Then leaves.' },
  stir: { label: 'stirs', needs: ['who', 'onto'], hint: 'Dips in behind the rim and goes round and round inside it. Then leaves.' },
  shake: { label: 'shakes over', needs: ['who', 'onto'], hint: 'Turns over above it and shakes; bits fall onto it. Then leaves.' },
  spray: { label: 'sprays', needs: ['who', 'onto'], hint: 'Stands beside it, tilts towards it and puffs a mist across, again and again. Then leaves.' },
  wipe: { label: 'wipes', needs: ['who', 'onto'], hint: 'Small circles over it, a gleam left after each. Then leaves.' },
  sweep: { label: 'sweeps', needs: ['who', 'onto'], hint: 'Wide swings side to side along its bottom edge, dust puffing out at each end. Then leaves.' },
  dig: { label: 'digs into', needs: ['who', 'onto'], hint: 'Scoops down into it and flicks up and out, earth flying. Then leaves.' },
  brush: { label: 'brushes', needs: ['who', 'onto'], hint: 'Long slow strokes across it, one under another, lifting off after each. Then leaves.' },
  iron: { label: 'irons', needs: ['who', 'onto'], hint: 'Glides flat across it and back, steam rising behind. Then leaves.' },
  reveal: { label: 'appears from', needs: ['who', 'onto'], hint: 'Bursts out; anything stacked on it is used up.' },
  serve: { label: 'is served', needs: ['who'], hint: 'Leaves the bubble to the right (in a left-to-right story) or upwards.' },
  pause: { label: 'pause', needs: [], hint: 'A beat where nothing new happens; the heat and props carry on.' },
  settle: { label: 'quiet moment', needs: [], hint: 'Nothing moves for a moment before the story starts again.' },
}

const ID = /^[a-z0-9][a-z0-9-]{0,59}$/
const isObj = (v: unknown): v is Record<string, unknown> => !!v && typeof v === 'object' && !Array.isArray(v)
const str = (v: unknown, fallback = '') => (typeof v === 'string' ? v : fallback)

/** A clean copy of a story, or null if it isn't one. Unknown fields are dropped. */
export function cleanStory(raw: unknown): Story | null {
  if (!isObj(raw) || typeof raw.id !== 'string' || !ID.test(raw.id)) return null
  const cast: Record<string, CastMember> = {}
  if (isObj(raw.cast))
    for (const [as, m] of Object.entries(raw.cast)) {
      if (!ID.test(as) || !isObj(m) || typeof m.picture !== 'string') continue
      const role: CastRole = m.role === 'hero' || m.role === 'result' ? m.role : 'support'
      cast[as] = { picture: m.picture, role, ...(Number.isInteger(m.version) && (m.version as number) > 0 ? { version: m.version as number } : {}), ...(typeof m.appear === 'string' && m.appear ? { appear: m.appear } : {}) }
    }
  const steps: Step[] = (Array.isArray(raw.steps) ? raw.steps : []).flatMap((s): Step[] => {
    if (!isObj(s) || typeof s.do !== 'string' || !(s.do in VERBS)) return []
    const step: Step = { do: s.do as Verb }
    if (typeof s.who === 'string') step.who = s.who
    if (typeof s.onto === 'string') step.onto = s.onto
    if (s.speed === 'quick' || s.speed === 'slow' || s.speed === 'normal') step.speed = s.speed
    if (typeof s.mark === 'string' && s.mark) step.mark = s.mark
    if (s.replace === true) step.replace = true
    return [step]
  })
  const ambient: Ambient[] = (Array.isArray(raw.ambient) ? raw.ambient : []).flatMap((a): Ambient[] =>
    isObj(a) && typeof a.picture === 'string' && typeof a.on === 'string' && Number.isInteger(a.fromStep) && Number.isInteger(a.toStep)
      ? [{ picture: a.picture, on: a.on, fromStep: a.fromStep as number, toStep: a.toStep as number }]
      : [],
  )
  const SLOTS: PropSlot[] = ['orbit', 'top-left', 'top-right', 'bottom-left', 'bottom-right']
  const props: Prop[] = (Array.isArray(raw.props) ? raw.props : []).flatMap((a): Prop[] =>
    isObj(a) && typeof a.picture === 'string' && SLOTS.includes(a.at as PropSlot) && Number.isInteger(a.fromStep) && Number.isInteger(a.toStep)
      ? [{ picture: a.picture, at: a.at as PropSlot, fromStep: a.fromStep as number, toStep: a.toStep as number }]
      : [],
  )
  const sfx: StorySfx[] = (Array.isArray(raw.sfx) ? raw.sfx : []).flatMap((c): StorySfx[] =>
    isObj(c) && Number.isInteger(c.step) && typeof c.cue === 'string'
      ? [{ step: c.step as number, at: c.at === 'start' || c.at === 'end' ? c.at : 'contact', cue: c.cue, owner: str(c.owner, String(raw.id)), kind: c.kind === 'asset-state' || c.kind === 'completion' ? c.kind : 'activity-beat' }]
      : [],
  )
  const applies = isObj(raw.appliesTo) ? raw.appliesTo : {}
  const pace = typeof raw.pace === 'number' && raw.pace >= 0.5 && raw.pace <= 2 ? raw.pace : 1
  return {
    schema: STORY_SCHEMA,
    id: raw.id,
    label: str(raw.label, raw.id),
    appliesTo: { assetId: str(applies.assetId), label: str(applies.label) },
    bodyCompatibility: raw.bodyCompatibility === 'dedicated-pose-required' ? 'dedicated-pose-required' : 'rear-work-with-context',
    afterStory: raw.afterStory === 'hold' || raw.afterStory === 'hide' ? raw.afterStory : 'loop',
    pace,
    flow: raw.flow === 'left-to-right' ? 'left-to-right' : 'around',
    ...(Number.isInteger(raw.loopFrom) && (raw.loopFrom as number) > 1 && (raw.loopFrom as number) <= steps.length ? { loopFrom: raw.loopFrom as number } : {}),
    cast,
    steps,
    ambient,
    props,
    sfx,
    ...(typeof raw.notes === 'string' && raw.notes ? { notes: raw.notes } : {}),
  }
}

/**
 * The studio's picture groups, in menu order. An object goes in the first
 * group that lists its family; every mark goes in Marks; a family no group
 * names yet goes in “Other”, so a new picture from Codex is never hidden.
 */
export const PICTURE_GROUPS: { label: string; families: string[] }[] = [
  { label: 'BBQ', families: ['bbq'] },
  { label: 'BBQ tools', families: ['bbq-tools'] },
  { label: 'Food and meals', families: ['meal', 'sandwich', 'cooking', 'ingredient', 'baking', 'eggs', 'food-provenance', 'mixing', 'tea', 'toast'] },
  { label: 'Condiments and seasoning', families: ['condiment', 'seasoning'] },
  { label: 'Knives and prep', families: ['kitchen-tools', 'preparation-action'] },
  { label: 'Washing up and dishwasher', families: ['washing', 'dishwasher'] },
  { label: 'Bathroom and personal care', families: ['bathroom', 'dental', 'hygiene'] },
  { label: 'Cleaning products', families: ['cleaning-products', 'cleaning-chemical'] },
  { label: 'Cleaning tools', families: ['cleaning-tools'] },
  { label: 'Sponges, cloths and bags', families: ['cleaning-cloths', 'consumable'] },
  { label: 'Laundry', families: ['laundry'] },
  { label: 'Aquarium', families: ['aquarium'] },
  { label: 'Fishing', families: ['fishing'] },
  { label: 'Gardening', families: ['garden'] },
  { label: 'Harvest', families: ['harvest'] },
  { label: 'Music', families: ['music'] },
  { label: 'Reading and writing', families: ['reading', 'writing'] },
  { label: 'Bedtime', families: ['sleep'] },
  { label: 'Clothes', families: ['wearable'] },
  { label: 'Pockets and accessories', families: ['personal-accessory'] },
  { label: 'Grooming', families: ['grooming'] },
  { label: 'Books and music', families: ['bedroom-leisure', 'leisure'] },
  { label: 'Pet care and play', families: ['pet-care'] },
  { label: 'Exercise and games', families: ['exercise', 'games'] },
  { label: 'Pottery', families: ['pottery'] },
  { label: 'Rest', families: ['rest'] },
  { label: 'Fixing things', families: ['maintenance', 'repair'] },
  { label: 'Pub', families: ['pub'] },
  { label: 'Art', families: ['art'] },
  { label: 'Scientific and inventing', families: ['inventing'] },
]
export const MARKS_GROUP = 'Marks'
export const OTHER_GROUP = 'Other'

/** The library's pictures sorted into the studio's groups (empty groups left out), each group in label order. */
export function groupPictures(lib: Library, kind?: Picture['kind']): { label: string; pictures: [string, Picture][] }[] {
  const groups = new Map<string, [string, Picture][]>([...PICTURE_GROUPS.map((g): [string, [string, Picture][]] => [g.label, []]), [MARKS_GROUP, []], [OTHER_GROUP, []]])
  for (const entry of Object.entries(lib.pictures)) {
    const p = entry[1]
    if (kind && p.kind !== kind) continue
    const label = p.kind === 'mark' ? MARKS_GROUP : (PICTURE_GROUPS.find((g) => g.families.includes(p.family))?.label ?? OTHER_GROUP)
    groups.get(label)!.push(entry)
  }
  return [...groups]
    .filter(([, list]) => list.length)
    .map(([label, list]) => ({ label, pictures: list.sort(([, a], [, b]) => a.label.localeCompare(b.label)) }))
}

/** A step in words, as the studio and the command line show it: “Sausages · flips onto · Barbecue grill”. */
export function describeStep(lib: Library, story: Story, s: Step | undefined): string {
  if (!s) return ''
  if (s.do === 'settle') return 'a quiet moment'
  const v = VERBS[s.do]
  const name = (as?: string) => (as && story.cast[as] ? (lib.pictures[story.cast[as].picture]?.label ?? story.cast[as].picture) : '…')
  return v.needs.includes('onto') ? `${name(s.who)} · ${v.label} · ${name(s.onto)}` : v.needs.includes('who') ? `${name(s.who)} · ${v.label}` : v.label
}

/** “plays once”, “plays twice”, “plays once or twice”, “plays 2–3 times”: how often a story fits a 20–30 s activity. */
export function playsText([lo, hi]: [number, number]): string {
  const n = (k: number) => (k === 1 ? 'once' : k === 2 ? 'twice' : `${k} times`)
  if (lo === hi) return hi === 0 ? 'is longer than the activity' : `plays ${n(hi)}`
  if (hi <= 2) return lo === 0 ? `plays ${n(hi)} at most` : 'plays once or twice'
  return lo === 0 ? `plays up to ${hi} times` : `plays ${lo}–${hi} times`
}

/** Where a picture dragged from the studio's library can land (Frank, 21 Oct: drag and drop instead of long menus). */
export type DropTarget =
  | { to: 'cast'; as?: string }
  | { to: 'step'; index: number }
  | { to: 'props'; index?: number }
  | { to: 'marks'; index?: number }
  /** A cast member's “when it appears” slot. */
  | { to: 'appear'; as: string }

/** Whether a picture of this kind can land there: objects join the cast, act in a step or circle as props; marks go on a step's touches, ride as extra marks or burst as a cast member appears. */
export function canPlace(story: Story, kind: Picture['kind'], target: DropTarget): boolean {
  switch (target.to) {
    case 'cast':
    case 'props':
      return kind === 'object'
    case 'marks':
      return kind === 'mark' && Object.keys(story.cast).length > 0
    case 'appear':
      return kind === 'mark' && !!story.cast[target.as]
    case 'step': {
      const s = story.steps[target.index]
      if (!s) return false
      return VERBS[s.do].needs.includes(kind === 'object' ? 'who' : 'onto')
    }
  }
}

/** A cast member with a new picture: same role and “when it appears” mark, and no pinned version (that belonged to the old picture). */
export function swapPicture(m: CastMember, picture: string): CastMember {
  return { picture, role: m.role, ...(m.appear ? { appear: m.appear } : {}) }
}

/** A fresh cast name from a picture's label: “Sponge (yellow)” becomes sponge, then sponge-2 if that is taken. */
function castName(story: Story, label: string): string {
  const base = (label.toLowerCase().match(/[a-z0-9]+/)?.[0] ?? 'extra').slice(0, 40)
  let name = base
  for (let n = 2; story.cast[name]; n++) name = `${base}-${n}`
  return name
}

/**
 * The story after a picture is dropped on a target, or null if it can't land there.
 * Cast: on a member swaps its picture (keeping its role), elsewhere adds a helper.
 * Step: an object becomes the step's actor (joining the cast if it isn't in it); a mark becomes its touch mark.
 * Props: on a prop swaps its picture, elsewhere adds one circling for the retold part of the story.
 * Extra marks: on one swaps its picture, elsewhere adds one riding on the main picture.
 * When it appears: the mark bursts as that cast member appears.
 */
export function placePicture(story: Story, lib: Library, picture: string, target: DropTarget): Story | null {
  const pic = lib.pictures[picture]
  if (!pic || !canPlace(story, pic.kind, target)) return null
  const lastStep = Math.max(1, story.steps.length - 1)
  switch (target.to) {
    case 'cast': {
      const m = target.as ? story.cast[target.as] : undefined
      if (target.as && m) return { ...story, cast: { ...story.cast, [target.as]: swapPicture(m, picture) } }
      return { ...story, cast: { ...story.cast, [castName(story, pic.label)]: { picture, role: 'support' } } }
    }
    case 'appear':
      return { ...story, cast: { ...story.cast, [target.as]: { ...story.cast[target.as], appear: picture } } }
    case 'step': {
      const steps = [...story.steps]
      const s = steps[target.index]
      if (pic.kind === 'mark') {
        steps[target.index] = { ...s, mark: picture }
        return { ...story, steps }
      }
      const existing = Object.entries(story.cast).find(([, m]) => m.picture === picture)?.[0]
      const who = existing ?? castName(story, pic.label)
      steps[target.index] = { ...s, who }
      return { ...story, cast: existing ? story.cast : { ...story.cast, [who]: { picture, role: 'support' } }, steps }
    }
    case 'props': {
      if (target.index !== undefined && story.props[target.index]) return { ...story, props: story.props.map((p, i) => (i === target.index ? { ...p, picture } : p)) }
      return { ...story, props: [...story.props, { picture, at: 'orbit', fromStep: story.loopFrom ?? 1, toStep: lastStep }] }
    }
    case 'marks': {
      if (target.index !== undefined && story.ambient[target.index]) return { ...story, ambient: story.ambient.map((a, i) => (i === target.index ? { ...a, picture } : a)) }
      const on = Object.entries(story.cast).find(([, m]) => m.role === 'hero')?.[0] ?? Object.keys(story.cast)[0]
      return { ...story, ambient: [...story.ambient, { picture, on, fromStep: 1, toStep: lastStep }] }
    }
  }
}

/** Claude's style review of the library against Tintin-style ligne claire (data/activity-stories/style-review.json). */
export type PictureStyle = 'ligne-claire' | 'close' | 'not-yet'
export interface StyleReview {
  schema: string
  reviewed: string
  by: string
  standard: string
  pictures: Record<string, { version: number; style: PictureStyle; note?: string }>
}

/** The style verdict for a picture's current version; undefined if it was never reviewed or Codex has added a newer version since. */
export function styleOf(review: StyleReview, lib: Library, id: string): StyleReview['pictures'][string] | undefined {
  const r = review.pictures[id]
  return r && lib.pictures[id]?.current === r.version ? r : undefined
}

/** The version of a picture a cast member uses (pinned, or the library's current). */
export function versionFor(lib: Library, picture: string, pinned?: number): PictureVersion | undefined {
  const p = lib.pictures[picture]
  if (!p) return undefined
  const want = pinned ?? p.current
  return p.versions.find((v) => v.v === want) ?? p.versions.find((v) => v.v === p.current)
}
