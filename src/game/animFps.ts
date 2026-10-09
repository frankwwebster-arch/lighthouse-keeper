/**
 * ANIMATION SPEEDS. The grown-ups can set any animation's frames per second
 * while the game runs (Grown-ups panel, "Animation speeds"). One setting for
 * the whole game, not per player: it is how the art plays, not a dial for a
 * child. Saved with the grown-ups' PIN (database `settings`, or this browser).
 *
 * Same range and steps as Codex's review page (docs/keeper-scale-audit/review.html),
 * so a speed chosen in either place means the same thing. Settled speeds are
 * copied out (`fpsExport`) and baked into the sprite sidecars by Codex.
 */

export const FPS = { min: 1, max: 20, step: 0.5 } as const

/** Sprite name → frames per second, for the ones changed from how they were drawn. */
export type FpsOverrides = Record<string, number>

/** A speed in range, on the half-step. */
export const clampFps = (n: number) => Math.min(FPS.max, Math.max(FPS.min, Math.round(n / FPS.step) * FPS.step))

/** Keep only sensible entries from saved or sent data (anything else is dropped, not guessed). */
export function cleanFps(raw: unknown): FpsOverrides {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return {}
  const out: FpsOverrides = {}
  for (const [name, v] of Object.entries(raw as Record<string, unknown>)) {
    if (!/^[a-z0-9_]{1,80}$/.test(name)) continue
    const n = typeof v === 'number' ? v : typeof v === 'string' && v.trim() !== '' ? Number(v) : NaN
    if (Number.isFinite(n)) out[name] = clampFps(n)
  }
  return out
}

/** The speed to play at: the grown-ups' own, or the one it was drawn with. */
export const fpsFor = (overrides: FpsOverrides, name: string, drawn: number) => overrides[name] ?? drawn

/** Set one speed; `undefined` (or the drawn speed) puts it back to how it was drawn. */
export function withFps(overrides: FpsOverrides, name: string, fps: number | undefined, drawn: number): FpsOverrides {
  const next = { ...overrides }
  if (fps === undefined || clampFps(fps) === drawn) delete next[name]
  else next[name] = clampFps(fps)
  return next
}

/** For Codex: the changed speeds, ready to bake into each sprite's JSON sidecar as `animationFps`. */
export const fpsExport = (overrides: FpsOverrides) => JSON.stringify({ animationFps: Object.fromEntries(Object.entries(overrides).sort(([a], [b]) => a.localeCompare(b))) }, null, 2)
