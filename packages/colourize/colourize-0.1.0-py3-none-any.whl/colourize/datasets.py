from pathlib import Path
from glob import glob

import torch
from torch.utils.data import Dataset


class ColourizedDataset(Dataset):
    """A PyTorch Dataset for preprocessed datasets.

    Colourized dataset, serialized to (image, target) paris.
    """
    def __init__(self, root, transforms=None, train=True):
        if train:
            self.root = Path(root).expanduser() / 'train'
        else:
            self.root = Path(root).expanduser() / 'val'

        if not self.root.exists():
            raise(ValueError("Path {} does not exist".format(self.root)))

        regex = str(self.root) + '/*'
        self.transforms = transforms
        self.data = glob(regex)

    def __getitem__(self, idx):
        image, target = torch.load(self.data[idx])
        image.squeeze_(0)
        if self.transforms:
            image = self.transforms(image)
        return image, target.item()

    def __len__(self):
        return len(self.data)
