# Kitchen v14 V3 — image-generation record

Tool: OpenAI built-in image generator.

## Production direction

The authored unit was the complete kitchen room, not an individual appliance
or cabinet. The approved v14 schematic was supplied only for geometry. The V8
furnished room and style test supplied shell, scale, line, palette and material
references. The older approved kitchen family supplied continuity principles
only; its royal-blue palette and obsolete layout were explicitly excluded.

The main room prompt required one coherent British lighthouse cottage kitchen:
matching duck-egg cabinetry, seamless pine worktop runs, consistent counter and
plinth heights, chunky cream appliances, copper hardware, shared line weight,
one upper-left light and silhouettes that survive lighthouse reduction. It
prohibited contact sheets, isolated-object presentation, mismatched styles,
cast shadows, gloss, chrome, skinny furniture, tables and chairs.

Targeted room-wide edits then:

1. removed the generated Keeper so the exact Prime could be registered later;
2. corrected the fridge from counter-height to tall and chunky;
3. corrected the left run to exactly three coherent modules;
4. aligned the Belfast sink, left window and matching wall cupboard;
5. narrowed and shifted the left window before exact approved-window
   registration in the deterministic build.

Selected source: `sources/imagegen/kitchen-v14-coherent-room-no-keeper.png`.
The build uses crop/scale/place/mask/assemble operations only and records the
source and output hashes in `manifest.json`.
