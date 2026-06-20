def freeze_backbone(model):
    for param in model.parameters():
        param.requires_grad = False

    for param in model.fc.parameters():
        param.requires_grad = True


def unfreeze_model(model):
    for param in model.parameters():
        param.requires_grad = True