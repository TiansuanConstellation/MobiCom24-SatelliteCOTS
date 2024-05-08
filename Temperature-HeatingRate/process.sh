#!/usr/bin/bash

python3 gnd_atlas.py > gnd_atlas.log
python3 gnd_pi.py    > gnd_pi.log
python3 sat_atlas.py > sat_atlas.log
python3 sat_pi.py    > sat_pi.log