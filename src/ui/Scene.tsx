import { useEffect, useMemo, useRef, useState } from 'react'
import { BREAKABLE_OBJECTS, OBJECTS, maxTier, type FxKey, type ObjectId } from '../game/config'
import { darkness, stormNow, tierOf, type State } from '../game/engine'
import { ALL_ROOM_FLOORS, UNDERGROUND } from '../game/config'
import { objectAvailable, towerOf } from '../game/missions'
import { FLOOR_Y, LAYOUT, STAGE, STAIRS_X, TOWER_X, applyLayout, floorOf, focusFor, worldX } from '../game/world'
import { Actors, type Pose } from './Actors'
import { ObjectArt } from './art'
import { FloorModule, floorsOnShow } from './floors'
import { parseBrokenPreview, parseTierPreview, visualStateFor } from './objectState'

const FX: Record<FxKey, string> = { steam: '💨', bubbles: '🫧', sparkles: '✨', dust: '🌫️', scribbles: '✏️', music: '🎵', zzz: '💤', tv: '📺', hearts: '💗', stench: '🤢', burp: '💨', splash: '💦', coins: '🪙', ring: '🔔', stars: '⭐' }

const W = STAGE.w
const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v))

interface Props {
  s: State
  selected: ObjectId | null
  flash: number
  shrugAt: number
  petJump: number
  onObject: (id: ObjectId) => void
  onArrive: () => void
  onPose: (p: Pose) => void
}

function Rain() {
  const drops = useMemo(() => Array.from({ length: 46 }, (_, i) => ({ x: (i * 97) % W, d: (i % 7) * 0.12, s: 0.5 + (i % 5) * 0.08 })), [])
  return (
    <g className="rain" pointerEvents="none">
      {drops.map((r, i) => (
        <line key={i} x1={r.x} y1={0} x2={r.x - 14} y2={34} stroke="#cfe6ff" strokeWidth={2} opacity={0.6} style={{ animationDelay: `${r.d}s`, animationDuration: `${r.s}s` }} />
      ))}
    </g>
  )
}

/** `?floors=all` in the address shows every floor (and the lift) as if unlocked, for checking art. */
const previewAllFloors = () => typeof window !== 'undefined' && new URLSearchParams(window.location.search).get('floors') === 'all'

export function Scene({ s, selected, flash, shrugAt, petJump, onObject, onArrive, onPose }: Props) {
  // The tower is whatever floors he has unlocked: stack them before anything is drawn.
  const allFloors = useMemo(previewAllFloors, [])
  if (allFloors) applyLayout(ALL_ROOM_FLOORS.filter((f) => !UNDERGROUND.includes(f)), UNDERGROUND, true)
  else {
    const tower = towerOf(s)
    applyLayout(tower.stack, tower.below, s.unlocked.includes('lift'))
  }
  const top = LAYOUT.top
  const H = LAYOUT.bottom - LAYOUT.top
  const has = (id: ObjectId) => allFloors || objectAvailable(s, id)
  const svgRef = useRef<SVGSVGElement>(null)
  const [aspect, setAspect] = useState(W / STAGE.h)
  useEffect(() => {
    const el = svgRef.current
    if (!el || typeof ResizeObserver === 'undefined') return
    const ro = new ResizeObserver(() => el.clientHeight > 0 && setAspect(el.clientWidth / el.clientHeight))
    ro.observe(el)
    return () => ro.disconnect()
  }, [])
  const dark = darkness(s.clock)
  const storm = stormNow(s)
  const d = s.doing
  const doingNow = d && d.phase === 'doing' && d.object !== 'here' ? d : null
  const focus = doingNow ? focusFor(doingNow.object) : null
  const z = focus ? focus.zoom : 1
  const bottom = top + H
  // The first-day tower keeps its usual framing. A taller one zooms out until it all fits,
  // widening the view to the screen's shape so there are no bars at the sides.
  const tall = H > STAGE.h
  const vw = tall ? Math.max(W, H * aspect) : W
  const left = (W - vw) / 2
  const right = left + vw
  const tx = focus ? clamp(left + vw / 2 - focus.x * z, right - right * z, left - left * z) : 0
  const ty = focus ? clamp(top + H / 2 - focus.y * z, bottom - bottom * z, top - top * z) : 0
  const sunT = clamp((s.clock - 6 * 60) / (19 * 60 - 6 * 60), 0, 1)
  const sunX = 80 + sunT * 1040
  const sunY = 320 - Math.sin(sunT * Math.PI) * 250
  const ship = s.plan.ship
  const shipT = (s.clock - (ship.at - 70)) / 140
  const shipX = 1260 - shipT * 640
  const tvOn = d?.id.startsWith('tv') && d.phase === 'doing'
  const cabin = doingNow && doingNow.priv
  const previewBroken = useMemo(
    () => parseBrokenPreview(typeof window === 'undefined' ? null : new URLSearchParams(window.location.search).get('broken'), BREAKABLE_OBJECTS),
    [],
  )
  const broken = new Set([...s.broken, ...previewBroken])
  const previewTiers = useMemo(
    () => parseTierPreview(typeof window === 'undefined' ? null : new URLSearchParams(window.location.search).get('tiers'), maxTier, OBJECTS.map((o) => o.id)),
    [],
  )
  const activeObject = doingNow?.object && doingNow.object !== 'here' ? doingNow.object : s.lampLit ? 'lamp' : s.ringing ? 'phone' : null

  const obj = (id: ObjectId, x?: number) => {
    const def = OBJECTS.find((o) => o.id === id)!
    const wx = x ?? worldX(id)
    const state = visualStateFor(id, id === 'tv' && tvOn ? 'tv' : activeObject, broken)
    return <ObjectArt key={id} id={id} x={wx} y={FLOOR_Y[def.floor]} state={state} tier={previewTiers[id] ?? tierOf(s, id)} extra={{ ringing: !!s.ringing, ready: s.garden.ready }} />
  }

  return (
    <svg className="scene" ref={svgRef} viewBox={`${left} ${top} ${vw} ${H}`} preserveAspectRatio={tall ? 'xMidYMid meet' : 'xMidYMid slice'} role="img" aria-label="The lighthouse">
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#5db6ea" />
          <stop offset="1" stopColor="#bfe7f7" />
        </linearGradient>
        <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#2f89c6" />
          <stop offset="1" stopColor="#14507f" />
        </linearGradient>
      </defs>
      <g className="camera" style={{ transform: `translate(${tx}px, ${ty}px) scale(${z})`, transformOrigin: '0 0' }}>
        <rect x={left - 300} y={top - 200} width={vw + 600} height={H + 400} fill="url(#sky)" />
        {/* sun and moon */}
        <circle cx={sunX} cy={sunY} r={46} fill="#ffe27a" opacity={1 - dark} />
        <circle cx={1060} cy={130} r={30} fill="#f4f2dc" opacity={dark} />
        {dark > 0.2 && Array.from({ length: 30 }, (_, i) => <circle key={i} cx={(i * 173) % W} cy={(i * 59) % 330} r={1.6 + (i % 3) * 0.6} fill="#fff" opacity={dark * 0.9} />)}
        {/* clouds */}
        <g opacity={0.9 - dark * 0.4} className="clouds">
          <ellipse cx={420} cy={90} rx={70} ry={20} fill="#fff" />
          <ellipse cx={900} cy={160} rx={90} ry={22} fill="#fff" />
        </g>
        {/* sea, land */}
        <rect x={700} y={560} width={right - 700 + 300} height={bottom - 560 + 200} fill="url(#sea)" />
        <g className="waves" opacity={0.6}>
          {[0, 1, 2, 3].map((i) => <path key={i} d={`M${720 + i * 120} ${600 + (i % 2) * 40} q20 -10 40 0 t40 0`} stroke="#d6f0ff" strokeWidth={3} fill="none" />)}
        </g>
        <path d={`M${left - 300} 640 L760 640 L720 560 L${left - 300} 560 Z`} fill="#6aa84f" />
        <rect x={left - 300} y={640} width={760 - left + 300} height={bottom - 640 + 200} fill="#5b9441" />
        <path d="M660 640 Q720 600 780 640 L800 760 L640 760 Z" fill="#8a8f93" />
        {/* the ship */}
        {shipT > 0 && shipT < 1 && (
          <g transform={`translate(${shipX} 598)`}>
            <path d="M-50 0 L50 0 L36 22 L-36 22 Z" fill="#8a3a2a" />
            <rect x={-6} y={-40} width={4} height={40} fill="#5b3d1f" />
            <path d="M-2 -38 L34 -8 L-2 -8 Z" fill="#fff" />
            <circle cx={-34} cy={-4} r={3} fill="#ffd35a" opacity={dark > 0.3 ? 1 : 0} />
          </g>
        )}
        {/* fixed-width modular lighthouse core */}
        <g>
          {floorsOnShow().map((floor) => <FloorModule key={floor.id} floor={floor} />)}
          {/* the lift: a stand-in shaft behind the stairs until it has art */}
          {LAYOUT.lift && (
            <g className="lift" pointerEvents="none">
              <rect x={TOWER_X + STAIRS_X - 30} y={FLOOR_Y.lamp} width={60} height={FLOOR_Y[LAYOUT.rooms[0]] - FLOOR_Y.lamp} fill="#00000010" stroke="#14243a" strokeWidth={4} strokeDasharray="12 8" opacity={0.4} />
            </g>
          )}
          {/* lamp room, always on top */}
          <g transform={`translate(0 ${FLOOR_Y.lamp - 220})`}>
            <rect x={TOWER_X + 70} y={80} width={380} height={140} fill={s.lampLit ? '#fff2a8' : '#cfe8ee'} opacity={0.85} stroke="#5d6d73" strokeWidth={5} />
            {[0, 1, 2, 3].map((i) => <line key={i} x1={TOWER_X + 165 + i * 95} y1={80} x2={TOWER_X + 165 + i * 95} y2={220} stroke="#5d6d73" strokeWidth={4} />)}
            <path d={`M${TOWER_X + 60} 80 L${TOWER_X + 260} 20 L${TOWER_X + 460} 80 Z`} fill="#b8433a" stroke="#6b2520" strokeWidth={5} />
            <circle cx={TOWER_X + 260} cy={14} r={9} fill="#6b2520" />
          </g>
        </g>
        {/* the beam */}
        {s.lampLit && (
          <g className="beam" pointerEvents="none" transform={`translate(0 ${FLOOR_Y.lamp - 220})`}>
            <path d={`M${TOWER_X + 450} 150 L${W + 300} 20 L${W + 300} 300 Z`} fill="#fff6b0" opacity={0.28 + dark * 0.35} />
            <path d={`M${TOWER_X + 70} 150 L-300 20 L-300 300 Z`} fill="#fff6b0" opacity={(0.28 + dark * 0.35) * 0.7} />
          </g>
        )}

        {/* objects */}
        {OBJECTS.map((o) => (o.id === 'toilet' || !has(o.id) ? null : obj(o.id)))}
        {obj('toilet')}
        {/* the shut loo door */}
        {cabin && (
          <g>
            <rect x={worldX('toilet') - 36} y={FLOOR_Y.bedroom - 104} width={74} height={104} rx={4} fill="#8a5a2b" stroke="#4a2a12" strokeWidth={4} />
            <rect x={worldX('toilet') - 22} y={FLOOR_Y.bedroom - 92} width={46} height={18} rx={3} fill="#c9433b" />
            <text x={worldX('toilet') + 1} y={FLOOR_Y.bedroom - 79} textAnchor="middle" fontSize={11} fontWeight={800} fill="#fff">ENGAGED</text>
          </g>
        )}

        {/* hit areas */}
        {OBJECTS.filter((o) => has(o.id)).map((o) => {
          const wx = worldX(o.id)
          const w = o.id === 'jetty' ? 230 : o.id === 'shop' ? 140 : 96
          const hh = o.id === 'shop' ? 130 : 110
          const fy = FLOOR_Y[o.floor]
          return (
            <g
              key={o.id}
              className={`hit ${selected === o.id ? 'picked' : ''} ${(o.id === 'phone' && s.ringing) || (o.id === 'door' && s.visits.some((v) => v.state === 'waiting')) ? 'alert' : ''}`}
              role="button"
              tabIndex={0}
              aria-label={o.label}
              onClick={() => onObject(o.id)}
              onKeyDown={(event) => {
                if (event.key === 'Enter' || event.key === ' ') {
                  event.preventDefault()
                  onObject(o.id)
                }
              }}
            >
              <rect x={wx - w / 2} y={fy - hh} width={w} height={hh} rx={10} />
              <title>{o.label}</title>
            </g>
          )
        })}

        <Actors s={s} onArrive={onArrive} shrugAt={shrugAt} petJump={petJump} onPose={onPose} />

        {/* effects */}
        {d && d.phase === 'doing' && d.fx && (
          <g pointerEvents="none" className={`fx fx-${d.fx}`} key={`${d.n}`}>
            {Array.from({ length: d.fx === 'stench' ? 7 : 4 }, (_, i) => {
              const ox = worldX(d.object === 'here' ? 'bed' : d.object)
              const oy = FLOOR_Y[floorOf(d.object === 'here' ? 'bed' : d.object)] - 90
              const spread = d.fx === 'stench' ? 80 : 36
              return (
                <text key={i} x={ox + (i - 2) * (spread / 3)} y={oy} fontSize={d.fx === 'stench' ? 30 : 24} textAnchor="middle" style={{ animationDelay: `${i * 0.45}s` }}>
                  {FX[d.fx!]}
                </text>
              )
            })}
          </g>
        )}
        {d && d.fx === 'stench' && d.phase === 'doing' && (
          <g pointerEvents="none">
            {[0, 1, 2, 3].map((i) => <circle key={i} className="gas" cx={worldX('toilet') - 20 - i * 30} cy={FLOOR_Y.bedroom - 40 - (i % 2) * 24} r={22 + i * 5} fill="#9bd15a" style={{ animationDelay: `${i * 0.6}s` }} />)}
          </g>
        )}

        {/* night and weather */}
        <rect x={left - 300} y={top - 200} width={vw + 600} height={H + 400} fill="#0b1236" opacity={dark * 0.55 + (storm ? 0.18 : 0)} pointerEvents="none" />
        {storm && <Rain />}
        {flash > 0 && <rect key={flash} className="lightning" x={left - 300} y={top - 200} width={vw + 600} height={H + 400} fill="#fff" pointerEvents="none" />}
      </g>
    </svg>
  )
}
