# Keeper Prime side-right ↔ back Turn V1 handoff

Status: **draft awaiting visual approval**.

This pack joins the exact approved Side-right V1 proxy to the exact approved V5 rear endpoint in eight poses at 90°, 98°, 105°, 120°, 135°, 150°, 165° and 180°. The reverse strip is the exact reverse frame order. Every frame is 256 × 320, 298 pixels high, pinned to cap y=18 and floor y=316, and has a transparent safety gutter.

The six intermediate angular poses were independently drawn with the built-in image-generation workflow, then uniformly registered with Lanczos resampling. No creative pixel warp was used. A first 150° candidate was rejected because the face stayed too visible and the boots retained toe-facing construction. A first 165° candidate was rejected because its cap and upper-body silhouette would have snapped into the wider approved back endpoint. Both remain as rejected provenance.

Visual review should concentrate on the face and forward beard disappearing into rear hair, the cap badge disappearing, the widening from 135° through 180°, and both boots resolving into the approved rear boot backs. The registered height and floor are deterministic; perceived perspective continuity remains the visual approval gate.

Nothing in production, Final, the runtime manifest, prior authorities or prior review exports has changed.

The review page uses route-absolute asset URLs under its own versioned directory. This avoids Vercel's trailing-slash canonicalisation resolving animation frames one directory too high, and the verifier rejects any return to trailing-slash-dependent relative URLs.
