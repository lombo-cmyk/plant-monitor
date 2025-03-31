#!/bin/bash

if [ ! -d "venv" ]; then
  echo "Creating new python env"
  python -m venv venv
fi

source venv/bin/activate

python -m pip install --upgrade pip

for w in plant_common camera diagnostics illumination notification
do
  echo "Installing requirements for $w"
  python -m pip install -r "$w/requirements.txt" -q
done
echo "Installing test requirements"
python -m pip install -r ./build_helpers/requirements-test.txt -q

for module in plant_common camera diagnostics illumination notification
do
  echo "Installing module $module"
  python -m pip install -e "./$module" -q
done
