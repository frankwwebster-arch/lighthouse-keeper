/**
 * THE KEEPER'S QUESTIONS FOR RALPH. Times tables, sums, word problems,
 * spelling and general knowledge, for a bright seven-year-old. All made or
 * looked up here: no AI. `makeQuiz` takes a random-number function so it can
 * be tested.
 */

import { normalise, similarity } from './matcher'

export type QuizKind = 'times' | 'divide' | 'sum' | 'bonds' | 'word' | 'spelling' | 'knowledge'

export interface Quiz {
  id: string
  kind: QuizKind
  /** What the keeper says. */
  text: string
  /** What counts as right (already tidied). */
  answers: string[]
  /** What the keeper tells him if he gives up. */
  show: string
  /** A nudge after a wrong try. */
  hint: string
  numeric: boolean
}

type Rand = () => number
const pick = <T,>(list: readonly T[], rand: Rand): T => list[Math.min(list.length - 1, Math.floor(rand() * list.length))]
const between = (lo: number, hi: number, rand: Rand) => lo + Math.floor(rand() * (hi - lo + 1))

// ─── Numbers in words ────────────────────────────────────────────────────────

const ONES = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
const TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

/** "42", "forty two", "forty-two" → 42. Anything else → null. */
export function numberFrom(text: string): number | null {
  const t = normalise(text)
  if (/^-?\d+$/.test(t)) return Number(t)
  let total = 0
  let seen = false
  for (const w of t.split(' ')) {
    if (w === 'and') continue
    const o = ONES.indexOf(w)
    const tn = TENS.indexOf(w)
    if (o >= 0) { total += o; seen = true }
    else if (tn >= 2) { total += tn * 10; seen = true }
    else if (w === 'hundred') { total = (total || 1) * 100; seen = true }
    else return null
  }
  return seen ? total : null
}

export function numberWords(n: number): string {
  if (n < 20) return ONES[n]
  if (n < 100) return TENS[Math.floor(n / 10)] + (n % 10 ? ' ' + ONES[n % 10] : '')
  return String(n)
}

// ─── The makers ──────────────────────────────────────────────────────────────

const num = (id: string, kind: QuizKind, text: string, answer: number, hint: string): Quiz => ({ id, kind, text, answers: [String(answer)], show: String(answer), hint, numeric: true })

/** The tables he is working on get asked more: 6, 7, 8 and 9. */
const TABLE_WEIGHTED = [2, 3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 11, 12]

function times(rand: Rand): Quiz {
  const a = pick(TABLE_WEIGHTED, rand)
  const b = between(2, 12, rand)
  return num(`times-${a}x${b}`, 'times', `What is ${a} times ${b}?`, a * b, `Think of ${a} groups of ${b}. Or count up in ${Math.min(a, b)}s.`)
}

function divide(rand: Rand): Quiz {
  const a = pick(TABLE_WEIGHTED, rand)
  const b = between(2, 12, rand)
  return num(`div-${a * b}/${a}`, 'divide', `What is ${a * b} divided by ${a}?`, b, `How many ${a}s fit into ${a * b}? Use your ${a} times table.`)
}

function sum(rand: Rand): Quiz {
  if (rand() < 0.5) {
    const a = between(11, 70, rand)
    const b = between(11, 99 - a, rand)
    return num(`add-${a}+${b}`, 'sum', `What is ${a} + ${b}?`, a + b, 'Add the tens first, then the ones.')
  }
  const a = between(30, 99, rand)
  const b = between(11, a - 5, rand)
  return num(`sub-${a}-${b}`, 'sum', `What is ${a} take away ${b}?`, a - b, 'Count back in tens first, then the ones.')
}

function bonds(rand: Rand): Quiz {
  const a = between(1, 19, rand) * 5
  return num(`bond-${a}`, 'bonds', `What do you add to ${a} to make 100?`, 100 - a, 'Think of how far it is to 100.')
}

function word(rand: Rand, who: { name: string; pet: string }): Quiz {
  const kind = between(0, 4, rand)
  if (kind === 0) {
    const a = between(3, 9, rand)
    const b = between(3, 9, rand)
    return num(`word-fish-${a}-${b}`, 'word', `I caught ${a} fish in the morning and ${b} fish in the afternoon. How many fish is that?`, a + b, 'Put the two lots together.')
  }
  if (kind === 1) {
    const sweets = between(2, 5, rand)
    const each = between(2, 5, rand)
    return num(`word-bags-${sweets}-${each}`, 'word', `There are ${sweets} bags of apples, with ${each} apples in each bag. How many apples is that?`, sweets * each, `That is ${sweets} groups of ${each}.`)
  }
  if (kind === 2) {
    const have = between(30, 90, rand)
    const cost = between(10, have - 5, rand)
    return num(`word-pence-${have}-${cost}`, 'word', `I have ${have}p. I buy a biscuit for ${cost}p. How much do I have left?`, have - cost, 'Take the price away from what you started with.')
  }
  if (kind === 3) {
    const total = between(3, 8, rand) * 2
    return num(`word-share-${total}`, 'word', `${who.pet} has ${total} fish treats and shares them out equally between ${who.pet} and me. How many do I get?`, total / 2, 'Half of the treats each.')
  }
  const lamps = between(2, 4, rand)
  return num(`word-lamps-${lamps}`, 'word', `A lighthouse has ${lamps} floors and each floor has 12 steps. How many steps is that?`, lamps * 12, `Count up in 12s, ${lamps} times.`)
}

/** [clue, word]: Year 2 to 4 spelling. He types the whole word. */
const SPELLINGS: readonly (readonly [string, string])[] = [
  ['the opposite of "small"', 'big'], ['the day after Monday', 'tuesday'], ['a baby cat', 'kitten'], ['what you hear with', 'ears'],
  ['a word for "very big"', 'enormous'], ['the thing we write with, made of wood', 'pencil'], ['we use it to look at the stars: a tele...', 'telescope'],
  ['what the sun does in the morning', 'rise'], ['a word for "pal" (starts with F)', 'friend'], ['the reason: "I like it ______ it is fun"', 'because'],
  ['the season after summer', 'autumn'], ['what you drink from a cow', 'milk'], ['the number after nineteen', 'twenty'], ['the colour of the sky on a sunny day', 'blue'],
  ['a very pretty thing is...', 'beautiful'], ['the opposite of "question"', 'answer'], ['the month after July', 'august'], ['a shiny thing that sits in the lamp room: a l...', 'lantern'],
  ['more than one child', 'children'], ['the opposite of "early"', 'late'], ['you do it with a book', 'read'], ['the thing that tells the time on your wrist', 'watch'],
  ['the place where ships come in', 'harbour'], ['a boat with sails', 'yacht'], ['a country: the one with the Eiffel Tower', 'france'], ['not easy', 'difficult'],
  ['what you do with a ball and a goal', 'score'], ['the day after Friday', 'saturday'], ['the opposite of "up"', 'down'], ['the person who flies a plane', 'pilot'],
]

function spelling(rand: Rand): Quiz {
  const [clue, answer] = pick(SPELLINGS, rand)
  return { id: `spell-${answer}`, kind: 'spelling', text: `Spell this word for me: ${clue}.`, answers: [answer], show: answer, hint: `It has ${answer.length} letters and starts with ${answer[0].toUpperCase()}.`, numeric: false }
}

const KNOWLEDGE: readonly (readonly [string, readonly string[], string])[] = [
  ['How many legs does a spider have?', ['8', 'eight'], 'Think of an octopus: octo means eight.'],
  ['What is the capital of France?', ['paris'], 'It has a very famous tower.'],
  ['Which planet is closest to the Sun?', ['mercury'], 'It is named after a messenger god.'],
  ['What colour do you get if you mix blue and yellow?', ['green'], 'Think of grass.'],
  ['How many days are there in a week?', ['7', 'seven'], 'Monday to Sunday.'],
  ['What does a caterpillar turn into?', ['butterfly', 'a butterfly', 'moth', 'a moth'], 'It has pretty wings.'],
  ['What is the biggest animal in the sea?', ['blue whale', 'whale', 'a whale', 'the blue whale'], 'It is a mammal, not a fish.'],
  ['How many sides does a hexagon have?', ['6', 'six'], 'Think of a honeycomb cell.'],
  ['What do you call frozen water?', ['ice'], 'Think of an ice lolly.'],
  ['What is the capital of England?', ['london'], 'Big Ben lives there.'],
  ['How many minutes are there in an hour?', ['60', 'sixty'], 'Count the minutes round a clock.'],
  ['How many months are there in a year?', ['12', 'twelve'], 'January to December.'],
  ['What do bees make?', ['honey'], 'It is sticky and sweet.'],
  ['What is the fastest animal on land?', ['cheetah', 'a cheetah', 'the cheetah'], 'It is a spotty big cat.'],
  ['What is the biggest planet in our solar system?', ['jupiter'], 'It has a great red spot.'],
  ['How many continents are there?', ['7', 'seven'], 'Africa, Antarctica, Asia, Australia, Europe and two Americas.'],
  ['What shape has three sides?', ['triangle', 'a triangle'], 'Tri means three.'],
  ['What is the tallest animal in the world?', ['giraffe', 'a giraffe', 'the giraffe'], 'It has a very long neck.'],
  ['Which season comes after summer?', ['autumn', 'fall'], 'The leaves fall off the trees.'],
  ['What do you call a baby dog?', ['puppy', 'a puppy', 'pup'], 'It is very waggy.'],
  ['What do we breathe in to stay alive?', ['oxygen', 'air'], 'Plants make it.'],
  ['What is the capital of Scotland?', ['edinburgh'], 'It has a famous castle on a hill.'],
  ['What is the capital of Wales?', ['cardiff'], 'It begins with C.'],
  ['How many players are in a football team on the pitch?', ['11', 'eleven'], 'Ten outfield players and a goalkeeper.'],
  ['What is the biggest ocean?', ['pacific', 'the pacific', 'pacific ocean', 'the pacific ocean'], 'It sounds like "peaceful".'],
  ['Who flies a plane?', ['pilot', 'a pilot', 'the pilot'], 'He sits in the cockpit.'],
  ['Which animal is known as the king of the jungle?', ['lion', 'a lion', 'the lion'], 'It has a big mane.'],
  ['How many legs does an insect have?', ['6', 'six'], 'Think of an ant.'],
  ['What is the opposite of north?', ['south'], 'Think of a compass.'],
  ['How many wheels does a tricycle have?', ['3', 'three'], 'Tri means three.'],
  ['What colour is a ripe banana?', ['yellow'], 'Think of a smiley face.'],
  ['What is the name of the planet we live on?', ['earth', 'the earth'], 'It is the third planet from the Sun.'],
  ['What bird cannot fly but loves the cold: a penguin or an eagle?', ['penguin', 'a penguin', 'the penguin'], 'It waddles on the ice.'],
  ['How many seconds are there in a minute?', ['60', 'sixty'], 'The same as the minutes in an hour.'],
  ['What do we call the line of lights that guides ships at night?', ['lighthouse', 'a lighthouse', 'the lighthouse', 'lighthouses'], 'Look around you!'],
  ['What is half of 100?', ['50', 'fifty'], 'Split it into two equal groups.'],
  ['Which is heavier: a feather or a brick?', ['brick', 'a brick', 'the brick'], 'Think about carrying them.'],
  ['What is the colour of a stop sign?', ['red'], 'It is also the colour of tomatoes.'],
  ['How many sides does a square have?', ['4', 'four'], 'Think of a window.'],
]

function knowledge(rand: Rand): Quiz {
  const [text, answers, hint] = pick(KNOWLEDGE, rand)
  const nums = answers.every((a) => /^\d+$/.test(a) || ONES.includes(a))
  return { id: `gk-${text.slice(0, 24)}`, kind: 'knowledge', text, answers: answers.map(normalise), show: answers[0], hint, numeric: nums }
}

const MAKERS: readonly { weight: number; make: (rand: Rand, who: { name: string; pet: string }) => Quiz }[] = [
  { weight: 5, make: times },
  { weight: 1.5, make: divide },
  { weight: 2, make: sum },
  { weight: 1, make: bonds },
  { weight: 2, make: word },
  { weight: 2, make: spelling },
  { weight: 3, make: knowledge },
]


// ─── Harder questions (for older players): levels 2 and 3 ────────────────────

const LEVEL = (min: 2 | 3, make: Maker) => ({ min, make })
type Maker = (rand: Rand, who: { name: string; pet: string }, level: number) => Quiz

const times2: Maker = (rand, _w, level) => {
  const a = level >= 3 ? between(13, 35, rand) : between(11, 19, rand)
  const b = level >= 3 ? between(3, 12, rand) : between(2, 9, rand)
  return num(`t2-${a}x${b}`, 'times', `What is ${a} times ${b}?`, a * b, `Split ${a} into tens and ones, times each, then add.`)
}
const divide2: Maker = (rand, _w, level) => {
  const a = level >= 3 ? between(12, 25, rand) : between(6, 12, rand)
  const b = level >= 3 ? between(6, 15, rand) : between(6, 15, rand)
  return num(`d2-${a * b}/${a}`, 'divide', `What is ${a * b} divided by ${a}?`, b, `How many ${a}s fit into ${a * b}?`)
}
const sum2: Maker = (rand, _w, level) => {
  const hi = level >= 3 ? 9999 : 899
  const lo = level >= 3 ? 1000 : 100
  const a = between(lo, hi, rand)
  const b = between(lo, hi, rand)
  if (rand() < 0.5) return num(`s2-${a}+${b}`, 'sum', `What is ${a} + ${b}?`, a + b, 'Add the ones, then the tens, hundreds and thousands, carrying as you go.')
  const [big, small] = a > b ? [a, b] : [b, a]
  return num(`s2-${big}-${small}`, 'sum', `What is ${big} take away ${small}?`, big - small, 'Take away in chunks: hundreds, then tens, then ones.')
}
const fraction: Maker = (rand, _w, level) => {
  const d = [2, 3, 4, 5, 8, 10][between(0, 5, rand)]
  const n = level >= 3 ? between(1, d - 1, rand) : 1
  const whole = d * between(2, 9, rand)
  return num(`fr-${n}/${d}-${whole}`, 'sum', `What is ${n}/${d} of ${whole}?`, (whole / d) * n, `Divide ${whole} by ${d}${n > 1 ? `, then times by ${n}` : ''}.`)
}
const percent: Maker = (rand) => {
  const p = [10, 20, 25, 50, 75][between(0, 4, rand)]
  const whole = between(2, 20, rand) * 20
  return num(`pc-${p}-${whole}`, 'sum', `What is ${p}% of ${whole}?`, (whole * p) / 100, p === 10 ? 'Divide by 10.' : p === 25 ? 'A quarter: halve it twice.' : p === 50 ? 'Half.' : 'Work out 10% first and build from there.')
}
const order: Maker = (rand) => {
  const a = between(2, 9, rand)
  const b = between(2, 9, rand)
  const c = between(2, 9, rand)
  return num(`op-${a}+${b}x${c}`, 'sum', `What is ${a} + ${b} × ${c}?`, a + b * c, 'Multiplication comes before addition.')
}
const squares: Maker = (rand) => {
  const a = between(6, 16, rand)
  return num(`sq-${a}`, 'times', `What is ${a} squared?`, a * a, `${a} times ${a}.`)
}
const area: Maker = (rand, _w, level) => {
  const a = between(3, level >= 3 ? 15 : 9, rand)
  const b = between(3, level >= 3 ? 15 : 9, rand)
  if (rand() < 0.5) return num(`area-${a}x${b}`, 'word', `A rectangle is ${a} cm long and ${b} cm wide. What is its area in square centimetres?`, a * b, 'Length times width.')
  return num(`per-${a}x${b}`, 'word', `A rectangle is ${a} cm long and ${b} cm wide. How far is it all the way round, in centimetres?`, 2 * (a + b), 'Add all four sides.')
}
const word2: Maker = (rand, who) => {
  const k = between(0, 2, rand)
  if (k === 0) {
    const n = between(3, 9, rand)
    const p = between(12, 48, rand)
    return num(`w2-pk-${n}-${p}`, 'word', `${n} packets of fish treats cost ${p}p each. How many pence is that altogether?`, n * p, `${n} lots of ${p}.`)
  }
  if (k === 1) {
    const parts = [3, 4, 6][between(0, 2, rand)]
    const total = between(4, 12, rand) * parts
    return num(`w2-sh-${total}-${parts}`, 'word', `${who.name} bakes ${total} biscuits and puts them equally into ${parts} tins. How many go in each tin?`, total / parts, `Share ${total} between ${parts}.`)
  }
  const had = between(200, 900, rand)
  const spent = between(50, had - 20, rand)
  return num(`w2-sp-${had}-${spent}`, 'word', `${who.name} had ${had} credits and spent ${spent}. How many are left?`, had - spent, 'Take away what was spent.')
}

const SPELLINGS_HARD: readonly (readonly [string, string])[] = [
  ['the day after Tuesday', 'wednesday'], ['the second month of the year', 'february'], ['you need it: it is ______ to wear a coat in snow', 'necessary'],
  ['to split into two: se...', 'separate'], ['a piece of land with sea all round it', 'island'], ['a place with lots of books', 'library'],
  ['what you know is your ______', 'knowledge'], ['the natural world around us', 'environment'], ['the beat in music', 'rhythm'],
  ['for sure: "I will ______ come"', 'definitely'], ['an amazing, exciting experience: an ad...', 'adventure'], ['to look after, protect', 'guard'],
  ['the opposite of "ancient"', 'modern'], ['a very strong wind and rain: a h...', 'hurricane'], ['someone who sails ships: a n...', 'navigator'],
  ['a light that warns ships: a b...', 'beacon'], ['a big wave of the sea that goes out and in: the t...', 'tide'], ['the person who looks after a lighthouse', 'keeper'],
]
const spelling2: Maker = (rand) => {
  const [clue, answer] = pick(SPELLINGS_HARD, rand)
  return { id: `spell2-${answer}`, kind: 'spelling', text: `Spell this word for me: ${clue}.`, answers: [answer], show: answer, hint: `It has ${answer.length} letters and starts with ${answer[0].toUpperCase()}.`, numeric: false }
}

const KNOWLEDGE_HARD: readonly (readonly [string, readonly string[], string])[] = [
  ['What is the capital of Italy?', ['rome'], 'Think of the Colosseum.'],
  ['What is the capital of Japan?', ['tokyo'], 'It is the biggest city in Japan.'],
  ['What is the capital of Australia?', ['canberra'], 'It is not Sydney!'],
  ['How many planets are in our solar system?', ['8', 'eight'], 'Mercury to Neptune.'],
  ['What force pulls everything towards the ground?', ['gravity'], 'Newton and the apple.'],
  ['What gas do plants take in from the air?', ['carbon dioxide', 'co2'], 'We breathe it out.'],
  ['How many degrees are there in a right angle?', ['90', 'ninety'], 'The corner of a square.'],
  ['What do we call an animal that only eats plants?', ['herbivore', 'a herbivore'], 'Think of a cow.'],
  ['Who wrote the play Romeo and Juliet?', ['shakespeare', 'william shakespeare'], 'He was born in Stratford.'],
  ['How many sides does an octagon have?', ['8', 'eight'], 'Think of a stop sign.'],
  ['At what temperature in Celsius does water freeze?', ['0', 'zero'], 'Ice.'],
  ['Which planet is known as the Red Planet?', ['mars'], 'Named after a Roman god of war.'],
  ['What is the largest desert in Africa?', ['sahara', 'the sahara', 'sahara desert'], 'It starts with S.'],
  ['What is the chemical symbol for water?', ['h2o'], 'Two hydrogens and one oxygen.'],
  ['What do we call the layer of gas around the Earth?', ['atmosphere', 'the atmosphere'], 'It starts with A.'],
  ['How many bones does an adult human have, roughly: 106, 206 or 306?', ['206', 'two hundred and six'], 'The middle one.'],
  ['What is the Roman numeral for 10?', ['x'], 'It looks like a cross.'],
  ['Which ocean lies between Europe and America?', ['atlantic', 'the atlantic', 'atlantic ocean', 'the atlantic ocean'], 'It starts with A.'],
]
const knowledge2: Maker = (rand) => {
  const [text, answers, hint] = pick(KNOWLEDGE_HARD, rand)
  const nums = answers.every((a) => /^\d+$/.test(a) || ONES.includes(a))
  return { id: `gk2-${text.slice(0, 24)}`, kind: 'knowledge', text, answers: answers.map(normalise), show: answers[0], hint, numeric: nums }
}

const HARDER: readonly { weight: number; min: 2 | 3; make: Maker }[] = [
  { weight: 4, ...LEVEL(2, times2) },
  { weight: 2, ...LEVEL(2, divide2) },
  { weight: 3, ...LEVEL(2, sum2) },
  { weight: 2, ...LEVEL(2, fraction) },
  { weight: 2, ...LEVEL(2, area) },
  { weight: 2, ...LEVEL(2, word2) },
  { weight: 2, ...LEVEL(2, spelling2) },
  { weight: 2, ...LEVEL(2, knowledge2) },
  { weight: 2, ...LEVEL(3, percent) },
  { weight: 2, ...LEVEL(3, order) },
  { weight: 2, ...LEVEL(3, squares) },
]

/** A question for him. `level` 1 is for a 7-year-old, 2 for about 9, 3 for 11 and over. `skip` is the ids of recent ones, so it does not repeat. */
export function makeQuiz(rand: Rand = Math.random, who: { name: string; pet: string } = { name: 'the keeper', pet: 'the cat' }, skip: readonly string[] = [], level = 1): Quiz {
  const easyShare = level >= 3 ? 0.25 : level === 2 ? 0.5 : 1
  const pool: { weight: number; make: (rand: Rand, who: { name: string; pet: string }) => Quiz }[] = MAKERS.map((m) => ({ weight: m.weight * easyShare, make: m.make }))
  if (level >= 2) for (const h of HARDER) if (h.min <= level) pool.push({ weight: h.weight, make: (r, w) => h.make(r, w, level) })
  const total = pool.reduce((a, m) => a + m.weight, 0)
  let quiz: Quiz | null = null
  for (let tries = 0; tries < 8; tries++) {
    let at = rand() * total
    let maker = pool[0]
    for (const m of pool) {
      if ((at -= m.weight) <= 0) {
        maker = m
        break
      }
    }
    quiz = maker.make(rand, who)
    if (!skip.includes(quiz.id)) return quiz
  }
  return quiz!
}

/** Is what he typed right? Numbers may be digits or words; spelling must be exact; general knowledge forgives a slip in a long answer. */
export function checkAnswer(q: Quiz, text: string): boolean {
  const said = normalise(text)
  if (!said) return false
  if (q.numeric) {
    const n = numberFrom(said)
    return n !== null && q.answers.some((a) => numberFrom(a) === n)
  }
  if (q.answers.includes(said)) return true
  if (q.kind === 'spelling') return false
  return q.answers.some((a) => a.length >= 6 && similarity(said, a) >= 0.85)
}
