/**
 * THE READER. Turns what Ralph typed into jobs from the command book
 * (`commands.ts`). No AI: it works by lining his words up against the book's
 * phrases, forgiving the odd typo.
 *
 *   sure   (a clear match, even with a small slip)  → he just does it
 *   maybe  (a near miss)                            → "I'm not sure what 'fishig' means. Did you mean 'go fishing'?"
 *   nothing                                         → a shrug
 *
 * Several jobs can be chained: "make toast then play the piano".
 */

import { COMMANDS, FOOD_WORDS, type CommandDef, type DoOrder } from './commands'
import { GAME, INTERACTIONS } from './config'

export type MatchResult =
  | { kind: 'do'; doing: DoOrder[] }
  | { kind: 'ask'; doing: DoOrder[]; say: string; heard: string }
  | { kind: 'shrug' }
  | { kind: 'empty' }

/** Lower case, no punctuation, single spaces. */
export function normalise(text: string): string {
  return text
    .toLowerCase()
    .replace(/[’`']/g, '')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
    .slice(0, GAME.match.maxChars)
}

/** Take the common endings off a longer word: "fishing", "fished", "fishes" and "fish" all meet in the middle. */
export function stem(word: string): string {
  if (word.length <= 3) return word
  if (word.length === 4) return word.endsWith('e') ? word.slice(0, -1) : word
  for (const end of ['ing', 'ed', 'es', 's', 'e']) {
    if (word.endsWith(end) && word.length - end.length >= 3) return word.slice(0, -end.length)
  }
  return word
}

/** How many single-letter slips (add, drop, change, swap two neighbours) turn `a` into `b`. */
export function distance(a: string, b: string): number {
  const d: number[][] = []
  for (let i = 0; i <= a.length; i++) d[i] = [i]
  for (let j = 0; j <= b.length; j++) d[0][j] = j
  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1)
    }
  }
  return d[a.length][b.length]
}

export const similarity = (a: string, b: string) => (a === b ? 1 : 1 - distance(a, b) / Math.max(a.length, b.length))

interface Entry {
  cmd: CommandDef
  words: string[]
  joined: string
  /** The same phrase as typed, with no endings taken off. */
  rawJoined: string
  letters: number
}

let book: Entry[] | null = null
function entries(): Entry[] {
  if (book) return book
  book = []
  for (const cmd of COMMANDS) {
    for (const phrase of cmd.phrases) {
      const raw = normalise(phrase).split(' ').filter(Boolean)
      const words = raw.map(stem)
      if (!words.length) continue
      book.push({ cmd, words, joined: words.join(''), rawJoined: raw.join(''), letters: words.join('').length })
    }
  }
  return book
}

interface Best {
  cmd: CommandDef
  score: number
  size: number
}

/** The phrase in the book that lines up best with these words. A longer phrase beats a shorter one at the same score. */
function best(tokens: string[]): Best | null {
  const stems = tokens.map(stem)
  let top: Best | null = null
  for (const e of entries()) {
    const m = e.words.length
    for (let i = 0; i + m <= stems.length; i++) {
      const win = stems.slice(i, i + m)
      let score = 0
      if (win.every((w, k) => w === e.words[k])) score = 1
      else if (e.letters >= GAME.match.fuzzyMinLetters) {
        const typed = tokens.slice(i, i + m).join('')
        const s = Math.max(similarity(win.join(''), e.joined), similarity(typed, e.rawJoined))
        // A fuzzy match must keep the first letter: "cool" is not "pool".
        if (s >= GAME.match.maybe && win.join('')[0] === e.joined[0]) score = s
      }
      if (score === 0) continue
      const size = e.letters
      if (!top || score > top.score || (score === top.score && size > top.size)) top = { cmd: e.cmd, score, size }
    }
  }
  return top
}

/** A food word in what he typed ("cook pasta"), so the job can use that one. */
function foodIn(tokens: string[]): string | undefined {
  for (const t of tokens) if (FOOD_WORDS[t]) return FOOD_WORDS[t]
  return undefined
}

/** A last chance: a single word that is one of an action's own keywords ("snack", "fishing"), in a short message. */
function spot(tokens: string[]): CommandDef | null {
  if (tokens.length > 4) return null
  for (const t of tokens.map(stem)) {
    for (const a of INTERACTIONS) {
      if (a.keywords.some((k) => !k.includes(' ') && stem(k) === t)) {
        const found = COMMANDS.find((c) => c.doing.some((d) => d.id === a.id))
        if (found) return found
      }
    }
  }
  return null
}

function withFood(doing: readonly DoOrder[], tokens: string[]): DoOrder[] {
  const item = foodIn(tokens)
  return doing.map((d) => (item && (d.id === 'fridge_snack' || d.id === 'cooker_cook') ? { ...d, item } : { ...d }))
}

/** Read what he typed. */
export function read(text: string): MatchResult {
  const said = normalise(text)
  if (!said) return { kind: 'empty' }
  const clauses = said.split(/\b(?:and then|then|after that|and)\b/).map((c) => c.trim()).filter(Boolean)
  const doing: DoOrder[] = []
  const asks: { say: string; heard: string }[] = []
  for (const clause of clauses) {
    const tokens = clause.split(' ')
    const top = best(tokens)
    if (top && top.score >= GAME.match.sure) {
      doing.push(...withFood(top.cmd.doing, tokens))
    } else if (top) {
      doing.push(...withFood(top.cmd.doing, tokens))
      asks.push({ say: top.cmd.say, heard: clause })
    } else {
      const kw = spot(tokens)
      if (kw) doing.push(...withFood(kw.doing, tokens))
    }
  }
  if (!doing.length) return { kind: 'shrug' }
  const limited = doing.slice(0, GAME.queueLimit)
  if (asks.length) return { kind: 'ask', doing: limited, say: asks.map((a) => a.say).join(', then '), heard: asks[0].heard }
  return { kind: 'do', doing: limited }
}

const YES = new Set(['y', 'yes', 'yeah', 'yep', 'yup', 'yea', 'ok', 'okay', 'sure', 'aye', 'correct', 'right', 'please', 'yes please', 'that one', 'thats right', 'do it'])
const NO = new Set(['n', 'no', 'nope', 'nah', 'nay', 'wrong', 'no thanks', 'not that', 'cancel'])
export const isYes = (text: string) => YES.has(normalise(text))
export const isNo = (text: string) => NO.has(normalise(text))
