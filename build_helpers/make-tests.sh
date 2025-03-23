#!/bin/bash

source venv/bin/activate

for w in plant_common camera diagnostics illumination
do
  echo "Running $w tests"
  pytest "./$w/"
done
