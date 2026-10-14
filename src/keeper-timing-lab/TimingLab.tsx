'use client'

import { useEffect, useMemo, useState, type CSSProperties } from 'react'
import styles from './timingLab.module.css'
import { changedProfileFields, clampProfile, frameDurationMs, phaseFrameCounts, phaseLabels, profileDurationMs, sectionFrames, type LoopSection, type SavedProposal, type TimingCatalogue, type TimingFrame, type TimingProfile } from './model'

const STORAGE_KEY = 'keeper-timing-lab:v1'

function downloadJson(filename: string, value: unknown) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2) + '\n'], { type: 'application/json' }))
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  anchor.click()
  URL.revokeObjectURL(url)
}

function formatSeconds(milliseconds: number) {
  return `${(milliseconds / 1000).toFixed(2)}s`
}

function Playback({ title, frames, profile, section, loop, playSignal, pauseSignal, distance, interactive = false }: {
  title: string
  frames: TimingFrame[]
  profile: TimingProfile
  section: LoopSection
  loop: boolean
  playSignal: number
  pauseSignal: number
  distance: number
  interactive?: boolean
}) {
  const sequence = useMemo(() => sectionFrames(frames, section), [frames, section])
  const counts = useMemo(() => phaseFrameCounts(sequence), [sequence])
  const [index, setIndex] = useState(0)
  const [playing, setPlaying] = useState(false)
  useEffect(() => { setIndex(0); setPlaying(false) }, [sequence])
  useEffect(() => { if (playSignal > 0 && sequence.length) { setIndex(0); setPlaying(true) } }, [playSignal, sequence.length])
  useEffect(() => { if (pauseSignal > 0) setPlaying(false) }, [pauseSignal])
  useEffect(() => {
    if (!playing || !sequence.length) return
    const current = sequence[Math.min(index, sequence.length - 1)]
    const timer = window.setTimeout(() => {
      if (index + 1 < sequence.length) setIndex(index + 1)
      else if (loop) setIndex(0)
      else setPlaying(false)
    }, Math.max(32, Math.round(frameDurationMs(current, profile, counts))))
    return () => window.clearTimeout(timer)
  }, [counts, index, loop, playing, profile, sequence])
  const current = sequence[Math.min(index, Math.max(0, sequence.length - 1))]
  const progress = current ? current.x / Math.max(1, distance) : 0
  const actorStyle = { '--actor-x': `${10 + progress * 50}%` } as CSSProperties
  return <section className={styles.player}>
    <div className={styles.playerHeading}><div><h3>{title}</h3><p>{current ? `${phaseLabels[current.phase]} · ${current.pose} · ${index + 1}/${sequence.length}` : 'No frames'}</p></div><span>{formatSeconds(profileDurationMs(sequence, profile))}</span></div>
    <div className={styles.stage}>
      {current && <div className={styles.actor} style={actorStyle}><img src={current.src} alt={`${current.pose}, ${title}`} /></div>}
      <div className={styles.floorLine} aria-hidden="true" />
    </div>
    <div className={styles.gameScale}><span>Exact game scale</span>{current && <img src={current.src} alt="" />}</div>
    <div className={styles.frameMeter}><span style={{ width: `${sequence.length ? ((index + 1) / sequence.length) * 100 : 0}%` }} /></div>
    {interactive && <div className={styles.transport}>
      <button type="button" onClick={() => setPlaying((value) => !value)} disabled={!sequence.length}>{playing ? 'Pause' : 'Play'}</button>
      <button type="button" onClick={() => { setPlaying(false); setIndex((value) => Math.max(0, value - 1)) }} disabled={!sequence.length}>Previous frame</button>
      <button type="button" onClick={() => { setPlaying(false); setIndex((value) => Math.min(sequence.length - 1, value + 1)) }} disabled={!sequence.length}>Next frame</button>
    </div>}
  </section>
}

function Slider({ label, value, min, max, step, unit, help, onChange }: { label: string; value: number; min: number; max: number; step: number; unit: string; help: string; onChange: (value: number) => void }) {
  return <label className={styles.slider}>
    <span><strong>{label}</strong><output>{value}{unit}</output></span>
    <input type="range" min={min} max={max} step={step} value={value} onChange={(event) => onChange(Number(event.target.value))} />
    <small>{help}</small>
  </label>
}

export default function TimingLab() {
  const [catalogue, setCatalogue] = useState<TimingCatalogue | null>(null)
  const [loadError, setLoadError] = useState('')
  const [selectedClipId, setSelectedClipId] = useState('')
  const [profile, setProfile] = useState<TimingProfile | null>(null)
  const [projectDefaults, setProjectDefaults] = useState<TimingProfile | null>(null)
  const [saved, setSaved] = useState<SavedProposal[]>([])
  const [proposalName, setProposalName] = useState('Quicker front turn')
  const [sectionId, setSectionId] = useState('all')
  const [loop, setLoop] = useState(true)
  const [playSignal, setPlaySignal] = useState(0)
  const [pauseSignal, setPauseSignal] = useState(0)
  const [message, setMessage] = useState('')

  useEffect(() => {
    void fetch('/keeper-timing-lab/catalog-v2.json', { cache: 'no-store' })
      .then((response) => { if (!response.ok) throw new Error(`Catalogue returned ${response.status}`); return response.json() as Promise<TimingCatalogue> })
      .then((next) => {
        setCatalogue(next)
        const clip = next.clips[0]
        setSelectedClipId(clip?.id ?? '')
        setProfile(clip?.recommended ?? next.defaults)
        let stored: { projectDefaults?: TimingProfile; saved?: SavedProposal[] } = {}
        try { stored = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '{}') as typeof stored } catch { setMessage('Saved timing proposals could not be read; artwork is unaffected.') }
        setProjectDefaults(stored.projectDefaults ? clampProfile(stored.projectDefaults) : next.defaults)
        setSaved(Array.isArray(stored.saved) ? stored.saved : [])
        setPlaySignal(1)
      })
      .catch((error: Error) => setLoadError(error.message))
  }, [])

  useEffect(() => {
    if (catalogue && projectDefaults) localStorage.setItem(STORAGE_KEY, JSON.stringify({ version: 1, projectDefaults, saved }))
  }, [catalogue, projectDefaults, saved])

  const clip = catalogue?.clips.find((candidate) => candidate.id === selectedClipId) ?? catalogue?.clips[0]
  const section = catalogue?.loopSections.find((candidate) => candidate.id === sectionId) ?? catalogue?.loopSections[0]
  useEffect(() => { if (clip) setProfile(clip.recommended) }, [clip?.id])
  const candidate = profile ?? clip?.recommended
  const changes = clip && candidate ? changedProfileFields(clip.baseline, candidate) : []
  const isApprovedCandidate = candidate ? changedProfileFields(catalogue?.defaults ?? candidate, candidate).length === 0 : false
  const baselineDuration = clip ? profileDurationMs(clip.frames, clip.baseline) : 0
  const candidateDuration = clip && candidate ? profileDurationMs(clip.frames, candidate) : 0
  const approvedTransition = catalogue?.approvedTransitionProfile

  const patchProfile = (change: Partial<TimingProfile>) => {
    if (!candidate) return
    setProfile(clampProfile({ ...candidate, ...change }))
  }
  const saveProposal = () => {
    if (!clip || !candidate) return
    const item: SavedProposal = { id: `proposal-${Date.now()}`, name: proposalName.trim() || 'Untitled timing proposal', clipId: clip.id, savedAt: new Date().toISOString(), profile: candidate }
    setSaved((current) => [item, ...current])
    setMessage(`Saved “${item.name}” on this device. Artwork remains locked.`)
  }
  const exportProposal = () => {
    if (!clip || !candidate) return
    downloadJson(`${clip.id}-timing-proposal.json`, {
      version: 1, exportedAt: new Date().toISOString(), clipId: clip.id,
      sourceRegister: clip.sourceRegister, sourceRegisterSha256: clip.sourceRegisterSha256,
      artworkLocked: true, baseline: clip.baseline, proposal: candidate,
      changedFields: changedProfileFields(clip.baseline, candidate),
      durationsMs: { baseline: baselineDuration, proposal: candidateDuration },
    })
  }

  if (loadError) return <main className={styles.lab}><div className={styles.loading}><h1>Keeper Timing Lab</h1><p>Could not load the timing catalogue: {loadError}</p></div></main>
  if (!catalogue || !clip || !section || !candidate || !projectDefaults) return <main className={styles.lab}><div className={styles.loading}><h1>Keeper Timing Lab</h1><p>Loading immutable artwork and timing profiles…</p></div></main>

  return <main className={styles.lab}>
    <header className={styles.header}>
      <div><p className={styles.eyebrow}>Artwork locked · timing remains adjustable</p><h1>Keeper Timing Lab</h1><p>Tune the rhythm of every phase without redrawing, reordering or silently promoting approved frames.</p></div>
      <nav><a href="/keeper-review/keeper-prime-walk-stop-turn-front-v1/">Source review</a><a href="/animation-workbench">Animation Workbench</a></nav>
    </header>

    <section className={styles.statusBar}>
      <div><strong>{clip.title}</strong><span>{clip.description}</span></div>
      <span className={styles.locked}>Approved pixels locked</span>
      <span className={approvedTransition ? styles.approved : styles.pending}>{approvedTransition ? `${approvedTransition.name} approved` : 'Timing proposal'}</span>
    </section>
    {message && <button type="button" className={styles.message} onClick={() => setMessage('')}>{message}</button>}

    <div className={styles.shell}>
      <aside className={styles.sidebar}>
        <section><h2>Animation library</h2><p>More approved routes can be added without changing this timing model.</p>{catalogue.clips.map((item) => <button key={item.id} type="button" className={item.id === clip.id ? styles.selectedClip : ''} onClick={() => setSelectedClipId(item.id)}><strong>{item.title}</strong><span>{item.outfit} uniform</span><small>{item.status === 'artwork-and-fast-transition-timing-approved' ? 'Artwork + transition timing approved' : 'Artwork accepted · timing open'}</small></button>)}</section>
        <section><h2>Saved proposals</h2>{saved.filter((item) => item.clipId === clip.id).map((item) => <div className={styles.savedItem} key={item.id}><button type="button" onClick={() => { setProfile(item.profile); setMessage(`Loaded “${item.name}”.`) }}><strong>{item.name}</strong><span>{item.profile.turnFps} fps turn</span></button><button type="button" aria-label={`Delete ${item.name}`} onClick={() => setSaved((current) => current.filter((candidateItem) => candidateItem.id !== item.id))}>×</button></div>)}{!saved.some((item) => item.clipId === clip.id) && <p className={styles.empty}>No saved proposals yet.</p>}</section>
      </aside>

      <div className={styles.content}>
        <section className={styles.compareHeader}>
          <div><p className={styles.kicker}>A/B timing comparison</p><h2>Reviewed timing against your live proposal</h2><p>{approvedTransition ? 'Fast Timing V1 is approved for walks, stopping bridges and turns. Action animation timing remains independent.' : 'The recommended starting point changes only the turn from 8 to 10 fps.'}</p></div>
          <div className={styles.masterControls}><button type="button" className={styles.primary} onClick={() => setPlaySignal((value) => value + 1)}>Play both</button><button type="button" onClick={() => setPauseSignal((value) => value + 1)}>Pause both</button><label>Loop section<select value={sectionId} onChange={(event) => setSectionId(event.target.value)}>{catalogue.loopSections.map((item) => <option key={item.id} value={item.id}>{item.label}</option>)}</select></label><label className={styles.check}><input type="checkbox" checked={loop} onChange={(event) => setLoop(event.target.checked)} /> Loop</label></div>
        </section>

        <div className={styles.players}>
          <Playback title="A · original reviewed timing" frames={clip.frames} profile={clip.baseline} section={section} loop={loop} playSignal={playSignal} pauseSignal={pauseSignal} distance={clip.distanceHighResolutionPixels} />
          <Playback title={approvedTransition && isApprovedCandidate ? 'B · approved Fast Timing V1' : 'B · live timing proposal'} frames={clip.frames} profile={candidate} section={section} loop={loop} playSignal={playSignal} pauseSignal={pauseSignal} distance={clip.distanceHighResolutionPixels} interactive />
        </div>

        <section className={styles.tuningPanel}>
          <div className={styles.panelHeading}><div><p className={styles.kicker}>Independent phase timing</p><h2>Tune the rhythm, not the artwork</h2></div><div className={styles.duration}><span>Route duration</span><strong>{formatSeconds(candidateDuration)}</strong><small>{candidateDuration < baselineDuration ? `${formatSeconds(baselineDuration - candidateDuration)} quicker` : candidateDuration > baselineDuration ? `${formatSeconds(candidateDuration - baselineDuration)} slower` : 'matches reviewed timing'}</small></div></div>
          <div className={styles.sliders}>
            <Slider label="Walk" value={candidate.walkFps} min={4} max={16} step={0.5} unit=" fps" help="The repeating locomotion cadence." onChange={(walkFps) => patchProfile({ walkFps })} />
            <Slider label="Deceleration" value={candidate.decelerationFps} min={4} max={16} step={0.5} unit=" fps" help="The four frames that bring him to rest." onChange={(decelerationFps) => patchProfile({ decelerationFps })} />
            <Slider label="Neutral beat" value={candidate.settleMs} min={0} max={500} step={25} unit=" ms" help="The intentional pause before the turn begins." onChange={(settleMs) => patchProfile({ settleMs })} />
            <Slider label="Turn" value={candidate.turnFps} min={4} max={16} step={0.5} unit=" fps" help="Your requested adjustment. Recommended: 10 fps." onChange={(turnFps) => patchProfile({ turnFps })} />
            <Slider label="Front hold" value={candidate.frontHoldMs} min={125} max={1500} step={125} unit=" ms" help="Review-only hold after reaching full face." onChange={(frontHoldMs) => patchProfile({ frontHoldMs })} />
          </div>
        </section>

        <section className={styles.presets}>
          <div className={styles.panelHeading}><div><p className={styles.kicker}>Quick comparisons</p><h2>Timing presets</h2></div><p>{changes.length ? `${changes.length} field${changes.length === 1 ? '' : 's'} differ from reviewed V1.` : 'This matches reviewed V1.'}</p></div>
          <div className={styles.presetGrid}>{catalogue.presets.map((preset) => <button type="button" key={preset.id} onClick={() => { setProfile(preset.profile); setMessage(`Applied “${preset.name}”.`) }}><strong>{preset.name}</strong><span>{preset.description}</span><small>{preset.status === 'approved' ? 'Project authority' : preset.status === 'superseded' ? 'Retained history' : `${preset.profile.turnFps} fps turn`}</small></button>)}</div>
        </section>

        <section className={styles.savePanel}>
          <div><p className={styles.kicker}>Non-destructive proposals</p><h2>Save or compare personal alternatives</h2><p>The approved project transition standard comes from the repository. Saving here keeps a private preview preference on this device and never changes artwork, Final, production or action timing.</p></div>
          <div className={styles.saveControls}><input value={proposalName} onChange={(event) => setProposalName(event.target.value)} aria-label="Proposal name" /><button type="button" onClick={saveProposal}>Save proposal</button><button type="button" onClick={exportProposal}>Export JSON</button><button type="button" aria-label="Use as project defaults on this device only" onClick={() => { setProjectDefaults(candidate); setMessage('Set this profile as this device’s personal preview default.') }}>Use as personal preview default</button><button type="button" onClick={() => { setProfile(catalogue.defaults); setMessage('Restored approved Fast Timing V1.') }}>Reset to approved</button></div>
          <dl><div><dt>Project default</dt><dd>Walk {catalogue.defaults.walkFps} · deceleration {catalogue.defaults.decelerationFps} · turn {catalogue.defaults.turnFps} fps</dd></div><div><dt>Personal preview</dt><dd>Walk {projectDefaults.walkFps} · deceleration {projectDefaults.decelerationFps} · turn {projectDefaults.turnFps} fps</dd></div><div><dt>Changed fields</dt><dd>{changes.length ? changes.join(', ') : 'none'}</dd></div><div><dt>Artwork SHA-256</dt><dd>{clip.sourceRegisterSha256}</dd></div></dl>
        </section>

        {approvedTransition && <section className={styles.scope}><p className={styles.kicker}>Approved scope</p><h2>Fast between activities; expressive inside them</h2><p>{approvedTransition.designDirection}</p><div><article><strong>Fast Timing V1 applies to</strong><ul>{approvedTransition.appliesTo.map((item) => <li key={item}>{item}</li>)}</ul></article><article><strong>Timed separately per action</strong><ul>{approvedTransition.excludes.map((item) => <li key={item}>{item}</li>)}</ul></article></div><p className={styles.policy}>{approvedTransition.policy}</p></section>}

        <section className={styles.contract}><h2>Approval model</h2><div><article><strong>1 · Artwork authority</strong><p>Frame pixels, order, endpoints and root motion remain hash-pinned.</p></article><article><strong>2 · Timing profile</strong><p>Phase speeds and deliberate holds are tuned here and approved separately.</p></article><article><strong>3 · Final and production</strong><p>Still require their own explicit promotion after complete route review.</p></article></div><p className={styles.limit}>Recorded visual limitation: {clip.acceptedVisualLimitation}.</p></section>
      </div>
    </div>
  </main>
}
