import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { verifyPin } from '../game/remote'
import { compileStory, FPS, type Frame } from './compile'
import { LIBRARY, STORY_DRAFTS } from './drafts'
import { STORY_SCHEMA, VERBS, cleanStory, versionFor, type Ambient, type CastRole, type Speed, type Step, type Story, type Verb } from './format'
import { loadStories, resetStory, saveStory, storyHash, type SavedStory } from './store'

const DRAFT_BY_ID = Object.fromEntries(STORY_DRAFTS.map((s) => [s.id, s]))
const OBJECTS = Object.entries(LIBRARY.pictures).filter(([, p]) => p.kind === 'object').sort(([a], [b]) => a.localeCompare(b))
const MARKS = Object.entries(LIBRARY.pictures).filter(([, p]) => p.kind === 'mark').sort(([a], [b]) => a.localeCompare(b))
const AFTER: Record<Story['afterStory'], string> = { loop: 'Keep retelling it', hold: 'Tell once, then hold the result', hide: 'Tell once, then the bubble goes' }
const PACES: [number, string][] = [[0.75, 'Slower'], [1, 'Normal'], [1.25, 'Quicker'], [1.5, 'Quickest']]
const SPEEDS: Speed[] = ['quick', 'normal', 'slow']
const picLabel = (id: string) => LIBRARY.pictures[id]?.label ?? id
const slug = (v: string) => v.toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60)

export default function StoryStudio() {
  const [db, setDb] = useState(false)
  const [loaded, setLoaded] = useState(false)
  const [saved, setSaved] = useState<Record<string, SavedStory>>({})
  const [docs, setDocs] = useState<Record<string, Story>>(DRAFT_BY_ID)
  const [dirty, setDirty] = useState<Set<string>>(new Set())
  const [pin, setPin] = useState<string | null>(null)
  const [typed, setTyped] = useState('')
  const [pinWrong, setPinWrong] = useState(false)
  const [saveState, setSaveState] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle')
  const [docId, setDocId] = useState(() => (typeof location !== 'undefined' && location.hash.slice(1)) || STORY_DRAFTS[0].id)
  const [newName, setNewName] = useState('')

  useEffect(() => {
    void loadStories().then((r) => {
      setDb(r.db)
      setSaved(r.saved)
      setDocs({ ...DRAFT_BY_ID, ...r.saved })
      setLoaded(true)
    })
  }, [])

  const story = docs[docId] ?? STORY_DRAFTS[0]
  useEffect(() => {
    if (typeof history !== 'undefined') history.replaceState(null, '', `#${story.id}`)
  }, [story.id])
  const compiled = useMemo(() => compileStory(story, LIBRARY), [story])
  const editable = !!pin

  // ── Playback ──
  const [playing, setPlaying] = useState(true)
  const [reduced, setReduced] = useState(() => typeof matchMedia !== 'undefined' && matchMedia('(prefers-reduced-motion: reduce)').matches)
  const [showMarks, setShowMarks] = useState(true)
  const [showBubble, setShowBubble] = useState(true)
  const [f, setF] = useState(0)
  const clock = useRef({ start: 0, from: 0 })
  const frames = reduced ? compiled.reduced : compiled.full
  useEffect(() => {
    if (!playing) return
    clock.current = { start: performance.now(), from: f }
    let raf = 0
    const tick = (now: number) => {
      const step = Math.floor(((now - clock.current.start) / 1000) * FPS) + clock.current.from
      // “Hold” shows the result for two seconds in the preview, then replays.
      const span = compiled.afterStory === 'hold' ? frames.length + 2 * FPS : frames.length
      setF(Math.min(step % span, frames.length - 1))
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
    // Restart the clock when the story or mode changes; `f` is only read at the start.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playing, frames, compiled.afterStory])
  const frame = frames[Math.min(f, frames.length - 1)]
  const bodyFrame = LIBRARY.keeper.rearWork[Math.floor((f / FPS) * 4) % LIBRARY.keeper.rearWork.length]

  // Decode every picture once, so playback never stutters.
  useEffect(() => {
    const urls = new Set<string>(LIBRARY.keeper.rearWork.map((r) => r.url))
    for (const p of Object.values(LIBRARY.pictures)) for (const v of p.versions) urls.add(v.url)
    for (const u of urls) {
      const img = new Image()
      img.src = u
    }
  }, [])

  // ── Editing ──
  const edit = useCallback((next: Story) => {
    setDocs((d) => ({ ...d, [next.id]: next }))
    setDirty((s) => new Set(s).add(next.id))
    setSaveState('idle')
  }, [])
  const setStep = (i: number, s: Step) => edit({ ...story, steps: story.steps.map((x, j) => (j === i ? s : x)) })
  const moveStep = (from: number, to: number) => {
    if (to < 0 || to >= story.steps.length || from === to) return
    const steps = [...story.steps]
    const [s] = steps.splice(from, 1)
    steps.splice(to, 0, s)
    edit({ ...story, steps })
  }
  const dragFrom = useRef<number | null>(null)

  const unlock = async () => {
    if (await verifyPin(typed, db)) {
      setPin(typed)
      setPinWrong(false)
    } else setPinWrong(true)
  }
  const saveAll = async () => {
    if (!pin || !dirty.size) return
    setSaveState('saving')
    const done: Record<string, SavedStory> = {}
    for (const id of dirty) {
      const s: SavedStory = { ...docs[id], draftHash: DRAFT_BY_ID[id] ? storyHash(DRAFT_BY_ID[id]) : undefined }
      if (await saveStory(pin, s, db)) done[id] = s
    }
    setSaved((m) => ({ ...m, ...done }))
    setDirty((d) => new Set([...d].filter((id) => !done[id])))
    setSaveState(Object.keys(done).length === dirty.size ? 'saved' : 'error')
  }
  const backToDraft = async () => {
    if (!pin || !DRAFT_BY_ID[story.id]) return
    if (!saved[story.id] || (await resetStory(pin, story.id, db))) {
      setSaved((m) => Object.fromEntries(Object.entries(m).filter(([k]) => k !== story.id)))
      setDocs((d) => ({ ...d, [story.id]: DRAFT_BY_ID[story.id] }))
      setDirty((s) => new Set([...s].filter((k) => k !== story.id)))
    }
  }
  const createStory = () => {
    const id = slug(newName)
    if (!id || docs[id]) return
    const fresh = cleanStory({ schema: STORY_SCHEMA, id, label: newName.trim(), appliesTo: { assetId: '', label: '' }, cast: { hero: { picture: OBJECTS[0][0], role: 'hero' } }, steps: [{ do: 'arrive', who: 'hero' }, { do: 'settle' }] })!
    edit(fresh)
    setDocId(id)
    setNewName('')
  }
  const copyJson = () => {
    const text = JSON.stringify(story, null, 2)
    void navigator.clipboard?.writeText(text).catch(() => undefined)
  }

  const draftMoved = !!saved[story.id]?.draftHash && DRAFT_BY_ID[story.id] && saved[story.id].draftHash !== storyHash(DRAFT_BY_ID[story.id])
  const castNames = Object.keys(story.cast)
  const windowOf = (i: number) => compiled.windows[i]
  const currentStep = frame?.step ?? 1

  return (
    <div className="studio ss">
      <header className="st-head">
        <h1>Bubble stories</h1>
        <a href="/studio">← Recipe studio</a>
        <span className="st-dim">{loaded ? (db ? 'Saved for everyone' : 'Local copy: stories stay in this browser') : 'Loading…'}</span>
        <span className="st-grow" />
        {editable ? (
          <>
            <span className={`st-save ${saveState === 'error' ? 'error' : ''}`}>{saveState === 'saving' ? 'Saving…' : saveState === 'saved' ? 'Saved' : saveState === 'error' ? 'Not saved' : dirty.size ? `${dirty.size} unsaved` : 'All saved'}</span>
            <button type="button" disabled={!dirty.size} onClick={() => void saveAll()}>Save</button>
          </>
        ) : (
          <form className="st-pin" onSubmit={(e) => { e.preventDefault(); void unlock() }}>
            <input type="password" inputMode="numeric" placeholder="PIN to edit" value={typed} onChange={(e) => setTyped(e.target.value)} />
            <button type="submit">Unlock</button>
            {pinWrong && <b>Not right</b>}
          </form>
        )}
      </header>

      <aside className="st-list">
        <h2>Stories</h2>
        <ul>
          {Object.values(docs).map((s) => (
            <li key={s.id}>
              <button type="button" className={s.id === story.id ? 'on' : ''} onClick={() => { setDocId(s.id); setF(0) }}>
                <span className={`st-status ${saved[s.id] ? 'needs-work' : ''}`} />
                {s.label}
                {dirty.has(s.id) && <small> · unsaved</small>}
                {saved[s.id] && !dirty.has(s.id) && <small> · yours</small>}
              </button>
            </li>
          ))}
        </ul>
        {editable && (
          <form className="ss-new" onSubmit={(e) => { e.preventDefault(); createStory() }}>
            <input placeholder="New story name" value={newName} onChange={(e) => setNewName(e.target.value)} />
            <button type="submit" disabled={!slug(newName) || !!docs[slug(newName)]}>Add</button>
          </form>
        )}
        <h2>Picture library</h2>
        <p className="st-dim">Codex adds and replaces pictures. A new version reaches every story straight away; pin an older one in a story’s cast to put it back.</p>
        <ul className="ss-lib">
          {[...OBJECTS, ...MARKS].map(([id, p]) => (
            <li key={id} title={p.review?.note ?? ''}>
              <img src={versionFor(LIBRARY, id)?.url} alt="" />
              <span>{p.label}<small> · v{p.current}{p.versions.length > 1 ? ` of ${p.versions.length}` : ''}{p.review?.status === 'rework-requested' ? ' · rework asked' : ''}</small></span>
            </li>
          ))}
        </ul>
      </aside>

      <main className="st-main">
        <div className="st-title">
          <h2>{story.label}</h2>
          <span className="st-dim">{story.appliesTo.label || 'No object yet'} · {compiled.seconds.toFixed(1)} s · {compiled.storyFrames} frames at {FPS} fps</span>
          <span className="st-grow" />
          {editable && DRAFT_BY_ID[story.id] && (saved[story.id] || dirty.has(story.id)) && <button type="button" onClick={() => void backToDraft()}>Back to Claude’s draft</button>}
          <button type="button" onClick={copyJson} title="For Claude or Codex">Copy story</button>
        </div>
        {draftMoved && <p className="st-warn">Claude has updated the draft since you edited this. Your version is showing; “Back to Claude’s draft” shows the new one.</p>}

        <div className="ss-stagewrap">
          <BubbleStage frame={frame} body={bodyFrame?.url} showMarks={showMarks} showBubble={showBubble} />
          <div className="ss-beat">
            Step {currentStep}: {stepText(story, story.steps[currentStep - 1])}
            {frame?.phase === 'quiet' ? ' · quiet' : frame?.phase === 'clear' ? ' · clearing for the next telling' : ''}
          </div>
        </div>

        <div className="st-transport">
          <button type="button" className="st-play" onClick={() => setPlaying((p) => !p)}>{playing ? '⏸ Pause' : '▶ Play'}</button>
          <button type="button" onClick={() => { setPlaying(false); setF((x) => Math.max(0, x - 1)) }}>◀ Frame</button>
          <button type="button" onClick={() => { setPlaying(false); setF((x) => Math.min(frames.length - 1, x + 1)) }}>Frame ▶</button>
          <button type="button" onClick={() => { setF(0); setPlaying(true) }}>Replay</button>
          <input type="range" min={0} max={frames.length - 1} value={Math.min(f, frames.length - 1)} onChange={(e) => { setPlaying(false); setF(Number(e.target.value)) }} aria-label="Frame" />
          <span className="st-readout">{Math.min(f, frames.length - 1) + 1}/{frames.length}</span>
          <label><input type="checkbox" checked={reduced} onChange={(e) => setReduced(e.target.checked)} /> Reduced motion</label>
          <label><input type="checkbox" checked={showMarks} onChange={(e) => setShowMarks(e.target.checked)} /> Marks</label>
          <label><input type="checkbox" checked={showBubble} onChange={(e) => setShowBubble(e.target.checked)} /> Bubble</label>
        </div>

        {compiled.issues.length > 0 ? (
          <ul className="st-problems">
            {compiled.issues.map((i, k) => <li key={k} className={i.level === 'error' ? 'ss-err' : ''}>{i.level === 'error' ? '⛔' : '⚠️'} {i.text}</li>)}
          </ul>
        ) : (
          <p className="st-ok">No problems: every step can play, every touch mark lands where two pictures meet, and the story lasts between 5 and 10 seconds.</p>
        )}

        <h2>How it ends</h2>
        <div className="ss-row">
          <label>When he keeps working <select disabled={!editable} value={story.afterStory} onChange={(e) => edit({ ...story, afterStory: e.target.value as Story['afterStory'] })}>{Object.entries(AFTER).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select></label>
          <label>Pace <select disabled={!editable} value={story.pace} onChange={(e) => edit({ ...story, pace: Number(e.target.value) })}>{PACES.map(([v, t]) => <option key={v} value={v}>{t}</option>)}</select></label>
        </div>
      </main>

      <aside className="st-side">
        <h2>Steps, in order</h2>
        <p className="st-dim">Drag a step, or use the arrows, to change the order. Tap a step’s number to watch it.</p>
        <ol className="ss-steps">
          {story.steps.map((s, i) => {
            const needs = VERBS[s.do].needs
            return (
              <li
                key={i}
                className={i + 1 === currentStep ? 'on' : ''}
                draggable={editable}
                onDragStart={() => { dragFrom.current = i }}
                onDragOver={(e) => e.preventDefault()}
                onDrop={() => { if (dragFrom.current !== null) moveStep(dragFrom.current, i); dragFrom.current = null }}
              >
                <button type="button" className="ss-num" onClick={() => { setPlaying(false); setF(windowOf(i)?.start ?? 0) }} title="Watch this step">{i + 1}</button>
                <div className="ss-fields">
                  {needs.includes('who') && <select disabled={!editable} value={s.who ?? ''} onChange={(e) => setStep(i, { ...s, who: e.target.value })}><option value="">who?</option>{castNames.map((c) => <option key={c} value={c}>{c}</option>)}</select>}
                  <select disabled={!editable} value={s.do} onChange={(e) => setStep(i, { ...s, do: e.target.value as Verb })} title={VERBS[s.do].hint}>{Object.entries(VERBS).map(([k, v]) => <option key={k} value={k}>{v.label}</option>)}</select>
                  {needs.includes('onto') && <select disabled={!editable} value={s.onto ?? ''} onChange={(e) => setStep(i, { ...s, onto: e.target.value })}><option value="">what?</option>{castNames.map((c) => <option key={c} value={c}>{c}</option>)}</select>}
                  {s.do !== 'settle' && <select disabled={!editable} value={s.speed ?? 'normal'} onChange={(e) => setStep(i, { ...s, speed: e.target.value as Speed })}>{SPEEDS.map((v) => <option key={v} value={v}>{v}</option>)}</select>}
                  {needs.includes('onto') && <select disabled={!editable} value={s.mark ?? ''} onChange={(e) => setStep(i, { ...s, mark: e.target.value || undefined })} title="The mark at each touch"><option value="">usual mark</option>{MARKS.map(([id, p]) => <option key={id} value={id}>{p.label}</option>)}</select>}
                  {(s.do === 'reveal' || s.do === 'land-on' || s.do === 'flip') && <label className="st-dim" title={s.do === 'reveal' ? 'The result takes the place of what it came from' : 'What was already on it sinks in and vanishes'}><input type="checkbox" disabled={!editable} checked={!!s.replace} onChange={(e) => setStep(i, { ...s, replace: e.target.checked || undefined })} /> {s.do === 'reveal' ? 'takes its place' : 'replaces what’s on it'}</label>}
                </div>
                {editable && (
                  <span className="ss-tools">
                    <button type="button" className="st-mini" onClick={() => moveStep(i, i - 1)} title="Earlier">↑</button>
                    <button type="button" className="st-mini" onClick={() => moveStep(i, i + 1)} title="Later">↓</button>
                    <button type="button" className="st-mini" onClick={() => edit({ ...story, steps: story.steps.filter((_, j) => j !== i) })} title="Remove">✕</button>
                  </span>
                )}
              </li>
            )
          })}
        </ol>
        {editable && <button type="button" className="st-add" onClick={() => edit({ ...story, steps: [...story.steps.slice(0, -1), { do: 'land-on', who: castNames[1], onto: castNames[0] }, ...story.steps.slice(-1)] })}>Add a step</button>}

        <h2>Cast</h2>
        <ul className="ss-cast">
          {Object.entries(story.cast).map(([as, m]) => {
            const p = LIBRARY.pictures[m.picture]
            return (
              <li key={as}>
                <img src={versionFor(LIBRARY, m.picture, m.version)?.url} alt="" />
                <b>{as}</b>
                <select disabled={!editable} value={m.picture} onChange={(e) => edit({ ...story, cast: { ...story.cast, [as]: { picture: e.target.value, role: m.role } } })}>{OBJECTS.map(([id, o]) => <option key={id} value={id}>{o.label}</option>)}</select>
                <select disabled={!editable} value={m.role} onChange={(e) => edit({ ...story, cast: { ...story.cast, [as]: { ...m, role: e.target.value as CastRole } } })}><option value="hero">main</option><option value="support">helper</option><option value="result">result</option></select>
                {p && p.versions.length > 1 && (
                  <select disabled={!editable} value={m.version ?? ''} onChange={(e) => edit({ ...story, cast: { ...story.cast, [as]: { picture: m.picture, role: m.role, ...(e.target.value ? { version: Number(e.target.value) } : {}) } } })} title="Pin an older version">
                    <option value="">newest (v{p.current})</option>
                    {p.versions.filter((v) => v.v !== p.current).map((v) => <option key={v.v} value={v.v}>v{v.v} · {v.added}</option>)}
                  </select>
                )}
              </li>
            )
          })}
        </ul>
        {editable && <AddCast onAdd={(as, picture) => edit({ ...story, cast: { ...story.cast, [as]: { picture, role: 'support' } } })} taken={castNames} />}

        <h2>Extra marks</h2>
        <p className="st-dim">A mark that rides on one picture for some steps, like heat over the grill.</p>
        <ul className="ss-cast">
          {story.ambient.map((a, i) => {
            const set = (next: Ambient) => edit({ ...story, ambient: story.ambient.map((x, j) => (j === i ? next : x)) })
            return (
              <li key={i}>
                <img src={versionFor(LIBRARY, a.picture)?.url} alt="" />
                <select disabled={!editable} value={a.picture} onChange={(e) => set({ ...a, picture: e.target.value })}>{MARKS.map(([id, p]) => <option key={id} value={id}>{p.label}</option>)}</select>
                on <select disabled={!editable} value={a.on} onChange={(e) => set({ ...a, on: e.target.value })}>{castNames.map((c) => <option key={c} value={c}>{c}</option>)}</select>
                steps <input type="number" disabled={!editable} min={1} max={story.steps.length} value={a.fromStep} onChange={(e) => set({ ...a, fromStep: Number(e.target.value) })} />–<input type="number" disabled={!editable} min={1} max={story.steps.length} value={a.toStep} onChange={(e) => set({ ...a, toStep: Number(e.target.value) })} />
                {editable && <button type="button" className="st-mini" onClick={() => edit({ ...story, ambient: story.ambient.filter((_, j) => j !== i) })}>✕</button>}
              </li>
            )
          })}
        </ul>
        {editable && <button type="button" className="st-add" onClick={() => edit({ ...story, ambient: [...story.ambient, { picture: MARKS[0][0], on: castNames[0], fromStep: 1, toStep: 1 }] })}>Add an extra mark</button>}
        {story.notes && <><h2>Notes</h2><p className="st-dim">{story.notes}</p></>}
      </aside>
    </div>
  )
}

function stepText(story: Story, s: Step | undefined): string {
  if (!s) return ''
  const v = VERBS[s.do]
  const name = (as?: string) => (as && story.cast[as] ? picLabel(story.cast[as].picture) : '…')
  if (s.do === 'settle') return 'a quiet moment'
  return v.needs.includes('onto') ? `${name(s.who)} · ${v.label} · ${name(s.onto)}` : `${name(s.who)} · ${v.label}`
}

function AddCast({ onAdd, taken }: { onAdd: (as: string, picture: string) => void; taken: string[] }) {
  const [picture, setPicture] = useState(OBJECTS[0][0])
  const as = slug(picLabel(picture).split(' ')[0]) || 'extra'
  const name = taken.includes(as) ? `${as}-2` : as
  return (
    <div className="ss-row">
      <select value={picture} onChange={(e) => setPicture(e.target.value)}>{OBJECTS.map(([id, o]) => <option key={id} value={id}>{o.label}</option>)}</select>
      <button type="button" onClick={() => onAdd(name, picture)}>Add to cast</button>
    </div>
  )
}

/** The bubble over the approved rear-work keeper, drawn the same way as Codex's V2 review pages. */
export function BubbleStage({ frame, body, showMarks, showBubble }: { frame: Frame | undefined; body?: string; showMarks: boolean; showBubble: boolean }) {
  return (
    <div className="ss-stage">
      {body && <img className="ss-actor" src={body} alt="The keeper at work, seen from behind" />}
      <div className="ss-cloud">
        {showBubble && (
          <>
            <div className="ss-bubble" style={{ opacity: frame?.bubble.opacity ?? 1, transform: `scale(${frame?.bubble.scale ?? 1})` }} />
            <div className="ss-ring ss-ring1" style={{ opacity: frame?.bubble.opacity ?? 1 }} />
            <div className="ss-ring ss-ring2" style={{ opacity: frame?.bubble.opacity ?? 1 }} />
          </>
        )}
        {frame?.items.filter((i) => showMarks || i.kind === 'object').map((i) => (
          <img
            key={i.id}
            className={`ss-piece${i.kind === 'mark' ? ' ss-mark' : ''}`}
            src={i.url}
            alt=""
            style={{ opacity: i.opacity, zIndex: i.z, transform: `translate(calc(-50% + ${i.x}px), calc(-50% + ${i.y}px)) rotate(${i.rotation}deg) scale(${i.scale})` }}
          />
        ))}
      </div>
    </div>
  )
}
