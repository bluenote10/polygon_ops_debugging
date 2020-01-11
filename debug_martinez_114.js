#!/usr/bin/env node
// Test martinez bug https://github.com/w8r/martinez/issues/114

const converter = require("./converter");
const exec = require('child_process').exec;

import * as martinez from "../index";

var bug_id = 114;

const p1 = [[
  [180.60987101280907, 22.943242898435663],
  [280.6098710128091, 22.943242898435663],
  [280.6098710128091, 62.94324289843566],
  [180.60987101280907, 62.94324289843566],
  [180.60987101280907, 22.943242898435663]
]];
const p2 = [[
  [-5.65625, 110.828125],
  [-7.53125, 202.234375],
  [366.0625, 202.234375],
  [356.6875, 65.828125],
  [260.125, 59.265625],
  [253.09375, 40.984375],
  [189.34375, 19.890625],
  [141.0625, 36.765625],
  [111.53125, 6.765625],
  [73.5625, 36.765625],
  [67.46875, 10.984375],
  [41.21875, 10.515625],
  [36.0625, 42.390625],
  [65.59375, 53.171875],
  [-5.65625, 110.828125]
]];

let union = martinez.union(p1, p2);

console.log("raw output:", JSON.stringify(union));

const fn_i = `output/bug_${bug_id}_w8r_input.json`;
const fn_o = `output/bug_${bug_id}_w8r_output.json`;
converter.store_polygons([p1, p2], fn_i);
converter.store_polygons(union, fn_o);

exec(`plot_polygons.py ${fn_i} ${fn_o}`, function callback(error, stdout, stderr){});
