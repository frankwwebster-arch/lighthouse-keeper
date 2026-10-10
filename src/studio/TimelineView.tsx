import { useRef } from 'react'
import type { Issue, Timeline, TimedCue } from './recipe'
import type { Sel } from './StageView'

export const SOUND_DRAG = 'application/x-studio-sound'
const ROW = { ruler: 18, seg: 30, cue: 20 }

/** Cues stacked into lanes so overlapping ones do not hide each other. */
function lanesOf(cues: readonly TimedCue[], lengthOf: (c: TimedCue) => number) {
  const ends: number[] = []
  return cues.map((c) => {
    const end = c.time + lengthOf(c)
    let lane = ends.findIndex((e) => e <= c.time + 1e-6)
    if (lane < 0) lane = ends.length
    ends[lane] = end
    return lane
  })
}

/**
 * The recipe along time: its steps (macro steps grouped), the sound cues
 * underneath, problems marked, and the playhead. Click to jump; drag a cue to
 * move it; drop a sound from the library (or an audio file) to add one.
 */
export function TimelineView({ tl, t, pps, sel, issues, soundLength, onSeek, onSelect, onMoveCue, onDropSound, onDropFile }: {
  tl: Timeline
  t: number
  pps: number
  sel: Sel | null
  issues: Issue[]
  soundLength: (sound: string) => number
  onSeek: (t: number) => void
  onSelect: (s: Sel) => void
  onMoveCue: (stepId: string, cueId: string, at: number) => void
  onDropSound: (time: number, sound: string) => void
  onDropFile: (time: number, file: File) => void
}) {
  const box = useRef<HTMLDivElement>(null)
  const timeAt = (clientX: number) => {
    const r = box.current?.getBoundingClientRect()
    return r ? Math.max(0, (clientX - r.left) / pps) : 0
  }
  const len = (c: TimedCue) => (c.until !== null ? Math.max(0.1, c.until - c.time) : Math.max(0.1, (c.trimEnd ?? soundLength(c.sound)) - c.trimStart))
  // Wide enough to read its name, and stacked by that width so names never overlap.
  const shown = (c: TimedCue) => Math.max(len(c), (c.sound.length * 6.5 + 20) / pps)
  const lanes = lanesOf(tl.cues, shown)
  const nLanes = Math.max(1, ...lanes.map((l) => l + 1))
  const width = Math.max(600, Math.ceil(tl.duration * pps) + 60)
  const stepStart = (id: string) => tl.steps.find((s) => s.id === id)?.start ?? 0
  const seconds = Array.from({ length: Math.ceil(tl.duration) + 2 }, (_, i) => i)

  const scrub = (e: React.PointerEvent) => {
    const el = e.currentTarget as Element
    el.setPointerCapture(e.pointerId)
    onSeek(timeAt(e.clientX))
    const move = (ev: PointerEvent) => onSeek(timeAt(ev.clientX))
    const up = () => {
      el.removeEventListener('pointermove', move as EventListener)
      el.removeEventListener('pointerup', up)
    }
    el.addEventListener('pointermove', move as EventListener)
    el.addEventListener('pointerup', up)
  }
  const dragCue = (e: React.PointerEvent, c: TimedCue) => {
    e.stopPropagation()
    onSelect({ type: 'cue', stepId: c.stepId, cueId: c.id })
    if (c.fromMacro || c.fromClip) return // a macro's own cue is changed in the macro; a sheet's, on the sheet
    const el = e.currentTarget as Element
    el.setPointerCapture(e.pointerId)
    const grab = timeAt(e.clientX) - c.time
    const s0 = stepStart(c.stepId)
    const move = (ev: PointerEvent) => onMoveCue(c.stepId, c.id, Math.max(0, Math.round((timeAt(ev.clientX) - grab - s0) * 100) / 100))
    const up = () => {
      el.removeEventListener('pointermove', move as EventListener)
      el.removeEventListener('pointerup', up)
    }
    el.addEventListener('pointermove', move as EventListener)
    el.addEventListener('pointerup', up)
  }

  return (
    <div className="st-timeline-wrap">
      <div
        ref={box}
        className="st-timeline"
        style={{ width, height: ROW.ruler + ROW.seg + nLanes * ROW.cue + 8 }}
        onDragOver={(e) => {
          if (e.dataTransfer.types.includes(SOUND_DRAG) || e.dataTransfer.types.includes('Files')) e.preventDefault()
        }}
        onDrop={(e) => {
          e.preventDefault()
          const time = timeAt(e.clientX)
          const sound = e.dataTransfer.getData(SOUND_DRAG)
          if (sound) return onDropSound(time, sound)
          const file = [...e.dataTransfer.files].find((f) => f.type.startsWith('audio/'))
          if (file) onDropFile(time, file)
        }}
      >
        <div className="st-ruler" style={{ height: ROW.ruler }} onPointerDown={scrub}>
          {seconds.map((s) => (
            <span key={s} style={{ left: s * pps }}>{s}s</span>
          ))}
        </div>
        <div className="st-segs" style={{ top: ROW.ruler, height: ROW.seg }} onPointerDown={scrub}>
          {tl.steps.map((s) => {
            const segs = tl.segments.filter((g) => g.stepId === s.id)
            const first = segs[0]
            const main = segs.some((g) => g.main)
            const hidden = segs.length > 0 && segs.every((g) => !g.visible)
            const macro = first?.fromMacro
            const bad = issues.some((i) => i.stepId === s.id)
            return (
              <button
                key={s.id}
                type="button"
                className={`st-seg ${first?.kind ?? 'empty'} ${main ? 'main' : ''} ${hidden ? 'hidden' : ''} ${macro ? 'macro' : ''} ${bad ? 'bad' : ''} ${sel?.type === 'step' && sel.id === s.id ? 'sel' : ''}`}
                style={{ left: s.start * pps, width: Math.max(6, (s.end - s.start) * pps) }}
                onPointerDown={(e) => e.stopPropagation()}
                onClick={() => { onSelect({ type: 'step', id: s.id }); onSeek(s.start) }}
                title={first?.label}
              >
                {macro && segs.map((g) => <i key={g.innerId + g.start} style={{ left: (g.start - s.start) * pps }} className={g.visible ? '' : 'hid'} />)}
                <span>{macro ? `▸ ${macro.replace(/_/g, ' ')}` : first?.label ?? '(no time)'}</span>
              </button>
            )
          })}
        </div>
        {tl.cues.map((c, i) => (
          <button
            key={`${c.stepId}-${c.id}-${c.time}`}
            type="button"
            className={`st-cue ${c.fromMacro || c.fromClip ? 'macro' : ''} ${c.loop ? 'loop' : ''} ${sel?.type === 'cue' && sel.cueId === c.id && sel.stepId === c.stepId ? 'sel' : ''}`}
            style={{ left: c.time * pps, width: shown(c) * pps, top: ROW.ruler + ROW.seg + 4 + lanes[i] * ROW.cue }}
            onPointerDown={(e) => dragCue(e, c)}
            title={c.fromClip ? `${c.sound} (marked on the ${c.fromClip} sheet itself)` : c.fromMacro ? `${c.sound} (part of the ${c.fromMacro} macro: change it there)` : `${c.sound}: drag to move`}
          >
            {c.loop ? '↻ ' : '♪ '}{c.sound}
          </button>
        ))}
        {issues.map((i, k) => (
          <span key={k} className="st-issue" style={{ left: i.time * pps }} title={i.text} />
        ))}
        <div className="st-playhead" style={{ left: t * pps }} />
      </div>
    </div>
  )
}
