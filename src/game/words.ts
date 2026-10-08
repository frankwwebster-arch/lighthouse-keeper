/**
 * EVERYTHING HE SAYS about what happens, and the lines for his diary.
 * (What he says to typed commands is in `commands.ts`; his questions are in
 * `quiz.ts` and `chat.ts`.) Lines may use {name} {pet} {petkind} {time} {who}.
 */

import { ACKS, reactionById } from './commands'
import { INTERACTIONS, NEED_LABEL, foodById, interactionById, midSentence, missionById, objectById, upgradeTier, visitorById, type NeedId, type ObjectId, type UnlockId } from './config'
import { moodWord, type Happening, type MoodWord, type State } from './engine'

export function clockText(minutes: number): string {
  const m = Math.floor(minutes) % (24 * 60)
  const h = Math.floor(m / 60)
  return `${h % 12 === 0 ? 12 : h % 12}:${String(m % 60).padStart(2, '0')}${h < 12 ? 'am' : 'pm'}`
}

export const NAMES = {
  keeper: ['Barnaby', 'Angus', 'Horatio', 'Wilf', 'Mungo', 'Seamus', 'Fergus', 'Bertie', 'Magnus', 'Ezra', 'Cuthbert', 'Alfie'],
  cat: ['Biscuit', 'Mackerel', 'Captain', 'Sprat', 'Pudding', 'Kipper', 'Marmite', 'Smudge'],
  gull: ['Chips', 'Gulliver', 'Squawk', 'Admiral', 'Pebble', 'Nelson', 'Scampi', 'Beaky'],
} as const

export const moodName: Record<MoodWord, string> = { chipper: 'Chipper', content: 'Content', soso: 'So-so', grumpy: 'Grumpy', miserable: 'Miserable' }
export const moodFace: Record<MoodWord, string> = { chipper: '😄', content: '🙂', soso: '😐', grumpy: '😠', miserable: '😭' }

export const fill = (text: string, s: Pick<State, 'name' | 'petName' | 'petKind' | 'clock'>, extra: Record<string, string> = {}): string => {
  let out = text.replace(/\{name\}/g, s.name).replace(/\{pet\}/g, s.petName).replace(/\{petkind\}/g, s.petKind).replace(/\{time\}/g, clockText(s.clock))
  for (const [k, v] of Object.entries(extra)) out = out.replace(new RegExp(`\\{${k}\\}`, 'g'), v)
  return out
}

/** How he answers a job he has been given, by temperament and mood. */
export function ack(s: State, n: number): string {
  const pool = [...ACKS.plain, ...ACKS[s.personality.trait]]
  const word = moodWord(0)
  void word
  return pool[Math.abs(n) % pool.length]
}

const moan: Record<NeedId, string> = {
  hunger: 'My tummy is rumbling like a foghorn!',
  energy: 'I am so tired I could sleep standing up.',
  fun: 'I am SO bored. Is there nothing to do?',
  hygiene: 'I am starting to smell like old fish...',
  bladder: 'I need the loo! Quick!',
  social: 'It is very quiet. I wish someone would visit.',
  tidiness: 'This place is a tip. Look at it!',
}

const refuse = (h: Happening): string => {
  const def = h.id ? interactionById(h.id) : undefined
  const why = h.why
  if (why === 'missing') return pick(['We have not got one of those... yet. Maybe a mission will sort that out!', 'One of those? In THIS lighthouse? Not yet. Check the missions!'], h.n)
  if (why === 'storm') return 'Fishing in THIS? Not on your life. I would be blown to Norway.'
  if (why === 'nobody') return h.id === 'phone_answer' ? 'The phone is not ringing...' : 'There is nobody here.'
  if (why === 'early') return 'It is not bedtime yet! I will have a nap instead.'
  if (why === 'quiz') return 'Hang on, answer my question first! Then I will do that.'
  if (why === 'bursting') return 'NOT NOW! I need the loo, RIGHT NOW!'
  if (why === 'grumpy') return pick(['I do not feel like it. Maybe later.', 'Hmph. Not in the mood.', 'No. I am cross.'], h.n)
  if (why === 'phone_busy') return 'I only just put the phone down! Give it a bit.'
  if (why === 'phone_mood') return 'I do not feel like chatting to anyone. Not today.'
  if (why === 'phone_none') return 'Everyone I know is already here!'
  if (why === 'broke' && h.id === 'upgrade') return 'We cannot afford that upgrade yet. Save up a bit more!'
  if (why === 'broke') return h.item ? `I cannot afford the ${foodById(h.item)?.label.toLowerCase() ?? 'that'}. Not enough credits.` : 'We have not got the credits for that today.'
  if (why === 'broken') return 'It is broken. I need to repair it first.'
  if (why === 'notready') return 'Nothing is ready to pick. Water the garden first.'
  if (why === 'pizza_pending') return 'We have already ordered one. Be patient!'
  if (why === 'empty') return h.id === 'cooker_cook' ? 'There is nothing to cook! Toast it is. Or go to the shop.' : 'The fridge is empty. Just cobwebs. Go to the shop?'
  return def ? `I cannot do that right now.` : 'Hmm.'
}

const UNLOCK_NAMES: Record<UnlockId, string> = { aquarium: 'aquarium', weather: 'weather station', lair: 'hidden lair', lift: 'lift' }

const pick = <T,>(list: readonly T[], n: number): T => list[Math.abs(Math.trunc(n)) % list.length]

export interface Told {
  /** What the keeper says (in a bubble), if anything. */
  say?: string
  /** What goes in the diary, if anything. */
  diary?: string
  /** How the screen should react. */
  tone?: 'good' | 'bad' | 'info'
  /** An effect to play at the keeper. */
  boom?: 'thunder' | 'horn'
}

/** What a happening comes to: his words, and a diary line. */
export function tell(h: Happening, s: State): Told {
  const who = h.who ? visitorById(h.who) : undefined
  const t = clockText(h.at)
  switch (h.kind) {
    case 'dawn':
      return { diary: `Day ${s.day}. ${t}. A fresh start.`, say: s.day === 1 ? 'Morning! What shall we do today?' : `Good morning! A new day. ${h.amount ? `We have ${h.amount} fresh credits.` : ''}` }
    case 'chose': {
      const def = h.id ? interactionById(h.id) : undefined
      if (h.id === 'react') return { diary: `${t} He felt like doing something silly.`, say: undefined }
      return def ? { say: `I think I will ${def.label.toLowerCase()}.`, diary: `${t} He decided to ${def.label.toLowerCase()}.` } : {}
    }
    case 'done': {
      const def = h.id ? interactionById(h.id) : undefined
      const tail = h.item ? ` (${foodById(h.item)?.label ?? h.item})` : ''
      return { diary: `${t} He ${(def?.did ?? 'did something').replace('{pet}', s.petName)}${tail}.`, tone: h.sulky ? 'bad' : undefined }
    }
    case 'react': {
      const r = h.react ? reactionById(h.react) : undefined
      return r ? { say: fill(r.line, s), diary: `${t} ${fill(r.line, s)}` } : {}
    }
    case 'refuse':
      return { say: refuse(h), diary: `${t} He would not.`, tone: 'bad' }
    case 'moan':
      return { say: h.need ? moan[h.need] : undefined, diary: h.need ? `${t} ${NEED_LABEL[h.need]} is low.` : undefined, tone: 'bad' }
    case 'caller':
      return { say: `Someone is at the door! It is ${who?.the ?? 'a visitor'}.`, diary: `${t} ${who?.the ?? 'Someone'} knocked at the door.`, tone: 'info' }
    case 'caller_met':
      return { say: `Come in, come in!${h.amount ? ` Oh, ${h.amount} credits for me? Lovely.` : ''}`, diary: `${t} He let ${who?.the ?? 'them'} in.`, tone: 'good' }
    case 'caller_gone':
      return { say: `Oh, they went away. I was too slow.`, diary: `${t} ${who?.the ?? 'The visitor'} gave up waiting and left.`, tone: 'bad' }
    case 'visitor_left':
      return { say: `Goodbye, ${who?.name ?? 'friend'}! Come again!`, diary: `${t} ${who?.the ?? 'The visitor'} said goodbye.`, tone: 'info' }
    case 'horn':
      return { say: 'I can hear a ship horn out at sea! Is the lamp lit?', diary: `${t} A ship horn, far off.`, tone: 'info', boom: 'horn' }
    case 'ship':
      return h.safe ? { say: 'Hooray! The ship saw our light and sailed safely by!', diary: `${t} The ship passed safely.`, tone: 'good' } : { say: 'Oh no! The lamp was out. The ship nearly hit the rocks!', diary: `${t} The ship passed in the dark. Close call.`, tone: 'bad' }
    case 'storm':
      return h.on ? { say: 'Storm coming in! Hold on to your hat!', diary: `${t} A storm blew in.`, tone: 'info' } : { say: 'The storm has passed. Phew.', diary: `${t} The storm blew itself out.`, tone: 'info' }
    case 'thunder':
      return { diary: undefined, boom: 'thunder' }
    case 'dusk':
      return { say: 'It is getting dark. Time to think about the lamp.', diary: `${t} Dusk.`, tone: 'info' }
    case 'lamp_lit':
      return { say: 'The great lamp is lit!', diary: `${t} The lamp is burning.`, tone: 'good' }
    case 'lamp_out':
      return { say: 'The lamp has gone out.', diary: `${t} The lamp burned out.`, tone: 'bad' }
    case 'spotted': {
      if (h.what === 'storm') return { say: `There is a storm brewing. About ${Math.max(10, h.inMinutes ?? 0)} minutes away.`, diary: `${t} He spotted a storm.` }
      if (h.what === 'caller') return { say: `A boat is coming. It looks like ${who?.the ?? 'someone'}.`, diary: `${t} He spotted a boat.` }
      if (h.what === 'ship') return { say: 'A ship will pass tonight. Remember the lamp!', diary: `${t} He spotted tonight's ship.` }
      return { say: 'Nothing but sea and sky.', diary: `${t} Nothing out there.` }
    }
    case 'bed':
      return { say: h.by === 'self' ? 'RIGHT. That is it. I am going to bed. Goodnight!' : 'Goodnight! Zzzzz...', diary: `${t} He went to bed.` }
    case 'annoyed':
      return { say: pick(['It is bedtime, you know...', 'I am TIRED! Bed. Now. Please.', 'RIGHT. If you do not send me to bed I am going myself.'], (h.level ?? 1) - 1), diary: `${t} He is getting grumpy about bedtime.`, tone: 'bad' }
    case 'ring':
      return { say: 'The phone is ringing!', diary: `${t} The phone rang.`, tone: 'info' }
    case 'friend_coming':
      return { say: `${who?.name ?? 'My friend'} is coming over!`, diary: `${t} ${who?.name ?? 'A friend'} is on the way.`, tone: 'good' }
    case 'pizza_ordered':
      return { say: `Pizza is on its way! That is ${h.amount} credits.`, diary: `${t} He ordered a takeaway pizza.` }
    case 'pizza_arrived':
      return { say: 'DING DONG! The pizza is here! It is in the fridge.', diary: `${t} The pizza arrived.`, tone: 'good' }
    case 'bought':
      return { say: `One ${foodById(h.item ?? '')?.label.toLowerCase() ?? 'thing'}, please! That is ${h.amount} credits.`, diary: `${t} He bought ${foodById(h.item ?? '')?.label.toLowerCase() ?? 'something'}.`, tone: 'good' }
    case 'locked':
      return { say: 'I am IN THE LOO! Go away! I will be out when I am out!', tone: 'bad' }
    case 'pet': {
      const pet = s.petName
      if (h.petDid === 'steal') return { say: `${pet}! Come back with that ${foodById(h.item ?? '')?.label.toLowerCase() ?? 'snack'}!`, diary: `${t} ${pet} stole a ${foodById(h.item ?? '')?.label.toLowerCase() ?? 'snack'}.`, tone: 'bad' }
      if (h.petDid === 'knock') return { say: `${pet}! Look what you did to the tidying!`, diary: `${t} ${pet} knocked something over.`, tone: 'bad' }
      if (h.petDid === 'gift') return { say: s.petKind === 'cat' ? `${pet} has brought me a present. It is a... dead leaf. Thank you!` : `${pet} has brought me a shiny shell!`, diary: `${t} ${pet} brought him a present.`, tone: 'good' }
      return { diary: `${t} ${pet} purred on his lap.`, tone: 'good' }
    }
    case 'quiz':
      return h.correct ? { say: pick(['Spot on! Clever clogs!', 'Correct! I knew you knew that.', 'Brilliant! Right you are.'], h.n), tone: 'good' } : {}
    case 'chat':
      return {}
    case 'credits':
      return { say: `A surprise! ${h.amount} extra credits for me. Brilliant!`, diary: `${t} A surprise gift of ${h.amount} credits.`, tone: 'good' }
    case 'breakdown': {
      const label = objectById(h.id as ObjectId)?.label ?? 'Something'
      return { say: `Oh no! The ${label.toLowerCase()} has broken down.`, diary: `${t} The ${label.toLowerCase()} broke down.`, tone: 'bad' }
    }
    case 'repaired': {
      const label = objectById(h.id as ObjectId)?.label ?? 'thing'
      return { say: `Fixed! The ${label.toLowerCase()} is working again.`, diary: `${t} He repaired the ${label.toLowerCase()}.`, tone: 'good' }
    }
    case 'upgraded': {
      const name = midSentence(upgradeTier(h.id as ObjectId, h.level ?? 2)?.name ?? 'upgrade')
      const a = /^[aeiouAEIOU]/.test(name) ? 'an' : 'a'
      const old = objectById(h.id as ObjectId)?.label.toLowerCase() ?? 'thing'
      return h.gift
        ? { say: `A present from the grown-ups: ${a} ${name}! Best day ever.`, diary: `${t} The grown-ups gave him ${a} ${name}.`, tone: 'good' }
        : { say: pick([`Out with the old ${old}, in with the ${name}!`, `Ooh, ${a} ${name}! Worth every credit.`, `Look at that! ${a === 'an' ? 'An' : 'A'} ${name}. Very posh.`], h.n), diary: `${t} He upgraded to ${a} ${name} for ${h.amount} credits.`, tone: 'good' }
    }
    case 'mission_done': {
      const m = h.id ? missionById(h.id) : undefined
      return { say: `MISSION COMPLETE: ${m?.title ?? 'done'}! ${h.amount ? `And ${h.amount} credits for us!` : ''}`, diary: `${t} Mission complete: ${m?.title ?? h.id}.`, tone: 'good' }
    }
    case 'unlocked': {
      const name = UNLOCK_NAMES[h.id as UnlockId] ?? 'something new'
      return { say: h.id === 'lift' ? 'A LIFT! No more stairs! My knees thank you.' : h.id === 'lair' ? `WHAT?! There was a ${name} under the lighthouse all along!` : `Look! A brand new floor: the ${name}! And it is all furnished!`, diary: `${t} The ${name} arrived.`, tone: 'good' }
    }
    default:
      return {}
  }
}

/** Menu names. */
export const labelFor = (id: string, s: Pick<State, 'petName'>): string => {
  const def = INTERACTIONS.find((i) => i.id === id)
  if (!def) return id
  return def.label.replace('the pet', s.petName)
}
