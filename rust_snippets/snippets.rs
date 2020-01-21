// To write GeoJSON with plain serde:
let f = File::create(filename).expect("Unable to create json file.");
serde_json::to_writer_pretty(f, &output_geojson).expect("Unable to write json file.");
