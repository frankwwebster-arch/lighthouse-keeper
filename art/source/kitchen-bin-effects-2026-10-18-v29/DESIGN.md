# Kitchen bin V29 effect source

This revision preserves the four approved V28 bin and room PNGs byte-for-byte.
It replaces only the reusable environmental overlays.

- Native effect cell: 80 × 80 px with a transparent safety gutter.
- Playback: 40 frames at 4 fps, one seamless 10-second loop.
- Miasma: restrained olive/grey-green ribbons, low contrast, irregular edges,
  sparse dissipation pixels, and a permanent throat anchored to the bin opening.
- Flies: three subdued insects moving on shallow, slow ten-second orbits.
- The bin object has no animated pixels.
- Placeholder fly SFX cue: `kitchen_bin_flies_slow_loop`.

The deterministic source is `scripts/build_kitchen_bin_effects_v29.py`. Rebuilds
must retain the pinned V28 hashes declared there.
