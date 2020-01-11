#!/usr/bin/env node

const converter = require("./converter");
const exec = require('child_process').exec;
const fs = require('fs');

import * as martinez from "../index";


function main() {
  var args = process.argv.slice(2)

  if (args.length < 2) {
    console.log(process.argv);
    console.log("ERROR: Wrong number of arguments.")
  } else {
    let geojson_in = args[0];
    let modes = args.slice(1);

    let data = JSON.parse(fs.readFileSync(geojson_in));

    //const subject = load.sync(path.join(__dirname, 'featureTypes', ts.subjectPoly + '.geojson'));
    let p1_geometry = data.features[0].geometry;
    let p2_geometry = data.features[1].geometry;

    let p1 = p1_geometry.type === "Polygon" ? [p1_geometry.coordinates] : p1.geometry.coordinates;
    let p2 = p2_geometry.type === "Polygon" ? [p2_geometry.coordinates] : p2.geometry.coordinates;

    for (let mode of modes) {

      var op;
      switch (mode) {
        case "union":
          op = martinez.union; break;
        case "intersection":
          op = martinez.intersection; break;
        case "diff":
          op = martinez.diff; break;
        case "xor":
          op = martinez.xor; break;
      }
      if (op == null) {
        throw `Invalid mode: ${mode}`;
      }

      const result = op(p1, p2);

      const fn_i = `output/tmp_w8r_input.json`;
      const fn_o = `output/tmp_w8r_output.json`;
      converter.store_polygons(p1.concat(p2), fn_i);
      converter.store_polygons(result, fn_o);

      exec(`plot_polygons.py ${fn_i} ${fn_o}`, function callback(error, stdout, stderr){});
    }

  }


}

main()
