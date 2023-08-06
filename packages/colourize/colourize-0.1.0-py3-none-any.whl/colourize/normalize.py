"""
"""
import yaml
import torch
from tqdm import tqdm

from colourize import _select


def outer_loop(dataset_name, dataset_root, colourspaces, outfile, force):
    """
    """
    norms = {}
    if outfile and outfile.exists():
        print("Outfile exists, loading...")
        with open(outfile, 'r') as infile:
            norms = yaml.load(infile)

    for colourspace in colourspaces:
        if colourspace.std_name in norms.keys() and not force:
            print("Normas for Colourspace {} already calculated".format(colourspace))
            continue

        print("Calculating norms for {} colourspace".format(colourspace))
        transforms = _select.transforms(colourspace.colour)
        train_loader, _ = _select.dataset(dataset_name, dataset_root, transforms)
        mean, std = inner_loop(train_loader, colourspace.channels)
        mean, std = mean.tolist(), std.tolist()
        norms[colourspace.std_name] = {'mean': mean, 'std': std}

        print("{}:".format(colourspace))
        print("\tMean: {}\n\tStandard Deviation: {}".format(mean, std))

    if outfile:
        with open(outfile, 'w') as outfile:
            yaml.dump(norms, outfile, default_flow_style=False)


def inner_loop(loader, channels):
    """Inner loop over each colourspace.
    """
    cnt = 0
    fst_moment = torch.zeros(channels)
    snd_moment = torch.zeros(channels)

    for data, _ in tqdm(loader):
        cnt, fst_moment, snd_moment = norm(data, cnt, fst_moment, snd_moment)

    return fst_moment, torch.sqrt(snd_moment - fst_moment ** 2)


def norm(data, cnt, fst_moment, snd_moment):
    """Compute the mean and sd in an online fashion

        Var[x] = E[X^2] - E^2[X]
    """
    b, c, h, w = data.shape
    nb_pixels = b * h * w
    sum_ = torch.sum(data, dim=[0, 2, 3])
    sum_of_square = torch.sum(data ** 2, dim=[0, 2, 3])
    fst_moment = (cnt * fst_moment + sum_) / (cnt + nb_pixels)
    snd_moment = (cnt * snd_moment + sum_of_square) / (cnt + nb_pixels)
    cnt += nb_pixels
    return cnt, fst_moment, snd_moment
