#!/usr/bin/env node

const converter = require("./converter");
const exec = require('child_process').exec;
const fs = require('fs');
const path = require('path');
import stringify from 'json-stringify-pretty-compact';

import * as martinez from "../index";


function extractExpectedResults(features) {
  return features.map(feature => {
    let mode = feature.properties.operation;
    var op;
    switch (mode) {
      case "union":
        op = martinez.union;
        break;
      case "intersection":
        op = martinez.intersection;
        break;
      case "xor":
        op = martinez.xor;
        break;
      case "diff":
        op = martinez.diff;
        break;
      case "diff_ba":
        op = (a, b) => martinez.diff(b, a);
        break;
    }
    if (op == null) {
      throw `Invalid mode: ${mode}`;
    }
    return {
      op: op,
      coordinates: feature.geometry.coordinates,
    };
  });
}


function runTestCase(testCaseFile) {
  let testName = 'Generic test case: ' + path.basename(testCaseFile);

  //const data = load.sync(testCaseFile);
  const data = JSON.parse(fs.readFileSync(testCaseFile));
  if (data.features.length < 2) {
    throw `Test case file must contain at least two features, but ${testCaseFile} doesn't.`;
  }

  let p1Geometry = data.features[0].geometry;
  let p2Geometry = data.features[1].geometry;

  let p1 = p1Geometry.type === 'Polygon' ? [p1Geometry.coordinates] : p1Geometry.coordinates;
  let p2 = p2Geometry.type === 'Polygon' ? [p2Geometry.coordinates] : p2Geometry.coordinates;

  let expectedResults = extractExpectedResults(data.features.slice(2));

  let featureIndex = 2;
  for (const expectedResult of expectedResults) {
    const result = expectedResult.op(p1, p2);

    // Update output data for re-generation mode
    data.features[featureIndex].geometry.type = 'MultiPolygon';
    data.features[featureIndex].geometry.coordinates = result;
    featureIndex += 1;
  }

  let resultFile = testCaseFile + ".generated";
  fs.writeFileSync(resultFile, stringify(data));
  console.log("Written: " + resultFile);

  return resultFile;
}


function main() {
  var args = process.argv.slice(2)

  if (args.length < 1) {
    console.log(process.argv);
    console.log("ERROR: Wrong number of arguments.")
  } else {
    let testCaseFile = args[0];

    let resultTestCaseFile = runTestCase(testCaseFile);

    let cmd = `plot_test_cases.py -i ${resultTestCaseFile}`;
    console.log("Running: " + cmd);
    //exec(cmd, function callback(error, stdout, stderr){});
    var spawn = require('child_process').spawn;
    spawn('plot_test_cases.py', ['-i', resultTestCaseFile], { stdio: 'inherit' });
  }
}

/*
function main_old() {
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
        case "diff_ba":
          op = (a, b) => martinez.diff(b, a); break;
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

      let cmd = `plot_polygons.py ${fn_i} ${fn_o}`;
      console.log("Running: " + cmd);
      exec(cmd, function callback(error, stdout, stderr){});
    }

  }

}
*/

main()
