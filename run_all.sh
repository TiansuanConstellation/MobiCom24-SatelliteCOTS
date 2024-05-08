#!/usr/bin/bash

echo "Running tests under Temperature-Overview"
cd Temperature-Overview
python plot-section3-figure2.py

echo "Running tests under Temperature-Power-Variations"
cd ../Temperature-Power-Variations
python plot-section3-figure3.py

echo "Running tests under Temperature-Overheating"
cd ../Temperature-Overheating
python plot-section3-figure4.py
python plot-section3-figure5.py
python plot-section3-figure6.py

echo "Running tests under Temperature-HeatingRate"
cd ../Temperature-HeatingRate
bash process.sh

echo "Running tests under Temperature-DaylightEclipse"
cd ../Temperature-DaylightEclipse
python plot-section3-figure7.py
python plot-section3-figure8.py
python plot-section3-figure9.py

echo "Running tests under Energy-Overview"
cd ../Energy-Overview
python plot-section4-figure10.py

echo "Running tests under Energy-ShortTerm"
cd ../Energy-ShortTerm
python plot-section4-figure11.py

echo "Running tests under Energy-LongTerm"
cd ../Energy-LongTerm
python plot-section4-figure12n13.py longest
python plot-section4-figure12n13.py common

echo "Running tests under Energy-Available"
cd ../Energy-Available
python plot-section4-figure14.py longest

echo "Running tests under Energy-Efficiency"
cd ../Energy-Efficiency
bash process.sh