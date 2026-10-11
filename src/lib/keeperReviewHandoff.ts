export type HandoffReview = { name: string; updatedAt?: unknown; [key: string]: unknown }

function canonicalValue(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalValue)
  if (!value || typeof value !== 'object') return value
  return Object.fromEntries(
    Object.entries(value as Record<string, unknown>)
      .sort(([left], [right]) => left.localeCompare(right))
      .map(([key, item]) => [key, canonicalValue(item)]),
  )
}

/**
 * A handoff's timestamp describes when it was saved, not a production request.
 * Compare all other review data by exact animation name so future Codex work can
 * concentrate on only the records whose actual decision or notes changed.
 */
function comparableReview(review: HandoffReview): string {
  const { name: _name, updatedAt: _updatedAt, ...decision } = review
  return JSON.stringify(canonicalValue(decision))
}

export function changedReviewNames(current: HandoffReview[], previous?: HandoffReview[]): string[] {
  if (!previous) return current.map((review) => review.name).sort((left, right) => left.localeCompare(right))
  const previousByName = new Map(previous.map((review) => [review.name, comparableReview(review)]))
  return current
    .filter((review) => previousByName.get(review.name) !== comparableReview(review))
    .map((review) => review.name)
    .sort((left, right) => left.localeCompare(right))
}
