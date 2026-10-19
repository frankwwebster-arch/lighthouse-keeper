# Prime Keeper upper-body override POC V2

V2 changes no animation artwork, route order, root path or timing. It corrects only the V1 reviewer's mirrored-cell placement.

The source anchor is 18.75 lp inside a 48 lp cell. Under CSS horizontal mirroring that point becomes 29.25 lp. V1 continued subtracting 18.75 lp, so playback jumped 10.5 lp at frame 18. V2 subtracts 29.25 lp for every mirrored frame, preserving the declared root position across frame 17 to 18 and throughout the mirrored return.

Frank described V1 as a valuable POC and requested this correction. That feedback is not recorded as formal approval. No production or runtime assets change.
