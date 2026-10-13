# Keeper Prime Rig Motion V3 handoff

Status: **slower walk-cadence revision awaiting Frank's visual review**.

Frank judged V2 otherwise very good but asked for more leg movement, more steps and a slower crossing. V3 changes only the walk. Idle, reach and planted-ankle sit/stand remain byte-for-byte identical as motion records.

The walk now takes five seconds rather than two, contains four complete gait cycles/eight implied steps rather than one cycle/two steps, and travels at 168 px/s rather than 420 px/s. Thigh swing increases from 25° to 32° and maximum knee lift from 34° to 44°. Root travel remains 840 px, starting and ending fully hidden.

Review `/keeper-review/keeper-prime-rig-v3/`. This is still a construction mannequin, not finished Keeper artwork, and nothing is promoted.

Rebuild with `/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_rig_motion_v3.py` and verify with `npm run verify:keeper-prime-rig-v3`.
