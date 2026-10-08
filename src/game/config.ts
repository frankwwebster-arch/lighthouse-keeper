/**
 * LIGHTHOUSE KEEPER: every number and every list the game runs on.
 * (Evolved from the Keeper mini game in Stranded Studio: same needs-and-mood
 * model, same day marks, same pet and callers, now with credits, a phone,
 * a loo, a shop, bedtime and a proper multi-day loop.)
 *
 * Nothing in the rules (`engine.ts`) has a number of its own: change one here
 * and the game changes with it. Its only import is the upgrade list, made
 * from data/upgrades.csv.
 */

import { UPGRADE_ROWS } from './upgrades.data'

const H = 60

export const NEEDS = ['hunger', 'energy', 'fun', 'hygiene', 'bladder', 'social', 'tidiness'] as const
export type NeedId = (typeof NEEDS)[number]

export const NEED_LABEL: Record<NeedId, string> = {
  hunger: 'Food',
  energy: 'Energy',
  fun: 'Fun',
  hygiene: 'Wash',
  bladder: 'Loo',
  social: 'Company',
  tidiness: 'Tidy',
}

export const FLOORS = ['ground', 'living', 'bedroom', 'aquarium', 'weather', 'lair', 'lamp', 'outside'] as const
export type FloorId = (typeof FLOORS)[number]
/** A floor with a room in it (not the lamp room on top, not outside). */
export type RoomFloor = Exclude<FloorId, 'lamp' | 'outside'>

/**
 * How the tower stacks (docs/EXPANSION_DESIGN.md, "Locked tower layout"): the
 * kitchen is always at the bottom, the bedroom always just under the lamp room,
 * and every other floor sits in the middle in no set order. A new floor takes
 * a random middle place when it arrives, which the save keeps for good.
 * Underground floors hang below the kitchen. Locked floors take no space.
 */
export const BASE_FLOOR = 'ground' satisfies RoomFloor
export const TOP_FLOOR = 'bedroom' satisfies RoomFloor
/** The middle of the tower on day 1. */
export const START_MIDDLE: readonly RoomFloor[] = ['living']
export const UNDERGROUND: readonly RoomFloor[] = ['lair']
export const START_FLOORS: readonly RoomFloor[] = [BASE_FLOOR, ...START_MIDDLE, TOP_FLOOR]
/** Every room floor there is, for the `?floors=all` preview. */
export const ALL_ROOM_FLOORS: readonly RoomFloor[] = ['ground', 'living', 'aquarium', 'weather', 'bedroom', 'lair']

/** Things a mission can unlock: a floor, or the lift. */
export type UnlockId = 'aquarium' | 'weather' | 'lair' | 'lift'

export type ObjectId =
  | 'fridge'
  | 'cooker'
  | 'tv'
  | 'bookshelf'
  | 'piano'
  | 'basin'
  | 'toilet'
  | 'bed'
  | 'phone'
  | 'desk'
  | 'telescope'
  | 'lamp'
  | 'jetty'
  | 'garden'
  | 'shop'
  | 'petbowl'
  | 'door'
  | 'broom'
  // Unlocked by missions
  | 'tank'
  | 'fishfood'
  | 'barometer'
  | 'radio'
  | 'console'
  | 'gadgets'
  /** Not a thing: wherever he is. */
  | 'here'

export type AnimKey = 'busy' | 'eat' | 'sleep' | 'read' | 'piano' | 'tv' | 'telescope' | 'fish' | 'pet' | 'wave' | 'dance' | 'greet' | 'phone' | 'dig' | 'loo' | 'wash' | 'think' | 'shrug' | 'jump' | 'spin' | 'shake' | 'wobble' | 'sway' | 'flop' | 'bow' | 'none'
export type FxKey = 'steam' | 'bubbles' | 'sparkles' | 'dust' | 'scribbles' | 'music' | 'zzz' | 'tv' | 'hearts' | 'stench' | 'burp' | 'splash' | 'coins' | 'ring' | 'stars'

export interface ObjectDef {
  id: ObjectId
  label: string
  floor: FloorId
  /** Where he stands to use it, in the picture's units (see `world.ts`). */
  x: number
  /** How close the camera comes when he uses it. */
  zoom: number
}

// ─── Food and the shop ───────────────────────────────────────────────────────

export interface FoodDef {
  id: string
  label: string
  /** Credits in the shop (0 = always in the larder). */
  cost: number
  hunger: number
  fun?: number
  /** `snack`: from the fridge. `cook`: needs the cooker. `takeaway`: ordered on the phone. */
  kind: 'snack' | 'cook' | 'takeaway' | 'staple'
  /** Minutes to cook and eat. */
  minutes: number
}

export const FOODS: readonly FoodDef[] = [
  // Always there, so the keeper can never be stuck with nothing to eat.
  { id: 'toast', label: 'Toast and butter', cost: 0, hunger: 22, kind: 'staple', minutes: 12 },
  { id: 'apple', label: 'An apple', cost: 1, hunger: 12, kind: 'snack', minutes: 6 },
  { id: 'cheese', label: 'Cheese and crackers', cost: 2, hunger: 16, kind: 'snack', minutes: 8 },
  { id: 'lolly', label: 'Ice lolly', cost: 2, hunger: 8, fun: 10, kind: 'snack', minutes: 6 },
  { id: 'cake', label: 'Slice of cake', cost: 3, hunger: 14, fun: 12, kind: 'snack', minutes: 8 },
  { id: 'sausages', label: 'Sausages and mash', cost: 5, hunger: 46, fun: 6, kind: 'cook', minutes: 35 },
  { id: 'pasta', label: 'Spaghetti bolognese', cost: 5, hunger: 46, fun: 6, kind: 'cook', minutes: 35 },
  { id: 'chips', label: 'Fish finger sandwich and chips', cost: 6, hunger: 50, fun: 8, kind: 'cook', minutes: 35 },
  { id: 'pizza', label: 'Takeaway pizza', cost: 10, hunger: 70, fun: 14, kind: 'takeaway', minutes: 20 },
]
export const foodById = (id: string) => FOODS.find((f) => f.id === id)

// ─── What he can do ──────────────────────────────────────────────────────────

export interface InteractionDef {
  id: string
  object: ObjectId
  /** What the menu says. */
  label: string
  /** His diary: "He ___." */
  did: string
  minutes: number
  effects: Partial<Record<NeedId, number>>
  anim: AnimKey
  fx?: FxKey
  /** Left alone, he may pick this himself. */
  self: boolean
  /** A treat: it waits until the keeper's question has been answered. The basics (loo, bed, food, wash) never do. */
  gated: boolean
  /** The door is shut while he does it, and the room is out of sight (the loo). */
  private?: boolean
  /** Costs credits (set per item in the shop, so 0 here). */
  cost?: number
  /** Words the plain-English reader may use to point at it. */
  keywords: readonly string[]
  /** For the menu: something to try typing. */
  example: string
}

/** Everything on the menus. The click menu of an object lists the ones whose `object` is that object. */
export const INTERACTIONS: readonly InteractionDef[] = [
  // Fridge and cooker
  { id: 'fridge_snack', object: 'fridge', label: 'Have a snack', did: 'had a snack from the fridge', minutes: 8, effects: {}, anim: 'eat', self: true, gated: false, keywords: ['snack', 'fridge', 'eat', 'nibble', 'hungry', 'biscuit'], example: 'have a snack' },
  { id: 'cooker_cook', object: 'cooker', label: 'Cook something', did: 'cooked a proper meal', minutes: 35, effects: { tidiness: -8 }, anim: 'busy', fx: 'steam', self: true, gated: false, keywords: ['cook', 'supper', 'dinner', 'lunch', 'breakfast', 'meal', 'stove', 'cooker'], example: 'cook some supper' },
  { id: 'cooker_toast', object: 'cooker', label: 'Make toast', did: 'made some toast', minutes: 12, effects: { hunger: 22 }, anim: 'busy', fx: 'steam', self: true, gated: false, keywords: ['toast'], example: 'make some toast' },
  // TV and sofa
  { id: 'tv_watch', object: 'tv', label: 'Watch TV', did: 'watched the telly', minutes: 40, effects: { fun: 30, energy: -4 }, anim: 'tv', fx: 'tv', self: true, gated: true, keywords: ['tv', 'telly', 'television', 'watch', 'cartoons', 'channel'], example: 'watch TV' },
  { id: 'tv_nature', object: 'tv', label: 'Watch the nature channel', did: 'watched a nature programme', minutes: 40, effects: { fun: 22, social: 6 }, anim: 'tv', fx: 'tv', self: false, gated: true, keywords: ['nature', 'animals', 'documentary'], example: 'watch the nature channel' },
  { id: 'tv_nap', object: 'tv', label: 'Snooze on the sofa', did: 'snoozed on the sofa', minutes: 45, effects: { energy: 26, fun: 4 }, anim: 'sleep', fx: 'zzz', self: true, gated: false, keywords: ['sofa', 'snooze', 'nap', 'doze', 'forty winks', 'lie down'], example: 'have a nap on the sofa' },
  // Books and piano
  { id: 'read_book', object: 'bookshelf', label: 'Read a book', did: 'read a book', minutes: 40, effects: { fun: 26, energy: 3 }, anim: 'read', self: true, gated: true, keywords: ['read', 'book', 'story'], example: 'read a book' },
  { id: 'play_piano', object: 'piano', label: 'Play the piano', did: 'played the piano', minutes: 30, effects: { fun: 30, social: 4 }, anim: 'piano', fx: 'music', self: true, gated: true, keywords: ['piano', 'tune', 'music', 'play something'], example: 'play the piano' },
  // Bathroom things
  { id: 'wash_basin', object: 'basin', label: 'Have a wash', did: 'had a wash', minutes: 15, effects: { hygiene: 40 }, anim: 'wash', fx: 'bubbles', self: true, gated: false, keywords: ['wash', 'bath', 'shower', 'scrub', 'soap', 'clean yourself'], example: 'have a wash' },
  { id: 'brush_teeth', object: 'basin', label: 'Brush teeth', did: 'brushed his teeth', minutes: 6, effects: { hygiene: 15 }, anim: 'wash', fx: 'bubbles', self: true, gated: false, keywords: ['teeth', 'toothbrush', 'brush your teeth'], example: 'brush your teeth' },
  { id: 'loo_wee', object: 'toilet', label: 'Go to the loo', did: 'went to the loo', minutes: 8, effects: { bladder: 70 }, anim: 'loo', private: true, self: true, gated: false, keywords: ['loo', 'toilet', 'wee', 'pee', 'bathroom'], example: 'go to the loo' },
  { id: 'loo_poo', object: 'toilet', label: 'Do a poo', did: 'locked himself in the loo for a long, long time', minutes: 14, effects: { bladder: 100, fun: 8 }, anim: 'loo', fx: 'stench', private: true, self: false, gated: false, keywords: ['poo', 'poop', 'number two'], example: 'do a poo' },
  // Bed
  { id: 'bed_sleep', object: 'bed', label: 'Go to bed for the night', did: 'went to bed', minutes: 30, effects: { energy: 20 }, anim: 'sleep', fx: 'zzz', self: false, gated: false, keywords: ['sleep', 'bed', 'goodnight', 'good night', 'bedtime'], example: 'go to bed' },
  { id: 'bed_nap', object: 'bed', label: 'Have a nap', did: 'had a nap', minutes: 60, effects: { energy: 38 }, anim: 'sleep', fx: 'zzz', self: true, gated: false, keywords: ['nap', 'snooze', 'winks', 'tired', 'rest'], example: 'have forty winks' },
  // Desk
  { id: 'desk_diary', object: 'desk', label: 'Write in his diary', did: 'wrote in his diary', minutes: 20, effects: { fun: 10, social: 6 }, anim: 'busy', fx: 'scribbles', self: true, gated: true, keywords: ['diary', 'write', 'journal', 'letter'], example: 'write in your diary' },
  { id: 'desk_tidy', object: 'broom', label: 'Tidy up', did: 'tidied up the lighthouse', minutes: 25, effects: { tidiness: 40, fun: -6 }, anim: 'busy', fx: 'dust', self: true, gated: false, keywords: ['tidy', 'sweep', 'dust', 'clean', 'mop', 'clear up'], example: 'tidy up' },
  // Lamp room
  { id: 'lamp_light', object: 'lamp', label: 'Light the lamp', did: 'lit the great lamp', minutes: 10, effects: {}, anim: 'busy', fx: 'sparkles', self: false, gated: false, keywords: ['light the lamp', 'lamp on', 'switch on the lamp', 'lantern', 'beam'], example: 'light the lamp' },
  { id: 'lamp_polish', object: 'lamp', label: 'Polish the lamp', did: 'polished the lamp until it shone', minutes: 25, effects: { tidiness: 6 }, anim: 'busy', fx: 'sparkles', self: false, gated: false, keywords: ['polish', 'shine', 'buff'], example: 'polish the lamp' },
  { id: 'scope_look', object: 'telescope', label: 'Look through the telescope', did: 'looked out to sea', minutes: 20, effects: { fun: 16 }, anim: 'telescope', self: true, gated: true, keywords: ['telescope', 'look out', 'spy', 'horizon', 'out to sea'], example: 'look through the telescope' },
  // Outside
  { id: 'jetty_fish', object: 'jetty', label: 'Go fishing', did: 'went fishing off the jetty', minutes: 45, effects: { fun: 22, hunger: 14, energy: -6, hygiene: -4 }, anim: 'fish', fx: 'splash', self: true, gated: true, keywords: ['fish', 'fishing', 'rod', 'catch'], example: 'go fishing' },
  { id: 'garden_tend', object: 'garden', label: 'Tend the garden', did: 'weeded and watered the garden', minutes: 30, effects: { fun: 12, energy: -6, hygiene: -10, tidiness: 6 }, anim: 'dig', fx: 'splash', self: true, gated: true, keywords: ['garden', 'water', 'weed', 'dig', 'plants', 'veg', 'vegetables'], example: 'water the garden' },
  { id: 'garden_pick', object: 'garden', label: 'Pick something to eat', did: 'picked something fresh from the garden', minutes: 10, effects: { hunger: 14, hygiene: -3 }, anim: 'dig', self: true, gated: false, keywords: ['pick', 'harvest', 'tomato', 'carrot'], example: 'pick some veg' },
  { id: 'shop_buy', object: 'shop', label: 'Go shopping', did: 'popped to the shop', minutes: 15, effects: { fun: 6 }, anim: 'busy', fx: 'coins', self: false, gated: true, keywords: ['shop', 'shopping', 'buy', 'store', 'groceries'], example: 'go to the shop' },
  // Pet
  { id: 'pet_feed', object: 'petbowl', label: 'Feed the pet', did: 'fed the pet', minutes: 8, effects: { social: 8 }, anim: 'pet', fx: 'hearts', self: true, gated: false, keywords: ['feed'], example: 'feed the cat' },
  { id: 'pet_play', object: 'here', label: 'Play with the pet', did: 'played with the pet', minutes: 20, effects: { fun: 16, social: 18 }, anim: 'pet', fx: 'hearts', self: true, gated: true, keywords: ['stroke', 'pet', 'cuddle', 'play with', 'fuss', 'tickle'], example: 'play with the cat' },
  // Phone and door
  { id: 'phone_call', object: 'phone', label: 'Phone a friend', did: 'rang a friend', minutes: 10, effects: { social: 12 }, anim: 'phone', fx: 'ring', self: false, gated: true, keywords: ['phone', 'call', 'ring', 'telephone', 'invite'], example: 'phone a friend' },
  { id: 'phone_pizza', object: 'phone', label: 'Order a takeaway pizza', did: 'ordered a pizza', minutes: 6, effects: {}, anim: 'phone', fx: 'ring', self: false, gated: true, keywords: ['pizza', 'takeaway'], example: 'order a pizza' },
  { id: 'phone_answer', object: 'phone', label: 'Answer the phone', did: 'answered the phone', minutes: 8, effects: { social: 12, fun: 4 }, anim: 'phone', fx: 'ring', self: true, gated: false, keywords: ['answer the phone', 'pick up'], example: 'answer the phone' },
  { id: 'door_greet', object: 'door', label: 'Welcome the visitor in', did: 'opened the door to a visitor', minutes: 10, effects: { social: 22 }, anim: 'greet', self: false, gated: false, keywords: ['door', 'greet', 'answer', 'visitor', 'let them in', 'welcome'], example: 'answer the door' },
  // Together, when a visitor is in
  { id: 'with_chat', object: 'here', label: 'Have a chat', did: 'had a good chat', minutes: 25, effects: { social: 30, fun: 8 }, anim: 'think', self: true, gated: false, keywords: ['chat', 'talk', 'natter'], example: 'have a chat' },
  { id: 'with_cards', object: 'here', label: 'Play cards', did: 'played cards', minutes: 35, effects: { fun: 28, social: 22 }, anim: 'busy', self: true, gated: false, keywords: ['cards', 'snap'], example: 'play cards' },
  { id: 'with_tv', object: 'tv', label: 'Watch TV together', did: 'watched telly together', minutes: 40, effects: { fun: 26, social: 22 }, anim: 'tv', fx: 'tv', self: false, gated: false, keywords: ['together'], example: 'watch TV together' },
  // The aquarium (unlocked by a mission)
  { id: 'tank_watch', object: 'tank', label: 'Watch the fish', did: 'watched the fish swim round and round', minutes: 25, effects: { fun: 22, energy: 4 }, anim: 'tv', fx: 'bubbles', self: true, gated: true, keywords: ['aquarium', 'tank', 'watch the fish', 'fish tank'], example: 'watch the fish' },
  { id: 'tank_feed', object: 'fishfood', label: 'Feed the fish', did: 'fed the fish', minutes: 8, effects: { social: 8, fun: 6 }, anim: 'pet', fx: 'bubbles', self: true, gated: false, keywords: ['feed the fish', 'fish food', 'flakes'], example: 'feed the fish' },
  // The weather station
  { id: 'weather_check', object: 'barometer', label: 'Check the weather', did: 'checked the weather instruments', minutes: 10, effects: { fun: 6 }, anim: 'think', self: true, gated: false, keywords: ['weather', 'forecast', 'barometer', 'rain'], example: 'check the weather' },
  { id: 'radio_chat', object: 'radio', label: 'Chat on the radio', did: 'chatted to the ships on the radio', minutes: 20, effects: { social: 24, fun: 6 }, anim: 'phone', fx: 'ring', self: true, gated: true, keywords: ['radio', 'over and out', 'mayday', 'coastguard'], example: 'chat on the radio' },
  // The hidden lair
  { id: 'lair_console', object: 'console', label: 'Use the secret computer', did: 'tapped away at the secret computer', minutes: 30, effects: { fun: 28, energy: -4 }, anim: 'busy', fx: 'sparkles', self: true, gated: true, keywords: ['computer', 'secret', 'console', 'hack', 'lair', 'hideout'], example: 'use the secret computer' },
  { id: 'lair_gadgets', object: 'gadgets', label: 'Tinker with gadgets', did: 'invented a gadget (it nearly worked)', minutes: 30, effects: { fun: 24, tidiness: -8 }, anim: 'busy', fx: 'sparkles', self: true, gated: true, keywords: ['gadget', 'invent', 'tinker', 'build', 'workbench'], example: 'tinker with gadgets' },
]
export const interactionById = (id: string) => INTERACTIONS.find((i) => i.id === id)
/** Only done when a visitor is in the house. */
export const VISITOR_ONLY = ['with_chat', 'with_cards', 'with_tv']

export const OBJECTS: readonly ObjectDef[] = [
  // Inside the tower: x is measured from the tower's left edge (see `world.ts`). Outside: x is the picture's own.
  { id: 'door', label: 'Front door', floor: 'ground', x: 92, zoom: 1.7 },
  { id: 'fridge', label: 'Fridge', floor: 'ground', x: 176, zoom: 2.0 },
  { id: 'cooker', label: 'Cooker', floor: 'ground', x: 256, zoom: 2.0 },
  { id: 'broom', label: 'Broom', floor: 'ground', x: 324, zoom: 1.8 },
  { id: 'petbowl', label: 'Pet bowl', floor: 'ground', x: 400, zoom: 2.0 },
  { id: 'tv', label: 'TV', floor: 'living', x: 140, zoom: 2.0 },
  { id: 'bookshelf', label: 'Bookshelf', floor: 'living', x: 256, zoom: 2.0 },
  { id: 'piano', label: 'Piano', floor: 'living', x: 376, zoom: 2.0 },
  { id: 'bed', label: 'Bed', floor: 'bedroom', x: 132, zoom: 2.0 },
  { id: 'phone', label: 'Phone', floor: 'bedroom', x: 224, zoom: 2.2 },
  { id: 'desk', label: 'Desk', floor: 'bedroom', x: 292, zoom: 2.0 },
  { id: 'basin', label: 'Wash basin', floor: 'bedroom', x: 380, zoom: 2.1 },
  { id: 'toilet', label: 'Loo', floor: 'bedroom', x: 440, zoom: 2.1 },
  { id: 'telescope', label: 'Telescope', floor: 'lamp', x: 135, zoom: 2.1 },
  { id: 'lamp', label: 'The great lamp', floor: 'lamp', x: 280, zoom: 1.9 },
  { id: 'garden', label: 'Garden', floor: 'outside', x: 95, zoom: 1.8 },
  { id: 'shop', label: 'Shop', floor: 'outside', x: 215, zoom: 1.8 },
  { id: 'jetty', label: 'Jetty', floor: 'outside', x: 1040, zoom: 1.7 },
  // Floors that missions unlock. Places are first guesses for the art to move.
  { id: 'tank', label: 'Fish tank', floor: 'aquarium', x: 200, zoom: 1.9 },
  { id: 'fishfood', label: 'Fish food', floor: 'aquarium', x: 368, zoom: 2.1 },
  { id: 'barometer', label: 'Weather instruments', floor: 'weather', x: 200, zoom: 2.0 },
  { id: 'radio', label: 'Radio', floor: 'weather', x: 360, zoom: 2.1 },
  { id: 'console', label: 'Secret computer', floor: 'lair', x: 200, zoom: 2.0 },
  { id: 'gadgets', label: 'Gadget bench', floor: 'lair', x: 368, zoom: 2.0 },
]
export const objectById = (id: ObjectId) => OBJECTS.find((o) => o.id === id)

/** Keeper-owned assets may fail, including large outdoor structures. The off-island shop belongs to somebody else. */
export const BREAKABLE_OBJECTS: readonly ObjectId[] = OBJECTS.filter((object) => object.id !== 'shop').map((object) => object.id)
export type BreakdownSound = 'electronic-fizzle' | 'mechanical-clunk' | 'plumbing-sputter' | 'structure-crack'
export const BREAKDOWN_SFX: Partial<Record<ObjectId, BreakdownSound>> = {
  fridge: 'electronic-fizzle', cooker: 'electronic-fizzle', tv: 'electronic-fizzle', phone: 'electronic-fizzle', lamp: 'electronic-fizzle',
  basin: 'plumbing-sputter', toilet: 'plumbing-sputter',
  door: 'mechanical-clunk', broom: 'mechanical-clunk', petbowl: 'mechanical-clunk', bookshelf: 'mechanical-clunk', piano: 'mechanical-clunk', bed: 'mechanical-clunk', desk: 'mechanical-clunk', telescope: 'mechanical-clunk',
  garden: 'structure-crack', jetty: 'structure-crack',
}

// ─── Upgrades ────────────────────────────────────────────────────────────────

/** One step up for an object. The first in a list is tier 2 (tier 1 is what he starts with). */
export interface UpgradeTier {
  name: string
  /** Normal price in credits (the grown-ups' dials scale or replace it). */
  cost: number
}

/**
 * Objects he can upgrade, bought with credits from the object's own menu (no
 * furniture shop). The list lives in data/upgrades.csv (one row per object per
 * tier; `npm run upgrades` copies it into the game). What a tier does is the
 * same for every object (`GAME.upgrades`); the bed also gives a better night.
 * Names are written as headings ("Big flat-screen TV"); `midSentence` lowers the first letter.
 */
const objectIds = new Set<string>(OBJECTS.map((o) => o.id))
const tierRows = (id: ObjectId) => UPGRADE_ROWS.filter((r) => r.object === id).sort((a, b) => a.tier - b.tier)
/** Each object's tiers from 2 up, stopping at the first gap in the list. */
export const UPGRADES: Partial<Record<ObjectId, readonly UpgradeTier[]>> = Object.fromEntries(
  [...new Set(UPGRADE_ROWS.map((r) => r.object))]
    .filter((id) => objectIds.has(id))
    .map((id) => {
      const tiers: UpgradeTier[] = []
      for (const r of tierRows(id as ObjectId)) {
        if (r.tier !== tiers.length + 2) continue
        tiers.push({ name: r.name, cost: Math.max(1, r.price) })
      }
      return [id, tiers] as const
    })
    .filter(([, tiers]) => tiers.length),
)
/** What tier 1 is called ("Basic oven"), where the list names it. */
export const baseTierName = (id: ObjectId) => tierRows(id).find((r) => r.tier === 1)?.name
/** The top tier an object goes to (1 = no upgrades). */
export const maxTier = (id: ObjectId) => 1 + (UPGRADES[id]?.length ?? 0)
/** Tier 2 and up: its name and normal price. */
export const upgradeTier = (id: ObjectId, tier: number): UpgradeTier | undefined => (tier >= 2 ? UPGRADES[id]?.[tier - 2] : undefined)
/** A name inside a sentence: "a big flat-screen TV" (words like American keep their capital). */
export const midSentence = (name: string) => (/^(American|English|French|Italian|Japanese|Victorian)\b/.test(name) ? name : name[0].toLowerCase() + name.slice(1))
export const upgradeKey = (id: ObjectId, tier: number) => `${id}:${tier}`

// ─── Missions ────────────────────────────────────────────────────────────────

/**
 * Things that count towards a mission. `done:<interaction>` is a finished
 * job; the rest are events: `ship_safe` (the lamp saw a ship home),
 * `caller_met`, `repaired`, `quiz_right`, `good_day` (a day scored at least
 * GAME.missions.goodDay).
 */
export type MissionEvent = `done:${string}` | 'ship_safe' | 'caller_met' | 'repaired' | 'upgraded' | 'quiz_right' | 'good_day'

export interface MissionDef {
  id: string
  title: string
  /** What he says about it. */
  blurb: string
  unlocks: UnlockId
  /** Open only once the tower has at least this many floors above ground (the lift is for a tall tower). */
  needsFloors?: number
  /** Shown as a mystery until he has made a start on it (the lair must be a surprise). */
  secret?: boolean
  goals: readonly { event: MissionEvent; count: number; label: string }[]
}

/** All open at once, in no order: whichever he finishes first, he gets first. */
export const MISSIONS: readonly MissionDef[] = [
  {
    id: 'fishy',
    title: 'Fishy Business',
    blurb: 'I want my own fish to look after. Help me learn about sea creatures and I will build an aquarium!',
    unlocks: 'aquarium',
    goals: [
      { event: 'done:jetty_fish', count: 3, label: 'Go fishing off the jetty' },
      { event: 'done:tv_nature', count: 2, label: 'Watch the nature channel' },
    ],
  },
  {
    id: 'storm',
    title: 'Storm Chaser',
    blurb: 'A proper keeper needs a weather station. Keep watch and keep the ships safe, and we will build one!',
    unlocks: 'weather',
    goals: [
      { event: 'done:scope_look', count: 3, label: 'Look out to sea through the telescope' },
      { event: 'ship_safe', count: 3, label: 'Guide ships safely past with the lamp' },
    ],
  },
  {
    id: 'rumble',
    title: 'Strange Rumblings',
    blurb: 'Something is rumbling under the garden. Dig around, and ask the visitors if they have heard anything...',
    unlocks: 'lair',
    secret: true,
    goals: [
      { event: 'done:garden_tend', count: 4, label: 'Dig in the garden' },
      { event: 'caller_met', count: 2, label: 'Welcome visitors in and ask about it' },
    ],
  },
  {
    id: 'puffed',
    title: 'Puffed Out',
    blurb: 'All these stairs! Show me you have the brains and the know-how, and we will put in a lift.',
    unlocks: 'lift',
    // Today's tallest tower: kitchen, living room, both mission floors and the bedroom. Raise it as floors are added.
    needsFloors: 5,
    goals: [
      { event: 'quiz_right', count: 10, label: 'Get questions right' },
      { event: 'good_day', count: 2, label: 'Have a really good day' },
    ],
  },
]
export const missionById = (id: string) => MISSIONS.find((m) => m.id === id)

// ─── Visitors and friends ────────────────────────────────────────────────────

export interface VisitorDef {
  id: string
  name: string
  /** "the postman" (used in sentences). */
  the: string
  /** What greeting them gives him on top of the company. */
  gift: Partial<Record<NeedId, number>>
  /** Credits they leave (the postman brings the odd bit of pocket money). */
  credits?: number
  /** He can ring this one up. */
  friend: boolean
}

export const VISITORS: readonly VisitorDef[] = [
  { id: 'fisherman', name: 'Old Mac', the: 'Old Mac the fisherman', gift: { hunger: 20 }, friend: false },
  { id: 'postman', name: 'Pat', the: 'Pat the postie', gift: { fun: 16 }, credits: 2, friend: false },
  { id: 'tourist', name: 'a lost tourist', the: 'a lost tourist', gift: { fun: 10 }, friend: false },
  { id: 'sam', name: 'Skipper Sam', the: 'Skipper Sam', gift: { fun: 10 }, friend: true },
  { id: 'nell', name: 'Nell', the: 'Nell from the lifeboat', gift: { fun: 8 }, friend: true },
]
export const visitorById = (id: string) => VISITORS.find((v) => v.id === id)

export type PetKind = 'cat' | 'gull'

export const TRAITS = ['cheerful', 'grumpy', 'dreamy', 'fussy'] as const
export type TraitId = (typeof TRAITS)[number]
export const TASTE_POOL = ['tv_watch', 'read_book', 'play_piano', 'jetty_fish', 'garden_tend', 'pet_play', 'desk_tidy', 'wash_basin', 'scope_look', 'desk_diary'] as const

// ─── Everything numeric ──────────────────────────────────────────────────────

/** The dials a grown-up can turn (see the Grown-ups panel). Saved with the game. */
export interface Rules {
  /** Every morning's allowance has at least this much. */
  allowanceBase: number
  /** On top of the base, in proportion to how many of the needs ended the day green (all of them = all of this). */
  allowanceBonus: number
  /** The very first day's credits. */
  firstDay: number
  /** How many credits he may keep from one day to the next. */
  carryCap: number
  /** A need counts as green when its average over the day is at least this. */
  greenAt: number
  /** Shop and pizza prices, as a percentage of the normal prices. */
  priceScale: number
  /** Your own price for a food (id → credits); beats the scale. */
  prices: Record<string, number>
  /** Quiz difficulty: 1 = age 7, 2 = about 9, 3 = 11 and over. */
  quizLevel: 1 | 2 | 3
  /** Average game-minutes between faults. Zero disables random breakdowns. */
  breakdownMinutes: number
  /** Maximum objects that may be broken at the same time. */
  maxBreakdowns: number
  /** Every mission goal's target, as a percentage of normal (individual targets below beat it). */
  missionScale: number
  /** Credits for finishing any mission (individual rewards below beat it). */
  missionReward: number
  /** Your own target for a mission goal (`<mission>:<goal number from 0>` → how many); beats the one in MISSIONS. */
  missionGoals: Record<string, number>
  /** Your own credits for finishing a mission (mission id → credits); beats `missionReward`. */
  missionRewards: Record<string, number>
  /** Every upgrade's price, as a percentage of normal (individual prices below beat it). */
  upgradeScale: number
  /** Your own price for one upgrade (`<object>:<tier>` → credits); beats the scale. */
  upgradePrices: Record<string, number>
}

export const DEFAULT_RULES: Rules = { allowanceBase: 8, allowanceBonus: 20, firstDay: 20, carryCap: 40, greenAt: 50, priceScale: 100, prices: {}, quizLevel: 1, breakdownMinutes: 0, maxBreakdowns: 1, missionScale: 100, missionReward: 10, missionGoals: {}, missionRewards: {}, upgradeScale: 100, upgradePrices: {} }

export const GAME = {
  /** The day, in minutes after midnight. He wakes at 7am; the lamp is lit at dusk; bed is 8pm. */
  day: {
    start: 7 * H,
    dusk: 17 * H + 30,
    dark: 19 * H,
    /** From here "go to bed" ends the day. Before it he only naps. */
    bedFrom: 19 * H,
    /** From here the keeper wants bed, and gets more annoyed until he goes himself. */
    bedtime: 20 * H,
    /** He puts himself to bed at this point whatever you say. */
    forced: 21 * H + 30,
  },
  /** Seconds of play in a whole day (07:00 to 21:30 is the longest). About eight minutes. */
  dayRealSeconds: 480,
  /** The night: how long the sped-up night takes on screen (seconds), and the time he wakes. */
  nightSeconds: 6,

  /** How much each need falls in an hour of his day. */
  drift: { hunger: 6, energy: 5, fun: 6, hygiene: 3, bladder: 8, social: 4, tidiness: 2 } as Record<NeedId, number>,
  startNeeds: { hunger: 62, energy: 90, fun: 60, hygiene: 70, bladder: 70, social: 60, tidiness: 70 } as Record<NeedId, number>,
  /** What a night does: these needs fall a bit while he sleeps. (Energy comes back by the bed's tier: `upgrades.bedEnergy`.) */
  overnight: { hungerLoss: 20, hungerFloor: 35, bladder: 55, hygieneLoss: 12 },

  mood: {
    averageShare: 0.6,
    worstShare: 0.4,
    spiritsLimit: 25,
    spiritsFade: 4,
    taste: 6,
    likedBonus: 0.5,
    /** Done while grumpy, a job does this much of its good. */
    sulkyShare: 0.6,
    moodWords: { chipper: 80, content: 60, soso: 40, grumpy: 20 },
  },

  /** He needs the loo so badly he will not do anything else, below this. */
  bursting: 12,
  /** And he will refuse to do treats when his mood is under this. */
  refuseMoodBelow: 28,

  self: { idleMinutes: 25, needBelow: 35, quirkChance: 0.45, moanBelow: 25 },
  travelLimit: 40,
  queueLimit: 4,
  /** Sped-up walking, picture units a second. */
  walk: { stroll: 200 },
  breakdown: { repairMinutes: 25 },
  /**
   * What each tier does, listed from tier 1: this much more of the good a job
   * does (%), done this much quicker (%), and the energy a night in the bed
   * brings back.
   */
  upgrades: { boost: [0, 25, 50], quicker: [0, 15, 30], bedEnergy: [80, 90, 100] },
  /** Missions: the score that counts as a really good day. (Mission sizes and rewards are grown-ups' dials.) */
  missions: { goodDay: 60 },

  /** Money. */
  credits: {
    /** The first day's allowance. */
    first: 20,
    /** Each later day: this plus the yesterday's score (out of 100) times `perPoint`, rounded. */
    base: 10,
    perPoint: 0.3,
    /** What he may have left over and keep (savings carry on). */
    carryCap: 40,
    /** Items in the fridge/larder at the start (id → count). */
    startItems: { apple: 1, cheese: 1 } as Record<string, number>,
  },

  /** Pizza takes this long to turn up (minutes), and waits at the door. */
  pizzaMinutes: 45,

  lamp: { burnMinutes: 5 * H, polish: 45, dullsOvernight: 20, shiny: 50, startShine: 40 },
  ship: { earliest: 19 * H + 15, latest: 20 * H + 15, hornBefore: 50 },

  visitor: {
    /** Surprise callers a day. */
    min: 0,
    max: 1,
    earliest: 9 * H,
    latest: 16 * H,
    /** They wait at the door this long, then go (minutes). */
    waits: 90,
    missed: 6,
    /** A friend he rang turns up after this long (minutes), and stays this long. */
    friendArrives: 40,
    stays: 120,
  },
  /** The phone: not always on tap. */
  phone: {
    /** Hours between calls he is willing to make. */
    cooldownMinutes: 120,
    /** He won't phone unless his mood is at least this. */
    moodMin: 35,
    /** The phone rings with a call for him (an invitation to chat) between these times. */
    ringsMin: 0,
    ringsMax: 2,
  },

  storm: { chance: 0.3, earliest: 10 * H, latest: 15 * H, lasts: 150, thunderEvery: 45, funDrift: 1.5 },

  /** The pet. */
  pet: {
    /** Its own hunger and happiness, 0 to 100, fall this much an hour. */
    hungerDrift: 8,
    funDrift: 5,
    startHunger: 70,
    startFun: 60,
    feedGain: 60,
    playGain: 35,
  },

  /** Marks for the day: they add up to 100. */
  score: {
    mood: 30,
    ship: 20,
    friends: 10,
    pet: 10,
    house: 10,
    brain: 10,
    bedtime: 10,
    /** House: tidiness and wash both at or over this at bedtime. */
    houseAt: 50,
    /** Pet: its hunger and fun both at or over this at bedtime. */
    petAt: 40,
    /** Bedtime: in bed by this many minutes after `bedtime` for the full marks. */
    bedWindow: 45,
  },
  ratings: [
    { from: 85, id: 'master' },
    { from: 70, id: 'fine' },
    { from: 50, id: 'fair' },
    { from: 30, id: 'rough' },
    { from: 0, id: 'forget' },
  ] as const,

  /** Questions to him. */
  quiz: {
    /** After this long with no taps (real seconds), the keeper may ask Ralph something. */
    idleSeconds: 25,
    /** At least this long between questions (real seconds). */
    gapSeconds: 150,
    /** After this many wrong goes he tells Ralph the answer (and Ralph types it to carry on). */
    triesBeforeAnswer: 3,
    /** Chance an idle moment brings a quiz rather than a chat question. */
    quizShare: 0.6,
    /** Marks: how many right answers earn the full brain score in a day. */
    fullMarksAt: 4,
  },
  chat: { socialGain: 8, spirits: 3 },

  /** The keeper's typing: how far off a word may be and still be understood. */
  match: {
    /** From this similarity he just does it. */
    sure: 0.85,
    /** From this he asks "did you mean…?" */
    maybe: 0.68,
    /** Phrases shorter than this must be typed exactly. */
    fuzzyMinLetters: 4,
    maxChars: 120,
  },
  /** Stripped from the start of what is typed. */
  fillers: ['please', 'can you', 'could you', 'would you', 'will you', 'go and', 'go', 'now', 'just', 'quickly', 'keeper', 'you', 'i want you to', 'i want to', 'i wanna', 'lets', "let's", 'have a go at', 'start', 'start to', 'try to', 'try', 'hey'],

  camera: { overview: 1, talkZoom: 1.1 },
  diaryLimit: 40,
} as const

export const minutesPerSecond = () => (GAME.day.forced - GAME.day.start) / GAME.dayRealSeconds
