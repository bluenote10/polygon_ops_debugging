#!/usr/bin/env python

from __future__ import print_function, division

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import PathPatch
from matplotlib.path import Path

import argparse
import json
import os


def parse_args():
    parser = argparse.ArgumentParser("Tool to plot test cases")
    parser.add_argument(
        "mode",
        choices=[
            "checkerboard1",
            "nested_polys",
            "multiple_depth_zero",
        ]
    )
    args = parser.parse_args()
    return args


def gen_poly(x_min, y_min, x_max, y_max):
    return [
        [x_min, y_min],
        [x_min, y_max],
        [x_max, y_max],
        [x_max, y_min],
        [x_min, y_min],
    ]


def gen_square(size, center_x=0, center_y=0):
    return gen_poly(
        center_x - size / 2,
        center_y - size / 2,
        center_x + size / 2,
        center_y + size / 2,
    )


def main():
    args = parse_args()

    type_a = "MultiPolygon"
    type_b = "MultiPolygon"

    if args.mode == "checkerboard1":
        polys_a = []
        polys_b = []
        for i in range(3):
            for j in range(3):
                poly = gen_poly(i, j, i+1, j+1)
                if (i + j) % 2 == 0:
                    polys_a.append([poly])
                else:
                    polys_b.append([poly])

    elif args.mode == "nested_polys":
        polys_a = [
            [gen_square(20), gen_square(19)],
            [gen_square(18), gen_square(17)],
            #[gen_square(16), gen_square(15)],
        ]
        polys_b = [
            [gen_square(14), gen_square(13)],
            [gen_square(12), gen_square(11)],
            #[gen_square(10), gen_square(9)],
        ]

    elif args.mode == "multiple_depth_zero":
        polys_a = [
            [gen_square(0.9, center_x=1, center_y=1)],
            [gen_square(0.9, center_x=2, center_y=2)],
        ]
        polys_b = [
            [gen_square(0.9, center_x=1, center_y=2)],
            [gen_square(0.9, center_x=2, center_y=1)],
        ]

    print("A:\n{}".format(polys_a))
    print("B:\n{}".format(polys_b))

    print("""
{
  "features": [
    {
      "geometry": {
        "coordinates": PLACEHOLDER,
        "type": "PLACEHOLDER"
      },
      "properties": {},
      "type": "Feature"
    },
    {
      "geometry": {
        "coordinates": PLACEHOLDER,
        "type": "PLACEHOLDER"
      },
      "properties": {},
      "type": "Feature"
    },
    {
      "geometry": {
        "coordinates": [
        ],
        "type": "MultiPolygon"
      },
      "properties": {
        "operation": "union"
      },
      "type": "Feature"
    }
  ],
 "type": "FeatureCollection"
}""".replace("{", "{{").replace("}", "}}").replace("PLACEHOLDER", "{}").format(
        polys_a, type_a, polys_b, type_b
    ))

if __name__ == "__main__":
    main()

