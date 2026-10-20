# Claude BBQ tools and ephemera pack V1 prompt log

**Tool:** built-in image generation, 20 October 2026.

The accepted outputs used the existing BBQ food contact sheet as a style-only
reference. The pack records each original generated PNG SHA-256 and geometry,
fits its visible alpha proportionally inside a 384 × 384 transparent canvas,
and stores that review source as lossless WebP. Final 256 × 256 PNG
normalization is deterministic. No generative edit follows source acceptance.

Every prompt shared this production specification:

> Use case: stylized-concept. Asset type: independently controllable 2D game activity-callout prop. Input image: style reference only; do not copy its subjects. Style/medium: match the reference's polished hand-drawn comic illustration, bold dark navy outer line, warm saturated colour, restrained highlights and soft internal shading. Scene/backdrop: genuinely transparent background. Composition/framing: one complete isolated object centered, slight three-quarter view, generous transparent safety gutter on every side; nothing touches or crosses the canvas edge. Lighting/mood: cheerful, clean and readable at small size. Constraints: exactly one object; preserve a clean silhouette; no text; no letters; no logo; no watermark; no frame; no checkerboard; no background; no extra objects.

The individual primary requests were:

1. **BBQ tongs:** long stainless-steel locking barbecue tongs with dark navy-blue rubber grips and a small orange accent near the hinge.
2. **Slotted turner:** broad stainless-steel slotted barbecue turner spatula with a dark navy-blue handle and a small orange end accent.
3. **Basting brush:** silicone barbecue basting brush with orange bristles, a dark navy-blue handle and a small steel collar.
4. **Grill fork:** sturdy two-prong stainless-steel barbecue carving fork with a dark navy-blue handle and a small orange end accent.
5. **Heatproof mitt:** single quilted heatproof barbecue mitt, dark navy-blue fabric with orange binding and a small hanging loop.
6. **Charcoal chimney:** compact metal charcoal chimney starter with a dark navy-blue heat shield, orange grip accent, visible charcoal pieces inside but no flame or smoke.
7. **Skewer bundle:** one bundle of three reusable stainless-steel barbecue skewers held together as a single tidy prop, pointed tips aligned, dark navy-blue loop handles with small orange accents, completely empty with no food.
8. **Charcoal bag:** one sealed upright paper bag of lumpwood charcoal, dark navy-blue and warm orange packaging with only a simple black charcoal-lump pictogram; absolutely no writing or lettering.

The last four prompts additionally prohibited cast shadows or glows extending
away from the object. Low-alpha generation residue was removed during the
documented source isolation pass; no painted subject pixels were redrawn.
