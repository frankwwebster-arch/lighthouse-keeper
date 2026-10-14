import { describe, expect, it } from 'vitest'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { decide } from './vercel-ignore-build.mjs'

const script = fileURLToPath(new URL('./vercel-ignore-build.mjs', import.meta.url))

function exitCode(env: Record<string, string>): number {
  try {
    execFileSync(process.execPath, [script], { env: { ...process.env, ...env }, stdio: 'pipe' })
    return 0
  } catch (error) {
    return (error as { status: number }).status
  }
}

describe('vercel ignored build step', () => {
  it('skips ordinary pushes to main', () => {
    expect(decide({ ref: 'main', message: 'Add Keeper timing lab' }).build).toBe(false)
  })

  it('builds main when the latest commit carries the deploy marker', () => {
    expect(decide({ ref: 'main', message: 'Deploy: review batch 3 [deploy]' }).build).toBe(true)
    expect(decide({ ref: 'main', message: 'Release\n\nbody [DEPLOY]' }).build).toBe(true)
  })

  it('never builds branch pushes, even with the marker', () => {
    expect(decide({ ref: 'claude/furniture-locomotion', message: 'x [deploy]' }).build).toBe(false)
    expect(decide({ ref: 'codex/review', message: 'x [deploy]' }).build).toBe(false)
  })

  it('skips when Vercel supplies no git metadata', () => {
    expect(decide({}).build).toBe(false)
  })

  it('uses Vercel exit-code semantics: 0 skips, 1 builds', () => {
    expect(exitCode({ VERCEL_GIT_COMMIT_REF: 'main', VERCEL_GIT_COMMIT_MESSAGE: 'tweak' })).toBe(0)
    expect(exitCode({ VERCEL_GIT_COMMIT_REF: 'main', VERCEL_GIT_COMMIT_MESSAGE: 'Deploy [deploy]' })).toBe(1)
  })
})
