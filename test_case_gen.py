#!/usr/bin/env python

from __future__ import print_function, division

import argparse

import numpy as np


TEMPLATE = """
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
}
"""


class Modes(object):
    checkerboard1 = "checkerboard1"
    nested_polys = "nested_polys"
    multiple_depth_zero = "multiple_depth_zero"
    vertical_ulp_slopes1 = "vertical_ulp_slopes1"


def parse_args():
    parser = argparse.ArgumentParser("Tool to generate test cases")
    parser.add_argument(
        "mode",
        choices=sorted([k for k in Modes.__dict__.keys() if not k.startswith("__")]),
        help="Test case to generate"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output JSON file"
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


def gen_rects_ulp_slopes(x_ext=1.0, y_ext=2.0):
    n = 9
    xs = np.linspace(-x_ext, +x_ext, 2 * n)

    polys = []
    i = 0
    for l in [-1, 0, +1]:
        for r in [-1, 0, +1]:
            x_l = xs[i]
            x_r = xs[i + 1]

            p = gen_poly(x_l, -y_ext, x_r, +y_ext)

            # Note: upper left is on index 1, upper right on index 2
            if l < 0:
                p[1][0] = np.nextafter(p[1][0], -np.inf)
            elif l > 0:
                p[1][0] = np.nextafter(p[1][0], +np.inf)
            if r < 0:
                p[2][0] = np.nextafter(p[2][0], -np.inf)
            elif r > 0:
                p[2][0] = np.nextafter(p[2][0], +np.inf)

            polys.append([p])   # wrap in list to convert ring to true poly
            i += 2

    return polys


def swap_xy(polys):
    return [
        [
            [
                [p[1], p[0]]
                for p in ring
            ]
            for ring in poly
        ]
        for poly in polys
    ]


def main():
    args = parse_args()

    type_a = "MultiPolygon"
    type_b = "MultiPolygon"

    if args.mode == Modes.checkerboard1:
        polys_a = []
        polys_b = []
        for i in range(3):
            for j in range(3):
                poly = gen_poly(i, j, i+1, j+1)
                if (i + j) % 2 == 0:
                    polys_a.append([poly])
                else:
                    polys_b.append([poly])

    elif args.mode == Modes.nested_polys:
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

    elif args.mode == Modes.multiple_depth_zero:
        polys_a = [
            [gen_square(0.9, center_x=1, center_y=1)],
            [gen_square(0.9, center_x=2, center_y=2)],
        ]
        polys_b = [
            [gen_square(0.9, center_x=1, center_y=2)],
            [gen_square(0.9, center_x=2, center_y=1)],
        ]

    elif args.mode == Modes.vertical_ulp_slopes1:
        polys_a = gen_rects_ulp_slopes()
        polys_b = swap_xy(polys_a)

    else:
        raise ValueError("Invalid mode: {}".format(args.mode))

    print("A:\n{}".format(polys_a))
    print("B:\n{}".format(polys_b))

    json_output = TEMPLATE.replace("{", "{{").replace("}", "}}").replace("PLACEHOLDER", "{}").format(
        polys_a, type_a, polys_b, type_b
    )

    print(json_output)

    if args.output is not None:
        with open(args.output, "w") as f:
            f.write(json_output)


if __name__ == "__main__":
    main()

