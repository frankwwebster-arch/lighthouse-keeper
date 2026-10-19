# Prime Keeper upper-body override POC V3

V3 changes no Keeper pixel, gait order, turn order, root-motion speed or duration. It makes two review-presentation corrections requested by Frank:

1. Playback frame 18 receives a one-logical-pixel left registration. V2 fixed the mathematical cell mirror, but the generated proxy's visible silhouette still moved 1.333 lp right at the rear crossing. The V3 correction reduces the adjacent full-silhouette centroid changes to +0.333 and -0.408 lp.
2. Playback is one-shot. Walk-right stops after the standard 21-lp cycle at its translated endpoint; replay restarts from frame 1. It no longer wraps immediately to the start and therefore no longer reads as walking on the spot.

This remains a non-production POC. Frank has not formally approved it.
