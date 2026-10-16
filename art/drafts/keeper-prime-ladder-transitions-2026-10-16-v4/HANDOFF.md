# Keeper Prime ladder transitions V4

V4 supersedes V3 for review. It restores each original source frame's smooth antialiased fringe, raises only solid paint (alpha >= 240) to fully opaque, and retains all RGB values. The complete ladder is never masked. The review compositor decodes and mounts all 29 unique frames before playback, then performs atomic visibility switches without recreating either the Keeper or architecture. V2/V3 timing, frame order, roots, geometry and accepted hand/foot-to-rung tolerance remain exact. Nothing is promoted.

Review: `/keeper-review/keeper-prime-ladder-transitions-v4/`.
