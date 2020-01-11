#!/usr/bin/env node
// Test martinez bug https://github.com/w8r/martinez/issues/110

const converter = require("./converter");
const exec = require('child_process').exec;

import * as martinez from "../index";

var bug_id = 110;

const p1 = [[[115,96], [140,206], [120,210], [125,250], [80,300], [115,96]]];
const p2 = [[[111,228], [129,192], [309,282], [111,228]]];
// Variations changing first:
// - x 115 => 116
// - x 115 => 114
// - y 96 => 97
// Variants changing third (the point that cuts the short segment):
// - x 120 => 121 fixes problem
// - x 120 => 119 creates problem with tiny hole

let union = martinez.union(p1, p2);

console.log("raw output:", JSON.stringify(union));

const fn_i = `output/bug_${bug_id}_w8r_input.json`;
const fn_o = `output/bug_${bug_id}_w8r_output.json`;
converter.store_polygons([p1, p2], fn_i);
converter.store_polygons(union, fn_o);

exec(`plot_polygons.py ${fn_i} ${fn_o}`, function callback(error, stdout, stderr){});
