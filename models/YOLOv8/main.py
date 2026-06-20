import torch
import torchvision.transforms as transforms
from ultralytics import YOLO
from ultralytics.data.dataset import ClassificationDataset
from ultralytics.models.yolo.classify import (
    ClassificationTrainer,
    ClassificationValidator,
)

# ── REMOVED ──────────────────────────────────────────────────
# from splitfolders import ratio
# ratio("dataset", output="split_dataset", seed=42, ratio=(0.7,0.15,0.15))
# ^ random per-file split — same leakage risk as ResNet50 had
# ─────────────────────────────────────────────────────────────
# Run grouped_split.py separately first (same script used for ResNet50),
# pointing SOURCE_ROOT at your cropped YOLO data and OUTPUT_ROOT at
# wherever you want split_dataset to live. Then YOLO just reads the
# already-correctly-split folder below.

model = YOLO("yolov8m-cls.pt")

class AugmentedData(ClassificationDataset):
    def __init__(self, root, args, augment=False, prefix=""):
        super().__init__(root, args, augment, prefix)

        train_data = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=(-25, 25)),
            transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2, hue=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        val_data = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.torch_transforms = train_data if augment else val_data


class Trainer(ClassificationTrainer):
    def build_dataset(self, img_path, mode="train"):
        return AugmentedData(root=img_path, args=self.args, augment=(mode == "train"), prefix=mode)


class Validation(ClassificationValidator):
    def build_dataset(self, img_path):
        return AugmentedData(root=img_path, args=self.args, augment=False, prefix=self.args.split)


model.train(data="split_dataset", trainer=Trainer, epochs=50, batch=32)
model.val(data="split_dataset", validator=Validation, batch=32)