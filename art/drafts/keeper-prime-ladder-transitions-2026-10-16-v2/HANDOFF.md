# Keeper Prime ladder transitions V2

V2 changes no Keeper, ladder-contact, walk, bridge or turn pixels. It adds a narrow central-rung occlusion layer between the ladder and Keeper only while their bodies overlap, so rungs cannot flash through changing transparent gaps while the rails remain visible. Turns change from 62.5 ms to 50 ms per frame; contact, passing, mount and dismount frames change to 150 ms. Hand/foot-to-rung geometry remains V1 exactly. Nothing is promoted.

Review: `/keeper-review/keeper-prime-ladder-transitions-v2/`.
