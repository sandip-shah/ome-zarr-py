#!/usr/bin/env python

import argparse
import logging

from ome_zarr import info as zarr_info
from ome_zarr import download as zarr_download


def info(args):
    zarr_info(args.path)


def download(args):
    zarr_download(args.path, args.output, args.name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0)
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # foo
    parser_info = subparsers.add_parser('info')
    parser_info.add_argument('path')
    parser_info.set_defaults(func=info)

    # download
    parser_download = subparsers.add_parser('download')
    parser_download.add_argument('path')
    parser_download.add_argument('--output', default='')
    parser_download.add_argument('--name', default='')
    parser_download.set_defaults(func=download)

    args = parser.parse_args()
    loglevel = logging.WARNING - (10 * args.verbose)
    logging.basicConfig(level=loglevel)
    # DEBUG logging for s3fs so we can track remote calls
    logging.getLogger('s3fs').setLevel(logging.DEBUG)

    args.func(args)
