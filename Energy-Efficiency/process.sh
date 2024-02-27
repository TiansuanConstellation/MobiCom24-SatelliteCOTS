#!/usr/bin/bash

python gnd_atlas.py             > gnd_atlas.log
python gnd_pi.py                > gnd_pi.log
python sat_atlas.py             > sat_atlas.log
python sat_pi.py                > sat_pi.log
python gnd_sat_atlas_cl_dp.py   > gnd_sat_atlas_cl_dp.log