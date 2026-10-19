# Activity Cloud Composer V3 — album-sleeve homages

**Status:** immutable, reversible review candidate built 19 October 2026; not
approved, promoted, deployed or connected to runtime recipes.

## Change from V2

V3 preserves Composer V2's 74 components, Prime rear-work body, complete route,
default Garden BBQ recipe, 42-frame callout timing and interface behaviour. It
adds twelve independently selectable album-sleeve homages to the `music`
family:

- Sgt. Pepper, Morning Glory, Screamadelica and the Velvet Underground banana;
- London Calling, Dark Side of the Moon, Abbey Road and Tapestry;
- Sticky Fingers, Never Mind the Bollocks, Born in the U.S.A. and Nevermind.

The sleeves are recognisable through simplified composition, colour and object
motifs. They do not reproduce titles, artist names, logos, copied typography,
photographs or real-person likenesses. The Nevermind homage replaces the
original child subject with a fully clothed generic adult swimmer.

## Boundaries

- Composer V1 and V2 remain immutable and independently discardable.
- Each generated source, derived component, public reference and archive object
  is SHA-256 pinned.
- Each sleeve owns exactly one isolated 256 × 256 cell with at least a 16-pixel
  transparent gutter.
- Turntable, household asset, Keeper body, sleeve tokens and SFX remain separate.
- Runtime, Final, Workbench and Kitchen files are unchanged.
- Rejection consists of discarding only the V3 draft, public shell, set manifest
  and its twelve content-addressed objects.

## Files and verification

- Review tool: `public/keeper-review/activity-cloud-composer-v3/index.html`
- Draft/source: `art/drafts/activity-cloud-composer-2026-10-19-v3/`
- Builder: `scripts/build_activity_cloud_composer_v3.py`
- Verifier: `scripts/verify_activity_cloud_composer_v3.mjs`

Run:

```sh
npm run verify:activity-cloud-composer-v3
```

The verifier rejects any V2 component, Prime body, route, default recipe or
timing change. It also checks every source edge, component owner, transparent
gutter, hash, archive mapping, preload/decode contract and non-promotion
boundary.
