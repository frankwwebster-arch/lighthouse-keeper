/**
 * THE COMMAND BOOK. Everything Ralph can type is looked up here: there is no
 * live AI anywhere in the game. A command is a bucket of phrases that all
 * mean the same thing, and the same bucket always gives the same reply and the
 * same move. To add a silly one: add a reaction below, then a bucket for it.
 *
 * Lines may use {name} (the keeper), {pet} (his pet), {time} (his clock).
 */

import type { AnimKey, FxKey, NeedId, ObjectId } from './config'

export interface ReactionDef {
  id: string
  anim: AnimKey
  fx?: FxKey
  /** Minutes of his day it takes. */
  minutes: number
  /** What he says. */
  line: string
  effects?: Partial<Record<NeedId, number>>
  /** A nudge to his spirits (-/+). */
  spirits?: number
}

const r = (id: string, anim: AnimKey, line: string, extra: Partial<ReactionDef> = {}): ReactionDef => ({ id, anim, line, minutes: 3, ...extra })

export const REACTIONS: readonly ReactionDef[] = [
  r('hello', 'wave', 'Hello there! Lovely day for it.'),
  r('thanks', 'bow', 'Oh, you are very welcome. *tips hat*'),
  r('dance', 'dance', 'Oh, I do love a boogie! Watch these moves!', { fx: 'music', minutes: 10, effects: { fun: 15, energy: -6 } }),
  r('sing', 'sway', 'La la laaa! ♪ (I am NOT very good, but I am very loud.)', { fx: 'music', minutes: 6, effects: { fun: 10 } }),
  r('whistle', 'sway', '♪ Phweeee-phwoo! ♪ ...Nope, that was the kettle.', { fx: 'music' }),
  r('burp', 'shake', 'BUUUUURRRP! ...Pardon me. That one had a fish finger in it.', { fx: 'burp', effects: { fun: 4 } }),
  r('fart', 'shake', '*PARP!* ...That was not me. That was {pet}. Definitely {pet}.', { fx: 'stench', effects: { fun: 5 } }),
  r('bum', 'wobble', 'Ha ha ha! You said BUM! Again! Say it again!', { effects: { fun: 6 } }),
  r('pants', 'jump', 'PANTS! PANTS! PANTS! ...Oh no. I think I am wearing the stripy ones.', { effects: { fun: 5 } }),
  r('bogey', 'shake', 'EW! I would NEVER. ...Okay, only on a Tuesday.', { fx: 'stars', effects: { fun: 4 } }),
  r('stinky', 'shake', 'Phwoar. You are right. {pet} has left the room.', { fx: 'stench' }),
  r('joke', 'think', 'What do you call a lighthouse keeper with no lamp? ...Lost! Hee hee hee. I made that up. (I did not.)', { effects: { fun: 6 } }),
  r('knock', 'think', 'Knock knock! ...Who is there? Boo. ...Boo who? Oh, do not cry, it is only a joke!', { effects: { fun: 6 } }),
  r('robot', 'wobble', 'BEEP. BOOP. I AM A LIGHTHOUSE ROBOT. DOES NOT COMPUTE. BEEP.', { fx: 'stars', effects: { fun: 6 } }),
  r('chicken', 'wobble', 'Bwaaaak! Bawk bawk bawk! ...Is it working? Have I laid an egg?', { effects: { fun: 6 } }),
  r('cat_noise', 'wobble', 'Meeeeow! ...{pet} is giving me a very funny look.'),
  r('dog_noise', 'jump', 'WOOF! WOOF! ...Wrong animal? Oh well. Nobody checks.'),
  r('pirate', 'sway', 'ARRRR! Shiver me timbers! Pass the grog. Er... I mean, the cocoa.', { effects: { fun: 8 } }),
  r('dinosaur', 'jump', 'RAAAWWWWR! I am a dinosaur! A very small, very tidy dinosaur!', { effects: { fun: 8 } }),
  r('ghost', 'sway', 'Wooooooo! I am the ghost of the lighthouse! Wooooo! ...Is it working?', { fx: 'stars' }),
  r('headstand', 'flop', 'Whoa! Everything is upside down! The floor is on the ceiling!', { effects: { fun: 8, energy: -4 } }),
  r('jump', 'jump', 'Boing! Boing! Boing! ...My knees! Stop! Boing!', { effects: { fun: 6, energy: -3 } }),
  r('spin', 'spin', 'Wheeeeee! I am... dizzy... whoa... the walls are going round...', { effects: { fun: 6 } }),
  r('flex', 'jump', 'Behold! The mighty arms of the lighthouse keeper! (They are not mighty.)', { fx: 'sparkles' }),
  r('kiss_pet', 'bow', 'Mwah! {pet} looks deeply unimpressed. That was a bit slobbery.', { fx: 'hearts', effects: { social: 6 } }),
  r('love', 'bow', 'Aww! I like you too, you great lump. Not in a weird way.', { fx: 'hearts', spirits: 4, effects: { social: 6 } }),
  r('sneeze', 'shake', 'Ah... ah... AAAH... AAAAATCHOOO! ...Bless me.'),
  r('face', 'wobble', 'Bleurgh! Look at my face! ...Oh no. It is stuck. Ha ha, not really.', { effects: { fun: 5 } }),
  r('cry', 'flop', 'Boo hoo hoo hoo... ...Just kidding! Ha!'),
  r('laugh', 'shake', 'HA HA HA HA HOO HOO! ...What was funny? I forgot.', { effects: { fun: 6 } }),
  r('hide', 'flop', 'Shhh! I am hiding! You cannot see me! ...I am behind the pianoforte.'),
  r('count', 'think', 'One... two... three... four... um... ten! Next!'),
  r('smelly', 'shake', 'I do NOT smell! ...*sniffs armpit* ...Okay. A bit.', { fx: 'stench' }),
  r('sulk', 'flop', 'That was not very nice. I am going to sulk now.', { spirits: -5 }),
  r('sorry', 'bow', 'That is all right. Apology accepted!', { spirits: 3 }),
  r('name', 'think', 'I am {name}, keeper of this fine lighthouse. And this is {pet}.'),
  r('age', 'think', 'Old enough to know better. Young enough not to care.'),
  r('favourite_food', 'think', 'Pizza. Always pizza. (Do not tell the {petkind}.)'),
  r('time', 'think', 'Let me see... it is {time}.'),
  r('help', 'think', 'Click on things in the lighthouse, or type what you want me to do. Try "go fishing" or "watch TV". Or something silly...'),
  r('shrug', 'shrug', 'Hmm. I am not sure what that means. *shrugs*'),
  r('wave', 'wave', 'Hello! *waves both arms*'),
  r('bow', 'bow', 'Thank you, thank you. *takes a bow*'),
]
export const reactionById = (id: string) => REACTIONS.find((x) => x.id === id)

/** What a bucket makes him do. */
export interface DoOrder {
  /** An interaction id (config.ts) or 'react'. */
  id: string
  item?: string
  react?: string
  /** Used by generic jobs such as repairing a particular broken object. */
  object?: ObjectId
}

export interface CommandDef {
  id: string
  /** Everything that means this. Typed words are matched whole, with typo-forgiveness for the longer ones. */
  phrases: readonly string[]
  /** What it makes him do. */
  doing: readonly DoOrder[]
  /** "go fishing": what the keeper says back when he asks "did you mean…?" */
  say: string
  /** A hidden or cheeky one (not shown in the help list). */
  hidden?: boolean
}

const rx = (react: string): DoOrder => ({ id: 'react', react })
const act = (id: string, item?: string): DoOrder => ({ id, ...(item ? { item } : {}) })

/** The book. Order does not matter: the best match wins, and a longer phrase beats a shorter one. */
export const COMMANDS: readonly CommandDef[] = [
  // ── The loo, and everything cheeky around it ──────────────────────────────
  { id: 'poo', say: 'do a poo', hidden: true, doing: [act('loo_poo')], phrases: ['poo', 'poop', 'poos', 'do a poo', 'do a big poo', 'do a poop', 'have a poo', 'need a poo', 'go for a poo', 'number two', 'do a number two', 'do your business', 'sit on the loo', 'sit on the toilet', 'drop a log', 'do a stinky poo', 'big stinky poo', 'stinky poo', 'make a deposit', 'visit the little boys room', 'dump', 'doodoo', 'do a dump'] },
  { id: 'wee', say: 'go for a wee', doing: [act('loo_wee')], phrases: ['wee', 'wees', 'do a wee', 'have a wee', 'need a wee', 'go for a wee', 'pee', 'do a pee', 'need a pee', 'toilet', 'the toilet', 'to the toilet', 'loo', 'the loo', 'to the loo', 'go to the toilet', 'go to the loo', 'use the toilet', 'bathroom', 'the bog', 'to the bog', 'spend a penny', 'number one', 'you need the loo'] },
  { id: 'fart', say: 'do a fart', hidden: true, doing: [rx('fart')], phrases: ['fart', 'farts', 'do a fart', 'let one rip', 'trump', 'do a trump', 'parp', 'pass wind', 'cut the cheese', 'stinky bum', 'bottom burp'] },
  { id: 'burp', say: 'burp', hidden: true, doing: [rx('burp')], phrases: ['burp', 'burps', 'do a burp', 'belch', 'do a big burp'] },
  { id: 'bum', say: 'say bum', hidden: true, doing: [rx('bum')], phrases: ['bum', 'bums', 'bottom', 'say bum', 'say bottom', 'botty', 'say botty', 'bum bum', 'bumhole', 'bumface', 'big bum', 'your bum', 'show your bum', 'say bum bum'] },
  { id: 'pants', say: 'say pants', hidden: true, doing: [rx('pants')], phrases: ['pants', 'underpants', 'say pants', 'knickers', 'say knickers', 'undies', 'show your pants', 'pants on your head', 'your pants'] },
  { id: 'bogey', say: 'pick your nose', hidden: true, doing: [rx('bogey')], phrases: ['bogey', 'bogeys', 'pick your nose', 'pick a bogey', 'snot', 'eat a bogey', 'nose picking', 'picking your nose', 'booger'] },
  { id: 'stinky', say: 'smelly feet', hidden: true, doing: [rx('stinky')], phrases: ['smelly feet', 'stinky feet', 'take your socks off', 'cheesy feet', 'sniff your socks', 'smelly socks', 'stinky socks'] },
  { id: 'smelly', say: 'you smell', hidden: true, doing: [rx('smelly')], phrases: ['you smell', 'you stink', 'you are smelly', 'youre smelly', 'smelly keeper', 'you pong', 'phwoar', 'pooey', 'stinker', 'you are stinky', 'youre stinky', 'stinky'] },
  { id: 'sneeze', say: 'sneeze', hidden: true, doing: [rx('sneeze')], phrases: ['sneeze', 'achoo', 'atchoo', 'do a sneeze', 'ah choo'] },

  // ── Silly voices and not-the-keeper replies ───────────────────────────────
  { id: 'robot', say: 'be a robot', hidden: true, doing: [rx('robot')], phrases: ['robot', 'be a robot', 'do the robot', 'beep boop', 'beep', 'boop', 'you are a robot', 'youre a robot', 'talk like a robot', 'robot voice'] },
  { id: 'chicken', say: 'be a chicken', hidden: true, doing: [rx('chicken')], phrases: ['chicken', 'be a chicken', 'cluck', 'bawk', 'do a chicken', 'bwaaak', 'lay an egg', 'act like a chicken', 'cluck cluck', 'chicken dance'] },
  { id: 'meow', say: 'meow', hidden: true, doing: [rx('cat_noise')], phrases: ['meow', 'miaow', 'miaou', 'be a cat', 'say meow', 'do a cat', 'purr', 'meeow', 'be a kitten'] },
  { id: 'woof', say: 'woof', hidden: true, doing: [rx('dog_noise')], phrases: ['woof', 'bark', 'be a dog', 'say woof', 'do a dog', 'arf', 'ruff ruff', 'be a puppy'] },
  { id: 'pirate', say: 'talk like a pirate', hidden: true, doing: [rx('pirate')], phrases: ['pirate', 'be a pirate', 'arr', 'arrr', 'ahoy matey', 'talk like a pirate', 'shiver me timbers', 'yo ho ho', 'walk the plank'] },
  { id: 'dinosaur', say: 'be a dinosaur', hidden: true, doing: [rx('dinosaur')], phrases: ['dinosaur', 'be a dinosaur', 'roar', 'rawr', 'raaawr', 'trex', 't rex', 'do a dinosaur', 'be a t rex', 'be a monster'] },
  { id: 'ghost', say: 'be a ghost', hidden: true, doing: [rx('ghost')], phrases: ['ghost', 'be a ghost', 'woooo', 'boo', 'scare me', 'be scary', 'spooky', 'haunt'] },
  { id: 'headstand', say: 'do a headstand', hidden: true, doing: [rx('headstand')], phrases: ['headstand', 'handstand', 'do a headstand', 'stand on your head', 'cartwheel', 'do a cartwheel', 'somersault', 'do a roll', 'upside down', 'do a handstand', 'backflip', 'do a backflip'] },
  { id: 'jump', say: 'jump', doing: [rx('jump')], phrases: ['jump', 'jump up and down', 'hop', 'bounce', 'boing', 'do a jump', 'skip', 'leap', 'jump about'] },
  { id: 'spin', say: 'spin round', doing: [rx('spin')], phrases: ['spin', 'spin round', 'twirl', 'go round and round', 'turn around', 'whirl', 'spin around', 'do a spin', 'get dizzy'] },
  { id: 'flex', say: 'show your muscles', hidden: true, doing: [rx('flex')], phrases: ['flex', 'show your muscles', 'muscles', 'be strong', 'strongman', 'flex your muscles', 'lift something heavy', 'show me your muscles'] },
  { id: 'face', say: 'pull a face', hidden: true, doing: [rx('face')], phrases: ['pull a face', 'funny face', 'make a face', 'silly face', 'face', 'make a funny face', 'pull a funny face', 'grimace'] },
  { id: 'cry', say: 'cry', doing: [rx('cry')], phrases: ['cry', 'boo hoo', 'be sad', 'weep', 'sob', 'have a cry'] },
  { id: 'laugh', say: 'laugh', doing: [rx('laugh')], phrases: ['laugh', 'giggle', 'ha ha', 'hahaha', 'lol', 'cackle', 'chuckle', 'have a laugh', 'lolol'] },
  { id: 'hide', say: 'hide', hidden: true, doing: [rx('hide')], phrases: ['hide', 'go and hide', 'hide and seek', 'play hide and seek', 'hide from the cat', 'disappear'] },
  { id: 'kiss_pet', say: 'kiss the cat', hidden: true, doing: [rx('kiss_pet')], phrases: ['kiss the cat', 'kiss the gull', 'kiss the pet', 'give the cat a kiss', 'smooch', 'give kisses', 'kiss kiss', 'kiss the bird'] },
  { id: 'sing', say: 'sing a song', doing: [rx('sing')], phrases: ['sing', 'sing a song', 'sing something', 'sing us a song', 'karaoke', 'do a song', 'belt it out', 'la la la'] },
  { id: 'whistle', say: 'whistle', doing: [rx('whistle')], phrases: ['whistle', 'whistle a tune', 'do a whistle'] },
  { id: 'count', say: 'count to ten', doing: [rx('count')], phrases: ['count', 'count to ten', 'count to 10', 'one two three', 'count to a hundred', 'count to 100', 'count the stairs'] },
  { id: 'joke', say: 'tell a joke', doing: [rx('joke')], phrases: ['joke', 'jokes', 'tell a joke', 'tell me a joke', 'make me laugh', 'say something funny', 'be funny', 'funny'] },
  { id: 'knock', say: 'knock knock', doing: [rx('knock')], phrases: ['knock knock', 'knock knock joke', 'tell me a knock knock joke', 'tell a knock knock joke'] },
  { id: 'dance', say: 'dance', doing: [rx('dance')], phrases: ['dance', 'do a dance', 'have a dance', 'boogie', 'groove', 'jig', 'do a jig', 'shake it', 'floss', 'dance dance', 'hornpipe', 'bust a move', 'shake your booty'] },

  // ── Manners and chat ──────────────────────────────────────────────────────
  { id: 'hello', say: 'say hello', doing: [rx('hello')], phrases: ['hello', 'hi', 'hiya', 'hey', 'ahoy', 'good morning', 'morning', 'good afternoon', 'good evening', 'howdy', 'hello keeper', 'yo', 'wave', 'say hello', 'give us a wave', 'wave hello'] },
  { id: 'thanks', say: 'thank you', doing: [rx('thanks')], phrases: ['thanks', 'thank you', 'cheers', 'well done', 'good job', 'nice one', 'great job', 'good keeper', 'good boy', 'thankyou', 'ta'] },
  { id: 'sorry', say: 'sorry', doing: [rx('sorry')], phrases: ['sorry', 'im sorry', 'i am sorry', 'my bad', 'apologies', 'forgive me'] },
  { id: 'sulk', say: 'be rude', hidden: true, doing: [rx('sulk')], phrases: ['idiot', 'stupid', 'shut up', 'dumb', 'you are rubbish', 'rubbish', 'useless', 'you are a loser', 'loser', 'i hate you', 'you are ugly', 'ugly', 'dummy', 'moron'] },
  { id: 'love', say: 'I love you', doing: [rx('love')], phrases: ['love you', 'i love you', 'you are the best', 'youre the best', 'best keeper', 'i like you', 'you are great', 'you are brilliant', 'lovely keeper', 'give me a hug', 'hug', 'give a hug'] },
  { id: 'name', say: 'what is your name', doing: [rx('name')], phrases: ['what is your name', 'whats your name', 'your name', 'who are you', 'name', 'what are you called', 'say your name'] },
  { id: 'age', say: 'how old are you', doing: [rx('age')], phrases: ['how old are you', 'your age', 'whats your age', 'how old', 'what age are you'] },
  { id: 'favourite_food', say: 'what is your favourite food', doing: [rx('favourite_food')], phrases: ['favourite food', 'what is your favourite food', 'whats your favourite food', 'what do you like to eat', 'best food', 'favorite food', 'what is your favorite food'] },
  { id: 'time', say: 'what is the time', doing: [rx('time')], phrases: ['what time is it', 'what is the time', 'whats the time', 'the time', 'time please', 'what time', 'tell me the time'] },
  { id: 'help', say: 'help', doing: [rx('help')], phrases: ['help', 'help me', 'what can you do', 'what can i do', 'what can i say', 'commands', 'what do i do', 'instructions', 'how do i play', 'im stuck', 'i am stuck'] },

  // ── The proper jobs ───────────────────────────────────────────────────────
  { id: 'snack', say: 'have a snack', doing: [act('fridge_snack')], phrases: ['snack', 'have a snack', 'get a snack', 'eat something', 'eat', 'the fridge', 'open the fridge', 'raid the fridge', 'nibble', 'have a biscuit', 'biscuit', 'am hungry', 'im hungry', 'you are hungry', 'have something to eat', 'get some food', 'food', 'eat some food', 'munch', 'have a bite', 'eat a snack', 'eat pizza', 'eat the pizza', 'eat a pizza', 'have some pizza', 'have pizza', 'eat cake', 'eat an apple', 'eat cheese', 'eat a lolly'] },
  { id: 'cook', say: 'cook some supper', doing: [act('cooker_cook')], phrases: ['cook', 'cook something', 'cook some supper', 'cook supper', 'cook dinner', 'cook lunch', 'cook breakfast', 'cook a meal', 'make supper', 'make dinner', 'make lunch', 'make breakfast', 'make a meal', 'make some food', 'make sausages', 'cook sausages', 'cook pasta', 'cook spaghetti', 'make pasta', 'cook chips', 'make chips', 'the cooker', 'use the cooker', 'use the stove', 'fry something', 'bake something', 'fish fingers'] },
  { id: 'toast', say: 'make some toast', doing: [act('cooker_toast')], phrases: ['toast', 'make toast', 'make some toast', 'make me some toast', 'do some toast', 'toast and butter', 'have some toast', 'burn some toast', 'toaster'] },
  { id: 'tv', say: 'watch TV', doing: [act('tv_watch')], phrases: ['tv', 'telly', 'television', 'watch tv', 'watch the tv', 'watch telly', 'watch the telly', 'watch television', 'switch on the tv', 'turn on the tv', 'put the tv on', 'turn the tv on', 'switch the tv on', 'tv on', 'watch cartoons', 'cartoons', 'change the channel', 'watch something', 'put the telly on', 'switch on the telly'] },
  { id: 'nature', say: 'watch the nature channel', doing: [act('tv_nature')], phrases: ['nature channel', 'watch nature', 'watch the nature channel', 'nature programme', 'watch animals', 'wildlife', 'watch a documentary', 'documentary', 'watch the news'] },
  { id: 'sofa', say: 'snooze on the sofa', doing: [act('tv_nap')], phrases: ['sofa', 'the sofa', 'sit on the sofa', 'snooze on the sofa', 'nap on the sofa', 'lie on the sofa', 'relax', 'put your feet up', 'have a sit down', 'sit down', 'chill'] },
  { id: 'read', say: 'read a book', doing: [act('read_book')], phrases: ['read', 'read a book', 'read a story', 'get a book', 'books', 'book', 'bookshelf', 'story', 'read something', 'read the paper', 'read comics', 'read a comic', 'have a read'] },
  { id: 'piano', say: 'play the piano', doing: [act('play_piano')], phrases: ['piano', 'play the piano', 'play piano', 'play a tune', 'play music', 'play us a tune', 'play something', 'tickle the ivories', 'play a song', 'keyboard', 'music'] },
  { id: 'wash', say: 'have a wash', doing: [act('wash_basin')], phrases: ['wash', 'have a wash', 'wash yourself', 'wash your face', 'wash your hands', 'wash up', 'have a bath', 'bath', 'have a shower', 'shower', 'scrub', 'soap', 'clean yourself', 'get clean', 'freshen up', 'get washed', 'the basin', 'the sink', 'wash your pits'] },
  { id: 'teeth', say: 'brush your teeth', doing: [act('brush_teeth')], phrases: ['teeth', 'brush your teeth', 'brush teeth', 'clean your teeth', 'toothbrush', 'toothpaste', 'brush', 'brushing'] },
  { id: 'sleep', say: 'go to bed', doing: [act('bed_sleep')], phrases: ['bed', 'go to bed', 'to bed', 'sleep', 'go to sleep', 'bedtime', 'time for bed', 'night night', 'goodnight', 'good night', 'turn in', 'get into bed', 'sleepy time', 'off to bed', 'hit the hay', 'hit the sack', 'lights out', 'put yourself to bed'] },
  { id: 'nap', say: 'have a nap', doing: [act('bed_nap')], phrases: ['nap', 'have a nap', 'take a nap', 'forty winks', '40 winks', 'snooze', 'doze', 'rest', 'have a rest', 'have a lie down', 'lie down', 'lie in bed', 'catnap', 'tired', 'you are tired', 'im tired', 'have a sleep', 'close your eyes'] },
  { id: 'diary', say: 'write in your diary', doing: [act('desk_diary')], phrases: ['diary', 'write', 'write in your diary', 'write a diary', 'write your diary', 'write a letter', 'letter', 'journal', 'the desk', 'dear diary', 'write something', 'doodle', 'draw', 'draw a picture'] },
  { id: 'tidy', say: 'tidy up', doing: [act('desk_tidy')], phrases: ['tidy', 'tidy up', 'clean up', 'clean', 'sweep', 'sweep up', 'dust', 'mop', 'clear up', 'tidy the house', 'tidy the lighthouse', 'clean the house', 'do the cleaning', 'do some tidying', 'broom', 'hoover', 'vacuum', 'housework', 'chores', 'do your chores', 'tidy your room', 'tidy the kitchen'] },
  { id: 'lamp', say: 'light the lamp', doing: [act('lamp_light')], phrases: ['light the lamp', 'lamp on', 'switch on the lamp', 'turn on the lamp', 'light the light', 'turn on the light', 'switch on the light', 'light up', 'light the beam', 'the lamp', 'the great lamp', 'put the light on', 'lantern', 'beam', 'switch the lamp on', 'turn the lamp on', 'turn on the lighthouse', 'start the lighthouse'] },
  { id: 'polish', say: 'polish the lamp', doing: [act('lamp_polish')], phrases: ['polish', 'polish the lamp', 'shine the lamp', 'make the lamp shine', 'buff the lamp', 'clean the lamp', 'give the lamp a polish', 'shine', 'shine it up', 'polish the light'] },
  { id: 'telescope', say: 'look through the telescope', doing: [act('scope_look')], phrases: ['telescope', 'look through the telescope', 'use the telescope', 'look out to sea', 'spy', 'spy on someone', 'look out', 'lookout', 'horizon', 'look at the sea', 'see what is out there', 'look for ships', 'look for boats', 'binoculars', 'look through the window', 'look out of the window', 'out to sea'] },
  { id: 'fish', say: 'go fishing', doing: [act('jetty_fish')], phrases: ['fish', 'fishing', 'go fishing', 'catch a fish', 'catch fish', 'go and fish', 'fishing rod', 'the jetty', 'to the jetty', 'go to the jetty', 'go out on the jetty', 'rod', 'cast a line', 'cast the line', 'get a fish', 'catch some fish', 'catch a big fish', 'go fish'] },
  { id: 'garden', say: 'water the garden', doing: [act('garden_tend')], phrases: ['garden', 'the garden', 'water the garden', 'water the plants', 'tend the garden', 'weed the garden', 'weed', 'do the gardening', 'gardening', 'dig', 'dig the garden', 'plant something', 'plant seeds', 'water', 'water the veg', 'go to the garden', 'grow something'] },
  { id: 'garden_pick', say: 'pick some veg', doing: [act('garden_pick')], phrases: ['pick some veg', 'pick veg', 'pick something', 'harvest', 'harvest the veg', 'pick a tomato', 'pick tomatoes', 'pick a carrot', 'pick carrots', 'pick vegetables', 'get some veg', 'pick something to eat', 'pick the veg', 'pick a vegetable'] },
  { id: 'shop', say: 'go to the shop', doing: [act('shop_buy')], phrases: ['shop', 'the shop', 'go to the shop', 'go shopping', 'shopping', 'to the shop', 'buy', 'buy something', 'buy food', 'buy some food', 'groceries', 'get some shopping', 'visit the shop', 'go to the store', 'go to the shops', 'spend money', 'spend some money', 'spend credits', 'buy snacks', 'get some snacks'] },
  { id: 'feed_pet', say: 'feed the cat', doing: [act('pet_feed')], phrases: ['feed', 'feed the cat', 'feed the gull', 'feed the pet', 'feed the bird', 'feed the kitty', 'pet food', 'give the cat some food', 'cat food', 'give the cat food', 'feed the animal', 'feed your pet', 'feed the kitten'] },
  { id: 'play_pet', say: 'play with the cat', doing: [act('pet_play')], phrases: ['play with the cat', 'play with the gull', 'play with the pet', 'play with the bird', 'stroke the cat', 'stroke the pet', 'cuddle the cat', 'cuddle', 'tickle the cat', 'pet the cat', 'fuss the cat', 'play with your pet', 'stroke', 'fuss', 'pat the cat', 'play with the kitten', 'play with the kitty', 'play fetch'] },
  { id: 'phone', say: 'phone a friend', doing: [act('phone_call')], phrases: ['phone', 'phone a friend', 'call a friend', 'ring a friend', 'phone someone', 'ring someone', 'call someone', 'use the phone', 'make a call', 'make a phone call', 'telephone', 'invite someone', 'invite a friend', 'invite someone over', 'ring sam', 'phone sam', 'call sam', 'ring nell', 'phone nell', 'call nell', 'ring a mate', 'invite a friend over', 'ring up a friend', 'call up a friend'] },
  { id: 'phone_answer', say: 'answer the phone', doing: [act('phone_answer')], phrases: ['answer the phone', 'pick up the phone', 'get the phone', 'answer it', 'phone is ringing', 'pick it up', 'answer the telephone', 'get the telephone', 'take the call'] },
  { id: 'pizza', say: 'order a pizza', doing: [act('phone_pizza')], phrases: ['pizza', 'order a pizza', 'order pizza', 'get a pizza', 'takeaway', 'order a takeaway', 'get a takeaway', 'order takeaway', 'pizza please', 'get pizza', 'phone for a pizza', 'ring for a pizza', 'order some pizza', 'pizza time', 'get takeaway', 'i want pizza', 'we want pizza'] },
  { id: 'greet', say: 'answer the door', doing: [act('door_greet')], phrases: ['answer the door', 'the door', 'open the door', 'let them in', 'let them in please', 'get the door', 'greet', 'greet the visitor', 'greet the guest', 'welcome', 'welcome the visitor', 'who is at the door', 'whos at the door', 'see who it is', 'see who is there', 'say hello to the visitor', 'let the visitor in', 'let the guest in', 'visitor', 'guest', 'someone is at the door', 'there is somebody at the door', 'door'] },
  { id: 'chat', say: 'have a chat', doing: [act('with_chat')], phrases: ['chat', 'have a chat', 'talk to them', 'talk to the visitor', 'natter', 'have a natter', 'chat to your friend', 'chat to the visitor', 'chat with the visitor', 'chat with your friend', 'speak to them', 'talk to your friend'] },
  { id: 'cards', say: 'play cards', doing: [act('with_cards')], phrases: ['cards', 'play cards', 'snap', 'play snap', 'a game of cards', 'play a game', 'play a game of cards', 'deal the cards', 'play top trumps', 'play with your friend', 'play together'] },
  { id: 'tv_together', say: 'watch TV together', doing: [act('with_tv')], phrases: ['watch tv together', 'watch telly together', 'watch the tv together', 'watch tv with your friend', 'watch tv with them', 'watch telly with them', 'tv together'] },
]

/** Words in a typed message that point at a particular food. */
export const FOOD_WORDS: Record<string, string> = {
  apple: 'apple', apples: 'apple', cheese: 'cheese', crackers: 'cheese', lolly: 'lolly', lollies: 'lolly', icelolly: 'lolly', cake: 'cake', sausages: 'sausages', sausage: 'sausages', mash: 'sausages', pasta: 'pasta', spaghetti: 'pasta', bolognese: 'pasta', chips: 'chips', fishfingers: 'chips', toast: 'toast', pizza: 'pizza',
}

/** How he answers an ordinary job, depending on what he is like and how he was asked. */
export const ACKS = {
  plain: ['Right you are!', 'On it!', 'Aye aye!', 'No problem.', 'Consider it done.', 'Righto.'],
  grumpy: ['Hmph. If I must.', 'Fine. FINE.', 'Oh, all right then.', 'Always me, is it.'],
  dreamy: ['Ooh, yes... lovely idea.', 'Mmm... if the sea does not mind.', 'Right-o, drifting there now.'],
  fussy: ['Very well. But properly.', 'Certainly. In the correct order.', 'Hmm, yes. At once.'],
  cheerful: ['Brilliant idea!', 'Ooh yes, let us!', 'Absolutely!', 'Whistling as I go!'],
} as const
