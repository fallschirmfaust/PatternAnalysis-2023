import torch
import torchvision
from dataset import CustomDataset
from torch.utils.data import DataLoader

def get_loaders(train_dir,
                train_maskdir,
                val_dir,
                val_maskdir,
                batch_size,
                train_transform,
                val_transform,
                num_workers=4,
                pin_memory=True,):
    """
    Initializes and returns data loaders for training and validation datasets.

    :param train_dir: Directory containing training images.
    :param train_maskdir: Directory containing corresponding training masks (ground truth).
    :param val_dir: Directory containing validation images.
    :param val_maskdir: Directory containing corresponding validation masks (ground truth).
    :param batch_size: Number of samples per batch.
    :param train_transform: Transformations to be applied on training images.
    :param val_transform: Transformations to be applied on validation images.
    :param num_workers: Number of subprocesses to use for data loading. Default is 4.
    :param pin_memory: Whether to copy tensors into CUDA pinned memory. Set it to True if using GPU. Default is True.
    
    :return: Tuple containing training and validation data loaders.
    """
    train_ds = CustomDataset(image_dir=train_dir,
                            mask_dir=train_maskdir,
                            transform=train_transform,)

    train_loader = DataLoader(train_ds,
                            batch_size=batch_size,
                            num_workers=num_workers,
                            pin_memory=pin_memory,
                            shuffle=True,)

    val_ds = CustomDataset(image_dir=val_dir,
                            mask_dir=val_maskdir,
                            transform=val_transform,)

    val_loader = DataLoader(val_ds,
                            batch_size=batch_size,
                            num_workers=num_workers,
                            pin_memory=pin_memory,
                            shuffle=False,)
    
    return train_loader, val_loader

def check_accuracy(loader, model, device="cuda"):
    """
    Computes and prints the accuracy and Dice score of the given model on the provided data loader.

    :param loader: The data loader containing the dataset to test.
    :param model: The model to test.
    :param device: Device to which the model and data should be moved before testing. Default is "cuda" for GPU.

    :return: None, but prints the accuracy and Dice score of the model on the dataset.
    """
    num_correct = 0
    num_pixels = 0
    dice_score = 0
    model.eval()

    with torch.no_grad():
        for x, y in loader:
            x = x.to(device)
            y = y.to(device).unsqueeze(1)
            preds = model(x)
            preds = (preds > 0.5).float()
            num_correct += (preds == y).sum()
            num_pixels += torch.numel(preds)
            dice_score += (2 * (preds * y).sum()) / (
                (preds + y).sum() + 1e-8
            )

    print(f"Got {num_correct}/{num_pixels} with acc {num_correct/num_pixels*100:.2f}")
    print(f"Dice score: {dice_score/len(loader)}")
    model.train()

def save_predictions_as_imgs(loader, model, folder="saved_images/", device="cuda"):    
    """
    Saves the predictions of the model as image files.

    :param loader: DataLoader for the dataset for which predictions are to be saved.
    :param model: Model used for making predictions.
    :param folder: Directory in which the saved images will be stored. Default is "saved_images/".
    :param device: Device on which the model and data are. Default is "cuda".
    """
    model.eval()
    for idx, (x, y) in enumerate(loader):
        x = x.to(device=device)
        with torch.no_grad():
            preds = model(x)
            preds = (preds > 0.5).float()
        torchvision.utils.save_image(
            preds, f"{folder}/pred_{idx}.png"
        )
        torchvision.utils.save_image(y.unsqueeze(1), f"{folder}{idx}.png")

    model.train()