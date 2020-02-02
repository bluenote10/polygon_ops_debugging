#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import os

import numpy as np


def parse_args():
    parser = argparse.ArgumentParser("Check floats.")
    parser.add_argument(
        "x",
        type=float,
        nargs="+",
        help="Value to check",
    )
    parser.add_argument(
        "--steps",
        type=int,
        help="Number of steps",
        default=5,
    )
    args = parser.parse_args()
    return args


def repeated_next_after(x, direction, steps):
    for i in range(steps):
        x = np.nextafter(x, direction)
    return x


def check(xs, steps):
    x_min = repeated_next_after(min(xs), -np.inf, steps)
    x_max = repeated_next_after(max(xs), +np.inf, steps)

    x = x_min
    while x <= x_max:
        print("{} {:<30s} {:30.17g} {:40.30g}".format(
            "[*]" if x in xs else "   ",
            json.dumps(x),
            x,
            x,
        ))
        x = np.nextafter(x, np.inf)


def main():
    args = parse_args()
    check(args.x, args.steps)


if __name__ == "__main__":
    main()
