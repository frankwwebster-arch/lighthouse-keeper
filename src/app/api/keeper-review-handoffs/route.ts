import { randomUUID } from 'node:crypto'
import { NextResponse } from 'next/server'
import { ensureSchema, hasDb, sql } from '../../../lib/db'

export const dynamic = 'force-dynamic'

type ReviewRecord = { name?: unknown }

function validBatch(value: unknown): value is { reviews: ReviewRecord[]; reviewStatuses?: unknown; version?: unknown } {
  if (!value || typeof value !== 'object') return false
  const reviews = (value as { reviews?: unknown }).reviews
  if (!Array.isArray(reviews) || reviews.length < 1 || reviews.length > 173) return false
  const names = new Set<string>()
  for (const review of reviews) {
    if (!review || typeof review.name !== 'string' || !/^keeper_[a-z0-9_]+$/.test(review.name) || names.has(review.name)) return false
    names.add(review.name)
  }
  return true
}

/**
 * A durable, non-destructive reviewer handoff queue. The public review page
 * submits browser-local decisions here; later Codex work reads the exact-name
 * payload before proposing any reversible production draft or promotion.
 */
export async function POST(req: Request) {
  if (!hasDb()) return NextResponse.json({ error: 'review handoff is unavailable because no database is configured' }, { status: 503 })
  const body: unknown = await req.json().catch(() => null)
  if (!validBatch(body)) return NextResponse.json({ error: 'invalid review handoff batch' }, { status: 400 })
  await ensureSchema()
  const id = randomUUID()
  const payload = JSON.stringify(body)
  const rows = (await sql()`insert into keeper_review_handoffs (id, review, animation_count, source) values (${id}, ${payload}::jsonb, ${body.reviews.length}, 'keeper-review') returning submitted_at`) as { submitted_at: string }[]
  return NextResponse.json({ ok: true, handoff: { id, animationCount: body.reviews.length, submittedAt: rows[0]?.submitted_at } })
}

/** The latest queue entries are intentionally readable by a future Codex task. */
export async function GET() {
  if (!hasDb()) return NextResponse.json({ db: false, handoffs: [] })
  await ensureSchema()
  const rows = (await sql()`select id, review, animation_count, source, submitted_at from keeper_review_handoffs order by submitted_at desc limit 20`) as { id: string; review: unknown; animation_count: number; source: string; submitted_at: string }[]
  return NextResponse.json({
    db: true,
    handoffs: rows.map((row) => ({ id: row.id, review: row.review, animationCount: row.animation_count, source: row.source, submittedAt: row.submitted_at })),
  })
}
