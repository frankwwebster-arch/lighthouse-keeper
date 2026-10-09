/**
 * ANIMATION SPEEDS. The grown-ups can set any animation's frames per second
 * while the game runs (Grown-ups panel, "Animation speeds"). One setting for
 * the whole game, not per player: it is how the art plays, not a dial for a
 * child. Saved with the grown-ups' PIN (database `settings`, or this browser).
 *
 * Same range and steps as Codex's review page (docs/keeper-scale-audit/review.html),
 * so a speed chosen in either place means the same thing. The sprite sheets'
 * metadata stays the real record: a tweak lasts only while its sheet keeps the
 * speed it was made against, and settled tweaks are copied out (`fpsExport`)
 * into that metadata.
 */

export const FPS = { min: 1, max: 20, step: 0.5 } as const

/**
 * Sprite name → the grown-ups' speed, and the speed the sheet had when they set
 * it. The sprite sheet's metadata is the real record: if its speed is changed
 * later, the sheet wins and the old tweak no longer applies.
 */
export type FpsOverrides = Record<string, { fps: number; drawn: number }>

/** A speed in range, on the half-step. */
export const clampFps = (n: number) => Math.min(FPS.max, Math.max(FPS.min, Math.round(n / FPS.step) * FPS.step))

const num = (v: unknown) => (typeof v === 'number' ? v : typeof v === 'string' && v.trim() !== '' ? Number(v) : NaN)

/** Keep only sensible entries from saved or sent data (anything else is dropped, not guessed). */
export function cleanFps(raw: unknown): FpsOverrides {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return {}
  const out: FpsOverrides = {}
  for (const [name, v] of Object.entries(raw as Record<string, unknown>)) {
    if (!/^[a-z0-9_]{1,80}$/.test(name) || !v || typeof v !== 'object') continue
    const fps = num((v as { fps?: unknown }).fps)
    const drawn = num((v as { drawn?: unknown }).drawn)
    if (Number.isFinite(fps) && Number.isFinite(drawn) && drawn > 0) out[name] = { fps: clampFps(fps), drawn }
  }
  return out
}

/** Is the grown-ups' speed in force for this sheet (set, and the sheet's own speed unchanged since)? */
export const isTweaked = (overrides: FpsOverrides, name: string, drawn: number) => overrides[name]?.drawn === drawn

/** The speed to play at: the grown-ups' own while it still applies, or the sheet's. */
export const fpsFor = (overrides: FpsOverrides, name: string, drawn: number) => (isTweaked(overrides, name, drawn) ? overrides[name].fps : drawn)

/** Set one speed; `undefined` (or the sheet's own speed) puts it back to the sheet's. */
export function withFps(overrides: FpsOverrides, name: string, fps: number | undefined, drawn: number): FpsOverrides {
  const next = { ...overrides }
  if (fps === undefined || clampFps(fps) === drawn) delete next[name]
  else next[name] = { fps: clampFps(fps), drawn }
  return next
}

/** Forget tweaks the sheets have moved on from (or that name a sheet that has gone). */
export const pruneFps = (overrides: FpsOverrides, sheetFps: (name: string) => number | undefined): FpsOverrides =>
  Object.fromEntries(Object.entries(overrides).filter(([name, o]) => sheetFps(name) === o.drawn))

/** For the sprite metadata: the tweaked speeds as `animationFps`, sorted. */
export const fpsExport = (overrides: FpsOverrides) => JSON.stringify({ animationFps: Object.fromEntries(Object.entries(overrides).sort(([a], [b]) => a.localeCompare(b)).map(([n, o]) => [n, o.fps])) }, null, 2)
