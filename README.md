## Datasets on Satellite Computing with COTS Devices

In this repository, we release the dataset and tools in MobiCom '24 paper, [*Deciphering the Enigma of Satellite Computing with COTS Devices: Measurement and Analysis*](https://arxiv.org/abs/2401.03435). 
Amidst the rapid growth of low-Earth orbit constellations, utilizing COTS computing devices as in-orbit computing units offers significant advantages: low cost, high performance, and reusability of software and hardware ecosystems. This paper aims to explore how to better utilize computational resources in orbit, considering the constraints of temperature and power consumption on satellite platforms.

The dataset from this paper is derived from the [BUPT-1](http://www.tiansuan.org.cn/sate-b1.html) satellite, the flagship 12U CubeSat of the [TianSuan Constellation](http://www.tiansuan.org.cn/index.html) project. BUPT-1 equipped with popular COTS computing payloads including Atlas 200 DK and Raspberry Pi 4B, primarily for satellite computing research. 

### Dataset Structure
The data can be categorized into **platform data** (sensor-acquired telemetry data within the satellite) and **payload data** (generated from COTS computing payloads during computational tasks). 

The repository is structured around experimental types mentioned in the paper, with folders dedicated to temperature control and energy management. There are five folders for temperature control: `Temperature-Overview`, `Temperature-Power-Variations`, `Temperature-Overheating`, `Temperature-HeatingRate`, and `Temperature-DaylightEclipse`. For energy management, the folders are: `Energy-Overview`, `Energy-ShortTerm`, `Energy-LongTerm`, `Energy-Available`, and `Energy-Efficiency`. Each folder contains a README providing detailed explanations. 

Source code for data processing and plotting, along with the datasets used in the experiments, are contained within each folder.
We included the dataset file under the `Data` folder for all experiments.
All telemetry data collected during the experiment is compiled into a table and placed in the `CommonData-Telemetries` folder for convenience.

### Installation Instructions



### Usage Instructions

Before you start, you may use these commands to install the Python environment required:
```bash
# Makesure $PWD is the root directory of the repo
# Replace "your_env_name" at your ease
conda create -n your_env_name python=3.9.11
conda activate your_env_name
pip3 install numpy pandas scipy matplotlib
```

Additionally, you should uncompress the dataset file：
- You must use `cd` navigate to sub-directories in order to run the code.
- Before running code, you must navigate to `CommonData-Telemetries` folder to `unzip` the "telemetry_all.csv.zip".

After that, you can run all the scripts in once using `run_all.sh`:

```bash
bash run_all.sh
```

It would produce all the `.pdf` and `.log` results, you may use this command to inspect:

```bash
find . -type f \( -name "*.pdf" -o -name "*.log" \)
```
And the correct results are like:

```text
./Temperature-HeatingRate/sat_pi.log
./Temperature-HeatingRate/gnd_atlas.log
./Temperature-HeatingRate/sat_atlas.log
./Temperature-HeatingRate/gnd_pi.log
./Energy-Available/figure14.pdf
./Temperature-Overview/figure2.pdf
./Temperature-DaylightEclipse/figure8.pdf
./Temperature-DaylightEclipse/figure9.pdf
./Temperature-DaylightEclipse/figure7.pdf
./Energy-ShortTerm/figure11.pdf
./Energy-Overview/figure10.pdf
./Energy-LongTerm/figure13.pdf
./Energy-LongTerm/figure12.pdf
./Energy-Efficiency/sat_pi.log
./Energy-Efficiency/gnd_sat_atlas_cl_dp.log
./Energy-Efficiency/gnd_atlas.log
./Energy-Efficiency/sat_atlas.log
./Energy-Efficiency/gnd_pi.log
./Temperature-Overheating/figure6.pdf
./Temperature-Overheating/figure4.pdf
./Temperature-Overheating/figure5.pdf
./Temperature-Power-Variations/figure3.pdf
```
We also provide a cleaning scripts to delete all the generated results.
Simply run the commands like:

```bash
bash clear all.sh
```

---

### Paper Structure to Folder Structure

|           Content in Paper           |                       Folder in Repo.                        | Description                                                                                  |
| :----------------------------------: | :----------------------------------------------------------: | -------------------------------------------------------------------------------------------- |
|         Figure 2 (Section 3)         |         [Temperature-Overview](Temperature-Overview)         | Surface Temperature Varitions with or without Computing Tasks.                                               |
|       Figure 3  (Section 3.1)        | [Temperature-Power-Variations](Temperature-Power-Variations) | Temperature and Power Varitions under different CPU/NPU/Power Level Settings.      |
|     Figure 4 to 6  (Section 3.2)     |      [Temperature-Overheating](Temperature-Overheating)      | Overheating Effects on Atlas and Pi. |
|        Table 3 (Section 3.3)         |      [Temperature-HeatingRate](Temperature-HeatingRate)      | Relations of Power and Heating Rate. |
|     Figures 7 to 9 (Section 3.4)     |  [Temperature-DaylightEclipse](Temperature-DaylightEclipse)  | Impact of Daylight and Eclipse Zones on Temperature  |
|        Figures 10 (Section 4)        |              [Energy-Overview](Energy-Overview)              | Solar/Consumed Power Varitions with or without Computing Tasks.  |
|    Figures 11 (Section 4.1, 4.2)     |             [Energy-ShortTerm](Energy-ShortTerm)             | Typical Solar/Consumed Power Varitions within an Orbiting Period (about 90 mins). |
| Figures 12 and 13 (Section 4.1, 4.2) |              [Energy-LongTerm](Energy-LongTerm)              |  Solar/Consumed Energy Varitions within 2 weeks.   |
|       Figures 14 (Section 4.2)       |             [Energy-Available](Energy-Available)             | Solar/Consumed Energy Varitions on Identical Time Range.   |
|     Table 4 and 5 (Section 4.3)      |            [Energy-Efficiency](Energy-Efficiency)            | Explore the underutilization of solar energy and the excessive use of battery power.   |

---

### Measurement tools

In the terrestrial tests, we use Monsoon Power Monitor to record the current.

### Support

If there are any questions, feel free to reach out to us (<xrl@bupt.edu.cn>)! 
