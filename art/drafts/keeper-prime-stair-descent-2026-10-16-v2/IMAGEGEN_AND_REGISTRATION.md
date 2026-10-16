# Keeper Prime stair descent V2 — image generation and registration

Status: review candidate only. V1 is retained as rejected provenance. No approved,
Final, runtime or production asset is changed.

## Final image-editing prompts

The four accepted raw outputs were generated from the approved side-right Prime
Keeper and approved V16 stair poses. The operative requirements in each prompt
were:

- preserve the approved adult Keeper identity, cap, beard, moustache,
  single-stripe jumper, trousers, boots, palette and smooth outline;
- strict side-right profile, transparent background, no stair or shadow;
- exactly two arms, two hands, two legs and two boots;
- right-contact: anatomical right foot forward/downhill and flat, left foot
  trailing/uphill and flat one riser higher;
- left-passing: right foot bears weight while left foot lifts compactly and
  passes forward/downhill; restrained opposite arm movement;
- left-contact: anatomical left foot forward/downhill and flat, right foot
  trailing/uphill and flat one riser higher;
- right-passing: left foot bears weight while right foot lifts compactly and
  passes forward/downhill; restrained opposite arm movement.

Two preliminary right-contact and one preliminary left-passing render created a
third arm. Those outputs were rejected. The retained corrected outputs were made
with an explicit edit instruction to remove the entire far-left stray arm and
reconstruct the torso edge while preserving the two intended arms.

## Deterministic cell registration

All retained raw files are 1122 × 1402 RGBA PNGs. Registration crops the alpha
content at threshold 16, scales it to 286 px high with Lanczos filtering,
centres it horizontally in a 256 × 320 RGBA cell, and places the registered
content at y=30. This reproduces the V16 stair-pose vertical envelope and leaves
a four-pixel minimum bottom safety gutter.

| Pose | Raw crop `w:h:x:y` | Registered width |
|---|---:|---:|
| right contact | `625:1221:283:115` | 146 px |
| left passing | `578:1222:326:114` | 135 px |
| left contact | `651:1178:281:129` | 158 px |
| right passing | `635:1188:272:117` | 153 px |

The builder records SHA-256 values for both raw and registered files. The V2
verifier checks dimensions, hashes, transparent cell edges, route membership,
unchanged staircase geometry, monotonic descent roots and the exact repeating
gait `RIGHT contact → LEFT passing → LEFT contact → RIGHT passing`.
