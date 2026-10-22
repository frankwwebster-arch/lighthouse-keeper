import { NextResponse } from 'next/server'
import { reviewArchiveEntry } from '../../../../../lib/reviewArchive'
import { proxyReviewArchiveEntry } from '../../../../../lib/reviewArchiveProxy'

export const dynamic = 'force-dynamic'
export const runtime = 'nodejs'

const SAME_ORIGIN_ARCHIVE_SETS = new Set([
  'kitchen-built-in-state-ligne-claire-v4-delivery-v2',
  'kitchen-built-in-state-ligne-claire-v4-delivery-v3',
  'keeper-prime-morning-drafts-v1',
  'kitchen-ligne-claire-healing-workbench-v42',
  'kitchen-ligne-claire-complete-review-v43',
  'kitchen-ligne-claire-complete-review-v44',
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
