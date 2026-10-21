/** Shared helpers for the bubble-story picture library (see data/activity-stories/README.md). */

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
export const LIBRARY_FILE = path.join(ROOT, 'data/activity-stories/pictures.json')
export const STORIES_DIR = path.join(ROOT, 'data/activity-stories/stories')
export const PUBLIC_DIR = path.join(ROOT, 'public/activity-stories/pictures')
export const CELL = 256
export const MIN_GUTTER = 16
export const ID = /^[a-z0-9][a-z0-9-]{0,59}$/

const archive = () => JSON.parse(fs.readFileSync(path.join(ROOT, 'review-archive/index.json'), 'utf8')).legacyPaths

/** The file on disk behind a library URL: a pack file under art/drafts/, an archived /keeper-review/ path or a /activity-stories/ file in public/. */
export const REPO_PREFIX = '/activity-stories/repo/'
export function fileFor(url) {
  if (url.startsWith(REPO_PREFIX)) return path.join(ROOT, url.slice(REPO_PREFIX.length))
  if (url.startsWith('/activity-stories/')) return path.join(ROOT, 'public', url)
  const entry = archive()[url]
  return entry ? path.join(ROOT, entry.object) : null
}

export const sha256 = (buf) => crypto.createHash('sha256').update(buf).digest('hex')

/** Measure a picture: cell size, alpha > 8 bounds [x0, y0, x1, y1] and the smallest transparent gutter. */
export function measure(buf) {
  const png = PNG.sync.read(buf)
  let x0 = png.width, y0 = png.height, x1 = -1, y1 = -1
  for (let y = 0; y < png.height; y++)
    for (let x = 0; x < png.width; x++)
      if (png.data[(y * png.width + x) * 4 + 3] > 8) {
        if (x < x0) x0 = x
        if (x > x1) x1 = x
        if (y < y0) y0 = y
        if (y > y1) y1 = y
      }
  if (x1 < 0) return { cell: [png.width, png.height], bounds: null, gutter: 0 }
  const bounds = [x0, y0, x1 + 1, y1 + 1]
  return { cell: [png.width, png.height], bounds, gutter: Math.min(x0, y0, png.width - bounds[2], png.height - bounds[3]) }
}

export const readLibrary = () => JSON.parse(fs.readFileSync(LIBRARY_FILE, 'utf8'))
export const writeLibrary = (lib) => fs.writeFileSync(LIBRARY_FILE, JSON.stringify(lib, null, 2) + '\n')
