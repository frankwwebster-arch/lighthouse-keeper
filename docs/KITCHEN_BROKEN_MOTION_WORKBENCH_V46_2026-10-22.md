# Kitchen Broken-Appliance Motion Workbench V46

Date: 22 October 2026
Status: kettle motion/SFX presentation approved by Frank; Dishwasher V1 rejected; not promoted or wired

## Outcome

Kitchen Complete Review V46 replaces every selectable kettle predecessor in the
closed kitchen reviewer with the three exact Off/On/Broken states from approved
Kitchen Kettle Bubble Authority V47. V47 is the sole kettle visual authority on
the page. Its art remains unpromoted and unwired; V46 adds only a reversible
presentation proof for broken-appliance motion and sound.

Open the current kitchen reviewer at `/keeper-review/kitchen` or the immutable
version at
`/keeper-review/kitchen-ligne-claire-complete-review-v46/index.html`.

## Motion contract

`lighthouse-keeper/broken-appliance-motion@1` keeps approved/static pixels
separate from presentation transforms:

- Off, Subtle and Emphatic modes drive an irregular whole-object translate and
  rotate layer around the appliance's bottom-contact pivot.
- Named component layers are optional. The V47 Broken kettle derives separate
  body and airborne-lid layers which recompose pixel-for-pixel to the approved
  static Broken image. The lid receives its own hover/vibration transform.
- Environmental effects keep independent anchors. Broken steam remains fixed
  over the open top while the body and lid move; dishwasher suds retain their
  existing asset-local ownership.
- The dishwasher exercises the same whole-object contract and retains the
  component-layer extension point for its door.
- Repair to any non-Broken state zeros transforms, cancels pending rattle
  timers, stops active sound nodes and releases the existing movement lock
  synchronously.

The workbench preserves the approved V41 snap, swap, Broken-position lock,
repair-unlock and countertop-healing behaviour. No source or production asset,
runtime selector, gameplay state or approved artwork changed.

## Replaceable SFX placeholder

The intermittent metal-rattle cue is deliberately a short placeholder. SFX is
off by default and independent of motion strength. Enable it with **SFX on**.
Replace it for the current browser session by dropping any audio file on the
slot or clicking the slot to use the file picker. The replacement is decoded in
memory and never overwrites canonical audio or review evidence.

Frank's wider request for state-aware SFX slots on every game asset belongs in
the main runtime/studio codebase. The implementation prompt for Claude is
[`docs/prompts/CLAUDE_GAME_WIDE_ASSET_STATE_SFX_SLOTS_2026-10-22.md`](prompts/CLAUDE_GAME_WIDE_ASSET_STATE_SFX_SLOTS_2026-10-22.md).
It requires Standard/On/Broken and transition slots, reuses the existing
drag-and-drop sound library, and makes repair stop Broken loops immediately.

## Integrity and rollback

The immutable V46 pack contains 60 object/state records, 16 effects, 14 contact
sheets and 139 published review assets. Key SHA-256 values before archive
maintenance were:

- manifest: `eb232ec988d09fa042453fe6f90e65fab3d9622d69437944cf024e1db527ae9e`
- derived Broken body: `e9a3c52c1e82df598ce86d47bf1d6413a778887dc331a32586a843a44af08433`
- derived Broken lid: `b8ffe1192eaac084cafd78c2037b4563ab6c20ddb665109a60a493bda2aca9a0`
- placeholder WAV: `72f9b08156118717f14edcd6b73321cd14e0bd94dc419bb59490e4eb35ea4d47`

Frank approved the kettle with “kettle is approved” on 22 October 2026. The
external record
`docs/review/kitchen-broken-motion-workbench-v46-kettle-approval-2026-10-22.json`
pins the exact shell, manifest, kettle states, derived body/lid layers and
placeholder WAV. The same decision explicitly rejects Dishwasher V1. Complete
Review V50 carries the approved kettle presentation forward byte-for-byte and
offers Dishwasher V3 as a separate unapproved correction.

The registration gate remains closed. Revoking the approval requires removing
only its external record; V46, V47, V50, production assets and runtime remain
untouched.

## Verification

```bash
npm run verify:kitchen-broken-motion-workbench-v46
npm run verify:kitchen-broken-motion-workbench-v46-kettle-approval
npm run maintain:keeper-review
npm test
npm run typecheck
npm run build
```

The verifier checks V47-only kettle selection, all three exact states,
pixel-exact body/lid recomposition, the three motion modes, the independent
replaceable SFX slot, static environmental anchors, the closed registration
gate, and synchronous repair shutdown.
