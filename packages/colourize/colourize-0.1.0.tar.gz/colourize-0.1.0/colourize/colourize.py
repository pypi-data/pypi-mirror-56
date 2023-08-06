#!/bin/python3
import sys
from functools import partial

import yaml
import torch
from tqdm import tqdm

from colourize.cli import parse_args
from colourize.colourspace import Colourspace, COLOURSPACES
from colourize import normalize
from colourize import serialize
from colourize import _select


def main():
    args = parse_args(sys.argv[1:])

    if args.all_colours:
        colourspaces = COLOURSPACES
    else:
        colourspaces = [Colourspace(colour) for colour in args.colours]

    if args.action == 'normalize':
        normalize.outer_loop(args.dataset_name,
                             args.root,
                             colourspaces,
                             args.outfile,
                             args.force)
    if args.action == 'serialize':
        serialize.outer_loop(args.dataset_name,
                             args.root,
                             colourspaces,
                             args.outdir,
                             args.force)
    if args.action == 'colourize':
        colourize(args.dataset_name,
                  args.root,
                  colourspaces,
                  args.outdir,
                  args.force)


def colourize(dataset_name, dataset_root, colourspaces, outdir, force):
    norms = {}
    outpath = outdir / (dataset_name + '.yml')
    if outdir and outpath.exists():
        print("Outfile exists, loading...")
        with open(outpath, 'r') as infile:
            norms = yaml.load(infile)

    for colourspace in colourspaces:
        colourdir = outdir / (dataset_name + '-' + colourspace.std_name)

        # FIXME(S): we prevent both not just one
        if colourdir.exists():
            print("Colourspace {} already serialized".format(colourspace))
            continue
        if colourspace.std_name in norms.keys() and not force:
            print("Normas for Colourspace {} already calculated".format(colourspace))
            continue

        traindir = colourdir / 'train'
        valdir = colourdir / 'val'
        traindir.mkdir(parents=True, exist_ok=True)
        valdir.mkdir(parents=True, exist_ok=True)
        print("Colourizing {} colourspace".format(colourspace))
        transforms = _select.transforms(colourspace.colour)
        loaders = _select.dataset(dataset_name, dataset_root, transforms)
        mean, std = process_colourspace(loaders,
                                        colourdir,
                                        colourspace.channels)
        mean, std = mean.tolist(), std.tolist()
        norms[colourspace.std_name] = {'mean': mean, 'std': std}

        print("{}:".format(colourspace))
        print("\tMean: {}\n\tStandard Deviation: {}".format(mean, std))
        if outpath:
            with open(outpath, 'w') as outfile:
                yaml.dump(norms, outfile, default_flow_style=False)

    if outpath:
        with open(outpath, 'w') as outfile:
            yaml.dump(norms, outfile, default_flow_style=False)


def process_colourspace(loaders, path, channels):
    """
    """
    cnt = 0
    fst_moment = torch.zeros(channels)
    snd_moment = torch.zeros(channels)

    train_loader, val_loader = loaders
    serialize_train = partial(serialize.serialize, path / 'train')
    serialize_val = partial(serialize.serialize, path / 'val')
    print("Training set:")
    for idx, data in enumerate(tqdm(train_loader)):
        image, _ = data
        serialize_train(idx, data)
        cnt, fst_moment, snd_moment = normalize.norm(image,
                                                     cnt,
                                                     fst_moment,
                                                     snd_moment)
    print("Validation set:")
    for idx, data in enumerate(tqdm(val_loader)):
        serialize_val(idx, data)

    return fst_moment, torch.sqrt(snd_moment - fst_moment ** 2)


if __name__ == '__main__':
    main()
