import { createContext, useContext, useEffect, useId, useState, type ReactNode } from 'react'
import { fpsFor, type FpsOverrides } from '../game/animFps'
import { loadAnimFps } from '../game/remote'

/**
 * Sprites from Codex drop into `art/raw/`; `npm run sprites` snaps them to the
 * grid, writes them to `public/sprites/` and lists them in
 * `public/sprites/manifest.json`:
 *   { "obj_tv_on": { "file": "obj_tv_on.png", "w": 28, "h": 23, "frames": 4, "fps": 8 } }
 * `w`,`h` are one frame in logical pixels, drawn at PX real units each (the
 * asset kit's 4×). An entry without them, or a plain string, is fitted to the
 * vector drawing's box as before.
 * Anything not listed is drawn as a vector, so the game always works.
 * The grown-ups can change any animation's speed while playing (src/game/animFps.ts).
 * (docs/CODEX_ASSETS.md has the full list of names.)
 */
export const PX = 4
export type ManifestEntry = string | { file: string; frames?: number; fps?: number; w?: number; h?: number; effectOrigin?: [number, number]; loop?: boolean }
type Manifest = Record<string, ManifestEntry>
const Ctx = createContext<Manifest>({})
const Speeds = createContext<{ fps: FpsOverrides; setFps: (next: FpsOverrides) => void }>({ fps: {}, setFps: () => undefined })

/** The grown-ups' animation speeds, and a way to change them (the change shows at once; saving is the caller's). */
export const useAnimSpeeds = () => useContext(Speeds)

/** The pictures Codex has delivered so far, by name. */
export const useSprites = () => useContext(Ctx)

export function SpriteProvider({ children }: { children: ReactNode }) {
  const [m, setM] = useState<Manifest>({})
  const [fps, setFps] = useState<FpsOverrides>({})
  useEffect(() => {
    let alive = true
    void loadAnimFps().then((f) => alive && setFps(f))
    fetch('/sprites/manifest.json')
      .then((r) => (r.ok ? r.json() : {}))
      .then((j) => alive && typeof j === 'object' && j && setM(j as Manifest))
      .catch(() => undefined)
    return () => {
      alive = false
    }
  }, [])
  return (
    <Ctx.Provider value={m}>
      <Speeds.Provider value={{ fps, setFps }}>{children}</Speeds.Provider>
    </Ctx.Provider>
  )
}

/**
 * An SVG animation counts from when the page loaded, so one added later (a new
 * clip, or a changed speed) would start part-way through, and a play-once clip
 * would already be over. Each one starts when it appears instead. (Kept outside
 * the component so React calls it once per new animation, not every frame.)
 */
const startNow = (el: SVGAnimateTransformElement | null) => el?.beginElement?.()

/** A picture if we have one, otherwise the vector drawing. `x,y` is the bottom-centre. */
export function Sprite({ name, x = 0, y = 0, w, h, children }: { name: string | readonly string[]; x?: number; y?: number; w: number; h: number; children: ReactNode }) {
  const manifest = useContext(Ctx)
  const speeds = useContext(Speeds).fps
  const clipId = `sprite-${useId().replaceAll(':', '')}`
  const names = typeof name === 'string' ? [name] : name
  const key = names.find((k) => manifest[k])
  const entry = key ? manifest[key] : undefined
  if (!key || !entry) return <>{children}</>
  const file = typeof entry === 'string' ? entry : entry.file
  if (typeof entry !== 'string' && entry.w && entry.h) {
    // A snapped sprite: its own size on the 4× grid, bottom-centre on whole pixels.
    w = entry.w * PX
    h = entry.h * PX
    x = Math.round((x - w / 2) / PX) * PX + w / 2
    y = Math.round(y / PX) * PX
  }
  const frames = typeof entry === 'string' ? 1 : Math.max(1, entry.frames ?? 1)
  const drawn = typeof entry === 'string' ? 0 : Math.max(0, entry.fps ?? 0)
  const fps = drawn > 0 ? fpsFor(speeds, key, drawn) : 0
  const loop = typeof entry === 'string' ? true : entry.loop !== false
  if (frames === 1 || fps === 0) return <image href={`/sprites/${file}`} x={x - w / 2} y={y - h} width={w} height={h} preserveAspectRatio="xMidYMax meet" style={{ imageRendering: 'pixelated' }} />
  const values = Array.from({ length: frames }, (_, frame) => `${-frame * w} 0`).join(';')
  return (
    <g clipPath={`url(#${clipId})`}>
      <defs><clipPath id={clipId}><rect x={x - w / 2} y={y - h} width={w} height={h} /></clipPath></defs>
      <image href={`/sprites/${file}`} x={x - w / 2} y={y - h} width={w * frames} height={h} preserveAspectRatio="none" style={{ imageRendering: 'pixelated' }}>
        <animateTransform key={fps} ref={startNow} begin="indefinite" attributeName="transform" type="translate" values={values} dur={`${frames / fps}s`} calcMode="discrete" repeatCount={loop ? 'indefinite' : 1} fill={loop ? 'remove' : 'freeze'} />
      </image>
    </g>
  )
}
