# Standard-uniform snooker canon redraw — rejected V1 study

Status: **rejected during authoring; no normalized strip and no reviewer draft**.

Frank asked for `keeper_snooker` to be rebuilt from the standard-uniform
`keeper_walk` canon because the existing side-on snooker beard does not match
the visible walk-to-table identity. Three built-in image-generator requests
were attempted with exact prompts preserved here:

- `PROMPT.txt`: 4×2 referenced-image full-character redraw; rejected because
  long cues crossed neighbouring ownership cells;
- `PROMPT-V2.txt`: wider 3×3 isolation layout; cell ownership improved, but
  Frank rejected the beard as non-canonical compared with `keeper_walk`;
- `PROMPT-V3-BEARD-CORRECTION.txt`: targeted facial-hair-only correction of V2;
  rejected during authoring because the result still shortened and rounded the
  `keeper_walk` beard, especially in leaning poses.

The generated files are retained unchanged under `generated/rejected-overlap/`
with SHA-256 values:

- V1: `effbfc6a707cc63b1ab2c7305b59e7160fd73fa73b890b718173f27adb95fee5`;
- V2: `c33bff99c862a90f0dcbf79b7c8089a6809eade301399b1ea629fe516b8b0b56`;
- V3: `91aec0de0c02d8a8b2b942040e5683183b747c5fc3599a217d5ed142f1fe580d`.

Pinned referenced inputs:

- `art/source/keeper-first-batch/keeper-walk-generated-source.png` — identity,
  standard uniform, proportions and beard authority — SHA-256
  `637b3c4e66b4019730eaa7354812b18df788aedc4ab3e3b7c619589854e0da5f`;
- `art/raw/keeper-first-batch/keeper_neutral_standing-side-right_f1.png` —
  gameplay-scale side silhouette — SHA-256
  `02106cfc54b224c8d4e9985e58420f1350f114d24e2e6c6258cad68e513657ce`;
- `art/source/keeper-first-batch/keeper-snooker-generated-source.png` — action
  and cue choreography only — SHA-256
  `d78fd0505de0fa0b4dd477a6fb035ec1eed1fd241694d11b93a8c2210cf08d58`.

No canonical source, raw strip, runtime sprite, manifest, immutable review
export or deployed review comparison was changed. Do not resume by generating
more variants from these failed prompts. A later attempt needs a method that
can enforce the approved canonical beard geometry through changing lean angles
without a head transplant; Frank's exact-name reviewed queue remains the scope
authority.
