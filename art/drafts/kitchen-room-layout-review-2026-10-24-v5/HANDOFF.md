# Kitchen room layout V5 redraft handoff

V5 is the active reversible review boundary for loose kitchen objects and the
Prime/furniture scale proof. V4's fitted-unit approval remains authoritative
and byte-identical; V4's loose objects are retained only as rejected evidence.
The live 84 x 74 runtime and gameplay are unchanged.

The loose appliance plate and furniture plate are new target-sized generated
sources. Their production crops are extracted at 1:1 with no downscaling,
resampling or colour transform. Each object retains an authored curved contact
shadow and an eight-pixel transparent safety gutter. Worktop objects register
at local y=84, thirteen source pixels farther forward than V4.

The ON toaster is a connected object with toast seated in its slots. Kettle ON
is byte-identical to OFF because steam is a separate future effect. The broken
bowl is a newly drawn damaged state whose front-left wall is absent rather than
an intact panel with deleted stripes.

The scale proof registers both art families into one world density. Kitchen art
uses 228/21 source pixels per logical pixel. Existing Prime cells use 8 source
pixels per logical pixel, so the 256 x 320 source cell is displayed at
228/168 = 1.357142857 times its source dimensions, or 347.43 x 434.29 kitchen
world pixels. The camera then zooms the composed world uniformly. This does not
downscale or rewrite kitchen art. The locked worktop reads as 850 mm against a
1,750 mm Prime; table height is 750 mm and chair seat height is 460 mm.

Reject V5 by deleting only its page/route, generated source plates, V5 native
outputs and V5 references. Preserve the approved fitted files and their
approval record, every V1-V4 page, Runtime Promotion V1 and the retained 84 x 74
room.

Build with `npm run build:kitchen-room-layout-review-v5` and verify with
`npm run verify:kitchen-room-layout-review-v5`.
