'use client'

import { useEffect, useMemo, useRef, useState } from 'react'
import styles from './primeKeeperDraftReview.module.css'

type Frame = { id: string; label: string; phase?: string; src: string; sha256: string; durationMs: number; redraftSlot: string; amendmentComparison?: { label: string; src: string; sha256: string } }
type Sequence = { id: string; title: string; status: string; fps: number; startPose: string; endPose: string; source: { path: string; sha256: string }; draftStrip: { path: string; sha256: string }; frames: Frame[] }
type Batch = {
  version: number
  generatedOn: string
  status: string
  note: string
  dimensions: { logicalCell: number[]; authoringCell: number[]; scale: number; anchor: number[]; capTop: number; floorOpaqueY: number }
  colourLock: Record<string, number[]>
  canonicalAuthorities: Record<string, { path: string; sha256: string }>
  reviewAuthorities?: Record<string, { src: string; sha256: string; status: string }>
  quarantinedSources: Array<{ id: string; title: string; path: string; sha256: string; reason: string }>
  sequences: Sequence[]
}
type Command = { type: 'play' | 'pause' | 'previous' | 'next' | 'stop'; nonce: number }
type SandboxEntry = { key: string; sequenceId: string; reverse: boolean }

const AUTHORITY_SPRITES: Record<string, string> = {
  front: '/sprites/keeper_prime_neutral_standing-front.png',
  back: '/sprites/keeper_prime_neutral_standing-back.png',
  sideRight: '/sprites/keeper_prime_neutral_standing-side-right.png',
}
const NOTES_KEY = 'keeper-prime-draft-redraft-notes:v1'
const SANDBOX_KEY = 'keeper-prime-draft-sandbox:v1'

function preload(src: string) {
  return new Promise<void>((resolve, reject) => {
    const image = new Image()
    image.onload = () => image.decode?.().then(() => resolve()).catch(() => resolve()) ?? resolve()
    image.onerror = () => reject(new Error(src))
    image.src = src
  })
}

function Transport({ index, length, playing, ready, onCommand, onSeek }: { index: number; length: number; playing: boolean; ready: boolean; onCommand: (type: Command['type']) => void; onSeek: (index: number) => void }) {
  return <div className={styles.transport}>
    <button disabled={!ready || playing} onClick={() => onCommand('play')}>▶ Play</button>
    <button disabled={!ready || !playing} onClick={() => onCommand('pause')}>Ⅱ Pause</button>
    <button disabled={!ready} onClick={() => onCommand('previous')}>← Frame</button>
    <button disabled={!ready} onClick={() => onCommand('next')}>Frame →</button>
    <button disabled={!ready} onClick={() => onCommand('stop')}>■ Stop</button>
    <output>{index + 1} / {length}</output>
    <input aria-label="Animation frame" type="range" min={0} max={Math.max(0, length - 1)} value={index} disabled={!ready} onChange={(event) => onSeek(Number(event.target.value))} />
  </div>
}

function Player({ frames, ready, command, onFrame, large = false }: { frames: Frame[]; ready: boolean; command: Command; onFrame?: (frame: Frame) => void; large?: boolean }) {
  const [index, setIndex] = useState(0)
  const [playing, setPlaying] = useState(false)
  const seen = useRef(-1)
  useEffect(() => { setIndex(0); setPlaying(false) }, [frames])
  useEffect(() => {
    if (seen.current === command.nonce) return
    seen.current = command.nonce
    if (command.type === 'play') setPlaying(true)
    if (command.type === 'pause') setPlaying(false)
    if (command.type === 'stop') { setPlaying(false); setIndex(0) }
    if (command.type === 'previous') { setPlaying(false); setIndex((value) => Math.max(0, value - 1)) }
    if (command.type === 'next') { setPlaying(false); setIndex((value) => Math.min(frames.length - 1, value + 1)) }
  }, [command, frames.length])
  useEffect(() => {
    if (!playing || !ready || !frames.length) return
    const timer = window.setTimeout(() => setIndex((value) => value >= frames.length - 1 ? 0 : value + 1), frames[index]?.durationMs ?? 125)
    return () => window.clearTimeout(timer)
  }, [frames, index, playing, ready])
  const frame = frames[index]
  useEffect(() => { if (frame) onFrame?.(frame) }, [frame, onFrame])
  const apply = (type: Command['type']) => {
    if (type === 'play') setPlaying(true)
    if (type === 'pause') setPlaying(false)
    if (type === 'stop') { setPlaying(false); setIndex(0) }
    if (type === 'previous') { setPlaying(false); setIndex((value) => Math.max(0, value - 1)) }
    if (type === 'next') { setPlaying(false); setIndex((value) => Math.min(frames.length - 1, value + 1)) }
  }
  const seek = (value: number) => { setPlaying(false); setIndex(value) }
  return <>
    <div className={`${styles.stage} ${large ? styles.stageLarge : ''}`}>{frame && <img src={frame.src} alt={`${frame.id}: ${frame.label}`} />}{!ready && <span>Decoding every frame…</span>}</div>
    <div className={styles.frameLabel}><strong>{frame?.label}</strong><code>{frame?.redraftSlot}</code></div>
    <Transport index={index} length={frames.length} playing={playing} ready={ready} onCommand={apply} onSeek={seek} />
    <div className={styles.frameRail}>{frames.map((item, frameIndex) => <button className={frameIndex === index ? styles.selectedFrame : ''} key={item.id} onClick={() => seek(frameIndex)}><img src={item.src} alt="" /><span>{frameIndex + 1}</span></button>)}</div>
  </>
}

export default function PrimeKeeperDraftReview({ batch, manualAlignmentHref }: { batch: Batch; manualAlignmentHref?: string }) {
  const [ready, setReady] = useState(false)
  const [loadError, setLoadError] = useState('')
  const [command, setCommand] = useState<Command>({ type: 'pause', nonce: 0 })
  const [sandbox, setSandbox] = useState<SandboxEntry[]>([])
  const [notes, setNotes] = useState<Record<string, string>>({})
  const [activeFrame, setActiveFrame] = useState<Frame | null>(batch.sequences[0]?.frames[0] ?? null)
  const sequenceMap = useMemo(() => new Map(batch.sequences.map((sequence) => [sequence.id, sequence])), [batch.sequences])
  const authoritySprites = useMemo(() => Object.fromEntries(Object.keys(batch.canonicalAuthorities).map((name) => [name, batch.reviewAuthorities?.[name]?.src ?? AUTHORITY_SPRITES[name]])), [batch.canonicalAuthorities, batch.reviewAuthorities])
  const sources = useMemo(() => [...new Set([...Object.values(authoritySprites), ...batch.sequences.flatMap((sequence) => sequence.frames.flatMap((frame) => [frame.src, frame.amendmentComparison?.src].filter((src): src is string => Boolean(src))))])], [authoritySprites, batch.sequences])

  useEffect(() => {
    let cancelled = false
    let cursor = 0
    const worker = async () => {
      while (cursor < sources.length) {
        const src = sources[cursor]
        cursor += 1
        try {
          await preload(src)
        } catch {
          await new Promise((resolve) => window.setTimeout(resolve, 150))
          await preload(src)
        }
      }
    }
    Promise.all(Array.from({ length: Math.min(6, sources.length) }, worker))
      .then(() => { if (!cancelled) setReady(true) })
      .catch((error: Error) => { if (!cancelled) setLoadError(error.message) })
    return () => { cancelled = true }
  }, [sources])
  useEffect(() => {
    try {
      setNotes(JSON.parse(localStorage.getItem(NOTES_KEY) ?? '{}'))
      const stored = JSON.parse(localStorage.getItem(SANDBOX_KEY) ?? '[]') as SandboxEntry[]
      setSandbox(stored.filter((entry) => sequenceMap.has(entry.sequenceId)))
    } catch { /* start clean */ }
  }, [sequenceMap])
  useEffect(() => { localStorage.setItem(NOTES_KEY, JSON.stringify(notes)) }, [notes])
  useEffect(() => { localStorage.setItem(SANDBOX_KEY, JSON.stringify(sandbox)) }, [sandbox])

  const sandboxFrames = useMemo(() => sandbox.flatMap((entry) => {
    const frames = sequenceMap.get(entry.sequenceId)?.frames ?? []
    return entry.reverse ? [...frames].reverse() : frames
  }), [sandbox, sequenceMap])
  const frameCount = batch.sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0)
  const approvedCompositionCount = batch.sequences.filter((sequence) => sequence.status === 'approved-components-choreography-review').length
  const broadcast = (type: Command['type']) => setCommand((current) => ({ type, nonce: current.nonce + 1 }))
  const addSequence = (sequence: Sequence) => setSandbox((items) => [...items, { key: `${sequence.id}-${Date.now()}`, sequenceId: sequence.id, reverse: false }])
  const move = (index: number, direction: -1 | 1) => setSandbox((items) => {
    const target = index + direction
    if (target < 0 || target >= items.length) return items
    const next = [...items]; [next[index], next[target]] = [next[target], next[index]]; return next
  })

  return <main className={styles.page}>
    <header className={styles.hero}>
      <nav><a href="/prime-keeper-animations">Approved library</a><span>/</span><strong>{batch.version < 2 ? 'Morning draft batch V1' : `Expanded review batch V${batch.version}`}</strong>{batch.version < 2 && <><span>/</span><a href="/prime-keeper-animation-drafts-v2">Open expanded V2 →</a></>}{manualAlignmentHref && <><span>/</span><a href={manualAlignmentHref}>Manual rear-task alignment →</a></>}</nav>
      <p className={styles.eyebrow}>Versioned · reversible · frame-addressable</p>
      <h1>Prime Keeper<br />next motions.</h1>
      <p className={styles.lede}>{batch.version < 2 ? 'P0 circulation plus the first food, hygiene and reaction motions, held outside the production bank until you approve or request individual frame changes.' : batch.version >= 9 ? manualAlignmentHref ? 'V9 is rejected and retained as reversible evidence. Exact-source inspection now identifies the moving upper seam of the ribbed jumper band as the faulty join, not the lower seam. Use Manual rear-task alignment to remove that upper seam while retaining the approved complete band, lower seam, trousers and boots.' : 'Feedback-corrected circulation and daily-life drafts. V9 replaces only rear-task frames 11–31: the exact V8 side alignment is retained, but the fixed trouser waistband edge is hidden behind the moving jumper hem so only one bottom seam is visible; nothing here is promoted until accepted.' : batch.version >= 8 ? 'Feedback-corrected circulation and daily-life drafts. V8 replaces only rear-task frames 11–31: the complete moving torso and its one natural hem are retained, then approved rear-authority legs begin where both side outlines meet exactly; nothing here is promoted until accepted.' : batch.version >= 7 ? 'Feedback-corrected circulation and daily-life drafts. V7 preserves every accepted earlier change and replaces only rear-task frames 11–31: the upper action is retained while the corrected rear Prime authority supplies one lower-jumper hem, trousers and boots; nothing here is promoted until accepted.' : batch.version >= 6 ? 'Feedback-corrected circulation and daily-life drafts. V6 preserves every accepted earlier change and tapers the generated rear-task lower jumper onto authority trousers; it remains rejected review evidence.' : batch.version >= 5 ? 'Feedback-corrected circulation and daily-life drafts. V5 preserves every accepted earlier change and rebuilds rear-task frames 11–31 with the complete moving jumper hem over clean authority trousers; nothing here is promoted until accepted.' : batch.version >= 4 ? 'Feedback-corrected circulation and daily-life drafts. V4 preserves every accepted V3 change and rebuilds rear-task frames 11–31 with one continuous authority-locked jumper hem; nothing here is promoted until accepted.' : batch.version >= 3 ? 'Feedback-corrected circulation and daily-life drafts. Passive front/back colour, lift timing, route naming and the rear-work waist seam are revised in reversible V3 copies; nothing here is promoted until accepted.' : 'P0 circulation and daily-life drafts, plus exact approved-component choreography for seating, diary and rear tasks. Candidate sequences remain outside the production bank until their complete motion is accepted.'}</p>
    </header>

    <section className={styles.readiness}><strong>{loadError ? 'Playback locked' : ready ? `All ${sources.length} images decoded` : `Preparing ${sources.length} images…`}</strong><span>{loadError || 'No player starts until every frame is available.'}</span></section>

    <section className={styles.contract}>
      <div><span>01</span><h2>Prime identity gate</h2></div>
      <p><strong>32×40 logical pixels · 256×320 authoring · 8 px/lp · anchor 128,320.</strong> Cap top y18; opaque floor y316. Jumper, cream band, trousers and boots are colour-locked to the measured Prime palette below.</p>
      <div className={styles.authorities}>{Object.entries(batch.canonicalAuthorities).map(([name, authority]) => { const review = batch.reviewAuthorities?.[name]; return <article key={name}><div className={styles.authorityStage}><img src={authoritySprites[name]} alt={`${review ? `V${batch.version} review` : 'Canonical'} ${name} Prime Keeper`} /></div><strong>{name.replace(/([A-Z])/g, ' $1')}</strong><code>{(review?.sha256 ?? authority.sha256).slice(0, 16)}…</code></article> })}</div>
      <dl className={styles.palette}>{Object.entries(batch.colourLock).map(([name, rgb]) => <div key={name}><i style={{ background: `rgb(${rgb.join(',')})` }} /><dt>{name}</dt><dd>{rgb.join(', ')}</dd></div>)}</dl>
      <p className={styles.boundary}><strong>Review boundary:</strong> this page contains {frameCount} frame occurrences. {approvedCompositionCount ? `${approvedCompositionCount} sequences reuse byte-exact approved component art; their order, holds and joins are still presented for choreography review. ` : ''}Generated action drafts and the isolated broom candidate remain unapproved. Canonical Prime art and approved sources are unchanged; V{batch.version} corrections are separate review copies. Every occurrence has a stable feedback slot.</p>
      <div className={styles.quarantine}><strong>{batch.quarantinedSources.length} generated sources withheld by the isolation gate</strong><ul>{batch.quarantinedSources.map((item) => <li key={item.id}><span>{item.title}</span> — {item.reason}</li>)}</ul></div>
    </section>

    <section className={styles.review}>
      <div className={styles.sectionTitle}><div><span>02</span><h2>Animation review</h2></div><div className={styles.global}><button disabled={!ready} onClick={() => broadcast('play')}>▶ All</button><button disabled={!ready} onClick={() => broadcast('pause')}>Ⅱ All</button><button disabled={!ready} onClick={() => broadcast('previous')}>← Frame</button><button disabled={!ready} onClick={() => broadcast('next')}>Frame →</button><button disabled={!ready} onClick={() => broadcast('stop')}>■ Stop</button></div></div>
      <div className={styles.sequenceGrid}>{batch.sequences.map((sequence) => <article className={styles.sequence} key={sequence.id}>
        <header><div><span>{sequence.status === 'approved-components-choreography-review' ? 'Approved art · choreography review' : sequence.id.includes('sweep') ? 'Isolated action candidate' : 'Review draft'}</span><h3>{sequence.title}</h3><p>{sequence.startPose} → {sequence.endPose} · {sequence.frames.length} frames at {sequence.fps} fps</p></div><button onClick={() => addSequence(sequence)}>＋ Sandbox</button></header>
        <Player frames={sequence.frames} ready={ready} command={command} onFrame={setActiveFrame} />
        <details><summary>Source and draft hashes</summary><dl><div><dt>Source authority</dt><dd><code>{sequence.source.sha256}</code></dd></div><div><dt>Versioned strip</dt><dd><code>{sequence.draftStrip.sha256}</code></dd></div></dl></details>
      </article>)}</div>
    </section>

    <section className={styles.redraft}>
      <div><span>03</span><h2>Frame-specific redraft notes</h2></div>
      <p>Select any frame above. Notes stay in this browser and are keyed to that exact frame slot.</p>
      {activeFrame?.amendmentComparison && <div className={styles.comparison}><article><span>{activeFrame.amendmentComparison.label}</span><div><img src={activeFrame.amendmentComparison.src} alt={`${activeFrame.label} rejected predecessor comparison`} /></div><code>{activeFrame.amendmentComparison.sha256.slice(0, 16)}…</code></article><article><span>V{batch.version} corrected draft</span><div><img src={activeFrame.src} alt={`${activeFrame.label} V${batch.version} draft`} /></div><code>{activeFrame.sha256.slice(0, 16)}…</code></article></div>}
      {activeFrame && <div className={styles.noteBox}><div><strong>{activeFrame.label}</strong><code>{activeFrame.redraftSlot}</code><small>SHA-256 {activeFrame.sha256}</small></div><textarea aria-label="Redraft note" placeholder="What should change in this frame only?" value={notes[activeFrame.redraftSlot] ?? ''} onChange={(event) => setNotes((current) => ({ ...current, [activeFrame.redraftSlot]: event.target.value }))} /><button onClick={() => navigator.clipboard.writeText(`${activeFrame.redraftSlot}: ${notes[activeFrame.redraftSlot] ?? ''}`)}>Copy note</button></div>}
    </section>

    <section className={styles.sandbox}>
      <div className={styles.sectionTitle}><div><span>04</span><h2>Draft sequence sandbox</h2></div><p>Combine, reverse and inspect without altering any source frame.</p></div>
      <div className={styles.sandboxGrid}><article className={styles.sandboxPlayer}>{sandboxFrames.length ? <Player frames={sandboxFrames} ready={ready} command={command} large /> : <div className={styles.empty}><strong>No draft sequence yet.</strong><p>Use “＋ Sandbox” on any animation.</p></div>}</article><article className={styles.builder}><header><strong>Sequence order</strong><button onClick={() => setSandbox([])}>Clear</button></header>{sandbox.map((entry, index) => { const sequence = sequenceMap.get(entry.sequenceId); return <div className={styles.builderRow} key={entry.key}><span>{index + 1}</span><strong>{sequence?.title}</strong><label><input type="checkbox" checked={entry.reverse} onChange={(event) => setSandbox((items) => items.map((item) => item.key === entry.key ? { ...item, reverse: event.target.checked } : item))} /> reverse</label><button disabled={index === 0} onClick={() => move(index, -1)}>↑</button><button disabled={index === sandbox.length - 1} onClick={() => move(index, 1)}>↓</button><button onClick={() => setSandbox((items) => items.filter((item) => item.key !== entry.key))}>×</button></div>})}</article></div>
    </section>
  </main>
}
