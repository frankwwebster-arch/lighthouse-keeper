# Keeper Prime Walk V4 — rear-arm cadence redraft

Status: review draft awaiting Frank's visual approval. Nothing in this directory is Final or production.

## Purpose

Walk V3 kept the rear/screen-left arm too static: F2/F3 were nearly identical and F5/F6/F7 held almost the same silhouette. V4 gives that arm an explicit cycle while retaining the existing eight body/leg poses:

1. rearward maximum;
2. rearward-to-passing halfway;
3. vertical passing;
4. unchanged V3 up pose;
5. cuff and hand begin reappearing;
6. vertical passing on return;
7. clear rearward swing;
8. rearward approach to the loop seam.

## Reversibility and scope

- Walk V1–V3 are immutable and unchanged.
- F1, F4 and F8 are byte-identical to Walk V3.
- F2, F3 and F5–F7 use separate built-in image-generation edits, registered to the shared height/floor and composited only within declared rear-arm polygons.
- Two attempted F4 occlusion redraws are rejected provenance: one left a circular shoulder loop and the other introduced a full-body model shift.
- The verifier rejects any changed pixel outside the five declared rear-arm regions.
- Production sprites, runtime manifests and the workbench Final lane remain unchanged.
- Rejection requires deleting only this V4 draft directory and its matching public review directory.

## Review gate

Review the in-place loop, translated walk, individual stepping and synchronized V3/V4 comparison at exact game size. Approval applies only to this walk candidate; it does not approve walk-to-stop or production promotion.
