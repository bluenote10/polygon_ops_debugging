const predicates = require("robust-predicates");
const ulp = require("ulp");
const fs = require("fs");

function signedArea(p0, p1, p2) {
  return (p0[0] - p2[0]) * (p1[1] - p2[1]) - (p1[0] - p2[0]) * (p0[1] - p2[1]);
}

let p1 = [1.0, 1.0];
let p2 = [1.0, 1.0];

let dx = 90
let dy = 29

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
