# Kitchen room layout review V2

Status: review-only native-pixel composition awaiting Frank's requested
amendments to the loose assets.

Review route: `/keeper-review/kitchen-room-layout-v2/`.

V1 is rejected. It used the 84 × 74 compatibility runtime bodies as visual
review art, resized source crops, changed colour with a blend mode and placed
the result on a schematic canvas. It remains frozen only as rejection evidence.

V2 uses the approved 1536 × 1024 master at intrinsic size. The fitted run is a
1:1 browser crop of that master. The movable toaster, kettle, bin, bowl, table
and chair cutouts are deterministic 1:1 crops: only border-connected warm-paper
pixels become transparent, four transparent safety pixels are added outside
the crop, and every retained RGB byte is identical to the source. The build and
exact hashes are recorded in `native-cutouts/extraction-register.json`.

Camera zoom is presentation only. The initial 50% camera shows the complete
room; at 100%, one kitchen-source pixel equals one CSS pixel. The existing 193
× 56 logical-pixel room tier and approved density-8
Prime Keeper standing frame provide the scale proof. One Keeper pace is 10.5
logical pixels / 84 Keeper units and projects to 114 kitchen-source pixels;
each 228-pixel fitted bay is exactly two paces wide. Every counter, worktop and
floor interaction centre lies on that pace lattice.

No approved source, canonical asset or runtime file is changed. Reject V2 by
discarding this directory, `data/kitchen_room_layout_review_v2.json`, its
versioned route/shell and its review-archive set alone.
