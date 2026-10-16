#!/usr/bin/env node
/** Run the existing suite with archive-backed compatibility for immutable paths. */
import { spawnSync } from 'node:child_process'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const hook = pathToFileURL(path.join(root, 'scripts/review_archive_fs_hook.mjs')).href
const nodeOptions = [process.env.NODE_OPTIONS, `--import=${hook}`].filter(Boolean).join(' ')
const foundation = spawnSync('node', ['scripts/verify_keeper_movement_foundation_v1.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (foundation.error) throw foundation.error
if (foundation.status !== 0) process.exit(foundation.status ?? 1)
const foundationV2 = spawnSync('node', ['scripts/verify_keeper_movement_foundation_v2.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (foundationV2.error) throw foundationV2.error
if (foundationV2.status !== 0) process.exit(foundationV2.status ?? 1)
const ovenApproach = spawnSync('node', ['scripts/verify_keeper_object_approach_oven_v1.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ovenApproach.error) throw ovenApproach.error
if (ovenApproach.status !== 0) process.exit(ovenApproach.status ?? 1)
const ovenPerspective = spawnSync('node', ['scripts/verify_keeper_object_approach_oven_v3.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ovenPerspective.error) throw ovenPerspective.error
if (ovenPerspective.status !== 0) process.exit(ovenPerspective.status ?? 1)
const ovenFloorSurface = spawnSync('node', ['scripts/verify_keeper_object_approach_oven_v4.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ovenFloorSurface.error) throw ovenFloorSurface.error
if (ovenFloorSurface.status !== 0) process.exit(ovenFloorSurface.status ?? 1)
const ovenVisibleFloor = spawnSync('node', ['scripts/verify_keeper_object_approach_oven_v5.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ovenVisibleFloor.error) throw ovenVisibleFloor.error
if (ovenVisibleFloor.status !== 0) process.exit(ovenVisibleFloor.status ?? 1)
const ovenVisibleFloorDelivery = spawnSync('node', ['scripts/verify_keeper_object_approach_oven_v6.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ovenVisibleFloorDelivery.error) throw ovenVisibleFloorDelivery.error
if (ovenVisibleFloorDelivery.status !== 0) process.exit(ovenVisibleFloorDelivery.status ?? 1)
const ovenRestrainedFloor = spawnSync('node', ['scripts/verify_keeper_object_approach_oven_v7.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ovenRestrainedFloor.error) throw ovenRestrainedFloor.error
if (ovenRestrainedFloor.status !== 0) process.exit(ovenRestrainedFloor.status ?? 1)
const liftEntry = spawnSync('node', ['scripts/verify_keeper_lift_entry_alignment_v1.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (liftEntry.error) throw liftEntry.error
if (liftEntry.status !== 0) process.exit(liftEntry.status ?? 1)
const circulationEntry = spawnSync('node', ['scripts/verify_keeper_circulation_entry_alignment_v1.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (circulationEntry.error) throw circulationEntry.error
if (circulationEntry.status !== 0) process.exit(circulationEntry.status ?? 1)
const stairAscent = spawnSync('node', ['scripts/verify_keeper_prime_stair_ascent_v1.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (stairAscent.error) throw stairAscent.error
if (stairAscent.status !== 0) process.exit(stairAscent.status ?? 1)
const stairAscentV2 = spawnSync('node', ['scripts/verify_keeper_prime_stair_ascent_v2.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (stairAscentV2.error) throw stairAscentV2.error
if (stairAscentV2.status !== 0) process.exit(stairAscentV2.status ?? 1)
const walkAwayApproval = spawnSync('node', ['scripts/verify_keeper_prime_walk_stop_turn_back_v3.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (walkAwayApproval.error) throw walkAwayApproval.error
if (walkAwayApproval.status !== 0) process.exit(walkAwayApproval.status ?? 1)
const stairTransitionsV6 = spawnSync('node', ['scripts/verify_keeper_prime_stair_transitions_v6.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (stairTransitionsV6.error) throw stairTransitionsV6.error
if (stairTransitionsV6.status !== 0) process.exit(stairTransitionsV6.status ?? 1)
const staircaseGeometryV1 = spawnSync('node', ['scripts/verify_keeper_staircase_geometry_v1.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (staircaseGeometryV1.error) throw staircaseGeometryV1.error
if (staircaseGeometryV1.status !== 0) process.exit(staircaseGeometryV1.status ?? 1)
const stairDescentV1 = spawnSync('node', ['scripts/verify_keeper_prime_stair_descent_v1.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (stairDescentV1.error) throw stairDescentV1.error
if (stairDescentV1.status !== 0) process.exit(stairDescentV1.status ?? 1)
const ladderTransitionsV1 = spawnSync('node', ['scripts/verify_keeper_prime_ladder_transitions_v1.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ladderTransitionsV1.error) throw ladderTransitionsV1.error
if (ladderTransitionsV1.status !== 0) process.exit(ladderTransitionsV1.status ?? 1)
const ladderTransitionsV2 = spawnSync('node', ['scripts/verify_keeper_prime_ladder_transitions_v2.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ladderTransitionsV2.error) throw ladderTransitionsV2.error
if (ladderTransitionsV2.status !== 0) process.exit(ladderTransitionsV2.status ?? 1)
const ladderTransitionsV3 = spawnSync('node', ['scripts/verify_keeper_prime_ladder_transitions_v3.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ladderTransitionsV3.error) throw ladderTransitionsV3.error
if (ladderTransitionsV3.status !== 0) process.exit(ladderTransitionsV3.status ?? 1)
const ladderTransitionsV4 = spawnSync('node', ['scripts/verify_keeper_prime_ladder_transitions_v4.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ladderTransitionsV4.error) throw ladderTransitionsV4.error
if (ladderTransitionsV4.status !== 0) process.exit(ladderTransitionsV4.status ?? 1)
const ladderTransitionsV4Approval = spawnSync('node', ['scripts/verify_keeper_prime_ladder_transitions_v4_approval.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ladderTransitionsV4Approval.error) throw ladderTransitionsV4Approval.error
if (ladderTransitionsV4Approval.status !== 0) process.exit(ladderTransitionsV4Approval.status ?? 1)
const ladderTransitionsV5 = spawnSync('node', ['scripts/verify_keeper_prime_ladder_transitions_v5.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ladderTransitionsV5.error) throw ladderTransitionsV5.error
if (ladderTransitionsV5.status !== 0) process.exit(ladderTransitionsV5.status ?? 1)
const ladderTransitionsV6 = spawnSync('node', ['scripts/verify_keeper_prime_ladder_transitions_v6.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (ladderTransitionsV6.error) throw ladderTransitionsV6.error
if (ladderTransitionsV6.status !== 0) process.exit(ladderTransitionsV6.status ?? 1)
const result = spawnSync('npm', ['run', 'test:core'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (result.error) throw result.error
process.exit(result.status ?? 1)
