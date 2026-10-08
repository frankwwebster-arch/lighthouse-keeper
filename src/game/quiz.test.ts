import { describe, expect, it } from 'vitest'
import { checkAnswer, makeQuiz, numberFrom } from './quiz'

describe('quiz', () => {
  it('always makes a question that its own answer satisfies', () => {
    let seed = 1
    const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647)
    for (let i = 0; i < 300; i++) {
      const q = makeQuiz(rand)
      expect(q.text.length).toBeGreaterThan(3)
      expect(checkAnswer(q, q.answers[0]), q.text).toBe(true)
    }
  })
  it('harder levels always make answerable questions', () => {
    for (const level of [2, 3]) {
      let seed = 5 + level
      const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647)
      const seen = new Set<string>()
      for (let i = 0; i < 400; i++) {
        const q = makeQuiz(rand, undefined, [], level)
        seen.add(q.kind)
        expect(checkAnswer(q, q.answers[0]), q.text).toBe(true)
        expect(checkAnswer(q, q.show), q.text).toBe(true)
        expect(Number.isFinite(Number(q.answers[0])) || !q.numeric, q.text).toBe(true)
      }
      expect(seen.size).toBeGreaterThan(3)
    }
  })
  it('reads numbers as words', () => {
    expect(numberFrom('forty two')).toBe(42)
    expect(numberFrom('42')).toBe(42)
  })
  it('rejects a wrong number', () => {
    const q = makeQuiz(() => 0.3)
    if (q.numeric) expect(checkAnswer(q, '9999')).toBe(false)
  })
})
