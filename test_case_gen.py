#!/usr/bin/env python

from __future__ import print_function, division

import argparse
import json
import os

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
    overlapping_segments3 = "overlapping_segments3"
    overlapping_segments4 = "overlapping_segments4"
    collinear_segments1 = "collinear_segments1"
    self_overlaps1 = "self_overlaps1"
    rust_issue12 = "rust_issue12"
    many_vertical1 = "many_vertical1"
    xor_holes1 = "xor_holes1"
    xor_holes2 = "xor_holes2"
    intersections_at_endpoints = "intersections_at_endpoints"

    worldmap = "worldmap"


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


RUST_ISSUE12_A = """[{"exterior":[{"x":0.0,"y":0.0},{"x":128.0,"y":0.0},{"x":128.0,"y":16.0},{"x":16.0,"y":16.0},{"x":16.0,"y":32.0},{"x":32.0,"y":48.0},{"x":32.0,"y":208.0},{"x":48.0,"y":224.0},{"x":64.0,"y":224.0},{"x":64.0,"y":256.0},{"x":80.0,"y":272.0},{"x":0.0,"y":272.0},{"x":0.0,"y":256.0},{"x":0.0,"y":0.0}],"interiors":[]},{"exterior":[{"x":64.0,"y":96.0},{"x":80.0,"y":80.0},{"x":96.0,"y":96.0},{"x":96.0,"y":128.0},{"x":112.0,"y":144.0},{"x":96.0,"y":160.0},{"x":64.0,"y":128.0},{"x":64.0,"y":96.0}],"interiors":[]},{"exterior":[{"x":160.0,"y":176.0},{"x":176.0,"y":160.0},{"x":176.0,"y":144.0},{"x":192.0,"y":128.0},{"x":208.0,"y":128.0},{"x":224.0,"y":144.0},{"x":224.0,"y":160.0},{"x":240.0,"y":176.0},{"x":256.0,"y":176.0},{"x":272.0,"y":192.0},{"x":272.0,"y":208.0},{"x":288.0,"y":208.0},{"x":304.0,"y":192.0},{"x":304.0,"y":144.0},{"x":320.0,"y":128.0},{"x":336.0,"y":128.0},{"x":352.0,"y":144.0},{"x":352.0,"y":176.0},{"x":368.0,"y":192.0},{"x":368.0,"y":224.0},{"x":352.0,"y":240.0},{"x":256.0,"y":240.0},{"x":176.0,"y":240.0},{"x":160.0,"y":224.0},{"x":160.0,"y":176.0}],"interiors":[]},{"exterior":[{"x":192.0,"y":0.0},{"x":256.0,"y":0.0},{"x":480.0,"y":0.0},{"x":480.0,"y":64.0},{"x":464.0,"y":48.0},{"x":416.0,"y":48.0},{"x":400.0,"y":32.0},{"x":416.0,"y":32.0},{"x":400.0,"y":32.0},{"x":336.0,"y":32.0},{"x":320.0,"y":48.0},{"x":304.0,"y":48.0},{"x":304.0,"y":32.0},{"x":288.0,"y":16.0},{"x":256.0,"y":16.0},{"x":192.0,"y":16.0},{"x":192.0,"y":0.0}],"interiors":[]},{"exterior":[{"x":416.0,"y":80.0},{"x":432.0,"y":64.0},{"x":448.0,"y":64.0},{"x":448.0,"y":96.0},{"x":432.0,"y":96.0},{"x":416.0,"y":80.0}],"interiors":[]},{"exterior":[{"x":416.0,"y":256.0},{"x":432.0,"y":240.0},{"x":432.0,"y":224.0},{"x":448.0,"y":208.0},{"x":480.0,"y":208.0},{"x":480.0,"y":256.0},{"x":416.0,"y":256.0}],"interiors":[]}]"""
RUST_ISSUE12_B = """[{"exterior":[{"x":400.0,"y":272.0},{"x":416.0,"y":256.0},{"x":480.0,"y":256.0},{"x":480.0,"y":272.0},{"x":400.0,"y":272.0}],"interiors":[]}]"""
RUST_ISSUE12_C = """[{"exterior":[{"x":384.0,"y":0.0},{"x":416.0,"y":0.0},{"x":448.0,"y":0.0},{"x":448.0,"y":32.0},{"x":416.0,"y":32.0},{"x":384.0,"y":32.0},{"x":384.0,"y":0.0}],"interiors":[]}]"""
RUST_ISSUE12_D = """[{"exterior":[{"x":400.0,"y":32.0},{"x":416.0,"y":32.0},{"x":416.0,"y":48.0},{"x":400.0,"y":32.0}],"interiors":[]}]"""


def convert_from_geo_type_json(string_data):
    """
    Converter for stuff posted on GitHub in geo-types jsons.
    """
    json_data = json.loads(string_data)

    def convert_ring(coords):
        return [
            [coord["x"], coord["y"]] for coord in coords
        ]

    geojson_data = [
        [convert_ring(poly["exterior"])] + [convert_ring(interior) for interior in poly["interiors"]]
        for poly in json_data
    ]
    return geojson_data


# -----------------------------------------------------------------------------
# Geometry data types
# -----------------------------------------------------------------------------

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


# -----------------------------------------------------------------------------
# Geometry helpers
# -----------------------------------------------------------------------------

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


def subdivide_ring(poly_ring, num_subdivisions):
    points = [poly_ring[0]]

    for p_next in poly_ring[1:]:
        p_prev = points[-1]

        ratios = list(np.linspace(0, 1, num_subdivisions + 1))[1:]
        for ratio in ratios:
            x = p_prev[0] + (p_next[0] - p_prev[0]) * ratio
            y = p_prev[1] + (p_next[1] - p_prev[1]) * ratio
            points.append([x, y])

    return points


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


# -----------------------------------------------------------------------------
# Generators
# -----------------------------------------------------------------------------

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


def gen_overlapping_segments_1():
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
            [25, +5],
        ])],
        [close_ring([
            [20, -10],
            [25, -10],
            [25, -5],
        ])],
    ]
    return polys_a, polys_b


def gen_overlapping_segments_boxes():
    polys_a = [
        [gen_poly(2 * i, -1, 2 * i + 1, +1)]
        for i in range(1, 11)
    ]

    def get_modifier(i):
        y_factor = +1 if i <= 5 else -1
        if i % 5 == 1:
            return y_factor, 2 * i, 2 * i + 0.5
        elif i % 5 == 2:
            return y_factor, 2 * i + 0.5, 2 * i + 1
        elif i % 5 == 3:
            return y_factor, 2 * i + 0.25, 2 * i + 0.75
        elif i % 5 == 4:
            return y_factor, 2 * i, 2 * i + 1
        elif i % 5 == 0:
            return y_factor, 2 * i - 0.5, 2 * i + 0.5

    polys_b = [
        [gen_poly(x_min, +1 * y_factor, x_max, +2 * y_factor)]
        for y_factor, x_min, x_max in [get_modifier(i) for i in range(1, 11)]
    ]
    return polys_a, polys_b


def gen_self_overlaps_1():
    polys_a = [
        [gen_poly(0, +1, 1, +2)],
        [gen_poly(1, +1, 2, +2)],
        [gen_poly(3, +1, 4, +2)],
        [gen_poly(3, +2, 4, +3)],
        [close_ring([
            [5, +1],
            [5, +2],
            [6, +2],
        ])],
        [close_ring([
            [6, +2],
            [6, +1],
            [5, +1],
        ])],
    ]
    polys_b = [
        [gen_poly(0, -1, 1, -2)],
        [gen_poly(1, -1, 2, -2)],
        [gen_poly(3, -1, 4, -2)],
        [gen_poly(3, -2, 4, -3)],
        [close_ring([
            [5, -1],
            [5, -2],
            [6, -2],
        ])],
        [close_ring([
            [6, -2],
            [6, -1],
            [5, -1],
        ])],
    ]
    return polys_a, polys_b


def gen_many_vertical1():

    def generate(x0, x1, seed, n=10):
        np.random.seed(seed)

        ys = np.sort(np.random.uniform(-1.0, +1.0, size=2*n)).reshape(n, 2)
        polys = [
            [close_ring([
                [x0, 0],
                [x1, y0],
                [x1, y1],
            ])]
            for y0, y1 in ys
        ]
        return polys

    polys_a = generate(-1.0, +0.5, seed=0)
    polys_b = generate(+1.0, -0.5, seed=1)
    return polys_a, polys_b


def gen_xor_holes1():
    polys_a = [
        [close_ring([
            [-8, -1],
            [-5, +0.5],
            [-2, -1],
        ])],
        [close_ring([
            [+8, -1],
            [+5, +0.5],
            [+2, -1],
        ])],
    ]
    polys_b = [
        [close_ring([
            [-7, +1],
            [-4, -0.5],
            [-1, +1],
        ])],
        [close_ring([
            [+7, +1],
            [+4, -0.5],
            [+1, +1],
        ])],
    ]
    return polys_a, polys_b


def gen_xor_holes2():
    polys_a = [
        [gen_poly(-3, -1, -1, +0.5)],
        [gen_poly(+3, -1, +1, +0.5)],
    ]
    polys_b = [
        [gen_poly(-4, +1, -2, -0.5)],
        [gen_poly(+4, +1, +2, -0.5)],
    ]
    return polys_a, polys_b


def gen_intersections_at_endpoints(r_i, r_o, corner_cutoff):
    c = corner_cutoff
    ring = close_ring([
        [-r_o + c, +r_o],
        [+r_o - c, +r_o],
        [+r_i, +r_i],
        [+r_o, +r_o - c],
        [+r_o, -r_o + c],
        [+r_i, -r_i],
        [+r_o - c, -r_o],
        [-r_o + c, -r_o],
        [-r_i, -r_i],
        [-r_o, -r_o + c],
        [-r_o, +r_o - c],
        [-r_i, +r_i],
    ])
    return [[ring]]


def gen_extract_from_martinez_source(martinez_source, file):
    with open(os.path.join(martinez_source, file)) as f:
        lines = f.readlines()
    num_polys = int(lines[0])
    i = 1
    rings = []
    for _ in range(num_polys):
        num_points = int(lines[i].split()[0])
        i += 1
        points = []
        for _ in range(num_points):
            row = lines[i].split()
            x = float(row[0])
            y = float(row[1])
            points.append([x, y])
            i += 1
        rings.append(close_ring(points))
    return [rings]


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    args = parse_args()

    type_a = "MultiPolygon"
    type_b = "MultiPolygon"
    operation = "union"

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
        polys_a, polys_b = gen_overlapping_segments_1()

    elif args.mode == Modes.overlapping_segments2:
        polys_a = convert_from_geo_type_json(RUST_ISSUE12_C)
        polys_b = convert_from_geo_type_json(RUST_ISSUE12_D)

    elif args.mode == Modes.overlapping_segments3:
        polys_a, polys_b = gen_overlapping_segments_boxes()

    elif args.mode == Modes.overlapping_segments4:
        polys_a, polys_b = gen_overlapping_segments_boxes()
        polys_a = swap_xy(polys_a)
        polys_b = swap_xy(polys_b)

    elif args.mode == Modes.collinear_segments1:
        polys_a = [[subdivide_ring(gen_poly(0, 0, 1, 1), 4)]]
        polys_b = [[subdivide_ring(gen_poly(0, 0.25, 1, 1.25), 4)]]

    elif args.mode == Modes.self_overlaps1:
        polys_a, polys_b = gen_self_overlaps_1()

    elif args.mode == Modes.rust_issue12:
        polys_a = convert_from_geo_type_json(RUST_ISSUE12_A)
        polys_b = convert_from_geo_type_json(RUST_ISSUE12_B)

    elif args.mode == Modes.many_vertical1:
        polys_a, polys_b = gen_many_vertical1()

    elif args.mode == Modes.xor_holes1:
        polys_a, polys_b = gen_xor_holes1()
        operation = "xor"

    elif args.mode == Modes.xor_holes2:
        polys_a, polys_b = gen_xor_holes2()
        operation = "xor"

    elif args.mode == Modes.intersections_at_endpoints:
        polys_a = gen_intersections_at_endpoints(0.1, 10, 1.)
        polys_b = gen_intersections_at_endpoints(0.1, 10, 1.00001)
        # This leads to a crash: investigate later?
        # polys_a = gen_intersections_at_endpoints(0.1, 10, 1)
        # polys_b = gen_intersections_at_endpoints(0.1, 20, 1)
        operation = "union"

    elif args.mode == Modes.worldmap:
        martinez_src = os.path.join(
            os.path.dirname(__file__),
            "../../martinez-src/polygons/worldmap",
        )
        polys_a = gen_extract_from_martinez_source(martinez_src, "worldmap")
        polys_b = gen_extract_from_martinez_source(martinez_src, "15948_squares")

    else:
        raise ValueError("Invalid mode: {}".format(args.mode))

    # print("A:\n{}".format(polys_a))
    # print("B:\n{}".format(polys_b))

    json_output = TEMPLATE.replace("{", "{{").replace("}", "}}").replace("PLACEHOLDER", "{}").format(
        polys_a, type_a, polys_b, type_b, operation,
    )
    # print(json_output)

    if args.output is not None:
        with open(args.output, "w") as f:
            f.write(json_output)


if __name__ == "__main__":
    main()

