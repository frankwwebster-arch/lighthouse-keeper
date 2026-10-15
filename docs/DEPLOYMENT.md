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

**Status (14 October 2026): not yet applied.** The policy can be changed only
in the Vercel dashboard (the API and connector cannot set it), and Claude in
Chrome is not permitted on vercel.com. Until it is set, Hobby's default of
30 days applies. The deploy gate already stops the growth; the shorter policy
only clears old builds faster.

Target policy (Vercel → lighthouse-keeper → Settings → Security →
Deployment Retention Policy → Save):

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

Expected steady state after the content-addressed archive release: three or four
~43 MB production deployments, about 0.2 GB, against 7.8 GB before.

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

## Initial state after the 14 October cleanup

This is the historical baseline before the content-addressed archive release;
the current production deployment should be checked in Vercel after each
explicit release.

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

1. **Deleted deployments count for a while.** Usage reflects the recovery
   window, so expect the storage figure to drop over days, not minutes.
2. **No branch previews.** Review happens on production after a `[deploy]`. If
   isolated previews are ever needed, allow one named branch in
   `scripts/vercel-ignore-build.mjs` rather than re-enabling all branches.
3. **Dashboard redeploys.** "Redeploy" on a skipped commit is skipped too. Use
   `npm run deploy` or the GitHub button instead.
4. **The archive host reads the public Git repository.** Review objects are
   immutable and addressed by full SHA-256, but availability still depends on
   GitHub's raw-content service. The manifest and short-lived redirect keep the
   host replaceable if Vercel Blob or another object store is preferred later.

## Content-addressed review archive (implemented 14 October 2026)

Keeper review media is now stored once outside `public/`, without deleting any
evidence or changing immutable review-page bytes.

**Measured result (15 October 2026, including Stair Ascent V6):** 689 review-
media paths collapse to 306 unique objects. The paths represent 83.23 MiB; the
unique store is 49.46 MiB. The real `public/` deployment payload remains about
45 MiB rather than roughly 115 MiB. The archive itself stays in Git but is
outside `public/`, so Vercel does not copy those objects into every deployment.

### How it works

1. **One store, keyed by hash.** Every review asset is stored as
   `review-archive/objects/<sha256[0:2]>/<sha256>.<ext>`. The store stays in git,
   so all evidence remains versioned and reversible.
2. **One manifest per review set.** The 44 files under
   `review-archive/sets/` map every legacy review path to its full object hash,
   byte length, repository object and external URL. `review-archive/index.json`
   is the deterministic route index and records aggregate savings.
3. **Immutable HTML stays immutable.** Historical review HTML and approval
   registers keep their original `/keeper-review/...` addresses and original
   SHA-256. Two narrow server routes resolve those addresses and return
   short-lived temporary redirects, so hosting can change without leaving a
   year-long redirect in a reviewer's browser cache. Unknown paths return 404.
4. **Objects are hosted once outside deployments.** The backend is GitHub's
   raw-content endpoint over the public repository. URLs include the full
   SHA-256 object filename. jsDelivr is deliberately excluded because it
   refuses uncached files once a repository package exceeds 50 MB. The backend
   remains declared in the manifests and can later be replaced with Vercel
   Blob without changing evidence bytes.
5. **Keep the live game lean.** `public/sprites` (38 MB, used by the game) stays
   in the deployment. Approved Final artwork stays where the game reads it.
6. **Verification and old contracts.** `scripts/verify_review_archive.mjs`
   checks every hash, filename, manifest, immutable page, absence from public
   and the sub-50-MiB payload boundary. The test-only filesystem hook lets old
   immutable verifiers resolve historical public paths from the archive;
   production uses redirects, never that hook.
7. **Playback waits for media.** New moving review pages preload and decode
   every unique frame before enabling their controls or starting playback.
   If an existing immutable page lacks that gate, publish a new versioned page
   with new asset paths; never overwrite the historical export or ask Frank to
   clear browser caches.

### Adding or rebuilding review media

Existing authoring scripts may write a new versioned candidate into
`public/keeper-review` for assembly. Before committing:

```sh
npm run archive:keeper-review
npm test
npm run typecheck
npm run build
```

The archive command copies only new hashes, updates the set/global manifests,
then removes public media copies. It never removes an old archive object, even
if a legacy path later points to a newer hash. Do not manually edit object
filenames or manifests. To change archive hosting, update the archive builder,
regenerate manifests, verify, then release one tested batch.
