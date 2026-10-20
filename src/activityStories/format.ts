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
export type Verb = 'arrive' | 'present' | 'land-on' | 'flip' | 'drop-in' | 'strike' | 'scrub' | 'pour' | 'tighten' | 'reveal' | 'settle'

export interface CastMember {
  picture: string
  role: CastRole
  /** Pin an older picture version (Frank's one-tap undo). Absent = follow the library's current version. */
  version?: number
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
  /** reveal only: the result takes the target's place instead of sitting on it. */
  replace?: boolean
}

export interface Ambient {
  picture: string
  on: string
  /** First and last step (1-based) it shows during. */
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
  cast: Record<string, CastMember>
  steps: Step[]
  ambient: Ambient[]
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
  'land-on': { label: 'lands on', needs: ['who', 'onto'], hint: 'Swings in and stays stacked on top.' },
  flip: { label: 'flips onto', needs: ['who', 'onto'], hint: 'Somersaults in and stays on top.' },
  'drop-in': { label: 'drops into', needs: ['who', 'onto'], hint: 'Falls in and disappears inside.' },
  strike: { label: 'strikes', needs: ['who', 'onto'], hint: 'Hits it two or three times, then leaves.' },
  scrub: { label: 'scrubs', needs: ['who', 'onto'], hint: 'Rubs back and forth across it, then leaves.' },
  pour: { label: 'pours onto', needs: ['who', 'onto'], hint: 'Tips over it so drops fall, then leaves.' },
  tighten: { label: 'tightens', needs: ['who', 'onto'], hint: 'Turns in place on its edge, then leaves.' },
  reveal: { label: 'appears from', needs: ['who', 'onto'], hint: 'Bursts out; anything stacked on it is used up.' },
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
      cast[as] = { picture: m.picture, role, ...(Number.isInteger(m.version) && (m.version as number) > 0 ? { version: m.version as number } : {}) }
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
    cast,
    steps,
    ambient,
    sfx,
    ...(typeof raw.notes === 'string' && raw.notes ? { notes: raw.notes } : {}),
  }
}

/** The version of a picture a cast member uses (pinned, or the library's current). */
export function versionFor(lib: Library, picture: string, pinned?: number): PictureVersion | undefined {
  const p = lib.pictures[picture]
  if (!p) return undefined
  const want = pinned ?? p.current
  return p.versions.find((v) => v.v === want) ?? p.versions.find((v) => v.v === p.current)
}
