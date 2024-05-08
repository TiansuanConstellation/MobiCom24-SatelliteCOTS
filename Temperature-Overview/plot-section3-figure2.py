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
path = '../CommonData-Telemetries/telemetry_all.csv'
df = pd.read_csv(path)

# Figure Config
plt.rcParams['font.size'] = 19
fig, axs = plt.subplots(2,1,figsize=(13, 8))

def plot_temp_in2days(begin_index, end_index,df,ax):
    df = df[begin_index: end_index]
    df['TIME'] = pd.to_datetime(df['Time']).apply(lambda x: int(pd.Timestamp.timestamp(x)))

    df=df[(1683244800<=df['TIME'])&(df['TIME']<=1683244800+60*60*48)]
    df = df.reset_index(drop=True)
    df = df.dropna()
    
    # Find X range in Shadow Areas
    shadow_areas=[(35, 67), (130, 161), (223, 256), (317, 350), (412, 444), (506, 537), (600, 632), (694, 726), (789, 820), (883, 914), 
                  (976, 1009), (1071, 1103), (1165, 1197), (1259, 1291), (1353, 1385), (1448, 1479), (1542, 1573), (1635, 1668), (1729, 1762),
                    (1824, 1856), (1918, 1949), (2012, 2044), (2107, 2138), (2201, 2232), (2294, 2327), (2388, 2421), (2483, 2515), (2577, 2609), (2671, 2703), (2766, 2797), (2860, 2880)]

    rounds=[]
    for i, round in enumerate(shadow_areas):
        rounds.append(round[1])

    df['TIME'] = (df['TIME'] - df['TIME'].iloc[0])/60
    df['TIME'] = df['TIME'].astype(int)

    window_size = 60
    # Apply rolling mean to 'TIME' and 'TEMP'
    df['TIME'] = df['TIME'].rolling(window=window_size).mean()
    df['ATLAS_A_TEMP'] = df['ATLAS_A_TEMP'].replace(0, np.nan).fillna(method='ffill')
    df['ATLAS_B_TEMP'] = df['ATLAS_B_TEMP'].replace(0, np.nan).fillna(method='ffill')
    df['PI_A_TEMP'] = df['PI_A_TEMP'].replace(0, np.nan).fillna(method='ffill')

    for area in shadow_areas:
        ax.axvspan(area[0], area[1], alpha=0.3, color='gray')

    ax.plot(df['TIME'], df['PI_A_TEMP'], label='Pi-A Tempurature',color='DarkOrange')
    ax.plot(df['TIME'], df['ATLAS_A_TEMP'], label='Atlas-A Tempurature',color='red')
    ax.plot(df['TIME'], df['ATLAS_B_TEMP'], label='Atlas-B Tempurature',color='green')

    ax.set_xticks(rounds)
    tick_label=list(range(0, len(rounds)))
    filtered_tick_label = [label if i % 5 == 0 else '' for i, label in enumerate(tick_label)]
    filtered_tick_label = np.array(filtered_tick_label)
    ax.set_xticklabels(filtered_tick_label)

    # add legends and labels
    ax.set_title('(a) Temperature Varations in 2 Days with Computing Tasks',y=1.05)
    ax.set_xlabel("Orbital Period Number", fontsize=20)
    ax.set_ylabel("Temperature(°C)", fontsize=20)

def plot_temp_in10hs(begin_index, offset,df,ax):
    df = df[begin_index:begin_index+offset]
    df = df[(df['POBC_I_5V'] == 0) &
        (df['XMIT_A_12V'] == 0) &
        (df['XMIT_B_12V'] == 0) &
        (df['I_Atlas200DK-A'] == 0) &
        (df['I_Atlas200DK-B'] == 0) &
        (df['I_Pi-A'] == 0) &
        (df['I_Pi-B']==0)]
    df['TIME'] = pd.to_datetime(df['Time']).apply(lambda x: int(pd.Timestamp.timestamp(x)))

    df=df[(1685967037<=df['TIME'])&(df['TIME']<=1686004009)]
    df = df.reset_index(drop=True)

    df = df.dropna()
    shadow_areas=[(27.3, 58.8), (121.35, 152.9), (215.45, 247.0), (309.5, 341.05), (403.55, 435.15), (497.65, 529.25), (591.75, 616.2)]

    df['TIME'] = (df['TIME'] - df['TIME'].iloc[0])/60
    df['ATLAS_A_TEMP'] = df['ATLAS_A_TEMP'].replace(0, np.nan).fillna(method='ffill')
    df['ATLAS_B_TEMP'] = df['ATLAS_B_TEMP'].replace(0, np.nan).fillna(method='ffill')
    df['PI_A_TEMP'] = df['PI_A_TEMP'].replace(0, np.nan).fillna(method='ffill')
    window_size = 60
    df['TIME'] = df['TIME'].rolling(window=window_size).mean()

    for area in shadow_areas:
        ax.axvspan(area[0], area[1], alpha=0.3, color='gray')
    ax.plot(df['TIME'], df['PI_A_TEMP'],color='DarkOrange')
    ax.plot(df['TIME'], df['ATLAS_A_TEMP'],color='red')
    ax.plot(df['TIME'], df['ATLAS_B_TEMP'],color='green')

    rounds=[58.8,152.9,247.0, 341.05, 435.15, 529.25]
    ax.set_xticks(rounds)
    tick_label=list(range(1, len(rounds)+1))
    tick_label=np.array(tick_label)
    ax.set_xticklabels(tick_label)

    ax.set_xlabel("Orbital Period Number", fontsize=20.5)
    ax.set_ylabel("Temperature(°C)", fontsize=20.5)
    ax.set_title('(b) Temperature Varations in 9 Hours without Computing Tasks', y=1.05)


plot_temp_in2days(3722427,-1,df,axs[0])
plot_temp_in10hs(0,-1,df,axs[1])

plt.tight_layout()
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='white', label='Daylight', edgecolor='black', linewidth=0.5),
    Patch(facecolor='Gainsboro', label='Eclipse', edgecolor='black', linewidth=0.5)
]

plt.subplots_adjust(top=0.86)

legend=fig.legend(loc='upper center',bbox_to_anchor=(0.5, 1),frameon=False,ncol=4,fontsize=19) # bbox_to_anchor=(1, 0.5),

for line in legend.get_lines():
    line.set_linewidth(2.5)
axs[0].legend(handles=legend_elements,frameon=False,loc='upper left')
plt.subplots_adjust(hspace=0.5)

# Output Data
outputdir="."
plt.savefig(outputdir+"/figure2" + '.pdf', dpi=1000)
# plt.show()

