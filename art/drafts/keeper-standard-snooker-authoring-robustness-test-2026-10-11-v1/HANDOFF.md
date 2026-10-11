# Standard-uniform snooker authoring robustness test V1

Status: **visually accepted robustness test for side-right standard-uniform
snooker poses**.

Frank authorized exactly two isolated built-in referenced-image generations to
test whether the current single-pose prompt structure can reliably render the
canonical Keeper beyond the accepted upright reach:

1. an upright cue-contact pose;
2. the deepest two-hand snooker lean.

Both requests used the same four authorities:

- isolated canonical high-resolution standing Keeper — SHA-256
  `3f57bb341b20cfc9727c6a3c5bc4622a5b6dc60b8b1d6b5811b182a498f97517`;
- Frank-approved V5 upright reach source — SHA-256
  `edad59744798973b83af65d386261f94e4f8ba4da7fd8eb26fc4614820226539`;
- legacy high-resolution snooker source for cue/action geometry only — SHA-256
  `d78fd0505de0fa0b4dd477a6fb035ec1eed1fd241694d11b93a8c2210cf08d58`;
- exact canonical gameplay neutral — SHA-256
  `02106cfc54b224c8d4e9985e58420f1350f114d24e2e6c6258cad68e513657ce`.

## Upright cue contact

- exact prompt: `PROMPT-CUE-CONTACT.txt` — SHA-256
  `596817f4b78e2923bc1266e8d5e38212f0f94102d292000d2222bd26b756b7e3`;
- untouched output: `generated/cue-contact-v1.png` — SHA-256
  `b2d0e2e0b3dba7f89dbbda0b4f9575d12044eede001077fae9bac78a4ee3a830`;
- observed result: coherent upright pose, exactly two visible arms/hands, one
  cue, defined rear torso and a transparent safety gutter;
- status: visually accepted by Frank; unnormalized and not promoted.

## Deep lean

- exact prompt: `PROMPT-DEEP-LEAN.txt` — SHA-256
  `3baa4a513ca2242f371b3a2dbab9234905198bdd41ca8df71b735e72523067f1`;
- untouched output: `generated/deep-lean-v1-failed.png` — SHA-256
  `9ce261cb5ad8acd261ff45bb8276a5d1a33be38bbd65f685c22f3f24d4c8b6e8`;
- observed result: Frank confirmed that the two-hand bridge/control gesture
  reads correctly. The source also contains dark alpha/glow contamination and
  reaches the left and bottom edges; those are deterministic normalization and
  containment issues rather than rejected character-design issues;
- status: visually accepted by Frank; unnormalized and not promoted.

## Conclusion

Frank visually accepted both the upright prop-contact pose and the deepest
action lean. Together with the previously accepted upright reach, the same
reference hierarchy and single-pose prompt structure has now covered the two
extremes required by the snooker sequence. This is sufficient evidence to use
the recipe for the side-right standard-uniform snooker family. It does not yet
prove every facing, costume or unrelated activity family; those require their
own representative extremes.

The source-art method and the deterministic production stage remain distinct:
ImageGen authors one isolated coherent pose from canonical identity, accepted
family-continuity and action-only references; deterministic tooling then
isolates valid foreground, removes low-alpha glow, uniformly scales, aligns,
hardens alpha and adds contract gutters without changing internal proportions.

No production source, raw strip, runtime sprite, manifest, reviewer draft,
immutable review export or deployment was changed. Nothing was normalized,
registered, committed, pushed or promoted. Frank's acceptance applies to the
two visual exemplars and the snooker authoring recipe, not yet to a completed
animation strip.
