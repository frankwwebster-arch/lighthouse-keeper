# Kitchen Rebuild V1 standard foundation

Date: 18 October 2026

## Outcome

Rebuild V1 is a reversible clean-slate standard-kitchen review gate. The
fridge, kettle, toaster, oven/hob, mixing-bowl bay, basin bay and one-person
table/chair were drawn together as one coherent master. No old non-bin kitchen
asset is composited beneath or into this drawing.

The approved V28/V31 bin family is preserved byte-for-byte:

- standard: `86b05224a7da5fc5c05918f2875018920ed54cf46fc00cb08952ffd29789f9c0`;
- broken: `77ad87fabfd3e5c10a4a14f294af343a5d93a2a2015e6d77f18a4140b1f5fb4f`.

This is a standard-state foundation only. It deliberately contains no On or
Broken replacement states, environmental animation or new SFX placeholders.

## Exact room contract

- 193 × 56 logical pixels at 4 px/lp: exactly 772 × 224 pixels;
- fitted run x=84–588: exactly six adjacent 84-pixel bays;
- bay order: fridge, kettle, toaster, oven/hob, mixing bowl, basin;
- common worktop top y=134 and fascia top y=151;
- historical rear-wall foot line y=208;
- approved bin cell at x=8/y=149;
- complete table and rear-facing chair within x=680–764/y=148–222.

The standard room is one composition. Each isolated 84 × 120 module shown in
review is a literal crop from its corresponding bay in that composition.

## Review and provenance

Review route:

`/keeper-review/kitchen-rebuild-foundation-v1/`

The page shows the room at exact native game size, at 2× inspection size, with
a deterministic bay/alignment overlay, as six isolated standard bay crops, and
with both accepted bin cells for byte-pinned comparison.

The generated source, extraction prompt, normalization rules, raw outputs,
candidate catalogue and batch register live under versioned Rebuild V1 paths.
V41 and V32–V40 remain immutable rejected provenance. Final art and runtime
wiring are unchanged.

## Verification

Run:

```sh
npm run verify:kitchen-rebuild-foundation-v1
```

The verifier pins both generated source hashes and both accepted bin hashes,
checks the 772 × 224 room, exact six-bay measurements, deterministic
compositing, literal isolated crops, review-media preloading and the
content-addressed review archive.

## Next gate

Frank must first review this complete standard foundation. Only after approval
may coordinated Off/On/Broken families be developed from this construction.
Rejection is reversible by deleting only the Rebuild V1 source/raw/draft/page,
archive manifest, builder, verifier and documentation files.
