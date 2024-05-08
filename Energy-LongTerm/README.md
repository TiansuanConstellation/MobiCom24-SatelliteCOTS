# Energy ShortTerm

This folder contains details of the artifacts related to Section 4 (Energy Results). We provide details of the dataset, analysis scripts as well as plotting scripts to generate Figure 12 and 13.

## Folder structure
| Foldername/Filename                               | Description                                                                |
| ------------------------------------------------- | -------------------------------------------------------------------------- |
| Data/common_rounds_energy_df.csv  | The collected CSV dataset of the rounds within a same time range of a day. |
| Data/longest_rounds_energy_df.csv | The collected CSV dataset of longest continuous rounds.                    |
| plot-section4-figure12n13.py      | Scripts for generating figure 12 and 13.                                    |

---

## Dataset Description

The dataset file `telemetry_all.csv` contains several fields. We provide description for each field below.

| Field name               | Description of the field                 |
| ------------------------ | ---------------------------------------- |
| `round_start`            | Timestamp of the round start             |
| `round_end`              | Timestamp of the round end               |
| `total_energy`           | Total consumed energy（Wh）              |
| `solar_harvested_energy` | Collected solar energy（Wh）             |
| `comm_energy`            | Communications consumed energy (Wh)      |
| `payload_energy`         | Payload Computing consumed energy (Wh)   |
| `other_energy`           | Energy consumed by other components (mA) |

## Requirements

* Python (>=3.6)
* Numpy (>=1.19.5)
* Matplotlib (>=3.1.3)
* Numpy (>=1.19.5)

---

## Generating Plots

Use the following bash command to generate results/plots

```bash
python3 plot-section4-figure12n13.py longest
python3 plot-section4-figure12n13.py common
```
The generated results will be saved in the `Energy-LongTerm` folder.
