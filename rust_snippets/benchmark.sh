#!/bin/bash

for i in {1..20}
do
  cargo bench --bench benchmark
  #cargo run --bin naive_benchmark --release
  #target/release/naive_benchmark
done
