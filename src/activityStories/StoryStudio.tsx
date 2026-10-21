import { useCallback, useEffect, useMemo, useRef, useState, type DragEvent, type MouseEvent } from 'react'
import { bubbleOutline, compileStory, FPS, type Frame } from './compile'
import { LIBRARY, STORY_DRAFTS } from './drafts'
import { STORY_SCHEMA, VERBS, canPlace, cleanStory, describeStep, groupPictures, placePicture, playsText, versionFor, type Ambient, type DropTarget, type CastRole, type Flow, type Prop, type PropSlot, type Speed, type Step, type Story, type Verb } from './format'
import { loadStories, resetStory, saveStory, storyHash, type SavedStory } from './store'

const DRAFT_BY_ID = Object.fromEntries(STORY_DRAFTS.map((s) => [s.id, s]))
const OBJECTS = Object.entries(LIBRARY.pictures).filter(([, p]) => p.kind === 'object').sort(([a], [b]) => a.localeCompare(b))
const MARKS = Object.entries(LIBRARY.pictures).filter(([, p]) => p.kind === 'mark').sort(([, a], [, b]) => a.label.localeCompare(b.label))
/** Every picture menu is grouped the same way as the library list (format.ts PICTURE_GROUPS). */
const OBJECT_GROUPS = groupPictures(LIBRARY, 'object')
const ALL_GROUPS = groupPictures(LIBRARY)
const AFTER: Record<Story['afterStory'], string> = { loop: 'Keep retelling it', hold: 'Tell once, then hold the result', hide: 'Tell once, then the bubble goes' }
const PACES: [number, string][] = [[0.75, 'Slower'], [1, 'Normal'], [1.25, 'Quicker'], [1.5, 'Quickest']]
const SPEEDS: Speed[] = ['quick', 'normal', 'slow']
const FLOWS: Record<Flow, string> = { around: 'From both sides', 'left-to-right': 'Left to right' }
const SLOTS: Record<PropSlot, string> = { orbit: 'circling the bubble', 'top-left': 'top left', 'top-right': 'top right', 'bottom-left': 'bottom left', 'bottom-right': 'bottom right' }
const picLabel = (id: string) => LIBRARY.pictures[id]?.label ?? id
const stepText = (story: Story, s: Step | undefined) => describeStep(LIBRARY, story, s)
const slug = (v: string) => v.toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60)

export default function StoryStudio() {
  const [db, setDb] = useState(false)
  const [loaded, setLoaded] = useState(false)
  const [saved, setSaved] = useState<Record<string, SavedStory>>({})
  const [docs, setDocs] = useState<Record<string, Story>>(DRAFT_BY_ID)
  const [dirty, setDirty] = useState<Set<string>>(new Set())
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
  // No PIN for bubble stories (Frank, 21 Oct): anyone with the studio open can edit and save.
  const editable = true

  // ── Playback ──
  const [playing, setPlaying] = useState(true)
  const [reduced, setReduced] = useState(() => typeof matchMedia !== 'undefined' && matchMedia('(prefers-reduced-motion: reduce)').matches)
  const [showMarks, setShowMarks] = useState(true)
  const [showBubble, setShowBubble] = useState(true)
  const [f, setF] = useState(0)
  const clock = useRef({ start: 0, from: 0 })
  // The opening plays once, then the story; retellings jump back to the retelling step, so the bubble stays up.
  const intro = reduced ? compiled.introReduced : compiled.intro
  const frames = useMemo(() => [...intro, ...(reduced ? compiled.reduced : compiled.full)], [intro, reduced, compiled])
  useEffect(() => {
    if (!playing) return
    clock.current = { start: performance.now(), from: f }
    let raf = 0
    const tick = (now: number) => {
      const step = Math.floor(((now - clock.current.start) / 1000) * FPS) + clock.current.from
      // “Hold” shows the result for two seconds in the preview, then replays; a story with a retelling step jumps back there.
      const back = compiled.afterStory === 'loop' ? intro.length + compiled.loopStart : 0
      const span = compiled.afterStory === 'hold' ? frames.length + 2 * FPS : frames.length
      setF(step < span ? Math.min(step, frames.length - 1) : Math.min(back + ((step - span) % (span - back)), frames.length - 1))
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
    // Restart the clock when the story or mode changes; `f` is only read at the start.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playing, frames, compiled.afterStory, compiled.loopStart, intro.length])
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

  // ── Drag and drop from the library (Frank, 21 Oct): drag a picture onto the story, or tap it and tap where it goes ──
  const [carrying, setCarrying] = useState<{ id: string; tapped: boolean } | null>(null)
  const [over, setOver] = useState<string | null>(null)
  const carriedKind = carrying ? LIBRARY.pictures[carrying.id]?.kind : undefined
  useEffect(() => {
    if (!carrying?.tapped) return
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape') setCarrying(null) }
    addEventListener('keydown', esc)
    return () => removeEventListener('keydown', esc)
  }, [carrying])
  const place = (target: DropTarget) => {
    const next = carrying && placePicture(story, LIBRARY, carrying.id, target)
    if (next) edit(next)
    setCarrying(null)
    setOver(null)
  }
  /** Makes an element a drop spot for the carried picture; it lights up when the picture can land there. */
  const dropZone = (target: DropTarget, base = '') => {
    const ok = editable && !!carriedKind && canPlace(story, carriedKind, target)
    const key = JSON.stringify(target)
    return {
      className: `${base}${ok ? ' ss-drop-ok' : ''}${ok && over === key ? ' ss-drop-over' : ''}`,
      onDragOver: (e: DragEvent) => {
        if (!ok) return
        e.preventDefault()
        e.stopPropagation()
        if (over !== key) setOver(key)
      },
      onDragLeave: (e: DragEvent) => {
        if (!e.currentTarget.contains(e.relatedTarget as Node | null)) setOver((o) => (o === key ? null : o))
      },
      onDrop: (e: DragEvent) => {
        if (!ok) return
        e.preventDefault()
        e.stopPropagation()
        place(target)
      },
      // A tapped picture lands on the next highlighted spot tapped, before any menu inside it opens.
      onClickCapture: (e: MouseEvent) => {
        if (!ok || !carrying?.tapped) return
        e.preventDefault()
        e.stopPropagation()
        place(target)
      },
    }
  }

  const saveAll = async () => {
    if (!dirty.size) return
    setSaveState('saving')
    const done: Record<string, SavedStory> = {}
    for (const id of dirty) {
      const s: SavedStory = { ...docs[id], draftHash: DRAFT_BY_ID[id] ? storyHash(DRAFT_BY_ID[id]) : undefined }
      if (await saveStory(s, db)) done[id] = s
    }
    setSaved((m) => ({ ...m, ...done }))
    setDirty((d) => new Set([...d].filter((id) => !done[id])))
    setSaveState(Object.keys(done).length === dirty.size ? 'saved' : 'error')
  }
  const backToDraft = async () => {
    if (!DRAFT_BY_ID[story.id]) return
    if (!saved[story.id] || (await resetStory(story.id, db))) {
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
  const currentStep = frame?.step ?? 1 // 0 while the bubble opens

  return (
    <div className="studio ss">
      <header className="st-head">
        <h1>Bubble stories</h1>
        <a href="/studio">← Recipe studio</a>
        <span className="st-dim">{loaded ? (db ? 'Saved for everyone' : 'Local copy: stories stay in this browser') : 'Loading…'}</span>
        <span className="st-grow" />
        <span className={`st-save ${saveState === 'error' ? 'error' : ''}`}>{saveState === 'saving' ? 'Saving…' : saveState === 'saved' ? 'Saved' : saveState === 'error' ? 'Not saved' : dirty.size ? `${dirty.size} unsaved` : 'All saved'}</span>
        <button type="button" disabled={!dirty.size} onClick={() => void saveAll()}>Save</button>
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
        <p className="st-dim">Drag a picture onto the story on the right: a step, the cast, Props or Extra marks. Or tap a picture, then tap where it goes. Codex adds and replaces pictures; a new version reaches every story straight away.</p>
        <PictureLibrary story={story} editable={editable} carrying={carrying?.id ?? null} onCarry={setCarrying} />
      </aside>

      <main className="st-main">
        <div className="st-title">
          <h2>{story.label}</h2>
          <span className="st-dim">{story.appliesTo.label || 'No object yet'} · {compiled.seconds.toFixed(1)} s · {compiled.storyFrames} frames at {FPS} fps · {playsText(compiled.tellings)} in a 20–30 s activity</span>
          <span className="st-grow" />
          {editable && DRAFT_BY_ID[story.id] && (saved[story.id] || dirty.has(story.id)) && <button type="button" onClick={() => void backToDraft()}>Back to Claude’s draft</button>}
          <button type="button" onClick={copyJson} title="For Claude or Codex">Copy story</button>
        </div>
        {draftMoved && <p className="st-warn">Claude has updated the draft since you edited this. Your version is showing; “Back to Claude’s draft” shows the new one.</p>}

        <div className="ss-stagewrap">
          <BubbleStage frame={frame} t={f} body={bodyFrame?.url} showMarks={showMarks} showBubble={showBubble} />
          <div className="ss-beat">
            {currentStep === 0 ? 'The bubble opens' : <>Step {currentStep}: {stepText(story, story.steps[currentStep - 1])}</>}
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
          <p className="st-ok">No problems: every step can play, every touch mark lands where two pictures meet, and the story takes its time (at least 5 seconds).</p>
        )}

        <h2>How it ends</h2>
        <div className="ss-row">
          <label>When he keeps working <select disabled={!editable} value={story.afterStory} onChange={(e) => edit({ ...story, afterStory: e.target.value as Story['afterStory'] })}>{Object.entries(AFTER).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select></label>
          <label>Pace <select disabled={!editable} value={story.pace} onChange={(e) => edit({ ...story, pace: Number(e.target.value) })}>{PACES.map(([v, t]) => <option key={v} value={v}>{t}</option>)}</select></label>
          <label>Pictures move <select disabled={!editable} value={story.flow} onChange={(e) => edit({ ...story, flow: e.target.value as Flow })}>{Object.entries(FLOWS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select></label>
          {story.afterStory === 'loop' && (
            <label>Each retelling starts at <select disabled={!editable} value={story.loopFrom ?? 1} onChange={(e) => { const n = Number(e.target.value); const { loopFrom: _drop, ...rest } = story; edit(n > 1 ? { ...rest, loopFrom: n } : rest) }}>{story.steps.map((s, i) => <option key={i} value={i + 1}>step {i + 1}{i === 0 ? ' (the beginning)' : `: ${stepText(story, s)}`}</option>)}</select></label>
          )}
        </div>
      </main>

      <aside className="st-side">
        {carrying?.tapped && (
          <p className="ss-carry">
            Placing <b>{picLabel(carrying.id)}</b>: tap a highlighted spot. <button type="button" className="st-mini" onClick={() => setCarrying(null)}>Cancel</button>
          </p>
        )}
        <h2>Steps, in order</h2>
        <p className="st-dim">Drag a step, or use the arrows, to change the order. Tap a step’s number to watch it. Drop a picture on a step to make it the one acting, or a mark to use at each touch.</p>
        <ol className="ss-steps">
          {story.steps.map((s, i) => {
            const needs = VERBS[s.do].needs
            // One row is both a drop spot for library pictures and a handle for reordering steps.
            const zone = dropZone({ to: 'step', index: i }, i + 1 === currentStep ? 'on' : '')
            return (
              <li
                key={i}
                {...zone}
                draggable={editable}
                onDragStart={() => { dragFrom.current = i }}
                onDragOver={(e) => { if (carrying) zone.onDragOver(e); else e.preventDefault() }}
                onDrop={(e) => {
                  if (carrying) return zone.onDrop(e)
                  if (dragFrom.current !== null) moveStep(dragFrom.current, i)
                  dragFrom.current = null
                }}
              >
                <button type="button" className="ss-num" onClick={() => { setPlaying(false); setF(intro.length + (windowOf(i)?.start ?? 0)) }} title="Watch this step">{i + 1}</button>
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
              <li key={as} {...dropZone({ to: 'cast', as })}>
                <img src={versionFor(LIBRARY, m.picture, m.version)?.url} alt="" />
                <b>{as}</b>
                <select disabled={!editable} value={m.picture} onChange={(e) => edit({ ...story, cast: { ...story.cast, [as]: { picture: e.target.value, role: m.role } } })}><ObjectOptions /></select>
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
        {editable && <div {...dropZone({ to: 'cast' }, 'ss-dropbox')}>Drop a picture here to add it to the cast; drop it on a cast member to swap its picture</div>}
        {editable && <AddCast onAdd={(as, picture) => edit({ ...story, cast: { ...story.cast, [as]: { picture, role: 'support' } } })} taken={castNames} />}

        <h2>Extra marks</h2>
        <p className="st-dim">A mark that rides on one picture for some steps, like heat over the grill.</p>
        <ul className="ss-cast">
          {story.ambient.map((a, i) => {
            const set = (next: Ambient) => edit({ ...story, ambient: story.ambient.map((x, j) => (j === i ? next : x)) })
            return (
              <li key={i} {...dropZone({ to: 'marks', index: i })}>
                <img src={versionFor(LIBRARY, a.picture)?.url} alt="" />
                <select disabled={!editable} value={a.picture} onChange={(e) => set({ ...a, picture: e.target.value })}>{MARKS.map(([id, p]) => <option key={id} value={id}>{p.label}</option>)}</select>
                on <select disabled={!editable} value={a.on} onChange={(e) => set({ ...a, on: e.target.value })}>{castNames.map((c) => <option key={c} value={c}>{c}</option>)}</select>
                steps <input type="number" disabled={!editable} min={1} max={story.steps.length} value={a.fromStep} onChange={(e) => set({ ...a, fromStep: Number(e.target.value) })} />–<input type="number" disabled={!editable} min={1} max={story.steps.length} value={a.toStep} onChange={(e) => set({ ...a, toStep: Number(e.target.value) })} />
                {editable && <button type="button" className="st-mini" onClick={() => edit({ ...story, ambient: story.ambient.filter((_, j) => j !== i) })}>✕</button>}
              </li>
            )
          })}
        </ul>
        {editable && <div {...dropZone({ to: 'marks' }, 'ss-dropbox')}>Drop a mark here to add it, riding on the main picture</div>}
        {editable && <button type="button" className="st-add" onClick={() => edit({ ...story, ambient: [...story.ambient, { picture: MARKS[0][0], on: castNames[0], fromStep: 1, toStep: 1 }] })}>Add an extra mark</button>}
        <h2>Props</h2>
        <p className="st-dim">Small scene-setting pictures, like the BBQ tools and sauces, that circle the bubble or sit in a corner, away from the main action.</p>
        <ul className="ss-cast">
          {story.props.map((pr, i) => {
            const set = (next: Prop) => edit({ ...story, props: story.props.map((x, j) => (j === i ? next : x)) })
            return (
              <li key={i} {...dropZone({ to: 'props', index: i })}>
                <img src={versionFor(LIBRARY, pr.picture)?.url} alt="" />
                <select disabled={!editable} value={pr.picture} onChange={(e) => set({ ...pr, picture: e.target.value })}><ObjectOptions /></select>
                <select disabled={!editable} value={pr.at} onChange={(e) => set({ ...pr, at: e.target.value as PropSlot })}>{Object.entries(SLOTS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
                steps <input type="number" disabled={!editable} min={1} max={story.steps.length} value={pr.fromStep} onChange={(e) => set({ ...pr, fromStep: Number(e.target.value) })} />–<input type="number" disabled={!editable} min={1} max={story.steps.length} value={pr.toStep} onChange={(e) => set({ ...pr, toStep: Number(e.target.value) })} />
                {editable && <button type="button" className="st-mini" onClick={() => edit({ ...story, props: story.props.filter((_, j) => j !== i) })}>✕</button>}
              </li>
            )
          })}
        </ul>
        {editable && <div {...dropZone({ to: 'props' }, 'ss-dropbox')}>Drop a picture here to add it circling the bubble</div>}
        {editable && <button type="button" className="st-add" onClick={() => edit({ ...story, props: [...story.props, { picture: OBJECTS[0][0], at: 'orbit', fromStep: 1, toStep: Math.max(1, story.steps.length - 1) }] })}>Add a prop</button>}
        {story.notes && <><h2>Notes</h2><p className="st-dim">{story.notes}</p></>}
      </aside>
    </div>
  )
}

/** The library in fold-out groups, with a search box. Groups holding a picture this story uses are marked. */
function PictureLibrary({ story, editable, carrying, onCarry }: { story: Story; editable: boolean; carrying: string | null; onCarry: (c: { id: string; tapped: boolean } | null) => void }) {
  const [q, setQ] = useState('')
  const used = new Set([...Object.values(story.cast).map((m) => m.picture), ...story.ambient.map((a) => a.picture), ...story.props.map((p) => p.picture), ...story.steps.flatMap((s) => (s.mark ? [s.mark] : []))])
  const needle = q.trim().toLowerCase()
  const groups = ALL_GROUPS.map((g) => ({ ...g, pictures: needle ? g.pictures.filter(([id, p]) => id.includes(needle) || p.label.toLowerCase().includes(needle) || g.label.toLowerCase().includes(needle)) : g.pictures })).filter((g) => g.pictures.length)
  return (
    <>
      <input className="ss-search" type="search" placeholder={`Search ${Object.keys(LIBRARY.pictures).length} pictures`} value={q} onChange={(e) => setQ(e.target.value)} />
      {groups.map((g) => {
        const inStory = g.pictures.filter(([id]) => used.has(id)).length
        return (
          // A search opens every matching group; the key change resets each group's own open state when the search clears.
          <details key={`${g.label}-${needle ? 'search' : 'browse'}`} className="ss-group" open={!!needle || undefined}>
            <summary>{g.label} <small>{g.pictures.length}{inStory ? ` · ${inStory} in this story` : ''}</small></summary>
            <ul className="ss-lib">
              {g.pictures.map(([id, p]) => (
                <li
                  key={id}
                  title={p.review?.note ?? ''}
                  className={`${used.has(id) ? 'used' : ''}${carrying === id ? ' carrying' : ''}`}
                  draggable={editable}
                  onDragStart={(e) => {
                    e.dataTransfer.setData('text/plain', id)
                    e.dataTransfer.effectAllowed = 'copy'
                    onCarry({ id, tapped: false })
                  }}
                  onDragEnd={() => onCarry(null)}
                  onClick={() => editable && onCarry(carrying === id ? null : { id, tapped: true })}
                >
                  <img src={versionFor(LIBRARY, id)?.url} alt="" loading="lazy" draggable={false} />
                  <span><span>{p.label}<small> · v{p.current}{p.versions.length > 1 ? ` of ${p.versions.length}` : ''}{p.review?.status === 'rework-requested' ? ' · rework asked' : ''}</small></span><code>{id}</code></span>
                </li>
              ))}
            </ul>
          </details>
        )
      })}
      {!groups.length && <p className="st-dim">No picture matches “{q}”.</p>}
    </>
  )
}

/** Object choices for a menu, in the library's groups. */
function ObjectOptions() {
  return (
    <>
      {OBJECT_GROUPS.map((g) => (
        <optgroup key={g.label} label={g.label}>
          {g.pictures.map(([id, o]) => <option key={id} value={id}>{o.label}</option>)}
        </optgroup>
      ))}
    </>
  )
}

function AddCast({ onAdd, taken }: { onAdd: (as: string, picture: string) => void; taken: string[] }) {
  const [picture, setPicture] = useState(OBJECTS[0][0])
  const as = slug(picLabel(picture).split(' ')[0]) || 'extra'
  const name = taken.includes(as) ? `${as}-2` : as
  return (
    <div className="ss-row">
      <select value={picture} onChange={(e) => setPicture(e.target.value)}><ObjectOptions /></select>
      <button type="button" onClick={() => onAdd(name, picture)}>Add to cast</button>
    </div>
  )
}

/** The bubble over the approved rear-work keeper, drawn the same way as Codex's V2 review pages. */
export function BubbleStage({ frame, t, body, showMarks, showBubble }: { frame: Frame | undefined; t: number; body?: string; showMarks: boolean; showBubble: boolean }) {
  return (
    <div className="ss-stage">
      {body && <img className="ss-actor" src={body} alt="The keeper at work, seen from behind" />}
      <div className="ss-cloud">
        {showBubble && (
          <>
            <svg className="ss-bubble" viewBox="0 0 360 230" aria-hidden="true" style={{ opacity: frame?.bubble.opacity ?? 1 }}>
              <path d={bubbleOutline(t, frame?.bubble.scale ?? 1)} />
            </svg>
            <div className="ss-ring ss-ring1" style={{ opacity: frame?.bubble.rings?.[0] ?? frame?.bubble.opacity ?? 1 }} />
            <div className="ss-ring ss-ring2" style={{ opacity: frame?.bubble.rings?.[1] ?? frame?.bubble.opacity ?? 1 }} />
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
