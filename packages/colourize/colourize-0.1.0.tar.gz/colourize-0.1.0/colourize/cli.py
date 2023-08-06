"""CLI interface for colorize.

Parses CLI argments and ensures they are valid.
"""
import argparse
from pathlib import Path


def parse_args(args):
    """Parse CLI arguments.
    """
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('dataset_name',
                        help='Dataset name')
    parent_parser.add_argument('root',
                        help='Dataset root location')
    parent_parser.add_argument('-f',
                        '--force',
                        action='store_true',
                        help='Overwrite norms/dataset if exists')
    colours = parent_parser.add_mutually_exclusive_group(required=True)
    colours.add_argument('--all',
                         dest='all_colours',
                         action='store_true',
                         help='Preprocess all colourspaces')
    colours.add_argument('--colours',
                         type=str,
                         nargs='+',
                         help='Colourspaces to process')

    description = "Colourize\n\n" \
                  "A tool for preprocessing image datasets."
    parser = argparse.ArgumentParser(description=description,
                                            add_help=False)


    subparsers = parser.add_subparsers(title='Subcommands',
                                       dest='action',
                                       required=True)


    parser_colourize_help = "Serialize and calculate normalization values " \
                            "for a dataset to disk as a PyTorch tensors and " \
                            "YAML for the specified colourspace."
    parser_colourize = subparsers.add_parser('colourize',
                                             parents=[parent_parser],
                                             help=parser_colourize_help)
    parser_colourize.add_argument('-o',
                                  '--outdir',
                                  default=Path.cwd() / 'colourized_data',
                                  type=Path,
                                  help='Path to directory where output should '
                                       'be written')

    parser_serialize_help = "Serialize a dataset to disk as a PyTorch " \
                            "tensor in the specified colourspace."
    parser_serialize = subparsers.add_parser('serialize',
                                             parents=[parent_parser],
                                             help=parser_serialize_help)
    parser_serialize.add_argument('-o',
                                  '--outdir',
                                  default=Path.cwd() / 'colourized_data',
                                  type=Path,
                                  help='Path to directory where output should '
                                       'be written')

    parser_normalize_help = "Calculate the normalization values for the " \
                            "given dataset and colourspace."
    parser_normalize = subparsers.add_parser('normalize',
                                             parents=[parent_parser],
                                             help=parser_normalize_help)
    parser_normalize.add_argument('-o',
                                  '--outfile',
                                  default=Path.cwd() / 'norms.yml',
                                  type=Path,
                                  help='Path to write normalization values.')
    parser_normalize.add_argument('--shuffle',
                                  action='store_true',
                                  help='Shuffle dataset')
    parser_normalize.add_argument('--seed',
                                  type=int,
                                  help='Random seed')
    parser_normalize.add_argument('--max',
                                  type=int,
                                  help='Max number of images to process')

    args = parser.parse_args(args)
    return args
