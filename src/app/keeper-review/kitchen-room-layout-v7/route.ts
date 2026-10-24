import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

/** Keep the documented V7 review URL stable while its immutable shell stays public. */
export function GET(request: Request) {
  const requestUrl = new URL(request.url)
  const host = request.headers.get('x-forwarded-host') ?? request.headers.get('host') ?? requestUrl.host
  const protocol = request.headers.get('x-forwarded-proto') ?? requestUrl.protocol.replace(':', '')
  const target = new URL('/keeper-review/kitchen-room-layout-v7/index.html', `${protocol}://${host}`)
  const response = NextResponse.redirect(target, 307)
  response.headers.set('Cache-Control', 'no-store')
  return response
}
