#!/usr/bin/env node
// Test martinez bug https://github.com/w8r/martinez/issues/97

const converter = require("./converter");
const exec = require('child_process').exec;

import * as martinez from "../index";

var bug_id = 97;

const p1 = [[
  [0, 0],
  [1, 0],
  [1, 1],
  [0, 1],
  [0, 0]
]];

const p2 = [[
  [0.5, 0.0],
  [0.6, 0.5],
  [0.7, 0.5],
  [0.5, 0.0]
]];

let union = martinez.intersection(p1, p2);

console.log("raw output:", JSON.stringify(union));

const fn_i = `output/bug_${bug_id}_w8r_input.json`;
const fn_o = `output/bug_${bug_id}_w8r_output.json`;
converter.store_polygons([p1, p2], fn_i);
converter.store_polygons(union, fn_o);

exec(`plot_polygons.py ${fn_i} ${fn_o}`, function callback(error, stdout, stderr){});
