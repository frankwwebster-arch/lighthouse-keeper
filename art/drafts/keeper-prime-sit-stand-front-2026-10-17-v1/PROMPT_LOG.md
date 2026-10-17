# Prime Keeper front sit/stand V1 prompt log

**Tool:** built-in image generation
**Date:** 17 October 2026
**Use:** four transparent intermediate pose sources only. F1 and F6 are exact
approved/registered Prime files and were never generated.

All four calls used these binding roles:

- approved Prime standing-front: identity, palette, rendering and F1 endpoint;
- registered Prime sitting-front: identity and exact F6 endpoint;
- historical `keeper_sit_front_f6.png`: choreography evidence only, with zero
  permitted pixel, anatomy, face or rendering reuse;
- the preceding generated pose where applicable: adjacency evidence only.

Every prompt required one isolated full-body front-facing Prime Keeper on a
genuinely transparent background, generous gutters, constant adult Prime
identity, the standard single-band uniform, rectangular eyes without glints,
separate moustache, closed mouth, established beard, exactly two arms and two
legs, planted boots, bilateral symmetry, no chair/prop/shadow/text, and smooth
high-resolution antialiased rendering matching the Prime endpoints.

## F2

First small movement after standing: knees just unlocked, pelvis and shoulders
lowered slightly together, elbows beginning to bend, hands moving inward and
down toward the front thighs; balanced anticipation, not yet a squat.

## F3

Controlled half-squat: pelvis and head lower without body scaling, knees open,
slight hip hinge, hands above the upper thighs, boots planted; clearly deeper
than F2 and higher than the seated endpoint.

## F4

Deep lowering: pelvis just above future support, knees farther bent and open,
torso upright, lower legs stable, hands settling onto upper thighs; not yet
seated.

## F5

Final pre-contact: almost the registered seated silhouette, but hips, head and
hands remain slightly higher and the knees retain a little extension so F6
visibly completes contact.

The raw generated sources are immutable inputs under `sources/generated/`.
The builder crops their alpha bounds and registers explicit widths/heights into
256×320 cells with Lanczos resampling. It performs no creative pixel warp.
