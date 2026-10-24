#!/usr/bin/env node
process.env.KITCHEN_REVIEW_VERSION = 'v6'
process.env.KITCHEN_LOOSE_SOURCE = 'art/drafts/kitchen-room-layout-review-2026-10-24-v6/sources/generated-loose-family-shadowless-source-plate.png'
process.env.KITCHEN_LOOSE_HASH = 'd3c7f612a0e63e160b7973dfec7dc3d57ff6f6f7e7257fa86a0e67ccd1f8ef0e'
process.env.KITCHEN_FURNITURE_SOURCE = 'art/drafts/kitchen-room-layout-review-2026-10-24-v6/sources/generated-furniture-shadowless-source-plate.png'
process.env.KITCHEN_FURNITURE_HASH = '39746a721da1021f620352f96d0ac1de640d48176db45cff1867e62e9db473fd'
await import('./build_kitchen_room_layout_review_v5.mjs')
