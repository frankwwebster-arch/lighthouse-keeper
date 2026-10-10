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
