# Keeper Prime Rig Motion V2 handoff

Status: **construction motion awaiting Frank's visual review**.

Frank approved KP Rig V1 on 13 October 2026 with the exact wording: “Approve KP Rig V1, let's see it animated”. The approved V1 review pack and rig JSON remain byte-for-byte unchanged. This successor pack demonstrates the registered skeleton as a simplified construction mannequin; it is not finished Keeper artwork.

Review `/keeper-review/keeper-prime-rig-v2/` for four deterministic clips: restrained idle, a walk with 840 px of root travel that begins and ends fully off-stage, a controlled right-hand reach, and a sit-to-stand proof with both ankles planted. Every sampled upper arm, forearm, wrist-to-palm, thigh and shin uses the fixed KP Rig V1 length.

Approval of this motion proof authorizes a separate smooth side-right artwork candidate aligned to all 15 registered y-datums. It does not approve any finished animation and does not permit production promotion.

Rebuild with:

`/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_rig_motion_v2.py`

Verify with `npm run verify:keeper-prime-rig-v2`.

Rollback is deletion of this V2 draft directory and `public/keeper-review/keeper-prime-rig-v2/` only.
