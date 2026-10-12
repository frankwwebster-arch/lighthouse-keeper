# Keeper party-hat rear-hand correction — 12 October 2026 v2

This reversible draft addresses Frank's annotated review of
`keeper_party_hat_put_on_back`: frame 2 placed the hands and hat on the wrong
side of the rear-facing body.

Only frame 2 may change. Frames 1 and 3–8 must remain byte-identical to the
11 October amendment draft. Canonical raw and runtime assets remain unchanged
until explicit promotion.

## Provenance

- Canonical raw strip SHA-256: `ca3877f5de83830f0e3609b7857f117093908396e5d2ed6ac640357c0823a935`
- Preserved 11 October draft SHA-256: `319b7ea9e97fed22dd0c4cf35b501602b0ea4d054e21593818b3f40ca26d7adf`
- Isolated rejected frame-2 source SHA-256: `7b36812a37ba79cd3fd5eb3f79906c1e3650d10587d2112b0601e366e643072d`
- Built-in image-edit result SHA-256: `757d8432b7eeec91c4513e95bb80b3839da9252a16a850029c659dad63fcdb93`
- New normalized draft SHA-256: `f782da08d76f30182c748dd38fddfa9e95b676f4ab772cf10d42303ce9dae31f`

The image edit requested a single full-body rear pose in the existing painted
sprite style: connected arms rising outward on the visible rear plane, both
hands holding the red-and-cream party hat at the nape, with the head, hair,
uniform, legs, scale and transparent background preserved. It explicitly
excluded front-facing anatomy, floating or duplicated hands, a captain's cap,
a visible face or smile, cropping, shadows, text and extra frames.

`build.py` normalizes that isolated result into frame 2, preserves frames 1 and
3–8 byte-for-byte, produces contact/GIF evidence, records all hashes and rejects
shared-edge alpha. Rollback is removal of this directory and its one registry
entry.
