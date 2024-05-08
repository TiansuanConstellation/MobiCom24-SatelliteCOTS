# Temperature Overheating

This folder contains details of the artifacts related to Section 3.2 (Overheating). We provide details of the dataset, analysis scripts as well as plotting scripts to generate Figures 4, 5, 6.

## Folder structure
| Foldername/Filename                 | Description                                                 |
| ----------------------------------- | ----------------------------------------------------------- |
| Data/extreme_temperature_test/[csv] | The collected CSV dataset of extreme temperature test       |
| Data/gnd_atlas_infer/[csv]          | The collected CSV dataset of Atlas experiment on the ground |
| Data/pi_sun_infer/[csv]             | The collected CSV dataset of Pi experiment                  |
| Data/sat_atlas_infer/[csv]          | The collected CSV dataset of Atlas experiment on satellite  |
| plot-section3-figure4.py            | Scripts for generating figure4                              |
| plot-section3-figure5.py            | Scripts for generating figure5                              |
| plot-section3-figure6.py            | Scripts for generating figure6                              |

---

## Dataset Description

The dataset file `telemetry_all.csv` contains several fields. We provide description for each field below.

| Field name       | Description of the field                      |
| ---------------- | --------------------------------------------- |
| `TIME`           | Timestamp of the test                         |
| `MPPT1_Uin`      | Input voltage of the first solar panel（mV）  |
| `MPPT1_Iin`      | Input current of the first solar panel（mA）  |
| `MPPT2_Uin`      | Input voltage of the second solar panel（mV） |
| `MPPT2_Iin`      | Input current of the second solar panel（mA） |
| `I_Atlas200DK-A` | Current of Atlas200DK-A (mA)                  |
| `I_Atlas200DK-B` | Current of Atlas200DK-B (mA)                  |
| `ATLAS_A_TEMP`   | ATLAS_A surface temperature                   |
| `ATLAS_B_TEMP`   | ATLAS_B surface temperature                   |
| `FREQUENCY(48)`  | The CPU frequency                             |

The dataset files `xxx.json` contain several fields. We provide description for each field below.

| `TEMP`         |                                       |
| -------------- | ------------------------------------- |
| `start_time`   | The start time                        |
| `execute_time` | The time taken for execution(ms)      |
| `infer_time`   | The time taken for this inference(ms) |


## Requirements

* Python (>=3.6)
* Numpy (>=1.19.5)
* Matplotlib (>=3.1.3)
* Numpy (>=1.19.5)

---

## Generating Plots

Use the following bash command to generate results/plots

```bash
python3 plot-section3-figure4.py
python3 plot-section3-figure5.py
python3 plot-section3-figure6.py
```
The generated results will be saved in the `Temperature-Overheating` folder.
