import { createContext, useContext, useEffect, useId, useState, type ReactNode } from 'react'

/**
 * Sprites from Codex (or an itch.io pack) drop into `public/sprites/` and are
 * listed in `public/sprites/manifest.json`:
 *   { "keeper_idle": "keeper_idle.png", ... }
 * Anything not listed is drawn as a vector, so the game always works.
 * (docs/CODEX_ASSETS.md has the full list of names.)
 */
type ManifestEntry = string | { file: string; frames?: number; fps?: number }
type Manifest = Record<string, ManifestEntry>
const Ctx = createContext<Manifest>({})

export function SpriteProvider({ children }: { children: ReactNode }) {
  const [m, setM] = useState<Manifest>({})
  useEffect(() => {
    let alive = true
    fetch('/sprites/manifest.json')
      .then((r) => (r.ok ? r.json() : {}))
      .then((j) => alive && typeof j === 'object' && j && setM(j as Manifest))
      .catch(() => undefined)
    return () => {
      alive = false
    }
  }, [])
  return <Ctx.Provider value={m}>{children}</Ctx.Provider>
}

/** A picture if we have one, otherwise the vector drawing. `x,y` is the bottom-centre. */
export function Sprite({ name, x = 0, y = 0, w, h, children }: { name: string | readonly string[]; x?: number; y?: number; w: number; h: number; children: ReactNode }) {
  const manifest = useContext(Ctx)
  const clipId = `sprite-${useId().replaceAll(':', '')}`
  const names = typeof name === 'string' ? [name] : name
  const entry = names.map((key) => manifest[key]).find(Boolean)
  if (!entry) return <>{children}</>
  const file = typeof entry === 'string' ? entry : entry.file
  const frames = typeof entry === 'string' ? 1 : Math.max(1, entry.frames ?? 1)
  const fps = typeof entry === 'string' ? 0 : Math.max(0, entry.fps ?? 0)
  if (frames === 1 || fps === 0) return <image href={`/sprites/${file}`} x={x - w / 2} y={y - h} width={w} height={h} preserveAspectRatio="xMidYMax meet" />
  const values = Array.from({ length: frames }, (_, frame) => `${-frame * w} 0`).join(';')
  return (
    <g clipPath={`url(#${clipId})`}>
      <defs><clipPath id={clipId}><rect x={x - w / 2} y={y - h} width={w} height={h} /></clipPath></defs>
      <image href={`/sprites/${file}`} x={x - w / 2} y={y - h} width={w * frames} height={h} preserveAspectRatio="none">
        <animateTransform attributeName="transform" type="translate" values={values} dur={`${frames / fps}s`} calcMode="discrete" repeatCount="indefinite" />
      </image>
    </g>
  )
}
