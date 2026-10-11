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
type HandoffStatus = 'queued' | 'processing' | 'completed'
type HandoffRow = { id: string; review: unknown; animation_count: number; source: string; submitted_at: string; status: HandoffStatus; processing_started_at: string | null; completed_at: string | null; processing_note: string }

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
  const rows = (await sql()`insert into keeper_review_handoffs (id, review, animation_count, source, status) values (${id}, ${payload}::jsonb, ${body.reviews.length}, 'keeper-review', 'queued') returning submitted_at`) as { submitted_at: string }[]
  return NextResponse.json({ ok: true, handoff: { id, animationCount: body.reviews.length, changedAnimationCount: changedAnimationNames.length, changedAnimationNames, comparedToHandoffId: latest[0]?.id ?? null, comparisonBaseline, submittedAt: rows[0]?.submitted_at } })
}

/** Claim before draft work; complete after delivery, or release if no work was started. */
export async function PATCH(req: Request) {
  if (!hasDb()) return NextResponse.json({ error: 'review handoff is unavailable because no database is configured' }, { status: 503 })
  const body: unknown = await req.json().catch(() => null)
  if (!body || typeof body !== 'object') return NextResponse.json({ error: 'invalid handoff status update' }, { status: 400 })
  const { id, action, note } = body as { id?: unknown; action?: unknown; note?: unknown }
  if (typeof id !== 'string' || !/^[0-9a-f-]{36}$/i.test(id) || (action !== 'claim' && action !== 'complete' && action !== 'release')) return NextResponse.json({ error: 'invalid handoff status update' }, { status: 400 })
  if (note !== undefined && (typeof note !== 'string' || note.length > 1000)) return NextResponse.json({ error: 'invalid handoff status note' }, { status: 400 })
  await ensureSchema()
  const nextStatus: HandoffStatus = action === 'claim' ? 'processing' : action === 'complete' ? 'completed' : 'queued'
  const rows = (await sql()`update keeper_review_handoffs set status = ${nextStatus}, processing_started_at = case when ${action} = 'claim' then now() when ${action} = 'release' then null else processing_started_at end, completed_at = case when ${action} = 'complete' then now() else null end, processing_note = ${typeof note === 'string' ? note : ''} where id = ${id} and status = ${action === 'claim' ? 'queued' : 'processing'} returning id, status, animation_count, processing_started_at, completed_at`) as { id: string; status: HandoffStatus; animation_count: number; processing_started_at: string | null; completed_at: string | null }[]
  if (!rows.length) return NextResponse.json({ error: action === 'claim' ? 'handoff is no longer available to claim' : 'handoff is not currently processing' }, { status: 409 })
  const row = rows[0]
  return NextResponse.json({ ok: true, handoff: { id: row.id, status: row.status, animationCount: row.animation_count, processingStartedAt: row.processing_started_at, completedAt: row.completed_at } })
}

/** The latest queue entries are intentionally readable by a future Codex task. */
export async function GET() {
  if (!hasDb()) return NextResponse.json({ db: false, handoffs: [] })
  await ensureSchema()
  const rows = (await sql()`select id, review, animation_count, source, submitted_at, status, processing_started_at, completed_at, processing_note from keeper_review_handoffs order by submitted_at desc limit 20`) as HandoffRow[]
  const processing = rows.find((row) => row.status === 'processing')
  return NextResponse.json({
    db: true,
    processingHandoff: processing ? { id: processing.id, animationCount: processing.animation_count, startedAt: processing.processing_started_at, note: processing.processing_note } : null,
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
        status: row.status,
        processingStartedAt: row.processing_started_at,
        completedAt: row.completed_at,
        processingNote: row.processing_note,
      }
    }),
  })
}
