import torch
from sklearn.metrics import classification_report, confusion_matrix


def accuracy(outputs, labels):
    _, preds = torch.max(outputs, 1)
    correct  = torch.sum(preds == labels).item()
    total    = labels.size(0)
    return correct / total


@torch.no_grad()
def full_evaluation(model, loader, class_names, device):
    """
    Runs the model on a full loader (typically test_loader) and prints:
      - per-class precision, recall, F1, support
      - returns the confusion matrix as a numpy array

    Call this ONCE after training is complete — never during training.
    """
    model.eval()
    all_preds, all_labels = [], []

    for images, labels in loader:
        images  = images.to(device)
        outputs = model(images)
        preds   = torch.argmax(outputs, dim=1).cpu().numpy()

        all_preds.extend(preds)
        all_labels.extend(labels.numpy())

    print(classification_report(all_labels, all_preds, target_names=class_names))
    return confusion_matrix(all_labels, all_preds)