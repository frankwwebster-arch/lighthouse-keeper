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
import { hardAlpha, keyMagenta, parseName, snap, type Img } from './pixelsnap.ts'

const RAW = process.env.SPRITES_RAW ?? 'art/raw'
const OUT = process.env.SPRITES_OUT ?? 'public/sprites'

interface Entry {
  file: string
  w: number
  h: number
  frames: number
  fps?: number
  pivot?: [number, number]
  /** Source pixels per logical pixel; playback w/h remain logical dimensions. */
  density?: number
  anchor?: [number, number]
  keeperUsePoint?: [number, number]
  effectOrigin?: [number, number]
  bubbleOrigin?: [number, number]
  seatPoint?: [number, number]
  handUsePoint?: [number, number]
  loop?: boolean
  reverseFor?: string
  mirrorSafe?: boolean
  facing?: string
  interaction?: string
  mirrorsFor?: string
  z?: number
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
// Validate every new density contract before clearing an existing export.
// A bad delivery must leave the last usable manifest and PNGs intact.
const contracts = new Map<string, Entry>()
for (const path of files) {
  const sidecarPath = path.replace(/\.png$/i, '.json')
  if (!existsSync(sidecarPath)) continue
  const contract = JSON.parse(readFileSync(sidecarPath, 'utf8')) as Entry
  const raw = read(path)
  const parsed = parseName(basename(path))
  const density = contract.density
  if (!Number.isInteger(density) || !density || density < 1 || !Number.isInteger(contract.w) || contract.w < 1 || !Number.isInteger(contract.h) || contract.h < 1 || contract.frames !== parsed.frames || raw.w !== contract.w * parsed.frames * density || raw.h !== contract.h * density || !Number.isFinite(contract.fps ?? 0) || (contract.fps ?? 0) < 0 || (parsed.frames > 1 && !(contract.fps && contract.fps > 0))) {
    throw new Error(`Invalid density/frame contract for ${relative(RAW, path)}`)
  }
  contracts.set(path, contract)
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
  // Optional additive contract for detailed artwork. A 420x140 room still
  // occupies 105x35 logical pixels and renders at the same integer 4x size.
  // Legacy deliveries continue through the unchanged pixel-snap route.
  const contract = contracts.get(path)
  const raw = read(path)
  const parsed = parseName(basename(path))
  const density = contract?.density
  const s = contract
    ? { name: parsed.name, img: hardAlpha(keyMagenta(raw)), frames: parsed.frames, frameW: contract.w, fps: contract.fps ?? 0, scale: 1, warnings: [] as string[], pivot: contract.pivot }
    : snap(basename(path), raw)
  if (manifest[s.name]) {
    console.log(`!  ${relative(RAW, path)}: a second picture called ${s.name}; skipped`)
    problems++
    continue
  }
  const file = `${s.name}.png`
  write(join(OUT, file), s.img)
  manifest[s.name] = { file, w: s.frameW, h: contract?.h ?? s.img.h, frames: s.frames, ...(s.fps ? { fps: s.fps } : {}), ...(s.pivot ? { pivot: s.pivot } : {}), ...(contract ? { density: contract.density, anchor: contract.anchor, keeperUsePoint: contract.keeperUsePoint, effectOrigin: contract.effectOrigin, bubbleOrigin: contract.bubbleOrigin, seatPoint: contract.seatPoint, handUsePoint: contract.handUsePoint, loop: contract.loop, reverseFor: contract.reverseFor, mirrorSafe: contract.mirrorSafe, facing: contract.facing, interaction: contract.interaction, mirrorsFor: contract.mirrorsFor, z: contract.z } : {}) }
  const size = `${s.frameW}x${contract?.h ?? s.img.h}${s.frames > 1 ? ` x${s.frames} @${s.fps}fps` : ''}${contract ? ` density ${density}` : ''}`
  const scale = s.scale === 1 ? 'already 1x' : `÷${Number.isInteger(s.scale) ? s.scale : s.scale.toFixed(2)}`
  console.log(`${s.warnings.length ? '!' : '✓'}  ${s.name.padEnd(34)} ${size.padEnd(22)} ${scale}`)
  for (const w of s.warnings) console.log(`     ${w}`)
  problems += s.warnings.length ? 1 : 0
}

const sorted = Object.fromEntries(Object.entries(manifest).sort(([a], [b]) => a.localeCompare(b)))
writeFileSync(manifestPath, JSON.stringify(sorted, null, 1) + '\n')
console.log(`\n${Object.keys(manifest).length} pictures ready, ${problems} to look at.`)
