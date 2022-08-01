import argparse
import glob
import os
import random

import numpy as np
from collections import deque

from utils import get_module_logger


def split(source: str, destination: str):
    """
    Create three splits from the processed records. The files should be moved to new folders in the
    same directory. This folder should be named train, val and test.

    args:
        - source [str]: source data directory, contains the processed tf records
        - destination [str]: destination data directory, contains 3 sub folders: train / val / test
    """
    records = glob.glob(f"{source}/*.tfrecord")
    random.shuffle(records)
    records = deque(records)

    partition = {
        "train": int(0.8 * len(records)),
        "val": int(0.1 * len(records)),
        "test": int(0.1 * len(records))
    }

    for pname in partition.keys():
        os.mkdir(f"{destination}/{pname}")

    for pname, psize in partition.items():
        for it in range(psize):
            src_path = records.popleft()
            dst_path = f"{destination}/{pname}/{os.path.basename(src_path)}"
            os.symlink(src_path, dst_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split data into training / validation / testing')
    parser.add_argument('--source', required=True,
                        help='source data directory')
    parser.add_argument('--destination', required=True,
                        help='destination data directory')
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info('Creating splits...')
    split(args.source, args.destination)