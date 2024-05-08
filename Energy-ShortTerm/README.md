# Energy ShortTerm

This folder contains details of the artifacts related to Section 4 (Energy Results). We provide details of the dataset, analysis scripts as well as plotting scripts to generate Figures 11.

## Folder structure
| Foldername/Filename                      | Description                                                   |
| ---------------------------------------- | ------------------------------------------------------------- |
| battery_curve           | The files needed to generate the battery characteristic curve |
| telemetries/all.csv     | The collected CSV dataset of telemetries.                     |
| telemetries/payload.csv | The collected CSV dataset of payload telemetries.             |
| plot-section3-figure11.py                | Scripts for generating figure11.                              |

---

## Dataset Description

The dataset file `telemetry_all.csv` contains several fields. We provide description for each field below.

| Field name       | Description of the field                      |
| ---------------- | --------------------------------------------- |
| `TIME`           | Timestamp of the test                         |
| `MPPT_Iout`      | Output current of the solar panel（mV）       |
| `UV_I`           | Current of the UV Band（mA）                  |
| `POBC_I_5V`      | Input voltage of the second solar panel（mV） |
| `XMIT_A_12V`     | Current of the baseband A (mA)                |
| `XMIT_B_12V`     | Current of the baseband B (mA)                |
| `I_Atlas200DK-B` | Current of Atlas200DK-B (mA)                  |
| `Battery_U`      | Battery Voltage（mV）                         |
| `Battery_I`      | Battery Current（mA）                         |

## Requirements

* Python (>=3.6)
* Numpy (>=1.19.5)
* Matplotlib (>=3.1.3)
* Numpy (>=1.19.5)

---

## Generating Plots

Use the following bash command to generate results/plots

```bash
python3 plot-section4-figure11.py
```
The generated results will be saved in the `Energy-ShortTerm` folder.
