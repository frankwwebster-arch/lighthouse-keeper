/**
 * Where each frame of a sprite strip actually has pixels, so the studio's
 * "is he covered?" check uses the drawing itself, not its transparent canvas.
 * Measured once per sheet in the browser, in logical pixels from his feet.
 */

import type { Bounds } from './recipe'

export interface SheetInfo {
  file: string
  w: number
  h: number
  frames: number
  anchor: [number, number]
  density: number
}

const cache = new Map<string, Promise<(Bounds | null)[]>>()

export function measureSheet(s: SheetInfo): Promise<(Bounds | null)[]> {
  let p = cache.get(s.file)
  if (!p) {
    p = new Promise((resolve) => {
      const img = new Image()
      img.onload = () => {
        const c = document.createElement('canvas')
        c.width = img.naturalWidth
        c.height = img.naturalHeight
        const g = c.getContext('2d', { willReadFrequently: true })
        if (!g) return resolve([])
        g.drawImage(img, 0, 0)
        const data = g.getImageData(0, 0, c.width, c.height).data
        const d = Math.max(1, Math.round(img.naturalWidth / (s.w * s.frames)) || s.density)
        const fw = s.w * d
        const out: (Bounds | null)[] = []
        for (let f = 0; f < s.frames; f++) {
          let x0 = Infinity, x1 = -1, y0 = Infinity, y1 = -1
          for (let y = 0; y < c.height; y++) {
            for (let x = f * fw; x < (f + 1) * fw; x++) {
              if (data[(y * c.width + x) * 4 + 3] > 24) {
                const lx = x - f * fw
                if (lx < x0) x0 = lx
                if (lx > x1) x1 = lx
                if (y < y0) y0 = y
                if (y > y1) y1 = y
              }
            }
          }
          out.push(x1 < 0 ? null : { left: Math.floor(x0 / d) - s.anchor[0], right: Math.ceil((x1 + 1) / d) - s.anchor[0], bottom: s.anchor[1] - Math.ceil((y1 + 1) / d), top: s.anchor[1] - Math.floor(y0 / d) })
        }
        resolve(out)
      }
      img.onerror = () => resolve([])
      img.src = `/sprites/${s.file}`
    })
    cache.set(s.file, p)
  }
  return p
}

// ─── Comparing two frames at a join ──────────────────────────────────────────

interface SheetPixels {
  info: SheetInfo
  /** Source pixels per logical pixel (keeper sheets are drawn at 4×). */
  d: number
  width: number
  data: Uint8ClampedArray
}
const pixelCache = new Map<string, Promise<SheetPixels | null>>()

export function sheetPixels(s: SheetInfo): Promise<SheetPixels | null> {
  let p = pixelCache.get(s.file)
  if (!p) {
    p = new Promise((resolve) => {
      const img = new Image()
      img.onload = () => {
        const c = document.createElement('canvas')
        c.width = img.naturalWidth
        c.height = img.naturalHeight
        const g = c.getContext('2d', { willReadFrequently: true })
        if (!g) return resolve(null)
        g.drawImage(img, 0, 0)
        resolve({ info: s, d: Math.max(1, Math.round(img.naturalWidth / (s.w * s.frames))), width: c.width, data: g.getImageData(0, 0, c.width, c.height).data })
      }
      img.onerror = () => resolve(null)
      img.src = `/sprites/${s.file}`
    })
    pixelCache.set(s.file, p)
  }
  return p
}

/** A frame's opaque pixels as drawn on the stage (feet at x, flipped if mirrored), at quarter-pixel detail. */
function placed(s: SheetPixels, frame: number, x: number, dy: number, mirror: boolean): Map<number, number> {
  const out = new Map<number, number>()
  const { w, h, anchor } = s.info
  const fw = w * s.d
  const block = Math.max(1, Math.round(4 / s.d))
  for (let py = 0; py < h * s.d; py++) {
    for (let px = 0; px < fw; px++) {
      const i = (py * s.width + frame * fw + px) * 4
      if (s.data[i + 3] < 128) continue
      const colour = (s.data[i] << 16) | (s.data[i + 1] << 8) | s.data[i + 2]
      const lx = px / s.d - anchor[0]
      const ly = py / s.d - anchor[1]
      const qx = Math.round((x + (mirror ? -lx - 1 / s.d : lx)) * 4)
      const qy = Math.round((ly - dy) * 4)
      for (let by = 0; by < block; by++) for (let bx = 0; bx < block; bx++) out.set((qy + by) * 100000 + (qx + bx), colour)
    }
  }
  return out
}

/** How much of him changes from one frame to the next across a join: 0 means the same pose exactly. */
export function joinChange(a: SheetPixels, aFrame: number, ax: number, ady: number, amirror: boolean, b: SheetPixels, bFrame: number, bx: number, bdy: number, bmirror: boolean): number {
  const A = placed(a, aFrame, ax, ady, amirror)
  const B = placed(b, bFrame, bx, bdy, bmirror)
  let changed = 0
  for (const [k, c] of A) if (B.get(k) !== c) changed++
  for (const k of B.keys()) if (!A.has(k)) changed++
  return Math.round((100 * changed) / Math.max(1, Math.max(A.size, B.size)))
}
