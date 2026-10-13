# Prompt log — Keeper Prime orthographic views V4

Built-in image editing was used on 13 October 2026 after Frank identified that
the V2 rear elevation retained front-facing feet.

The V2 back was the edit target. The legacy back was supplied only as rear-boot
orientation evidence. The first prompt required rear heel counters, vertical
back seams and rear sole edges. Its result improved orientation but retained
rounded heel panels that could still read as toe caps, so it is preserved under
`rejected-sources/`. A second, tighter edit required flat squared heel backs,
straight rear seams, rectangular heel-counter panels and visible rear heel
blocks, while explicitly forbidding every rounded or domed toe-like panel.
Both prompts forbade vamp highlights, shoelaces, side-facing feet and any change
above the knees, and preserved smooth rendering, exact pose, single broad
stripe, height, centreline, floor contact, silhouette and transparency.

The generated full-resolution edit is preserved in `sources/`. The deterministic
builder normalizes it, transfers only rows 273–315 into the immutable V2 back,
and copies the approved-front alpha exactly. This keeps rows 0–272 byte-identical
to V2 and makes the correction reversible.
