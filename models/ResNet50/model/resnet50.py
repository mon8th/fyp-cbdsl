import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights


def build_resnet50(num_classes: int) -> nn.Module:
    model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)

    in_features = model.fc.in_features  # 2048
    model.fc = nn.Sequential(
        nn.Dropout(p=0.5),
        nn.Linear(in_features, num_classes),
    )

    return model