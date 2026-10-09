import { useEffect, useMemo, useRef, useState } from 'react'
import { FPS, fpsExport, fpsFor, isTweaked, pruneFps, withFps, type FpsOverrides } from '../game/animFps'
import { PX, Sprite, useAnimSpeeds, useSprites } from './Sprite'

/**
 * Grown-ups: change any animation's frames per second while the game runs.
 * The change shows at once wherever that animation plays; most keeper clips
 * are not in the game yet, so each one can be watched here too.
 */
export function AnimationSpeeds({ onSave }: { onSave: (fps: FpsOverrides) => void }) {
  const manifest = useSprites()
  const { fps, setFps } = useAnimSpeeds()
  const [find, setFind] = useState('')
  const [pick, setPick] = useState<string | null>(null)
  const [replay, setReplay] = useState(0)
  const [copied, setCopied] = useState<string | null>(null)
  // A slider sends many changes a second: show each at once, save once it settles.
  const timer = useRef<ReturnType<typeof setTimeout>>()
  useEffect(() => () => clearTimeout(timer.current), [])

  const animated = useMemo(
    () =>
      Object.entries(manifest)
        .flatMap(([name, e]) => (typeof e !== 'string' && (e.frames ?? 1) > 1 && (e.fps ?? 0) > 0 ? [{ name, frames: e.frames!, drawn: e.fps!, w: e.w ?? 32, h: e.h ?? 40, loop: e.loop !== false }] : []))
        .sort((a, b) => a.name.localeCompare(b.name)),
    [manifest],
  )
  const words = find.trim().toLowerCase().split(/[\s_]+/).filter(Boolean)
  const shown = animated.filter((a) => words.every((w) => a.name.includes(w)))
  const sel = animated.find((a) => a.name === pick)
  // Tweaks the sheets have moved on from no longer count (the sheet's metadata wins).
  const live = pruneFps(fps, (n) => animated.find((a) => a.name === n)?.drawn)
  const changed = Object.keys(live).length

  const change = (next: FpsOverrides) => {
    const kept = pruneFps(next, (n) => animated.find((a) => a.name === n)?.drawn)
    setFps(kept)
    clearTimeout(timer.current)
    timer.current = setTimeout(() => onSave(kept), 400)
  }
  const copy = async () => {
    const text = fpsExport(live)
    try {
      await navigator.clipboard.writeText(text)
      setCopied('Copied. Put these speeds into each sprite sheet’s metadata; once a sheet has the new speed, its tweak here is no longer needed.')
    } catch {
      setCopied(text)
    }
  }

  if (!animated.length) return <p className="dim">No animations have been delivered yet.</p>
  const now = sel ? fpsFor(fps, sel.name, sel.drawn) : 0
  return (
    <div className="speeds">
      <p className="dim">Frames per second for any animation, on top of the speed in its sprite sheet’s metadata. A change shows straight away in the game, on every device. If a sheet’s own speed is changed later, the sheet wins and the tweak here drops away.</p>
      <input type="search" value={find} onChange={(e) => setFind(e.target.value)} placeholder={`Find one of ${animated.length} (e.g. walk, tv, pyjamas)`} />
      <div className="speed-list" role="listbox" aria-label="Animations">
        {shown.map((a) => {
          const own = isTweaked(fps, a.name, a.drawn)
          return (
            <button key={a.name} role="option" aria-selected={a.name === pick} className={a.name === pick ? 'on' : undefined} onClick={() => { setPick(a.name); setReplay((n) => n + 1) }}>
              <span>{a.name}</span>
              <b className={own ? 'own' : undefined}>{fpsFor(fps, a.name, a.drawn)} fps</b>
            </button>
          )
        })}
        {!shown.length && <p className="dim">Nothing matches.</p>}
      </div>
      {sel && (
        <div className="speed-pick">
          <svg key={`${sel.name}-${replay}`} className="speed-preview" viewBox={`0 0 ${sel.w * PX} ${sel.h * PX}`} role="img" aria-label={`${sel.name} at ${now} frames per second`}>
            <Sprite name={sel.name} x={(sel.w * PX) / 2} y={sel.h * PX} w={sel.w * PX} h={sel.h * PX}>
              <></>
            </Sprite>
          </svg>
          <div>
            <b>{sel.name}</b>
            <p className="dim">
              {sel.frames} frames · {(sel.frames / now).toFixed(2)}s {sel.loop ? 'a loop' : 'once through'} · drawn at {sel.drawn} fps
            </p>
            <div className="row">
              <button disabled={now <= FPS.min} onClick={() => change(withFps(fps, sel.name, now - FPS.step, sel.drawn))}>−{FPS.step}</button>
              <input type="range" min={FPS.min} max={FPS.max} step={FPS.step} value={now} aria-label="Frames per second" onChange={(e) => change(withFps(fps, sel.name, Number(e.target.value), sel.drawn))} />
              <button disabled={now >= FPS.max} onClick={() => change(withFps(fps, sel.name, now + FPS.step, sel.drawn))}>+{FPS.step}</button>
              <b>{now} fps</b>
            </div>
            <div className="row">
              <button onClick={() => setReplay((n) => n + 1)}>▶ Play again</button>
              <button disabled={!isTweaked(fps, sel.name, sel.drawn)} onClick={() => change(withFps(fps, sel.name, undefined, sel.drawn))}>Back to {sel.drawn} fps</button>
            </div>
          </div>
        </div>
      )}
      <div className="row">
        <button disabled={!changed} onClick={copy}>Copy {changed} change{changed === 1 ? '' : 's'} for the metadata</button>
        <button disabled={!changed} onClick={() => { if (confirm('Put every animation back to its sprite sheet’s speed?')) change({}) }}>Put all back to the sheets’ speeds</button>
      </div>
      {copied && (copied.startsWith('{') ? <textarea readOnly value={copied} rows={6} onFocus={(e) => e.target.select()} /> : <p className="dim">{copied}</p>)}
    </div>
  )
}
