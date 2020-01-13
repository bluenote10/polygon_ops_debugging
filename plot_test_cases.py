#!/usr/bin/env python

from __future__ import print_function

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import json
import os
import sys


def extract_multi_polygon(feature):
    kind = feature["geometry"]["type"]
    if kind == "Polygon":
        return [feature["geometry"]["coordinates"]]
    elif kind == "MultiPolygon":
        return feature["geometry"]["coordinates"]
    else:
        raise ValueError("Feature has wrong type: {}".format(kind))


def plot(ax, multi_polygon, label):
    for j, polygon in enumerate(multi_polygon):
        for k, ring in enumerate(polygon):
            xs = [p[0] for p in ring]
            ys = [p[1] for p in ring]
            ax.plot(xs, ys, "o-", label="{} (poly = {}, ring = {})".format(label, j + 1, k + 1), ms=2)


def main(interactive=False):
    if len(sys.argv) < 2:
        print("ERROR: No geojson files specified.")
        sys.exit(1)

    else:
        files = sys.argv[1:]

        with PdfPages("test_cases.pdf") as pp:

            for f in sorted(files):
                data = json.load(open(f))
                assert data["type"] == "FeatureCollection"

                features = data["features"]
                assert len(features) >= 2

                p1 = extract_multi_polygon(features[0])
                p2 = extract_multi_polygon(features[1])

                for feature in features[2:]:
                    op = feature["properties"]["operation"]
                    p_res = extract_multi_polygon(feature)

                    fig, axes = plt.subplots(1, 3, figsize=(18, 10), sharex=True, sharey=True)

                    plot(axes[0], p1, "A")
                    plot(axes[0], p2, "B")

                    plot(axes[1], p_res, "Result")

                    plot(axes[2], p1, "A")
                    plot(axes[2], p2, "B")
                    plot(axes[2], p_res, "Result")

                    #filename_out = filename.replace(".json", ".png")
                    #plt.savefig(filename_out)

                    axes[0].legend(loc="best")
                    axes[1].legend(loc="best")
                    axes[2].legend(loc="best")

                    fig.suptitle("{} / {}".format(os.path.basename(f), op))

                    plt.tight_layout()
                    plt.subplots_adjust(top=0.93)

                    if interactive:
                        plt.show()

                    pp.savefig(fig)
                    plt.close(fig)


if __name__ == "__main__":
    main()
