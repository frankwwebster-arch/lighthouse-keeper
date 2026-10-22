'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import styles from './primeKeeperAnimations.module.css'
import type { AnimationCatalogue, AnimationClip, AnimationFrame, AnimationGapInventory, PlayerCommand } from './types'

const SANDBOX_KEY = 'prime-keeper-animation-sandbox:v1'

type SandboxEntry = { key: string; clipId: string; reverse: boolean; repeats: number }

function preloadImage(src: string) {
  return new Promise<void>((resolve, reject) => {
    const image = new Image()
    image.onload = () => {
      const decoded = image.decode?.()
      if (decoded) decoded.then(() => resolve()).catch(() => resolve())
      else resolve()
    }
    image.onerror = () => reject(new Error(src))
    image.src = src
  })
}

function Transport({ index, length, playing, ready, onPlay, onPause, onPrevious, onNext, onRestart, onSeek, compact = false }: {
  index: number
  length: number
  playing: boolean
  ready: boolean
  onPlay: () => void
  onPause: () => void
  onPrevious: () => void
  onNext: () => void
  onRestart: () => void
  onSeek: (index: number) => void
  compact?: boolean
}) {
  return <div className={compact ? styles.transportCompact : styles.transport}>
    <div className={styles.transportButtons}>
      <button type="button" disabled={!ready || !length || playing} onClick={onPlay} aria-label="Play">▶ <span>Play</span></button>
      <button type="button" disabled={!ready || !length || !playing} onClick={onPause} aria-label="Pause">Ⅱ <span>Pause</span></button>
      <button type="button" disabled={!ready || !length} onClick={onPrevious} aria-label="Previous frame">← <span>Frame</span></button>
      <button type="button" disabled={!ready || !length} onClick={onNext} aria-label="Next frame"><span>Frame</span> →</button>
      <button type="button" disabled={!ready || !length} onClick={onRestart} aria-label="Stop and return to first frame">■ <span>Stop</span></button>
      <output>{length ? `${index + 1} / ${length}` : '0 / 0'}</output>
    </div>
    <input type="range" min={0} max={Math.max(0, length - 1)} value={Math.min(index, Math.max(0, length - 1))} disabled={!ready || !length} onChange={(event) => onSeek(Number(event.target.value))} aria-label="Animation frame" />
  </div>
}

function Player({ frames, loop, ready, command, title, large = false }: {
  frames: AnimationFrame[]
  loop: boolean
  ready: boolean
  command?: PlayerCommand
  title: string
  large?: boolean
}) {
  const [index, setIndex] = useState(0)
  const [playing, setPlaying] = useState(false)
  const commandNonce = useRef(-1)

  useEffect(() => {
    setIndex(0)
    setPlaying(false)
  }, [frames])

  useEffect(() => {
    if (!command || command.nonce === commandNonce.current) return
    commandNonce.current = command.nonce
    if (command.type === 'play') setPlaying(true)
    if (command.type === 'pause') setPlaying(false)
    if (command.type === 'restart') { setPlaying(false); setIndex(0) }
    if (command.type === 'previous') { setPlaying(false); setIndex((value) => Math.max(0, value - 1)) }
    if (command.type === 'next') { setPlaying(false); setIndex((value) => Math.min(frames.length - 1, value + 1)) }
  }, [command, frames.length])

  useEffect(() => {
    if (!ready) setPlaying(false)
  }, [ready])

  useEffect(() => {
    if (!playing || !frames.length) return
    const timer = window.setTimeout(() => {
      if (index < frames.length - 1) setIndex(index + 1)
      else if (loop) setIndex(0)
      else setPlaying(false)
    }, Math.max(30, frames[index]?.durationMs ?? 100))
    return () => window.clearTimeout(timer)
  }, [frames, index, loop, playing])

  const frame = frames[Math.min(index, Math.max(0, frames.length - 1))]
  const seek = (value: number) => { setPlaying(false); setIndex(value) }
  return <>
    <div className={`${styles.stage} ${large ? styles.stageLarge : ''}`}>
      {frame ? <img src={frame.src} alt={`${title}, ${frame.label}`} className={frame.flipX ? styles.flipped : undefined} /> : <p>Add an approved animation below to begin.</p>}
      {!ready && <span className={styles.stageLock}>Preparing approved frames…</span>}
    </div>
    <div className={styles.frameReadout} title={frame?.phase}>{frame?.phase ? `${frame.phase} · ` : ''}{frame?.label ?? 'Empty sequence'}</div>
    <Transport index={index} length={frames.length} playing={playing} ready={ready} onPlay={() => setPlaying(true)} onPause={() => setPlaying(false)} onPrevious={() => seek(Math.max(0, index - 1))} onNext={() => seek(Math.min(frames.length - 1, index + 1))} onRestart={() => seek(0)} onSeek={seek} compact={!large} />
  </>
}

function RuntimePlayer({ clip, ready, command }: { clip: AnimationClip; ready: boolean; command: PlayerCommand }) {
  const runtimeFrames = useMemo(() => clip.runtimeAssets.flatMap((asset) => Array.from({ length: asset.frames }, (_, index) => ({
    asset,
    index,
    durationMs: asset.fps > 0 ? 1000 / asset.fps : 625,
  }))), [clip.runtimeAssets])
  const [index, setIndex] = useState(0)
  const [playing, setPlaying] = useState(false)
  const commandNonce = useRef(-1)

  useEffect(() => { setIndex(0); setPlaying(false) }, [clip.id])
  useEffect(() => {
    if (command.nonce === commandNonce.current) return
    commandNonce.current = command.nonce
    if (command.type === 'play') setPlaying(true)
    if (command.type === 'pause') setPlaying(false)
    if (command.type === 'restart') { setPlaying(false); setIndex(0) }
    if (command.type === 'previous') { setPlaying(false); setIndex((value) => Math.max(0, value - 1)) }
    if (command.type === 'next') { setPlaying(false); setIndex((value) => Math.min(runtimeFrames.length - 1, value + 1)) }
  }, [command, runtimeFrames.length])
  useEffect(() => {
    if (!ready) setPlaying(false)
  }, [ready])
  useEffect(() => {
    if (!playing || !runtimeFrames.length) return
    const timer = window.setTimeout(() => {
      if (index < runtimeFrames.length - 1) setIndex(index + 1)
      else if (clip.loop) setIndex(0)
      else setPlaying(false)
    }, runtimeFrames[index]?.durationMs ?? 100)
    return () => window.clearTimeout(timer)
  }, [clip.loop, index, playing, runtimeFrames])

  const frame = runtimeFrames[Math.min(index, Math.max(0, runtimeFrames.length - 1))]
  const seek = (value: number) => { setPlaying(false); setIndex(value) }
  return <>
    <div className={`${styles.stage} ${styles.runtimeStage}`}>
      {frame && <svg viewBox={`0 0 ${frame.asset.w} ${frame.asset.h}`} role="img" aria-label={`${frame.asset.name}, frame ${frame.index + 1}`}>
        <image href={frame.asset.src} width={frame.asset.w * frame.asset.frames} height={frame.asset.h} transform={`translate(${-frame.index * frame.asset.w} 0)`} />
      </svg>}
      {!ready && <span className={styles.stageLock}>Preparing runtime sheets…</span>}
    </div>
    <div className={styles.frameReadout}>{frame ? `${frame.asset.name} · frame ${frame.index + 1} / ${frame.asset.frames}` : 'No direct runtime extraction'}</div>
    <Transport index={index} length={runtimeFrames.length} playing={playing} ready={ready} onPlay={() => setPlaying(true)} onPause={() => setPlaying(false)} onPrevious={() => seek(Math.max(0, index - 1))} onNext={() => seek(Math.min(runtimeFrames.length - 1, index + 1))} onRestart={() => seek(0)} onSeek={seek} compact />
  </>
}

function ClipCard({ clip, ready, command, onAdd }: { clip: AnimationClip; ready: boolean; command: PlayerCommand; onAdd: (clip: AnimationClip) => void }) {
  return <article className={styles.clipCard}>
    <div className={styles.clipHeading}>
      <div><span className={styles.category}>{clip.category}</span><h3>{clip.title}</h3><p>{clip.version}</p></div>
      <span className={styles.approved}>{clip.runtimeSprites.length ? 'In runtime' : 'Approved'}</span>
    </div>
    <div className={clip.runtimeAssets.length ? styles.deliveryComparison : undefined}>
      <div className={styles.deliveryPane}><strong className={styles.deliveryLabel}>Approved source</strong><Player frames={clip.frames} loop={clip.loop} ready={ready} command={command} title={clip.title} /></div>
      {!!clip.runtimeAssets.length && <div className={styles.deliveryPane}><strong className={styles.deliveryLabel}>Installed runtime delivery</strong><RuntimePlayer clip={clip} ready={ready} command={command} /></div>}
    </div>
    <div className={styles.clipMeta}>
      <p>{clip.scope}</p>
      <p className={styles.runtimeState}>{clip.productionState}</p>
      <dl><div><dt>Frames</dt><dd>{clip.frames.length}</dd></div><div><dt>Pose route</dt><dd>{clip.startPose} → {clip.endPose}</dd></div><div><dt>Decision</dt><dd>{clip.approvedOn}</dd></div></dl>
    </div>
    <div className={styles.clipActions}>
      <button type="button" className={styles.addButton} onClick={() => onAdd(clip)}>＋ Add to sandbox</button>
      <a href={clip.reviewUrl}>Open original review ↗</a>
    </div>
  </article>
}

function makeEntry(clipId: string): SandboxEntry {
  return { key: `${clipId}-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`, clipId, reverse: false, repeats: 1 }
}

export default function PrimeKeeperAnimationLibrary({ catalogue, gaps }: { catalogue: AnimationCatalogue; gaps: AnimationGapInventory }) {
  const [loaded, setLoaded] = useState(0)
  const [loadError, setLoadError] = useState('')
  const [category, setCategory] = useState('All')
  const [search, setSearch] = useState('')
  const [command, setCommand] = useState<PlayerCommand>({ type: 'pause', nonce: 0 })
  const [sandbox, setSandbox] = useState<SandboxEntry[]>([])
  const [storageReady, setStorageReady] = useState(false)
  const sandboxRef = useRef<HTMLElement>(null)

  const allSources = useMemo(() => [...new Set(catalogue.clips.flatMap((clip) => [
    ...clip.frames.map((frame) => frame.src),
    ...clip.runtimeAssets.map((asset) => asset.src),
  ]))], [catalogue])
  const ready = loaded === allSources.length && !loadError
  const clipMap = useMemo(() => new Map(catalogue.clips.map((clip) => [clip.id, clip])), [catalogue])
  const categories = ['All', ...new Set(catalogue.clips.map((clip) => clip.category))]

  useEffect(() => {
    let cancelled = false
    let count = 0
    let cursor = 0
    const worker = async () => {
      while (cursor < allSources.length) {
        const src = allSources[cursor]
        cursor += 1
        await preloadImage(src)
        count += 1
        if (!cancelled) setLoaded(count)
      }
    }
    Promise.all(Array.from({ length: Math.min(8, allSources.length) }, worker)).catch((error: Error) => {
      if (!cancelled) setLoadError(`One approved frame could not be prepared: ${error.message}`)
    })
    return () => { cancelled = true }
  }, [allSources])

  useEffect(() => {
    try {
      const saved = localStorage.getItem(SANDBOX_KEY)
      if (saved) {
        const parsed = JSON.parse(saved) as SandboxEntry[]
        setSandbox(parsed.filter((entry) => clipMap.has(entry.clipId)))
      }
    } catch { /* keep a clean local sandbox */ }
    setStorageReady(true)
  }, [clipMap])

  useEffect(() => {
    if (storageReady) localStorage.setItem(SANDBOX_KEY, JSON.stringify(sandbox))
  }, [sandbox, storageReady])

  const visibleClips = catalogue.clips.filter((clip) => {
    const categoryMatch = category === 'All' || clip.category === category
    const text = `${clip.title} ${clip.version} ${clip.scope} ${clip.category}`.toLowerCase()
    return categoryMatch && text.includes(search.toLowerCase())
  })

  const sandboxFrames = useMemo(() => sandbox.flatMap((entry) => {
    const clip = clipMap.get(entry.clipId)
    if (!clip) return []
    const source = entry.reverse ? [...clip.frames].reverse() : clip.frames
    return Array.from({ length: entry.repeats }, () => source).flat()
  }), [clipMap, sandbox])

  const joinWarnings = sandbox.flatMap((entry, index) => {
    if (!index) return []
    const previous = clipMap.get(sandbox[index - 1].clipId)
    const current = clipMap.get(entry.clipId)
    if (!previous || !current) return []
    const previousEnd = sandbox[index - 1].reverse ? previous.startPose : previous.endPose
    const currentStart = entry.reverse ? current.endPose : current.startPose
    return previousEnd === currentStart ? [] : [`${previous.title} ends “${previousEnd}”; ${current.title} starts “${currentStart}”.`]
  })

  const addToSandbox = (clip: AnimationClip) => {
    setSandbox((items) => [...items, makeEntry(clip.id)])
    window.setTimeout(() => sandboxRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 0)
  }
  const updateEntry = (key: string, change: Partial<SandboxEntry>) => setSandbox((items) => items.map((entry) => entry.key === key ? { ...entry, ...change } : entry))
  const moveEntry = (index: number, direction: -1 | 1) => setSandbox((items) => {
    const target = index + direction
    if (target < 0 || target >= items.length) return items
    const next = [...items]
    ;[next[index], next[target]] = [next[target], next[index]]
    return next
  })
  const exportSandbox = () => {
    const payload = { schema: 'lighthouse-keeper/prime-animation-sandbox@1', createdAt: new Date().toISOString(), entries: sandbox.map((entry) => ({ ...entry, key: undefined, clip: clipMap.get(entry.clipId)?.version })) }
    const url = URL.createObjectURL(new Blob([`${JSON.stringify(payload, null, 2)}\n`], { type: 'application/json' }))
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = 'prime-keeper-animation-sandbox.json'
    anchor.click()
    URL.revokeObjectURL(url)
  }
  const broadcast = (type: PlayerCommand['type']) => setCommand((current) => ({ type, nonce: current.nonce + 1 }))

  return <main className={styles.page}>
    <header className={styles.hero}>
      <nav><a href="/">Lighthouse Keeper</a><span>/</span><strong>Prime animation library</strong><span>·</span><a href="/prime-keeper-animation-drafts-v3">Open corrected review V3 →</a></nav>
      <div className={styles.heroGrid}>
        <div><p className={styles.eyebrow}>Approved motion · one living index</p><h1>The Prime Keeper<br />in motion.</h1><p className={styles.lede}>Every playable animation with an explicit approval record or approved core-motion authority, gathered in one place. Inspect them together, one frame at a time, then assemble your own sequence below.</p></div>
        <div className={styles.statusCard}><span className={styles.beacon} /><strong>{catalogue.summary.approvedPlayableClips}</strong><p>approved playable clips</p><dl><div><dt>Unique source images</dt><dd>{catalogue.summary.uniqueFrameImages}</dd></div><div><dt>Installed source clips</dt><dd>{catalogue.summary.runtimePromotions}</dd></div><div><dt>Last reconciled</dt><dd>{catalogue.generatedOn}</dd></div></dl></div>
      </div>
    </header>

    <section className={styles.progressPanel} aria-live="polite">
      <div><strong>{loadError ? 'Playback preparation stopped' : ready ? 'All approved and runtime images ready' : `Preparing image ${loaded} of ${allSources.length}`}</strong><span>{loadError || (ready ? 'Every approved frame and runtime sheet is decoded; all controls are unlocked.' : 'Controls unlock together, so no animation begins with missing frames.')}</span></div>
      <div className={styles.progressTrack}><i style={{ width: `${allSources.length ? loaded / allSources.length * 100 : 0}%` }} /></div>
    </section>

    <section className={styles.snapshot}>
      <div><span>01</span><h2>What we have achieved</h2></div>
      <div className={styles.achievementGrid}>
        <article><strong>Movement foundation</strong><p>Walk, acceleration/deceleration and both principal turn arcs now join the approved standing poses.</p></article>
        <article><strong>Vertical circulation</strong><p>A fourteen-riser stair system and full ladder route now cover door-to-door movement, including hidden scale handoffs.</p></article>
        <article><strong>Four-way seating</strong><p>Side-right, side-left, front and back sit/stand actions are approved with exact standing and seated endpoints.</p></article>
        <article><strong>Contextual proof</strong><p>Darts and rear-work sequences prove approved motion can survive complete room routes and activity choreography.</p></article>
      </div>
      <p className={styles.boundary}><strong>What “in runtime” means:</strong> 27 reusable sprites from 13 approved source clips are installed. Idle, walk start/cycle/stop, stairs and generic rear work are active; approved turns now bridge rear work and seating, side-facing leisure uses sit/hold/stand, and the diary uses turn/sit/hold/stand/turn. Ladder, front/left seating and darts remain installed but await matching gameplay consumers. The held-implement POC remains excluded because its proxy body art is explicitly non-production.</p>
    </section>

    <section className={styles.gapsSection}>
      <div className={styles.sectionTitle}><div><span>02</span><h2>What animation is still required</h2></div><p>Gameplay coverage, ordered by value. “Wiring” means the approved art is already installed; “new art” means it is genuinely still missing.</p></div>
      <div className={styles.gapSummary}>
        <article><strong>{gaps.installedNow.runtimeSprites}</strong><span>runtime sprites installed</span></article>
        <article><strong>{gaps.installedNow.registeredFrames}</strong><span>registered runtime frames</span></article>
        <article><strong>{gaps.installedNow.installedAwaitingGameplayChoreography.length}</strong><span>installed families awaiting choreography</span></article>
      </div>
      <div className={styles.gapGrid}>{gaps.priorities.map((group) => <article key={`${group.priority}-${group.title}`}>
        <div className={styles.gapHeading}><span>{group.priority}</span><em>{group.kind.replaceAll('-', ' ')}</em></div>
        <h3>{group.title}</h3>
        <p>{group.why}</p>
        <ul>{group.required.map((item) => <li key={item}>{item}</li>)}</ul>
        {!!group.interactionIds.length && <small>{group.interactionIds.length} current game interaction{group.interactionIds.length === 1 ? '' : 's'}</small>}
      </article>)}</div>
    </section>

    <section className={styles.librarySection}>
      <div className={styles.sectionTitle}><div><span>03</span><h2>Approved animation library</h2></div><p>{visibleClips.length} of {catalogue.clips.length} clips shown</p></div>
      <div className={styles.libraryToolbar}>
        <div className={styles.globalTransport}><span>All players</span><button disabled={!ready} onClick={() => broadcast('play')}>▶ Play</button><button disabled={!ready} onClick={() => broadcast('pause')}>Ⅱ Pause</button><button disabled={!ready} onClick={() => broadcast('previous')}>← Frame</button><button disabled={!ready} onClick={() => broadcast('next')}>Frame →</button><button disabled={!ready} onClick={() => broadcast('restart')}>■ Stop</button></div>
        <input type="search" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Find an animation…" aria-label="Find an animation" />
      </div>
      <div className={styles.categoryTabs}>{categories.map((name) => <button type="button" key={name} className={category === name ? styles.activeCategory : ''} onClick={() => setCategory(name)}>{name}</button>)}</div>
      <div className={styles.clipGrid}>{visibleClips.map((clip) => <ClipCard key={clip.id} clip={clip} ready={ready} command={command} onAdd={addToSandbox} />)}</div>
    </section>

    <section className={styles.sandboxSection} ref={sandboxRef}>
      <div className={styles.sectionTitle}><div><span>04</span><h2>Sequence sandbox</h2></div><p>Combine approved clips without changing their source frames.</p></div>
      <div className={styles.sandboxGrid}>
        <div className={styles.sandboxPlayer}>
          <Player frames={sandboxFrames} loop={false} ready={ready} title="Sandbox sequence" large />
          {!!joinWarnings.length && <div className={styles.joinWarnings}><strong>{joinWarnings.length} pose join{joinWarnings.length === 1 ? '' : 's'} need a bridge</strong><ul>{joinWarnings.map((warning, index) => <li key={`${warning}-${index}`}>{warning}</li>)}</ul></div>}
          {!joinWarnings.length && sandbox.length > 1 && <p className={styles.joinPass}>All declared pose endpoints line up.</p>}
        </div>
        <div className={styles.sequenceBuilder}>
          <div className={styles.builderHeading}><div><h3>Your sequence</h3><p>{sandbox.length} clip{sandbox.length === 1 ? '' : 's'} · {sandboxFrames.length} frames</p></div><div><button disabled={!sandbox.length} onClick={exportSandbox}>Export JSON</button><button disabled={!sandbox.length} onClick={() => setSandbox([])}>Clear</button></div></div>
          {!sandbox.length && <div className={styles.emptySandbox}><strong>Build a moment.</strong><p>Add clips from the library, or start with a useful route.</p><button onClick={() => setSandbox(['walk-v7', 'stop-walk-stop-v2', 'turn-front-side-v1', 'sit-front-v4'].map(makeEntry))}>Load walk → turn → sit</button></div>}
          <ol className={styles.sequenceList}>{sandbox.map((entry, index) => {
            const clip = clipMap.get(entry.clipId)
            if (!clip) return null
            return <li key={entry.key}>
              <span className={styles.sequenceNumber}>{String(index + 1).padStart(2, '0')}</span>
              <div className={styles.sequenceName}><strong>{clip.title}</strong><span>{entry.reverse ? clip.endPose : clip.startPose} → {entry.reverse ? clip.startPose : clip.endPose}</span></div>
              <label>Direction<select value={entry.reverse ? 'reverse' : 'forward'} onChange={(event) => updateEntry(entry.key, { reverse: event.target.value === 'reverse' })}><option value="forward">Forward</option><option value="reverse">Reverse</option></select></label>
              <label>Repeats<input type="number" min={1} max={8} value={entry.repeats} onChange={(event) => updateEntry(entry.key, { repeats: Math.max(1, Math.min(8, Number(event.target.value))) })} /></label>
              <div className={styles.rowActions}><button disabled={index === 0} onClick={() => moveEntry(index, -1)} aria-label="Move earlier">↑</button><button disabled={index === sandbox.length - 1} onClick={() => moveEntry(index, 1)} aria-label="Move later">↓</button><button onClick={() => setSandbox((items) => items.filter((item) => item.key !== entry.key))} aria-label="Remove">×</button></div>
            </li>
          })}</ol>
        </div>
      </div>
    </section>

    <section className={styles.excluded}>
      <h2>Approved proof, deliberately outside the playable bank</h2>
      {catalogue.excludedProofs.map((proof) => <p key={proof.id}><strong>{proof.title}.</strong> {proof.reason} <a href={proof.reviewUrl}>Open proof ↗</a></p>)}
    </section>
  </main>
}
