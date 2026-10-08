'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { GAME, minutesPerSecond, objectById, type ObjectId } from './game/config'
import { momentOf, pickChat, replyToChat } from './game/chat'
import type { DoOrder } from './game/commands'
import { answeredChat, arrive, ask, buy, dropChat, gift, setRules, nextDay, order, rightAnswer, rollPersonality, shopOpen, startGame, stopDoing, tick, wrongAnswer, type State } from './game/engine'
import { isNo, isYes, read } from './game/matcher'
import { checkAnswer, makeQuiz } from './game/quiz'
import { clear, load, loadAdmin, save, saveAdmin } from './game/storage'
import { ack, tell } from './game/words'
import { Alerts, CommandBar, Diary, Hud, ObjectMenu, PromptBar, GrownUps, Report, SettingsMenu, Setup, Shop, type Entry } from './ui/Panels'
import { Scene } from './ui/Scene'


const SHRUGS = ['Erm… I have no idea what that means.', 'Hmm? Say that another way?', 'You lost me there!', 'Sorry, I do not know that one.']
const RUDE = /\b(hurry|idiot|stupid|shut up|dumb|useless|you fool)\b/
const NICE = /\b(please|thanks|thank you|cheers|pretty please)\b/

export default function App() {
  const [s, setS] = useState<State | null>(() => load())
  const [started, setStarted] = useState(false)
  const [paused, setPaused] = useState(false)
  const [selected, setSelected] = useState<ObjectId | null>(null)
  const [diary, setDiary] = useState<Entry[]>([])
  const [showDiary, setShowDiary] = useState(false)
  const [showMenu, setShowMenu] = useState(false)
  const [showAdmin, setShowAdmin] = useState(false)
  const [admin, setAdmin] = useState(loadAdmin)
  const [say, setSay] = useState<{ text: string; key: number } | null>(null)
  const [pending, setPending] = useState<{ doing: DoOrder[]; text: string } | null>(null)
  const [flash, setFlash] = useState(0)
  const [shrugAt, setShrugAt] = useState(0)
  const [petJump, setPetJump] = useState(0)
  const sRef = useRef(s)
  sRef.current = s
  const seen = useRef(Math.max(0, ...(s?.happenings.map((h) => h.n) ?? [0])))
  const lastInput = useRef(performance.now())
  const lastAsk = useRef(performance.now())
  const recentQ = useRef<string[]>([])
  const shrugN = useRef(0)
  const ackN = useRef(0)

  const poke = () => {
    lastInput.current = performance.now()
  }
  const speak = useCallback((text: string) => setSay({ text, key: performance.now() }), [])

  // Time passes.
  useEffect(() => {
    let last = performance.now()
    const id = setInterval(() => {
      const now = performance.now()
      const dt = Math.min(0.5, (now - last) / 1000)
      last = now
      const cur = sRef.current
      if (!started || paused || !cur || cur.phase !== 'day') return
      let next = tick(cur, dt * minutesPerSecond())
      // The keeper asks Ralph something now and then, when he has been idle a while.
      const q = GAME.quiz
      const busy = next.doing?.priv || (next.doing?.id === 'bed_sleep' && next.doing.phase === 'doing')
      if (!next.prompt && !busy && now - lastInput.current > q.idleSeconds * 1000 && now - lastAsk.current > q.gapSeconds * 1000) {
        lastAsk.current = now
        if (Math.random() < q.quizShare) {
          const quiz = makeQuiz(Math.random, { name: next.name, pet: next.petName }, recentQ.current, next.rules.quizLevel)
          recentQ.current = [...recentQ.current, quiz.id].slice(-30)
          next = ask(next, { kind: 'quiz', quiz, tries: 0, revealed: false })
        } else {
          const chat = pickChat(momentOf(new Date()), recentQ.current, Math.floor(Math.random() * 1000))
          recentQ.current = [...recentQ.current, chat.id].slice(-30)
          next = ask(next, { kind: 'chat', chat })
        }
      }
      sRef.current = next
      setS(next)
    }, 100)
    return () => clearInterval(id)
  }, [started, paused])

  // Turn what happened into words.
  useEffect(() => {
    if (!s) return
    const fresh = s.happenings.filter((h) => h.n > seen.current)
    if (!fresh.length) return
    seen.current = Math.max(...fresh.map((h) => h.n))
    const entries: Entry[] = []
    let line: string | undefined
    for (const h of fresh) {
      const t = tell(h, s)
      if (t.say) line = t.say
      if (t.diary) entries.push({ n: h.n, text: t.diary, tone: t.tone })
      if (t.boom === 'thunder') setFlash((f) => f + 1)
      if (h.kind === 'pet') setPetJump(performance.now() + 1500)
    }
    if (line) speak(line)
    if (entries.length) setDiary((d) => [...d, ...entries].slice(-GAME.diaryLimit))
  }, [s, speak])

  // The line fades.
  useEffect(() => {
    if (!say) return
    const t = setTimeout(() => setSay(null), 7000)
    return () => clearTimeout(t)
  }, [say])

  // Keep the game.
  useEffect(() => {
    if (!started) return
    const id = setInterval(() => sRef.current && save(sRef.current), 4000)
    return () => clearInterval(id)
  }, [started])
  useEffect(() => {
    if (s?.phase === 'report') save(s)
  }, [s?.phase]) // eslint-disable-line react-hooks/exhaustive-deps

  const update = (fn: (x: State) => State) => {
    const cur = sRef.current
    if (!cur) return
    const next = fn(cur)
    sRef.current = next
    setS(next)
  }

  const give = (orders: DoOrder[], delta = 0, text?: string) => {
    poke()
    setSelected(null)
    update((x) => order(x, orders, delta))
    ackN.current += 1
    const cur = sRef.current
    if (cur && text !== undefined) speak(ack(cur, ackN.current + Math.floor(Math.random() * 7)))
  }

  const submit = (text: string) => {
    poke()
    const cur = sRef.current
    if (!cur) return
    if (pending) {
      if (isYes(text)) {
        const p = pending
        setPending(null)
        give(p.doing, 0, text)
        return
      }
      setPending(null)
      if (isNo(text)) {
        speak('Oh. What did you mean, then?')
        return
      }
    }
    const res = read(text)
    if (res.kind === 'empty') return
    if (res.kind === 'shrug') {
      shrugN.current += 1
      setShrugAt(performance.now() + 1800)
      speak(SHRUGS[shrugN.current % SHRUGS.length])
      return
    }
    if (cur.doing?.id === 'bed_sleep' && cur.doing.phase === 'doing') {
      speak('Zzzzz… (he is fast asleep)')
      return
    }
    if (res.kind === 'ask') {
      setPending({ doing: res.doing, text: res.say })
      speak(res.say)
      return
    }
    const delta = RUDE.test(text.toLowerCase()) ? -1 : NICE.test(text.toLowerCase()) ? 1 : 0
    give(res.doing, delta, text)
  }

  const answer = (text: string) => {
    poke()
    const cur = sRef.current
    const p = cur?.prompt
    if (!cur || !p) return
    if (p.kind === 'quiz') {
      if (checkAnswer(p.quiz, text)) {
        update(rightAnswer)
      } else {
        update(wrongAnswer)
        speak(p.tries + 1 >= GAME.quiz.triesBeforeAnswer ? 'Not quite. Let me tell you the answer…' : 'Not quite! Have another go.')
      }
    } else {
      const r = replyToChat(p.chat, text, { pet: cur.petName, name: cur.name })
      speak(r.line)
      setDiary((d) => [...d, { n: performance.now(), text: `Ralph and ${cur.name} had a chat. “${r.line}”` }].slice(-GAME.diaryLimit))
      update((x) => answeredChat(x, r.good))
    }
    lastAsk.current = performance.now()
  }

  const clickObject = (id: ObjectId) => {
    poke()
    setSelected((cur) => (cur === id ? null : id))
  }

  const begin = (name: string, petName: string, petKind: 'cat' | 'gull') => {
    const seed = Math.floor(Math.random() * 2 ** 31)
    clear()
    seen.current = 0
    setDiary([])
    const g = startGame(seed, { name, petName, petKind, personality: rollPersonality(seed) }, admin.rules)
    sRef.current = g
    setS(g)
    setStarted(true)
    lastInput.current = lastAsk.current = performance.now()
  }

  if (!started || !s) {
    return <Setup canContinue={!!s && s.v === 1} onContinue={() => { lastInput.current = lastAsk.current = performance.now(); setStarted(true) }} onStart={begin} />
  }

  const doingAt = s.doing?.phase === 'doing' ? s.doing.object : null
  const label = selected ? objectById(selected)?.label ?? '' : ''

  return (
    <div className="game" onPointerDown={poke} onKeyDown={poke}>
      <Hud s={s} paused={paused} onPause={() => setPaused((p) => !p)} onDiary={() => setShowDiary((d) => !d)} onMenu={() => setShowMenu(true)} />
      <main className="stage">
        <Scene
          s={s}
          selected={selected}
          flash={flash}
          shrugAt={shrugAt}
          petJump={petJump}
          onObject={clickObject}
          onArrive={() => update(arrive)}
          onPose={() => undefined}
        />
        {say && (
          <div className="speech" key={say.key}>
            <b>{s.name}:</b> {say.text}
          </div>
        )}
        {s.doing && doingAt && !shopOpen(s) && !s.doing.priv && (
          <button className="stopper" onClick={() => update(stopDoing)}>✋ Stop</button>
        )}
        {paused && <div className="paused">⏸ Paused</div>}
        {showDiary && <Diary entries={diary} onClose={() => setShowDiary(false)} />}
      </main>
      <footer className="dock">
        {selected && <ObjectMenu s={s} id={selected} label={label} onPick={(o) => give([o], 0, 'menu')} onClose={() => setSelected(null)} />}
        {!selected && <Alerts s={s} onPick={(o) => give([o], 0, 'menu')} />}
        {s.prompt && <PromptBar s={s} prompt={s.prompt} onAnswer={answer} onSkip={() => update(dropChat)} />}
        <CommandBar onSubmit={submit} placeholder={`Tell ${s.name} what to do… (try “${s.needs.hunger < 50 ? 'make some toast' : 'play the piano'}”)`} pending={pending?.text ?? null} onYes={() => submit('yes')} onNo={() => submit('no')} />
      </footer>
      {shopOpen(s) && <Shop s={s} onBuy={(id) => update((x) => buy(x, id))} onLeave={() => update(stopDoing)} />}
      {s.phase === 'report' && <Report s={s} onNext={() => { update(nextDay); setDiary([]) }} />}
      {showAdmin && (
        <GrownUps
          pin={admin.pin}
          rules={s.rules}
          credits={s.credits}
          onRules={(r) => { const a = { ...admin, rules: r }; setAdmin(a); saveAdmin(a); update((x) => setRules(x, r)) }}
          onGift={(n) => update((x) => gift(x, n))}
          onPin={(p) => { const a = { ...admin, pin: p }; setAdmin(a); saveAdmin(a) }}
          onClose={() => setShowAdmin(false)}
        />
      )}
      {showMenu && <SettingsMenu onGrownUps={() => { setShowMenu(false); setShowAdmin(true) }} onClose={() => setShowMenu(false)} onNew={() => { setShowMenu(false); clear(); setStarted(false); setS(null) }} />}
    </div>
  )
}
