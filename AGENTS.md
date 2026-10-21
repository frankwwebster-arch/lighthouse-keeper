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
`review-archive/objects`, never as a committed public binary. Oversized review
JSON (24 KiB or more) uses the same archive; small JSON remains public. After
any review builder writes evidence, run `npm run maintain:keeper-review`; it
deduplicates the bytes, updates the per-set manifests, removes only verified
public copies and checks the deployment payload. `npm test` fails if an
archiveable review payload returns or an archive hash/manifest is wrong.
Every new moving review page must preload and decode all unique frame URLs
before enabling controls or starting playback. Use a fresh versioned page and
asset prefix when correcting delivery; never rewrite an immutable old page.

Roles and other project rules: `CLAUDE.md` and `docs/CODEX_TO_CLAUDE_HANDOFF_2026-10-14.md`.
