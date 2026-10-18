# Kitchen Rebuild V1 generation prompts

Date: 18 October 2026

## Unified standard-room master

The image model was asked for one new straight-on panoramic kitchen drawing,
not an edit or collage. The prompt fixed six equal fitted bays in this order:
closed fridge, off kettle, off toaster, off oven with integrated hob, intact
mixing bowl, and dry basin. It required one uninterrupted sea-glass worktop,
one aligned storm-blue fascia, one common recessed plinth, an empty far-left
zone for the separately retained bin, and one complete rear-facing chair at a
one-person table on the right. It prohibited extra props, duplicated assets,
floating objects, visible effects, labels, people and watermarks.

The requested visual language was polished crisp pixel art with dark navy
outlines, restrained cream plaster and terracotta flooring, warm copper/orange
details and expressive classic British/French comic character. All components
had to share one drawing language, scale and projection.

Generated source:

- `generated/full-standard-kitchen-master-v1.png`
- SHA-256 `a6f0b8d3d8181096e0455effc2753630ad893c34760c68a20fb40baedb60b48d`

## Transparent furniture extraction

The same generated image was supplied back to the model with a
background-extraction request. It was instructed to remove only the cream wall
and terracotta floor, retain the complete six-bay run plus complete table and
chair exactly as drawn, preserve proportions/positions/colours/outlines, and
produce genuine transparency without adding or repairing anything.

Generated source:

- `generated/full-standard-kitchen-transparent-v2.png`
- SHA-256 `3a4430a0d07be4a945e00ba717d2f23e55e8730ba63b420efa41aaa3c283a9f1`

The deterministic builder registers that single furniture drawing to the
historical 772 × 224 room contract. No alternate state was generated in this
gate.
