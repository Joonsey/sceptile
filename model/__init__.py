import os

import torch
import torchvision.transforms as transforms

from PIL import Image
from torch.utils.data import Dataset

import torch.nn as nn
import torch.nn.functional as F

class PlantVillageDataset(Dataset):
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
    ])

    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.classes = os.listdir(root_dir)
        self.images = []
        self.labels = []

        for idx, cls in enumerate(self.classes):
            cls_path = os.path.join(root_dir, cls)
            for img_name in os.listdir(cls_path):
                img_path = os.path.join(cls_path, img_name)
                self.images.append(img_path)
                self.labels.append(idx)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        image = Image.open(img_path).convert("RGB")
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label


class SimpleCNN(nn.Module):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def __init__(self, features: int, device: torch.device):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(64 * 32 * 32, 512)
        self.fc2 = nn.Linear(512, features)

        self.device = device
        self.to(device)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 32 * 32)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def save(self, path: str = "out/model.pth"):
        torch.save(self.state_dict(), path)

    @staticmethod
    def load(path: str, features: int, device: torch.device):
        model = SimpleCNN(features, device=device)
        model.load_state_dict(torch.load(path))

        return model

    def predict_image(self, image_path: str, transform) -> float:
        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0)
        image = image.to(self.device)

        self.eval()
        with torch.no_grad():
            output = self(image)
            _, predicted = torch.max(output, 1)

        return predicted.item()
