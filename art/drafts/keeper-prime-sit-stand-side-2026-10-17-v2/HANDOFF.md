# Prime Keeper side-right sit/stand V2

V2 is a reversible chair-geometry correction. All six Keeper cells, the
forward and reverse pose order, all 45 route roots and every duration are
unchanged from V1. The candidate remains review-only.

The corrected chair contract uses the exact seated Prime F6 landmarks:

- top support surface: 11 logical pixels above the floor;
- spine/back contact: cell `[7,29]`, source `[56,232]`;
- back-of-knee line: cell `[18,29]`, source `[144,232]`;
- maximum usable side-view seat depth: 11 logical pixels.

The example seat begins at the spine/back contact and ends exactly at the
back-of-knee line. It does not extend beneath or beyond the knee. SHA-256
provenance and deterministic checks are in `batch-register.json`.
