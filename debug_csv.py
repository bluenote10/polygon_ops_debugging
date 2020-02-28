#!/usr/bin/env python

from __future__ import print_function

import pandas as pd
import tabloo

import matplotlib.pyplot as plt
from matplotlib import collections

import argparse


def parse_args():
    parser = argparse.ArgumentParser("Tool to plot test cases")
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Show interactive plot windows."
    )
    parser.add_argument(
        "debug_file",
        help="Debug file",
    )
    args = parser.parse_args()
    return args


def plot_by_column(ax, df, by_column):
    df = df.loc[df["lr"] == "L", :]

    for kind in df[by_column].unique():
        sub_df = df.loc[df[by_column] == kind, :]
        lines = [
            [(row["x"], row["y"]), (row["other_x"], row["other_y"])]
            for _, row in sub_df.iterrows()
        ]
        color = ax._get_lines.prop_cycler.next()['color']
        #color = ax._get_lines.get_next_color()
        lc = collections.LineCollection(lines, color=color, label=kind, alpha=0.5)
        ax.add_collection(lc)
        #ax.plot([], [])

    ax.autoscale()
    ax.margins(0.1)
    ax.legend()


def main():
    args = parse_args()

    df = pd.read_csv(args.debug_file, sep=";")
    print(df)

    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True, sharey=True)

    plot_by_column(axes[0], df, "result_transition")
    plot_by_column(axes[1], df, "in_out")
    plot_by_column(axes[2], df, "other_in_out")

    plt.show()

    if args.interactive:
        tabloo.show(df)


if __name__ == "__main__":
    main()
