# Keeper Prime Walk V2 routing wrapper

Walk V2 changes no artwork. It copies every published Walk V1 review asset
byte-for-byte and changes only the review page's asset addresses from relative
`assets/...` paths to absolute
`/keeper-review/keeper-prime-walk-v2/assets/...` paths.

Vercel canonicalizes the public directory URL by removing its trailing slash.
Under that URL, a relative path resolves incorrectly beneath
`/keeper-review/assets/` and returns 404. Absolute paths make the review page
independent of trailing-slash behavior.

Status: technical review wrapper, awaiting the same visual decision as Walk
V1. No raw sprite, runtime sprite, manifest, workbench Final entry, source art
or V1 file changed. Roll back by deleting only this V2 draft and public folder.
