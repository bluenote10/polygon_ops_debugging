#!/usr/bin/env node
// Test martinez bug https://github.com/w8r/martinez/issues/80

const converter = require("./converter");
const exec = require('child_process').exec;

import * as martinez from "../index";

var bug_id = 80;

let p1 = [
	[[ 10, 10 ], [ 80, 10 ], [ 80, 80 ], [ 10, 80 ], [ 10, 10 ]]
];

let p2 = [
	[[ 20, 10 ], [ 30, 10 ], [ 30, 80 ], [ 20, 80 ], [ 20, 10 ]]
];

let union = martinez.diff(p1, p2);

console.log("raw output:", JSON.stringify(union));

const fn_i = `output/bug_${bug_id}_w8r_input.json`;
const fn_o = `output/bug_${bug_id}_w8r_output.json`;
converter.store_polygons([p1, p2], fn_i);
converter.store_polygons(union, fn_o);

exec(`plot_polygons.py ${fn_i} ${fn_o}`, function callback(error, stdout, stderr){});
