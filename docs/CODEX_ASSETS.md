# Sprites to ask Codex for (live list)

The game draws vector placeholders. A PNG dropped into `public/sprites/` and listed in `public/sprites/manifest.json` replaces the placeholder with no code change:

```json
{ "keeper_walk": "keeper_walk.png", "obj_fridge": "fridge.png" }
```

Transparent PNGs, bottom-centre = where the feet/floor sit. Pick ONE style first (smooth cartoon or pixel art, see ART_REFERENCES.md) and keep it identical across everything. Still images are enough: the game animates them (bobbing, jumping, swaying). Frame-sheets are a later upgrade.

## Keeper (about 90 x 130; key `keeper_<pose>`)
`none` (standing), `walk`, `eat`, `busy` (cooking/tidying), `sleep` (lying), `read`, `piano`, `tv` (sitting), `telescope`, `fish`, `pet`, `wave`, `dance`, `greet`, `phone`, `dig`, `wash`, `think`, `shrug`, `jump`. Faces: happy / neutral / grumpy variants welcome.

## Pet (about 64 x 52; `pet_cat`, `pet_gull`)
Plus later: sleeping, eating, hungry, scared, playing.

## Visitors (about 80 x 120; `visitor_<id>`)
`fisherman` (Old Mac), `postman` (Pat), `tourist`, `sam` (Skipper Sam), `nell`.

## Objects (key `obj_<id>`)
door 50x96, fridge 48x96, cooker 70x60, broom 30x90, petbowl 40x20, toilet 50x70, tv 110x90, bookshelf 80x110, piano 100x70, bed 120x54, phone 60x70, basin 60x110, desk 100x80, telescope 90x90, lamp 120x140 (off and on), garden 120x70 (empty and 1-3 ripe), shop 130x120, jetty 220x60.

## Scenery (not wired yet, ask for after style is chosen)
Lighthouse tower cutaway with four rooms, sky/sea background, ship, clouds, rain, loo door, food icons for each item in the shop.

## Sound (optional, later)
Loo flush, fart/burp, thunder, ship horn, phone ring, doorbell.
