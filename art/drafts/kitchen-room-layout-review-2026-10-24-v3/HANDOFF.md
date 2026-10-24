# Kitchen room layout V3 correction handoff

V3 is a disposable, review-only correction boundary. It does not alter the
approved Kitchen V4 master, the 84 × 74 compatibility runtime, gameplay, V1 or
V2. Delete this directory, `data/kitchen_room_layout_review_v3.json`, the V3
public shell/route and its archive manifest to reject it cleanly.

The extraction register pins every source and output hash. All composites use
native pixels only: there is no resize, resampling or colour transform. The
toaster and kettle state bodies reuse OFF bytes exactly. Table and chair use
native-pixel straight-run extension to meet the approved seated geometry rather
than scaling an existing drawing.

Verify with `npm run verify:kitchen-room-layout-review-v3`.
