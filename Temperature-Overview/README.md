# Temperature Overview

This folder contains details of the artifacts related to Section 3 (Temperature Results). We provide details of the dataset, analysis scripts as well as plotting scripts to generate Figures 2.

## Folder structure

| Foldername/Filename      | Description                       |
| ------------------------ | --------------------------------- |
| plot-section3-figure2.py | The script to generate plots      |
| figure2.pdf              | The plot generated by the scripts |

---

## Dataset Description

The following is the field description in `telemetry_all.csv` in the `CommonData-Telemetries` folder used by the plot script.

| Field name   | Description of the field    |
| ------------ | --------------------------- |
| TIME         | Timestamp of the experiment |
| ATLAS_A_TEMP | ATLAS_A surface temperature |
| ATLAS_B_TEMP | ATLAS_B surface temperature |
| PI_A_TEMP    | PI_A surface temperature    |

---

## Requirements

* Python (>=3.6)
* Numpy (>=1.19.5)
* Matplotlib (>=3.1.3)
* Pandas (>=2.2.1)

---

## Generating Plots

Once `telemetry_all.csv`  in the `CommonData-Telemetries` folder is ready, use the following bash command to generate plots

```bash
python3 plot-section3-figure2.py
```

The generated results will be saved in the `Temperature-Overview` folder.