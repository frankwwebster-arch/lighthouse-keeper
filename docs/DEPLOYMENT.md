# Deployment: workflow, retention and rollback

_Last updated 25 October 2026._

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
- Batch review work sensibly, but do not ask Frank to authorise a review-page
  deployment. When a new versioned candidate is ready for inspection, deploy
  its reviewer, verify it, open it in the frame reviewer, and send Frank the
  production link before requesting any visual decision. Branch previews no
  longer exist.
- A review-page deployment is not artwork approval or promotion. Final,
  runtime and production-art promotion still require Frank's explicit
  approval.
- `npm run deploy` refuses to run with uncommitted changes or off `main`.
  It pulls first, because both agents push to `main`.
- `npm run deploy`, archive maintenance and the archive verifier all reject any
  new review page containing a relative `assets/...` URL. Vercel removes
  trailing slashes from static review-page URLs, so new payload references must
  be root-absolute: `/keeper-review/<set>/assets/<name>`. Historical pages are
  grandfathered only at their exact combined hash; changing one or adding a
  new relative reference fails before a deploy marker can be created. The same
  policy runs in the GitHub deployment action and Vercel's ignored-build gate,
  so manually authored deploy commits cannot bypass it.

## Retention policy

**Status (checked 25 October 2026): applied.** The project's
`deploymentExpiration` setting reads `expirationDays: 1`,
`expirationDaysCanceled: 1`, `expirationDaysErrored: 1`,
`expirationDaysProduction: 7` and `deploymentsToKeep: 10`, which matches the
target below. (On 14 October it was not yet set; it was applied in the
dashboard some time after.) The policy can be changed only in the Vercel
dashboard, and Claude in Chrome is not permitted on vercel.com. To read the
current setting:
`npx vercel api "/v9/projects/prj_tlJx4kAYbll5Mq6xISKPrdXEWqX2?teamId=team_UpVksYbRSmV1Yqak6TY6ocG6"`
and look at `deploymentExpiration`.

Policy (Vercel → lighthouse-keeper → Settings → Security →
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

Expected steady state after the content-addressed archive release: three or four
~45 MiB production deployments, about 0.2 GB, against 7.8 GB before.

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

## Clean-up of 25 October 2026

Approved by Frank on the project page (answers v1 and v2) after a read-only
safety check. Removed with the Vercel CLI (already signed in as
`frankwwebster-4308`), one deployment ID per call, with `--safe` (skip anything
with an active alias). Never `vercel remove <project-name>`: that removes every
deployment of the project.

- **Before:** 45 deployments, all from 23–25 October (24 READY production
  releases, 21 CANCELED skipped pushes). No tool reports per-deployment
  storage; each release carries 47–50 MiB of `public/` plus functions, so
  roughly 55–60 MB each, about 1.4 GB in all. The other 25 projects on the
  account keep about 3 deployments each.
- **Removed (31):** every deployment created before 24 October 18:18 UTC that
  was not the live one or one of the three previous releases: 16 READY
  releases (about 0.9 GB) and 15 CANCELED pushes, from `da1922e`
  (`dpl_4YePeNcHuTfDPga46MGBVADXFJ9U`, 23 Oct 09:45 UTC) to `65f097c`
  (`dpl_Fxww8gtNjX36mjpGYyrJoDgC4PXw`, 24 Oct 11:52 UTC). All 31 reported
  success; none was skipped. They are restorable until about 24 November under
  Settings → Security → Recently Deleted.
- **Kept (14):** production `03f6661` (`dpl_8kZ7UVnouiJMBBrKsmT73rsVUXHt`,
  Kitchen V13), the rollback versions `2a65167`
  (`dpl_6ZLQs7a5rjoookxHV2GicLWK5485`, Kitchen V12), `0f32be8`
  (`dpl_HBASgvRdKT9KqQ9fcFHGTEMC9cm8`, Kitchen V11) and `7e4983b`
  (`dpl_FDdxEkKvZ8wadDj48fqu7khffgeo`, Kitchen V10), and everything else from
  the 24 hours before the plan (four more releases, six skipped pushes).
- **Verified afterwards:** production is still `dpl_8kZ7…` and READY, with the
  live alias; the three rollback versions are READY; the game, `/studio`,
  `/studio/stories` and `/keeper-review/kitchen-room-layout-v13` load; 20
  random review and bubble-picture addresses return byte-identical pictures
  (SHA-256 checked). The deploy gate's 6 tests pass.
- **Not changed:** the project, domains, environment variables, retention
  policy, either desk's unsaved files or stashes, and the live database.
- **Known, not caused by this clean-up:** `/keeper-review/kitchen` returns 404.
  Codex removed that redirect (to the retired cabinetry review) in `d0c7179`
  on 24 October; the current kitchen review is `kitchen-room-layout-v13`.

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

**Measured result (21 October 2026):** 4,751 review-evidence paths across 197
sets collapse to 2,900 unique objects. The paths represent 360.72 MiB; the
unique retained store is 205.03 MiB. The clean-checkout `public/` deployment
payload is 45.04 MiB, 4.96 MiB below the unchanged 50 MiB repository guard
and down from the exact 53.3148 MiB failure baseline. The archive itself stays
in Git but is outside `public/`, so Vercel does not copy those objects into
every deployment.

### How it works

1. **One store, keyed by hash.** Every review asset is stored as
   `review-archive/objects/<sha256[0:2]>/<sha256>.<ext>`. The store stays in git,
   so all evidence remains versioned and reversible.
2. **One manifest per review set.** The files under
   `review-archive/sets/` map every legacy review path to its full object hash,
   byte length, repository object and external URL. `review-archive/index.json`
   is the deterministic route index and records aggregate savings.
   Retired evidence may remain in `review-archive/objects` without an active
   legacy path. `review-archive/retired` preserves its pages and old manifests;
   the archive index counts those retained object bytes but the resolver cannot
   publish them.
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
5. **Keep the live game lean.** `public/sprites` (36.9977 MiB, used by the game)
   stays in the deployment. Approved Final artwork stays where the game reads
   it. The archive also moves review-only JSON/JSON.GZ at or above 24 KiB while
   leaving HTML and small JSON public at their historical URLs. The one larger
   public exception is a hash-pinned shared V6 activity contract required by
   immutable approval verifiers.
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
8. **New payload URLs are root-absolute.** Static pages are served from a URL
   without a trailing slash, so `assets/name.png` resolves outside the review
   set. Use `/keeper-review/<set>/assets/name.png`. A fail-closed legacy-page
   tree hash in `scripts/review_page_url_policy.mjs` lets immutable old pages
   remain while preventing new relative references during archive maintenance,
   tests and `npm run deploy`.

### Adding or rebuilding review media

Existing authoring scripts may write a new versioned candidate into
`public/keeper-review` for assembly. Before committing:

```sh
npm run maintain:keeper-review
npm test
npm run typecheck
npm run build
```

When other untracked review work is present, replace only the intended set from
its reversible batch register instead of letting the global sweep absorb those
unrelated files:

```sh
npm run archive:keeper-review:set -- path/to/batch-register.json HEAD
```

That command starts from the named Git base, replaces just the register's set,
and computes committed-tree object statistics from the base plus that set. It
does not delete or stage unrelated archive objects or set manifests.

The archive command copies only new hashes and updates the set/global
manifests. Before removing a public copy it re-reads both manifests and proves
the stored object has the expected SHA-256. It never removes an old archive
object, even if a legacy path later points to a newer hash, and it ignores
unrelated untracked archive objects. The verifier rejects public review media,
oversized review data, broken manifest/object hashes, unresolved literal review
URLs and a `public/` payload at or above 50 MiB. Its payload diagnostic is about
`public/` only—not total repository size, `review-archive/`, or `art/drafts/`.
Do not manually edit object filenames or manifests. To change archive hosting,
update the archive builder, regenerate manifests, verify, then release one
tested batch.
