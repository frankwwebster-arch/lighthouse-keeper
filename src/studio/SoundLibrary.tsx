import { useEffect, useRef, useState } from 'react'
import { peaksOf, type Mixer } from './audio'
import type { SoundInfo } from './store'
import { SOUND_DRAG } from './TimelineView'

/**
 * Every sound the recipes name. Real files can be played and dragged onto the
 * timeline; placeholders (named in a recipe, no file yet) wait for a file:
 * drop one on its row and every cue that uses that name gets it.
 */
export function SoundLibrary({ sounds, placeholders, editable, busy, onUpload, onDelete, onPreview }: {
  sounds: SoundInfo[]
  placeholders: string[]
  editable: boolean
  busy: string | null
  onUpload: (file: File, as?: string) => void
  onDelete: (id: string) => void
  onPreview: (id: string) => void
}) {
  const [over, setOver] = useState<string | null>(null)
  const pick = useRef<HTMLInputElement>(null)
  const [pickFor, setPickFor] = useState<string | undefined>()
  const rows = [...sounds.map((s) => ({ id: s.id, file: s })), ...placeholders.filter((p) => !sounds.some((s) => s.id === p)).map((id) => ({ id, file: undefined }))].sort((a, b) => a.id.localeCompare(b.id))
  const dropProps = (as?: string) => ({
    onDragOver: (e: React.DragEvent) => {
      if (editable && e.dataTransfer.types.includes('Files')) {
        e.preventDefault()
        setOver(as ?? '*')
      }
    },
    onDragLeave: () => setOver(null),
    onDrop: (e: React.DragEvent) => {
      setOver(null)
      const file = [...e.dataTransfer.files].find((f) => f.type.startsWith('audio/'))
      if (!file) return
      e.preventDefault()
      e.stopPropagation()
      onUpload(file, as)
    },
  })
  return (
    <div className={`st-library ${over === '*' ? 'over' : ''}`} {...dropProps()}>
      <input ref={pick} type="file" accept="audio/*" hidden onChange={(e) => { const f = e.target.files?.[0]; if (f) onUpload(f, pickFor); e.target.value = '' }} />
      <p className="st-dim">{editable ? 'Drop audio files here to add them, or onto a placeholder to fill it. Drag a sound onto the timeline to cue it.' : 'Unlock with the PIN to add sounds.'}</p>
      <ul>
        {rows.map((r) => (
          <li key={r.id} className={`${r.file ? 'real' : 'placeholder'} ${over === r.id ? 'over' : ''}`} draggable onDragStart={(e) => { e.dataTransfer.setData(SOUND_DRAG, r.id); e.dataTransfer.setData('text/plain', r.id) }} {...dropProps(r.id)}>
            <button type="button" className="st-mini" onClick={() => onPreview(r.id)} title="Play">▶</button>
            <span className="st-name">{r.id}</span>
            <small>{busy === r.id ? 'uploading…' : r.file ? `${Math.round(r.file.bytes / 1024)} KB` : 'placeholder'}</small>
            {editable && (r.file ? <button type="button" className="st-mini" onClick={() => { if (confirm(`Remove the file for ${r.id}? Cues keep its name and play a placeholder blip.`)) onDelete(r.id) }} title="Remove the file">✕</button> : <button type="button" className="st-mini" onClick={() => { setPickFor(r.id); pick.current?.click() }} title="Choose a file">＋</button>)}
          </li>
        ))}
      </ul>
      {editable && <button type="button" onClick={() => { setPickFor(undefined); pick.current?.click() }}>Add a sound file…</button>}
    </div>
  )
}

/** A sound's waveform with its trim marked: drag either edge to trim. */
export function Waveform({ url, mixer, trimStart, trimEnd, onTrim }: { url: string | undefined; mixer: Mixer; trimStart: number; trimEnd: number | null; onTrim: (start: number, end: number | null) => void }) {
  const canvas = useRef<HTMLCanvasElement>(null)
  const [dur, setDur] = useState<number | null>(null)
  const [peaks, setPeaks] = useState<number[]>([])
  useEffect(() => {
    let alive = true
    setDur(null)
    setPeaks([])
    if (url)
      void mixer.load(url).then((b) => {
        if (!alive || !b) return
        setDur(b.duration)
        setPeaks(peaksOf(b, 240))
      })
    return () => {
      alive = false
    }
  }, [url, mixer])
  const end = trimEnd ?? dur ?? 0
  useEffect(() => {
    const c = canvas.current
    const g = c?.getContext('2d')
    if (!c || !g) return
    const css = getComputedStyle(c)
    g.clearRect(0, 0, c.width, c.height)
    if (!dur) return
    const x = (s: number) => (s / dur) * c.width
    g.fillStyle = css.getPropertyValue('--st-trim') || '#0002'
    g.fillRect(0, 0, x(trimStart), c.height)
    g.fillRect(x(end), 0, c.width - x(end), c.height)
    g.fillStyle = css.getPropertyValue('--st-wave') || '#2f6f9f'
    peaks.forEach((p, i) => {
      const h = Math.max(1, p * c.height)
      g.fillRect((i / peaks.length) * c.width, (c.height - h) / 2, Math.max(1, c.width / peaks.length - 0.5), h)
    })
    g.fillStyle = css.getPropertyValue('--st-accent') || '#c8463c'
    g.fillRect(x(trimStart) - 1, 0, 2, c.height)
    g.fillRect(x(end) - 1, 0, 2, c.height)
  }, [peaks, dur, trimStart, end])
  if (!url) return <p className="st-dim">A placeholder: no file yet, so it plays a blip. Drop a file on it in the sound library.</p>
  if (!dur) return <p className="st-dim">Loading the sound…</p>
  const drag = (e: React.PointerEvent<HTMLCanvasElement>) => {
    const c = e.currentTarget
    const r = c.getBoundingClientRect()
    const at = (cx: number) => Math.max(0, Math.min(dur, ((cx - r.left) / r.width) * dur))
    const which = Math.abs(at(e.clientX) - trimStart) < Math.abs(at(e.clientX) - end) ? 'start' : 'end'
    c.setPointerCapture(e.pointerId)
    const set = (cx: number) => {
      const v = Math.round(at(cx) * 100) / 100
      if (which === 'start') onTrim(Math.min(v, end - 0.02), trimEnd)
      else onTrim(trimStart, v >= dur - 0.005 ? null : Math.max(v, trimStart + 0.02))
    }
    set(e.clientX)
    const move = (ev: PointerEvent) => set(ev.clientX)
    const up = () => {
      c.removeEventListener('pointermove', move)
      c.removeEventListener('pointerup', up)
    }
    c.addEventListener('pointermove', move)
    c.addEventListener('pointerup', up)
  }
  return (
    <div className="st-wave">
      <canvas ref={canvas} width={480} height={64} onPointerDown={drag} />
      <small className="st-dim">Whole sound {dur.toFixed(2)}s · playing {trimStart.toFixed(2)}–{end.toFixed(2)}s. Drag either red edge.</small>
    </div>
  )
}
