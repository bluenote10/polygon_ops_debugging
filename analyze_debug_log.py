#!/usr/bin/env python

from __future__ import print_function

import json
import pandas as pd

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
    parser.add_argument(
        "-o", "--output",
        help="Output file basename",
        default="/tmp/iteration",
    )
    args = parser.parse_args()
    return args


def read_file(filename):
    json_lines = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                json_lines.append(json.loads(line))
    return json_lines


def replace_ids(json_lines):
    id = [0]
    addrs = {}

    def fix(addr):
        if isinstance(addr, int):
            return addr
        else:
            if not addr in addrs:
                addrs[addr] = id[0]
                id[0] += 1
            return addrs[addr]

    def replace_ids_rec(data):
        if isinstance(data, list):
            for x in data:
                replace_ids_rec(x)
        elif isinstance(data, dict):
            if "addr" in data:
                data["addr"] = fix(data["addr"])
            # priorities for recursion
            if "processEvent" in data:
                replace_ids_rec(data["processEvent"])
            if "self" in data:
                replace_ids_rec(data["self"])
            for value in data.values():
                replace_ids_rec(value)

    replace_ids_rec(json_lines)


def extract_bounding_box(json_lines):
    min_x = max_x = min_y = max_y = None
    for line in json_lines:
        process_event = line.get("processEvent")
        if process_event is not None:
            for name in ["self", "other"]:
                event = process_event[name]
                x = event["point"]["x"]
                y = event["point"]["y"]
                if x < min_x or min_x is None:
                    min_x = x
                if x > max_x or max_x is None:
                    max_x = x
                if y < min_y or min_y is None:
                    min_y = y
                if y > max_y or max_y is None:
                    max_y = y
    return min_x, max_x, min_y, max_y


def group_by_iteration(json_lines):
    iterations = []
    cur_iteration = {}
    for line in json_lines:
        process_event = line.get("processEvent")
        intersection = line.get("intersection")
        if process_event is not None:
            if len(cur_iteration) > 0:
                iterations.append(cur_iteration)
            cur_iteration = line.copy()
        elif intersection is not None:
            cur_iteration.setdefault("intersections", []).append(intersection)
        else:
            cur_iteration.update(line)
    return iterations


def plot_sequence(json_lines, bb, basename):
    i = 0
    for line in json_lines:
        print(line)
        process_event = line.get("processEvent")
        if process_event is not None:
            p_from = process_event["self"]["point"]
            p_from_x = p_from["x"]
            p_from_y = p_from["y"]
            p_upto = process_event["other"]["point"]
            p_upto_x = p_upto["x"]
            p_upto_y = p_upto["y"]

            if process_event["self"]["type"] == "L":
                color = "#00FF00"
            else:
                color = "#FF0000"

            fig, ax = plt.subplots(1, 1, figsize=(12, 7), sharex=True, sharey=True)
            ax.plot([p_from_x, p_upto_x], [p_from_y, p_upto_y], "-", color="k")
            ax.plot([p_from_x], [p_from_y], "o", ms=2, alpha=0.8, color=color)
            ax.plot([p_upto_x], [p_upto_y], "o", ms=2, alpha=0.8, color="#DDDDDD")

            offset_x = (bb[1] - bb[0]) * 0.03
            offset_y = (bb[3] - bb[2]) * 0.03
            ax.set_xlim([bb[0] - offset_x, bb[1] + offset_x])
            ax.set_ylim([bb[2] - offset_y, bb[3] + offset_y])

            fig.suptitle("{}".format(process_event))
            plt.tight_layout()
            plt.subplots_adjust(top=0.90)
            plt.savefig("{}_{:03d}.png".format(basename, i))
            i += 1

            plt.close(fig)


def main():
    args = parse_args()

    json_lines = read_file(args.debug_file)

    replace_ids(json_lines)
    bb = extract_bounding_box(json_lines)
    plot_sequence(json_lines, bb, args.output)


if __name__ == "__main__":
    main()
