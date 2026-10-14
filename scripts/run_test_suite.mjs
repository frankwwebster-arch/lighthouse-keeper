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
const walkAwayApproval = spawnSync('node', ['scripts/verify_keeper_prime_walk_stop_turn_back_v3.ts'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (walkAwayApproval.error) throw walkAwayApproval.error
if (walkAwayApproval.status !== 0) process.exit(walkAwayApproval.status ?? 1)
const result = spawnSync('npm', ['run', 'test:core'], {
  cwd: root,
  env: { ...process.env, NODE_OPTIONS: nodeOptions },
  stdio: 'inherit',
})
if (result.error) throw result.error
process.exit(result.status ?? 1)
