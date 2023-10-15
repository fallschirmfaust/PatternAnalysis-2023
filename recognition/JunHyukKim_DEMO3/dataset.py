import os
from PIL import Image
from torch.utils.data import Dataset
import numpy as np
import torch
import torch.utils.data

from glob import glob
from torchvision.transforms import Resize
import torchvision.transforms as transforms



TRAINDATA = "ISIC\ISIC-2017_Training_Data\ISIC-2017_Training_Data"
TESTDATA = "ISIC\ISIC-2017_Test_v2_Data\ISIC-2017_Test_v2_Data"
VALIDDATA = "ISIC\ISIC-2017_Validation_Data\ISIC-2017_Validation_Data"
TRAINTRUTH = "ISIC\ISIC-2017_Training_Part1_GroundTruth\ISIC-2017_Training_Part1_GroundTruth"
TESTTRUTH = "ISIC\ISIC-2017_Test_v2_Part1_GroundTruth\ISIC-2017_Test_v2_Part1_GroundTruth"
VALIDTRUTH = "ISIC\ISIC-2017_Validation_Part1_GroundTruth\ISIC-2017_Validation_Part1_GroundTruth"

NUM_EPOCHS = 5
BATCH_SIZE = 4
WORKERS = 4

class CustomDataset(Dataset):
    def __init__(self, image_dir, mask_dir, transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        
        self.image_files = sorted(glob(os.path.join(self.image_dir, "*.jpg")))
        self.mask_files = sorted(glob(os.path.join(self.mask_dir, "*.png")))
        self.resize = Resize((224, 224))

    def __len__(self):
        return len(self.mask_files)

    def __getitem__(self, index):
        img_path = self.image_files[index]
        mask_path = self.mask_files[index]

        image = self.resize(Image.open(img_path))
        mask = self.resize(Image.open(mask_path))
        image = image.convert("RGB")
        mask = mask.convert("L")

        if self.transform is not None:
            image = self.transform(image)
            mask = self.transform(mask)
        sample = {'image': image, 'mask': mask}
        return sample


train_dataset = CustomDataset(image_dir = TRAINDATA,
                                mask_dir=TRAINTRUTH,
                                transform=transforms.Compose([
                                transforms.RandomRotation(30),
                                transforms.RandomResizedCrop(224),
                                transforms.RandomHorizontalFlip(),
                                transforms.ToTensor()]))

train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE,
                                         shuffle=True)

valid_dataset = CustomDataset(image_dir = VALIDDATA,
                                mask_dir=VALIDTRUTH,
                                transform=transforms.Compose([
                                transforms.RandomRotation(30),
                                transforms.RandomResizedCrop(224),
                                transforms.RandomHorizontalFlip(),
                                transforms.ToTensor()]))

valid_dataloader = torch.utils.data.DataLoader(valid_dataset, batch_size=BATCH_SIZE,
                                         shuffle=True)

test_dataset = CustomDataset(image_dir = TESTDATA,
                                mask_dir=TESTTRUTH,
                                transform=transforms.Compose([
                                transforms.RandomRotation(30),
                                transforms.RandomResizedCrop(224),
                                transforms.RandomHorizontalFlip(),
                                transforms.ToTensor()]))

test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=BATCH_SIZE,
                                         shuffle=True)


#print(train_dataset.__getitem__(1)[0].shape)
#print(train_dataset.__getitem__(1)[1].shape)
print(enumerate(train_dataloader))
print(len(train_dataloader))
print(len(test_dataloader))
print(len(train_dataset))
print(len(test_dataset))
#print(train_dataset.__getitem__(1))