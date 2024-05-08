#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "battery_curve")
from processing import get_discharge_curve
from scipy import interpolate

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# Set Input Path
longest_rounds_path = 'Data/longest_rounds_energy_df.csv'
telemetry_path = '../CommonData-Telemetries/telemetry_all.csv'

# Figure Config
plt.rcParams.update({'font.size': 16})

# Load data
df1 = pd.read_csv(longest_rounds_path, parse_dates=['round_start', 'round_end'])
df2 = pd.read_csv(telemetry_path, parse_dates=['Time'])

# Determine earliest and latest times
start_time = df1['round_start'].min()
end_time = df1['round_end'].max()

# Select entries in df2 that fall within this time range
mask = (df2['Time'] >= start_time) & (df2['Time'] <= end_time)
df2 = df2.loc[mask]

# Calculate battery left energy
voltage, battery_percentage = get_discharge_curve()  # Assuming this function returns two lists: voltage and corresponding battery percentage
f = interpolate.interp1d(voltage, battery_percentage)
df2['battery_DOD'] = (f(df2['BATTERY1_U']/1000) + f(df2['BATTERY2_U']/1000))/2

# Make time relative to the start time and convert it to days
df2['Relative_Time'] = (df2['Time'] - start_time).dt.total_seconds() / 86400

# Calculate available_energy
df1['available_energy'] = (df1['solar_harvested_energy'] * 1.1 - df1['total_energy'] * 0.9)

# Calculate the length of each round in days
df1['round_length'] = (df1['round_end'] - df1['round_start']).dt.total_seconds() / 86400

# Calculate the cumulative sum of round lengths to get the end time of each round in days from the start
df1['round_end_days'] = df1['round_length'].cumsum()

# Filter df1 based on the condition where 'available_energy' is greater than 0
df1_filtered = df1[df1['available_energy'] > 0]

# Iterate through the filtered df1 and calculate the sum of 'available_energy' where 'battery_DOD' is greater than 90% in the corresponding time range
total_available_energy = 0
for index, row in df1_filtered.iterrows():
    start_time = row['round_start']
    end_time = row['round_end']
    mask = (df2['Time'] >= start_time) & (df2['Time'] <= end_time) & (df2['battery_DOD'] < 10)
    if df2[mask].shape[0] > 0:
        total_available_energy += row['available_energy']

# Calculate the total 'solar_harvested_energy' in df1
total_solar_harvested_energy = df1['solar_harvested_energy'].sum()

# Calculate the ratio
ratio = total_available_energy / total_solar_harvested_energy

# Print the results
# print("Total available energy when battery left is greater than 90%:", total_available_energy)
# print("Total solar harvested energy:", total_solar_harvested_energy)
# print("Ratio:", ratio)

# Create a new figure and axes
fig, ax1 = plt.subplots(figsize=(10, 6))

# Make the first plot on ax1
color = 'darkgreen'
ax1.set_xlabel('Time (days)')
ax1.set_ylabel('Available Energy (Wh)')
ax1.set_ylim([-30, 70])
ax1.axhline(0, color='red', linestyle='--')
ax1.plot(df1['round_end_days'], df1['available_energy'], color=color, label='Available Energy')
ax1.tick_params(axis='y')

# Create a second axes that shares the same x-axis
ax2 = ax1.twinx()
ax2.set_ylim([100, 0])
color = 'darkblue'
ax2.set_ylabel('Depth of Discharge (%)')
ax2.plot(df2['Relative_Time'], df2['battery_DOD'], color=color, label='Depth of Discharge')
ax2.tick_params(axis='y')

# Here's the line that adds the horizontal line at 70%
ax2.axhline(30, color='red', linestyle='--')
fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.025), ncol=2, frameon=False)
fig.tight_layout()

# Output Data
outputdir='.'
plt.savefig(outputdir+"/figure14" + '.pdf', dpi=1000)
# plt.show()