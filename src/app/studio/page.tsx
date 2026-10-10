'use client'

import dynamic from 'next/dynamic'
import '../../studio/studio.css'

// The recipe studio plays sprites and sound in the browser, so it is never drawn on the server.
const Studio = dynamic(() => import('../../studio/Studio'), { ssr: false })

export default function Page() {
  return <Studio />
}
