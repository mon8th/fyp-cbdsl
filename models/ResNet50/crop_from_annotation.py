import json
from pathlib import Path
from PIL import Image

# ── Input: your current data/raw/<class>/ folders (image + json pairs) ──
SOURCE_ROOT = Path("data/raw")

# ── Output: cropped images go here, separate from raw to avoid overwriting ──
OUTPUT_ROOT = Path("data/cropped")

PADDING_RATIO = 0.15 


def crop_with_padding(image: Image.Image, box: list, padding_ratio: float) -> Image.Image:
    x1, y1, x2, y2 = box
    w, h = x2 - x1, y2 - y1

    pad_x = w * padding_ratio
    pad_y = h * padding_ratio

    x1 = max(0, x1 - pad_x)
    y1 = max(0, y1 - pad_y)
    x2 = min(image.width,  x2 + pad_x)
    y2 = min(image.height, y2 + pad_y)

    return image.crop((x1, y1, x2, y2))


def main():
    total_cropped = 0
    total_skipped = 0

    for class_folder in sorted(SOURCE_ROOT.iterdir()):
        if not class_folder.is_dir():
            continue

        class_name = class_folder.name   # "hat", "hello", "phone" — no suffix to strip
        out_dir = OUTPUT_ROOT / class_name
        out_dir.mkdir(parents=True, exist_ok=True)

        for json_path in class_folder.glob("*.json"):
            img_path = json_path.with_suffix(".jpg")
            if not img_path.exists():
                img_path = json_path.with_suffix(".JPG")
            if not img_path.exists():
                print(f"  [skip] no matching image for {json_path.name}")
                total_skipped += 1
                continue

            with open(json_path, "r") as f:
                ann = json.load(f)

            if not ann["shapes"]:
                print(f"  [skip] no bbox in {json_path.name}")
                total_skipped += 1
                continue

            shape = ann["shapes"][0]
            points = shape["points"]              
            x1, y1 = points[0]
            x2, y2 = points[1]
            box = [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]

            image   = Image.open(img_path).convert("RGB")
            cropped = crop_with_padding(image, box, PADDING_RATIO)

            out_path = out_dir / img_path.name
            cropped.save(out_path)
            total_cropped += 1

        print(f"{class_name}: done")

    print(f"\nTotal cropped: {total_cropped}")
    print(f"Total skipped: {total_skipped}")
    print(f"Output saved to: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()