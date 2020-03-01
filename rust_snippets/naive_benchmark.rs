extern crate geo_booleanop_tests;

use std::time::Instant;

use geo_booleanop::boolean::BooleanOp;
use geo_booleanop_tests::helper::load_test_case;

#[allow(dead_code)]
fn main_non_batched() {
    let (_, p1, p2) = load_test_case("tests/fixtures/generic_test_cases/issue96.geojson");

    let n = 5050;
    let mut result = p1.intersection(&p2);

    for _ in 0..2048 {
        result = p1.intersection(&p2);
    }

    let t1 = Instant::now();
    for _ in 0..n {
        result = p1.intersection(&p2);
    }
    let t2 = Instant::now();

    let elapsed = t2 - t1;
    println!("time: {:.1} us", elapsed.as_secs_f64() / n as f64 * 1e6);
    assert!(result.0.len() > 0);
}

#[allow(dead_code)]
fn main_batched() {
    let (_, p1, p2) = load_test_case("tests/fixtures/generic_test_cases/issue96.geojson");

    let mut result = p1.intersection(&p2);

    for _ in 0..2048 {
        result = p1.intersection(&p2);
    }

    let mut min_elapsed = std::f64::MAX;
    let n = 505;
    let batches = 10;

    let mut times: Vec<f64> = (0..batches).map(|_| {
        let t1 = Instant::now();
        for _ in 0..n {
            result = p1.intersection(&p2);
        }
        let t2 = Instant::now();
        let elapsed = (t2 - t1).as_secs_f64();
        if elapsed < min_elapsed {
            min_elapsed = elapsed;
        }
        elapsed / n as f64 * 1e6
    }).collect();
    times.sort_by(|a, b| a.partial_cmp(b).unwrap());

    println!("{:?}", times);
    assert!(result.0.len() > 0);
}

fn main() {
    let (_, p1, p2) = load_test_case("tests/fixtures/generic_test_cases/issue96.geojson");

    let mut result = p1.intersection(&p2);

    for _ in 0..2048 {
        result = p1.intersection(&p2);
    }

    let mut min_elapsed = std::f64::MAX;
    let n = 505;
    let batches = 30;

    let mut times: Vec<f64> = (0..batches).map(|_| {
        let (_, p1, p2) = load_test_case("tests/fixtures/generic_test_cases/issue96.geojson");
        let t1 = Instant::now();
        for _ in 0..n {
            result = p1.intersection(&p2);
        }
        let t2 = Instant::now();
        let elapsed = (t2 - t1).as_secs_f64();
        if elapsed < min_elapsed {
            min_elapsed = elapsed;
        }
        elapsed / n as f64 * 1e6
    }).collect();
    times.sort_by(|a, b| a.partial_cmp(b).unwrap());

    println!("{:?}", times);
    assert!(result.0.len() > 0);
}
