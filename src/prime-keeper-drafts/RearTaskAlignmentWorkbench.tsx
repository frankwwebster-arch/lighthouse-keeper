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
type EditorMode = 'crop' | 'align'
type HemCurve = [number, number, number, number, number]
type Adjustment = {
  torsoX: number
  torsoY: number
  torsoCutY: number
  hemOffsets: HemCurve
  legsX: number
  legsY: number
  legsCropY: number
  cropConfirmed: boolean
  aligned: boolean
}

type OpaqueBounds = { x0: number; y0: number; x1: number; y1: number; width: number; height: number; centreX: number }
type DimensionAudit = { composite: OpaqueBounds; authority: OpaqueBounds }

const WIDTH = 256
const HEIGHT = 320
const CLEAN_TROUSER_START = 219
const TROUSER_UNDERLAP = 4
const WAIST_X = 82
const WAIST_WIDTH = 91
const UNDERLAP_SAMPLE_X = 100
const UNDERLAP_SAMPLE_ROW = 220
const HEM_CONTROL_X = [82, 105, 128, 151, 174] as const
const DEFAULT_HEM_OFFSETS: HemCurve = [-4, -1, 0, -1, -4]
const HEM_POINT_NAMES = ['left edge', 'left middle', 'centre', 'right middle', 'right edge'] as const
const STORAGE_KEY = 'prime-keeper-rear-task-alignment:v1'

function defaultAdjustment(frame: RearTaskAlignmentFrame): Adjustment {
  return {
    torsoX: 0,
    torsoY: 0,
    torsoCutY: 214,
    hemOffsets: [...DEFAULT_HEM_OFFSETS],
    legsX: frame.defaultLegsX,
    legsY: 0,
    legsCropY: CLEAN_TROUSER_START,
    cropConfirmed: false,
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

function normaliseHemOffsets(value: unknown): HemCurve {
  if (!Array.isArray(value) || value.length !== HEM_CONTROL_X.length || value.some((item) => typeof item !== 'number' || !Number.isFinite(item))) return [...DEFAULT_HEM_OFFSETS]
  return value.map((item) => clamp(Number(item), -16, 16)) as HemCurve
}

function hemPoints(adjustment: Adjustment, includePosition = true) {
  const x = includePosition ? adjustment.torsoX : 0
  const y = includePosition ? adjustment.torsoY : 0
  return HEM_CONTROL_X.map((controlX, index) => ({ x: controlX + x, y: adjustment.torsoCutY + adjustment.hemOffsets[index] + y }))
}

function traceTorsoMask(context: CanvasRenderingContext2D, points: ReturnType<typeof hemPoints>) {
  context.beginPath()
  context.moveTo(0, 0)
  context.lineTo(WIDTH, 0)
  context.lineTo(WIDTH, points[points.length - 1].y)
  for (let index = points.length - 1; index >= 0; index -= 1) context.lineTo(points[index].x, points[index].y)
  context.lineTo(0, points[0].y)
  context.closePath()
}

function traceHem(context: CanvasRenderingContext2D, points: ReturnType<typeof hemPoints>) {
  context.beginPath()
  context.moveTo(points[0].x, points[0].y)
  for (let index = 1; index < points.length; index += 1) context.lineTo(points[index].x, points[index].y)
}

function curveYAt(points: ReturnType<typeof hemPoints>, x: number) {
  if (x <= points[0].x) return points[0].y
  if (x >= points[points.length - 1].x) return points[points.length - 1].y
  for (let index = 1; index < points.length; index += 1) {
    if (x <= points[index].x) {
      const left = points[index - 1]
      const right = points[index]
      const progress = (x - left.x) / (right.x - left.x)
      return Math.round(left.y + (right.y - left.y) * progress)
    }
  }
  return points[points.length - 1].y
}

function opaqueBounds(context: CanvasRenderingContext2D): OpaqueBounds | null {
  const pixels = context.getImageData(0, 0, WIDTH, HEIGHT).data
  let x0 = WIDTH
  let y0 = HEIGHT
  let x1 = -1
  let y1 = -1
  for (let y = 0; y < HEIGHT; y += 1) {
    for (let x = 0; x < WIDTH; x += 1) {
      if (pixels[(y * WIDTH + x) * 4 + 3] < 128) continue
      x0 = Math.min(x0, x)
      y0 = Math.min(y0, y)
      x1 = Math.max(x1, x)
      y1 = Math.max(y1, y)
    }
  }
  return x1 < 0 ? null : { x0, y0, x1, y1, width: x1 - x0 + 1, height: y1 - y0 + 1, centreX: (x0 + x1) / 2 }
}

export default function RearTaskAlignmentWorkbench({ frames, legsSrc, legsSha256 }: Props) {
  const defaults = useMemo(() => Object.fromEntries(frames.map((frame) => [frame.position, defaultAdjustment(frame)])) as Record<number, Adjustment>, [frames])
  const [adjustments, setAdjustments] = useState<Record<number, Adjustment>>(defaults)
  const [frameIndex, setFrameIndex] = useState(0)
  const [selectedLayer, setSelectedLayer] = useState<Layer>('legs')
  const [editorMode, setEditorMode] = useState<EditorMode>('crop')
  const [selectedHemPoint, setSelectedHemPoint] = useState(2)
  const [dimensionAudit, setDimensionAudit] = useState<DimensionAudit | null>(null)
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
  const dragRef = useRef<{ kind: EditorMode; pointerId: number; startX: number; startY: number; initialX: number; initialY: number; hemIndex?: number } | null>(null)

  const frame = frames[frameIndex]
  const adjustment = adjustments[frame.position] ?? defaultAdjustment(frame)
  const cropped = Object.values(adjustments).filter((item) => item.cropConfirmed).length
  const completed = Object.values(adjustments).filter((item) => item.aligned).length

  useEffect(() => {
    try {
      const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '{}') as Record<number, Partial<Adjustment>>
      setAdjustments(Object.fromEntries(frames.map((item) => {
        const restored = { ...defaultAdjustment(item), ...(stored[item.position] ?? {}) }
        return [item.position, {
          ...restored,
          legsCropY: clamp(restored.legsCropY, CLEAN_TROUSER_START, 230),
          hemOffsets: normaliseHemOffsets(restored.hemOffsets),
        }]
      })))
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

    const legsCropY = clamp(adjustment.legsCropY, CLEAN_TROUSER_START, HEIGHT - 1)
    const points = hemPoints(adjustment)
    const sourcePoints = hemPoints(adjustment, false)
    // The approved rear authority is a full standing figure. Its hands sit at
    // waist height, outside the verified lower-body ownership bounds. Keep the
    // exact trouser/boot pixels only: the narrow waist through row 230, then
    // the wider legs below. Rows 214–218 contain the authority's visible top
    // seam, so the clean trousers begin at row 219. One exact flat-colour pixel
    // from the clean trouser interior is repeated above that boundary as a
    // seam-free safety underlap. It remains behind the torso and prevents a
    // transparent tear when the torso moves laterally.
    const waistStart = Math.max(legsCropY, CLEAN_TROUSER_START)
    const waistDestination = waistStart + adjustment.legsY
    if (editorMode === 'align') {
      for (let column = 0; column < WAIST_WIDTH; column += 1) {
        const x = WAIST_X + adjustment.legsX + column
        const underlapTop = Math.min(waistDestination, curveYAt(points, x) - TROUSER_UNDERLAP)
        for (let y = underlapTop; y < waistDestination; y += 1) {
          context.drawImage(legs, UNDERLAP_SAMPLE_X, UNDERLAP_SAMPLE_ROW, 1, 1, x, y, 1, 1)
        }
      }
    }
    if (editorMode === 'align' && waistStart < 231) context.drawImage(legs, WAIST_X, waistStart, WAIST_WIDTH, 231 - waistStart, WAIST_X + adjustment.legsX, waistDestination, WAIST_WIDTH, 231 - waistStart)
    const lowerStart = Math.max(legsCropY, 231)
    if (editorMode === 'align' && lowerStart < HEIGHT) context.drawImage(legs, 70, lowerStart, 117, HEIGHT - lowerStart, 70 + adjustment.legsX, lowerStart + adjustment.legsY, 117, HEIGHT - lowerStart)

    context.save()
    traceTorsoMask(context, points)
    context.clip()
    context.drawImage(torso, adjustment.torsoX, adjustment.torsoY)
    context.restore()
    traceHem(context, points)
    context.strokeStyle = '#000000'
    context.lineWidth = 2
    context.lineCap = 'round'
    context.lineJoin = 'round'
    context.stroke()

    torsoSourceContext.clearRect(0, 0, WIDTH, HEIGHT)
    torsoSourceContext.save()
    traceTorsoMask(torsoSourceContext, sourcePoints)
    torsoSourceContext.clip()
    torsoSourceContext.drawImage(torso, 0, 0)
    torsoSourceContext.restore()
    traceHem(torsoSourceContext, sourcePoints)
    torsoSourceContext.strokeStyle = '#000000'
    torsoSourceContext.lineWidth = 2
    torsoSourceContext.lineCap = 'round'
    torsoSourceContext.lineJoin = 'round'
    torsoSourceContext.stroke()
    legsSourceContext.clearRect(0, 0, WIDTH, HEIGHT)
    for (let column = 0; column < WAIST_WIDTH; column += 1) {
      const x = WAIST_X + column
      const underlapTop = Math.min(waistStart, curveYAt(sourcePoints, x) - TROUSER_UNDERLAP)
      for (let y = underlapTop; y < waistStart; y += 1) {
        legsSourceContext.drawImage(legs, UNDERLAP_SAMPLE_X, UNDERLAP_SAMPLE_ROW, 1, 1, x, y, 1, 1)
      }
    }
    if (waistStart < 231) legsSourceContext.drawImage(legs, WAIST_X, waistStart, WAIST_WIDTH, 231 - waistStart, WAIST_X, waistStart, WAIST_WIDTH, 231 - waistStart)
    if (lowerStart < HEIGHT) legsSourceContext.drawImage(legs, 70, lowerStart, 117, HEIGHT - lowerStart, 70, lowerStart, 117, HEIGHT - lowerStart)

    if (editorMode === 'align') {
      const authorityCanvas = document.createElement('canvas')
      authorityCanvas.width = WIDTH
      authorityCanvas.height = HEIGHT
      const authorityContext = authorityCanvas.getContext('2d')
      const compositeBounds = opaqueBounds(context)
      if (authorityContext && compositeBounds) {
        authorityContext.drawImage(legs, 0, 0)
        const authorityBounds = opaqueBounds(authorityContext)
        if (authorityBounds) setDimensionAudit({ composite: compositeBounds, authority: authorityBounds })
      }
    } else {
      setDimensionAudit(null)
      context.fillStyle = '#e0ad43'
      points.forEach((point, index) => {
        context.beginPath()
        context.arc(point.x, point.y, index === selectedHemPoint ? 3.5 : 2.25, 0, Math.PI * 2)
        context.fill()
        context.strokeStyle = index === selectedHemPoint ? '#ffffff' : '#092b37'
        context.lineWidth = 1
        context.stroke()
      })
    }

    seamContext.clearRect(0, 0, seam.width, seam.height)
    seamContext.imageSmoothingEnabled = false
    seamContext.drawImage(canvas, 48, 184, 160, 72, 0, 0, 160, 72)
  }, [adjustment, editorMode, frame.torsoSrc, legsSrc, selectedHemPoint])

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

  const setHemPointRow = useCallback((index: number, row: number) => {
    setSelectedHemPoint(index)
    setEditorMode('crop')
    updateCurrent((current) => {
      const nextOffsets = [...current.hemOffsets] as HemCurve
      nextOffsets[index] = clamp(row - current.torsoCutY - current.torsoY, -16, 16)
      return { ...current, hemOffsets: nextOffsets, cropConfirmed: false, aligned: false }
    })
  }, [updateCurrent])

  const nudge = useCallback((dx: number, dy: number) => {
    if (editorMode === 'crop') {
      if (dy) updateCurrent((current) => {
        const nextOffsets = [...current.hemOffsets] as HemCurve
        nextOffsets[selectedHemPoint] = clamp(nextOffsets[selectedHemPoint] + dy, -16, 16)
        return { ...current, hemOffsets: nextOffsets, cropConfirmed: false, aligned: false }
      })
      return
    }
    updateCurrent((current) => selectedLayer === 'torso'
      ? { ...current, torsoX: current.torsoX + dx, torsoY: current.torsoY + dy, aligned: false }
      : { ...current, legsX: current.legsX + dx, legsY: current.legsY + dy, aligned: false })
  }, [editorMode, selectedHemPoint, selectedLayer, updateCurrent])

  const exportPayload = useCallback(() => ({
    schema: 'lighthouse-keeper/prime-rear-task-manual-alignment@4',
    savedAt: new Date().toISOString(),
    source: {
      torsoBatch: 'keeper-prime-morning-drafts-v6',
      legsSha256,
      layerOrder: ['approved rear legs', 'moving action torso'],
      trouserCleanStartRow: CLEAN_TROUSER_START,
      minimumTrouserUnderlap: TROUSER_UNDERLAP,
      hemControlX: HEM_CONTROL_X,
      hemOutline: { colour: '#000000', width: 2 },
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
    const hemIndex = editorMode === 'crop'
      ? HEM_CONTROL_X.reduce((closest, x, index) => Math.abs(point.x - adjustment.torsoX - x) < Math.abs(point.x - adjustment.torsoX - HEM_CONTROL_X[closest]) ? index : closest, 0)
      : undefined
    if (hemIndex !== undefined) setHemPointRow(hemIndex, point.y)
    dragRef.current = {
      kind: editorMode,
      pointerId: event.pointerId,
      startX: point.x,
      startY: point.y,
      initialX: selectedLayer === 'torso' ? adjustment.torsoX : adjustment.legsX,
      initialY: selectedLayer === 'torso' ? adjustment.torsoY : adjustment.legsY,
      hemIndex,
    }
    event.currentTarget.setPointerCapture(event.pointerId)
  }

  const onPointerMove = (event: React.PointerEvent<HTMLCanvasElement>) => {
    const drag = dragRef.current
    if (!drag || drag.pointerId !== event.pointerId) return
    const point = pointerPosition(event)
    if (drag.kind === 'crop') {
      setHemPointRow(drag.hemIndex ?? selectedHemPoint, point.y)
      return
    }
    const x = drag.initialX + Math.round(point.x - drag.startX)
    const y = drag.initialY + Math.round(point.y - drag.startY)
    updateCurrent((current) => selectedLayer === 'torso'
      ? { ...current, torsoX: x, torsoY: y, aligned: false }
      : { ...current, legsX: x, legsY: y, aligned: false })
  }

  const stopDragging = (event: React.PointerEvent<HTMLCanvasElement>) => {
    if (dragRef.current?.pointerId === event.pointerId) dragRef.current = null
  }

  const seamPointerPosition = (event: React.PointerEvent<HTMLCanvasElement>) => {
    const bounds = event.currentTarget.getBoundingClientRect()
    return {
      x: 48 + (event.clientX - bounds.left) * 160 / bounds.width,
      y: 184 + (event.clientY - bounds.top) * 72 / bounds.height,
    }
  }

  const onSeamPointerDown = (event: React.PointerEvent<HTMLCanvasElement>) => {
    if (!ready || editorMode !== 'crop') return
    const point = seamPointerPosition(event)
    const hemIndex = HEM_CONTROL_X.reduce((closest, x, index) => Math.abs(point.x - adjustment.torsoX - x) < Math.abs(point.x - adjustment.torsoX - HEM_CONTROL_X[closest]) ? index : closest, 0)
    setHemPointRow(hemIndex, point.y)
    dragRef.current = { kind: 'crop', pointerId: event.pointerId, startX: point.x, startY: point.y, initialX: 0, initialY: 0, hemIndex }
    event.currentTarget.setPointerCapture(event.pointerId)
  }

  const onSeamPointerMove = (event: React.PointerEvent<HTMLCanvasElement>) => {
    const drag = dragRef.current
    if (!drag || drag.kind !== 'crop' || drag.pointerId !== event.pointerId) return
    setHemPointRow(drag.hemIndex ?? selectedHemPoint, seamPointerPosition(event).y)
  }

  const onKeyDown = (event: React.KeyboardEvent<HTMLCanvasElement>) => {
    const step = event.shiftKey ? 8 : 1
    if (editorMode === 'crop') {
      if (event.key !== 'ArrowUp' && event.key !== 'ArrowDown') return
      event.preventDefault()
      nudge(0, event.key === 'ArrowUp' ? -step : step)
      return
    }
    const direction = event.key === 'ArrowLeft' ? [-step, 0] : event.key === 'ArrowRight' ? [step, 0] : event.key === 'ArrowUp' ? [0, -step] : event.key === 'ArrowDown' ? [0, step] : null
    if (!direction) return
    event.preventDefault()
    nudge(direction[0], direction[1])
  }

  const changeFrame = (next: number) => {
    setPlaying(false)
    setFrameIndex(clamp(next, 0, frames.length - 1))
    setEditorMode('crop')
  }

  return <main className={styles.page}>
    <header className={styles.hero}>
      <nav><a href="/prime-keeper-animation-drafts">Animation review</a><span>/</span><strong>Manual rear-task alignment</strong></nav>
      <p className={styles.eyebrow}>Exact source layers · no artwork overwritten</p>
      <h1>You place<br />the join.</h1>
      <p>This is the fallback you requested. First trace the jumper’s shallow U-shaped hem with five independently editable points. Only after you confirm the curve does the tool introduce the exact approved rear legs for alignment. Every frame saves independently in this browser.</p>
    </header>

    <section className={styles.status} aria-live="polite">
      <strong>{loadError || (ready ? 'All 22 exact source images decoded' : 'Decoding exact source images…')}</strong>
      <span>{cropped} / {frames.length} jumper crops confirmed · {completed} / {frames.length} fully aligned</span>
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
              style={{ width: WIDTH * zoom, height: HEIGHT * zoom, cursor: editorMode === 'crop' ? 'crosshair' : 'move' }}
              tabIndex={0}
              aria-label={editorMode === 'crop' ? `Frame ${frame.position} five-point jumper hem crop. Drag a control point or use up and down arrow keys.` : `Frame ${frame.position} composite. Drag selected ${selectedLayer} layer or use arrow keys.`}
              onPointerDown={onPointerDown}
              onPointerMove={onPointerMove}
              onPointerUp={stopDragging}
              onPointerCancel={stopDragging}
              onKeyDown={onKeyDown}
            />
            <i className={styles.floorGuide} style={{ top: 316 * zoom }}><span>floor 316</span></i>
          </div>
        </div>
        <div className={styles.seamBlock}>
          <span>4× editable waist inspection</span>
          <div><canvas ref={seamRef} width={160} height={72} tabIndex={0} aria-label="Editable four-times waist inspection. Drag the nearest gold hem point." onPointerDown={onSeamPointerDown} onPointerMove={onSeamPointerMove} onPointerUp={stopDragging} onPointerCancel={stopDragging} onKeyDown={onKeyDown} /></div>
        </div>
      </div>

      <aside className={styles.controls}>
        <section>
          <h3>1. Crop the jumper first</h3>
          <div className={styles.layerButtons}>
            <button className={editorMode === 'crop' ? styles.active : ''} onClick={() => setEditorMode('crop')}><span>Crop-only view</span><code>legs hidden</code></button>
            <button className={adjustment.cropConfirmed ? styles.active : ''} onClick={() => { updateCurrent({ cropConfirmed: true, aligned: false }); setEditorMode('align') }}><span>{adjustment.cropConfirmed ? '✓ Crop confirmed' : 'Confirm jumper crop'}</span><code>then show legs</code></button>
          </div>
          <label>Move the whole curve around row <output>{adjustment.torsoCutY}</output><input aria-label="Whole jumper hem row" type="range" min={190} max={226} value={adjustment.torsoCutY} onChange={(event) => { setEditorMode('crop'); updateCurrent({ torsoCutY: Number(event.target.value), cropConfirmed: false, aligned: false }) }} /></label>
          <div className={styles.hemPoints}>{HEM_POINT_NAMES.map((name, index) => <button key={name} className={selectedHemPoint === index ? styles.activeHemPoint : ''} onClick={() => { setEditorMode('crop'); setSelectedHemPoint(index) }}><span>{name}</span><code>row {adjustment.torsoCutY + adjustment.hemOffsets[index] + adjustment.torsoY}</code></button>)}</div>
          <div className={styles.nudge}><button aria-label="Move selected hem point up one pixel" onClick={() => nudge(0, -1)}>↑</button><button disabled>←</button><button aria-label="Move selected hem point down one pixel" onClick={() => nudge(0, 1)}>↓</button><button disabled>→</button></div>
          <div className={styles.curveActions}><button onClick={() => updateCurrent((current) => ({ ...current, hemOffsets: [current.hemOffsets[0], current.hemOffsets[1], current.hemOffsets[2], current.hemOffsets[1], current.hemOffsets[0]], cropConfirmed: false, aligned: false }))}>Mirror left → right</button><button onClick={() => updateCurrent((current) => ({ ...current, hemOffsets: [current.hemOffsets[4], current.hemOffsets[3], current.hemOffsets[2], current.hemOffsets[3], current.hemOffsets[4]], cropConfirmed: false, aligned: false }))}>Mirror right → left</button><button onClick={() => updateCurrent((current) => ({ ...current, hemOffsets: [...DEFAULT_HEM_OFFSETS], cropConfirmed: false, aligned: false }))}>Reset shallow U</button></div>
          <p>Only the torso is shown. Drag any gold point directly on the large view or the 4× waist inspection, then nudge the selected point by one pixel. The final black outline follows the five-point curve.</p>
        </section>

        <section>
          <h3>2. Align the retained torso and legs</h3>
          <div className={styles.layerButtons}>
            <button disabled={!adjustment.cropConfirmed} className={editorMode === 'align' && selectedLayer === 'torso' ? styles.active : ''} onClick={() => { setEditorMode('align'); setSelectedLayer('torso') }}><span>Retained torso</span><code>x {adjustment.torsoX} · y {adjustment.torsoY}</code></button>
            <button disabled={!adjustment.cropConfirmed} className={editorMode === 'align' && selectedLayer === 'legs' ? styles.active : ''} onClick={() => { setEditorMode('align'); setSelectedLayer('legs') }}><span>Approved legs</span><code>x {adjustment.legsX} · y {adjustment.legsY}</code></button>
          </div>
          <p>{adjustment.cropConfirmed ? 'The cropped jumper is now composited over the legs. Drag the selected layer or use arrow keys; Shift + arrow moves eight pixels.' : 'Confirm the jumper crop above to reveal and align the legs.'}</p>
        </section>

        <section>
          <h3>3. Nudge the selected layer</h3>
          <div className={styles.nudge}>
            <button disabled={!adjustment.cropConfirmed || editorMode !== 'align'} onClick={() => nudge(0, -1)}>↑</button>
            <button disabled={!adjustment.cropConfirmed || editorMode !== 'align'} onClick={() => nudge(-1, 0)}>←</button>
            <button disabled={!adjustment.cropConfirmed || editorMode !== 'align'} onClick={() => nudge(0, 1)}>↓</button>
            <button disabled={!adjustment.cropConfirmed || editorMode !== 'align'} onClick={() => nudge(1, 0)}>→</button>
          </div>
        </section>

        <section>
          <h3>4. Refine the legs boundary</h3>
          <label>Clean trousers begin from source row <output>{adjustment.legsCropY}</output><input aria-label="Clean trousers source row" type="range" min={CLEAN_TROUSER_START} max={230} value={adjustment.legsCropY} onChange={(event) => updateCurrent({ legsCropY: Number(event.target.value), aligned: false })} /></label>
          <p>The approved trousers are the lower, behind layer. They keep at least {TROUSER_UNDERLAP} hidden pixels beneath the cropped jumper, so lateral torso movement cannot open a transparent tear. The authority's rows 214–218, which contain its top seam, remain excluded.</p>
        </section>

        <section>
          <h3>5. Check against the Prime Keeper</h3>
          {dimensionAudit ? <div className={styles.dimensionAudit}>
            <span>Opaque height<strong className={dimensionAudit.composite.height === dimensionAudit.authority.height ? styles.match : styles.mismatch}>{dimensionAudit.composite.height} / {dimensionAudit.authority.height} px</strong></span>
            <span>Overall width<strong className={dimensionAudit.composite.width === dimensionAudit.authority.width ? styles.match : styles.mismatch}>{dimensionAudit.composite.width} / {dimensionAudit.authority.width} px</strong></span>
            <span>Floor row<strong className={dimensionAudit.composite.y1 === dimensionAudit.authority.y1 ? styles.match : styles.mismatch}>{dimensionAudit.composite.y1} / {dimensionAudit.authority.y1}</strong></span>
            <span>Centre x<strong className={dimensionAudit.composite.centreX === dimensionAudit.authority.centreX ? styles.match : styles.mismatch}>{dimensionAudit.composite.centreX} / {dimensionAudit.authority.centreX}</strong></span>
          </div> : <p>Confirm the curved jumper crop to reveal the trousers and measure this composite against the approved Prime back authority.</p>}
          {dimensionAudit && (dimensionAudit.composite.height !== dimensionAudit.authority.height || dimensionAudit.composite.width !== dimensionAudit.authority.width || dimensionAudit.composite.y1 !== dimensionAudit.authority.y1) ? <p className={styles.auditWarning}>Dimension mismatch: do not mark this frame aligned until the discrepancy is deliberate and approved.</p> : null}
        </section>

        <section className={styles.frameActions}>
          <h3>6. Save this frame</h3>
          <button disabled={!adjustment.cropConfirmed} className={adjustment.aligned ? styles.approved : ''} onClick={() => updateCurrent({ aligned: !adjustment.aligned })}>{adjustment.aligned ? '✓ Marked aligned' : adjustment.cropConfirmed ? 'Mark frame aligned' : 'Confirm jumper crop first'}</button>
          <button onClick={() => { updateCurrent(defaultAdjustment(frame)); setEditorMode('crop') }}>Reset this frame</button>
          <button onClick={() => setAdjustments((current) => Object.fromEntries(frames.map((item) => [item.position, { ...(current[item.position] ?? defaultAdjustment(item)), torsoY: adjustment.torsoY, torsoCutY: adjustment.torsoCutY, hemOffsets: [...adjustment.hemOffsets] as HemCurve, legsY: adjustment.legsY, legsCropY: adjustment.legsCropY, cropConfirmed: false, aligned: false }]))) }>Copy curve and vertical setup to all</button>
          <button disabled={editorMode !== 'align'} onClick={downloadFrame}>Download current 256×320 PNG</button>
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
      <div className={styles.frameRail}>{frames.map((item, index) => <button key={item.position} className={`${index === frameIndex ? styles.current : ''} ${adjustments[item.position]?.aligned ? styles.done : ''}`} onClick={() => changeFrame(index)}><span>{item.position}</span><small>{adjustments[item.position]?.aligned ? '✓' : adjustments[item.position]?.cropConfirmed ? 'C' : ''}</small></button>)}</div>
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
