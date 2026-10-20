/**
 * Turns a bubble story (an ordered list of steps) into frames the bubble can
 * play, for full and reduced motion. Every motion and mark comes from the
 * verb rules here, so a story can be edited step by step and still move the
 * same way, and a replaced picture slots straight in.
 *
 * Space: bubble-local pixels, origin at the bubble's centre (the V2 review
 * pages use the same 360 × 230 box). Objects draw in a 140 px box and marks
 * in a 92 px box, each times its scale, as in V2.
 *
 * Rules that came out of the 20 Oct Activity Cloud Review:
 * - contact marks fire on the frame two silhouettes actually touch, at the
 *   touching edge, and last four frames;
 * - things that stack land and stay; tools do their job and leave;
 * - motion trails show only while something moves fast, and draw beneath
 *   every object;
 * - supports swing in from the outer lanes and reach the middle only on
 *   their own beat;
 * - reduced motion keeps the same steps and the same ending with at most two
 *   objects and one mark, and nothing travels.
 */

import { VERBS, versionFor, type AfterStory, type Library, type Speed, type Step, type Story, type Verb } from './format'

export const FPS = 8
export const BOX = { object: 140, mark: 92 }
export const QUIET_MIN = 5
const CLEAR_FRAMES = 3

export interface FrameItem {
  id: string
  picture: string
  url: string
  kind: 'object' | 'mark'
  x: number
  y: number
  scale: number
  rotation: number
  opacity: number
  z: number
}

export interface Frame {
  step: number
  phase: 'story' | 'quiet' | 'clear'
  bubble: { opacity: number; scale: number }
  items: FrameItem[]
}

export interface Contact {
  frame: number
  step: number
  actor: string
  target: string
  /** Gap between the two silhouettes' boxes at the touch, in px (0 = touching or overlapping). */
  gap: number
}

export interface Issue {
  level: 'error' | 'warn'
  step?: number
  text: string
}

export interface Compiled {
  fps: number
  full: Frame[]
  reduced: Frame[]
  /** Frames that tell the story, before any clearing frames. */
  storyFrames: number
  quiet: [number, number]
  afterStory: AfterStory
  windows: { step: number; start: number; end: number }[]
  contacts: Contact[]
  sfx: { frame: number; cue: string; owner: string; kind: string }[]
  seconds: number
  issues: Issue[]
}

interface Pose {
  x: number
  y: number
  s: number
  r: number
  o: number
  z: number
}

type Status = 'hidden' | 'focus' | 'aside' | 'stacked' | 'gone'

const HOME = { x: 0, y: 18 }
const HEAD = { x: 0, y: 98 }
const ASIDE = { x: -112, y: 46 }
const LANES = [
  { x: -104, y: -22 },
  { x: 104, y: -22 },
  { x: -100, y: 36 },
  { x: 100, y: 36 },
  { x: 0, y: -58 },
]
const SCALE = { hero: 0.78, support: 0.5, result: 0.7, aside: 0.44, mark: 0.42, contact: 0.48, trail: 0.36 }
const APPROACH: Record<Speed, number> = { quick: 3, normal: 4, slow: 6 }
const WORK: Record<Speed, number> = { quick: 4, normal: 6, slow: 9 }
const LAND: Record<Speed, number> = { quick: 3, normal: 4, slow: 6 }
const SOLO: Record<Speed, number> = { quick: 4, normal: 6, slow: 8 }
const EXIT = 2
/** A support first pops up at its own lane, so you see what's coming before it swings in. */
const ENTER = 2
const TOOLS = new Set<Verb>(['strike', 'scrub', 'pour', 'tighten'])
const DEFAULT_MARK: Partial<Record<Verb, string>> = {
  'land-on': 'symbol-impact-star',
  flip: 'symbol-impact-star',
  'drop-in': 'symbol-impact-star',
  strike: 'symbol-impact-star',
  scrub: 'symbol-soap-bubbles',
  pour: 'symbol-water-droplets',
  tighten: 'symbol-impact-star',
  reveal: 'symbol-impact-star',
}

const ease = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2)
const lerp = (a: number, b: number, t: number) => a + (b - a) * t
const bez = (a: number, c: number, b: number, t: number) => (1 - t) * (1 - t) * a + 2 * (1 - t) * t * c + t * t * b
const r2 = (n: number) => Math.round(n * 100) / 100
const sideOf = (x: number) => (x < 0 ? -1 : 1)

const paced = (k: number, pace: number) => Math.max(1, Math.round(k / pace))

/** Frames a step takes at the story's pace. The quiet moment never drops below five frames. */
export function stepFrames(step: Step, pace = 1): number {
  const sp = step.speed ?? 'normal'
  switch (step.do) {
    case 'arrive':
    case 'present':
      return paced(SOLO[sp], pace)
    case 'reveal':
      return Math.max(4, paced(SOLO[sp] + 1, pace))
    case 'settle':
      return Math.max(QUIET_MIN, paced(SOLO[sp], pace))
    default:
      return ENTER + (TOOLS.has(step.do) ? paced(APPROACH[sp], pace) + paced(WORK[sp], pace) + EXIT : paced(APPROACH[sp], pace) + paced(LAND[sp], pace))
  }
}

/** Check a story against the library before (and as well as) compiling it. */
export function checkStory(story: Story, lib: Library): Issue[] {
  const issues: Issue[] = []
  for (const [as, m] of Object.entries(story.cast)) {
    const p = lib.pictures[m.picture]
    if (!p) issues.push({ level: 'error', text: `${as}: the library has no picture called ${m.picture}` })
    else if (p.kind !== 'object') issues.push({ level: 'error', text: `${as}: ${m.picture} is a mark, not an object` })
    else if (m.version && !p.versions.some((v) => v.v === m.version)) issues.push({ level: 'warn', text: `${as}: version ${m.version} of ${m.picture} doesn't exist, so the current one is used` })
  }
  const status: Record<string, Status> = Object.fromEntries(Object.keys(story.cast).map((k) => [k, 'hidden']))
  story.steps.forEach((s, i) => {
    const n = i + 1
    const needs = VERBS[s.do].needs
    for (const key of needs) {
      const who = s[key]
      if (!who) issues.push({ level: 'error', step: n, text: `Step ${n} needs ${key === 'who' ? 'someone to act' : 'something to act on'}` })
      else if (!story.cast[who]) issues.push({ level: 'error', step: n, text: `Step ${n}: ${who} isn’t in the cast` })
    }
    if (s.who && s.onto && s.who === s.onto) issues.push({ level: 'error', step: n, text: `Step ${n}: ${s.who} can’t act on itself` })
    if (s.onto && status[s.onto] && (status[s.onto] === 'hidden' || status[s.onto] === 'gone')) issues.push({ level: 'error', step: n, text: `Step ${n}: ${s.onto} isn’t on show yet` })
    if (s.who && status[s.who] === 'gone') issues.push({ level: 'error', step: n, text: `Step ${n}: ${s.who} has already been used up` })
    if (s.mark && lib.pictures[s.mark]?.kind !== 'mark') issues.push({ level: 'error', step: n, text: `Step ${n}: ${s.mark} isn’t a mark` })
    // Track who is on show, the same way compile does.
    if (!s.who || !status[s.who]) return
    if (s.do === 'arrive' || s.do === 'present') {
      for (const k of Object.keys(status)) if (status[k] === 'focus') status[k] = 'aside'
      status[s.who] = 'focus'
    } else if (s.do === 'drop-in' || TOOLS.has(s.do)) status[s.who] = 'gone'
    else if (s.do === 'reveal') {
      status[s.who] = s.replace ? 'focus' : 'stacked'
      if (s.replace && s.onto) status[s.onto] = 'gone'
      for (const k of Object.keys(status)) if (k !== s.who && status[k] === 'stacked') status[k] = 'gone'
    } else status[s.who] = 'stacked'
  })
  if (story.steps[0]?.do !== 'arrive') issues.push({ level: 'warn', step: 1, text: 'The first step is usually something arriving' })
  for (const a of story.ambient) {
    if (!story.cast[a.on]) issues.push({ level: 'error', text: `Extra mark ${a.picture} sits on ${a.on}, which isn’t in the cast` })
    if (lib.pictures[a.picture]?.kind !== 'mark') issues.push({ level: 'error', text: `Extra mark ${a.picture} isn’t a mark` })
    if (a.fromStep < 1 || a.toStep > story.steps.length + 1 || a.toStep < a.fromStep) issues.push({ level: 'warn', text: `Extra mark ${a.picture}: steps ${a.fromStep}–${a.toStep} don’t fit the story` })
  }
  return issues
}

export function compileStory(input: Story, lib: Library): Compiled {
  const issues = checkStory(input, lib)
  const story: Story = { ...input, steps: [...input.steps] }
  if (story.steps.at(-1)?.do !== 'settle') {
    story.steps.push({ do: 'settle' })
    issues.push({ level: 'warn', text: 'A quiet moment was added at the end' })
  }
  const pace = story.pace || 1
  const members = Object.keys(story.cast)
  const url = (as: string) => versionFor(lib, story.cast[as].picture, story.cast[as].version)?.url ?? ''
  const markUrl = (pic: string) => versionFor(lib, pic)?.url ?? ''
  /** Half width and height of a picture's visible pixels at scale s. */
  const half = (pic: string, s: number, box: number, pinned?: number) => {
    const v = versionFor(lib, pic, pinned)
    const [cw, ch] = v?.cell ?? [256, 256]
    const [x0, y0, x1, y1] = v?.bounds ?? [20, 20, 236, 236]
    return { w: ((x1 - x0) / cw) * box * s * 0.5, h: ((y1 - y0) / ch) * box * s * 0.5 }
  }
  const ext = (as: string, s: number) => half(story.cast[as]?.picture ?? '', s, BOX.object, story.cast[as]?.version)

  // Per-frame poses of every cast member, filled step by step.
  const poses: Record<string, (Pose | null)[]> = Object.fromEntries(members.map((m) => [m, []]))
  const status: Record<string, Status> = Object.fromEntries(members.map((m) => [m, 'hidden']))
  const last: Record<string, Pose | null> = Object.fromEntries(members.map((m) => [m, null]))
  const stacks: Record<string, string[]> = Object.fromEntries(members.map((m) => [m, []]))
  const lanes: Record<string, { x: number; y: number }> = {}
  const pulse: Record<string, Record<number, number>> = Object.fromEntries(members.map((m) => [m, {}]))
  const marks: { id: string; picture: string; frames: Record<number, { x: number; y: number; s: number; r: number; o: number }> }[] = []
  const contacts: Contact[] = []
  const windows: Compiled['windows'] = []
  const firstContact: Record<number, number> = {}
  let frame = 0
  let laneNext = 0

  const laneFor = (as: string) => (lanes[as] ??= LANES[laneNext++ % LANES.length])
  const baseScale = (as: string) => (story.cast[as].role === 'hero' ? SCALE.hero : story.cast[as].role === 'result' ? SCALE.result : SCALE.support)
  const set = (as: string, f: number, p: Pose | null) => {
    poses[as][f] = p
    last[as] = p
  }
  const zFor = (as: string) => (status[as] === 'focus' ? 4 : status[as] === 'aside' ? 3 : status[as] === 'stacked' ? 5 + stacks[stackOwner(as)]?.indexOf(as) : 10)
  const stackOwner = (as: string) => members.find((m) => stacks[m].includes(as)) ?? as
  const stackTop = (target: string, add: string) => {
    const t = last[target]!
    const th = ext(target, t.s).h
    const height = stacks[target].reduce((sum, m) => sum + ext(m, baseScale(m)).h * 0.7, 0)
    return { x: t.x, y: t.y - th * 0.55 - ext(add, baseScale(add)).h * 0.5 - height }
  }
  let stepEnd = 0
  /** A touch: a four-frame mark at the touching edge, a small bump on the target, and a record to measure later. Marks never spill into the next step. */
  const touch = (n: number, f: number, actor: string, target: string, at: { x: number; y: number }, pic: string, s = SCALE.contact, measure = true) => {
    const id = `contact-${n}-${marks.length}`
    const r = ((n * 37 + marks.length * 23) % 31) - 15
    const life = [{ s: s * 1.15, o: 1 }, { s, o: 1 }, { s: s * 0.92, o: 0.6 }, { s: s * 0.85, o: 0.25 }]
    marks.push({ id, picture: pic, frames: Object.fromEntries(life.flatMap((l, i) => (f + i < stepEnd ? [[f + i, { ...at, s: l.s, r, o: l.o }]] : []))) })
    pulse[target][f] = 1.05
    if (measure) contacts.push({ frame: f, step: n, actor, target, gap: 0 })
    firstContact[n] ??= f
  }
  /**
   * Pop up at its lane (or wind up where it is) for ENTER frames, then swing in
   * to `to`. Frames f0 .. f0 + ENTER + k - 1; the last one is the touch.
   */
  const approach = (as: string, start: number, k: number, to: { x: number; y: number }, s: number, opts: { high?: boolean; spin?: number } = {}) => {
    const lane = laneFor(as)
    const was = last[as]
    const away = sideOf(lane.x)
    for (let i = 0; i < ENTER; i++) {
      const at = was && was.o > 0.5 ? { x: was.x + away * 4 * (i + 1), y: was.y - 3 * (i + 1) } : lane
      set(as, start + i, { x: at.x, y: at.y, s: s * (was && was.o > 0.5 ? 1 : i === 0 ? 0.6 : 1.08), r: away * 8 * (i + 1), o: was && was.o > 0.5 ? 1 : i === 0 ? 0.6 : 1, z: 10 })
    }
    const f0 = start + ENTER
    const from = last[as]!
    const ctrl = opts.high ? { x: (from.x + to.x) / 2, y: Math.min(from.y, to.y) - 70 } : { x: from.x * 0.7 + to.x * 0.3, y: Math.min(from.y, to.y) - 26 }
    for (let i = 0; i < k; i++) {
      const t = ease((i + 1) / k)
      set(as, f0 + i, {
        x: bez(from.x, ctrl.x, to.x, t),
        y: bez(from.y, ctrl.y, to.y, t),
        s: lerp(from.s, s, Math.min(1, t * 1.4)),
        r: opts.spin ? opts.spin * (1 - t) : lerp(from.r, 0, t),
        o: Math.min(1, from.o + (i + 1) * 0.5),
        z: 10,
      })
    }
  }
  const leave = (as: string, f0: number) => {
    const p = last[as]!
    const lane = laneFor(as)
    for (let i = 0; i < EXIT; i++) {
      const t = (i + 1) / EXIT
      set(as, f0 + i, { ...p, x: lerp(p.x, lane.x, t * 0.4), y: lerp(p.y, lane.y, t * 0.4) - 6 * t, s: p.s * (1 - 0.2 * t), o: 1 - t, z: 10 })
    }
    status[as] = 'gone'
  }

  story.steps.forEach((step, idx) => {
    const n = idx + 1
    const total = stepFrames(step, pace)
    const f0 = frame
    stepEnd = f0 + total
    const sp = step.speed ?? 'normal'
    const scaleK = (k: number) => paced(k, pace)
    const who = step.who && story.cast[step.who] ? step.who : undefined
    const onto = step.onto && story.cast[step.onto] && last[step.onto] ? step.onto : undefined
    const mark = step.mark ?? DEFAULT_MARK[step.do] ?? 'symbol-impact-star'
    // Moves that bring a support in start after its ENTER frames.
    const g = f0 + ENTER, rest = total - ENTER
    windows.push({ step: n, start: f0, end: f0 + total })
    const playable = who && (VERBS[step.do].needs.includes('onto') ? !!onto : true) && status[who] !== 'gone'

    if (step.do === 'settle' || !playable) {
      // Nothing moves.
    } else if (step.do === 'arrive' || step.do === 'present') {
      const prev = members.find((m) => status[m] === 'focus' && m !== who)
      const s = story.cast[who].role === 'support' ? SCALE.hero * 0.9 : baseScale(who)
      for (let i = 0; i < total; i++) {
        const t = ease((i + 1) / total)
        const from = last[who] ?? { ...HEAD, s: s * 0.3, r: 0, o: 0, z: 4 }
        const pop = i === total - 2 ? 1.12 : 1
        set(who, f0 + i, { x: lerp(from.x, HOME.x, t), y: lerp(from.y, HOME.y, t), s: lerp(from.s, s, t) * pop, r: 0, o: Math.min(1, from.o + 0.5), z: 4 })
        if (prev && last[prev]) {
          const p = last[prev]!
          set(prev, f0 + i, { ...p, x: lerp(p.x, ASIDE.x, t), y: lerp(p.y, ASIDE.y, t), s: lerp(p.s, SCALE.aside, t), z: 3 })
        }
      }
      if (prev) status[prev] = 'aside'
      status[who] = 'focus'
    } else if (step.do === 'land-on' || step.do === 'flip') {
      const k = scaleK(APPROACH[sp])
      const s = baseScale(who)
      const to = stackTop(onto!, who)
      approach(who, f0, k, to, s, step.do === 'flip' ? { high: true, spin: 360 * -sideOf(laneFor(who).x) } : {})
      const e = ext(who, s)
      touch(n, g + k - 1, who, onto!, { x: to.x + sideOf(laneFor(who).x) * e.w * 0.7, y: to.y + e.h * 0.6 }, mark)
      for (let i = k; i < rest; i++) {
        const w = (i - k + 1) / (rest - k)
        set(who, g + i, { x: to.x, y: to.y, s: s * (i === k ? 0.94 : 1), r: 6 * Math.sin(w * Math.PI * 2) * (1 - w), o: 1, z: 10 })
      }
      stacks[onto!].push(who)
      status[who] = 'stacked'
    } else if (step.do === 'drop-in') {
      const k = scaleK(APPROACH[sp])
      const s = baseScale(who)
      const t = last[onto!]!
      const top = t.y - ext(onto!, t.s).h * 0.6
      const to = { x: t.x, y: top - ext(who, s).h * 0.4 }
      approach(who, f0, k, to, s)
      touch(n, g + k - 1, who, onto!, { x: t.x + sideOf(laneFor(who).x) * ext(onto!, t.s).w * 0.45, y: top }, mark)
      for (let i = k; i < rest; i++) {
        const w = (i - k + 1) / (rest - k)
        set(who, g + i, { x: to.x, y: lerp(to.y, t.y - 4, w), s: s * (1 - 0.55 * w), r: 0, o: Math.max(0, 1 - w * 1.6), z: 3 })
      }
      status[who] = 'gone'
    } else if (TOOLS.has(step.do)) {
      const k = scaleK(APPROACH[sp])
      const work = scaleK(WORK[sp])
      const s = baseScale(who)
      const t = last[onto!]!
      const et = ext(onto!, t.s), ea = ext(who, s)
      const side = sideOf(laneFor(who).x)
      if (step.do === 'strike') {
        const to = { x: t.x + side * (et.w * 0.6 + ea.w * 0.45), y: t.y - et.h * 0.35 }
        approach(who, f0, k, to, s)
        const hits = sp === 'quick' ? 2 : 3
        const every = Math.max(2, Math.floor(work / hits))
        const hitAt = new Set([k - 1, ...Array.from({ length: hits - 1 }, (_, h) => k - 1 + every * (h + 1))].filter((h) => h < k + work))
        for (const h of hitAt) touch(n, g + h, who, onto!, { x: t.x + side * et.w * 0.55, y: to.y + ea.h * 0.2 }, mark)
        for (let i = k; i < k + work; i++) set(who, g + i, { x: to.x + (hitAt.has(i) ? -side * 4 : 0), y: to.y, s, r: hitAt.has(i) ? -side * 18 : side * 28, o: 1, z: 10 })
        poses[who][g + k - 1] = { ...poses[who][g + k - 1]!, r: -side * 18 }
      } else if (step.do === 'scrub') {
        const to = { x: t.x, y: t.y - et.h * 0.15 }
        approach(who, f0, k, to, s)
        touch(n, g + k - 1, who, onto!, { x: to.x, y: to.y + ea.h * 0.7 }, mark, SCALE.mark)
        // Back and forth, one stroke every frame; a soap mark at each end of a stroke.
        const amp = et.w * 0.45
        for (let i = k; i < k + work; i++) {
          const swing = Math.round(Math.sin(((i - k + 1) * Math.PI) / 2))
          const x = to.x + amp * swing
          set(who, g + i, { x, y: to.y, s, r: 9 * swing, o: 1, z: 10 })
          if (swing !== 0) touch(n, g + i, who, onto!, { x: x + swing * ea.w * 0.5, y: to.y + ea.h * 0.6 }, mark, SCALE.mark)
        }
      } else if (step.do === 'pour') {
        const to = { x: t.x + side * ea.w * 0.5, y: t.y - et.h - ea.h * 0.35 }
        approach(who, f0, k, to, s)
        for (let i = k; i < k + work; i++) set(who, g + i, { x: to.x, y: to.y, s, r: -side * 70 * Math.min(1, (i - k + 1) / 2), o: 1, z: 10 })
        const spout = { x: to.x - side * ea.w * 0.9, y: to.y + ea.h * 0.1 }
        const land = t.y - et.h * 0.5
        for (let d = 0; d < 2; d++) {
          const start = g + k + 1 + d * 3
          if (start + 2 >= g + k + work + EXIT) break
          const id = `drip-${n}-${d}`
          const frames: (typeof marks)[number]['frames'] = {}
          for (let j = 0; j < 2; j++) frames[start + j] = { x: lerp(spout.x, t.x, (j + 1) / 3), y: lerp(spout.y, land, (j + 1) / 3), s: SCALE.mark * 0.8, r: 0, o: 1 }
          marks.push({ id, picture: mark, frames })
          touch(n, start + 2, who, onto!, { x: t.x - side * 4, y: land }, mark, SCALE.mark, false)
        }
      } else {
        const to = { x: t.x + side * et.w * 0.5, y: t.y - et.h * 0.1 }
        approach(who, f0, k, to, s)
        for (let i = k; i < k + work; i++) {
          const turn = Math.floor((i - k) / 2)
          set(who, g + i, { x: to.x, y: to.y, s, r: side * 40 * Math.min(3, turn + 1), o: 1, z: 10 })
          if ((i - k) % 2 === 0) touch(n, g + i, who, onto!, { x: to.x - side * ea.w * 0.4, y: to.y - ea.h * 0.6 }, mark, SCALE.mark)
        }
      }
      const tail = g + k + work
      leave(who, tail)
    } else if (step.do === 'reveal') {
      const t = last[onto!]!
      const used = stacks[onto!].filter((m) => m !== who)
      const replace = !!step.replace
      const s = baseScale(who)
      stacks[onto!] = []
      const to = replace ? { x: HOME.x, y: HOME.y } : stackTop(onto!, who)
      for (let i = 0; i < total; i++) {
        const w = Math.min(1, (i + 1) / 3)
        for (const m of used) {
          const p = last[m]
          if (p) set(m, f0 + i, { ...p, x: lerp(p.x, t.x, w), y: lerp(p.y, t.y, w), s: p.s * (1 - 0.15 * w), o: Math.max(0, 1 - w), z: p.z })
        }
        if (replace) set(onto!, f0 + i, { ...t, s: t.s * (1 - 0.3 * w), o: Math.max(0, 1 - w) })
        const pop = i === 0 ? 0 : i === 1 ? 0.45 : i === 2 ? 1.15 : 1
        set(who, f0 + i, { x: to.x, y: to.y, s: s * pop, r: 0, o: i === 0 ? 0 : 1, z: replace ? 4 : 6 })
      }
      for (const m of used) status[m] = 'gone'
      if (replace) {
        status[onto!] = 'gone'
        status[who] = 'focus'
      } else {
        stacks[onto!].push(who)
        status[who] = 'stacked'
      }
      touch(n, f0 + 1, who, onto!, { x: to.x + ext(who, s).w * 0.6, y: to.y - ext(who, s).h * 0.5 }, mark, 0.5)
    }

    // Everyone not moved this step holds still.
    for (const m of members) for (let i = 0; i < total; i++) if (poses[m][f0 + i] === undefined) poses[m][f0 + i] = last[m] && last[m]!.o > 0 ? { ...last[m]!, z: zFor(m) } : null
    frame += total
  })

  const storyFrames = frame
  // Measure every touch now that all poses are known.
  for (const c of contacts) {
    const a = poses[c.actor][c.frame], b = poses[c.target][c.frame]
    if (!a || !b) {
      c.gap = 999
      continue
    }
    const ea = ext(c.actor, a.s), eb = ext(c.target, b.s)
    c.gap = r2(Math.max(0, Math.abs(a.x - b.x) - (ea.w + eb.w), Math.abs(a.y - b.y) - (ea.h + eb.h)))
  }
  const quietStep = story.steps.length
  const quiet: [number, number] = [windows[quietStep - 1].start, storyFrames - 1]
  const clear = story.afterStory === 'hold' ? 0 : CLEAR_FRAMES
  const totalFrames = storyFrames + clear

  // Extra marks that ride on a cast member (heat curls over the grill).
  const ambient = story.ambient.flatMap((a, i) => {
    const from = windows[a.fromStep - 1]?.start
    const to = windows[Math.min(a.toStep, windows.length) - 1]?.end
    if (from === undefined || to === undefined || !story.cast[a.on]) return []
    return [{ id: `extra-${i}`, picture: a.picture, on: a.on, from, to }]
  })

  const objectItems = (f: number): FrameItem[] =>
    members.flatMap((m) => {
      const p = poses[m][Math.min(f, storyFrames - 1)]
      if (!p || p.o <= 0) return []
      const fade = f >= storyFrames ? 1 - (f - storyFrames + 1) / (CLEAR_FRAMES + 0) : 1
      return [{ id: m, picture: story.cast[m].picture, url: url(m), kind: 'object' as const, x: r2(p.x), y: r2(p.y), scale: r2(p.s * (pulse[m][f] ?? 1)), rotation: r2(p.r), opacity: r2(Math.max(0, p.o * fade)), z: p.z }]
    }).filter((i) => i.opacity > 0)

  const full: Frame[] = []
  for (let f = 0; f < totalFrames; f++) {
    const items = objectItems(f)
    if (f < storyFrames) {
      for (const mk of marks) {
        const st = mk.frames[f]
        if (st && st.o > 0) items.push({ id: mk.id, picture: mk.picture, url: markUrl(mk.picture), kind: 'mark', x: r2(st.x), y: r2(st.y), scale: r2(st.s), rotation: st.r, opacity: st.o, z: 20 })
      }
      for (const a of ambient) {
        const p = poses[a.on][f]
        if (!p || p.o < 0.5 || f < a.from || f >= a.to) continue
        const h = ext(a.on, p.s).h
        const fadeIn = Math.min(1, (f - a.from + 1) / 2), fadeOut = Math.min(1, (a.to - f) / 2)
        items.push({ id: a.id, picture: a.picture, url: markUrl(a.picture), kind: 'mark', x: r2(p.x + 4 * Math.sin(f * 0.8)), y: r2(p.y - h - 14 - (f % 8) * 1.2), scale: SCALE.mark, rotation: r2(6 * Math.sin(f * 0.6)), opacity: r2(Math.min(fadeIn, fadeOut)), z: 15 })
      }
      // Motion trails: only while something moves fast, always beneath the objects.
      for (const m of members) {
        const a = poses[m][f], b = f > 0 ? poses[m][f - 1] : null
        if (!a || !b || a.o < 0.5) continue
        const vx = a.x - b.x, vy = a.y - b.y, v = Math.hypot(vx, vy)
        if (v <= 6) continue
        const e = ext(m, a.s)
        items.push({ id: `trail-${m}`, picture: 'symbol-motion-ticks', url: markUrl('symbol-motion-ticks'), kind: 'mark', x: r2(a.x - (vx / v) * (e.w + 8)), y: r2(a.y - (vy / v) * (e.h * 0.6 + 6)), scale: r2(SCALE.trail + Math.min(0.15, v / 120)), rotation: r2((Math.atan2(vy, vx) * 180) / Math.PI), opacity: r2(Math.min(1, 0.5 + (v - 6) / 12)), z: 2 })
      }
    }
    const step = windows.find((w) => f >= w.start && f < w.end)?.step ?? quietStep
    const inflate = f === 0 ? 0.7 : f === 1 ? 1.05 : 1
    const bubbleOut = story.afterStory === 'hide' && f >= storyFrames ? 1 - (f - storyFrames + 1) / CLEAR_FRAMES : 1
    full.push({ step, phase: f >= storyFrames ? 'clear' : f >= quiet[0] ? 'quiet' : 'story', bubble: { opacity: r2((f === 0 ? 0.5 : 1) * bubbleOut), scale: inflate }, items: items.sort((x, y) => x.z - y.z) })
  }

  // Reduced motion: the same steps and ending, two objects at most, one mark, nothing travels.
  const reduced: Frame[] = []
  let pair: string[] = []
  for (const w of windows) {
    const s = story.steps[w.step - 1]
    const atTouch = TOOLS.has(s.do) || s.do === 'drop-in'
    const key = s.do === 'settle' ? w.start - 1 : atTouch ? (firstContact[w.step] ?? w.end - 1) : w.end - 1
    const keyFrame = Math.max(0, key)
    const next = s.do === 'settle' ? pair : s.do === 'arrive' || s.do === 'present' || (s.do === 'reveal' && s.replace) ? [s.who] : [s.onto, s.who]
    const shown = next.filter((m, i, l): m is string => !!m && !!story.cast[m] && l.indexOf(m) === i && (poses[m][keyFrame]?.o ?? 0) > 0.5).slice(-2)
    const c = contacts.find((x) => x.step === w.step)
    const cm = c ? marks.find((mk) => mk.frames[c.frame] && mk.id.startsWith(`contact-${w.step}-`)) : undefined
    for (let f = w.start; f < w.end; f++) {
      const items: FrameItem[] = shown.map((m) => {
        let p = poses[m][keyFrame]!
        // Only two pictures show, so a filling sits straight on its target, not on hidden layers.
        if ((s.do === 'land-on' || s.do === 'flip') && m === s.who && s.onto && poses[s.onto][keyFrame]) {
          const t = poses[s.onto][keyFrame]!
          p = { ...p, x: t.x, y: t.y - ext(s.onto, t.s).h * 0.55 - ext(m, p.s).h * 0.5 }
        }
        const fresh = !pair.includes(m) && f - w.start < 2
        return { id: m, picture: story.cast[m].picture, url: url(m), kind: 'object' as const, x: r2(p.x), y: r2(p.y), scale: r2(p.s), rotation: 0, opacity: fresh ? 0.5 + 0.25 * (f - w.start) : 1, z: p.z }
      })
      if (cm && c && f >= c.frame && f <= Math.min(w.end - 1, c.frame + 3)) {
        const st = cm.frames[c.frame + 1] ?? cm.frames[c.frame]
        items.push({ id: cm.id, picture: cm.picture, url: markUrl(cm.picture), kind: 'mark', x: r2(st.x), y: r2(st.y), scale: r2(st.s), rotation: 0, opacity: 1, z: 20 })
      }
      reduced.push({ step: w.step, phase: f >= quiet[0] ? 'quiet' : 'story', bubble: { opacity: 1, scale: 1 }, items: items.sort((x, y) => x.z - y.z) })
    }
    pair = shown
  }
  for (let f = storyFrames; f < totalFrames; f++) {
    const fade = 1 - (f - storyFrames + 1) / CLEAR_FRAMES
    const lastFrame = reduced[storyFrames - 1]
    reduced.push({ ...lastFrame, phase: 'clear', bubble: { opacity: story.afterStory === 'hide' ? r2(fade) : 1, scale: 1 }, items: lastFrame.items.filter((i) => i.kind === 'object').map((i) => ({ ...i, opacity: r2(i.opacity * fade) })) })
  }

  const sfx = story.sfx.flatMap((c) => {
    const w = windows[c.step - 1]
    if (!w) return []
    const at = c.at === 'start' ? w.start : c.at === 'end' ? w.end - 1 : (firstContact[c.step] ?? w.start)
    return [{ frame: at, cue: c.cue, owner: c.owner, kind: c.kind }]
  })

  const seconds = storyFrames / FPS
  if (seconds < 5) issues.push({ level: 'warn', text: `The story lasts ${seconds.toFixed(1)} s; aim for 5–10 s` })
  if (seconds > 10) issues.push({ level: 'warn', text: `The story lasts ${seconds.toFixed(1)} s; aim for 5–10 s` })
  const crowd = Math.max(...full.map((fr) => fr.items.filter((i) => i.kind === 'object').length))
  if (crowd > 5) issues.push({ level: 'warn', text: `${crowd} pictures are on show at once; five is plenty` })

  return { fps: FPS, full, reduced, storyFrames, quiet, afterStory: story.afterStory, windows, contacts, sfx, seconds, issues }
}
