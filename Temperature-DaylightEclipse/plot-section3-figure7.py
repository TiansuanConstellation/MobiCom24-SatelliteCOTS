#!/usr/bin/python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

import warnings
warnings.filterwarnings("ignore")

# Set Input Path
directory_pi = 'Data/pi_infer_yolo'
directory_atlas = 'Data/atlas_sun_shadow'

# Figure Config
plt.rc('font', size=14)  # controls default text sizes

def process_df(filepath, payload):
    df = pd.read_csv(filepath)
    while True:
        if df.empty or df.iloc[0]['INDEX'] != -1:
            break
        df = df.iloc[1:]
    df.reset_index(drop=True, inplace=True)
    df['TIME'] = (df['TIME'] - df['TIME'].min()) / 60  # convert TIME to mins
    df = df[df['TIME'] < 60]
    window_size = 100
    if payload=='pi':
        df['POWER'] = df['I_Pi-A'] /1000 * 5.1
    if payload=='atlas':
        df['POWER'] = df['I_Atlas200DK-B'] /1000 * 12.1 
    df['TEMP'] = df['TEMP'].rolling(window=window_size).mean()
    df['POWER'] = df['POWER'].rolling(window=window_size).mean()
    if payload=='pi':
        df['PI_A_TEMP'] = df['PI_A_TEMP'].replace(0, np.nan).fillna(method='ffill')
    if payload=='atlas':
        df['ATLAS_B_TEMP'] = df['ATLAS_B_TEMP'].replace(0, np.nan).fillna(method='ffill')
    df = df.dropna()

    df.reset_index(drop=True, inplace=True)
    return df

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
        shadow_areas.append((len(df)-60*30, len(df)))    
    return shadow_areas

def plot_pi_data(directory):
    files = [
        ('EX4_PiA_Sun_Yolofastest_60.csv', 'EX2_PiA_Umbra_yolofastest_60.csv'),
        ('EX4_PiA_Sun_Yolov5lite_60.csv', 'EX2_PiA_Umbra_yolo-v5lite_60.csv'),
        ('EX4_PiA_Sun_Yolov354460_60.csv', 'EX2_PiA_Umbra_yolov3_544_60.csv'),
    ]
    titles=[
        'YOLO-Fastest','YOLOv3',' YOLOv5-Lite'
    ]
    for i, file_pair in enumerate(files):
        col = i
        ax2 = axs[col].twinx()
        filepath1 = os.path.join(directory, file_pair[0])
        df1=process_df(filepath1,'pi')

        filepath2 = os.path.join(directory, file_pair[1])
        df2=process_df(filepath2,'pi')
        
        if df1['PI_A_TEMP'].iloc[0] > df2['PI_A_TEMP'].iloc[0]:
            df1['PI_A_TEMP'] = df1['PI_A_TEMP'] - (df1['PI_A_TEMP'].iloc[0] - df2['PI_A_TEMP'].iloc[0])
        else:
            df2['PI_A_TEMP'] = df2['PI_A_TEMP'] - (df2['PI_A_TEMP'].iloc[0] - df1['PI_A_TEMP'].iloc[0])
        
        label1 = 'Test1 Chip Temperature'
        label2 = 'Test1 Power'
        label3 = 'Test1 Surface Temperature'

        if col==0:
            axs[col].plot(df1['TIME'], df1['TEMP'], label=label1,color='red' , linestyle='-.')
            axs[col].plot(df1['TIME'], df1['PI_A_TEMP'], label=label3,color='DarkOrange', linestyle='-.',linewidth=2.5)
            ax2.plot(df1['TIME'], df1['POWER'],label=label2,color='hotpink')
        else:
            axs[col].plot(df1['TIME'], df1['TEMP'],color='red', linestyle='-.')
            axs[col].plot(df1['TIME'], df1['PI_A_TEMP'], color='darkOrange', linestyle='-.',linewidth=2.5)
            ax2.plot(df1['TIME'], df1['POWER'],color='hotpink')
        
        if i==0:
            shadow_areas=[(64+60*60,-1)]
        if i==1:
            shadow_areas=[(91+60*60,-1)]
        if i==2:
            shadow_areas=[(103+60*60,-1)]

        label1 = 'Test2 Chip Temperature'
        label2 = 'Test2 Power'
        label3 = 'Test2 Surface Temperature'
        
        if col==0:
            axs[col].plot(df2['TIME'], df2['TEMP'], label=label1,color='blue', linestyle='-.')

            ax2.plot(df2['TIME'], df2['POWER'],label=label2,color='green')
            axs[col].plot(df2['TIME'], df2['PI_A_TEMP'], label=label3,color='purple', linestyle='-.')
        else:
            axs[col].plot(df2['TIME'], df2['TEMP'],color='blue', linestyle='-.')
            
            ax2.plot(df2['TIME'], df2['POWER'],color='green')
            axs[col].plot(df2['TIME'], df2['PI_A_TEMP'],color='purple', linestyle='-.')

        shadow_areas=get_shadow_area(df2)
        for area in shadow_areas:
            axs[col].axvspan(df2['TIME'].iloc[area[0]], df2['TIME'].iloc[area[1]-1], alpha=0.3, color='gray')
 
        axs[col].set_xlabel('Time (min)')
        if col==0:
            axs[col].set_ylabel('Temperature (℃)')
        axs[col].set_ylim(0, 85) 
        ax2.set_ylim(0, 6)
        axs[col].set_title('('+chr(97+col)+')'+' Pi_'+titles[col])

def plot_atlas_data(directory):
    files = [
        ('EX2_200B_Sun_FULL_1T_60_30.csv', 'EX2_200B_Umbra_FULL_1T_60_30.csv'),
        ('EX2_200B_Sun_FULL_4T_60_30.csv', 'EX2_200B_Umbra_FULL_4T_60_30.csv')
    ]
    titles=[
        'Full-1T','Full-4T'
    ]

    for i, file_pair in enumerate(files):
        col = i+3
        ax2 = axs[col].twinx()
       
        for j, file in enumerate(file_pair):
            if j == 0:
                filepath = os.path.join(directory, file)
                df=process_df(filepath,'atlas')
               
                axs[col].plot(df['TIME'], df['TEMP'],color='red', linestyle='-.')
                axs[col].plot(df['TIME'], df['ATLAS_B_TEMP'], color='darkOrange', linestyle='-.',linewidth=2.5)
                ax2.plot(df['TIME'], df['POWER'],color='hotpink')
                shadow_areas=get_shadow_area(df)
                
                for area in shadow_areas:
                    axs[col].axvspan(df['TIME'].iloc[area[0]], df['TIME'].iloc[area[1]-1], alpha=0.3, color='lightgray')
            else:
                filepath = os.path.join(directory, file)
                df=process_df(filepath,'atlas')
             
                axs[col].plot(df['TIME'], df['TEMP'],color='blue', linestyle='-.')
                ax2.plot(df['TIME'], df['POWER'],color='green')
                axs[col].plot(df['TIME'], df['ATLAS_B_TEMP'],color='purple', linestyle='-.')
                shadow_areas=get_shadow_area(df)

                for area in shadow_areas:
                    axs[col].axvspan(df['TIME'].iloc[area[0]], df['TIME'].iloc[area[1]-1], alpha=0.3, color='gray')
 
        axs[col].set_xlabel('Time (min)')#, fontsize=12
        if(col==4):
            ax2.set_ylabel('Power (w)')
        axs[col].set_ylim(0, 70)
        ax2.set_ylim(0, 12)
        ax2.set_yticks(np.arange(0, 13, 3))
        axs[col].set_title('('+chr(97+col)+')'+' Atlas_'+titles[i])

fig, axs = plt.subplots(1, 5, figsize=(18,4)) #3.85

# Plot data
plot_pi_data(directory_pi)
plot_atlas_data(directory_atlas)

plt.tight_layout()
plt.subplots_adjust(wspace=0.23)
plt.subplots_adjust(top=0.73)
legend=fig.legend(loc='upper center',bbox_to_anchor=(0.35,1),ncol=3,frameon=False)

for line in legend.get_lines():
    line.set_linewidth(2.5)
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='white', label='Daylight', edgecolor='black', linewidth=0.5),
    Patch(facecolor='Gainsboro', label='Eclipse', edgecolor='black', linewidth=0.5)
]

fig.legend(handles=legend_elements, bbox_to_anchor=(0.70,1),frameon=False)
fig.text(0.71, 0.85, 'Test1 Starts at DayLight\nTest2 Starts at Eclipse',fontsize=16)

# Output Data
outputdir="."
plt.savefig(outputdir+"/figure7" + '.pdf', dpi=1000)
# plt.show()