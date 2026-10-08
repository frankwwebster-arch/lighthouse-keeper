# Source provenance and review decisions

The three `tv-original-*-source.png` files are copies of the project's previously created isolated `style_b_pixel/obj_tv_*_ai.png` drafts. Frank explicitly selected these as the style guide. The standard casing is the production master; state-specific screen artwork is registered inside it. All tiers and future items should follow this original CRT's detailed, sharp pixel style, subject to Frank's review.

`lantern-inset-source.png` is the corrected isolated image-generation result: inset glazed iron lantern chamber and exterior wraparound walkway, matching the full lighthouse reference. Its roof, active lamp and telescope are separate renderer elements. Export crop/size and anchors are recorded in `export-contract.json`.

`room-lamp-source.png` (full-width domestic room), `lantern-inset-alpha-defect-source.png`, `tv-rejected-transparent-screen.png`, `tv-basic-source.png`, `tv-registered-source.png`, `tv-registration.json`, `rejected-coarse/` and `rejected-design/` are rejected studies. They are retained for audit and never consumed by the current conversion script. No concept plate is sliced into production assets.

`build_catalogue_asset_batch.py` reproduces the approved-master conversion, the supplied BBC NEWS reference reworked into the literal `B B SEA` wordmark, NEWS title and newsreader head, a single damaged TV frame, and shared smoke/sparks strips. Four ON frames form one animated channel state. Sports is football; Nature shows penguin and gull. The mark is a deliberately tiny broadcast graphic within the actual CRT screen, not a separately scaled logo asset.

Pixel review controls let Frank soften sharpness through integer source-pixel blocks without changing logical dimensions. Any edited export needs inspection and reintegration through the same sidecar pipeline. The image-generation workflow produced isolated source images; deterministic conversion is handled by Pillow and the established sprite pipeline. Final delivery candidates remain pending Frank's review.
