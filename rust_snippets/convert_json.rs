extern crate geo_booleanop_tests;

use geojson::GeoJson;

use geo_booleanop_tests::helper::load_fixture_from_path;
use geo_booleanop_tests::compact_geojson::write_compact_geojson;

use serde_json::json;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename_in = &args[1];
    let filename_out = &args[2];

    let geojson = load_fixture_from_path(&filename_in);

    let features = match geojson {
        GeoJson::FeatureCollection(collection) => collection.features,
        _ => panic!("Fixture is not a feature collection"),
    };

    write_compact_geojson(&features, &filename_out);

    let x = 117.63331139400017;
    let y = json!(x);
    let z = serde_json::to_string(&y).expect("Conversion failed");

    println!("{} {} {}", x, y, z);

    let x_val = 117.63331139400017;
    let x_str = x_val.to_string();
    println!("{} == {}", x_val, x_str);

    let x_parsed: f64 = serde_json::from_str(&json!(x_val).to_string()).unwrap();
    println!("{} == {}", x_val, x_parsed);

    //println!("{}", json!(x_val).to_string());
    println!("117.63331139400017 == {:?}", serde_json::from_str::<f64>("117.63331139400017").unwrap());
    println!("117.63331139400017 == {:?}", serde_json::from_str::<serde_json::Value>("117.63331139400017").unwrap());
    println!("117.63331139400017 == {:?}", "117.63331139400017".parse::<f64>().unwrap());

}