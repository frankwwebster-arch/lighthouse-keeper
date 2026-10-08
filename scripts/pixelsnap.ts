/**
 * PIXEL SNAP. Turns whatever Codex hands over (true low-res pixel art, or a
 * big upscaled picture with soft edges) into clean 1x pixel art: one art pixel
 * per real pixel, hard edges, no half-transparent fringes. The game then draws
 * every art pixel as a 4 × 4 block.
 *
 * Sizes and joints follow docs/CODEX_BRIEF.md and docs/PRODUCTION_ASSET_KIT.md.
 * Pure functions over RGBA buffers, so they can be tested without files.
 */

export interface Img {
  w: number
  h: number
  /** RGBA, row by row. */
  data: Uint8Array
}

export const blank = (w: number, h: number): Img => ({ w, h, data: new Uint8Array(w * h * 4) })

const at = (img: Img, x: number, y: number) => (y * img.w + x) * 4

/** Flat #FF00FF magenta (and near it) becomes see-through. */
export function keyMagenta(img: Img): Img {
  const d = img.data
  for (let i = 0; i < d.length; i += 4) {
    if (d[i] > 200 && d[i + 1] < 90 && d[i + 2] > 200) d[i + 3] = 0
  }
  return img
}

/** Every pixel is either solid or gone; gone pixels are zeroed so they compare equal. */
export function hardAlpha(img: Img): Img {
  const d = img.data
  for (let i = 0; i < d.length; i += 4) {
    if (d[i + 3] >= 128) d[i + 3] = 255
    else d[i] = d[i + 1] = d[i + 2] = d[i + 3] = 0
  }
  return img
}

function differ(d: Uint8Array, a: number, b: number): boolean {
  if ((d[a + 3] === 0) !== (d[b + 3] === 0)) return true
  if (d[a + 3] === 0) return false
  return Math.abs(d[a] - d[b]) + Math.abs(d[a + 1] - d[b + 1]) + Math.abs(d[a + 2] - d[b + 2]) > 60
}

/** Where colour changes happen, counted along each axis. */
function edges(img: Img): { xs: number[]; ys: number[] } {
  const xs = new Array(img.w + 1).fill(0)
  const ys = new Array(img.h + 1).fill(0)
  for (let y = 0; y < img.h; y++)
    for (let x = 1; x < img.w; x++) if (differ(img.data, at(img, x - 1, y), at(img, x, y))) xs[x]++
  for (let x = 0; x < img.w; x++)
    for (let y = 1; y < img.h; y++) if (differ(img.data, at(img, x, y - 1), at(img, x, y))) ys[y]++
  return { xs, ys }
}

/** How much of the edge count sits on a grid of this size (best offset). */
function fit(hist: number[], s: number): { score: number; offset: number } {
  let total = 0
  for (const v of hist) total += v
  if (!total) return { score: 1, offset: 0 }
  let best = 0
  let offset = 0
  for (let o = 0; o < s; o++) {
    let hit = 0
    for (let p = 0; p < hist.length; p++) if ((((p - o) % s) + s) % s === 0) hit += hist[p]
    if (hit > best) {
      best = hit
      offset = o
    }
  }
  return { score: best / total, offset }
}

export interface ScaleGuess {
  scale: number
  offsetX: number
  offsetY: number
  /** True when the picture's own edges agree with the grid (clean upscaled art). */
  clean: boolean
}

/**
 * The size of one art pixel in this picture. Clean upscaled art gives itself
 * away: almost every colour change lands on the grid. When several sizes fit,
 * the one giving the expected size wins; with none, the expected size decides.
 */
export function detectScale(img: Img, expect?: { w?: number; h?: number }): ScaleGuess {
  const { xs, ys } = edges(img)
  const fits: ScaleGuess[] = [{ scale: 1, offsetX: 0, offsetY: 0, clean: true }]
  const top = Math.min(64, Math.floor(Math.min(img.w, img.h) / 2))
  for (let s = 2; s <= top; s++) {
    const fx = fit(xs, s)
    const fy = fit(ys, s)
    if (fx.score >= 0.92 && fy.score >= 0.92) fits.push({ scale: s, offsetX: fx.offset, offsetY: fy.offset, clean: true })
  }
  const wanted = expectedScale(img, expect)
  if (!wanted) return fits[fits.length - 1]
  const closest = fits.reduce((a, b) => (Math.abs(b.scale - wanted) < Math.abs(a.scale - wanted) ? b : a))
  // A grid that lands far from the expected size is a coincidence, not the art's grid.
  if (Math.abs(closest.scale - wanted) / wanted < 0.2) return closest
  return { scale: wanted, offsetX: 0, offsetY: 0, clean: false }
}

function expectedScale(img: Img, expect?: { w?: number; h?: number }): number | null {
  if (expect?.h) return img.h / expect.h
  if (expect?.w) return img.w / expect.w
  return null
}

/** One output pixel per cell: the commonest colour in the middle of the cell. */
export function downsample(img: Img, g: ScaleGuess): Img {
  if (g.scale === 1) return img
  const s = g.scale
  const ow = Math.max(1, Math.round((img.w - g.offsetX) / s))
  const oh = Math.max(1, Math.round((img.h - g.offsetY) / s))
  const out = blank(ow, oh)
  const inset = s >= 3 ? s * 0.2 : 0
  for (let cy = 0; cy < oh; cy++) {
    for (let cx = 0; cx < ow; cx++) {
      const x0 = Math.max(0, Math.floor(g.offsetX + cx * s + inset))
      const x1 = Math.min(img.w, Math.max(x0 + 1, Math.ceil(g.offsetX + (cx + 1) * s - inset)))
      const y0 = Math.max(0, Math.floor(g.offsetY + cy * s + inset))
      const y1 = Math.min(img.h, Math.max(y0 + 1, Math.ceil(g.offsetY + (cy + 1) * s - inset)))
      const counts = new Map<number, { n: number; r: number; g: number; b: number; a: number }>()
      for (let y = y0; y < y1; y++)
        for (let x = x0; x < x1; x++) {
          const i = at(img, x, y)
          const d = img.data
          const key = d[i + 3] === 0 ? -1 : ((d[i] >> 3) << 10) | ((d[i + 1] >> 3) << 5) | (d[i + 2] >> 3)
          const c = counts.get(key) ?? { n: 0, r: 0, g: 0, b: 0, a: 0 }
          c.n++
          c.r += d[i]
          c.g += d[i + 1]
          c.b += d[i + 2]
          c.a += d[i + 3]
          counts.set(key, c)
        }
      let best: { n: number; r: number; g: number; b: number; a: number } | null = null
      for (const c of counts.values()) if (!best || c.n > best.n) best = c
      if (!best) continue
      const o = at(out, cx, cy)
      out.data[o] = Math.round(best.r / best.n)
      out.data[o + 1] = Math.round(best.g / best.n)
      out.data[o + 2] = Math.round(best.b / best.n)
      out.data[o + 3] = Math.round(best.a / best.n)
    }
  }
  return out
}

/** The box around the solid pixels (null when the picture is empty). */
export function bbox(img: Img): { x: number; y: number; w: number; h: number } | null {
  let x0 = img.w
  let y0 = img.h
  let x1 = -1
  let y1 = -1
  for (let y = 0; y < img.h; y++)
    for (let x = 0; x < img.w; x++)
      if (img.data[at(img, x, y) + 3]) {
        if (x < x0) x0 = x
        if (x > x1) x1 = x
        if (y < y0) y0 = y
        if (y > y1) y1 = y
      }
  return x1 < 0 ? null : { x: x0, y: y0, w: x1 - x0 + 1, h: y1 - y0 + 1 }
}

/**
 * Where a keeper part turns, from the asset kit (docs/PRODUCTION_ASSET_KIT.md):
 * shoulders, hips, neck, on the shared 32 × 40 canvas. Other pictures do not turn.
 */
const KEEPER_PIVOTS: [RegExp, [number, number]][] = [
  [/_arm_l$/, [10, 15]],
  [/_arm_r$/, [22, 15]],
  [/_leg_l$/, [13, 25]],
  [/_leg_r$/, [19, 25]],
  [/_torso$/, [16, 25]],
  [/_head(_[a-z]+)?$/, [16, 11]],
]

export function pivotFor(name: string): [number, number] | undefined {
  if (!/^keeper_(front|back)_/.test(name)) return undefined
  return KEEPER_PIVOTS.find(([re]) => re.test(name))?.[1]
}

/** Frames a second for strips, from the asset kit; anything else plays at 8. */
const FPS: Record<string, number> = {
  keeper_idle: 6, keeper_walk: 10, keeper_reach_use: 10, keeper_cook_back: 8, keeper_watch_tv: 5, keeper_read: 5,
  keeper_piano: 10, keeper_sleep: 4, keeper_phone: 6, keeper_brush_teeth_back: 8, keeper_wash_back: 8,
  fx_broken_sparks: 12, fx_zzz: 4, bubble_alert: 8, bubble_speech: 6, bubble_thought: 6,
}
export const fpsFor = (name: string, frames: number) => (frames > 1 ? (FPS[name] ?? 8) : 0)

/** `obj_tv_on_f4.png` → name `obj_tv_on`, 4 frames. */
export function parseName(file: string): { name: string; frames: number } {
  const base = file.replace(/\.png$/i, '').toLowerCase()
  const m = base.match(/^(.*)_f(\d+)$/)
  return m ? { name: m[1], frames: Math.max(1, Number(m[2])) } : { name: base, frames: 1 }
}

/** Sizes from docs/CODEX_BRIEF.md (art pixels), used to check deliveries and steady messy pictures. */
const OBJECT_SIZES: Record<string, [number, number]> = {
  door: [13, 24], fridge: [12, 24], cooker: [18, 15], broom: [8, 23], petbowl: [10, 5], toilet: [13, 18],
  tv: [28, 23], bookshelf: [20, 28], piano: [25, 18], bed: [30, 14], phone: [15, 18], basin: [15, 28],
  desk: [25, 20], telescope: [23, 23], lamp: [30, 35], garden: [30, 18], shop: [33, 30], jetty: [55, 15],
}

/**
 * The size the brief asked for, if it fixes one. Keeper parts, stripes and
 * rooms are exact; object sizes are only a guide, so they steady the guess
 * but are not forced.
 */
export function expectedSize(name: string, frames: number): { w?: number; h?: number; exact: boolean } | undefined {
  if (name.startsWith('keeper_')) return { w: 32 * frames, h: 40, exact: true }
  if (name.startsWith('tower_stripe_')) return { w: 110, h: 8, exact: true }
  if (name === 'tower_base' || name === 'tower_lamproom') return { w: 110, h: 35, exact: true }
  if (name === 'tower_roof') return { w: 110, h: 20, exact: true }
  if (name.startsWith('room_')) return { w: 105 * frames, h: 35, exact: true }
  if (name === 'ground_strip') return { w: 300, h: 30, exact: true }
  const m = name.match(/^obj_([a-z]+)_/)
  if (m && OBJECT_SIZES[m[1]]) {
    const [w, h] = OBJECT_SIZES[m[1]]
    return { w: w * frames, h, exact: false }
  }
  return undefined
}

export interface Snapped {
  img: Img
  scale: number
  clean: boolean
  frames: number
  frameW: number
  fps: number
  pivot?: [number, number]
  warnings: string[]
}

/** The whole job for one picture. */
export function snap(file: string, raw: Img): Snapped & { name: string } {
  const { name, frames } = parseName(file)
  const expect = expectedSize(name, frames)
  keyMagenta(raw)
  hardAlpha(raw)
  const guess = detectScale(raw, expect?.exact ? expect : expect ? { h: expect.h } : undefined)
  const img = hardAlpha(downsample(raw, guess))
  const warnings: string[] = []
  if (!guess.clean) warnings.push(`soft edges: resized by ${guess.scale.toFixed(2)} to fit the brief; check it by eye`)
  if (img.w % frames) warnings.push(`width ${img.w} does not split into ${frames} equal frames`)
  if (expect?.exact) {
    if (expect.w && img.w !== expect.w) warnings.push(`width ${img.w}, brief says ${expect.w}`)
    if (expect.h && img.h !== expect.h) warnings.push(`height ${img.h}, brief says ${expect.h}`)
  } else if (expect?.h && Math.abs(img.h - expect.h) / expect.h > 0.35) {
    warnings.push(`height ${img.h}, brief suggests about ${expect.h}`)
  }
  return { name, img, scale: guess.scale, clean: guess.clean, frames, frameW: Math.floor(img.w / frames), fps: fpsFor(name, frames), pivot: pivotFor(name), warnings }
}
