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

/** A question for him. `skip` is the ids of recent ones, so it does not repeat. */
export function makeQuiz(rand: Rand = Math.random, who: { name: string; pet: string } = { name: 'the keeper', pet: 'the cat' }, skip: readonly string[] = []): Quiz {
  const total = MAKERS.reduce((a, m) => a + m.weight, 0)
  let quiz: Quiz | null = null
  for (let tries = 0; tries < 8; tries++) {
    let at = rand() * total
    let maker = MAKERS[0]
    for (const m of MAKERS) {
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
