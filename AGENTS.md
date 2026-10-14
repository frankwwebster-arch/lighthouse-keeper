# Lighthouse Keeper: notes for coding agents (Codex and others)

**Deployment is manual.** Pushing to `main` does not deploy. Vercel builds only
when the newest commit on `main` has a subject line ending in `[deploy]`; branch
pushes never build.

- Commit and push freely, but never end an ordinary commit subject with `[deploy]`.
- Release once per review batch: `npm run deploy -- "short note"` (it pulls,
  adds an empty `[deploy]` commit and pushes). Frank can also use GitHub →
  Actions → "Deploy to production".
- Branch previews no longer exist. To show Frank a review page, deploy, then
  send the production link.
- Full workflow, retention policy and rollback: `docs/DEPLOYMENT.md`.

**Review media is content-addressed.** Review HTML and small JSON files remain
under `public/keeper-review`, but PNG/GIF/JPEG/WebP/AVIF evidence belongs in
`review-archive/objects`, never as a committed public binary. After any review
builder writes media, run `npm run archive:keeper-review`; it deduplicates the
bytes, updates the per-set manifests and removes the public copies. `npm test`
fails if public review media returns or an archive hash/manifest is wrong.

Roles and other project rules: `CLAUDE.md` and `docs/CODEX_TO_CLAUDE_HANDOFF_2026-10-14.md`.
