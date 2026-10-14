#!/usr/bin/env node
// Vercel "Ignored Build Step" for Lighthouse Keeper.
//
// Vercel runs this before every Git-triggered build (see vercel.json
// "ignoreCommand"). Exit code 0 tells Vercel to SKIP the build; exit code 1
// tells it to BUILD. A skipped build is recorded as Canceled and stores no
// build output, so it costs no deployment storage.
//
// Rule: build only when the SUBJECT LINE (first line) of the newest commit on
// `main` ends with the marker "[deploy]". Mentioning the marker anywhere else
// (mid-subject, or in the body) does not count, so prose about the workflow
// cannot trigger a release by accident. Every other push (ordinary work on
// main, and all branch pushes such as claude/* or codex/*) is skipped.
//
// See docs/DEPLOYMENT.md for the full workflow.

export const DEPLOY_MARKER = '[deploy]'
export const PRODUCTION_BRANCH = 'main'

/**
 * @param {{ ref?: string, message?: string }} input
 * @returns {{ build: boolean, reason: string }}
 */
export function decide({ ref = '', message = '' } = {}) {
  if (ref !== PRODUCTION_BRANCH) {
    return {
      build: false,
      reason: `Branch "${ref || '(none)'}" is not ${PRODUCTION_BRANCH}; branch pushes never deploy.`,
    }
  }
  const subject = message.split(/\r?\n/, 1)[0].trim().toLowerCase()
  if (!subject.endsWith(DEPLOY_MARKER)) {
    return {
      build: false,
      reason: `Latest commit subject does not end with ${DEPLOY_MARKER}; skipping. Run "npm run deploy" to release.`,
    }
  }
  return { build: true, reason: `${DEPLOY_MARKER} marker found on ${PRODUCTION_BRANCH}; building.` }
}

const invokedDirectly = process.argv[1] && import.meta.url === new URL(`file://${process.argv[1]}`).href

if (invokedDirectly) {
  const result = decide({
    ref: process.env.VERCEL_GIT_COMMIT_REF,
    message: process.env.VERCEL_GIT_COMMIT_MESSAGE,
  })
  console.log(`[vercel-ignore-build] ${result.reason}`)
  process.exit(result.build ? 1 : 0)
}
