import type { ReactNode } from 'react'
import type { ObjectId } from '../game/config'
import { Sprite } from './Sprite'

export type ObjectVisualState = 'standard' | 'on' | 'broken'

function StateEffects({ state }: { state: ObjectVisualState }) {
  if (state === 'standard') return null
  if (state === 'on') {
    return <path className="object-on-pulse" d="M-26-6h52" fill="none" stroke="#ffd35a" strokeWidth={4} strokeLinecap="square" />
  }
  return (
    <g className="broken-effects" pointerEvents="none" aria-hidden="true">
      <g className="broken-smoke">
        <rect x={-12} y={-82} width={12} height={12} fill="#7b8792" />
        <rect x={2} y={-102} width={16} height={16} fill="#a3abb2" />
      </g>
      <g className="broken-sparks" fill="#ffd35a">
        <rect x={20} y={-68} width={8} height={4} />
        <rect x={28} y={-76} width={4} height={8} />
        <rect x={-30} y={-58} width={8} height={4} />
      </g>
    </g>
  )
}

/** Vector drawings of every object. (x = centre, y = the floor.) */
export function ObjectArt({ id, x, y, state = 'standard', extra }: { id: ObjectId; x: number; y: number; state?: ObjectVisualState; extra?: { ringing?: boolean; ready?: number; waiting?: boolean } }): ReactNode {
  const on = state === 'on'
  const g = (w: number, h: number, kids: ReactNode) => (
    <g transform={`translate(${x} ${y})`} className={`object object-${id} state-${state}`} data-state={state}>
      <g className="object-body">
        <Sprite name={[`obj_${id}_${state}`, `obj_${id}`]} w={w} h={h}>
          {kids}
        </Sprite>
      </g>
      <StateEffects state={state} />
    </g>
  )
  switch (id) {
    case 'door':
      return g(50, 96, <><rect x={-24} y={-96} width={48} height={96} rx={4} fill="#7a4a24" stroke="#4a2a12" strokeWidth={3} /><circle cx={14} cy={-46} r={4} fill="#f3c64a" /><rect x={-14} y={-84} width={28} height={22} rx={3} fill="#9fd3ea" /></>)
    case 'fridge':
      return g(48, 96, <><rect x={-24} y={-96} width={48} height={96} rx={5} fill="#e9f1f5" stroke="#8aa1ad" strokeWidth={3} /><line x1={-24} y1={-62} x2={24} y2={-62} stroke="#8aa1ad" strokeWidth={3} /><rect x={14} y={-88} width={4} height={18} rx={2} fill="#8aa1ad" /><rect x={14} y={-56} width={4} height={26} rx={2} fill="#8aa1ad" /></>)
    case 'cooker':
      return g(70, 60, <><rect x={-34} y={-60} width={68} height={60} rx={4} fill="#3b3f46" stroke="#1d2024" strokeWidth={3} /><ellipse cx={-16} cy={-60} rx={13} ry={4} fill="#111" /><ellipse cx={16} cy={-60} rx={13} ry={4} fill="#111" /><rect x={-22} y={-36} width={44} height={26} rx={3} fill="#222a33" /><circle cx={-22} cy={-48} r={3} fill="#d9d9d9" /><circle cx={22} cy={-48} r={3} fill="#d9d9d9" /></>)
    case 'broom':
      return g(30, 90, <><line x1={0} y1={-90} x2={4} y2={-18} stroke="#8a5a2b" strokeWidth={5} strokeLinecap="round" /><path d="M-10 -20 L16 -20 L20 0 L-14 0 Z" fill="#d5b04a" stroke="#8a6d1f" strokeWidth={2} /></>)
    case 'petbowl':
      return g(40, 20, <><path d="M-18 -14 L18 -14 L13 0 L-13 0 Z" fill="#c9433b" stroke="#7d2420" strokeWidth={2} /><ellipse cx={0} cy={-14} rx={18} ry={4} fill="#e8bd78" /></>)
    case 'toilet':
      return g(50, 70, <><rect x={-12} y={-70} width={34} height={30} rx={4} fill="#f4f4f4" stroke="#aaa" strokeWidth={2} /><path d="M-24 -38 L16 -38 L12 -16 L-6 -6 L-6 0 L-20 0 L-20 -10 Z" fill="#fff" stroke="#aaa" strokeWidth={2} /></>)
    case 'tv':
      return g(110, 90, <><rect x={-42} y={-84} width={84} height={58} rx={6} fill="#23262b" stroke="#111" strokeWidth={3} /><rect x={-36} y={-78} width={72} height={46} rx={3} fill={on ? '#5ad1ff' : '#10161c'}>{on && <animate attributeName="fill" values="#5ad1ff;#ffd35a;#ff7b9c;#7dff9e;#5ad1ff" dur="1.6s" repeatCount="indefinite" />}</rect><rect x={-30} y={-26} width={60} height={26} rx={3} fill="#6d4a2b" /></>)
    case 'bookshelf':
      return g(80, 110, <><rect x={-36} y={-110} width={72} height={110} rx={3} fill="#7b5230" stroke="#4a2e16" strokeWidth={3} />{[0, 1, 2].map((r) => <g key={r}><rect x={-30} y={-102 + r * 34} width={60} height={4} fill="#4a2e16" />{['#d9534f', '#3b82c4', '#e6b800', '#4c9a5f', '#8e5bb5', '#e07b39'].map((c, i) => <rect key={i} x={-28 + i * 9.5} y={-98 + r * 34} width={8} height={28} fill={c} />)}</g>)}</>)
    case 'piano':
      return g(100, 70, <><rect x={-46} y={-70} width={92} height={60} rx={4} fill="#1d1d22" stroke="#000" strokeWidth={3} /><rect x={-42} y={-30} width={84} height={16} fill="#f8f8f4" />{Array.from({ length: 10 }, (_, i) => <rect key={i} x={-38 + i * 8.2} y={-30} width={4} height={10} fill="#111" />)}<rect x={-40} y={-10} width={6} height={10} fill="#111" /><rect x={34} y={-10} width={6} height={10} fill="#111" /></>)
    case 'bed':
      return g(120, 54, <><rect x={-56} y={-40} width={8} height={40} fill="#6b4423" /><rect x={-56} y={-26} width={112} height={18} rx={4} fill="#4a76b8" stroke="#2c4a7a" strokeWidth={2} /><rect x={-52} y={-34} width={30} height={12} rx={6} fill="#fafafa" stroke="#bbb" strokeWidth={1.5} /><rect x={50} y={-34} width={6} height={34} fill="#6b4423" /></>)
    case 'phone':
      return g(60, 70, <><rect x={-22} y={-34} width={44} height={34} rx={3} fill="#8a5a2b" /><g className={extra?.ringing ? 'ringing' : undefined}><rect x={-16} y={-48} width={32} height={14} rx={6} fill="#c9433b" stroke="#7d2420" strokeWidth={2} /><circle cx={-12} cy={-52} r={4} fill="#c9433b" /><circle cx={12} cy={-52} r={4} fill="#c9433b" /></g></>)
    case 'basin':
      return g(60, 110, <><rect x={-24} y={-110} width={48} height={42} rx={4} fill="#cfe9f3" stroke="#7ba7b8" strokeWidth={3} /><path d="M-26 -52 L26 -52 L20 -36 L-20 -36 Z" fill="#fff" stroke="#aaa" strokeWidth={2} /><rect x={-5} y={-36} width={10} height={36} fill="#e6e6e6" stroke="#aaa" strokeWidth={2} /><rect x={-3} y={-60} width={6} height={9} fill="#9aa" /></>)
    case 'desk':
      return g(100, 80, <><rect x={-46} y={-44} width={92} height={8} rx={2} fill="#8a5a2b" /><rect x={-42} y={-36} width={6} height={36} fill="#6b4423" /><rect x={36} y={-36} width={6} height={36} fill="#6b4423" /><rect x={-20} y={-54} width={34} height={10} fill="#b83a3a" /><rect x={22} y={-66} width={4} height={22} fill="#333" /><path d="M12 -66 L36 -66 L30 -80 Z" fill="#f3c64a" /></>)
    case 'telescope':
      return g(90, 90, <><line x1={-18} y1={0} x2={0} y2={-36} stroke="#5b3d1f" strokeWidth={5} /><line x1={18} y1={0} x2={0} y2={-36} stroke="#5b3d1f" strokeWidth={5} /><rect x={-34} y={-62} width={64} height={16} rx={6} fill="#b58b2a" stroke="#6d5314" strokeWidth={2} transform="rotate(-18 0 -48)" /></>)
    case 'lamp':
      return g(120, 140, <><rect x={-8} y={-30} width={16} height={30} fill="#555" /><circle cx={0} cy={-70} r={34} fill={on ? '#fff6b0' : '#cfe8ee'} stroke="#7a8a90" strokeWidth={4} opacity={0.95}>{on && <animate attributeName="r" values="34;37;34" dur="1.4s" repeatCount="indefinite" />}</circle><circle cx={0} cy={-70} r={14} fill={on ? '#fffbe0' : '#e9f4f7'} /></>)
    case 'garden':
      return g(120, 70, <><rect x={-54} y={-40} width={108} height={40} fill="#6b4a2b" rx={4} />{[0, 1, 2].map((i) => <g key={i} transform={`translate(${-34 + i * 34} -40)`}><line x1={0} y1={0} x2={0} y2={-22} stroke="#3c8a3c" strokeWidth={4} /><ellipse cx={-6} cy={-14} rx={7} ry={4} fill="#4fb04f" /><ellipse cx={7} cy={-18} rx={7} ry={4} fill="#4fb04f" />{(extra?.ready ?? 0) > i && <circle cx={0} cy={-26} r={7} fill="#e8503a" />}</g>)}<path d="M-58 0 L-58 -50 M58 0 L58 -50" stroke="#b9996a" strokeWidth={5} /></>)
    case 'shop':
      return g(130, 120, <><rect x={-52} y={-80} width={104} height={80} fill="#e9d3a3" stroke="#8a6d3a" strokeWidth={3} /><path d="M-60 -80 L60 -80 L50 -100 L-50 -100 Z" fill="#c9433b" /><g>{[0, 1, 2, 3, 4].map((i) => <rect key={i} x={-60 + i * 24} y={-82} width={12} height={10} fill="#fff" />)}</g><rect x={-18} y={-56} width={36} height={56} fill="#6d4a2b" /><rect x={-46} y={-62} width={22} height={20} fill="#9fd3ea" /><rect x={-34} y={-124} width={68} height={20} rx={4} fill="#fff7d6" stroke="#8a6d3a" strokeWidth={2} /><text x={0} y={-109} textAnchor="middle" fontSize={14} fontWeight={700} fill="#8a3a2a">SHOP</text></>)
    case 'jetty':
      return g(220, 60, <><rect x={-110} y={-14} width={220} height={10} fill="#a07a47" stroke="#6b4e28" strokeWidth={2} />{[-90, -40, 10, 60, 100].map((p) => <rect key={p} x={p} y={-4} width={8} height={36} fill="#6b4e28" />)}<line x1={30} y1={-14} x2={52} y2={-62} stroke="#3a2a14" strokeWidth={3} /><line x1={52} y1={-62} x2={78} y2={-8} stroke="#ddd" strokeWidth={1} /></>)
    default:
      return null
  }
}
