import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'

/**
 * Sprites from Codex (or an itch.io pack) drop into `public/sprites/` and are
 * listed in `public/sprites/manifest.json`:
 *   { "keeper_idle": "keeper_idle.png", ... }
 * Anything not listed is drawn as a vector, so the game always works.
 * (docs/CODEX_ASSETS.md has the full list of names.)
 */
type Manifest = Record<string, string>
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
export function Sprite({ name, x = 0, y = 0, w, h, children }: { name: string; x?: number; y?: number; w: number; h: number; children: ReactNode }) {
  const file = useContext(Ctx)[name]
  if (!file) return <>{children}</>
  return <image href={`/sprites/${file}`} x={x - w / 2} y={y - h} width={w} height={h} preserveAspectRatio="xMidYMax meet" />
}
