#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

import warnings
warnings.filterwarnings("ignore")

# Set Input Path
dir = 'Data/extreme_temperature_test'
telemetry_temperature_path = dir + "/telemetry_temperature.csv"
telemetry_power_path = dir + '/telemetry_power.csv'
telemetry_solar_path = dir + '/telemetry_solar.csv'
test_data_path = dir + '/atlasAB_surtemp.csv'

# Figure Config
plt.rc('font', size=14)

def get_shadow_area(df):
    is_shadow = ((df['MPPT1_Uin'] == 0) & (df['MPPT1_Iin'] == 0) & (df['MPPT2_Uin'] == 0) & (df['MPPT2_Iin'] == 0))
    shadow_areas = []
    start_index = None
    for index, value in enumerate(is_shadow):
        if value and start_index is None:
            start_index = index
        elif not value and start_index is not None:
            end_index = index
            if end_index - start_index >= 100:
                shadow_areas.append((start_index, end_index))
            start_index = None
    if start_index is not None and len(df) - start_index >= 100:
        shadow_areas.append((start_index, len(df)))
    return shadow_areas

fig, ax = plt.subplots(figsize=(10,5)) #3.85
ax2=ax.twinx()

df = pd.read_csv(test_data_path)
df1 = pd.read_csv(telemetry_temperature_path)
df2 = pd.read_csv(telemetry_power_path)
df3 = pd.read_csv(telemetry_solar_path)

df=df[100:]
df.reset_index(drop=True, inplace=True)
df['TIME'] = (df['TIME'] - df['TIME'].min()) / 60  # convert TIME to mins

df['ATLAS_A_TEMP'] = df['ATLAS_A_TEMP'].replace(0, np.nan).fillna(method='ffill')
df['ATLAS_B_TEMP'] = df['ATLAS_B_TEMP'].replace(0, np.nan).fillna(method='ffill')
df['POWERA'] = df['I_Atlas200DK-A'] /1000 * 12.1 
df['POWERB'] = df['I_Atlas200DK-B'] /1000 * 12.1 
window_size=100
df['TIME'] = df['TIME'].rolling(window=window_size).mean()
df['POWERA'] = df['POWERA'].rolling(window=window_size).mean()
df['POWERB'] = df['POWERB'].rolling(window=window_size).mean()
ax.plot(df['TIME'], df['ATLAS_A_TEMP'],label='Atlas-A Temperature',color='deeppink',linestyle='-.')
ax.plot(df['TIME'], df['ATLAS_B_TEMP'],label='Atlas-B Temperature',color='darkOrange',linestyle='-.',linewidth=2.5)
ax2.plot(df['TIME'], df['POWERA'],label='Atlas-A Power',color='blue')
ax2.plot(df['TIME'], df['POWERB'],label='Atlas-B Power',color='green')

ax.set_xlabel('Time (min)')
ax.set_ylabel('Temperature (℃)')
ax2.set_ylabel('Power (w)')

offset1=40
offset2=18
ax.axhline(y=30, color='red',linestyle=':')
ax.axhline(y=30-offset1, color='red',linestyle=':')
df1['ATLAS_B_TEMP'] = df1['ATLAS_B_TEMP'].replace(0, np.nan).fillna(method='ffill')
df2['POWERB'] = df2['I_Atlas200DK-B'] /1000 * 12.1 
window_size=100

df2['TIME'] = df2['TIME'].rolling(window=25).mean()
df2['POWERB'] = df2['POWERB'].rolling(window=25).mean()

ax.plot(df1['TIME'], df1['ATLAS_B_TEMP']-offset1,color='darkOrange',linestyle='-.',linewidth=2.5)
ax2.plot(df2['TIME'], df2['POWERB']-offset2,color='green')
shadow_areas=get_shadow_area(df)
for area in shadow_areas:
    ax.axvspan(df['TIME'].iloc[area[0]], df['TIME'].iloc[area[1]-1],ymin=0.5, alpha=0.3, color='gray')

shadow_areas=get_shadow_area(df3)
for area in shadow_areas:
    ax.axvspan(df3['TIME'].iloc[area[0]], df3['TIME'].iloc[area[1]-1],ymax=0.5, alpha=0.3, color='gray')
ax.axhline(0, color='black')

ax.set_ylim(-offset1, offset1)  # set y-axis limit here
ax2.set_ylim(-offset2, offset2)  # set y-axis limit here

yticks1 = ax.get_yticks()
yticklabels1 = [t if t >= 0 else t + offset1 for t in yticks1]
ax.set_yticklabels(yticklabels1)

yticks2 = ax2.get_yticks()
yticklabels2 = [t if t >= 0 else t + offset2 for t in yticks2]
ax2.set_yticklabels(yticklabels2)

plt.tight_layout()
legend=fig.legend(loc='upper right',bbox_to_anchor=(0.85, 0.83),frameon=False,fontsize=13) # bbox_to_anchor=(1, 0.5),
for line in legend.get_lines():
    line.set_linewidth(2)
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='white', label='Daylight', edgecolor='black', linewidth=0.5),
    Patch(facecolor='Gainsboro', label='Eclipse', edgecolor='black', linewidth=0.5)
]
fig.legend(handles=legend_elements,frameon=False,loc='upper right',ncol=2,bbox_to_anchor=(0.9, 0.95))

ax.text(-22, 36, 'Double On',fontdict = {'weight': 'bold'})
ax.text(-22, -4, 'Single On',fontdict = {'weight': 'bold'})

# Output Data
outputdir='.'
plt.savefig(outputdir+"/figure6" + '.pdf', dpi=1000)
# plt.show()
