/**
 * npm run sprites
 *
 * Reads every PNG under art/raw/ (Codex's deliveries), snaps each to the 4 px
 * grid, writes the clean 1x picture to public/sprites/ and rebuilds
 * public/sprites/manifest.json, which the game reads. Prints what it did and
 * anything that does not match the brief (docs/CODEX_BRIEF.md).
 */

import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync } from 'node:fs'
import { basename, join, relative } from 'node:path'
import { PNG } from 'pngjs'
import { snap, type Img } from './pixelsnap.ts'

const RAW = process.env.SPRITES_RAW ?? 'art/raw'
const OUT = process.env.SPRITES_OUT ?? 'public/sprites'

interface Entry {
  file: string
  w: number
  h: number
  frames: number
  fps?: number
  pivot?: [number, number]
}

function pngs(dir: string): string[] {
  if (!existsSync(dir)) return []
  return readdirSync(dir).flatMap((f) => {
    const p = join(dir, f)
    return statSync(p).isDirectory() ? pngs(p) : /\.png$/i.test(f) ? [p] : []
  })
}

const read = (path: string): Img => {
  const png = PNG.sync.read(readFileSync(path))
  return { w: png.width, h: png.height, data: new Uint8Array(png.data) }
}

const write = (path: string, img: Img) => {
  const png = new PNG({ width: img.w, height: img.h })
  png.data = Buffer.from(img.data)
  writeFileSync(path, PNG.sync.write(png))
}

const files = pngs(RAW)
if (!files.length) {
  console.log(`No pictures in ${RAW}/ yet. Put Codex's PNGs there and run again.`)
  process.exit(0)
}
mkdirSync(OUT, { recursive: true })

// Clear out what the last run made, so a renamed or deleted picture does not linger.
const manifestPath = join(OUT, 'manifest.json')
const old = existsSync(manifestPath) ? (JSON.parse(readFileSync(manifestPath, 'utf8')) as Record<string, Entry | string>) : {}
for (const e of Object.values(old)) {
  const f = typeof e === 'string' ? e : e.file
  if (f && existsSync(join(OUT, f))) rmSync(join(OUT, f))
}

const manifest: Record<string, Entry> = {}
let problems = 0
for (const path of files.sort()) {
  const s = snap(basename(path), read(path))
  if (manifest[s.name]) {
    console.log(`!  ${relative(RAW, path)}: a second picture called ${s.name}; skipped`)
    problems++
    continue
  }
  const file = `${s.name}.png`
  write(join(OUT, file), s.img)
  manifest[s.name] = { file, w: s.frameW, h: s.img.h, frames: s.frames, ...(s.fps ? { fps: s.fps } : {}), ...(s.pivot ? { pivot: s.pivot } : {}) }
  const size = `${s.frameW}x${s.img.h}${s.frames > 1 ? ` x${s.frames} @${s.fps}fps` : ''}`
  const scale = s.scale === 1 ? 'already 1x' : `÷${Number.isInteger(s.scale) ? s.scale : s.scale.toFixed(2)}`
  console.log(`${s.warnings.length ? '!' : '✓'}  ${s.name.padEnd(34)} ${size.padEnd(22)} ${scale}`)
  for (const w of s.warnings) console.log(`     ${w}`)
  problems += s.warnings.length ? 1 : 0
}

const sorted = Object.fromEntries(Object.entries(manifest).sort(([a], [b]) => a.localeCompare(b)))
writeFileSync(manifestPath, JSON.stringify(sorted, null, 1) + '\n')
console.log(`\n${Object.keys(manifest).length} pictures ready, ${problems} to look at.`)
