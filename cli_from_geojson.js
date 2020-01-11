#!/usr/bin/env node

const converter = require("./converter");
const exec = require('child_process').exec;
const fs = require('fs');

import * as martinez from "../index";


function main() {
  var args = process.argv.slice(2)

  if (args.length != 2) {
    console.log(process.argv);
    console.log("ERROR: Wrong number of arguments.")
  } else {
    var geojson_in = args[0];
    var mode = args[1];

    let data = JSON.parse(fs.readFileSync(filename_in));
    console.log(data);

    const subject = load.sync(path.join(__dirname, 'featureTypes', ts.subjectPoly + '.geojson'));

    const expectedIntResult = load.sync(path.join(outDir, 'intersection', t.name + '.geojson'))
    if (expectedIntResult.geometry.type === 'Polygon') expectedIntResult.geometry.coordinates = [expectedIntResult.geometry.coordinates]
    const intResult = martinez.intersection(subject.geometry.coordinates, clipping.geometry.coordinates);
    t.same(intResult, expectedIntResult.geometry.coordinates, ts.testName + ' - Intersect');



    let polygons = convert_input(data);
    console.log(JSON.stringify(polygons));

    var union = polygons[0];
    for (var i = 1; i < polygons.length; i++) {
      union = PolyBool.union(union, polygons[i]);
      console.log(JSON.stringify(union));
    }

    /*
    var segments = PolyBool.segments(polygons[0]);
    for (var i = 1; i < polygons.length; i++){
      var seg2 = PolyBool.segments(polygons[i]);
      var comb = PolyBool.combine(segments, seg2);
      segments = PolyBool.selectUnion(comb);
    }
    var union = PolyBool.polygon(segments);
    */

    console.log(JSON.stringify(union));

    let output_converted = convert_output(union);
    console.log(JSON.stringify(output_converted));
    fs.writeFileSync(filename_out, JSON.stringify(output_converted));
  }


}

main()
