#!/usr/bin/env node
// Test martinez bug https://github.com/w8r/martinez/issues/97

const converter = require("./converter");
const exec = require('child_process').exec;

import * as martinez from "../index";

var bug_id = 97;

let p1 = [
	[
		[
			-492.1913921306456,
			-246.09569606532278
		],
		[
			-492.1913921306456,
			246.09569606532278
		],
		[
			328.12759475376373,
			164.06379737688187
		],
		[
			328.12759475376373,
			82.03189868844093
		],
		[
			0,
			98.43827842612912
		],
		[
			0,
			-98.43827842612912
		],
		[
			328.12759475376373,
			-82.03189868844093
		],
		[
			328.12759475376373,
			-164.06379737688187
		],
		[
			-492.1913921306456,
			-246.09569606532278
		]
	]
];

let p2 = [
	[
		[
			118.12593411135472,
			92.53198172056138
		],
		[
			328.12759475376373,
			82.03189868844093
		],
		[
			328.12759475376373,
			92.53198172056136
		],
		[
			118.12593411135472,
			92.53198172056138
		]
	]
]
;

/*
p1 = [[
  [0,0],
  [3,0],
  [3,3],
  [0,3],
  [0,0]
]];
p2 = [[
  [1,0],
  [2,0],
  [2,4],
  [1,4],
  [1,0]
]];
*/

let union = martinez.diff(p1, p2);

console.log("raw output:", JSON.stringify(union));

const fn_i = `output/bug_${bug_id}_w8r_input.json`;
const fn_o = `output/bug_${bug_id}_w8r_output.json`;
converter.store_polygons([p1, p2], fn_i);
converter.store_polygons(union, fn_o);

exec(`plot_polygons.py ${fn_i} ${fn_o}`, function callback(error, stdout, stderr){});
