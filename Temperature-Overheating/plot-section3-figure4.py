#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# Set Input Path
gnd_infer_csv_path = "Data/pi_sun_infer/gnd_pi_infer_all_5.5V.csv"
sat_infer_csv_path = "Data/pi_sun_infer/sat_pi_sun_infer_180.csv"
gnd_infer_json_path = "Data/pi_sun_infer/gnd_pi_infer_all_5.5V.json"
sat_infer_json_path = "Data/pi_sun_infer/sat_pi_sun_Infer_180.json"

# Figure Config
plt.rc('font', size=14)  
fig, axs = plt.subplots(1,2,figsize=(14,4)) 

def deal_df(filepath):
    df = pd.read_csv(filepath)
    start=df['TIME'].min()
    df['TIME'] = (df['TIME'] - df['TIME'].min()) / 60  # convert TIME to mins
    df = df[df['TIME'] < 250]
    window_size = 100
    # Apply rolling mean to 'TIME' and 'TEMP'
    df['TIME'] = df['TIME'].rolling(window=window_size).mean()
    df['TEMP'] = df['TEMP'].rolling(window=window_size).mean()
    df['FREQUENCY(48)'] = df['FREQUENCY(48)'].rolling(window=2*window_size).mean()
    df['TEMP_normalized'] = df['TEMP'] 
    return start,df

def deal_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    cp_tasks = []
    ip_tasks = []
    whole_tasks = []
    for j in range(0, len(data)-3, 3):
        group = data[j:j+3]
        cp_task = group[0]
        cp_tasks.append(cp_task)
        ip_tasks.append(group[1])
        whole_task = group[2]
        whole_task['start_time'] = group[0]['start_time']
        whole_tasks.append(whole_task)
    return cp_tasks,ip_tasks


start1,df1 = deal_df(gnd_infer_csv_path)
start2,df2 = deal_df(sat_infer_csv_path)

cp_tasks1,ip_tasks1=deal_json(gnd_infer_json_path)
cp_tasks2,ip_tasks2=deal_json(sat_infer_json_path)

max_cp_time = max(max(t['execute_time'] for t in cp_tasks1),max(t['execute_time'] for t in cp_tasks2))
max_time_mv1_ssd = max(max(t['execute_time_0'] for t in ip_tasks1),max(t['execute_time_0'] for t in ip_tasks2))
max_time_yolofastest = max(max(t['execute_time_1'] for t in ip_tasks1),max(t['execute_time_1'] for t in ip_tasks2))
max_time_v3 = max(max(t['execute_time_2'] for t in ip_tasks1),max(t['execute_time_2'] for t in ip_tasks2))
max_time_v5 = max(max(t['execute_time_3'] for t in ip_tasks1),max(t['execute_time_3'] for t in ip_tasks2))
max_frequency=max(df1['FREQUENCY(48)'].max(),df2['FREQUENCY(48)'].max())

ip_start_times1=[t['start_time'] for t in ip_tasks1]
ip_start_times1=(np.array(ip_start_times1)-start1) / 60

cp_start_times1=[t['start_time'] for t in cp_tasks1]
cp_start_times1=(np.array(cp_start_times1)-start1) / 60
normalized_cp_exec_times = [t['execute_time'] / max_cp_time for t in cp_tasks1]
normalized_mv1_ssd_exec_times = [t['execute_time_0'] /max_time_mv1_ssd for t in ip_tasks1]
normalized_yolofastest_exec_times = [t['execute_time_1'] /max_time_yolofastest for t in ip_tasks1]
normalized_v3_exec_times = [t['execute_time_2'] /max_time_v3 for t in ip_tasks1]
normalized_v5_exec_times = [t['execute_time_3'] /max_time_v5 for t in ip_tasks1]

ax2=axs[0].twinx() 
axs[0].plot(ip_start_times1, normalized_mv1_ssd_exec_times,label=" SSD-MV1 Latency",color='blue')
axs[0].plot(ip_start_times1, normalized_yolofastest_exec_times,label="YOLO-Fastest Inference Latency",color='green')
axs[0].plot(ip_start_times1, normalized_v3_exec_times,label="YOLOv3 Inference Latency",color='orange')
axs[0].plot(ip_start_times1, normalized_v5_exec_times,label="YOLOv5-Lite Inference Latency",color='purple')

axs[0].plot(df1['TIME'], df1['FREQUENCY(48)']/ max_frequency,label="Frequency",color='black')
ax2.plot(df1['TIME'], df1['TEMP_normalized'], label="Temperature",color='red')
axs[0].set_xlabel("Time(min)")
axs[0].set_ylim(0.75, 1.05)
ax2.set_ylim(0,90)
axs[0].set_ylabel("Normalized Value")

ip_start_times2=[t['start_time'] for t in ip_tasks2]
ip_start_times2=(np.array(ip_start_times2)-start2) / 60

cp_start_times2=[t['start_time'] for t in cp_tasks2]
cp_start_times2=(np.array(cp_start_times2)-start2) / 60
normalized_cp_exec_times = [t['execute_time'] / max_cp_time for t in cp_tasks2]
normalized_mv1_ssd_exec_times = [t['execute_time_0'] /max_time_mv1_ssd for t in ip_tasks2]
normalized_yolofastest_exec_times = [t['execute_time_1'] /max_time_yolofastest for t in ip_tasks2]
normalized_v3_exec_times = [t['execute_time_2'] /max_time_v3 for t in ip_tasks2]
normalized_v5_exec_times = [t['execute_time_3'] /max_time_v5 for t in ip_tasks2]

ax2=axs[1].twinx() 
axs[1].plot(ip_start_times2, normalized_mv1_ssd_exec_times,color='blue')
axs[1].plot(ip_start_times2, normalized_yolofastest_exec_times,color='green')
axs[1].plot(ip_start_times2, normalized_v3_exec_times,color='orange')
axs[1].plot(ip_start_times2, normalized_v5_exec_times,color='purple')

axs[1].plot(df2['TIME'], df2['FREQUENCY(48)']/ max_frequency,color='black')
ax2.plot(df2['TIME'], df2['TEMP_normalized'],color='red')

axs[1].set_xlabel("Time(min)")
axs[1].set_ylim(0.75, 1.05)
ax2.set_ylim(0,90)
ax2.set_ylabel("Temperature(℃)")

axs[0].set_title('(a) Ground')
axs[1].set_title('(b) Satellite')
plt.tight_layout()
plt.subplots_adjust(top=0.75)
legend=fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1), ncol=3,frameon=False)

# Output Data
savedir='.'
plt.savefig(savedir+"/figure4" + '.pdf', dpi=1000)
# plt.show()