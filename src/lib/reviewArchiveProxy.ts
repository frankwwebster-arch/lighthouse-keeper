import { createHash } from 'node:crypto'
import type { ArchiveEntry } from './reviewArchive'

const CONTENT_TYPES: Record<string, string> = {
  '.avif': 'image/avif',
  '.gif': 'image/gif',
  '.jpeg': 'image/jpeg',
  '.jpg': 'image/jpeg',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.webp': 'image/webp',
}

export async function proxyReviewArchiveEntry(entry: ArchiveEntry): Promise<Response> {
  const upstream = await fetch(entry.url, { cache: 'force-cache' })
  if (!upstream.ok) {
    return Response.json(
      { error: 'review archive object unavailable' },
      { status: 502, headers: { 'Cache-Control': 'no-store' } },
    )
  }

  const bytes = await upstream.arrayBuffer()
  const digest = createHash('sha256').update(new Uint8Array(bytes)).digest('hex')
  if (bytes.byteLength !== entry.bytes || digest !== entry.sha256) {
    return Response.json(
      { error: 'review archive object failed integrity verification' },
      { status: 502, headers: { 'Cache-Control': 'no-store' } },
    )
  }

  return new Response(bytes, {
    status: 200,
    headers: {
      'Cache-Control': 'public, max-age=31536000, immutable',
      'Content-Length': String(bytes.byteLength),
      'Content-Type': CONTENT_TYPES[entry.extension] ?? 'application/octet-stream',
      'Cross-Origin-Resource-Policy': 'same-origin',
      ETag: `"${entry.sha256}"`,
      'X-Content-Type-Options': 'nosniff',
      'X-Review-Archive-Sha256': entry.sha256,
    },
  })
}
