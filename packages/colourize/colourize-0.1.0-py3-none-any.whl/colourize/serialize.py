from functools import partial

import torch
from tqdm import tqdm

from colourize import _select


def outer_loop(dataset_name, dataset_root, colourspaces, outdir, force):
    """
    """
    for colourspace in colourspaces:
        colourdir = outdir / (dataset_name + '-' + colourspace.std_name)
        if colourdir.exists():
            print("Colourspace {} already serialized".format(colourspace))
            continue
        colourdir.mkdir(parents=True, exist_ok=True)

        print("Serializing {} colourspace".format(colourspace))
        transforms = _select.transforms(colourspace.colour)
        train_loader, val_loader = _select.dataset(dataset_name,
                                                   dataset_root,
                                                   transforms)
        inner_loop(train_loader, colourdir / 'train')
        inner_loop(val_loader, colourdir / 'val')


def inner_loop(loader, path):
    serialize_ = partial(serialize, path)
    for idx, data in enumerate(tqdm(loader)):
        serialize_(idx, data)


def serialize(path, idx, data):
    path = path / '{0:010d}.pth'.format(idx)
    torch.save(data, path)
