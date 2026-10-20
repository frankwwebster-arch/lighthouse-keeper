import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { fpsFor } from '../game/animFps'
import { verifyPin } from '../game/remote'
import { SpriteProvider, useAnimSpeeds, useSprites } from '../ui/Sprite'
import { Mixer } from './audio'
import { joinChange, measureSheet, sheetPixels, type SheetInfo } from './bounds'
import { CATEGORIES, DRAFTS } from './drafts'
import { Inspector, KIND_LABEL } from './Inspector'
import { bridgesFor, checkSolids, type BridgeClip, cleanRecipe, compile, everyVariant, joinsOf, type Issue, type Join, hashOf, mainOf, moveStep, newCue, newId, resolveRecipe, shotAt, soundsUsed, withStep, type Bounds, type Category, type ClipInfo, type Recipe, type Step, type StepKind } from './recipe'
import { SoundLibrary } from './SoundLibrary'
import { StageView, type Sel, type SheetEntry } from './StageView'
import { deleteSound, loadStudio, resetDoc, saveDoc, saveType, soundIdFrom, uploadSound, type SavedCategory, type SavedDoc, type SoundInfo } from './store'
import { TimelineView } from './TimelineView'

type Rich = SheetEntry & { fps?: number; facing?: string; mirrorSafe?: boolean; outfit?: string; density?: number; sfxCues?: { frame: number; cue: string }[]; loop?: boolean; startPose?: string; endPose?: string }
const NOT_OUTFITS = new Set(['mosaic-privacy', 'towel-privacy', 'privacy-foam', 'party-hat-transition'])
const DRAFT_BY_ID = Object.fromEntries(DRAFTS.map((d) => [d.id, d]))

export default function StudioPage() {
  return (
    <SpriteProvider>
      <Studio />
    </SpriteProvider>
  )
}

function Studio() {
  const manifest = useSprites() as unknown as Record<string, Rich | string>
  const speeds = useAnimSpeeds().fps
  const mixer = useRef(new Mixer()).current

  // ── What is saved, and the working copies ──
  const [db, setDb] = useState(false)
  const [loaded, setLoaded] = useState(false)
  const [saved, setSaved] = useState<Record<string, SavedDoc>>({})
  const [docs, setDocs] = useState<Record<string, Recipe>>(DRAFT_BY_ID)
  const [cats, setCats] = useState<Record<string, Category>>(CATEGORIES)
  const [savedTypes, setSavedTypes] = useState<Record<string, SavedCategory>>({})
  const [sounds, setSounds] = useState<SoundInfo[]>([])
  const [pin, setPin] = useState<string | null>(null)
  const [typed, setTyped] = useState('')
  const [pinWrong, setPinWrong] = useState(false)
  const [dirty, setDirty] = useState<Set<string>>(new Set())
  const [saveState, setSaveState] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle')
  const [busySound, setBusySound] = useState<string | null>(null)
  const [message, setMessage] = useState<string | null>(null)

  useEffect(() => {
    void loadStudio().then((r) => {
      setDb(r.db)
      setSaved(r.saved)
      setDocs({ ...DRAFT_BY_ID, ...r.saved })
      setSavedTypes(r.types)
      setCats({ ...CATEGORIES, ...r.types })
      setSounds(r.sounds)
      setLoaded(true)
    })
  }, [])

  // ── Selection, playback ──
  const [docId, setDocId] = useState(() => (typeof location !== 'undefined' && location.hash.slice(1)) || 'armchair_nap')
  const [sel, setSel] = useState<Sel | null>({ type: 'recipe' })
  const [t, setT] = useState(0)
  const [playing, setPlaying] = useState(false)
  const [rate, setRate] = useState(1)
  const [looping, setLooping] = useState(false)
  const [mainCut, setMainCut] = useState<number | undefined>()
  const [zoom, setZoom] = useState(4)
  const [pps, setPps] = useState(60)
  const [filter, setFilter] = useState('')
  const [showRoute, setShowRoute] = useState(true)
  const [showGhosts, setShowGhosts] = useState(false)
  const [evening, setEvening] = useState(false)
  const doc = docs[docId] ?? DRAFTS[0]
  useEffect(() => {
    if (typeof history !== 'undefined') history.replaceState(null, '', `#${doc.id}`)
  }, [doc.id])

  // ── Clips, from the sprite manifest (speeds as the sheets say, plus any grown-ups' tweak) ──
  const sheet = useCallback((name: string): SheetEntry | undefined => {
    const e = manifest[name]
    return e && typeof e !== 'string' && e.w ? e : undefined
  }, [manifest])
  const lookup = useCallback((name: string): ClipInfo | undefined => {
    const e = manifest[name]
    if (!e || typeof e === 'string' || !e.w) return undefined
    const drawn = e.fps ?? 4
    return { w: e.w, h: e.h, frames: e.frames ?? 1, fps: fpsFor(speeds, name, drawn), anchor: e.anchor ?? [Math.round(e.w / 2), e.h], native: e.facing?.includes('left') ? 'left' : e.facing?.includes('right') ? 'right' : null, mirrorSafe: !!e.mirrorSafe, sfxCues: Array.isArray(e.sfxCues) ? e.sfxCues : undefined, closed: name.endsWith('_cycle') && e.loop !== false, startPose: e.startPose, endPose: e.endPose, outfit: e.outfit }
  }, [manifest, speeds])
  const clipNames = useMemo(() => Object.keys(manifest).filter((k) => k.startsWith('keeper_')).sort(), [manifest])
  const outfits = useMemo(() => ['standard', ...[...new Set(Object.values(manifest).flatMap((e) => (typeof e !== 'string' && e.outfit && !NOT_OUTFITS.has(e.outfit) ? [e.outfit] : [])))].sort()], [manifest])

  const macros = useMemo(() => Object.fromEntries(Object.values(docs).filter((d) => d.kind === 'macro').map((d) => [d.id, d])), [docs])
  // The recipe with each typed object filled in from its variant: what plays and what is checked.
  const resolved = useMemo(() => resolveRecipe(doc, cats), [doc, cats])
  const live = resolved.recipe
  const tl = useMemo(() => compile(live, macros, lookup, { mainSeconds: mainCut }), [live, macros, lookup, mainCut])

  // ── Each frame's real pixels, for the "covered by something in front" check ──
  const [bounds, setBounds] = useState<Record<string, (Bounds | null)[]>>({})
  useEffect(() => {
    for (const clip of new Set(tl.segments.flatMap((s) => (s.clip ? [s.clip] : [])))) {
      const e = manifest[clip]
      if (bounds[clip] || !e || typeof e === 'string') continue
      void measureSheet({ file: e.file, w: e.w, h: e.h, frames: e.frames ?? 1, anchor: e.anchor ?? [Math.round(e.w / 2), e.h], density: e.density ?? 1 }).then((b) => setBounds((m) => ({ ...m, [clip]: b })))
    }
  }, [tl, manifest, bounds])
  const ready = Object.keys(manifest).length > 0
  const boundsOf = useCallback((clip: string, frame: number) => bounds[clip]?.[frame] ?? null, [bounds])
  const issues = useMemo(() => (ready ? checkSolids(live, tl, boundsOf) : []), [ready, live, tl, boundsOf])
  const problems = ready ? [...new Set([...resolved.problems, ...tl.problems])] : []
  // The same recipe with every variant of every typed object: one recipe must work for all three ovens.
  const variants = useMemo(() => (ready ? everyVariant(doc, cats).map(({ object, variant, recipe }) => {
    const r = resolveRecipe(recipe, cats).recipe
    const vtl = compile(r, macros, lookup)
    return { object, variant, count: vtl.problems.length + checkSolids(r, vtl, boundsOf).length }
  }) : []), [ready, doc, cats, macros, lookup, boundsOf])

  // Every handover between two clips, compared pixel for pixel: a jump there is the flash you see.
  const sheetInfo = useCallback((name: string): SheetInfo | null => {
    const e = manifest[name]
    return e && typeof e !== 'string' && e.w ? { file: e.file, w: e.w, h: e.h, frames: e.frames ?? 1, anchor: e.anchor ?? [Math.round(e.w / 2), e.h], density: e.density ?? 1 } : null
  }, [manifest])
  const joins = useMemo(() => (ready ? joinsOf(tl) : []), [ready, tl])
  const joinKey = (j: Join) => [j.a.clip, j.aFrame, j.ax, j.a.dy, j.a.mirror, j.b.clip, j.bFrame, j.bx, j.b.dy, j.b.mirror].join('|')
  const [changes, setChanges] = useState<Record<string, number>>({})
  useEffect(() => {
    let alive = true
    for (const j of joins) {
      const key = joinKey(j)
      const a = sheetInfo(j.a.clip!)
      const b = sheetInfo(j.b.clip!)
      if (key in changes || !a || !b) continue
      void Promise.all([sheetPixels(a), sheetPixels(b)]).then(([pa, pb]) => {
        if (alive && pa && pb) setChanges((m) => ({ ...m, [key]: joinChange(pa, j.aFrame, j.ax, j.a.dy, j.a.mirror, pb, j.bFrame, j.bx, j.b.dy, j.b.mirror) }))
      })
    }
    return () => {
      alive = false
    }
  }, [joins, sheetInfo, changes])
  const JOIN_OK = 3
  const joinIssues: (Issue & { join: Join; change: number })[] = joins.flatMap((j) => {
    const change = changes[joinKey(j)]
    if (change === undefined || (change <= JOIN_OK && j.ax === j.bx)) return []
    const shift = j.ax !== j.bx ? `, and his feet jump ${Math.abs(j.bx - j.ax)} px` : ''
    return [{ time: j.time, stepId: j.b.stepId, kind: 'seam' as const, join: j, change, text: `jump between ${j.a.label} and ${j.b.label}: ${change}% of him changes in one frame${shift} (${j.a.clip} frame ${j.aFrame + 1} → ${j.b.clip} frame ${j.bFrame + 1})` }]
  })
  const allIssues: (Issue & { join?: Join; change?: number })[] = [...issues, ...joinIssues].sort((a, b) => a.time - b.time)
  const keeperClips = useMemo(() => clipNames.flatMap((name) => { const info = lookup(name); return info ? [{ name, info }] : [] }), [clipNames, lookup])
  const [look, setLook] = useState<Join | null>(null)
  const [bridgesOpen, setBridgesOpen] = useState<number | null>(null)
  const nameOf = (b: BridgeClip) => `${b.name.replace(/^keeper_/, '').replace(/_/g, ' ')}${b.reverse ? ' backwards' : ''}${b.mirror ? ' flipped' : ''}`
  const insertBridge = (j: Join, chain: BridgeClip[]) => {
    if (j.a.stepId === j.b.stepId) return setMessage('This join is inside one step or macro: open the macro to add a bridge there.')
    const i = doc.steps.findIndex((s) => s.id === j.b.stepId)
    if (i < 0) return
    // A flipped clip plays facing the other way from how it was drawn.
    const added: Step[] = chain.map((b) => ({ id: newId('bridge'), kind: 'play', clip: b.name, reverse: b.reverse, facing: (lookup(b.name)?.native === 'left') !== b.mirror ? 'left' : 'right', label: `Bridge: ${nameOf(b)}` }))
    edit({ ...doc, steps: [...doc.steps.slice(0, i), ...added, ...doc.steps.slice(i)] })
    setBridgesOpen(null)
    setMessage(`Added a bridge before “${doc.steps[i].label ?? doc.steps[i].kind}”.`)
  }
  const noteForCodex = (j: Join, change: number) => {
    const line = `Join at ${j.time.toFixed(2)}s: ${j.a.clip} frame ${j.aFrame + 1} → ${j.b.clip} frame ${j.bFrame + 1} changes ${change}%${j.ax !== j.bx ? ` and shifts ${Math.abs(j.bx - j.ax)} px` : ''}. Needs ${j.aPose && j.bPose && j.aPose !== j.bPose ? `a bridge from ${j.aPose} to ${j.bPose}` : `matching end frames (both should be ${j.aPose ?? 'the same pose'})`}.`
    edit({ ...doc, notes: doc.notes ? `${doc.notes}\n${line}` : line })
    setMessage('Added to the recipe’s notes for Codex.')
  }

  const shot = shotAt(tl, t, live)
  const main = mainOf(tl)

  // ── The clock ──
  const clock = useRef({ start: 0, from: 0 })
  const tRef = useRef(t)
  tRef.current = t
  const soundUrl = useCallback((id: string) => sounds.find((s) => s.id === id)?.url, [sounds])
  useEffect(() => {
    if (!playing) return
    clock.current = { start: performance.now(), from: tRef.current >= tl.duration - 1e-3 ? 0 : tRef.current }
    if (rate === 1) void mixer.play(tl.cues, clock.current.from, soundUrl)
    let raf = 0
    const tick = () => {
      const now = clock.current.from + ((performance.now() - clock.current.start) / 1000) * rate
      if (now >= tl.duration) {
        if (looping) {
          mixer.stop()
          setMainCut(undefined)
          clock.current = { start: performance.now(), from: 0 }
          setT(0)
          if (rate === 1) void mixer.play(tl.cues, 0, soundUrl)
        } else {
          setT(tl.duration)
          setPlaying(false)
          return
        }
      } else setT(now)
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => {
      cancelAnimationFrame(raf)
      mixer.stop()
    }
  }, [playing, tl, rate, looping, mixer, soundUrl])

  const seek = (to: number) => {
    setPlaying(false)
    setT(Math.max(0, Math.min(tl.duration, to)))
  }
  const restart = () => {
    setMainCut(undefined)
    setT(0)
    setPlaying(true)
  }
  const stopNow = () => {
    if (!main || t < main.start || t >= main.end) return
    setMainCut(t - main.start)
  }
  const frameStep = (dir: 1 | -1) => {
    const fps = shot.info?.fps ?? 8
    seek(t + dir / fps + (dir > 0 ? 1e-4 : 0))
  }

  // ── Editing and saving ──
  const edit = (next: Recipe) => {
    if (!pin) return
    setDocs((d) => ({ ...d, [next.id]: next }))
    setDirty((s) => new Set(s).add(next.id))
  }
  const docsRef = useRef(docs)
  docsRef.current = docs
  const catsRef = useRef(cats)
  catsRef.current = cats
  const editType = (next: Category) => {
    if (!pin) return
    setCats((c) => ({ ...c, [next.id]: next }))
    setDirty((s) => new Set(s).add(`cat-${next.id}`))
  }
  useEffect(() => {
    if (!pin || !dirty.size) return
    const timer = setTimeout(async () => {
      setSaveState('saving')
      const ids = [...dirty]
      setDirty(new Set())
      let ok = true
      const done: Record<string, SavedDoc> = {}
      for (const id of ids) {
        if (id.startsWith('cat-')) {
          const c = catsRef.current[id.slice(4)]
          const draft = CATEGORIES[c.id]
          const s: SavedCategory = { ...c, draftHash: savedTypes[c.id]?.draftHash ?? (draft ? hashOf(draft) : undefined) }
          if (await saveType(pin, s, db)) setSavedTypes((m) => ({ ...m, [c.id]: s }))
          else ok = false
          continue
        }
        const d = docsRef.current[id]
        const draft = DRAFT_BY_ID[id]
        const s: SavedDoc = { ...d, draftHash: saved[id]?.draftHash ?? (draft ? hashOf(draft) : undefined) }
        if (await saveDoc(pin, s, db)) done[id] = s
        else ok = false
      }
      setSaved((m) => ({ ...m, ...done }))
      setSaveState(ok ? 'saved' : 'error')
    }, 700)
    return () => clearTimeout(timer)
  }, [dirty, pin, db, saved, savedTypes])

  const unlock = async () => {
    if (await verifyPin(typed, db)) {
      setPin(typed)
      setPinWrong(false)
    } else setPinWrong(true)
    setTyped('')
  }
  const resetToDraft = async () => {
    if (!pin || !DRAFT_BY_ID[doc.id] || !confirm('Throw away your changes to this one and go back to the draft?')) return
    if (await resetDoc(pin, doc.id, db)) {
      setSaved((m) => {
        const n = { ...m }
        delete n[doc.id]
        return n
      })
      setDocs((d) => ({ ...d, [doc.id]: DRAFT_BY_ID[doc.id] }))
    }
  }
  const create = (kind: 'recipe' | 'macro', from?: Recipe) => {
    if (!pin) return
    const name = prompt(kind === 'macro' ? 'Name for the new macro' : 'Name for the new recipe', from ? `${from.title} (copy)` : '')
    if (!name) return
    const id = soundIdFrom(name)
    if (docs[id]) return setMessage(`There is already one called ${id}.`)
    const base = from ? { ...from } : cleanRecipe({ id, kind, title: name, steps: kind === 'recipe' ? [{ id: 'enter', kind: 'macro', macro: 'enter_room', label: 'Enter the room', params: { swapTo: '' } }, { id: 'go', kind: 'walk', to: 'action', label: 'Walk to it' }, { id: 'leave', kind: 'macro', macro: 'leave_room', label: 'Leave the room' }] : [] })!
    const next: Recipe = { ...base, id, kind, title: name, status: 'draft' }
    setDocs((d) => ({ ...d, [id]: next }))
    setDirty((s) => new Set(s).add(id))
    setDocId(id)
    setSel({ type: 'recipe' })
  }
  const addStep = (kind: StepKind, macro?: string) => {
    const s: Step = { id: newId('step'), kind, label: macro ? macros[macro]?.title : KIND_LABEL[kind] }
    if (kind === 'walk') s.to = 'action'
    if (kind === 'loop' || kind === 'wait') s.seconds = 2
    if (kind === 'hide') Object.assign(s, { through: 'door', seconds: 0.6 })
    if (macro) Object.assign(s, { macro, params: { swapTo: '' } })
    const i = sel?.type === 'step' ? doc.steps.findIndex((x) => x.id === sel.id) + 1 : doc.steps.length
    edit({ ...doc, steps: [...doc.steps.slice(0, i), s, ...doc.steps.slice(i)] })
    setSel({ type: 'step', id: s.id })
  }
  const addCue = (time: number, sound: string) => {
    const span = tl.steps.find((s) => time >= s.start && time < s.end) ?? tl.steps[tl.steps.length - 1]
    if (!span) return
    const c = newCue(sound, time - span.start)
    edit(withStep(doc, span.id, (s) => ({ ...s, cues: [...(s.cues ?? []), c] })))
    setSel({ type: 'cue', stepId: span.id, cueId: c.id })
  }
  const upload = async (file: File, as?: string) => {
    if (!pin) return setMessage('Unlock with the PIN to add sounds.')
    const id = as ?? soundIdFrom(file.name)
    setBusySound(id)
    const r = await uploadSound(pin, id, file, db)
    setBusySound(null)
    if ('error' in r) return setMessage(r.error)
    setSounds((list) => [...list.filter((s) => s.id !== id), r])
    setMessage(as ? `${file.name} now plays wherever “${id}” is cued.` : `Added ${id}.`)
    return id
  }

  // ── Keys: space plays, , and . step a frame, arrows nudge ──
  useEffect(() => {
    const key = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement).tagName
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return
      if (e.key === ' ') {
        e.preventDefault()
        setPlaying((p) => !p)
      } else if (e.key === ',') frameStep(-1)
      else if (e.key === '.') frameStep(1)
      else if (e.key.startsWith('Arrow') && pin) {
        const by = e.shiftKey ? 5 : 1
        const dx = e.key === 'ArrowLeft' ? -by : e.key === 'ArrowRight' ? by : 0
        const dy = e.key === 'ArrowUp' ? by : e.key === 'ArrowDown' ? -by : 0
        if (sel?.type === 'step') {
          e.preventDefault()
          edit(withStep(doc, sel.id, (s) => ({ ...s, dx: (s.dx ?? 0) + dx, dy: (s.dy ?? 0) + dy })))
        } else if (sel?.type === 'object' && dx) {
          e.preventDefault()
          edit({ ...doc, objects: doc.objects.map((o) => (o.id === sel.id ? { ...o, x: o.x + dx } : o)) })
        }
      } else if (e.key === 'Escape') setSel({ type: 'recipe' })
    }
    window.addEventListener('keydown', key)
    return () => window.removeEventListener('keydown', key)
  })

  const all = Object.values(docs).sort((a, b) => a.title.localeCompare(b.title))
  const shown = all.filter((d) => (d.title + d.id).toLowerCase().includes(filter.toLowerCase()))
  const placeholders = [...new Set([...soundsUsed(Object.values(docs)), ...tl.cues.map((c) => c.sound)])].sort().filter((s) => !sounds.some((x) => x.id === s))
  const draftMoved = saved[doc.id]?.draftHash && DRAFT_BY_ID[doc.id] && saved[doc.id].draftHash !== hashOf(DRAFT_BY_ID[doc.id])
  const editable = !!pin

  return (
    <div className="studio">
      <header className="st-head">
        <a href="/">← Game</a>
        <h1>Recipe studio</h1>
        <a href="/studio/stories">Bubble stories →</a>
        <span className="st-dim">{loaded ? (db ? 'Saved for everyone' : 'Local copy: recipes stay in this browser, sounds until you close it') : 'Loading…'}</span>
        <span className="st-grow" />
        {editable ? (
          <span className={`st-save ${saveState}`}>{dirty.size ? 'Unsaved changes' : saveState === 'saving' ? 'Saving…' : saveState === 'error' ? 'Could not save' : saveState === 'saved' ? 'All changes saved' : 'Unlocked'}</span>
        ) : (
          <form className="st-pin" onSubmit={(e) => { e.preventDefault(); void unlock() }}>
            <input type="password" inputMode="numeric" placeholder="PIN to edit" value={typed} onChange={(e) => setTyped(e.target.value)} />
            <button type="submit">Unlock</button>
            {pinWrong && <b>Not right</b>}
          </form>
        )}
      </header>
      {message && <div className="st-message" onClick={() => setMessage(null)}>{message} <small>(click to close)</small></div>}

      <aside className="st-list">
        <input type="search" placeholder="Find a recipe" value={filter} onChange={(e) => setFilter(e.target.value)} />
        {(['recipe', 'macro'] as const).map((kind) => (
          <section key={kind}>
            <h2>{kind === 'recipe' ? 'Recipes' : 'Macros (reusable)'}</h2>
            <ul>
              {shown.filter((d) => d.kind === kind).map((d) => (
                <li key={d.id}>
                  <button type="button" className={d.id === doc.id ? 'on' : ''} onClick={() => { setDocId(d.id); setSel({ type: 'recipe' }); setT(0); setPlaying(false); setMainCut(undefined) }}>
                    <i className={`st-status ${d.status}`} title={d.status} />
                    {d.title}
                    {saved[d.id] && <small> · edited</small>}
                  </button>
                </li>
              ))}
            </ul>
            {editable && <button type="button" className="st-add" onClick={() => create(kind)}>New {kind}</button>}
          </section>
        ))}
        <h2>Sounds</h2>
        <SoundLibrary sounds={sounds} placeholders={placeholders} editable={editable} busy={busySound} onUpload={(f, as) => void upload(f, as)} onDelete={async (id) => { if (pin && (await deleteSound(pin, id, db))) setSounds((l) => l.filter((s) => s.id !== id)) }} onPreview={(id) => void mixer.preview({ sound: id, trimStart: 0, trimEnd: null, volume: 1, loop: false }, soundUrl(id))} />
      </aside>

      <main className="st-main">
        <div className="st-title">
          <h2>{doc.title}</h2>
          <select value={doc.status} disabled={!editable} onChange={(e) => edit({ ...doc, status: e.target.value as Recipe['status'] })} className={`st-statussel ${doc.status}`}>
            <option value="draft">Draft</option>
            <option value="needs-work">Needs work</option>
            <option value="approved">Approved</option>
          </select>
          {editable && saved[doc.id] && DRAFT_BY_ID[doc.id] && <button type="button" onClick={() => void resetToDraft()}>Back to the draft</button>}
          {editable && <button type="button" onClick={() => create(doc.kind, doc)}>Duplicate</button>}
          <button type="button" onClick={() => void navigator.clipboard?.writeText(JSON.stringify(doc, null, 2)).then(() => setMessage('Copied as JSON.'), () => setMessage('Could not copy.'))}>Copy JSON</button>
        </div>
        {draftMoved && <p className="st-warn">The draft has been updated since you edited this. Your version is showing; “Back to the draft” shows theirs.</p>}

        <div className="st-stagewrap">
          <StageView doc={live} shot={shot} tl={tl} look={look ? { e: sheet(look.a.clip!), frame: look.aFrame, x: look.ax, y: look.a.dy, mirror: look.a.mirror } : null} showRoute={showRoute} showGhosts={showGhosts} evening={evening} zoom={zoom} sel={sel} sheet={sheet} editable={editable} onSelect={setSel} onObjectX={(id, x) => edit({ ...doc, objects: doc.objects.map((o) => (o.id === id ? { ...o, x } : o)) })} onActionDx={(dx) => edit({ ...doc, action: { ...doc.action, dx: dx - (live.action.dx - doc.action.dx) } })} />
        </div>

        <div className="st-transport">
          <button type="button" onClick={restart} title="From the start">⏮</button>
          <button type="button" className="st-play" onClick={() => setPlaying((p) => !p)}>{playing ? '⏸ Pause' : '▶ Play'}</button>
          <button type="button" onClick={() => frameStep(-1)} title="Back one frame (,)">◀ frame</button>
          <button type="button" onClick={() => frameStep(1)} title="Forward one frame (.)">frame ▶</button>
          <button type="button" className="st-stop" disabled={!main || t < main.start || t >= main.end} onClick={stopNow} title="As if the player gave another order">✋ Stop now</button>
          <label><input type="checkbox" checked={looping} onChange={(e) => setLooping(e.target.checked)} /> Loop</label>
          <label title="His whole route, worked out from where things are"><input type="checkbox" checked={showRoute} onChange={(e) => setShowRoute(e.target.checked)} /> Route</label>
          <label title="Faint copies of him at each stop"><input type="checkbox" checked={showGhosts} onChange={(e) => setShowGhosts(e.target.checked)} /> Ghosts</label>
          <label title="Dark outside: the room is lit only while its door is open"><input type="checkbox" checked={evening} onChange={(e) => setEvening(e.target.checked)} /> Evening</label>
          <select value={rate} onChange={(e) => setRate(Number(e.target.value))} title="Speed (sound plays at full speed only)">
            <option value={1}>1×</option>
            <option value={0.5}>½×</option>
            <option value={0.25}>¼×</option>
          </select>
          <span className="st-readout">
            {t.toFixed(2)} / {tl.duration.toFixed(2)}s · {shot.visible ? `${shot.clip ?? '—'} ${shot.info ? `frame ${shot.frame + 1}/${shot.info.frames} @ ${shot.info.fps}fps` : ''}` : 'hidden in the doorway'} · {shot.outfit} · x {shot.x}
          </span>
          <span className="st-grow" />
          <label>Size <select value={zoom} onChange={(e) => setZoom(Number(e.target.value))}>{[2, 3, 4, 5, 6, 8].map((z) => <option key={z} value={z}>{z}×</option>)}</select></label>
          <label>Timeline <select value={pps} onChange={(e) => setPps(Number(e.target.value))}>{[30, 60, 120, 240].map((z) => <option key={z} value={z}>{z} px/s</option>)}</select></label>
        </div>

        <TimelineView tl={tl} t={t} pps={pps} sel={sel} issues={allIssues} soundLength={(s) => (s && sounds.some((x) => x.id === s) ? 1 : 0.2)} onSeek={seek} onSelect={setSel} onMoveCue={(stepId, cueId, at) => edit(withStep(doc, stepId, (s) => ({ ...s, cues: (s.cues ?? []).map((c) => (c.id === cueId ? { ...c, at } : c)) })))} onDropSound={(time, s) => editable ? addCue(time, s) : setMessage('Unlock with the PIN to add sounds.')} onDropFile={async (time, f) => { const id = await upload(f); if (id) addCue(time, id) }} />

        {(problems.length > 0 || allIssues.length > 0) && (
          <ul className="st-problems">
            {problems.map((p) => <li key={p}>{p}</li>)}
            {allIssues.map((i, k) => {
              const j = i.join ? { join: i.join, change: i.change ?? 0 } : null
              const bridges = j ? bridgesFor(j.join, keeperClips) : []
              return (
                <li key={k}>
                  <button type="button" className="st-link" onClick={() => { seek(i.time); setSel({ type: 'step', id: i.stepId }) }}>{i.time.toFixed(2)}s</button> {i.kind === 'walk' ? '🚧' : i.kind === 'seam' ? '⚡' : i.kind === 'swap' ? '👀' : i.kind === 'place' ? '🚪' : '🙈'} {i.text}
                  {j && (
                    <span className="st-fixes">
                      <button type="button" className="st-mini" onClick={() => { setPlaying(false); setT(Math.max(0, j.join.time + 1e-4)); setLook(look === j.join ? null : j.join) }}>{look === j.join ? 'Stop looking' : 'Look'}</button>
                      {editable && <button type="button" className="st-mini" onClick={() => setBridgesOpen(bridgesOpen === k ? null : k)}>Bridges ({bridges.length})</button>}
                      {editable && <button type="button" className="st-mini" onClick={() => noteForCodex(j.join, j.change)}>Note for Codex</button>}
                    </span>
                  )}
                  {j && bridgesOpen === k && (
                    <div className="st-bridges">
                      {j.join.aPose && j.join.bPose ? <small>From <b>{j.join.aPose}</b> to <b>{j.join.bPose}</b>:</small> : <small>These clips have no recorded poses, so no bridge can be suggested.</small>}
                      {bridges.map((chain) => <button key={chain.map(nameOf).join('+')} type="button" className="st-mini" onClick={() => insertBridge(j.join, chain)}>{chain.map(nameOf).join(' → ')}</button>)}
                      {j.join.aPose && j.join.bPose && !bridges.length && <small>{j.join.aPose === j.join.bPose ? 'Same pose both sides, so the frames themselves differ: a note for Codex is the fix.' : 'No clip makes this move yet: a note for Codex is the fix.'}</small>}
                    </div>
                  )}
                </li>
              )
            })}
          </ul>
        )}
        {variants.length > 0 && (
          <div className="st-variants">
            <b>Every variant:</b>
            {variants.map(({ object, variant, count }) => (
              <button key={object.id + variant.id} type="button" className={`${count ? 'bad' : 'good'} ${(object.variant ?? cats[object.category!]?.variants[0].id) === variant.id ? 'on' : ''}`} onClick={() => setDocs((d) => ({ ...d, [doc.id]: { ...doc, objects: doc.objects.map((o) => (o.id === object.id ? { ...o, variant: variant.id } : o)) } }))} title="Show the recipe with this one (not saved unless you change something else)">
                {cats[object.category!]?.label}: {variant.label} {count ? `· ${count} problem${count > 1 ? 's' : ''}` : '✓'}
              </button>
            ))}
          </div>
        )}
        {ready && !problems.length && !allIssues.length && <p className="st-ok">No problems: every join between clips matches, he never walks into anything solid, nothing in front of him covers him while he can be seen, and his costume only changes out of sight.</p>}
      </main>

      <aside className="st-side">
        <h2>Steps</h2>
        <ol className="st-steps">
          {doc.steps.map((s) => (
            <li key={s.id} className={`${sel?.type === 'step' && sel.id === s.id ? 'on' : ''} ${issues.some((i) => i.stepId === s.id) ? 'bad' : ''}`}>
              <button type="button" className="st-steplabel" onClick={() => { setSel({ type: 'step', id: s.id }); seek(tl.steps.find((x) => x.id === s.id)?.start ?? 0) }}>
                <small>{s.kind === 'macro' ? '▸ macro' : KIND_LABEL[s.kind]}</small>
                {s.label ?? s.kind}{s.main ? ' ★' : ''}{(s.cues ?? []).length ? ` ♪${s.cues!.length}` : ''}
              </button>
              {editable && (
                <span>
                  <button type="button" className="st-mini" onClick={() => edit(moveStep(doc, s.id, -1))} title="Earlier">↑</button>
                  <button type="button" className="st-mini" onClick={() => edit(moveStep(doc, s.id, 1))} title="Later">↓</button>
                </span>
              )}
            </li>
          ))}
        </ol>
        {editable && (
          <div className="st-addstep">
            <select value="" onChange={(e) => { const v = e.target.value; if (!v) return; if (v.startsWith('macro:')) addStep('macro', v.slice(6)); else addStep(v as StepKind) }}>
              <option value="">Add a step…</option>
              {(['walk', 'play', 'loop', 'wait', 'hide'] as const).map((k) => <option key={k} value={k}>{KIND_LABEL[k]}</option>)}
              {Object.values(macros).filter((m) => m.id !== doc.id).map((m) => <option key={m.id} value={`macro:${m.id}`}>Macro: {m.title}</option>)}
            </select>
          </div>
        )}
        <Inspector doc={doc} live={live} cats={cats} onType={editType} sel={sel} macros={Object.values(macros)} clips={clipNames} outfits={outfits} sounds={[...sounds.map((s) => ({ id: s.id, url: s.url })), ...placeholders.map((id) => ({ id }))]} mixer={mixer} editable={editable} onChange={edit} onSelect={(s) => setSel(s ?? { type: 'recipe' })} onOpenMacro={(id) => { setDocId(id); setSel({ type: 'recipe' }); setT(0) }} />
        <datalist id="st-clips">{clipNames.map((c) => <option key={c} value={c} />)}</datalist>
        <datalist id="st-sounds">{[...sounds.map((s) => s.id), ...placeholders].map((s) => <option key={s} value={s} />)}</datalist>
      </aside>
    </div>
  )
}
