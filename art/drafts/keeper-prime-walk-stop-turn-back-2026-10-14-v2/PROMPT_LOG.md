# Prompt and provenance log

- User report, 14 October 2026: “new animation is half doing that vercel
  flickering problem, 404 or whatever it is”.
- Diagnosis: all playback frame paths resolved, but animation began before the
  redirected images had loaded. The first archive host also rejects uncached
  repository objects once the repository exceeds its 50 MB package limit.
- Correction: preserve exact V1 artwork and timing; publish new V2 asset paths;
  use GitHub's raw content endpoint; use a temporary, replaceable redirect;
  preload and decode all moving frames before playback.
- Rejected approach: modifying the immutable V1 review export or asking the
  reviewer to clear browser caches.
