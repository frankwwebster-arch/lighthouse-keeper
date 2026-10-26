#!/usr/bin/env node

const fs = require("node:fs");
const path = require("node:path");
const { PNG } = require("pngjs");

const root = path.resolve(__dirname, "..");
const inputs = [
  path.join(root, "public/art/reference/day1.png"),
  path.join(root, "public/art/reference/expanded.png"),
];

function isKeyLike(r, g, b) {
  return r > 210 && b > 210 && g < 90 && Math.abs(r - b) < 45;
}

function isBroadKeyLike(r, g, b) {
  return r > 190 && b > 190 && g < 130 && Math.abs(r - b) < 90;
}

function measure(file) {
  const png = PNG.sync.read(fs.readFileSync(file));
  const { width, height, data } = png;
  const foregroundByRow = new Uint32Array(height);
  const darkByRow = new Uint32Array(height);
  let exactKeyPixels = 0;
  let keyLikePixels = 0;

  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const offset = (y * width + x) * 4;
      const r = data[offset];
      const g = data[offset + 1];
      const b = data[offset + 2];
      if (r === 255 && g === 0 && b === 255) exactKeyPixels += 1;
      if (isKeyLike(r, g, b)) keyLikePixels += 1;
      else foregroundByRow[y] += 1;
      if (r < 45 && g < 45 && b < 45) darkByRow[y] += 1;
    }
  }

  // The waterline is the strongest dark horizontal rule in the lower third.
  const waterStart = Math.floor(height * 0.65);
  const waterEnd = Math.floor(height * 0.92);
  let waterlineY = waterStart;
  for (let y = waterStart + 1; y <= waterEnd; y += 1) {
    if (darkByRow[y] > darkByRow[waterlineY]) waterlineY = y;
  }

  // The rendered ground edge is the first row reaching 79% of the maximum
  // island coverage before the waterline. This resists grass and rock peaks.
  const groundStart = Math.floor(height * 0.45);
  const groundEnd = waterlineY - Math.floor(height * 0.07);
  let maxIslandCoverage = 0;
  for (let y = groundStart; y <= groundEnd; y += 1) {
    maxIslandCoverage = Math.max(maxIslandCoverage, foregroundByRow[y]);
  }
  const groundThreshold = maxIslandCoverage * 0.79;
  let groundLineY = groundStart;
  while (
    groundLineY <= groundEnd &&
    foregroundByRow[groundLineY] < groundThreshold
  ) {
    groundLineY += 1;
  }

  // Measure the tower above the terrain/vegetation zone, where it is the only
  // foreground silhouette. Requiring several non-key pixels rejects isolated
  // antialiasing noise in the chroma field.
  const cleanTowerLimitY = Math.floor(height * 0.45);
  let minX = width;
  let maxX = -1;
  let minY = height;
  for (let x = 0; x < width; x += 1) {
    let foregroundPixels = 0;
    let firstForegroundY = height;
    for (let y = 0; y < cleanTowerLimitY; y += 1) {
      const offset = (y * width + x) * 4;
      if (!isBroadKeyLike(data[offset], data[offset + 1], data[offset + 2])) {
        foregroundPixels += 1;
        firstForegroundY = Math.min(firstForegroundY, y);
      }
    }
    if (foregroundPixels >= 3) {
      minX = Math.min(minX, x);
      maxX = Math.max(maxX, x);
      minY = Math.min(minY, firstForegroundY);
    }
  }
  if (maxX < minX) throw new Error(`Could not measure tower bounds in ${file}`);

  const towerBounds = {
    xMin: minX,
    yMin: minY,
    xMax: maxX,
    yMax: groundLineY,
    width: maxX - minX + 1,
    height: groundLineY - minY + 1,
  };

  return {
    schemaVersion: 1,
    source: path.basename(file),
    canvas: { width, height },
    groundLineY,
    waterlineY,
    towerBounds,
    measurement: {
      coordinateSystem: "origin at top-left; inclusive bounds; integer pixels",
      towerDefinition: "lamp room, gallery, and tower exterior down to the measured ground line",
      exactPureMagentaPixelCount: exactKeyPixels,
      approximateMagentaKeyPixelCount: keyLikePixels,
      totalPixelCount: width * height,
    },
  };
}

for (const input of inputs) {
  const result = measure(input);
  const output = input.replace(/\.png$/i, ".json");
  fs.writeFileSync(output, `${JSON.stringify(result, null, 2)}\n`);
  console.log(`${path.relative(root, input)} -> ${path.relative(root, output)}`);
  console.log(JSON.stringify(result));
}
