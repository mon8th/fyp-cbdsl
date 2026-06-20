import os
import torch


def save_check(model, optimizer, epoch: int, val_acc: float, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save(
        {
            "epoch":      epoch + 1,
            "state_dict": model.state_dict(),
            "optimizer":  optimizer.state_dict(),
            "val_acc":    val_acc,
        },
        path,
    )


def load_check(model, path: str, device):
    ckpt = torch.load(path, map_location=device, weights_only=True)
    model.load_state_dict(ckpt["state_dict"])
    return model, ckpt.get("epoch", 0), ckpt.get("val_acc", 0.0)