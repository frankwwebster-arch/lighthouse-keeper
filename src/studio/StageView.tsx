import { useRef } from 'react'
import { DOOR, DOORWAY, STAGE, isFront, isSolid, placeX, type Recipe, type Shot, type StageObject } from './recipe'

/** A sprite entry as the manifest gives it (only what the stage needs). */
export interface SheetEntry {
  file: string
  w: number
  h: number
  frames?: number
  anchor?: [number, number]
}

export type Sel = { type: 'recipe' } | { type: 'step'; id: string } | { type: 'cue'; stepId: string; cueId: string } | { type: 'object'; id: string }

const VIEW = { left: -STAGE.stairW - 4, top: -STAGE.roomH - 10, right: STAGE.roomW + 22 }

/** One frame of a strip, its anchor on (x, floor − y), flipped about its anchor when mirrored. Whole pixels only. */
export function Frame({ e, frame, x, y, mirror, opacity = 1 }: { e: SheetEntry; frame: number; x: number; y: number; mirror: boolean; opacity?: number }) {
  const frames = e.frames ?? 1
  const [ax, ay] = e.anchor ?? [Math.round(e.w / 2), e.h]
  const pic = (
    <svg x={x - ax} y={-y - ay} width={e.w} height={e.h} viewBox={`${Math.min(frame, frames - 1) * e.w} 0 ${e.w} ${e.h}`} overflow="hidden" opacity={opacity}>
      <image href={`/sprites/${e.file}`} width={e.w * frames} height={e.h} preserveAspectRatio="none" style={{ imageRendering: 'pixelated' }} />
    </svg>
  )
  return mirror ? <g transform={`translate(${2 * x} 0) scale(-1 1)`}>{pic}</g> : pic
}

function Door({ at, open, side }: { at: number; open: boolean; side: 'left' | 'right' }) {
  // The jamb is on the stairway (outer) side; the leaf opens into the room, towards the camera.
  const s = side === 'left' ? 1 : -1
  const leafX = side === 'left' ? at : at - DOOR.leaf
  return (
    <g className="st-door">
      <rect className="st-jamb" x={side === 'left' ? at - DOOR.jamb : at} y={-STAGE.roomH} width={DOOR.jamb} height={STAGE.roomH} />
      {open ? <rect className="st-leaf open" x={leafX} y={-DOOR.height} width={DOOR.leaf} height={DOOR.height} /> : <rect className="st-leaf" x={at - (s > 0 ? 1 : 0)} y={-DOOR.height} width={1} height={DOOR.height} />}
      <rect className="st-lintel" x={Math.min(at, leafX) - DOOR.jamb} y={-DOOR.height - 2} width={DOOR.leaf + DOOR.jamb} height={2} />
    </g>
  )
}

function ObjectView({ o, sheet, selected, onPointerDown }: { o: StageObject; sheet?: SheetEntry; selected: boolean; onPointerDown: (e: React.PointerEvent) => void }) {
  const front = isFront(o)
  return (
    <g className={`st-obj ${front ? 'front' : 'back'} ${isSolid(o) ? 'solid' : ''} ${selected ? 'sel' : ''}`} onPointerDown={onPointerDown}>
      {sheet ? <Frame e={sheet} frame={0} x={Math.round(o.x)} y={0} mirror={false} /> : <rect className="st-box" x={o.x - o.w / 2} y={-o.h} width={o.w} height={o.h} />}
      <rect className="st-hit" x={o.x - o.w / 2} y={-o.h} width={o.w} height={o.h} />
      {(o.marks ?? []).map((m) => (
        <g key={m.label}>
          <line className="st-mark" x1={o.x - o.w / 2 - 2} x2={o.x + o.w / 2 + 2} y1={-m.y} y2={-m.y} />
          <text className="st-marktext" x={o.x + o.w / 2 + 3} y={-m.y + 1}>{m.label} {m.y}</text>
        </g>
      ))}
      <text className="st-label" x={o.x} y={-o.h - 2} textAnchor="middle">{o.label}{front ? ' · in front' : isSolid(o) ? ' · solid' : ''}</text>
    </g>
  )
}

/**
 * The room at its real proportions: stairway on the left, the room, its doors,
 * the objects and the keeper. Objects and the action point can be dragged;
 * everything snaps to whole logical pixels.
 */
export function StageView({ doc, shot, zoom, sel, sheet, onSelect, onObjectX, onActionDx, editable }: {
  doc: Recipe
  shot: Shot
  zoom: number
  sel: Sel | null
  sheet: (name: string) => SheetEntry | undefined
  onSelect: (s: Sel) => void
  onObjectX: (id: string, x: number) => void
  onActionDx: (dx: number) => void
  editable: boolean
}) {
  const svg = useRef<SVGSVGElement>(null)
  const right = doc.room.inner ? VIEW.right : STAGE.roomW + 8
  const W = right - VIEW.left
  const H = -VIEW.top + 8
  const toX = (clientX: number) => {
    const m = svg.current?.getScreenCTM()
    return m ? (clientX - m.e) / m.a : 0
  }
  const drag = (e: React.PointerEvent, start: number, apply: (v: number) => void) => {
    if (!editable) return
    e.stopPropagation()
    const target = e.currentTarget as Element
    target.setPointerCapture(e.pointerId)
    const grab = toX(e.clientX) - start
    const move = (ev: PointerEvent) => apply(Math.round(toX(ev.clientX) - grab))
    const up = () => {
      target.removeEventListener('pointermove', move as EventListener)
      target.removeEventListener('pointerup', up)
    }
    target.addEventListener('pointermove', move as EventListener)
    target.addEventListener('pointerup', up)
  }
  const back = doc.objects.filter((o) => !isFront(o))
  const front = doc.objects.filter(isFront)
  const keeper = shot.clip ? sheet(shot.clip) : undefined
  const ax = placeX(doc, 'action')
  const objSheet = (o: StageObject) => (o.sprite ? sheet(o.sprite) ?? sheet(`obj_${o.sprite}_standard`) : undefined)
  const actionObj = doc.objects.find((o) => o.id === doc.action.object)

  return (
    <svg ref={svg} className="st-stage" viewBox={`${VIEW.left} ${VIEW.top} ${W} ${H}`} width={W * zoom} height={H * zoom} shapeRendering="crispEdges" onPointerDown={() => onSelect({ type: 'recipe' })}>
      <rect className="st-stair" x={-STAGE.stairW} y={-STAGE.roomH} width={STAGE.stairW} height={STAGE.roomH} />
      <text className="st-roomname" x={-STAGE.stairW + 2} y={-STAGE.roomH + 5}>Stairway</text>
      <g className="st-ladder">
        <line x1={STAGE.ladderX - 5} x2={STAGE.ladderX - 5} y1={-STAGE.roomH} y2={0} />
        <line x1={STAGE.ladderX + 5} x2={STAGE.ladderX + 5} y1={-STAGE.roomH} y2={0} />
        {Array.from({ length: 9 }, (_, i) => <line key={i} x1={STAGE.ladderX - 5} x2={STAGE.ladderX + 5} y1={-4 - i * 6} y2={-4 - i * 6} />)}
      </g>
      <rect className="st-room" x={0} y={-STAGE.roomH} width={STAGE.roomW} height={STAGE.roomH} />
      <text className="st-roomname" x={DOOR.leaf + 2} y={-STAGE.roomH + 5}>{doc.room.name}</text>
      {doc.room.inner && <rect className="st-stair" x={STAGE.roomW} y={-STAGE.roomH} width={VIEW.right - STAGE.roomW - 2} height={STAGE.roomH} />}
      <line className="st-floor" x1={VIEW.left} x2={right} y1={0.5} y2={0.5} />
      {back.map((o) => <ObjectView key={o.id} o={o} sheet={objSheet(o)} selected={sel?.type === 'object' && sel.id === o.id} onPointerDown={(e) => { onSelect({ type: 'object', id: o.id }); drag(e, o.x, (x) => onObjectX(o.id, x)) }} />)}

      {/* The action point: where his feet go, and which way he faces. */}
      {actionObj && (
        <g className="st-action" onPointerDown={(e) => { onSelect({ type: 'recipe' }); drag(e, ax, (x) => onActionDx(x - Math.round(actionObj.x))) }}>
          <path d={`M${ax} -1 l3 3 l-3 3 l-3 -3 z`} />
          <path d={doc.action.facing === 'right' ? `M${ax + 3} 4.5 h5 l-2 -2 m2 2 l-2 2` : `M${ax - 3} 4.5 h-5 l2 -2 m-2 2 l2 2`} className="st-arrow" />
        </g>
      )}

      {shot.visible && keeper && <Frame e={keeper} frame={shot.frame} x={shot.x} y={shot.y} mirror={shot.mirror} />}

      {front.map((o) => <ObjectView key={o.id} o={o} sheet={objSheet(o)} selected={sel?.type === 'object' && sel.id === o.id} onPointerDown={(e) => { onSelect({ type: 'object', id: o.id }); drag(e, o.x, (x) => onObjectX(o.id, x)) }} />)}
      <Door at={DOORWAY.door} open={shot.door} side="left" />
      {doc.room.inner && <Door at={DOORWAY.inner} open={shot.inner} side="right" />}
      {!shot.visible && <text className="st-hidden" x={shot.x} y={-20} textAnchor="middle">hidden{shot.segment?.label ? ` · ${shot.segment.label}` : ''}</text>}
    </svg>
  )
}
