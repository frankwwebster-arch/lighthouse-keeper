import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const contractPath = path.join(root, "data/activity_callout_style_contract.json");
const contract = JSON.parse(await readFile(contractPath, "utf8"));

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const sha256 = async (relativePath) => {
  const bytes = await readFile(path.join(root, relativePath));
  return createHash("sha256").update(bytes).digest("hex");
};

assert(
  contract.schema === "lighthouse-keeper/activity-callout-authoring-standard@1",
  "Unexpected activity-callout authoring schema",
);
assert(contract.status === "binding-authoring-standard", "Standard is not binding");
assert(contract.document === "docs/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md", "Wrong standard document");
await readFile(path.join(root, contract.document), "utf8");

for (const reference of contract.authority.pinnedReferences) {
  const actual = await sha256(reference.path);
  assert(actual === reference.sha256, `${reference.role} hash drift: ${reference.path}`);
}

assert(contract.raster.componentCellPixels.join("x") === "256x256", "Wrong component cell");
assert(contract.raster.visibleAlphaThreshold === 8, "Wrong alpha threshold");
assert(contract.raster.minimumTransparentGutterPixels === 16, "Wrong minimum gutter");
assert(contract.raster.preferredTransparentGutterPixels === 20, "Wrong preferred gutter");
assert(contract.raster.ownersPerComponent === 1, "Components must have exactly one owner");
assert(contract.raster.ambiguousPixels === 0, "Ambiguous pixels must be zero");
assert(contract.raster.unownedVisiblePixels === 0, "Unowned visible pixels must be zero");
assert(contract.raster.outputEdgeAlphaPixels === 0, "Output edge alpha must be zero");

assert(contract.recipe.minimumElements === 4, "Recipes must allow four elements");
assert(contract.recipe.maximumElements === 5, "Recipes must allow five elements");
assert(contract.recipe.heroElementIndex === 0, "The first recipe element must be the hero");
assert(
  contract.recipe.bodyCompatibilityValues.join(",") ===
    "rear-work-with-context,dedicated-pose-required",
  "Body compatibility vocabulary drift",
);
assert(contract.recipe.dedicatedPoseBodyVisible === false, "Dedicated poses must withhold the generic body");

assert(contract.presentation.requiredTreatments.join(",") === "orbit,bustle", "Both treatments are required");
assert(contract.presentation.calloutFrames === 42, "Wrong callout frame count");
assert(contract.presentation.calloutFps === 8, "Wrong callout fps");
assert(contract.presentation.quietTailFrames === 5, "Wrong quiet tail");
assert(contract.presentation.bodyFrames === 24, "Wrong Prime rear-work body frame count");
assert(contract.presentation.bodyFps === 4, "Wrong Prime rear-work body fps");
assert(contract.presentation.foregroundReviewCounterAllowed === false, "Review counter must remain forbidden");
assert(contract.presentation.preloadAndDecodeBeforePlayback === true, "Preload/decode gate must remain required");

assert(contract.notation.seedAlgorithm === "fnv1a32-v1", "Notation seed drift");
assert(contract.notation.sequenceLengthFrames === 6, "Notation phrase length drift");
assert(contract.notation.visibleNotes === 3, "Notation visible-note count drift");
assert(contract.notation.independentlyControllable === true, "Notation must remain switchable");

const catalogue = JSON.parse(
  await readFile(path.join(root, "public/keeper-review/activity-cloud-composer-v6/catalogue.json"), "utf8"),
);
assert(catalogue.schema === "lighthouse-keeper/activity-cloud-composer@1", "Composer schema drift");
assert(catalogue.set === "activity-cloud-composer-v6", "Composer V6 identity drift");
assert(Object.keys(catalogue.components).length === 149, "Composer V6 component count drift");
assert(catalogue.composer.minimumElements === contract.recipe.minimumElements, "Composer minimum mismatch");
assert(catalogue.composer.maximumElements === contract.recipe.maximumElements, "Composer maximum mismatch");
assert(catalogue.composer.frames === contract.presentation.calloutFrames, "Composer frame mismatch");
assert(catalogue.composer.fps === contract.presentation.calloutFps, "Composer fps mismatch");
assert(catalogue.composer.quietTailFrames === contract.presentation.quietTailFrames, "Composer quiet-tail mismatch");
assert(
  catalogue.composer.treatments.join(",") === contract.presentation.requiredTreatments.join(","),
  "Composer treatment mismatch",
);
assert(catalogue.body.frames.length === contract.presentation.bodyFrames, "Body frame count mismatch");
for (const index of contract.presentation.bodyNeutralFrames) {
  assert(
    catalogue.body.frames[index - 1].src === catalogue.reviewReferences.exactRear,
    `Body frame ${index} is not exact rear neutral`,
  );
}
assert(
  catalogue.notationAccents.seedAlgorithm === contract.notation.seedAlgorithm,
  "Composer notation seed mismatch",
);
assert(
  catalogue.notationAccents.sequenceLengthFrames === contract.notation.sequenceLengthFrames,
  "Composer notation phrase mismatch",
);
assert(
  catalogue.notationAccents.visibleNotes === contract.notation.visibleNotes,
  "Composer notation count mismatch",
);

const loo = catalogue.suggestedRecipes["using-loo"];
assert(loo.bodyCompatibility === "dedicated-pose-required", "Loo package body compatibility drift");
assert(loo.elements.length === 5, "Loo package must remain a five-element evidence recipe");
for (const id of ["bathroom-flush-handle", "bathroom-loo-brush", "bathroom-bad-smell"]) {
  assert(loo.elements.includes(id), `Loo package is missing ${id}`);
}

const forbidden = new Set(contract.visual.forbiddenTraits);
for (const trait of [
  "flat-generic-symbol",
  "vignette-aura-haze-or-margin-glow",
  "text-letter-number-logo-brand-or-watermark",
  "context-baked-into-keeper-or-household-asset",
]) {
  assert(forbidden.has(trait), `Missing forbidden visual trait: ${trait}`);
}

for (const phrase of ["exactly one", "genuinely transparent background", "no watermark", "no glow"]) {
  assert(
    contract.generation.singleTokenPromptRequiredPhrases.includes(phrase),
    `Prompt scaffold lost required phrase: ${phrase}`,
  );
}

console.log("Activity-callout authoring standard verified.");
console.log(`Pinned references: ${contract.authority.pinnedReferences.length}`);
console.log(`Composer V6 components: ${Object.keys(catalogue.components).length}`);
console.log(
  `Raster contract: ${contract.raster.componentCellPixels.join("x")} cell, ` +
    `${contract.raster.minimumTransparentGutterPixels}px minimum / ` +
    `${contract.raster.preferredTransparentGutterPixels}px preferred gutter`,
);
