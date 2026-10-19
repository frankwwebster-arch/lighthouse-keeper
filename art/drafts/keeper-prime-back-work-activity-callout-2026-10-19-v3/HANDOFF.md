# Prime rear-work activity vocabulary V3 handoff

V3 is an immutable, reversible review candidate. It inherits the entire Prime
rear-work body and complete walk → stop → turn → action → reverse-turn → walk
route from V2/V1 byte-for-byte. It changes only the separately switchable
callout vocabulary, recipe phrase metadata and review presentation.

## Review changes

- removes the review counter/furniture completely;
- raises both callout treatments above the cap with deterministic clearance;
- adds 52 isolated object/story components while republishing the exact 16 V2
  components under the V3 review prefix;
- authors 25 42-frame recipes, including time-aware meals, animal-to-food
  lineage, and bread/ham/lettuce/tomato resolving into a sandwich;
- classifies every recipe as `rear-work`, `rear-work-with-context` or
  `dedicated-pose-required`;
- keeps body, callout envelope, primary/resolved object, supporting/story
  objects and declared SFX independently controllable.

## Verify

```sh
npm run verify:keeper-prime-back-work-activity-callout-v3
```

Nothing in runtime sprites, Final, the animation Workbench or Kitchen is
changed. Nothing is approved, promoted or deployed. Rejecting V3 requires only
discarding this directory, its V3 review page, its review-archive set and that
set's new content-addressed objects.
