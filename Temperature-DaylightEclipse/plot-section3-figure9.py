#!/usr/bin/python3
import os
import matplotlib.pyplot as plt
import json

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# Set Input Path
dir = 'Data/atlas_sun_shadow'

files = [
    ('200B_Sun_FULL_1T_60_30.json', '200B_Umbra_FULL_1T_60_30.json'),
    ('200B_Sun_FULL_4T_60_30.json', '200B_Umbra_FULL_4T_60_30.json')
]

# Figure Config
plt.rc('font', size=18)

def get_infer_times(file):
    with open(file) as f:
        data = json.load(f)
        infer_times = []
        
        for item in data:
            if 'success_list' in item:
                infer_time = int(item['infer_time']) / len(item['success_list']) / 1000
            else:
                infer_time = int(item['infer_time']) / 1000
            
            infer_times.append(infer_time)
        
    return infer_times

SunData = {
    'Full-1T': get_infer_times(os.path.join(dir, files[0][0])),
    'Full-4T': get_infer_times(os.path.join(dir, files[1][0]))
}

UmbraData = {
    'Full-1T': get_infer_times(os.path.join(dir, files[0][1])),
    'Full-4T': get_infer_times(os.path.join(dir, files[1][1]))
}

fig, ax1 = plt.subplots(figsize=(6.55,4))
ax2 = ax1.twinx()

colors = ['orange', 'lightgray']
positions = [1, 3]

ax1.boxplot(SunData['Full-1T'], positions=[1], patch_artist=True,  medianprops={'color': 'black'}, boxprops=dict(facecolor=colors[0]), showfliers=False,widths=0.5)
ax1.boxplot(UmbraData['Full-1T'], positions=[1.5], patch_artist=True,  medianprops={'color': 'black'}, boxprops=dict(facecolor=colors[1]), showfliers=False,widths=0.5)
ax2.boxplot(SunData['Full-4T'], positions=[3], patch_artist=True,  medianprops={'color': 'black'}, boxprops=dict(facecolor=colors[0]), showfliers=False,widths=0.5)
ax2.boxplot(UmbraData['Full-4T'], positions=[3.5], patch_artist=True,  medianprops={'color': 'black'}, boxprops=dict(facecolor=colors[1]), showfliers=False,widths=0.5)

ax1.set_ylim(2, 2.6)
ax2.set_ylim(0.08, 0.1)
ax1.set_ylabel('Inference Latency(s)')
ax2.set_ylabel('Inference Latency(s)')

labels = list(SunData.keys())
ax1.set_xticks( [1.3,3.3])

ax1.set_xticklabels(labels)
plt.axvline(x=2.35, color='black')
legend_elements = [
    plt.Rectangle((0, 0), 1, 1, color=colors[0], label='Daylight'),
    plt.Rectangle((0, 0), 1, 1, color=colors[1], label='Eclipse')
]
plt.legend(handles=legend_elements,frameon=False,fontsize=16)

fig.tight_layout()

# Output Data
outputdir="."
plt.savefig(outputdir+"/figure9" + '.pdf', dpi=1000)
# plt.show()