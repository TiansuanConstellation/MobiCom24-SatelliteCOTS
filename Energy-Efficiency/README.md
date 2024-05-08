# Temperature HeatingRate

This folder contains details of the artifacts related to Section 4.3 (Computational Energy Efficiency). We provide details of the dataset, and analysis scripts to generate Table 4 and 5.

## Folder structure
| Foldername/Filename                | Description                                                                                                      |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Data/gnd_atlas_infer/[csv]         | The collected CSV dataset of Atlas inference on the ground                                                       |
| Data/sat_atlas_infer/[csv]         | The collected CSV dataset of Atlas inference on satellite                                                        |
| Data/gnd_pi_stress_and_infer/[csv] | The collected CSV dataset of Pi inference on the ground                                                          |
| Data/sat_pi_stress_and_infer/[csv] | The collected CSV dataset of Pi inference on satellite                                                           |
| Data/gnd_sat_atlas_cl_dp/[csv]     | The collected CSV dataset of Atlas data processing and classification inference on both satellite and the ground |
| gnd_atlas.py                       | Scripts for generating results of Atlas inference on the ground                                                  |
| sat_atlas.py                       | Scripts for generating results of Atlas inference on satellite                                                   |
| gnd_pi.py                          | Scripts for generating results of Pi inference on the ground                                                     |
| sat_pi.py                          | Scripts for generating results of Pi inference on satellite                                                      |
| gnd_sat_atlas_cl_dp.py             | Scripts for generating results of Pi inference on satellite                                                      |
| process.sh                         | Scripts for generating results                                                                                   |

---

## Dataset Description

The dataset csv files contain several fields. We provide description for each field below.

| Field name       | Description of the field            |
| ---------------- | ----------------------------------- |
| `TIME`           | Timestamp of the test               |
| `TEMP`           | Surface Temperature of payload (°C) |
| `I_Pi-A`         | Current of Pi4B-A (mA)              |
| `I_Atlas200DK-B` | Current of Atlas200DK-B (mA)        |
| `INDEX`          | The index of test result            |
| `Main(mA)`       | Input current                       |

## Requirements

* Python (>=3.6)
* Numpy (>=1.19.5)
* pandas (>=2.2.1)

---

## Generating results

Use the following bash command to generate results

```Rbash
bash process.sh
```
The generated results will be saved in the `Energy-Efficiency` folder.
