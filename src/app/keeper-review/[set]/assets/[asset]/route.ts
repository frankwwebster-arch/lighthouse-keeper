import { NextResponse } from 'next/server'
import { reviewArchiveEntry } from '../../../../../lib/reviewArchive'
import { proxyReviewArchiveEntry } from '../../../../../lib/reviewArchiveProxy'

export const dynamic = 'force-dynamic'
export const runtime = 'nodejs'

const SAME_ORIGIN_ARCHIVE_SETS = new Set([
  'keeper-prime-morning-drafts-v1',
  'keeper-prime-morning-drafts-v6',
  'kitchen-room-layout-v1',
  'kitchen-room-layout-v2',
  'kitchen-room-layout-v3',
  'kitchen-room-layout-v4',
  'kitchen-room-layout-v5',
  'kitchen-room-layout-v6',
  'kitchen-room-layout-v7',
  'kitchen-room-layout-v8',
  'kitchen-room-layout-v9',
  'kitchen-room-layout-v10',
  'kitchen-room-layout-v11',
  'kitchen-room-layout-v12',
  'kitchen-room-layout-v13',
])

export async function GET(_request: Request, context: { params: { set: string; asset: string } }) {
  const pathname = `/keeper-review/${context.params.set}/assets/${context.params.asset}`
  const entry = reviewArchiveEntry(pathname)
  if (!entry) return NextResponse.json({ error: 'unknown review asset' }, { status: 404 })
  if (SAME_ORIGIN_ARCHIVE_SETS.has(context.params.set)) return proxyReviewArchiveEntry(entry)
  const response = NextResponse.redirect(entry.url, 307)
  response.headers.set('Cache-Control', 'public, max-age=300')
  response.headers.set('X-Review-Archive-Sha256', entry.sha256)
  return response
}
