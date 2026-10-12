'use client'

import { useEffect, useMemo, useRef, useState, type CSSProperties } from 'react'
import styles from './workbench.module.css'
import { copyTimelineEntry, copyToDraft, expandTimeline, itemPlayback, loopConflicts, moveTimelineEntry, reconcileDraftLibrary, removeTimelineEntry, resolvedLoops, transitionPlayback, transitionWarnings, type PlaybackFrame, type SectionLoop, type SpriteAsset, type WorkbenchCatalogue, type WorkbenchItem } from './model'

const STORAGE_KEY = 'keeper-animation-workbench:v3'

function uid(prefix: string) {
  return `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`
}

function SpriteFrame({ asset, frame, mirror = false, compact = false }: { asset: SpriteAsset; frame: number; mirror?: boolean; compact?: boolean }) {
  const position = asset.frames <= 1 ? 0 : (Math.max(0, Math.min(asset.frames - 1, frame)) / (asset.frames - 1)) * 100
  const style: CSSProperties = {
    aspectRatio: `${asset.w} / ${asset.h}`,
    backgroundImage: `url(${asset.file})`,
    backgroundSize: `${asset.frames * 100}% 100%`,
    backgroundPosition: `${position}% 0`,
    transform: mirror ? 'scaleX(-1)' : undefined,
  }
  return <span className={`${styles.sprite} ${compact ? styles.spriteCompact : ''}`} style={style} role="img" aria-label={`${asset.name} frame ${frame + 1}${mirror ? ', mirrored' : ''}`} />
}

function Preview({ title, sequence, assets, loop, onLoopChange, empty }: {
  title: string
  sequence: PlaybackFrame[]
  assets: Map<string, SpriteAsset>
  loop: boolean
  onLoopChange: (next: boolean) => void
  empty?: string
}) {
  const [index, setIndex] = useState(0)
  const [playing, setPlaying] = useState(false)
  useEffect(() => {
    setIndex(0)
    setPlaying(false)
  }, [sequence])
  useEffect(() => {
    if (!playing || !sequence.length) return
    const current = sequence[Math.min(index, sequence.length - 1)]
    const timer = window.setTimeout(() => {
      if (index + 1 < sequence.length) setIndex(index + 1)
      else if (loop) setIndex(0)
      else setPlaying(false)
    }, Math.max(40, Math.round(1000 / Math.max(1, current.fps))))
    return () => window.clearTimeout(timer)
  }, [index, playing, loop, sequence])
  const current = sequence[Math.min(index, Math.max(0, sequence.length - 1))]
  const asset = current ? assets.get(current.assetId) : undefined
  const entryDoor = sequence.find((frame) => frame.entryOcclusion)?.entryOcclusion
  const rootPositions = sequence.flatMap((frame) => frame.rootPosition === undefined ? [] : [frame.rootPosition])
  const rootMin = rootPositions.length ? Math.min(...rootPositions) : 0
  const rootMax = rootPositions.length ? Math.max(...rootPositions) : 0
  const hasRootMotion = rootMax !== rootMin
  const rootProgress = current?.rootPosition === undefined || !hasRootMotion ? 0.5 : (current.rootPosition - rootMin) / (rootMax - rootMin)
  const actorPosition = entryDoor
    ? entryDoor === 'door-right' ? 92 - rootProgress * 42 : 8 + rootProgress * 42
    : 24 + rootProgress * 36
  return (
    <section className={styles.previewPanel}>
      <div className={styles.sectionHeading}>
        <div><h2>{title}</h2>{current && <p>{current.label} · frame {current.frame + 1} · step {index + 1}/{sequence.length}</p>}</div>
        <label className={styles.check}><input type="checkbox" checked={loop} onChange={(event) => onLoopChange(event.target.checked)} /> Loop</label>
      </div>
      <div className={styles.stage}>
        {asset && current ? <div className={entryDoor || hasRootMotion ? styles.routeActor : styles.staticActor} style={entryDoor || hasRootMotion ? { left: `${actorPosition}%` } : undefined}><SpriteFrame asset={asset} frame={current.frame} mirror={current.mirror} /></div> : <p>{empty ?? 'No frames in this preview.'}</p>}
        {entryDoor && <div className={`${styles.doorMask} ${entryDoor === 'door-left' ? styles.doorLeft : styles.doorRight}`} aria-hidden="true"><span>hidden lead-in</span></div>}
      </div>
      <div className={styles.transport}>
        <button type="button" className={styles.primaryButton} disabled={!sequence.length} onClick={() => setPlaying((value) => !value)}>{playing ? 'Pause' : 'Play'}</button>
        <button type="button" disabled={!sequence.length} onClick={() => { setPlaying(false); setIndex(0) }}>Restart</button>
        <button type="button" disabled={!sequence.length} onClick={() => { setPlaying(false); setIndex((value) => Math.max(0, value - 1)) }}>Previous frame</button>
        <button type="button" disabled={!sequence.length} onClick={() => { setPlaying(false); setIndex((value) => Math.min(sequence.length - 1, value + 1)) }}>Next frame</button>
      </div>
      <input className={styles.scrubber} aria-label={`${title} playhead`} type="range" min={0} max={Math.max(0, sequence.length - 1)} value={Math.min(index, Math.max(0, sequence.length - 1))} onChange={(event) => { setPlaying(false); setIndex(Number(event.target.value)) }} />
    </section>
  )
}

function downloadJson(filename: string, value: unknown) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2) + '\n'], { type: 'application/json' }))
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  anchor.click()
  URL.revokeObjectURL(url)
}

export default function AnimationWorkbench() {
  const [catalogue, setCatalogue] = useState<WorkbenchCatalogue | null>(null)
  const [loadError, setLoadError] = useState('')
  const [drafts, setDrafts] = useState<WorkbenchItem[]>([])
  const [storageReady, setStorageReady] = useState(false)
  const [lane, setLane] = useState<'final' | 'draft'>('final')
  const [selectedId, setSelectedId] = useState('')
  const [selectedFrameId, setSelectedFrameId] = useState('')
  const [filter, setFilter] = useState('')
  const [message, setMessage] = useState('')
  const [previewLoop, setPreviewLoop] = useState(false)
  const [routeLoop, setRouteLoop] = useState(false)
  const [loopStart, setLoopStart] = useState('')
  const [loopEnd, setLoopEnd] = useState('')
  const [loopRepeats, setLoopRepeats] = useState(3)
  const importRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    let savedDrafts: WorkbenchItem[] = []
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      if (saved) {
        const parsed = JSON.parse(saved) as { drafts?: WorkbenchItem[] }
        if (Array.isArray(parsed.drafts)) savedDrafts = parsed.drafts
      }
    } catch {
      setMessage('The saved Draft library could not be read; Final remains unaffected.')
    }
    void fetch('/keeper-animation-workbench/catalog.json', { cache: 'no-store' })
      .then((response) => {
        if (!response.ok) throw new Error(`Catalogue returned ${response.status}`)
        return response.json() as Promise<WorkbenchCatalogue>
      })
      .then((next) => {
        setCatalogue(next)
        setDrafts(reconcileDraftLibrary(next.lanes.draft, savedDrafts, new Set(next.assets.map((asset) => asset.id))))
        setStorageReady(true)
      })
      .catch((error: Error) => setLoadError(error.message))
  }, [])

  useEffect(() => {
    if (storageReady) localStorage.setItem(STORAGE_KEY, JSON.stringify({ version: 1, drafts }))
  }, [drafts, storageReady])

  const finalItems = catalogue?.lanes.final ?? []
  const items = lane === 'final' ? finalItems : drafts
  const visibleItems = items.filter((item) => `${item.title} ${item.name} ${item.tags.join(' ')}`.toLowerCase().includes(filter.toLowerCase()))
  useEffect(() => {
    if (!items.some((item) => item.id === selectedId)) setSelectedId(items[0]?.id ?? '')
  }, [items, selectedId])
  const selected = items.find((item) => item.id === selectedId) ?? items[0]
  useEffect(() => {
    if (!selected) return
    setSelectedFrameId(selected.timeline[0]?.id ?? '')
    setLoopStart(selected.timeline[0]?.id ?? '')
    setLoopEnd(selected.timeline.at(-1)?.id ?? '')
    setPreviewLoop(selected.overallLoop)
  }, [selected?.id])

  const assets = useMemo(() => new Map((catalogue?.assets ?? []).map((asset) => [asset.id, asset])), [catalogue])
  const asset = selected ? assets.get(selected.assetId) : undefined
  const animationSequence = useMemo(() => selected && asset ? itemPlayback(selected, asset) : [], [selected, asset])
  const routeSequence = useMemo(() => selected ? transitionPlayback(selected, assets) : [], [selected, assets])
  const routeWarnings = useMemo(() => selected ? transitionWarnings(selected, assets) : [], [selected, assets])
  const conflicts = useMemo(() => selected ? loopConflicts(selected.timeline, selected.sectionLoops) : [], [selected])
  const loopRanges = useMemo(() => selected ? resolvedLoops(selected.timeline, selected.sectionLoops) : [], [selected])

  const updateDraft = (change: (item: WorkbenchItem) => WorkbenchItem) => {
    if (!selected || selected.lane !== 'draft') return
    setDrafts((current) => current.map((item) => item.id === selected.id ? { ...change(item), updatedAt: new Date().toISOString() } : item))
  }
  const createDraft = () => {
    if (!selected || selected.lane !== 'final') return
    const id = uid(`${selected.name}-draft`)
    const draft = copyToDraft(selected, id, new Date().toISOString())
    setDrafts((current) => [...current, draft])
    setLane('draft')
    setSelectedId(id)
    setMessage(`Copied “${selected.title}” to Draft. Final remains unchanged.`)
  }
  const addLoop = () => {
    if (!selected || selected.lane !== 'draft' || !loopStart || !loopEnd) return
    const loop: SectionLoop = { id: uid('section-loop'), startId: loopStart, endId: loopEnd, repeats: Math.max(2, Math.min(12, loopRepeats)) }
    updateDraft((item) => ({ ...item, sectionLoops: [...item.sectionLoops, loop] }))
  }
  const importDrafts = async (file: File) => {
    try {
      const parsed = JSON.parse(await file.text()) as { drafts?: WorkbenchItem[] }
      if (!Array.isArray(parsed.drafts)) throw new Error('No Draft library was found.')
      const imported = parsed.drafts.filter((item) => item.lane === 'draft' && assets.has(item.assetId))
      setDrafts(imported)
      setLane('draft')
      setSelectedId(imported[0]?.id ?? '')
      setMessage(`Imported ${imported.length} Draft animation${imported.length === 1 ? '' : 's'}.`)
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Draft import failed.')
    }
  }

  if (loadError) return <main className={styles.workbench}><div className={styles.loading}><h1>Keeper Animation Workbench</h1><p>Could not load the catalogue: {loadError}</p></div></main>
  if (!catalogue) return <main className={styles.workbench}><div className={styles.loading}><h1>Keeper Animation Workbench</h1><p>Loading Draft and Final…</p></div></main>

  return (
    <main className={styles.workbench}>
      <header className={styles.header}>
        <div>
          <p className={styles.eyebrow}>Separate review surface · production unchanged</p>
          <h1>Keeper Animation Workbench</h1>
          <p><strong>Final is empty.</strong> Prime Master V1 is awaiting approval before any animation is redrafted. Earlier V1/V2 routes remain provenance only.</p>
          <p><a href="/keeper-review/keeper-prime-master-v1/">Review the Prime Keeper master proposal →</a></p>
        </div>
        <nav><a href="/">Game</a><a href="/studio">Recipe Studio</a></nav>
      </header>
      <section className={styles.toolbar}>
        <div className={styles.laneTabs} role="tablist" aria-label="Animation library">
          <button type="button" role="tab" aria-selected={lane === 'final'} className={lane === 'final' ? styles.activeTab : ''} onClick={() => setLane('final')}>Final <span>{finalItems.length}</span></button>
          <button type="button" role="tab" aria-selected={lane === 'draft'} className={lane === 'draft' ? styles.activeTab : ''} onClick={() => setLane('draft')}>Draft <span>{drafts.length}</span></button>
        </div>
        <input type="search" value={filter} onChange={(event) => setFilter(event.target.value)} placeholder="Filter animations" aria-label="Filter animations" />
        <button type="button" onClick={() => downloadJson('keeper-animation-drafts.json', { version: 1, exportedAt: new Date().toISOString(), drafts })}>Export Draft JSON</button>
        <button type="button" onClick={() => importRef.current?.click()}>Import Draft JSON</button>
        <input ref={importRef} className={styles.hiddenInput} type="file" accept="application/json" onChange={(event) => { const file = event.target.files?.[0]; if (file) void importDrafts(file); event.target.value = '' }} />
      </section>
      {message && <button type="button" className={styles.message} onClick={() => setMessage('')}>{message}</button>}
      <div className={styles.layout}>
        <aside className={styles.library}>
          <div className={styles.libraryIntro}>
            <h2>{lane === 'final' ? 'Approved animations' : 'Working copies'}</h2>
            <p>{lane === 'final' ? 'No animation is currently Final.' : 'No active route remains: animation redrafting starts after Prime Master V1 approval.'}</p>
          </div>
          <ul>
            {visibleItems.map((item) => <li key={item.id}><button type="button" className={item.id === selected?.id ? styles.selectedItem : ''} onClick={() => setSelectedId(item.id)}><strong>{item.title}</strong><span>{item.name}</span><small>Complete transition route</small></button></li>)}
          </ul>
          {!visibleItems.length && <p className={styles.empty}>{lane === 'draft' ? 'No active Draft animations. Prime Master V1 is awaiting approval.' : 'No animations are currently Final.'}</p>}
        </aside>

        <div className={styles.content}>
          {!selected || !asset ? <section className={styles.emptyStage}><h2>Animation library reset</h2><p>Approve the smooth Prime Master V1 foundation before the first transition is redrafted.</p><p><a href="/keeper-review/keeper-prime-master-v1/">Open Prime Master V1 review</a></p></section> : <>
            <section className={styles.itemHeader}>
              <div>
                <div className={styles.badges}><span className={selected.lane === 'final' ? styles.finalBadge : styles.draftBadge}>{selected.lane}</span><span>{asset.frames} source frames</span><span>{asset.fps} fps</span><span>{asset.outfit ?? 'standard'}</span></div>
                {selected.lane === 'draft' ? <input className={styles.titleInput} value={selected.title} onChange={(event) => updateDraft((item) => ({ ...item, title: event.target.value }))} aria-label="Draft title" /> : <h2>{selected.title}</h2>}
                <p>{selected.description}</p>
              </div>
              <div className={styles.itemActions}>
                {selected.lane === 'final' ? <button type="button" className={styles.primaryButton} onClick={createDraft}>Copy to Draft</button> : <button type="button" className={styles.dangerButton} onClick={() => { if (confirm(`Delete Draft “${selected.title}”? Final and source art remain unchanged.`)) { setDrafts((current) => current.filter((item) => item.id !== selected.id)); setMessage('Draft removed. Final and source art were not changed.') } }}>Remove Draft</button>}
              </div>
            </section>

            {selected.approval && <blockquote className={styles.approval}>“{selected.approval.wording}” <footer>— {selected.approval.approvedBy}, {selected.approval.approvedOn}. Final-library approval only; runtime promotion remains separate.</footer></blockquote>}

            <div className={styles.previewGrid}>
              <Preview title="Animation preview" sequence={animationSequence} assets={assets} loop={previewLoop} onLoopChange={(next) => { setPreviewLoop(next); if (selected.lane === 'draft') updateDraft((item) => ({ ...item, overallLoop: next })) }} />
              <Preview title="Transition preview" sequence={routeSequence} assets={assets} loop={routeLoop} onLoopChange={setRouteLoop} empty="No complete transition route has been defined." />
            </div>

            <section className={styles.routePanel}>
              <div className={styles.sectionHeading}><div><h2>Transition route</h2><p>{selected.transitionReason}</p></div><span className={styles.required}>Required for every action</span></div>
              <ol className={styles.route}>{selected.transitionRoute.map((segment) => <li key={segment.id}><strong>{segment.label}</strong><span>{assets.get(segment.assetId)?.name ?? 'missing asset'}</span>{segment.entryOcclusion && <small>begins hidden behind {segment.entryOcclusion === 'door-left' ? 'left' : 'right'} door</small>}{segment.distanceMode === 'runtime-placement' && <small>cycles set by game placement</small>}{segment.repeats > 1 && <small>× {segment.repeats}</small>}{segment.mirror && <small>mirrored</small>}</li>)}</ol>
              {routeWarnings.length ? <ul className={styles.warnings}>{routeWarnings.map((warning) => <li key={warning}>{warning}</li>)}</ul> : <p className={styles.pass}>Pose and costume metadata agree at every route join.</p>}
            </section>

            <section className={styles.timelinePanel}>
              <div className={styles.sectionHeading}><div><h2>Frame timeline</h2><p>{selected.lane === 'final' ? 'Final uses the same timeline architecture but remains locked.' : `${selected.timeline.length} timeline steps expand to ${expandTimeline(selected.timeline, selected.sectionLoops).length} played frames.`}</p></div></div>
              <div className={styles.timeline}>
                {selected.timeline.map((entry, index) => {
                  const inLoop = loopRanges.some((range) => index >= range.start && index <= range.end)
                  return <button type="button" key={entry.id} className={`${styles.frameCard} ${entry.id === selectedFrameId ? styles.selectedFrame : ''} ${inLoop ? styles.loopFrame : ''}`} onClick={() => setSelectedFrameId(entry.id)}><SpriteFrame asset={asset} frame={entry.frame} compact /><strong>Step {index + 1}</strong><span>source F{entry.frame + 1}</span></button>
                })}
              </div>
              {selected.lane === 'draft' && <div className={styles.editor}>
                <div className={styles.frameTools}>
                  <button type="button" disabled={!selectedFrameId} onClick={() => { const id = uid('frame'); updateDraft((item) => copyTimelineEntry(item, selectedFrameId, id)); setSelectedFrameId(id) }}>Copy frame</button>
                  <button type="button" disabled={!selectedFrameId || selected.timeline.length <= 1} onClick={() => { const index = selected.timeline.findIndex((entry) => entry.id === selectedFrameId); const fallback = selected.timeline[Math.max(0, index - 1)]?.id ?? ''; updateDraft((item) => removeTimelineEntry(item, selectedFrameId)); setSelectedFrameId(fallback) }}>Remove frame</button>
                  <button type="button" disabled={selected.timeline[0]?.id === selectedFrameId} onClick={() => updateDraft((item) => moveTimelineEntry(item, selectedFrameId, -1))}>Move left</button>
                  <button type="button" disabled={selected.timeline.at(-1)?.id === selectedFrameId} onClick={() => updateDraft((item) => moveTimelineEntry(item, selectedFrameId, 1))}>Move right</button>
                </div>
                <div className={styles.loopBuilder}>
                  <label>Loop from<select value={loopStart} onChange={(event) => setLoopStart(event.target.value)}>{selected.timeline.map((entry, index) => <option key={entry.id} value={entry.id}>Step {index + 1} · F{entry.frame + 1}</option>)}</select></label>
                  <label>to<select value={loopEnd} onChange={(event) => setLoopEnd(event.target.value)}>{selected.timeline.map((entry, index) => <option key={entry.id} value={entry.id}>Step {index + 1} · F{entry.frame + 1}</option>)}</select></label>
                  <label>Total passes<input type="number" min={2} max={12} value={loopRepeats} onChange={(event) => setLoopRepeats(Number(event.target.value))} /></label>
                  <button type="button" onClick={addLoop}>Repeat section</button>
                </div>
                {!!selected.sectionLoops.length && <ul className={styles.loopList}>{selected.sectionLoops.map((loop) => {
                  const range = resolvedLoops(selected.timeline, [loop])[0]
                  return <li key={loop.id}><span>Steps {range ? range.start + 1 : '?'}–{range ? range.end + 1 : '?'} play {loop.repeats} times</span><button type="button" onClick={() => updateDraft((item) => ({ ...item, sectionLoops: item.sectionLoops.filter((candidate) => candidate.id !== loop.id) }))}>Remove loop</button></li>
                })}</ul>}
                {!!conflicts.length && <p className={styles.error}>Overlapping section loops are disabled until one is removed or its endpoints are reordered.</p>}
              </div>}
            </section>

            <section className={styles.provenance}>
              <h2>Source contract</h2>
              <dl><div><dt>Asset</dt><dd>{asset.name}</dd></div><div><dt>SHA-256</dt><dd>{asset.sha256}</dd></div><div><dt>Endpoint</dt><dd>{asset.startPose ?? '—'} → {asset.endPose ?? '—'}</dd></div><div><dt>Rule</dt><dd>{selected.lane === 'final' ? 'Final bytes are immutable.' : 'Versioned Draft PNG bytes remain unchanged; timeline edits reference source frames only.'}</dd></div></dl>
            </section>
          </>}
        </div>
      </div>
    </main>
  )
}
