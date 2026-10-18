# Prime Keeper sweep broom V7 prompt log

Mode: built-in image editing (`image_gen`). Two exploratory contact-sheet edits were generated from exact Walk V6 / Turn V9 plus the broom authority. Their generated broom pixels were rejected because the broom changed shape and tone. Apple Vision foreground extraction isolated the eight selected grip studies. Each study is registered to its corresponding Walk V6 frame and contributes pixels only inside the declared arm/hand corridor; all other visible Keeper pixels come from the exact approved Walk V6 authority. The generated broom is discarded. Turn V9 remains the exact base outside its carrying-arm corridor.

## Selected walk-edit prompt

Use case: precise-object-edit. Asset type: an eight-frame transparent animation contact sheet. In each of the eight supplied approved Walk V6 cells, replace only the two arms and hands with the same natural bent-forward two-hand grip shown in the supplied Sweep 3 reference. Preserve the exact approved Keeper body, face, beard, cap, jumper, trousers, boots, silhouette, scale, floor contact, left-foot/right-foot gait phase, frame order and spacing. Do not add a broom to the selected output. Do not change the legs or feet. Keep one isolated character in each cell on a clean transparent background with generous gutters.

## Runtime assembly rule

Both travel directions play F1→F8 at 125 ms per frame. Direction changes by mirroring and root motion only; the frame sequence is never time-reversed. The provisional broom is a separately owned layer rendered behind the hands.
