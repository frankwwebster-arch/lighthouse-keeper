'use client'

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import styles from './rearTaskAlignmentWorkbench.module.css'

export type RearTaskAlignmentFrame = {
  position: number
  label: string
  torsoSrc: string
  torsoSha256: string
  defaultLegsX: number
}

type Props = {
  frames: RearTaskAlignmentFrame[]
  legsSrc: string
  legsSha256: string
}

type Layer = 'torso' | 'legs'
type Adjustment = {
  torsoX: number
  torsoY: number
  torsoCutY: number
  legsX: number
  legsY: number
  legsCropY: number
  aligned: boolean
}

const WIDTH = 256
const HEIGHT = 320
const STORAGE_KEY = 'prime-keeper-rear-task-alignment:v1'

function defaultAdjustment(frame: RearTaskAlignmentFrame): Adjustment {
  return {
    torsoX: 0,
    torsoY: 0,
    torsoCutY: 214,
    legsX: frame.defaultLegsX,
    legsY: 0,
    legsCropY: 214,
    aligned: false,
  }
}

function loadImage(src: string) {
  return new Promise<HTMLImageElement>((resolve, reject) => {
    const image = new Image()
    image.onload = () => image.decode?.().then(() => resolve(image)).catch(() => resolve(image)) ?? resolve(image)
    image.onerror = () => reject(new Error(`Could not decode ${src}`))
    image.src = src
  })
}

function clamp(value: number, minimum: number, maximum: number) {
  return Math.min(maximum, Math.max(minimum, Math.round(value)))
}

export default function RearTaskAlignmentWorkbench({ frames, legsSrc, legsSha256 }: Props) {
  const defaults = useMemo(() => Object.fromEntries(frames.map((frame) => [frame.position, defaultAdjustment(frame)])) as Record<number, Adjustment>, [frames])
  const [adjustments, setAdjustments] = useState<Record<number, Adjustment>>(defaults)
  const [frameIndex, setFrameIndex] = useState(0)
  const [selectedLayer, setSelectedLayer] = useState<Layer>('legs')
  const [zoom, setZoom] = useState(2)
  const [ready, setReady] = useState(false)
  const [loadError, setLoadError] = useState('')
  const [hydrated, setHydrated] = useState(false)
  const [playing, setPlaying] = useState(false)
  const [copyMessage, setCopyMessage] = useState('')
  const images = useRef<Map<string, HTMLImageElement>>(new Map())
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const seamRef = useRef<HTMLCanvasElement>(null)
  const torsoSourceRef = useRef<HTMLCanvasElement>(null)
  const legsSourceRef = useRef<HTMLCanvasElement>(null)
  const dragRef = useRef<{ pointerId: number; startX: number; startY: number; initialX: number; initialY: number } | null>(null)

  const frame = frames[frameIndex]
  const adjustment = adjustments[frame.position] ?? defaultAdjustment(frame)
  const completed = Object.values(adjustments).filter((item) => item.aligned).length

  useEffect(() => {
    try {
      const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '{}') as Record<number, Partial<Adjustment>>
      setAdjustments(Object.fromEntries(frames.map((item) => [item.position, { ...defaultAdjustment(item), ...(stored[item.position] ?? {}) }])))
    } catch {
      setAdjustments(defaults)
    }
    setHydrated(true)
  }, [defaults, frames])

  useEffect(() => {
    if (hydrated) localStorage.setItem(STORAGE_KEY, JSON.stringify(adjustments))
  }, [adjustments, hydrated])

  useEffect(() => {
    let cancelled = false
    Promise.all([...new Set([legsSrc, ...frames.map((item) => item.torsoSrc)])].map(async (src) => {
      const image = await loadImage(src)
      images.current.set(src, image)
    })).then(() => {
      if (!cancelled) setReady(true)
    }).catch((error: Error) => {
      if (!cancelled) setLoadError(error.message)
    })
    return () => { cancelled = true }
  }, [frames, legsSrc])

  const renderComposite = useCallback(() => {
    const canvas = canvasRef.current
    const seam = seamRef.current
    const torsoSourceCanvas = torsoSourceRef.current
    const legsSourceCanvas = legsSourceRef.current
    const torso = images.current.get(frame.torsoSrc)
    const legs = images.current.get(legsSrc)
    if (!canvas || !seam || !torsoSourceCanvas || !legsSourceCanvas || !torso || !legs) return
    const context = canvas.getContext('2d')
    const seamContext = seam.getContext('2d')
    const torsoSourceContext = torsoSourceCanvas.getContext('2d')
    const legsSourceContext = legsSourceCanvas.getContext('2d')
    if (!context || !seamContext || !torsoSourceContext || !legsSourceContext) return
    context.clearRect(0, 0, WIDTH, HEIGHT)
    context.imageSmoothingEnabled = false

    const legsCropY = clamp(adjustment.legsCropY, 0, HEIGHT - 1)
    // The approved rear authority is a full standing figure. Its hands sit at
    // waist height, outside the verified lower-body ownership bounds. Keep the
    // exact trouser/boot pixels only: the narrow waist through row 230, then
    // the wider legs below. Nothing is repainted or inferred.
    const waistStart = Math.max(legsCropY, 214)
    if (waistStart < 231) context.drawImage(legs, 82, waistStart, 91, 231 - waistStart, 82 + adjustment.legsX, waistStart + adjustment.legsY, 91, 231 - waistStart)
    const lowerStart = Math.max(legsCropY, 231)
    if (lowerStart < HEIGHT) context.drawImage(legs, 70, lowerStart, 117, HEIGHT - lowerStart, 70 + adjustment.legsX, lowerStart + adjustment.legsY, 117, HEIGHT - lowerStart)

    const torsoCutY = clamp(adjustment.torsoCutY, 1, HEIGHT)
    context.drawImage(torso, 0, 0, WIDTH, torsoCutY, adjustment.torsoX, adjustment.torsoY, WIDTH, torsoCutY)

    torsoSourceContext.clearRect(0, 0, WIDTH, HEIGHT)
    torsoSourceContext.drawImage(torso, 0, 0, WIDTH, torsoCutY, 0, 0, WIDTH, torsoCutY)
    legsSourceContext.clearRect(0, 0, WIDTH, HEIGHT)
    if (waistStart < 231) legsSourceContext.drawImage(legs, 82, waistStart, 91, 231 - waistStart, 82, waistStart, 91, 231 - waistStart)
    if (lowerStart < HEIGHT) legsSourceContext.drawImage(legs, 70, lowerStart, 117, HEIGHT - lowerStart, 70, lowerStart, 117, HEIGHT - lowerStart)

    seamContext.clearRect(0, 0, seam.width, seam.height)
    seamContext.imageSmoothingEnabled = false
    seamContext.drawImage(canvas, 48, 184, 160, 72, 0, 0, 160, 72)
  }, [adjustment, frame.torsoSrc, legsSrc])

  useEffect(() => { renderComposite() }, [renderComposite, ready])

  useEffect(() => {
    if (!playing || !ready) return
    const timer = window.setTimeout(() => setFrameIndex((current) => (current + 1) % frames.length), 250)
    return () => window.clearTimeout(timer)
  }, [frameIndex, frames.length, playing, ready])

  const updateCurrent = useCallback((change: Partial<Adjustment> | ((current: Adjustment) => Adjustment)) => {
    setAdjustments((current) => {
      const existing = current[frame.position] ?? defaultAdjustment(frame)
      const next = typeof change === 'function' ? change(existing) : { ...existing, ...change }
      return { ...current, [frame.position]: next }
    })
  }, [frame])

  const nudge = useCallback((dx: number, dy: number) => {
    updateCurrent((current) => selectedLayer === 'torso'
      ? { ...current, torsoX: current.torsoX + dx, torsoY: current.torsoY + dy, aligned: false }
      : { ...current, legsX: current.legsX + dx, legsY: current.legsY + dy, aligned: false })
  }, [selectedLayer, updateCurrent])

  const exportPayload = useCallback(() => ({
    schema: 'lighthouse-keeper/prime-rear-task-manual-alignment@1',
    savedAt: new Date().toISOString(),
    source: {
      torsoBatch: 'keeper-prime-morning-drafts-v6',
      legsSha256,
      layerOrder: ['approved rear legs', 'moving action torso'],
    },
    dimensions: { width: WIDTH, height: HEIGHT, floorY: 316 },
    frames: frames.map((item) => ({
      position: item.position,
      label: item.label,
      torsoSrc: item.torsoSrc,
      torsoSha256: item.torsoSha256,
      ...adjustments[item.position],
    })),
  }), [adjustments, frames, legsSha256])

  const copySettings = async () => {
    await navigator.clipboard.writeText(JSON.stringify(exportPayload(), null, 2))
    setCopyMessage('All 21 frame settings copied')
    window.setTimeout(() => setCopyMessage(''), 1800)
  }

  const downloadSettings = () => {
    const blob = new Blob([`${JSON.stringify(exportPayload(), null, 2)}\n`], { type: 'application/json' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = 'prime-keeper-rear-task-manual-alignment.json'
    link.click()
    URL.revokeObjectURL(link.href)
  }

  const downloadFrame = () => {
    const link = document.createElement('a')
    link.href = canvasRef.current?.toDataURL('image/png') ?? ''
    link.download = `prime-keeper-rear-task-frame-${String(frame.position).padStart(2, '0')}.png`
    link.click()
  }

  const pointerPosition = (event: React.PointerEvent<HTMLCanvasElement>) => {
    const bounds = event.currentTarget.getBoundingClientRect()
    return {
      x: (event.clientX - bounds.left) * WIDTH / bounds.width,
      y: (event.clientY - bounds.top) * HEIGHT / bounds.height,
    }
  }

  const onPointerDown = (event: React.PointerEvent<HTMLCanvasElement>) => {
    if (!ready) return
    setPlaying(false)
    const point = pointerPosition(event)
    dragRef.current = {
      pointerId: event.pointerId,
      startX: point.x,
      startY: point.y,
      initialX: selectedLayer === 'torso' ? adjustment.torsoX : adjustment.legsX,
      initialY: selectedLayer === 'torso' ? adjustment.torsoY : adjustment.legsY,
    }
    event.currentTarget.setPointerCapture(event.pointerId)
  }

  const onPointerMove = (event: React.PointerEvent<HTMLCanvasElement>) => {
    const drag = dragRef.current
    if (!drag || drag.pointerId !== event.pointerId) return
    const point = pointerPosition(event)
    const x = drag.initialX + Math.round(point.x - drag.startX)
    const y = drag.initialY + Math.round(point.y - drag.startY)
    updateCurrent((current) => selectedLayer === 'torso'
      ? { ...current, torsoX: x, torsoY: y, aligned: false }
      : { ...current, legsX: x, legsY: y, aligned: false })
  }

  const stopDragging = (event: React.PointerEvent<HTMLCanvasElement>) => {
    if (dragRef.current?.pointerId === event.pointerId) dragRef.current = null
  }

  const onKeyDown = (event: React.KeyboardEvent<HTMLCanvasElement>) => {
    const step = event.shiftKey ? 8 : 1
    const direction = event.key === 'ArrowLeft' ? [-step, 0] : event.key === 'ArrowRight' ? [step, 0] : event.key === 'ArrowUp' ? [0, -step] : event.key === 'ArrowDown' ? [0, step] : null
    if (!direction) return
    event.preventDefault()
    nudge(direction[0], direction[1])
  }

  const changeFrame = (next: number) => {
    setPlaying(false)
    setFrameIndex(clamp(next, 0, frames.length - 1))
  }

  return <main className={styles.page}>
    <header className={styles.hero}>
      <nav><a href="/prime-keeper-animation-drafts">Animation review</a><span>/</span><strong>Manual rear-task alignment</strong></nav>
      <p className={styles.eyebrow}>Exact source layers · no artwork overwritten</p>
      <h1>You place<br />the join.</h1>
      <p>This is the fallback you requested. Each of frames 11–31 has the exact moving action torso above the exact approved rear legs. Drag either layer, nudge it one authoring pixel at a time, and move both crop boundaries. Every frame saves independently in this browser.</p>
    </header>

    <section className={styles.status} aria-live="polite">
      <strong>{loadError || (ready ? 'All 22 exact source images decoded' : 'Decoding exact source images…')}</strong>
      <span>{completed} / {frames.length} marked aligned</span>
    </section>

    <section className={styles.workbench}>
      <div className={styles.stageColumn}>
        <div className={styles.stageHeader}>
          <div><span>Frame {frame.position}</span><h2>{frame.label}</h2></div>
          <label>Zoom <select value={zoom} onChange={(event) => setZoom(Number(event.target.value))}><option value={1}>100%</option><option value={1.5}>150%</option><option value={2}>200%</option><option value={2.5}>250%</option></select></label>
        </div>
        <div className={styles.canvasScroller}>
          <div className={styles.canvasWrap} style={{ width: WIDTH * zoom, height: HEIGHT * zoom }}>
            <canvas
              ref={canvasRef}
              width={WIDTH}
              height={HEIGHT}
              style={{ width: WIDTH * zoom, height: HEIGHT * zoom }}
              tabIndex={0}
              aria-label={`Frame ${frame.position} composite. Drag selected ${selectedLayer} layer or use arrow keys.`}
              onPointerDown={onPointerDown}
              onPointerMove={onPointerMove}
              onPointerUp={stopDragging}
              onPointerCancel={stopDragging}
              onKeyDown={onKeyDown}
            />
            <i className={styles.floorGuide} style={{ top: 316 * zoom }}><span>floor 316</span></i>
            <i className={styles.cropGuide} style={{ top: (selectedLayer === 'torso' ? adjustment.torsoCutY + adjustment.torsoY : adjustment.legsCropY + adjustment.legsY) * zoom }}><span>{selectedLayer} boundary</span></i>
          </div>
        </div>
        <div className={styles.seamBlock}>
          <span>4× waist inspection</span>
          <div><canvas ref={seamRef} width={160} height={72} /></div>
        </div>
      </div>

      <aside className={styles.controls}>
        <section>
          <h3>1. Select the layer</h3>
          <div className={styles.layerButtons}>
            <button className={selectedLayer === 'torso' ? styles.active : ''} onClick={() => setSelectedLayer('torso')}><span>Moving torso</span><code>x {adjustment.torsoX} · y {adjustment.torsoY}</code></button>
            <button className={selectedLayer === 'legs' ? styles.active : ''} onClick={() => setSelectedLayer('legs')}><span>Approved legs</span><code>x {adjustment.legsX} · y {adjustment.legsY}</code></button>
          </div>
          <p>Drag directly on the large character, or focus it and use the arrow keys. Shift + arrow moves eight pixels.</p>
        </section>

        <section>
          <h3>2. Nudge by one pixel</h3>
          <div className={styles.nudge}>
            <button onClick={() => nudge(0, -1)}>↑</button>
            <button onClick={() => nudge(-1, 0)}>←</button>
            <button onClick={() => nudge(0, 1)}>↓</button>
            <button onClick={() => nudge(1, 0)}>→</button>
          </div>
        </section>

        <section>
          <h3>3. Set the join</h3>
          <label>Torso visible through row <output>{adjustment.torsoCutY - 1}</output><input type="range" min={204} max={226} value={adjustment.torsoCutY} onChange={(event) => updateCurrent({ torsoCutY: Number(event.target.value), aligned: false })} /></label>
          <label>Legs begin from source row <output>{adjustment.legsCropY}</output><input type="range" min={204} max={230} value={adjustment.legsCropY} onChange={(event) => updateCurrent({ legsCropY: Number(event.target.value), aligned: false })} /></label>
          <p>The legs are drawn first; the moving torso is drawn over them. Cropping does not repaint, stretch or generate a pixel.</p>
        </section>

        <section className={styles.frameActions}>
          <h3>4. Save this frame</h3>
          <button className={adjustment.aligned ? styles.approved : ''} onClick={() => updateCurrent({ aligned: !adjustment.aligned })}>{adjustment.aligned ? '✓ Marked aligned' : 'Mark frame aligned'}</button>
          <button onClick={() => updateCurrent(defaultAdjustment(frame))}>Reset this frame</button>
          <button onClick={() => setAdjustments((current) => Object.fromEntries(frames.map((item) => [item.position, { ...(current[item.position] ?? defaultAdjustment(item)), torsoY: adjustment.torsoY, torsoCutY: adjustment.torsoCutY, legsY: adjustment.legsY, legsCropY: adjustment.legsCropY, aligned: false }]))) }>Copy vertical join to all frames</button>
          <button onClick={downloadFrame}>Download current 256×320 PNG</button>
        </section>
      </aside>
    </section>

    <section className={styles.timeline}>
      <div className={styles.transport}>
        <button disabled={!ready} onClick={() => changeFrame(frameIndex - 1)}>← Frame</button>
        <button disabled={!ready} onClick={() => setPlaying((current) => !current)}>{playing ? 'Ⅱ Pause' : '▶ Play all'}</button>
        <button disabled={!ready} onClick={() => changeFrame(frameIndex + 1)}>Frame →</button>
        <output>{frameIndex + 1} / {frames.length}</output>
      </div>
      <div className={styles.frameRail}>{frames.map((item, index) => <button key={item.position} className={`${index === frameIndex ? styles.current : ''} ${adjustments[item.position]?.aligned ? styles.done : ''}`} onClick={() => changeFrame(index)}><span>{item.position}</span><small>{adjustments[item.position]?.aligned ? '✓' : ''}</small></button>)}</div>
    </section>

    <section className={styles.sources}>
      <div><span>Exact moving torso layer for frame {frame.position}</span><canvas style={{ gridRow: '1 / 3', width: '15rem', height: '18.75rem', maxWidth: '100%', backgroundColor: '#e2e7e2' }} ref={torsoSourceRef} width={WIDTH} height={HEIGHT} aria-label={`Isolated moving torso layer for frame ${frame.position}`} /><code>{frame.torsoSha256}</code></div>
      <div><span>Exact approved legs layer</span><canvas style={{ gridRow: '1 / 3', width: '15rem', height: '18.75rem', maxWidth: '100%', backgroundColor: '#e2e7e2' }} ref={legsSourceRef} width={WIDTH} height={HEIGHT} aria-label="Isolated approved rear trousers and boots layer" /><code>{legsSha256}</code></div>
    </section>

    <section className={styles.export}>
      <div><span>05</span><h2>Hand the positions back</h2></div>
      <p>The settings include every layer position and crop boundary for all 21 frames, keyed to the immutable source hashes. Copy or download them and send the file back here; they can then be reproduced exactly.</p>
      <div><button onClick={copySettings}>Copy all settings</button><button onClick={downloadSettings}>Download settings JSON</button><output aria-live="polite">{copyMessage}</output></div>
    </section>
  </main>
}
