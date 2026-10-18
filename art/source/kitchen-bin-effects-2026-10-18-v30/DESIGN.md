# Kitchen bin V30 taller stench cloud source

This revision preserves the approved V28 bin and room PNGs, plus the V29 fly
strip, byte-for-byte. It changes only the reusable miasma silhouette.

- Native effect cell: 80 × 80 px with a transparent safety gutter.
- Playback: 40 frames at 4 fps, one seamless 10-second loop.
- Colour: exact V29 miasma RGBA palette only; no new effect colours.
- Silhouette: a continuous, overlapping translucent cloud rising to y=3 in
  its cell, versus y=18–22 in V29.
- Readability: roughly four times V29's opaque pixel area at native scale,
  with broken edges and transparent holes to avoid a solid cartoon bubble.
- Source: permanently connected to the overflowing bin opening.
- The bin object and rubbish spill remain static.

The deterministic source is `scripts/build_kitchen_bin_effects_v30.py`.
