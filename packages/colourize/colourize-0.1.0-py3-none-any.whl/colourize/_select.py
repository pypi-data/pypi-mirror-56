from torch.utils.data import DataLoader
from torchvision.datasets import CIFAR10
from torchvision.transforms import ToTensor, Compose

from colourize.transforms import ConvertColorspace, ToArray


def transforms(colorspace):
    """Return transfroms for preprocessing a colorspace.
    """
    transforms = []
    if colorspace == 'sRGB':
        transforms.append(ToTensor()) # FIXME: This only scales because of
                                      # ToTensor, which is now done in
                                      # colorspace conversion.
    else:
        transforms.append(ToArray())
        transforms.append(ConvertColorspace(colorspace))
        transforms.append(ToTensor())
    return Compose(transforms)


def dataset(name, root, transforms):
    """Return dataloader for dataset.
    """
    if name.lower() == 'cifar10':
        train_dataset = CIFAR10(root, transform=transforms, train=True)
        val_dataset = CIFAR10(root, transform=transforms, train=False)
    else:
        raise ValueError("Dataset {} not found")

    train_loader = DataLoader(
        train_dataset,
        batch_size=1,
        num_workers=10,
        shuffle=False,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=1,
        num_workers=10,
        shuffle=False,
    )

    return train_loader, val_loader
