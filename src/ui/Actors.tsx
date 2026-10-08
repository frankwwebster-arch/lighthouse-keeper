import { useEffect, useRef, useState } from 'react'
import { VISITORS, objectById, type FloorId, type ObjectId, type PetKind } from '../game/config'
import { insideVisit, moodOf, moodWord, waitingVisit, type Happening, type State } from '../game/engine'
import { FLOOR_ORDER, FLOOR_Y, INTERIOR, LAYOUT, TOWER_X, floorOf, route, worldX, type Point } from '../game/world'
import { Sprite } from './Sprite'

const SPEED = 240
const interiorLeft = TOWER_X + INTERIOR.left
const interiorRight = TOWER_X + INTERIOR.right

/** Which floor a spot is on (ground and outside share a height, so the x tells them apart). */
export function floorAt(x: number, y: number): FloorId {
  let best: FloorId = 'ground'
  let d = Infinity
  for (const f of FLOOR_ORDER) {
    const dd = Math.abs(FLOOR_Y[f] - y)
    if (dd < d - 1e-6) {
      d = dd
      best = f
    }
  }
  if (best === 'ground' || best === 'outside') return x >= interiorLeft - 10 && x <= interiorRight + 10 ? 'ground' : 'outside'
  return best
}

const place = (id: ObjectId): { x: number; y: number } => ({ x: worldX(id), y: FLOOR_Y[floorOf(id)] })

/** Where the camera should look (null = the whole lighthouse). Used by the scene. */
export interface Pose {
  x: number
  y: number
}

interface Props {
  s: State
  onArrive: () => void
  shrugAt: number
  petJump: number
  onPose: (p: Pose) => void
}

const SKIN = '#f1c9a0'

function Keeper({ anim, mood, walking, face, rear, action }: { anim: string; mood: ReturnType<typeof moodWord>; walking: boolean; face: 1 | -1; rear: boolean; action?: string }) {
  const clip = walking ? 'walk' : anim === 'none' ? 'idle' : anim
  const productionClip = rear ? action === 'brush_teeth' ? 'brush_teeth_back' : action === 'wash_basin' ? 'wash_back' : 'cook_back' : clip
  const mouth = mood === 'chipper' ? 'M-6 -76 Q0 -68 6 -76' : mood === 'content' ? 'M-5 -75 Q0 -71 5 -75' : mood === 'soso' ? 'M-5 -74 L5 -74' : 'M-6 -72 Q0 -78 6 -72'
  return (
    <g className={`keeper a-${clip} ${rear ? 'keeper-rear' : ''}`}>
      <Sprite name={[`keeper_clip_${clip}_${rear ? 'rear' : 'side'}`, `keeper_${productionClip}`, `keeper_${clip}`]} w={90} h={130}>
        <g transform={`scale(${face} 1)`}>
          <g className="legs">
            <rect className="leg l1" x={-9} y={-30} width={8} height={30} fill="#2e3d5a" />
            <rect className="leg l2" x={1} y={-30} width={8} height={30} fill="#2e3d5a" />
          </g>
          <g className="torso">
            <rect x={-15} y={-64} width={30} height={38} rx={8} fill="#2c5f9e" stroke="#1c3d68" strokeWidth={2} />
            <rect x={-15} y={-48} width={30} height={5} fill="#fff" opacity={0.7} />
            <rect className="arm a1" x={-22} y={-62} width={8} height={26} rx={4} fill="#2c5f9e" />
            <rect className="arm a2" x={14} y={-62} width={8} height={26} rx={4} fill="#2c5f9e" />
            <g className="head">
              <circle cx={0} cy={-80} r={15} fill={SKIN} stroke="#c49266" strokeWidth={1.5} />
              {rear ? <path d="M-14 -82 Q0 -68 14 -82 L12 -64 Q0 -56 -12 -64 Z" fill="#f2f2f2" /> : <path d="M-14 -74 Q0 -52 14 -74 Q10 -60 0 -58 Q-10 -60 -14 -74 Z" fill="#f2f2f2" />}
              <path d="M-17 -88 Q0 -108 17 -88 L17 -92 Q0 -104 -17 -92 Z" fill="#1d2f4d" />
              <rect x={-18} y={-92} width={36} height={6} rx={3} fill="#1d2f4d" />
              {!rear && <><circle cx={-5} cy={-82} r={1.8} fill="#222" /><circle cx={5} cy={-82} r={1.8} fill="#222" /><path d={mouth} fill="none" stroke="#7a3b2a" strokeWidth={1.8} strokeLinecap="round" /></>}
            </g>
          </g>
        </g>
      </Sprite>
    </g>
  )
}

function Pet({ kind, jump, scared }: { kind: PetKind; jump: boolean; scared: boolean }) {
  return (
    <g className={`pet ${jump ? 'hop' : ''} ${scared ? 'scared' : ''}`}>
      <Sprite name={`pet_${kind}`} w={64} h={52}>
        {kind === 'cat' ? (
          <>
            <path className="tail" d="M-18 -14 Q-34 -26 -26 -40" stroke="#d9873b" strokeWidth={6} fill="none" strokeLinecap="round" />
            <ellipse cx={0} cy={-14} rx={20} ry={13} fill="#e8963f" />
            <circle cx={16} cy={-26} r={11} fill="#e8963f" />
            <path d="M8 -34 L10 -46 L17 -36 Z M20 -36 L26 -46 L28 -32 Z" fill="#e8963f" />
            <circle cx={20} cy={-28} r={1.6} fill="#222" />
            <circle cx={13} cy={-28} r={1.6} fill="#222" />
            <rect x={-12} y={-6} width={6} height={6} rx={3} fill="#c97a2f" />
            <rect x={8} y={-6} width={6} height={6} rx={3} fill="#c97a2f" />
          </>
        ) : (
          <>
            <ellipse cx={0} cy={-20} rx={20} ry={13} fill="#f4f6f8" stroke="#c4cdd4" strokeWidth={1.5} />
            <path d="M-20 -22 L-34 -18 L-20 -14 Z" fill="#cfd6dc" />
            <circle cx={16} cy={-34} r={9} fill="#f4f6f8" stroke="#c4cdd4" strokeWidth={1.5} />
            <path d="M23 -35 L36 -32 L23 -29 Z" fill="#f2b632" />
            <circle cx={18} cy={-36} r={1.6} fill="#222" />
            <rect x={-6} y={-8} width={2.5} height={9} fill="#f2b632" />
            <rect x={4} y={-8} width={2.5} height={9} fill="#f2b632" />
            <path d="M-12 -26 Q0 -34 10 -24" fill="#a9b6c0" opacity={0.7} />
          </>
        )}
      </Sprite>
    </g>
  )
}

const COLOURS: Record<string, { coat: string; hat: string }> = {
  fisherman: { coat: '#d6a21e', hat: '#d6a21e' },
  postman: { coat: '#c9433b', hat: '#c9433b' },
  tourist: { coat: '#3aa27f', hat: '#f0e3a0' },
  sam: { coat: '#2d6fb5', hat: '#f4f4f4' },
  nell: { coat: '#a94a9d', hat: '#e8503a' },
}

function Visitor({ who, label }: { who: string; label: string }) {
  const c = COLOURS[who] ?? { coat: '#777', hat: '#444' }
  return (
    <g className="visitor">
      <Sprite name={`visitor_${who}`} w={80} h={120}>
        <rect x={-8} y={-26} width={7} height={26} fill="#333" />
        <rect x={2} y={-26} width={7} height={26} fill="#333" />
        <rect x={-14} y={-58} width={28} height={36} rx={8} fill={c.coat} />
        <circle cx={0} cy={-72} r={13} fill={SKIN} />
        <rect x={-15} y={-86} width={30} height={9} rx={4} fill={c.hat} />
        <circle cx={-4} cy={-73} r={1.6} fill="#222" />
        <circle cx={4} cy={-73} r={1.6} fill="#222" />
        <path d="M-4 -67 Q0 -64 4 -67" stroke="#7a3b2a" strokeWidth={1.5} fill="none" />
      </Sprite>
      <text y={-96} textAnchor="middle" fontSize={13} fontWeight={700} fill="#fff" stroke="#000" strokeWidth={3} paintOrder="stroke">
        {label}
      </text>
    </g>
  )
}

/** The keeper, the pet and any visitors. Their walking is done here, a frame at a time. */
export function Actors({ s, onArrive, shrugAt, petJump, onPose }: Props) {
  const startAt = place('bed')
  const [pos, setPos] = useState({ x: startAt.x, y: startAt.y, face: 1 as 1 | -1, walking: false })
  const [pet, setPet] = useState({ x: startAt.x + 60, y: startAt.y })
  const path = useRef<{ x: number; y: number }[]>([])
  const walked = useRef(-1)
  const arrived = useRef(-1)
  const me = useRef({ x: startAt.x, y: startAt.y })
  const petMe = useRef({ x: startAt.x + 60, y: startAt.y })
  /** The layout as last drawn, and which floor each of them was on in it. */
  const seen = useRef({ version: LAYOUT.version, keeper: floorOf('bed') as FloorId, pet: floorOf('bed') as FloorId })
  const sRef = useRef(s)
  sRef.current = s
  const arriveRef = useRef(onArrive)
  arriveRef.current = onArrive
  const poseRef = useRef(onPose)
  poseRef.current = onPose
  const [now, setNow] = useState(0)

  // A new job: work out the walk.
  const d = s.doing
  useEffect(() => {
    if (!d || d.phase !== 'going' || walked.current === d.n) return
    walked.current = d.n
    const target = place(d.object)
    const from: Point = { x: me.current.x, floor: floorAt(me.current.x, me.current.y) }
    const to: Point = { x: target.x, floor: floorOf(d.object) }
    path.current = d.object === 'here' ? [] : route(from, to).map((p) => ({ x: p.x, y: FLOOR_Y[p.floor] }))
  }, [d])

  // The engine can end a walk early (it gives up waiting): snap to the job.
  useEffect(() => {
    if (d && d.phase === 'doing' && d.object !== 'here') {
      const t = place(d.object)
      if (Math.abs(t.x - me.current.x) > 2 || Math.abs(t.y - me.current.y) > 2) {
        me.current = { ...t }
        path.current = []
        setPos((p) => ({ ...p, x: t.x, y: t.y, walking: false }))
      }
    }
  }, [d?.n, d?.phase]) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    let raf = 0
    let last = performance.now()
    const frame = (t: number) => {
      const dt = Math.min(0.06, (t - last) / 1000)
      last = t
      const st = sRef.current
      // A floor arrived and the tower moved: keep him (and the pet) on their own floors, and re-plan any walk.
      if (seen.current.version !== LAYOUT.version) {
        const kf = seen.current.keeper
        const pf0 = seen.current.pet
        if (kf !== 'outside' && kf !== 'ground') me.current = { ...me.current, y: FLOOR_Y[kf] }
        if (pf0 !== 'outside' && pf0 !== 'ground') petMe.current.y = FLOOR_Y[pf0]
        const job = st.doing
        if (path.current.length && job && job.object !== 'here') {
          const target = place(job.object)
          path.current = route({ x: me.current.x, floor: kf }, { x: target.x, floor: floorOf(job.object) }).map((p) => ({ x: p.x, y: FLOOR_Y[p.floor] }))
        }
      }
      let walking = false
      let face = 0 as 0 | 1 | -1
      const next = path.current[0]
      if (next && st.doing?.phase === 'going') {
        walking = true
        const dx = next.x - me.current.x
        const dy = next.y - me.current.y
        const dist = Math.hypot(dx, dy)
        const step = SPEED * dt * (dy !== 0 ? (LAYOUT.lift ? 2.4 : 0.6) : 1)
        if (dist <= step) {
          me.current = { x: next.x, y: next.y }
          path.current.shift()
        } else {
          me.current = { x: me.current.x + (dx / dist) * step, y: me.current.y + (dy / dist) * step }
        }
        if (Math.abs(dx) > 1) face = dx > 0 ? 1 : -1
      } else if (st.doing?.phase === 'going' && arrived.current !== st.doing.n) {
        arrived.current = st.doing.n
        arriveRef.current()
      }
      // The pet tags along on the keeper's floor, keeping a little way off.
      const k = me.current
      const pf = petMe.current
      const bowl = st.doing?.object === 'petbowl' && st.doing.phase === 'doing' ? worldX('petbowl') + 30 : null
      const wander = Math.sin(t / 2300) * 50
      const goalX = bowl ?? Math.min(interiorRight - 10, Math.max(interiorLeft + 10, k.x + 70 + wander))
      const sameFloor = Math.abs(pf.y - k.y) < 4
      if (!sameFloor) {
        // follows after a moment: up the stairs.
        const stairsX = TOWER_X + 108
        if (Math.abs(pf.x - stairsX) > 6) pf.x += Math.sign(stairsX - pf.x) * 150 * dt
        else pf.y += Math.sign(k.y - pf.y) * 140 * dt
        if (Math.abs(pf.y - k.y) < 3) pf.y = k.y
      } else {
        const outsideNow = floorAt(k.x, k.y) === 'outside'
        const gx = outsideNow ? k.x + 70 + wander : goalX
        pf.x += Math.max(-90 * dt, Math.min(90 * dt, gx - pf.x))
      }
      setPos((p) => (p.x === k.x && p.y === k.y && p.walking === walking && (face === 0 || p.face === face) ? p : { x: k.x, y: k.y, walking, face: face === 0 ? p.face : face }))
      setPet({ x: pf.x, y: pf.y })
      setNow(t)
      poseRef.current({ x: k.x, y: k.y })
      seen.current = { version: LAYOUT.version, keeper: floorAt(k.x, k.y), pet: floorAt(pf.x, pf.y) }
      raf = requestAnimationFrame(frame)
    }
    raf = requestAnimationFrame(frame)
    return () => cancelAnimationFrame(raf)
  }, [])

  const anim = (() => {
    if (now < shrugAt) return 'shrug'
    if (d && d.phase === 'doing') return d.anim
    if (d && d.phase === 'going') return 'none'
    return s.annoyedLevel >= 2 ? 'shake' : 'none'
  })()
  const hidden = !!(d && d.priv && d.phase === 'doing')
  const asleep = d?.anim === 'sleep' && d.phase === 'doing'
  const rearWork = !!(d && d.phase === 'doing' && (d.object === 'cooker' || d.object === 'basin'))
  const wv = waitingVisit(s)
  const iv = insideVisit(s)
  const mood = moodWord(moodOf(s))
  const scared = !!s.plan.storm && s.pet.fright > 30

  const floor = floorAt(pos.x, pos.y)
  const vx = Math.min(interiorRight - 20, Math.max(interiorLeft + 20, pos.x + 80))

  return (
    <g>
      {wv && (
        <g transform={`translate(${TOWER_X - 22} ${FLOOR_Y.outside})`}>
          <Visitor who={wv.who} label={VISITORS.find((v) => v.id === wv.who)?.name ?? ''} />
        </g>
      )}
      {iv && (
        <g transform={`translate(${floor === 'outside' ? pos.x + 80 : vx} ${pos.y})`}>
          <Visitor who={iv.who} label={VISITORS.find((v) => v.id === iv.who)?.name ?? ''} />
        </g>
      )}
      <g transform={`translate(${pet.x} ${pet.y})`}>
        <Pet kind={s.petKind} jump={now < petJump} scared={scared} />
      </g>
      {!hidden && (
        <g transform={`translate(${pos.x} ${asleep ? pos.y - 26 : pos.y})`}>
          <g className={asleep ? 'lying' : undefined}>
            <Keeper anim={anim} mood={mood} walking={pos.walking} face={pos.face} rear={rearWork} action={d?.id} />
          </g>
        </g>
      )}
    </g>
  )
}

export const objectLabel = (id: ObjectId) => objectById(id)?.label ?? id
export type { Happening }
