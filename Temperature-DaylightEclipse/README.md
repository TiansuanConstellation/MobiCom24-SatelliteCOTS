# Temperature Overview

This folder contains details of the artifacts related to Section 3 (Temperature Results). We provide details of the dataset, analysis scripts as well as plotting scripts to generate Figures 7、8、9.

## Folder structure
| Foldername/Filename      | Description                      |
| ------------------------ | -------------------------------- |
| Data                     | Processed data can be found here |
| plot-section3-figure7.py | The script to generate figure7   |
| plot-section3-figure8.py | The script to generate figure8   |
| plot-section3-figure9.py | The script to generate figure9   |

---


## Dataset Description

The dataset files `*.csv` contain several fields. We provide description for each field below.

| Field name       | Description of the field                      |
| ---------------- | --------------------------------------------- |
| `TIME`           | Timestamp of the test                         |
| `I_Pi-A`         | Current of Pi4B-A (mA)                        |
| `I_Atlas200DK-B` | Current of Atlas200DK-B (mA)                  |
| `TEMP`           | Surface Temperature of payload (°C)           |
| `PI_A_TEMP`      | Chip Temperature of Pi4B-A (°C)               |
| `ATLAS_B_TEMP`   | Chip Temperature of Atlas200DK-B(°C)          |
| `MPPT1_Vin`      | Input voltage of the first solar panel（mV）  |
| `MPPT1_Ain`      | Input current of the first solar panel（mA）  |
| `MPPT2_Vin`      | Input voltage of the second solar panel（mV） |
| `MPPT2_Ain`      | Input current of the second solar panel（mA） |
| `INDEX`          | The index of test result                      |

The dataset files `*.json` contain several fields. We provide description for each field below.

| Field name                            | Description of the field               |
| ------------------------------------- | -------------------------------------- |
| `infer_time`                          |
| The time taken for this inference(ms) |
| `execute_time`                        | The time taken for this inference (ms) |
| `success_list`                        | Signs of success in inference subtask  |

## Requirements

* Python (>=3.6)
* Numpy (>=1.19.5)
* Matplotlib (>=3.1.3)
* pandas (>=2.2.1)

---

## Generating Plots
Use the following bash command to generate results/plots

```bash
python3 plot-section3-figure7.py
python3 plot-section3-figure8.py
python3 plot-section3-figure9.py
```
The generated results will be saved in the `Temperature-DaylightEclipse` folder.
