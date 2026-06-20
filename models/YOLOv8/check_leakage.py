# check_leakage_yolo.py
from pathlib import Path

classes = [d.name for d in Path("split_dataset/train").iterdir() if d.is_dir()]
splits = ["train", "val", "test"]

for cls in classes:
    sets = {}
    for split in splits:
        folder = Path(f"split_dataset/{split}/{cls}")
        sets[split] = {f.name for f in folder.glob("*.jpg")} | {f.name for f in folder.glob("*.JPG")}

    overlap_tv = sets["train"] & sets["val"]
    overlap_tt = sets["train"] & sets["test"]
    overlap_vt = sets["val"]   & sets["test"]

    print(f"{cls}: train∩val={len(overlap_tv)}  train∩test={len(overlap_tt)}  val∩test={len(overlap_vt)}")