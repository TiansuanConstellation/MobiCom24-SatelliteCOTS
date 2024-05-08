#!/usr/bin/python3
import os
import matplotlib.pyplot as plt
import json

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# Set Input Path
dir1 = 'Data/gnd_atlas_infer'
dir2 = 'Data/sat_atlas_infer'

# Figure Config
plt.rc('font', size=17)

# Your file pairs
files = [
    ('atlas_infer_low_od1.json', '200B_Sun_LOW_1T_180.json'),
    ('atlas_infer_mid_od1.json', '200B_Sun_MIDDLE_1T_180.json'),
    ('atlas_infer_high_od1.json', '200B_Sun_HIGH_1T_180.json'),
    ('atlas_infer_full_od1.json', '200B_Sun_FULL_1T_180.json')
]

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
GroundData = {
    'low': get_infer_times(os.path.join(dir1, files[0][0])),
    'mid': get_infer_times(os.path.join(dir1, files[1][0])),
    'high':get_infer_times(os.path.join(dir1, files[2][0])),
    'full':get_infer_times(os.path.join(dir1, files[3][0]))
}

SatData = {
    'low': get_infer_times(os.path.join(dir2, files[0][1])),
    'mid': get_infer_times(os.path.join(dir2, files[1][1])),
    'high':get_infer_times(os.path.join(dir2, files[2][1])),
    'full':get_infer_times(os.path.join(dir2, files[3][1]))
}
fig, ax = plt.subplots(figsize=(6,4))

colors = ['gray', 'orange']
positions = [1, 2,3,4]

ax.boxplot(GroundData.values(), positions=positions, patch_artist=True,showfliers=False, boxprops=dict(facecolor=colors[0]), widths=0.3,medianprops={'color': 'black'})
ax.boxplot(SatData.values(), positions=[pos+0.3 for pos in positions], patch_artist=True, showfliers=False,boxprops=dict(facecolor=colors[1]), widths=0.3,medianprops={'color': 'black'})

ax.set_ylabel('Inference Latency(s)')

legend_elements = [
    plt.Rectangle((0, 0), 1, 1, color=colors[0], label='Ground'),
    plt.Rectangle((0, 0), 1, 1, color=colors[1], label='Satellite')
]
plt.legend(handles=legend_elements,frameon=False)
labels = list(GroundData.keys())
ax.set_xticks([pos+0.15 for pos in positions])

ax.set_xticklabels(labels)
ax.set_xlabel('Computing Level')
fig.tight_layout()

# Output Data
outputdir='.'
plt.savefig(outputdir+"/figure5" + '.pdf', dpi=1000)
# plt.show()