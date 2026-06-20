from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader


def create_loaders(train_dir, val_dir, test_dir, train_transform, val_transform, test_transform, batch_size, num_workers=4):
    train_dataset = ImageFolder(train_dir, transform=train_transform)
    val_dataset   = ImageFolder(val_dir,   transform=val_transform)
    test_dataset  = ImageFolder(test_dir,  transform=test_transform)

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=False,
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
        drop_last=False,
    )

    return train_loader, val_loader, test_loader, train_dataset.classes