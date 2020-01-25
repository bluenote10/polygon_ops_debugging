#!/usr/bin/env python

from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import json
import sys


def plot(ax, data, predicate, color):

    xs = []
    ys = []
    for row in data:
        x = float(row["i"])
        y = float(row["j"])
        o = float(row["o"])
        if predicate(o):
            xs.append(x)
            ys.append(y)

    print(xs)
    print(ys)
    ax.plot(xs, ys, "o", color=color, ms=10)


def map_value(x):
    if x < 0:
        return -1
    elif x > 0:
        return +1
    else:
        return 0

def main():
    if len(sys.argv) != 2:
        print("Wrong number of arguments")
        sys.exit(1)

    filename = sys.argv[1]
    data = json.load(open(filename))

    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    plt.subplots_adjust(bottom=0.15, top=0.95, left=0.15, right=0.90)

    size_x = max([row["i"] for row in data]) + 1
    size_y = max([row["j"] for row in data]) + 1

    img = np.array([map_value(row["o"]) for row in data]).reshape((size_y, size_x), order="F")

    ax.imshow(img, aspect='auto', origin='lower', cmap='jet')

    # Major ticks
    ax.set_xticks(np.arange(0, size_x, 1));
    ax.set_yticks(np.arange(0, size_y, 1));

    # Labels for major ticks
    ax.set_xticklabels([""] * size_x) # np.arange(0, size_x, 1));
    ax.set_yticklabels([""] * size_y) # np.arange(0, size_y, 1));

    # Minor ticks
    ax.set_xticks(np.arange(-.5, size_x, 1), minor=True);
    ax.set_yticks(np.arange(-.5, size_y, 1), minor=True);

    # Gridlines based on minor ticks
    ax.grid(which='minor', color='k', linestyle='-', linewidth=1)

    fig.tight_layout()
    plt.show()



    """
    plot(ax, data, lambda x: x < 0, "g")
    plot(ax, data, lambda x: x > 0, "r")
    plot(ax, data, lambda x: x == 0, "b")

    #x_min = min([row["x"] for row in data])
    #x_max = max([row["x"] for row in data])
    #y_min = min([row["y"] for row in data])
    #y_max = max([row["y"] for row in data])
    #ax.set_xlim((x_min, x_max))
    #ax.set_ylim((y_min, y_max))

    xs_i = sorted(list(set([(row["i"], row["x"]) for row in data])))
    ys_j = sorted(list(set([(row["j"], row["y"]) for row in data])))
    print(xs_i)
    print(ys_j)
    ax.set_xticks([tick for tick, label in xs_i])
    ax.set_xticklabels([label.__repr__() for tick, label in xs_i], rotation=-20, ha="left")
    ax.set_yticks([tick for tick, label in ys_j])
    ax.set_yticklabels([label.__repr__() for tick, label in ys_j])

    #ax.tick_params(axis='x', rotation=-20)

    plt.show()
    """

main()