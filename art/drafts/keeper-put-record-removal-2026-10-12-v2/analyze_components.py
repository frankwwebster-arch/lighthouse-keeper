#!/usr/bin/env python3
"""Report alpha-connected source components for mask-removal verification."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "art/drafts/keeper-review-amendments-2026-10-11-v1/generated/outfit-walks/keeper_put_record-v1-neutral.png"
GENERATED = Path(__file__).resolve().parent / "mask-removal-generated.png"


def components(image: Image.Image) -> list[list[tuple[int, int]]]:
    alpha = image.getchannel("A")
    pixels = alpha.load()
    seen: set[tuple[int, int]] = set()
    result = []
    for y in range(image.height):
        for x in range(image.width):
            if pixels[x, y] < 32 or (x, y) in seen:
                continue
            stack = [(x, y)]
            seen.add((x, y))
            component = []
            while stack:
                px, py = stack.pop()
                component.append((px, py))
                for point in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                    nx, ny = point
                    if 0 <= nx < image.width and 0 <= ny < image.height and point not in seen and pixels[nx, ny] >= 32:
                        seen.add(point)
                        stack.append(point)
            result.append(component)
    return result


def main() -> None:
    source = Image.open(SOURCE).convert("RGBA")
    generated = Image.open(GENERATED).convert("RGBA")
    for index in range(8):
        left = round(source.width * index / 8)
        right = round(source.width * (index + 1) / 8)
        cell = source.crop((left, 0, right, source.height))
        summary = []
        for component in components(cell):
            xs = [point[0] for point in component]
            ys = [point[1] for point in component]
            summary.append((len(component), (min(xs), min(ys), max(xs) + 1, max(ys) + 1)))
        print(index + 1, sorted(summary, reverse=True)[:8])
        red = []
        for y in range(cell.height):
            for x in range(cell.width):
                r, g, b, a = cell.getpixel((x, y))
                if a >= 32 and r >= 120 and r > g * 2.2 and r > b * 1.8 and g < 70:
                    red.append((x, y))
        if red:
            print("  red", len(red), (min(x for x, y in red), min(y for x, y in red), max(x for x, y in red) + 1, max(y for x, y in red) + 1))
        generated_cell = generated.crop((left, 0, right, generated.height))
        removed = Image.new("RGBA", cell.size, (0, 0, 0, 0))
        removed_pixels = removed.load()
        for y in range(cell.height):
            for x in range(cell.width):
                if cell.getpixel((x, y))[3] >= 32 and generated_cell.getpixel((x, y))[3] < 32:
                    removed_pixels[x, y] = (255, 255, 255, 255)
        removed_summary = []
        for component in components(removed):
            xs = [point[0] for point in component]
            ys = [point[1] for point in component]
            removed_summary.append((len(component), (min(xs), min(ys), max(xs) + 1, max(ys) + 1)))
        print("  opaque-to-transparent", sorted(removed_summary, reverse=True)[:8])


if __name__ == "__main__":
    main()
