# Keeper Prime side-right ↔ back Turn V3 handoff

Status: **full standard-outfit palette correction awaiting visual approval**.

Frank identified that the F8 trousers and boots were darker as well as the jumper, and directed that standard-outfit colours remain consistent in every animation. V3 therefore treats the cap crown, cap band, jumper blue, cream band, trousers and boots as six separately masked palette components. F7 is the moving palette authority for this review candidate.

Frames 1–7 are byte-identical to V2. F8 retains exact V2 geometry and alpha. Only pixels inside the registered outfit-component masks may change. The generated full-outfit edit is retained as colour evidence only and rejected as geometry because it redrew the Keeper.

If Frank approves V3, its component medians become the standard-outfit palette target for later animation drafts. Each new batch must register component masks and pass deterministic colour, geometry, transparency and unchanged-pixel checks. Pose shading may vary within the registered distribution, but the outfit may not flash darker between frames.

Nothing in V1, V2, the approved rear master, Final, production or the runtime manifest has changed.
