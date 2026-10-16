# Keeper Prime ladder transitions V3

V3 removes V2's rectangular rung occluder completely. Every ladder rail and rung is drawn in every frame. Each of the 29 unique Keeper review images is instead alpha-normalized after registration: alpha >= 128 becomes fully opaque, alpha < 128 becomes fully transparent, and RGB is unchanged for every retained pixel. V2 timing, frame order, roots, geometry and accepted hand/foot-to-rung tolerance are exact. Nothing is promoted.

Review: `/keeper-review/keeper-prime-ladder-transitions-v3/`.
