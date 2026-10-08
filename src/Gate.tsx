import { useEffect, useState } from 'react'
import App from './App'
import type { Rules } from './game/config'
import type { State } from './game/engine'
import { addPlayer, listPlayers, loadGame, loadRules, type Player } from './game/remote'
import { SpriteProvider } from './ui/Sprite'

const LAST = 'lighthouse-keeper:last'

/** Who is playing? Each player has their own game and their own grown-ups' dials. */
export default function Gate() {
  const [players, setPlayers] = useState<Player[] | null>(null)
  const [db, setDb] = useState(false)
  const [chosen, setChosen] = useState<{ player: Player; initial: State | null; rules: Rules } | null>(null)
  const [adding, setAdding] = useState(false)
  const [name, setName] = useState('')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    let alive = true
    listPlayers().then((r) => {
      if (!alive) return
      setDb(r.db)
      setPlayers(r.players)
      setAdding(r.players.length === 0)
    })
    return () => {
      alive = false
    }
  }, [])

  const pick = async (player: Player) => {
    setBusy(true)
    const [initial, rules] = await Promise.all([loadGame(player.id, db), loadRules(player.id, db)])
    try {
      localStorage.setItem(LAST, player.id)
    } catch {
      // fine
    }
    setChosen({ player, initial, rules })
    setBusy(false)
  }

  if (chosen) {
    return (
      <SpriteProvider>
        <App key={chosen.player.id} player={chosen.player} db={db} initial={chosen.initial} rules={chosen.rules} onSwitch={() => setChosen(null)} />
      </SpriteProvider>
    )
  }

  let last = ''
  try {
    last = localStorage.getItem(LAST) ?? ''
  } catch {
    // fine
  }

  return (
    <div className="modal solid">
      <div className="card setup">
        <h1>🏝️ Lighthouse Keeper</h1>
        {players === null ? (
          <p>Loading…</p>
        ) : (
          <>
            <p>Who is playing?</p>
            <div className="players">
              {players.map((p) => (
                <button key={p.id} className={`big ${p.id === last ? 'on' : ''}`} disabled={busy} onClick={() => pick(p)}>
                  {p.name}
                </button>
              ))}
            </div>
            {adding ? (
              <form
                className="row"
                onSubmit={async (e) => {
                  e.preventDefault()
                  const n = name.trim()
                  if (!n) return
                  setBusy(true)
                  const p = await addPlayer(n, db)
                  setBusy(false)
                  if (p) {
                    setPlayers((l) => [...(l ?? []), p])
                    setName('')
                    setAdding(false)
                    void pick(p)
                  }
                }}
              >
                <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Type a name" autoCapitalize="words" maxLength={24} />
                <button className="go" type="submit" disabled={busy}>Add</button>
              </form>
            ) : (
              <button onClick={() => setAdding(true)}>➕ New player</button>
            )}
            {!db && <p className="dim">Saving on this device only.</p>}
          </>
        )}
      </div>
    </div>
  )
}
