# Deployment: workflow, retention and rollback

_Last updated 14 October 2026._

## Why this exists

On 14 October 2026 Vercel warned that the account had used its 10 GB of Hobby
deployment storage (Lighthouse Keeper alone: about 7.8 GB). Nothing was leaking:
every push to `main`, and every push to a `claude/*` or `codex/*` branch, built a
complete new deployment. Each one carries the whole `public/` folder (about
115 MB, three quarters of it `public/keeper-review`), and roughly 200 deployments
were made in a week. Each deployment is an immutable copy, so the storage added up.

## Vercel facts

| Item | Value |
| --- | --- |
| Team | `frankwwebster-4308's projects` (`team_UpVksYbRSmV1Yqak6TY6ocG6`) |
| Project | `lighthouse-keeper` (`prj_tlJx4kAYbll5Mq6xISKPrdXEWqX2`) |
| Production URL | https://lighthouse-keeper-mu.vercel.app |
| Production branch | `main` |
| Plan | Hobby |

## How deployment works now

**A push no longer deploys.** Vercel runs `scripts/vercel-ignore-build.mjs`
(wired up in `vercel.json` as the Ignored Build Step) before every Git build:

- A push to `main` builds **only** if the newest commit's subject line (its
  first line) **ends with** `[deploy]`. The marker anywhere else (mid-subject
  or in the body) is ignored, so writing about the workflow cannot trigger a
  release.
- Every other push to `main` is skipped.
- Branch pushes (`claude/*`, `codex/*`, anything not `main`) never build.

A skipped push still appears in the Vercel dashboard as **Canceled**. It has no
build output and uses no meaningful storage. That is expected.

Commit and push as often as you like. Release to production in batches, for
example once a review round is ready for Frank to look at.

### To deploy (Frank: no terminal needed)

Use whichever is easiest. All three do the same thing: they put one empty
commit marked `[deploy]` on top of `main`.

1. **Ask Claude or Codex: "deploy Lighthouse Keeper".** They run
   `npm run deploy -- "short note"`.
2. **One click on GitHub.** Go to the repository's **Actions** tab, choose
   **Deploy to production**, then **Run workflow**. A note is optional.
3. **By hand** (any agent or terminal): make the last commit of a push end its
   subject line with `[deploy]`.

The build takes a few minutes. When it finishes, production shows the new
version at the URL above.

### Rules for agents (Claude and Codex)

- Never end an ordinary commit subject with `[deploy]`.
- Batch review work. Deploy once per review round, not once per tweak.
- To show Frank a review page, deploy, then send the production link.
  Branch previews no longer exist.
- `npm run deploy` refuses to run with uncommitted changes or off `main`.
  It pulls first, because both agents push to `main`.

## Retention policy

Set on the project (Vercel → lighthouse-keeper → Settings → Security →
Deployment Retention Policy):

| Deployment state | Kept for |
| --- | --- |
| Canceled | 1 day |
| Errored | 1 day |
| Pre-Production (previews) | 1 day |
| Production | 1 week |

Whatever these periods say, Vercel always keeps the last 3 deployments and the
last 3 ready production deployments on Hobby, plus whichever deployment
currently serves production. So **at least three production versions are always
available to roll back to**, even after a quiet spell.

Expected steady state: three or four ~115 MB production deployments, about
0.5 GB, against 7.8 GB before.

## Rollback

Rolling back promotes an older production deployment that already exists.
Nothing is rebuilt, and it takes seconds.

- **Easiest:** ask Claude to roll back. Claude uses the Vercel connector to
  promote the previous production deployment.
- **Dashboard:** Vercel → lighthouse-keeper → Deployments. Find the version you
  want (production deployments show the commit message), open **⋯**, then choose
  **Instant Rollback** (or **Promote to Production**).
- **Limit:** Hobby's Instant Rollback goes back one production deployment at a
  time. Older retained versions can still be promoted from the Deployments page.
- **Already deleted?** Deleted deployments stay restorable for 30 days under
  Settings → Security → **Recently Deleted**.

After a rollback, `main` still holds the newer code. The next `[deploy]` will
release it again, so fix forward on `main` before deploying.

## State after the 14 October cleanup

- **Production:** commit `bf5075a`, the commit that introduced this workflow
  (deployment `dpl_83W6vQ9gQ7tyJcUJ8on6PUrfKMPe`). Its subject mentioned the
  marker mid-line, which the first version of the rule counted. The rule now
  requires the marker at the end of the subject.
- **Rollback candidates kept:** `abe2372` (`dpl_92escRn4NfBbcM3z3EP7LavLpAjJ`,
  production before this change), `65fe2ec` (`dpl_7z1DU7sjJCDg8PDAhuLtL7GUGgf2`)
  and `cca03dc` (`dpl_29EHFkfNdX3beJshRvsB2hpxpQJu`).
- The ~200 older deployments had already been removed by Vercel's 30-day Hobby
  retention. They sit in the 30-day recovery window, so the usage figure falls
  over the following days rather than instantly.
- No project, domain, production deployment or repository file was deleted.

## Remaining limitations

1. **Each release still copies all of `public/` (~115 MB).** The gate cuts the
   number of copies, not their size. The archive below fixes the size.
2. **Deleted deployments count for a while.** Usage reflects the recovery
   window, so expect the storage figure to drop over days, not minutes.
3. **No branch previews.** Review happens on production after a `[deploy]`. If
   isolated previews are ever needed, allow one named branch in
   `scripts/vercel-ignore-build.mjs` rather than re-enabling all branches.
4. **Dashboard redeploys.** "Redeploy" on a skipped commit is skipped too. Use
   `npm run deploy` or the GitHub button instead.

## Proposal: content-addressed review archive (not yet implemented)

Codex owns the review pages and their media (see `CLAUDE.md`), so this is a
proposal for Codex to implement, not a change made here.

**Measured on 14 October:** `public/` holds 924 files (116.5 MB). Only 628 are
unique by SHA-256; 26.5 MB is byte-identical duplicates. Among the review
folders, `public/keeper-review` is 75 MB, including `drafts/` at 21 MB. Review
assets already carry hash suffixes (`frame1-c097d78aac2d2c52.png`), so a
content-addressed layout is a small step from what exists.

**Design:**

1. **One store, keyed by hash.** Each review asset is stored once as
   `review-archive/objects/<sha256[0:2]>/<sha256>.<ext>`. The store stays in git,
   so all evidence is preserved, but sits outside `public/`, so it is not copied
   into deployments.
2. **One manifest per review set.** `review-archive/sets/<set-name>.json` maps
   each page path to its object hash. The review HTML is unchanged apart from its
   asset URLs.
3. **Host the store once, outside deployments.** Upload each object to Vercel
   Blob (or similar) a single time, named by its hash. Because the names never
   change, objects are never re-uploaded and can be cached forever. Deployments
   then carry only HTML and the active game sprites.
4. **Keep the live game lean.** `public/sprites` (38 MB, used by the game) stays
   in the deployment. Approved Final artwork stays where the game reads it.
5. **Verification.** A script checks that every manifest hash exists in the store
   and that every stored object's hash matches its name. Add it to `npm test`
   next to the existing `verify_keeper_*` scripts.

**Effect:** about 75 MB less per deployment (115 MB → about 40 MB). History
stops growing with each release, because identical frames are stored once
across all review versions.
