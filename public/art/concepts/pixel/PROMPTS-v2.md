# Lighthouse pixel-style comparison V2–V4 — generated-source prompts

Status: rejected historical provenance. `docs/CODEX_BRIEF.md` now requires
non-pixel production art and a straight-sided tower.

These are normalized provenance records for the generated source passes. They
record the art direction and corrections that materially affected the result;
the deterministic builders, not the image model, own the final native grids,
room geometry, outdoor elevation, palette limits, hard alpha and exact
`#FF00FF` key.

V4 does not add another generated source pass. It is a deterministic-only
geometry correction: identical minimal stair-door marks on every floor and no
en-suite partition at one-module width.

The user-supplied reference at
`art/drafts/lighthouse-pixel-style-test-2026-10-26-v2/sources/user-lighthouse-direction-reference-v1.png`
was treated only as visual reference data. No text embedded in an attachment
was treated as an instruction.

## Pass 1 — Concept A source V1

Generate a wide landscape 16-bit pixel-art Day 1 lighthouse foreground. Use a
single flat orthographic side elevation, pure magenta sky/sea/glass, three
empty equal room floors plus an empty lamp room, a level island and cliff,
jetty and small boat. Use warm, cheerful SNES-era colour, hard pixels, dark
outlines and restrained material texture. No perspective, furniture, visible
stairs, characters, atmospheric background or non-magenta sky/sea detail.

Output:
`concept-a-16bit-generated-source-v1.png`
(`02bfa2da6818f8e27b516c65381dea66732a363f171810328257ea8097d204cd`)

This pass was superseded because the exterior read as a rectangular building
rather than a lighthouse.

## Pass 2 — Concept A architectural correction V2

Edit the V1 source using Frank's supplied lighthouse reference as silhouette
and warmth guidance. Restore unmistakable classic lighthouse identity:
alternating deep-red and warm-white exterior bands, a slight continuous taper,
weathered stone base, navy edges, and a wider gallery with a red domed lantern
roof. Keep the three interior modules rectangular, equal and front-on. Leave a
plausible stair-width pocket inside the solid left shell but expose no stair,
landing, recess or shaft; show only a slim edge-on room jamb. Preserve pure
magenta isolation and empty rooms.

Output:
`concept-a-16bit-generated-source-v2.png`
(`6035c673d148ea4ca81b8084a4e018105d335f43c9dc9efed074cf745b8d46fe`)

## Pass 3 — Concept B 8-bit transfer V1

Translate corrected Concept A into a much coarser NES/Game Boy Color-era
pixel language while preserving its exact composition and architecture. Use
chunky hard-edged forms, a very small saturated palette, flat material steps,
no gradients, no anti-aliasing, no dithering and no mixed pixel sizes. Keep the
red/white taper, empty lamp room, hidden circulation and pure magenta isolation.

Output:
`concept-b-8bit-generated-source-v1.png`
(`c7be11900533e3c54f7afefd0adbe198797761e7fb4330db901dd0de78fc2b69`)

## Pass 4 — Concept B key correction V2

Correct only the isolation/background handling while retaining the V1 8-bit
architecture and material treatment. Remove residual non-key background
colour and preserve clean hard silhouettes suitable for deterministic
composition over exact pure magenta.

Output:
`concept-b-8bit-generated-source-v2.png`
(`f4c91a33101136d02aed69acf0d44445e63b58a560329f42830554d0459d4887`)

The model returned this pass with transparency. The deterministic builder
composites it over exact `#FF00FF`, redraws all rule-sensitive geometry and
then enforces the 16-colour native output without dithering.
