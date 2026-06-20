import torch
import torch.nn as nn
import torch.optim as optim

from config import (
    NUM_CLASSES, FREEZE_LR, FREEZE_EPOCHS,
    WEIGHT_DECAY, LABEL_SMOOTHING,
    TRAIN_DIR, VAL_DIR, TEST_DIR, IMAGE_SIZE, BATCH_SIZE,
    BEST_MODEL_PATH,
)
from model.resnet50     import build_resnet50
from utils.freeze       import freeze_backbone
from utils.checkpoints  import load_check
from utils.metrics      import full_evaluation
from data.dataset       import create_loaders
from data.transforms    import get_val_transforms
from train              import train


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")


    model = build_resnet50(NUM_CLASSES).to(device)
    freeze_backbone(model)   

    criterion = nn.CrossEntropyLoss(label_smoothing=LABEL_SMOOTHING)
    optimizer = optim.AdamW(
        model.fc.parameters(),
        lr=FREEZE_LR,
        weight_decay=WEIGHT_DECAY,
    )
    scheduler = optim.lr_scheduler.CosineAnnealingLR(
        optimizer,
        T_max=FREEZE_EPOCHS,
    )

    train(model, criterion, optimizer, scheduler, device)

    _, _, test_loader, class_names = create_loaders(
        TRAIN_DIR,
        VAL_DIR,
        TEST_DIR,
        get_val_transforms(IMAGE_SIZE),   
        get_val_transforms(IMAGE_SIZE),   
        get_val_transforms(IMAGE_SIZE),   
        BATCH_SIZE,
    )

    model, epoch, val_acc = load_check(model, BEST_MODEL_PATH, device)
    print(f"\nLoaded best checkpoint from epoch {epoch}  (val_acc={val_acc:.4f})")

    print("\n── Final Test Evaluation ──")
    full_evaluation(model, test_loader, class_names, device)


if __name__ == "__main__":
    main()