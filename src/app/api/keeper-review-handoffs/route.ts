import { randomUUID } from 'node:crypto'
import { NextResponse } from 'next/server'
import { ensureSchema, hasDb, sql } from '../../../lib/db'
import { changedReviewNames, type HandoffReview } from '../../../lib/keeperReviewHandoff'

export const dynamic = 'force-dynamic'

type ReviewBatch = { reviews: HandoffReview[]; baselineReviews?: HandoffReview[]; reviewStatuses?: unknown; version?: unknown; [key: string]: unknown }
type StoredReviewBatch = ReviewBatch & {
  handoffDelta: {
    changedAnimationNames: string[]
    comparedToHandoffId: string | null
    comparisonBaseline: 'initial-review' | 'previous-handoff'
  }
}

function validBatch(value: unknown): value is ReviewBatch {
  if (!value || typeof value !== 'object') return false
  const reviews = (value as { reviews?: unknown }).reviews
  if (!Array.isArray(reviews) || reviews.length < 1 || reviews.length > 173) return false
  const names = new Set<string>()
  for (const review of reviews) {
    if (!review || typeof review.name !== 'string' || !/^keeper_[a-z0-9_]+$/.test(review.name) || names.has(review.name)) return false
    names.add(review.name)
  }
  const baselineReviews = (value as { baselineReviews?: unknown }).baselineReviews
  if (baselineReviews !== undefined && (!Array.isArray(baselineReviews) || baselineReviews.length !== reviews.length)) return false
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
  const latest = (await sql()`select id, review from keeper_review_handoffs order by submitted_at desc limit 1`) as { id: string; review: unknown }[]
  const previous = latest[0]?.review as Partial<ReviewBatch> | undefined
  const previousReviews = Array.isArray(previous?.reviews) ? previous.reviews as HandoffReview[] : undefined
  const initialReviews = !previousReviews && Array.isArray(body.baselineReviews) ? body.baselineReviews : undefined
  const comparisonBaseline = previousReviews ? 'previous-handoff' : 'initial-review'
  const changedAnimationNames = changedReviewNames(body.reviews, previousReviews ?? initialReviews)
  const { baselineReviews: _baselineReviews, ...snapshot } = body
  const stored: StoredReviewBatch = {
    ...snapshot,
    handoffDelta: { changedAnimationNames, comparedToHandoffId: latest[0]?.id ?? null, comparisonBaseline },
  }
  const payload = JSON.stringify(stored)
  const rows = (await sql()`insert into keeper_review_handoffs (id, review, animation_count, source) values (${id}, ${payload}::jsonb, ${body.reviews.length}, 'keeper-review') returning submitted_at`) as { submitted_at: string }[]
  return NextResponse.json({ ok: true, handoff: { id, animationCount: body.reviews.length, changedAnimationCount: changedAnimationNames.length, changedAnimationNames, comparedToHandoffId: latest[0]?.id ?? null, comparisonBaseline, submittedAt: rows[0]?.submitted_at } })
}

/** The latest queue entries are intentionally readable by a future Codex task. */
export async function GET() {
  if (!hasDb()) return NextResponse.json({ db: false, handoffs: [] })
  await ensureSchema()
  const rows = (await sql()`select id, review, animation_count, source, submitted_at from keeper_review_handoffs order by submitted_at desc limit 20`) as { id: string; review: unknown; animation_count: number; source: string; submitted_at: string }[]
  return NextResponse.json({
    db: true,
    handoffs: rows.map((row) => {
      const delta = (row.review as Partial<StoredReviewBatch> | null)?.handoffDelta
      const changedAnimationNames = Array.isArray(delta?.changedAnimationNames) ? delta.changedAnimationNames : null
      return {
        id: row.id,
        review: row.review,
        animationCount: row.animation_count,
        // Pre-delta historical batches are recoverable snapshots, but must not
        // wake the checker as though every animation were newly changed.
        changedAnimationCount: changedAnimationNames?.length ?? null,
        changedAnimationNames,
        comparedToHandoffId: typeof delta?.comparedToHandoffId === 'string' ? delta.comparedToHandoffId : null,
        comparisonBaseline: delta?.comparisonBaseline === 'initial-review' || delta?.comparisonBaseline === 'previous-handoff' ? delta.comparisonBaseline : null,
        source: row.source,
        submittedAt: row.submitted_at,
      }
    }),
  })
}
