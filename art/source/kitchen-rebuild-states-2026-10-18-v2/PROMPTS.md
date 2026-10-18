# Kitchen Rebuild V2 amendment prompts

Date: 18 October 2026

The built-in image editor received the exact transparent Rebuild V1 furniture
master as its edit target. Both prompts required the 2172 × 724 framing,
six-bay geometry, palette, projection, cabinetry and complete table/chair to
remain fixed.

## On-object amendment

The edit was limited to:

- recolour the closed fridge door to warm white/ivory enamel while retaining
  its hinges, copper handle, outline and dimensions;
- expose two modest browned toast tops in the existing toaster;
- turn on the existing oven with turned controls, a solid red indicator, warm
  cavity light and one simple roasting dish.

It explicitly prohibited steam, heat haze, water, smoke, sparks, puddles or
other effects because those remain separate layers.

Output: `generated/on-object-amendments-v1.png`
SHA-256: `f7e459c8c39db0fc77b995cbdcdc31b569eaf9f54c1267991e32e077ff445086`

## Broken-object amendment

The edit was limited to the existing objects:

- white fridge door with failed top hinge, credible lower-hinge connection,
  visible generic contents and flat floor puddle;
- kettle lid displaced onto the worktop;
- blackened toast;
- attached oven door open/down with exposed dark cavity;
- bowl split into two recognisable ceramic halves;
- failed tap outlet ready for an upward spray.

It explicitly prohibited environmental effects and retained the table/chair.

Output: `generated/broken-object-amendments-v1.png`
SHA-256: `8a3f278218711a4684e9fdc7bdf318d19af29d8d768342ed5c7def4a53a141d8`

## Environmental-effect references

A transparent three-cell On reference requested, left to right, small kettle
steam, toaster heat ribbons and gentle tap flow. A separate six-cell Broken
reference requested fridge drip/ripple, open-kettle steam, toast smoke, oven
smoke, upward water spray and warning/cavity light. The On reference supplies
the production steam/heat/water silhouettes. The Broken sheet is retained as
visual provenance; deterministic connected native-scale effects implement its
effect grammar without importing the sheet's background.

- `generated/on-effects-reference-v1.png` — `fb76d72ac18bbbdc1dbd5235c30e4f3824e3ebf2f6f107eed1b29fa5aecc6e5f`
- `generated/broken-effects-reference-v2.png` — `a0b422980d159cffaba8fb8b782a4a8a2f21670b53cbf9c5136cbfe3caf68248`
