#!/usr/bin/python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# Set Input Path
pi_dir1 = 'Data/gnd_pi_stress_and_infer'
pi_dir2 = 'Data/sat_pi_stress_and_infer'
atlas_dir1 = 'Data/gnd_atlas_infer'
atlas_dir2 = 'Data/sat_atlas_infer'
processed_data_path = "Processed-Data"

# Figure Config
plt.rc('font', size=12)          # controls default text sizes
fig, axs = plt.subplots(3, 4, figsize=(17,8))

# Directories
def plot_data_atlas(directory1, directory2):
# File Pairs
    files = [
    ('atlas_infer_low_od1.csv', 'EX2_200B_Sun_LOW_1T_180.csv'),
    ('atlas_infer_mid_od1.csv', 'EX2_200B_Sun_MIDDLE_1T_180.csv'),
    ('atlas_infer_high_od1.csv', 'EX2_200B_Sun_HIGH_1T_180.csv'),
    ('atlas_infer_full_od1.csv', 'EX2_200B_Sun_FULL_1T_180.csv'),
    ('atlas_infer_low_od3.csv', 'EX2_200B_Sun_LOW_4T_180.csv'),
    ('atlas_infer_mid_od3.csv', 'EX2_200B_Sun_MIDDLE_4T_180.csv'),
    ('atlas_infer_high_od3.csv', 'EX2_200B_Sun_HIGH_4T_180.csv'),
    ('atlas_infer_full_od3.csv', 'EX2_200B_Sun_FULL_4T_180.csv')
    ]

    # Your custom labels
    labels = [
        'Low_1Thread',
        'Mid_1Thread',
        'High_1Thread',
        'Full_1Thread',
        'Low_4Thread',
        'Mid_4Thread',
        'High_4Thread',
        'Full_4Thread'
    ]
    for i, file_pair in enumerate(files):
        row = i // 4
        col = i % 4
        ax2 = axs[row+1,col].twinx()
        df = 1

        for j, file in enumerate(file_pair):
            if j == 0:
                directory = directory1
                filepath = os.path.join(directory, file)
                df = pd.read_csv(filepath)
                while True:
                    if df.empty or df.iloc[0]['INDEX'] != -1:
                        break
                    df = df.iloc[1:]
                df['TIME'] = (df['TIME'] - df['TIME'].min()) / 60  # convert TIME to mins
                df = df[df['TIME'] < 270]

                label1 = 'Ground Chip Temperature'
                window_size = 100
                # Apply rolling mean to 'TIME' and 'TEMP'
                df['TIME'] = df['TIME'].rolling(window=window_size).mean()
                df['TEMP'] = df['TEMP'].rolling(window=window_size).mean()
                # Drop rows with NaN values resulting from the rolling mean operation
                
                label2 = 'Ground Power'
                df['Main(mA)'] = df['Main(mA)'].rolling(window=window_size).mean()
                df['POWER'] = df['Main(mA)'] /1000 * 12  # calculate power
                df = df.dropna()

                # Process Data
                df[['TIME','POWER','TEMP']].to_csv(processed_data_path+'/'+'atlas_ground'+str(row+2)+'_'+str(col+1)+'.csv', index=False)
                if(col==0 and row==0):
                    axs[row+1, col].plot(df['TIME'], df['TEMP'], label=label1,color='orange', linestyle='-.',linewidth=2.5)
                    ax2.plot(df['TIME'], df['POWER'],label=label2,color='green')
                else:
                    axs[row+1, col].plot(df['TIME'], df['TEMP'],color='orange', linestyle='-.',linewidth=2.5)
                    ax2.plot(df['TIME'], df['POWER'],color='green')
                
            else:
                directory = directory2
                filepath = os.path.join(directory, file)
                df = pd.read_csv(filepath)
                while True:
                    if df.empty or df.iloc[0]['INDEX'] != -1:
                        break
                    df = df.iloc[1:]
                df['TIME'] = (df['TIME'] - df['TIME'].min()) / 60  # convert TIME to mins
                df = df[df['TIME'] < 270]

                window_size = 100
                label1 = 'Satellite Chip Tempurature'
                label2 = 'Satellite Surface Tempurature'
                df['TIME'] = df['TIME'].rolling(window=window_size).mean()
                df['TEMP'] = df['TEMP'].rolling(window=window_size).mean()
                df.loc[df['ATLAS_B_TEMP'] == 0, 'ATLAS_B_TEMP'] = np.nan
                df.dropna(subset=['ATLAS_B_TEMP'], inplace=True)
                
                label3 = 'Satellite Power'
                df['I_Atlas200DK-B'] = df['I_Atlas200DK-B'].rolling(window=window_size).mean()
                df['POWER'] = df['I_Atlas200DK-B'] /1000 * 12.1  # calculate power
                df = df.dropna()
                # Process Data
                df[['TIME','POWER','TEMP','ATLAS_B_TEMP']].to_csv(processed_data_path+'/'+'atlas_satellite'+str(row+2)+'_'+str(col+1)+'.csv', index=False)
                if(col==0 and row==0):
                    axs[row+1,col].plot(df['TIME'], df['TEMP'], label=label1,color='red', linestyle='-.',linewidth=2.5)
                    axs[row+1,col].plot(df['TIME'], df['ATLAS_B_TEMP'], label=label2,color='hotpink', linestyle='-.',linewidth=2.5)
                    ax2.plot(df['TIME'], df['POWER'],label=label3,color='blue')
                else:
                    axs[row+1,col].plot(df['TIME'], df['TEMP'],color='red', linestyle='-.',linewidth=2.5)
                    axs[row+1,col].plot(df['TIME'], df['ATLAS_B_TEMP'],color='hotpink', linestyle='-.',linewidth=2.5)
                    ax2.plot(df['TIME'], df['POWER'],color='blue')

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
                for area in shadow_areas:
                    axs[row+1,col].axvspan(df['TIME'].iloc[area[0]], df['TIME'].iloc[area[1]-1], alpha=0.3, color='gray')

        if(row+1==2):
            axs[row+1, col].set_xlabel('Time (min)', fontsize=12)

        axs[row+1, 0].set_ylabel('Temperature(℃)', fontsize=12)
        if(col==3):
            ax2.set_ylabel('Power (w)', fontsize=12)
        axs[row+1, col].set_ylim(0, 70)  # set y-axis limit here
        ax2.set_ylim(0, 14)  # set y-axis limit here
        axs[row+1,col].set_title('('+chr(97+(row+1)*4+col)+') '+labels[i])

# Directories
def plot_pi_data(directory1, directory2):
# File Pairs
    files = [
        ('pi_stress_lv1_5.5V.csv', 'EX2_PiA_Sun_1C_StressTest_180.csv'),
        ('pi_stress_lv2_5.5V.csv', 'EX2_PiA_Sun_2C_StressTest_180.csv'),
        ('pi_stress_lv3_5.5V.csv', 'EX2_PiA_Sun_3C_StressTest_180.csv'),
        ('pi_stress_lv4_5.5V.csv', 'EX2_PiA_Sun_4C_StressTest_180.csv')
    ]

    for i, file_pair in enumerate(files):
        col = i
        ax2 = axs[0,col].twinx()
        for j, file in enumerate(file_pair):

            if j == 0:
                filepath = os.path.join(directory1, file)
                df = pd.read_csv(filepath)
                label = 'Ground Chip Tempurature'
                label2 = 'Ground Power'
                df['TIME'] = (df['TIME'] - df['TIME'].min()) / 60  # convert TIME to mins
                df = df[df['TIME'] < 270]
                window_size = 100
                # Apply rolling mean to 'TIME' and 'TEMP'
                df['POWER'] = df['Main(mA)'] /1000 * 5.5 
                df['TIME'] = df['TIME'].rolling(window=window_size).mean()
                df['TEMP'] = df['TEMP'].rolling(window=window_size).mean()
                df['POWER'] = df['POWER'].rolling(window=window_size).mean()
                # Drop rows with NaN values resulting from the rolling mean operation
                df = df.dropna()

                 # Process Data
                df[['TIME','POWER','TEMP']].to_csv(processed_data_path+'/'+'pi_ground'+'1_'+str(col+1)+'.csv', index=False)
                if col==0:
                    axs[0,col].plot(df['TIME'], df['TEMP'], color='orange', linestyle='-.',linewidth=2.5)
                    ax2.plot(df['TIME'], df['POWER'],color='green')
                else:
                    axs[0,col].plot(df['TIME'], df['TEMP'],color='orange', linestyle='-.',linewidth=2.5)
                    ax2.plot(df['TIME'], df['POWER'],color='green')
            else:
                filepath = os.path.join(directory2, file)
                df = pd.read_csv(filepath)
                label1 = 'Satellite Chip Tempurature'
                label2 = 'Satellite Surface Tempurature'
                label3 = 'Satellite Power'
                df=df[90:]
                df['TIME'] = (df['TIME'] - df['TIME'].min()) / 60  # convert TIME to mins
                df = df[df['TIME'] < 270]
                df['POWER'] = df['I_Pi-A'] /1000 * 5.1
                window_size = 100
                df['TIME'] = df['TIME'].rolling(window=window_size).mean()
                df['TEMP'] = df['TEMP'].rolling(window=window_size).mean()
                df['POWER'] = df['POWER'].rolling(window=window_size).mean()
                df.loc[df['PI_A_TEMP'] == 0, 'PI_A_TEMP'] = np.nan
                df.dropna(subset=['PI_A_TEMP'], inplace=True)
                # Drop rows with NaN values resulting from the rolling mean operation
                df = df.dropna()

                 # Process Data
                df[['TIME','POWER','TEMP','PI_A_TEMP']].to_csv(processed_data_path+'/'+'pi_satellite'+'1_'+str(col+1)+'.csv', index=False)
                if col == 0:
                    axs[0, col].plot(df['TIME'], df['TEMP'], color='red', linestyle='-.')
                    axs[0, col].plot(df['TIME'], df['PI_A_TEMP'], color='hotpink', linestyle='-.',linewidth=2.5)
                    ax2.plot(df['TIME'], df['POWER'], color='blue')
                else:
                    axs[0, col].plot(df['TIME'], df['TEMP'], color='red', linestyle='-.')
                    axs[0, col].plot(df['TIME'], df['PI_A_TEMP'], color='hotpink', linestyle='-.',linewidth=2.5)
                    ax2.plot(df['TIME'], df['POWER'], color='blue')
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
                if(col==3):
                    shadow_areas[0] = (shadow_areas[0][1]-30*32, shadow_areas[0][1])
                for area in shadow_areas:
                    axs[0,col].axvspan(df['TIME'].iloc[area[0]], df['TIME'].iloc[area[1]-1], alpha=0.3, color='gray')

        if col==0:
            axs[0,col].set_ylabel('Temperature(℃)')
        if(col==3):
            ax2.set_ylabel('Power (w)', fontsize=12)
        axs[0,col].set_ylim(0, 90)  # set y-axis limit here
        ax2.set_ylim(0, 8)  # set y-axis limit here
        axs[0,col].set_title('('+chr(97+col)+') '+'Level '+str(i+1))

plot_pi_data(pi_dir1, pi_dir2)
plot_data_atlas(atlas_dir1, atlas_dir2)
plt.tight_layout()
plt.subplots_adjust(right=0.78)
legend=fig.legend(loc='lower right',frameon=True,bbox_to_anchor=(1, 0.06)) # bbox_to_anchor=(1, 0.5),
for line in legend.get_lines():
    line.set_linewidth(2.5)

from matplotlib.lines import Line2D
l = Line2D([0,1], [0.67,0.675], transform=fig.transFigure, ls='-', lw=2, c='k')
fig.add_artist(l)
l = Line2D([0,1,1,0,0], [0,0,1,1,0], transform=fig.transFigure, ls='-', lw=2, c='k')
fig.add_artist(l)

fig.text(0.83, 0.8, 'Raspberry Pi 4B\n  Experiments',fontdict = {'weight': 'bold','size':20})
fig.text(0.84, 0.52, 'Atlas 200 DK\nExperiments',fontdict = {'weight': 'bold','size':20})
fig.text(0.855, 0.243, 'Indicator Type',fontsize=16)
fig.text(0.855, 0.42, 'Orbital Phase',fontsize=16)

from matplotlib.patches import Patch

legend_elements = [
    Patch(facecolor='white', label='Daylight', edgecolor='black', linewidth=1),
    Patch(facecolor='Gainsboro', label='Eclipse', edgecolor='black', linewidth=1)
]
fig.legend(handles=legend_elements, bbox_to_anchor=(0.95, 0.42),handlelength=4.0, handleheight=2.)

# Output Data
outputdir='.'
plt.savefig(outputdir+"/figure3" + '.pdf', dpi=1000)
# plt.show()