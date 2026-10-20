import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

// Bubble-story pictures referenced in place in Codex's immutable art/drafts packs
// (data/activity-stories/README.md). Served from GitHub like the review archive,
// so nothing is copied into public/.
const RAW = 'https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/main/'

export async function GET(_request: Request, context: { params: { path: string[] } }) {
  const path = context.params.path.join('/')
  if (!/^art\/drafts\/[a-z0-9._/-]+\.png$/.test(path) || path.includes('..')) return NextResponse.json({ error: 'not a bubble-story picture' }, { status: 404 })
  const response = NextResponse.redirect(RAW + path, 307)
  response.headers.set('Cache-Control', 'public, max-age=300')
  return response
}
