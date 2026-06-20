import torch
import torch.optim as optim

from config import (
    IMAGE_SIZE, TRAIN_DIR, VAL_DIR, TEST_DIR, BATCH_SIZE, NUM_EPOCHS,
    FREEZE_EPOCHS, FINETUNE_LR, WEIGHT_DECAY, BEST_MODEL_PATH,
)
from data.dataset    import create_loaders
from data.transforms import get_train_transforms, get_val_transforms
from utils.freeze      import unfreeze_model
from utils.metrics     import accuracy
from utils.checkpoints import save_check


def train(model, criterion, optimizer, scheduler, device):
    train_loader, val_loader, test_loader, _ = create_loaders(
        TRAIN_DIR,
        VAL_DIR,
        TEST_DIR,
        get_train_transforms(IMAGE_SIZE),
        get_val_transforms(IMAGE_SIZE),  
        get_val_transforms(IMAGE_SIZE),   
        BATCH_SIZE,
    )

    best_val_acc = 0.0

    for epoch in range(NUM_EPOCHS):

        # Phase transition: unfreeze full model with differential LR
        if epoch == FREEZE_EPOCHS:
            unfreeze_model(model)

            early_params = (
                list(model.conv1.parameters()) +
                list(model.bn1.parameters())   +
                list(model.layer1.parameters()) +
                list(model.layer2.parameters()) +
                list(model.layer3.parameters())
            )
            late_params = (
                list(model.layer4.parameters()) +
                list(model.fc.parameters())
            )
            optimizer = optim.AdamW(
                [
                    {"params": early_params, "lr": FINETUNE_LR * 0.1},
                    {"params": late_params,  "lr": FINETUNE_LR},
                ],
                weight_decay=WEIGHT_DECAY,
            )
            scheduler = optim.lr_scheduler.CosineAnnealingLR(
                optimizer,
                T_max=NUM_EPOCHS - FREEZE_EPOCHS,
            )

        # Training
        model.train()
        train_loss, n_train = 0.0, 0

        for images, labels in train_loader:
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            optimizer.zero_grad()
            outputs = model(images)
            loss    = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * images.size(0)
            n_train    += images.size(0)

        train_loss /= n_train

        # Validation
        model.eval()
        val_loss, val_acc, n_val = 0.0, 0.0, 0

        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device, non_blocking=True)
                labels = labels.to(device, non_blocking=True)

                outputs = model(images)
                loss    = criterion(outputs, labels)

                val_loss += loss.item()                    * images.size(0)
                val_acc  += accuracy(outputs, labels)      * images.size(0)
                n_val    += images.size(0)

        val_loss /= n_val
        val_acc  /= n_val

        scheduler.step()

        print(
            f"Epoch [{epoch+1:02d}/{NUM_EPOCHS}]  "
            f"train loss={train_loss:.4f}  |  "
            f"val loss={val_loss:.4f}  val acc={val_acc:.4f}"
        )

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            save_check(model, optimizer, epoch, val_acc, BEST_MODEL_PATH)
            print(f"    [ckpt] saved  val_acc={val_acc:.4f}")