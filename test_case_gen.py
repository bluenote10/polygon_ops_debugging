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
        "operation": "PLACEHOLDER"
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
    vertical_ulp_slopes2 = "vertical_ulp_slopes2"
    many_rects = "many_rects"
    overlapping_segments1 = "overlapping_segments1"
    overlapping_segments2 = "overlapping_segments2"


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
    parser.add_argument(
        "--operation",
        help="Which output operation to request in the test case.",
        default="union",
    )
    args = parser.parse_args()
    return args


class Rect(object):
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def overlaps(self, that):
        return (
            self.x_min < that.x_max and that.x_min < self.x_max and
            self.y_min < that.y_max and that.y_min < self.y_max
        )

    def get_poly_ring(self):
        return gen_poly(
            self.x_min,
            self.y_min,
            self.x_max,
            self.y_max,
        )


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


def apply_noise_to_dim(poly_ring, dim, delta_min, delta_max):
    poly_ring = poly_ring[:-1]  # no need to add noise to last (redundant) point

    def apply_noise_to(p):
        if dim == 0:
            return [p[0] + np.random.uniform(delta_min, delta_max), p[1]]
        elif dim == 1:
            return [p[0], p[1] + np.random.uniform(delta_min, delta_max)]

    new_poly_ring = [apply_noise_to(p) for p in poly_ring]
    return new_poly_ring + [new_poly_ring[0]]


def close_ring(points):
    return points + [points[0]]


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


def gen_many_rects(seed):
    np.random.seed(seed)
    rects = []
    for _ in range(100):
        x = np.random.uniform(-100, +100)
        y = np.random.uniform(-100, +100)
        w = np.random.uniform(20, 50)
        h = np.random.uniform(20, 50)
        r = Rect(x - w / 2, y - h / 2, x + w / 2, y + w / 2)
        if not any([r.overlaps(other) for other in rects]):
            rects.append(r)
    polys = []
    for r in rects:
        polys.append([r.get_poly_ring()])
    return polys


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

    elif args.mode == Modes.vertical_ulp_slopes2:
        np.random.seed(2)
        polys_a = gen_rects_ulp_slopes()
        polys_b = swap_xy(polys_a)
        polys_a = [
            [apply_noise_to_dim(ring, 1, -0.2, +0.2) for ring in poly]
            for poly in polys_a
        ]
        polys_b = [
            [apply_noise_to_dim(ring, 0, -0.2, +0.2) for ring in poly]
            for poly in polys_b
        ]

    elif args.mode == Modes.many_rects:
        polys_a = gen_many_rects(1)
        polys_b = gen_many_rects(2)

    elif args.mode == Modes.overlapping_segments1:
        polys_a = [
            [close_ring([
                [10, +10],
                [15, +10],
                [15, +20],
            ])],
            [close_ring([
                [10, -10],
                [15, -10],
                [15, -20],
            ])],
            [close_ring([
                [20, +10],
                [25, +10],
                [25, +20],
            ])],
            [close_ring([
                [20, -10],
                [25, -10],
                [25, -20],
            ])],
        ]
        polys_b = [
            [close_ring([
                [10, +10],
                [15, +10],
                [15, +15],
            ])],
            [close_ring([
                [10, -10],
                [15, -10],
                [15, -15],
            ])],
            [close_ring([
                [20, +10],
                [25, +10],
                [25,  +5],
            ])],
            [close_ring([
                [20, -10],
                [25, -10],
                [25,  -5],
            ])],
        ]

    elif args.mode == Modes.overlapping_segments2:
        polys_a = [
            [gen_poly(2*i, -1, 2*i+1, +1)]
            for i in range(1, 9)
        ]

        def get_modifier(i):
            y_factor = +1 if i < 4 else -1
            if i % 4 == 0:
                return y_factor, 2*i, 2*i + 1
            elif i % 4 == 1:
                return y_factor, 2*i, 2*i + 0.5
            elif i % 4 == 2:
                return y_factor, 2*i + 0.5, 2*i + 1
            elif i % 4 == 3:
                return y_factor, 2*i + 0.25, 2*i + 0.75

        polys_b = [
            [gen_poly(x_min, +1 * y_factor, x_max, +2 * y_factor)]
            for y_factor, x_min, x_max in [get_modifier(i) for i in range(1, 9)]
        ]

    else:
        raise ValueError("Invalid mode: {}".format(args.mode))

    print("A:\n{}".format(polys_a))
    print("B:\n{}".format(polys_b))

    json_output = TEMPLATE.replace("{", "{{").replace("}", "}}").replace("PLACEHOLDER", "{}").format(
        polys_a, type_a, polys_b, type_b, args.operation,
    )

    print(json_output)

    if args.output is not None:
        with open(args.output, "w") as f:
            f.write(json_output)


if __name__ == "__main__":
    main()

