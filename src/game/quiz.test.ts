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
  it('reads numbers as words', () => {
    expect(numberFrom('forty two')).toBe(42)
    expect(numberFrom('42')).toBe(42)
  })
  it('rejects a wrong number', () => {
    const q = makeQuiz(() => 0.3)
    if (q.numeric) expect(checkAnswer(q, '9999')).toBe(false)
  })
})
