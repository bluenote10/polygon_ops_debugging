const predicates = require("robust-predicates");
const ulp = require("ulp");
const fs = require("fs");

function signedAreaApprox2(r, q, p) {
  var prx = p[0] - r[0]
  var pry = p[1] - r[1]
  var qrx = q[0] - r[0]
  var qry = q[1] - r[1]
  return prx * qry - pry * qrx
}

function signedAreaApprox(p0, p1, p2) {
  return (p0[0] - p2[0]) * (p1[1] - p2[1]) - (p1[0] - p2[0]) * (p0[1] - p2[1]);
}

function signedAreaRobust(p0, p1, p2) {
  return -predicates.orient2d(p0[0], p0[1], p1[0], p1[1], p2[0], p2[1]);
}

function applyDelta(x, deltaSteps) {
  var deltaFunc;
  if (deltaSteps > 0) {
    deltaFunc = ulp.nextUp;
  } else if (deltaSteps < 0) {
    deltaFunc = ulp.nextDown;
  } else {
    return x;
  }
  for (let i = 0; i < Math.abs(deltaSteps); i++) {
    x = deltaFunc(x);
  }
  return x;
}

function constructPZoom(p1, p2) {
  let pZoom = [
    p1[0] * alpha + (1 - alpha) * p2[0],
    p1[1] * alpha + (1 - alpha) * p2[1],
  ];
  return pZoom;
}

function generateGrid(p1, p2, pZoom, method) {
  console.log(`Zooming around ${pZoom}`)

  let dxMax = 50
  let dyMax = 50

  let result = [];

  let signedArea = method == "robust" ? signedAreaRobust : signedAreaApprox;

  for (let dx = -dxMax; dx <= dxMax; dx++) {
    for (let dy = -dyMax; dy <= dyMax; dy++) {
      let x = applyDelta(pZoom[0], dx);
      let y = applyDelta(pZoom[1], dy);
      //let o = signedArea([x, y], p1, p2);
      let o = signedArea(p1, p2, [x, y]);
      result.push({
        x: x,
        y: y,
        i: dx + dxMax,
        j: dy + dyMax,
        o: o,
      })
    }
  }

  fs.writeFileSync(`data_point_on_line_${method}.json`, JSON.stringify(result, null, 2));
}


function main() {
  //let p1 = [2e21, 0.0];
  //let p2 = [2e-21, 7.0000001];

  //let p1 = [-1, -1];
  //let p2 = [1, 1];
  //let alpha = 0.55;

  let p1 = [12, 12];
  let p2 = [24, 24];
  let pZoom = [0.5, 0.5];
  //let p1 = [0.5, 0.5];
  //let p2 = [12, 12];
  //let pZoom = [24, 24];

  generateGrid(p1, p2, pZoom, "robust");
  generateGrid(p1, p2, pZoom, "approx");
}

main();

/*
for (let i = 0; i < dx; i++) {
  p2[0] = ulp.nextUp(p2[0]);
}
for (let i = 0; i < dy; i++) {
  p2[1] = ulp.nextUp(p2[1]);
}

console.log(p1);
console.log(p2);

let result = [];

let x = p1[0];
for (let i = 0; i <= dx; i++) {
  let y = p1[1];
  for (let j = 0; j <= dy; j++) {
    let o = predicates.orient2d(x, y, p1[0], p1[1], p2[0], p2[1]);
    //let o = signedArea([x, y], p1, p2);
    result.push({
      x: x,
      y: y,
      i: i,
      j: j,
      o: o,
    })
    console.log(x, y, o);
    y = ulp.nextUp(y);
  }
  x = ulp.nextUp(x);
}

fs.writeFileSync("data.json", JSON.stringify(result, null, 2));
*/