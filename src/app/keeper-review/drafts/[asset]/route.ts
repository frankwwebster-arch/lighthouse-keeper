import { NextResponse } from 'next/server'
import { reviewArchiveEntry } from '../../../../lib/reviewArchive'

export const dynamic = 'force-dynamic'

export async function GET(_request: Request, context: { params: { asset: string } }) {
  const pathname = `/keeper-review/drafts/${context.params.asset}`
  const entry = reviewArchiveEntry(pathname)
  if (!entry) return NextResponse.json({ error: 'unknown review asset' }, { status: 404 })
  const response = NextResponse.redirect(entry.url, 308)
  response.headers.set('Cache-Control', 'public, max-age=31536000, immutable')
  response.headers.set('X-Review-Archive-Sha256', entry.sha256)
  return response
}
