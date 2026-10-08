import { useEffect, useRef, useState, type FormEvent } from 'react'
import { DEFAULT_RULES, FOODS, MISSIONS, INTERACTIONS, NEEDS, NEED_LABEL, OBJECTS, UPGRADES, VISITOR_ONLY, foodById, baseTierName, objectById, upgradeKey, upgradeTier, type InteractionDef, type NeedId, type ObjectId, type PetKind, type Rules } from '../game/config'
import { insideVisit, moodOf, moodWord, nextUpgrade, owned, priceOf, tierOf, upgradePrice, waitingVisit, type DayResult, type Prompt, type State } from '../game/engine'
import type { Order } from '../game/engine'
import { NAMES, clockText, labelFor, moodFace, moodName } from '../game/words'
import { floorCount, goalKey, goalTarget, goalsOf, objectAvailable, openMissions, rewardOf, scaledTarget, started } from '../game/missions'

// ─── Top bar ─────────────────────────────────────────────────────────────────

const needTone = (v: number) => (v < 25 ? 'low' : v < 55 ? 'mid' : 'ok')
const NEED_ICON: Record<NeedId, string> = { hunger: '🍽️', energy: '⚡', fun: '🎈', hygiene: '🧼', bladder: '🚽', social: '💬', tidiness: '🧹' }

export function Hud({ s, paused, onPause, onDiary, onMissions, onMenu }: { s: State; paused: boolean; onPause: () => void; onDiary: () => void; onMissions: () => void; onMenu: () => void }) {
  const mood = moodWord(moodOf(s))
  return (
    <header className="hud">
      <div className="hud-main">
        <strong>Day {s.day}</strong>
        <span className="clock">{clockText(s.clock)}</span>
        <span className="coins">🪙 {s.credits}</span>
        <span className={`mood m-${mood}`}>{moodFace[mood]} {moodName[mood]}</span>
        {s.broken.length > 0 && <span className="faults" title="Objects waiting for repair">🛠️ {s.broken.length}</span>}
        {s.annoyedLevel > 0 && <span className="sleepy">😴 Bedtime!</span>}
      </div>
      <div className="needs">
        {NEEDS.map((n) => (
          <div key={n} className={`need ${needTone(s.needs[n])}`} title={NEED_LABEL[n]}>
            <span>{NEED_ICON[n]}</span>
            <div className="bar"><i style={{ width: `${Math.round(s.needs[n])}%` }} /></div>
          </div>
        ))}
      </div>
      <div className="hud-btns">
        <button onClick={onPause}>{paused ? '▶ Play' : '⏸ Pause'}</button>
        <button onClick={onMissions}>🎯 Mission</button>
        <button onClick={onDiary}>📖 Diary</button>
        <button onClick={onMenu}>⚙</button>
      </div>
    </header>
  )
}

// ─── Object menu (Sims-style) ────────────────────────────────────────────────

export function menuFor(s: State, id: ObjectId): InteractionDef[] {
  const v = insideVisit(s)
  return INTERACTIONS.filter((i) => i.object === id).filter((i) => {
    if (VISITOR_ONLY.includes(i.id)) return !!v
    if (i.id === 'door_greet') return !!waitingVisit(s)
    if (i.id === 'phone_answer') return !!s.ringing
    return true
  })
}

export function ObjectMenu({ s, id, label, onPick, onUpgrade, onClose }: { s: State; id: ObjectId; label: string; onPick: (o: Order) => void; onUpgrade: () => void; onClose: () => void }) {
  const items = menuFor(s, id)
  const broken = s.broken.includes(id)
  const up = nextUpgrade(s, id)
  const now = upgradeTier(id, tierOf(s, id))?.name ?? baseTierName(id)
  return (
    <div className="sheet menu">
      <div className="sheet-head">
        <b>{now ?? label}</b>
        <button className="x" onClick={onClose} aria-label="Close">✕</button>
      </div>
      {broken && <p className="fault-copy">It has broken down. Repair it before using it again.</p>}
      {!broken && items.length === 0 && <p className="dim">Nothing to do with this right now.</p>}
      <div className="choices">
        {broken && <button className="big repair" onClick={() => onPick({ id: 'repair', object: id })}>🛠️ Repair {label.toLowerCase()}</button>}
        {!broken && items.map((i) => {
          const kind = i.id === 'fridge_snack' ? 'snack' : i.id === 'cooker_cook' ? 'cook' : null
          const stock = kind ? owned(s, kind) : []
          return (
            <div key={i.id} className="choice-group">
              <button className="big" onClick={() => onPick({ id: i.id })}>{labelFor(i.id, s)}</button>
              {stock.map((f) => (
                <button key={f} className="chip" onClick={() => onPick({ id: i.id, item: f })}>
                  {foodById(f)?.label} ×{s.items[f]}
                </button>
              ))}
            </div>
          )
        })}
        {up && (
          <button className="big upgrade" disabled={s.credits < up.price} onClick={onUpgrade}>
            ⬆️ Upgrade to {up.name} · 🪙 {up.price}
            {s.credits < up.price && <small> (save {up.price - s.credits} more)</small>}
          </button>
        )}
      </div>
    </div>
  )
}

/** Quick buttons for the things that need answering. */
export function Alerts({ s, onPick }: { s: State; onPick: (o: Order) => void }) {
  const v = insideVisit(s)
  const here = INTERACTIONS.filter((i) => i.object === 'here' && (VISITOR_ONLY.includes(i.id) ? !!v : true))
  return (
    <div className="alerts">
      {s.ringing && <button className="pulse" onClick={() => onPick({ id: 'phone_answer' })}>📞 Phone is ringing!</button>}
      {waitingVisit(s) && <button className="pulse" onClick={() => onPick({ id: 'door_greet' })}>🚪 Someone at the door</button>}
      {here.map((i) => <button key={i.id} onClick={() => onPick({ id: i.id })}>{labelFor(i.id, s)}</button>)}
    </div>
  )
}

// ─── Shop ────────────────────────────────────────────────────────────────────

export function Shop({ s, onBuy, onLeave }: { s: State; onBuy: (id: string) => void; onLeave: () => void }) {
  return (
    <div className="modal">
      <div className="card shop">
        <h2>🛒 The Shop</h2>
        <p>You have <b>🪙 {s.credits}</b></p>
        <div className="goods">
          {FOODS.filter((f) => f.cost > 0 && f.kind !== 'takeaway').map((f) => {
            const liked = s.personality.likes.includes('food:' + f.id)
            return (
              <button key={f.id} disabled={s.credits < priceOf(s, f)} onClick={() => onBuy(f.id)}>
                <span>{f.label}{liked ? ' ❤️' : ''}</span>
                <small>🪙 {priceOf(s, f)} · have {s.items[f.id] ?? 0}</small>
              </button>
            )
          })}
        </div>
        <button className="big" onClick={onLeave}>Done shopping</button>
      </div>
    </div>
  )
}

// ─── Typing bar ──────────────────────────────────────────────────────────────

export function CommandBar({ onSubmit, placeholder, pending, onYes, onNo }: { onSubmit: (t: string) => void; placeholder: string; pending: string | null; onYes: () => void; onNo: () => void }) {
  const [text, setText] = useState('')
  const submit = (e: FormEvent) => {
    e.preventDefault()
    if (!text.trim()) return
    onSubmit(text)
    setText('')
  }
  return (
    <form className="cmd" onSubmit={submit}>
      {pending && (
        <div className="didyou">
          <span>{pending}</span>
          <button type="button" onClick={onYes}>Yes</button>
          <button type="button" onClick={onNo}>No</button>
        </div>
      )}
      <div className="row">
        <input value={text} onChange={(e) => setText(e.target.value)} placeholder={placeholder} autoCapitalize="none" autoCorrect="off" spellCheck={false} enterKeyHint="go" aria-label="Tell the keeper what to do" />
        <button type="submit" className="go">Go</button>
      </div>
    </form>
  )
}

// ─── Questions from the keeper ───────────────────────────────────────────────

export function PromptBar({ s, prompt, onAnswer, onSkip }: { s: State; prompt: Prompt; onAnswer: (t: string) => void; onSkip: () => void }) {
  const [text, setText] = useState('')
  const ref = useRef<HTMLInputElement>(null)
  useEffect(() => {
    ref.current?.focus({ preventScroll: true })
  }, [prompt])
  const quiz = prompt.kind === 'quiz'
  return (
    <form
      className={`ask ${quiz ? 'quiz' : 'chat'}`}
      onSubmit={(e) => {
        e.preventDefault()
        if (!text.trim()) return
        onAnswer(text)
        setText('')
      }}
    >
      <div className="q">
        <b>{s.name} asks:</b> {quiz ? prompt.quiz.text : prompt.chat.text}
        {quiz && prompt.tries > 0 && !prompt.revealed && <em> Hint: {prompt.quiz.hint}</em>}
        {quiz && prompt.revealed && <em> The answer is “{prompt.quiz.show}”. Type it to carry on.</em>}
      </div>
      <div className="row">
        <input ref={ref} value={text} onChange={(e) => setText(e.target.value)} placeholder="Type your answer…" autoCapitalize="none" autoCorrect="off" spellCheck={false} aria-label="Your answer" />
        <button type="submit" className="go">Answer</button>
        {!quiz && <button type="button" onClick={onSkip}>Skip</button>}
      </div>
    </form>
  )
}

// ─── Diary ───────────────────────────────────────────────────────────────────

export interface Entry {
  n: number
  text: string
  tone?: 'good' | 'bad' | 'info'
}

const UNLOCK_NAME: Record<string, string> = { aquarium: 'aquarium', weather: 'weather station', lair: 'hidden lair', lift: 'lift' }

/** Every open mission and its goals (work on any, in any order), what is being built tonight, and what is done. A secret mission stays a mystery until he makes a start. */
export function Missions({ s, onClose }: { s: State; onClose: () => void }) {
  const open = openMissions(s.missions, floorCount(s))
  const later = MISSIONS.filter((x) => !s.missions.done.includes(x.id) && !open.includes(x))
  return (
    <aside className="drawer missions">
      <div className="sheet-head">
        <b>🎯 Missions</b>
        <button className="x" onClick={onClose}>✕</button>
      </div>
      {s.arriving.length > 0 && <p className="good">🏗️ Something is being built tonight… wait and see in the morning!</p>}
      {open.length === 0 && later.length === 0 && <p>Every mission done. What a keeper!</p>}
      {open.map((m) => (
        m.secret && !started(m, s.missions) ? (
          <div key={m.id} className="mission">
            <h3>??? A mystery</h3>
            <p className="dim">Something strange is going on. Keep exploring and it might show itself…</p>
          </div>
        ) : (
          <div key={m.id} className="mission">
            <h3>{m.title}</h3>
            <p>{m.blurb}</p>
            <ul>
              {goalsOf(m, s.missions, s.rules).map((g) => (
                <li key={g.event} className={g.met ? 'good' : undefined}>
                  {g.met ? '✅' : '⬜'} {g.label}: <b>{g.got} / {g.count}</b>
                </li>
              ))}
            </ul>
          </div>
        )
      ))}
      <ul>
        {later.map((x) => <li key={x.id} className="dim">🔒 {x.secret ? '???' : x.title} (needs a taller lighthouse: {x.needsFloors} floors)</li>)}
        {MISSIONS.filter((x) => s.missions.done.includes(x.id)).map((x) => <li key={x.id} className="good">🏆 {x.title}</li>)}
      </ul>
    </aside>
  )
}

export function Diary({ entries, onClose }: { entries: Entry[]; onClose: () => void }) {
  return (
    <aside className="drawer">
      <div className="sheet-head">
        <b>Diary</b>
        <button className="x" onClick={onClose}>✕</button>
      </div>
      <ul>
        {[...entries].reverse().map((e) => <li key={e.n} className={e.tone}>{e.text}</li>)}
      </ul>
    </aside>
  )
}

// ─── Start, report, settings ─────────────────────────────────────────────────

const pickOf = <T,>(list: readonly T[]): T => list[Math.floor(Math.random() * list.length)]

export function Setup({ who, canContinue, onContinue, onStart }: { who: string; canContinue: boolean; onContinue: () => void; onStart: (name: string, petName: string, kind: PetKind) => void }) {
  const [kind, setKind] = useState<PetKind>('cat')
  const [name, setName] = useState('')
  const [pet, setPet] = useState('')
  return (
    <div className="modal solid">
      <form
        className="card setup"
        onSubmit={(e) => {
          e.preventDefault()
          onStart(name.trim() || pickOf(NAMES.keeper), pet.trim() || pickOf(kind === 'cat' ? NAMES.cat : NAMES.gull), kind)
        }}
      >
        <h1>🏝️ Lighthouse Keeper</h1>
        <p className="dim">Playing as {who}</p>
        {canContinue && <button type="button" className="big" onClick={onContinue}>▶ Carry on with my game</button>}
        <p>{canContinue ? 'Or start a new keeper:' : 'Let’s meet your keeper!'}</p>
        <label>
          What is the keeper called?
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Type a name (or leave blank)" autoCapitalize="words" />
        </label>
        <div className="kinds">
          <button type="button" className={kind === 'cat' ? 'on' : ''} onClick={() => setKind('cat')}>🐱 A cat</button>
          <button type="button" className={kind === 'gull' ? 'on' : ''} onClick={() => setKind('gull')}>🐦 A seagull</button>
        </div>
        <label>
          What is the pet called?
          <input value={pet} onChange={(e) => setPet(e.target.value)} placeholder="Type a name (or leave blank)" autoCapitalize="words" />
        </label>
        <button type="submit" className="big">Start!</button>
      </form>
    </div>
  )
}

const PART_LABEL: Record<DayResult['parts'][number]['id'], string> = { mood: 'Happy keeper', ship: 'Ship saved', friends: 'Friends & visitors', pet: 'Pet looked after', house: 'Clean & tidy', brain: 'Brainy answers', bedtime: 'Bedtime' }

export function Report({ s, onNext }: { s: State; onNext: () => void }) {
  const r = s.history[s.history.length - 1]
  const [ready, setReady] = useState(false)
  useEffect(() => {
    const t = setTimeout(() => setReady(true), 2600)
    return () => clearTimeout(t)
  }, [])
  if (!r) return null
  return (
    <div className="modal solid night">
      {!ready ? (
        <div className="sleeping">🌙 <span>Zzz…</span></div>
      ) : (
        <div className="card report">
          <h2>Day {r.day} is over!</h2>
          <div className="score">{r.score}<small>/100</small></div>
          <p className="rating">{r.rating.replace(/_/g, ' ')}</p>
          <h3>Needs: {r.greens} of {r.needs.length} green</h3>
          <ul className="greens">
            {r.needs.map((n) => (
              <li key={n.id} className={n.green ? 'green' : 'red'}>
                <span>{NEED_ICON[n.id]} {NEED_LABEL[n.id]}</span>
                <div className="bar"><i style={{ width: `${n.avg}%` }} /></div>
                <b>{n.green ? '✔' : '✘'}</b>
              </li>
            ))}
          </ul>
          <h3>Bonus marks</h3>
          <ul>
            {r.parts.map((p) => (
              <li key={p.id}>
                <span>{PART_LABEL[p.id]}</span>
                <div className="bar"><i style={{ width: `${(p.got / p.of) * 100}%` }} /></div>
                <b>{p.got}/{p.of}</b>
              </li>
            ))}
          </ul>
          <p>Tomorrow’s allowance: <b>🪙 {r.allowance}</b> <small>(more green bars = more credits)</small></p>
          <button className="big" onClick={onNext}>☀️ Start day {r.day + 1}</button>
        </div>
      )}
    </div>
  )
}

export function SettingsMenu({ who, onClose, onNew, onGrownUps, onSwitch }: { who: string; onClose: () => void; onNew: () => void; onGrownUps: () => void; onSwitch: () => void }) {
  return (
    <div className="modal" onClick={onClose}>
      <div className="card" onClick={(e) => e.stopPropagation()}>
        <h2>Menu</h2>
        <p className="dim">Playing as {who}</p>
        <button className="big" onClick={onClose}>Back to the game</button>
        <button onClick={onSwitch}>👥 Switch player</button>
        <button onClick={onGrownUps}>🔒 Grown-ups</button>
        <button onClick={() => { if (confirm('Start again from day 1? The saved game will be lost.')) onNew() }}>New game</button>
      </div>
    </div>
  )
}

// ─── Grown-ups' panel ────────────────────────────────────────────────────────

const Num = ({ label, hint, value, onChange, min = 0, max = 999 }: { label: string; hint?: string; value: number; onChange: (n: number) => void; min?: number; max?: number }) => (
  <label className="num">
    <span>{label}{hint && <small> {hint}</small>}</span>
    <input type="number" inputMode="numeric" min={min} max={max} value={value} onChange={(e) => onChange(Math.min(max, Math.max(min, Math.round(Number(e.target.value) || 0))))} />
  </label>
)

export function GrownUps({ s, rules, credits, who, verify, onRules, onGift, onGiftUpgrade, onFinishMission, onPin, onClose }: { s: State; rules: Rules; credits: number; who: string; verify: (pin: string) => Promise<boolean>; onRules: (r: Rules, pin: string) => void; onGift: (n: number) => void; onGiftUpgrade: (id: ObjectId) => void; onFinishMission: (id: string) => void; onPin: (pin: string, newPin: string) => Promise<boolean>; onClose: () => void }) {
  const [typed, setTyped] = useState('')
  const [pin, setPin] = useState<string | null>(null)
  const [wrong, setWrong] = useState(false)
  const [gift, setGift] = useState(10)
  const [newPin, setNewPin] = useState('')
  const [pinMsg, setPinMsg] = useState('')
  const open = pin !== null
  const set = (patch: Partial<Rules>) => onRules({ ...rules, ...patch }, pin ?? '')
  const setPrice = (id: string, price: number | undefined) => {
    const prices = { ...rules.prices }
    if (price === undefined) delete prices[id]
    else prices[id] = price
    set({ prices })
  }
  if (!open) {
    return (
      <div className="modal" onClick={onClose}>
        <form className="card" onClick={(e) => e.stopPropagation()} onSubmit={async (e) => { e.preventDefault(); if (await verify(typed)) setPin(typed); else { setWrong(true); setTyped('') } }}>
          <h2>🔒 Grown-ups only</h2>
          <p>Enter the PIN (it starts as 1234).{wrong && <b> Not right, try again.</b>}</p>
          <input type="password" inputMode="numeric" value={typed} onChange={(e) => setTyped(e.target.value)} autoFocus />
          <button className="big" type="submit">Open</button>
          <button type="button" onClick={onClose}>Back</button>
        </form>
      </div>
    )
  }
  return (
    <div className="modal">
      <div className="card admin">
        <h2>Grown-ups’ dials: {who}</h2>
        <h3>Daily allowance</h3>
        <Num label="Guaranteed each morning" value={rules.allowanceBase} onChange={(n) => set({ allowanceBase: n })} />
        <Num label="Extra for all 7 bars green" hint="(shared out: each green bar earns a seventh)" value={rules.allowanceBonus} onChange={(n) => set({ allowanceBonus: n })} />
        <Num label="A bar is green at" hint="(average % over the day)" value={rules.greenAt} min={10} max={95} onChange={(n) => set({ greenAt: n })} />
        <Num label="First day’s credits" value={rules.firstDay} onChange={(n) => set({ firstDay: n })} />
        <Num label="Most he can save overnight" value={rules.carryCap} onChange={(n) => set({ carryCap: n })} />
        <h3>Questions</h3>
        <label className="num">
          <span>Difficulty <small>(1 = age 7, 2 = about 9, 3 = 11+: harder sums, fractions, percentages, spelling and general knowledge)</small></span>
          <input type="range" min={1} max={3} step={1} value={rules.quizLevel} onChange={(e) => set({ quizLevel: Number(e.target.value) as 1 | 2 | 3 })} />
          <b>Level {rules.quizLevel}</b>
        </label>
        <h3>Breakdowns</h3>
        <Num label="Average game-minutes between faults" hint="(0 = off; 60 ≈ hourly)" value={rules.breakdownMinutes} min={0} max={1440} onChange={(n) => set({ breakdownMinutes: n })} />
        <Num label="Most broken at once" hint="(0 also turns faults off)" value={rules.maxBreakdowns} min={0} max={10} onChange={(n) => set({ maxBreakdowns: n })} />
        <h3>Prices</h3>
        <label className="num">
          <span>All prices <small>(% of normal)</small></span>
          <input type="range" min={25} max={300} step={5} value={rules.priceScale} onChange={(e) => set({ priceScale: Number(e.target.value) })} />
          <b>{rules.priceScale}%</b>
        </label>
        {FOODS.filter((f) => f.cost > 0).map((f) => (
          <Num key={f.id} label={f.label} hint={rules.prices[f.id] === undefined ? `(normal ${f.cost}, now ${priceOf({ rules }, f)})` : '(your price)'} value={rules.prices[f.id] ?? priceOf({ rules }, f)} onChange={(n) => setPrice(f.id, n)} />
        ))}
        <button onClick={() => set({ prices: {} })}>Clear my own prices</button>
        <h3>Surprise gift</h3>
        <div className="row">
          <Num label={`Credits (he has ${credits})`} value={gift} onChange={setGift} />
          <button className="big" onClick={() => onGift(gift)}>🎁 Give</button>
        </div>
        <h3>Upgrades</h3>
        <label className="num">
          <span>All upgrade prices <small>(% of normal; applies to every upgrade)</small></span>
          <input type="range" min={25} max={300} step={5} value={rules.upgradeScale} onChange={(e) => set({ upgradeScale: Number(e.target.value) })} />
          <b>{rules.upgradeScale}%</b>
        </label>
        <details className="mission-dials">
          <summary>Set each upgrade price yourself</summary>
          <p className="dim">These beat the overall setting above.</p>
          {(Object.keys(UPGRADES) as ObjectId[]).map((id) => (
            <div key={id}>
              <b>{objectById(id)?.label}</b>
              {UPGRADES[id]!.map((u, i) => {
                const tier = i + 2
                const own = rules.upgradePrices?.[upgradeKey(id, tier)]
                return <Num key={tier} label={u.name} hint={own === undefined ? `(normal ${u.cost}, now ${upgradePrice(rules, id, tier)})` : '(your price)'} value={upgradePrice(rules, id, tier)} onChange={(n) => set({ upgradePrices: { ...rules.upgradePrices, [upgradeKey(id, tier)]: n } })} />
              })}
            </div>
          ))}
          <button onClick={() => set({ upgradePrices: {} })}>Clear my own upgrade prices</button>
        </details>
        <details className="mission-dials">
          <summary>Give an upgrade as a present</summary>
          {OBJECTS.filter((o) => UPGRADES[o.id] && objectAvailable(s, o.id)).map((o) => {
            const up = nextUpgrade(s, o.id)
            const has = upgradeTier(o.id, tierOf(s, o.id))
            return (
              <div key={o.id} className="row">
                <span>{o.label}: <b>{has?.name ?? baseTierName(o.id) ?? 'Standard'}</b></span>
                {up ? <button onClick={() => onGiftUpgrade(o.id)}>🎁 Give {up.name}</button> : <small className="dim">top tier</small>}
              </div>
            )
          })}
        </details>
        <h3>Missions</h3>
        <label className="num">
          <span>Mission size <small>(% of normal: 120% means fishing 4 times instead of 3; applies to every mission)</small></span>
          <input type="range" min={25} max={300} step={5} value={rules.missionScale} onChange={(e) => set({ missionScale: Number(e.target.value) })} />
          <b>{rules.missionScale}%</b>
        </label>
        <Num label="Credits for finishing a mission" value={rules.missionReward} onChange={(n) => set({ missionReward: n })} />
        <details className="mission-dials">
          <summary>Set each mission yourself</summary>
          <p className="dim">These beat the overall settings above. Lowering a target below what he has already done finishes the mission.</p>
          {MISSIONS.map((m) => (
            <div key={m.id}>
              <b>{m.title}</b> <small>(unlocks the {UNLOCK_NAME[m.unlocks]})</small>
              {m.goals.map((g, i) => (
                <Num key={g.event} label={g.label} hint={rules.missionGoals?.[goalKey(m, i)] === undefined ? `(from the size: ${scaledTarget(m, i, rules)})` : '(your number)'} value={goalTarget(m, i, rules)} min={1} max={99} onChange={(n) => set({ missionGoals: { ...rules.missionGoals, [goalKey(m, i)]: n } })} />
              ))}
              <Num label="Credits for finishing it" hint={rules.missionRewards?.[m.id] === undefined ? '(the overall amount)' : '(your number)'} value={rewardOf(m, rules)} onChange={(n) => set({ missionRewards: { ...rules.missionRewards, [m.id]: n } })} />
            </div>
          ))}
          <button onClick={() => set({ missionGoals: {}, missionRewards: {} })}>Clear my own mission numbers</button>
        </details>
        {openMissions(s.missions, floorCount(s)).map((m) => (
          <div key={m.id} className="row">
            <span>Open: <b>{m.title}</b></span>
            <button onClick={() => onFinishMission(m.id)}>🎁 Finish it now</button>
          </div>
        ))}
        <p className="dim">A finished floor mission builds its floor overnight: it appears the next morning (one new floor a morning). The lift goes in at once.</p>
        <h3>PIN</h3>
        <div className="row">
          <input value={newPin} onChange={(e) => setNewPin(e.target.value.replace(/\D/g, '').slice(0, 8))} placeholder="New PIN (digits)" inputMode="numeric" />
          <button disabled={newPin.length < 3} onClick={async () => { const ok = await onPin(pin ?? '', newPin); if (ok) setPin(newPin); setPinMsg(ok ? 'PIN changed.' : 'Could not change it.'); setNewPin('') }}>Change</button>
        </div>
        {pinMsg && <p>{pinMsg}</p>}
        <button onClick={() => onRules({ ...DEFAULT_RULES }, pin ?? '')}>Reset all dials</button>
        <button className="big" onClick={onClose}>Done</button>
      </div>
    </div>
  )
}
