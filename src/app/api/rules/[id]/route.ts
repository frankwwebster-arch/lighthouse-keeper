import { NextResponse } from 'next/server'
import { ensureSchema, hasDb, pinOk, sql, validId } from '../../../../lib/db'

export const dynamic = 'force-dynamic'

const clampNum = (v: unknown, lo: number, hi: number, d: number) => (typeof v === 'number' && Number.isFinite(v) ? Math.min(hi, Math.max(lo, Math.round(v))) : d)

/** Keeps only sensible values, so a bad request cannot break the game. */
function clean(r: Record<string, unknown>) {
  const prices: Record<string, number> = {}
  if (r.prices && typeof r.prices === 'object') for (const [k, v] of Object.entries(r.prices as Record<string, unknown>)) if (/^[a-z]{2,20}$/.test(k)) prices[k] = clampNum(v, 0, 999, 0)
  return {
    allowanceBase: clampNum(r.allowanceBase, 0, 999, 8),
    allowanceBonus: clampNum(r.allowanceBonus, 0, 999, 20),
    firstDay: clampNum(r.firstDay, 0, 999, 20),
    carryCap: clampNum(r.carryCap, 0, 999, 40),
    greenAt: clampNum(r.greenAt, 10, 95, 50),
    priceScale: clampNum(r.priceScale, 25, 300, 100),
    quizLevel: clampNum(r.quizLevel, 1, 3, 1),
    prices,
  }
}

export async function GET(_req: Request, { params }: { params: { id: string } }) {
  if (!hasDb() || !validId(params.id)) return NextResponse.json({ rules: null })
  await ensureSchema()
  const rows = (await sql()`select rules from player_rules where player_id = ${params.id}`) as { rules: unknown }[]
  return NextResponse.json({ rules: rows[0]?.rules ?? null })
}

/** Changing a player's dials needs the grown-ups' PIN. */
export async function PUT(req: Request, { params }: { params: { id: string } }) {
  if (!hasDb() || !validId(params.id)) return NextResponse.json({ error: 'no' }, { status: 400 })
  const body = (await req.json().catch(() => ({}))) as { pin?: unknown; rules?: Record<string, unknown> }
  await ensureSchema()
  if (!(await pinOk(body.pin))) return NextResponse.json({ error: 'wrong pin' }, { status: 403 })
  const rules = JSON.stringify(clean(body.rules ?? {}))
  await sql()`insert into player_rules (player_id, rules) values (${params.id}, ${rules}::jsonb) on conflict (player_id) do update set rules = excluded.rules`
  return NextResponse.json({ ok: true })
}
