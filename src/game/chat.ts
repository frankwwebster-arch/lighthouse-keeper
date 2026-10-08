/**
 * THE KEEPER'S CHAT. Now and then he asks Ralph an everyday question, chosen
 * by the real day and time ("How was school?" on a weekday afternoon, "How was
 * your football match?" on a Saturday). What Ralph types back is sorted into a
 * few kinds (good, bad, a food, a score…) and met with a fixed, pre-written
 * reply. No AI.
 */

import { normalise } from './matcher'

export interface Moment {
  /** 0 = Sunday … 6 = Saturday. */
  day: number
  /** Hours as a decimal: 15.5 = half past three. */
  hour: number
}
export const momentOf = (d: Date): Moment => ({ day: d.getDay(), hour: d.getHours() + d.getMinutes() / 60 })

export interface ChatQ {
  id: string
  text: string
  when: (m: Moment) => boolean
  /** How it is answered, by the kind of thing Ralph said. */
  replies: { pos: string; neg: string; neutral: string; food?: string; score?: Record<'win' | 'lose' | 'draw' | 'none', string>; fallback: string }
}

const weekday = (m: Moment) => m.day >= 1 && m.day <= 5
const weekend = (m: Moment) => m.day === 0 || m.day === 6
const between = (m: Moment, a: number, b: number) => m.hour >= a && m.hour < b

const generic = { neutral: 'Ah, fair enough. Every day is a bit different.', fallback: 'Hmm! I will have a good think about that.' }

export const CHATS: readonly ChatQ[] = [
  { id: 'how-are-you', text: 'How are you today?', when: () => true, replies: { ...generic, pos: 'Marvellous! That makes two of us.', neg: 'Oh no. Never mind. A cuppa and a biscuit will help. For me, anyway.' } },
  { id: 'school-after', text: 'How was school today?', when: (m) => weekday(m) && between(m, 15, 19.5), replies: { ...generic, pos: 'Brilliant! I knew you were a clever one.', neg: 'Oh dear. Tomorrow will be better. They always are.', fallback: 'Mmm, sounds like a proper school day!' } },
  { id: 'school-before', text: 'Are you off to school soon? Have you had your breakfast?', when: (m) => weekday(m) && between(m, 6, 8.75), replies: { ...generic, pos: 'Good! A full tummy makes a full brain.', neg: 'Eat something! Toast, at least. I make very good toast.', food: 'Mmm, {food}! A proper breakfast.', fallback: 'Right-o. Do not forget your bag!' } },
  { id: 'lunch', text: 'What did you have for lunch?', when: (m) => between(m, 12, 15), replies: { ...generic, pos: 'Lovely. I had a sandwich with the crusts on.', neg: 'Oh no. Was it the sort with sprouts?', food: 'Mmm, {food}! Now I am hungry.', fallback: 'Ooh, interesting. I wish I had had some.' } },
  { id: 'dinner-soon', text: 'What are you having for dinner tonight?', when: (m) => between(m, 14.5, 18), replies: { ...generic, pos: 'Lovely. Save me a bit.', neg: 'Not a favourite? There is always toast.', food: 'Mmm, {food}! Lucky you.', fallback: 'Sounds tasty. Do not tell the cat.' } },
  { id: 'dinner-done', text: 'What did you have for dinner?', when: (m) => between(m, 18, 21), replies: { ...generic, pos: 'Lovely. A good dinner makes a good night.', neg: 'Oh dear. I hope there was pudding.', food: 'Mmm, {food}! Was there pudding?', fallback: 'Sounds tasty. I had toast. Again.' } },
  { id: 'football', text: 'How was your football match this morning?', when: (m) => m.day === 6 && between(m, 12, 18), replies: { ...generic, pos: 'Brilliant! Did you score? I bet you did.', neg: 'Oh no! Unlucky. There is always next week.', score: { win: 'YES! A win! Hip hip hooray! Tell me everything!', lose: 'Oh, unlucky! It is only a game. Chin up!', draw: 'A draw! Well. Nobody lost, which is something.', none: 'Not a football day then? Fair enough. Plenty of other fun to be had.' }, fallback: 'Sounds exciting! I always wanted to be a goalkeeper.' } },
  { id: 'sunday-fun', text: 'Did you do anything fun this morning?', when: (m) => m.day === 0 && between(m, 12, 18), replies: { ...generic, pos: 'Brilliant! I love a fun morning.', neg: 'Oh dear. A lazy afternoon, then?', fallback: 'Ooh, interesting! Tell me more next time.' } },
  { id: 'weekend-plans', text: 'Got any plans for the weekend?', when: (m) => (m.day === 5 && m.hour >= 15) || (weekend(m) && between(m, 6, 12)), replies: { ...generic, pos: 'Brilliant! Make it a good one.', neg: 'Oh. Well, you can always come and visit the lighthouse.', fallback: 'Sounds good. I will be here. I am always here.' } },
  { id: 'best-thing', text: 'What was the best thing that happened today?', when: (m) => between(m, 12, 21), replies: { ...generic, pos: 'Ooh, lovely. Keep hold of that one.', neg: 'Oh dear. Tomorrow, then.', fallback: 'That is a good one. I will remember it.' } },
  { id: 'bedtime', text: 'Is it nearly your bedtime?', when: (m) => between(m, 18.5, 21.5), replies: { ...generic, pos: 'Good plan. Sleep tight!', neg: 'I know, bedtimes are the worst. Mine is 8 o\'clock, no arguments.', fallback: 'Well, do not stay up too late. The lighthouse will still be here.' } },
  { id: 'reading', text: 'Have you read anything good lately?', when: () => true, replies: { ...generic, pos: 'Excellent! I love a good book.', neg: 'Oh. Maybe try a different one? There is a book for everyone.', fallback: 'I will read it next, I think.' } },
  { id: 'favourite-animal', text: 'What is your favourite animal?', when: () => true, replies: { ...generic, pos: 'Ooh, good choice. {pet} is a bit jealous.', neg: 'Fair enough. Not everybody likes animals.', fallback: 'Great choice. Mine is {pet}, obviously.' } },
]

const POS = /\b(good|great|fun|amazing|brilliant|ace|awesome|fine|well|nice|best|happy|yes|yeah|yep|cool|lovely|excellent|loved|love|super|fantastic|brill|epic|wicked)\b/
const NEG = /\b(bad|boring|tired|sad|rubbish|awful|hard|horrible|terrible|no|nope|worst|angry|cross|poor|hated|hate|nothing)\b/
const WIN = /\b(won|win|winning|scored|score|goal|goals|hat trick|hat-trick)\b/
const LOSE = /\b(lost|lose|losing|beat us|beaten|thrashed)\b/
const DRAW = /\b(drew|draw|drawn|tied|nil nil|nil-nil)\b/
const NOGAME = /\b(didnt|did not|no match|cancelled|rained off|no game|wasnt|was not)\b/
const FOODS = /\b(pizza|pasta|spaghetti|sausages?|chips|burger|burgers|chicken|rice|curry|fish|soup|sandwich|sandwiches|toast|cereal|eggs?|beans|noodles|cheese|pancakes|nuggets|fajitas|lasagne|roast|pie|jacket potato|porridge|wrap|baguette|salad|fish fingers|macaroni)\b/

/** Pick a question for this moment. `skip` is the ids asked lately; `n` is a number that varies, to pick among several. */
export function pickChat(m: Moment, skip: readonly string[] = [], n = 0): ChatQ {
  const fits = CHATS.filter((c) => c.when(m))
  const fresh = fits.filter((c) => !skip.includes(c.id))
  const pool = fresh.length ? fresh : fits
  // The more specific questions (those that are tied to the time of day) come first.
  const special = pool.filter((c) => c.id !== 'how-are-you' && c.id !== 'reading' && c.id !== 'favourite-animal' && c.id !== 'best-thing')
  const from = special.length && n % 3 !== 0 ? special : pool
  return from[Math.abs(Math.trunc(n)) % from.length]
}

/** What he says back to what Ralph typed. */
export function replyToChat(q: ChatQ, text: string, fillers: { pet: string; name: string } = { pet: 'the cat', name: 'the keeper' }): { line: string; good: boolean } {
  const said = normalise(text)
  const fill = (s: string, food?: string) => s.replace('{pet}', fillers.pet).replace('{name}', fillers.name).replace('{food}', food ?? 'that')
  const r = q.replies
  const food = said.match(FOODS)?.[0]
  if (food && r.food) return { line: fill(r.food, food), good: true }
  if (r.score) {
    if (WIN.test(said)) return { line: fill(r.score.win), good: true }
    if (LOSE.test(said)) return { line: fill(r.score.lose), good: false }
    if (DRAW.test(said)) return { line: fill(r.score.draw), good: true }
    if (NOGAME.test(said)) return { line: fill(r.score.none), good: true }
  }
  const neg = NEG.test(said)
  const pos = POS.test(said)
  if (neg && !pos) return { line: fill(r.neg), good: false }
  if (pos && !neg) return { line: fill(r.pos), good: true }
  if (said.length <= 3 || /^(ok|okay|alright|so so|not bad|meh)$/.test(said)) return { line: fill(r.neutral), good: true }
  return { line: fill(r.fallback), good: true }
}
