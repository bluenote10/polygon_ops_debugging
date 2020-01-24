// To write GeoJSON with plain serde:
use geojson::{GeoJson, Feature, FeatureCollection, Value, Geometry};

let output_geojson = GeoJson::FeatureCollection(FeatureCollection {
  bbox: None,
  features: output_features,
  foreign_members: None,
});
let f = File::create(filename).expect("Unable to create json file.");
serde_json::to_writer_pretty(f, &output_geojson).expect("Unable to write json file.");
