import { NextResponse } from 'next/server'
import { reviewArchiveEntry } from '../../../../../lib/reviewArchive'

export const dynamic = 'force-dynamic'

export async function GET(_request: Request, context: { params: { set: string; asset: string } }) {
  const pathname = `/keeper-review/${context.params.set}/assets/${context.params.asset}`
  const entry = reviewArchiveEntry(pathname)
  if (!entry) return NextResponse.json({ error: 'unknown review asset' }, { status: 404 })
  const response = NextResponse.redirect(entry.url, 307)
  response.headers.set('Cache-Control', 'public, max-age=300')
  response.headers.set('X-Review-Archive-Sha256', entry.sha256)
  return response
}
