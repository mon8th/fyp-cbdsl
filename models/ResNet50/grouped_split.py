import re
import random
import shutil
from pathlib import Path
from collections import defaultdict

SOURCE_ROOT = Path("data/cropped")
OUTPUT_ROOT = Path("data/split_grouped")
RATIOS      = (0.7, 0.15, 0.15)   # train, val, test
SEED        = 42


def get_group_id(stem: str) -> str:
    match = re.match(r'^(.*\D)(\d+)$', stem)
    if match:
        return match.group(1)
    return stem


def main():
    random.seed(SEED)

    for class_folder in sorted(SOURCE_ROOT.iterdir()):
        if not class_folder.is_dir():
            continue

        class_name = class_folder.name
        images = sorted(class_folder.glob("*.jpg")) + sorted(class_folder.glob("*.JPG"))

        groups = defaultdict(list)
        for img_path in images:
            gid = get_group_id(img_path.stem)
            groups[gid].append(img_path)

        group_ids = list(groups.keys())
        rng = random.Random(SEED)
        rng.shuffle(group_ids)
        group_ids.sort(key=lambda g: -len(groups[g]))

        total_images = len(images)
        targets = {
            "train": total_images * RATIOS[0],
            "val":   total_images * RATIOS[1],
            "test":  total_images * RATIOS[2],
        }
        counts = {"train": 0, "val": 0, "test": 0}
        bucket = {"train": [], "val": [], "test": []}

        for gid in group_ids:
            files = groups[gid]
            deficits = {s: targets[s] - counts[s] for s in counts}
            best_split = max(deficits, key=deficits.get)
            bucket[best_split].extend(files)
            counts[best_split] += len(files)

        train_files, val_files, test_files = bucket["train"], bucket["val"], bucket["test"]

        for split_name, file_list in [("train", train_files), ("val", val_files), ("test", test_files)]:
            out_dir = OUTPUT_ROOT / split_name / class_name
            out_dir.mkdir(parents=True, exist_ok=True)
            for f in file_list:
                shutil.copy2(f, out_dir / f.name)

        print(
            f"{class_name:10s}  "
            f"train={len(train_files):4d}  "
            f"val={len(val_files):4d}  "
            f"test={len(test_files):4d}  "
            f"groups={len(group_ids)}"
        )

    print(f"\nDone. Output saved to: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()