# Codex: ligne-claire redraws for bubble stories (from Claude, 21 Oct 2026)

**Status: draft, waiting for Frank's approval on the project page (question r1).**
Frank asked what art direction would make sure Codex understands Hergé's
rules of ligne claire. This is it. It adds to, and never overrides, your
approved recipe: the three style champions (washing plate, sandwich tomato,
repair tool chest), “ligne claire, not cartoon”, and the binding taxonomy
**one even black outline, flat colour, no shine**.

## The rules of Hergé's ligne claire, as they apply to one picture

1. **One line, one weight.** Every contour is the same near-black line of
   the same thickness: outside edges, inner edges, folds, small parts. No
   thick-and-thin swelling, no tapering into points, no heavier outer
   silhouette. The line is steady and drawn by hand (the plate's slight
   irregularity), never a vector-perfect ellipse.
2. **The line only says what is really there.** A line marks a real edge,
   seam, fold or change of material. Nothing describes light: no hatching,
   no cross-hatching, no stipple, no speed lines baked into the object, no
   texture strokes for wood grain, fabric weave or rust. If a surface needs
   one cue (a single grain line, one seam), give it one, not ten.
3. **Every area is closed and flat.** Each shape is fully enclosed by the
   line and filled with one flat colour. No gradients, airbrush, soft
   shading, glow, rim light, specular highlight, reflection band or
   painted texture. Shadow, where it is truly needed to read the form, is
   at most one flat, slightly darker tone with a clean edge, used sparingly.
4. **Local colour, even light.** Colour is the object's own colour (a red
   tomato is red all over), as if lit by flat, even daylight. A small,
   coherent palette, clear but slightly muted, never neon or saturated
   plastic. Glass and metal are shown by their outline and at most two or
   three short construction ticks, not by shine.
5. **Objects are documented, not invented.** Hergé drew cars, aircraft,
   tools and machines with reference-level accuracy while keeping the line
   simple. Proportions, mechanisms and counts must be credible to an adult:
   a saw has a real handle and tooth line, a kettle a real spout and lid.
   Simplify by leaving detail out, never by inflating, rounding or
   cutesifying. No faces on objects, no mascots, no stickers, no toy look.
6. **Clarity first.** One readable silhouette at 64 px, a plain three-quarter
   or side viewpoint, no dramatic foreshortening, nothing ambiguous where
   parts overlap. If a detail does not read at game size, remove it.
7. **Black is a colour, not a shadow.** Solid black only where the thing is
   black (a tyre, a cast-iron pan, a hole). Never as a pool of shade.
8. **Marks follow the same line.** Comic marks (stars, drops, steam, smells,
   glints, sawdust) use the same even line and flat colour as the objects,
   so marks and objects belong to one drawing. Marks stay separate sprites.

**Quick test before you submit a picture:** cover the line and look at the
colour: is every area one flat colour? Cover the colour and look at the
line: is it one weight, and does every line mark a real edge? Shrink it to
64 px: does it still read, and does it look like a real object rather than a
cartoon one?

## What to redraw, in order (Frank's choice under r1)

Work a family at a time, as before: an immutable pack, one contact sheet,
Frank's approval, then each approved picture added as a new version with
`npm run activity-stories:add-picture` (every earlier version stays
selectable). Claude's verdicts are in `data/activity-stories/style-review.json`;
the studio's “Only pictures not yet in ligne claire” filter shows them.

**Batch 1: pictures the drafted stories use that are not yet ligne claire (25).**
- Kitchen tools and tea: `knife-bread`, `knife-chef`, `knife-paring`,
  `condiment-salt-mill`, `condiment-pepper-mill`, `tea-kettle`, `tea-milk`,
  `tea-mug`, `toast-slices`.
- Cleaning: `consumable-microfiber-cloth`, `consumable-scouring-pad`,
  `wear-rubber-gloves-pair`.
- Workshop: `repair-cordless-drill`, `repair-drill-bit-case`.
- Marks: `symbol-impact-star`, `symbol-motion-ticks`, `symbol-water-droplets`,
  `symbol-soap-bubbles`, `symbol-sizzle-spark`, `symbol-heat-curls`,
  `symbol-heat-shimmer`, `symbol-pleasant-aroma`, `symbol-foul-odour`,
  `symbol-clean-glint`, `symbol-question-mark`.

**Batch 2: new pictures the stories are waiting for** (new ids, so the
stories pick them up once Claude adds them):
- Objects: a tea bag (`tea-bag`), the finished cake (`baking-cake`), a plain
  wooden plank (`repair-plank`), a ploughman's lunch on a plate
  (`meal-ploughmans`), a clean, plain dinner plate with no food and no suds
  (`kitchen-plate`; `washing-plate` is the one being washed up), an empty egg
  basket (`eggs-basket-empty`, the same basket as `eggs-basket` with no eggs, so
  the eggs can fill it at the end), a single paintbrush (`art-paintbrush`), a clothes
  iron (`laundry-iron`), a little dust pile (`cleaning-dust-pile`).
- Marks for the new actions (kind `mark`; the engine uses each the moment it
  exists): `symbol-sawdust`, `symbol-seasoning-flecks`, `symbol-spray-mist`,
  `symbol-dust-puff`, `symbol-earth-clods`, `symbol-steam-puff`.

**Then the rest**, a group at a time in the studio's group order, starting
with the groups the next stories use (cleaning, bathroom, bedtime).

## Rules

- Do not edit `data/activity-stories/stories/`, `src/activityStories/` or
  any approved authority. Never overwrite a version.
- Run `npm run verify:activity-stories` and `npm test`. Commit and push
  without `[deploy]`; Claude releases.
- To see a picture in motion: `npm run stories -- render <story>` (for
  example `make-tea`), or one action on its own:
  `npm run stories -- render data/activity-stories/demos/stir.json`.
