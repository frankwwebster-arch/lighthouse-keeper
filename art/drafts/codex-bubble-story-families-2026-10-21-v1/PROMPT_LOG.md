# Codex Bubble-story family expansion V1 prompt log

**Tool:** built-in image generation, 21 October 2026.

Every requested picture was generated in its own call. The exact per-picture
primary requests and original cache filenames are recorded in
`source-register.json`. The shared prompt contract was:

> Use case: stylized-concept
>
> Asset type: isolated game activity-callout token
>
> Primary request: Create exactly one [SUBJECT], immediately recognisable at
> small size: [THE RECORDED PRIMARY REQUEST].
>
> Scene/backdrop: genuinely transparent background, every pixel outside the
> object fully transparent.
>
> Style/medium: highly polished hand-painted 2D game illustration for a cosy
> maritime Lighthouse Keeper game; smooth anti-aliased contours; strong
> substantial dark-navy outer line; warm cream highlights; aged brass/copper,
> sea-glass teal, storm blue and restrained coral; subtle tactile painterly
> texture; friendly compact silhouette; matching established activity-callout
> tokens.
>
> Composition/framing: exactly one owned illustration or ordinary semantic set,
> centred, compact and readable at thumbnail size, with generous transparent
> margin on all four sides.
>
> Constraints: hard clean transparent cutout only; no person or Keeper unless
> the subject is the requested fictional pet; no room, table, floor, panel,
> word, letter, number, logo, brand, watermark, frame, vignette, halo, aura,
> background glow, cast shadow, detached fragment, duplicate object or
> unrelated prop.

Subject-specific constraints in the recorded requests governed safe hooks,
blank paper/canvas, unnumbered pub equipment, contained laboratory liquids and
the absence of detached effects. The pet figures are fictional archetypes, not
real animals or identifiable characters.

The first art-easel candidate (`exec-c9ec822d-5932-4c67-81c0-2a4a1d27d7b3.png`)
was rejected because visible alpha touched the top and bottom source edges. The
accepted retry asked for the complete table-top easel in the middle 70 percent
of the square canvas, every foot visible and at least 15 percent clear of all
edges. No generated subject was manually repainted. Deterministic processing
clears only alpha 8 or below, isolates the visible bounds, proportionally fits
the source into a 384-pixel review cell, and then fits the final into the
standard 256-pixel cell.
