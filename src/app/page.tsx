'use client'

import dynamic from 'next/dynamic'

// The game lives in the browser (clock, saved game, typing), so it is never drawn on the server.
const Game = dynamic(() => import('../Game'), { ssr: false })

export default function Page() {
  return <Game />
}
