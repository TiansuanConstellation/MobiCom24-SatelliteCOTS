#!/usr/bin/python3
import os
import matplotlib.pyplot as plt
import json

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# Set Input Path
dir = 'Data/pi_infer_yolo'

files = [
    ('PiA_Sun_Yolofastest_60.json', 'PiA_Umbra_yolofastest_60.json'),
    ('PiA_Sun_Yolov5lite_60.json', 'PiA_Umbra_yolo-v5lite_60.json'),
    ('PiA_Sun_Yolov354460_60.json', 'PiA_Umbra_yolov3_544_60.json')
]

# Figure Config
plt.rc('font', size=18)

def get_infer_times(file):
    with open(file) as f:
        data = json.load(f)
        infer_times = []
        
        for item in data:
            if 'success_list' in item:
                infer_time = int(item['execute_time']) / len(item['success_list']) / 1000
            else:
                infer_time = int(item['execute_time']) / 1000
            
            infer_times.append(infer_time)
        
    return infer_times

SunData = {
    'YOLO-Fastest': get_infer_times(os.path.join(dir, files[0][0])),
    'YOLOv3':get_infer_times(os.path.join(dir, files[2][0])),
    'YOLOv5-Lite': get_infer_times(os.path.join(dir, files[1][0])),
}

UmbraData = {
    'YOLO-Fastest': get_infer_times(os.path.join(dir, files[0][1])),
    'YOLOv3':get_infer_times(os.path.join(dir, files[2][1])),
    'YOLOv5-Lite': get_infer_times(os.path.join(dir, files[1][1])),
}

fig, ax1 = plt.subplots(figsize=(6,4))
ax2 = ax1.twinx()

colors = ['orange', 'lightgray']
positions = [0.8,1.8, 3]

ax2.boxplot([SunData['YOLOv3'],SunData['YOLOv5-Lite']], positions=[1.8,3], patch_artist=True,  medianprops={'color': 'black'}, boxprops=dict(facecolor=colors[0]), showfliers=False,widths=0.3)
ax2.boxplot([SunData['YOLOv3'],SunData['YOLOv5-Lite']], positions=[2.1,3.3], patch_artist=True,  medianprops={'color': 'black'}, boxprops=dict(facecolor=colors[1]), showfliers=False,widths=0.3)

ax1.boxplot(SunData['YOLO-Fastest'], positions=[0.8], patch_artist=True, boxprops=dict(facecolor=colors[0]),  medianprops={'color': 'black'}, showfliers=False,widths=0.3)
ax1.boxplot(UmbraData['YOLO-Fastest'], positions=[1.1], patch_artist=True, boxprops=dict(facecolor=colors[1]),  medianprops={'color': 'black'}, showfliers=False,widths=0.3)

ax1.set_ylim(0, 5)
ax1.set_ylabel('Inference Latency(s)')
ax2.set_ylabel('Inference Latency(s)')

labels = list(SunData.keys())
ax1.set_xticks([0.85,2.1,3.15])

ax1.set_xticklabels(labels,fontsize=16)
plt.axvline(x=1.5, color='black')
legend_elements = [
    plt.Rectangle((0, 0), 1, 1, color=colors[0], label='Daylight'),
    plt.Rectangle((0, 0), 1, 1, color=colors[1], label='Eclipse')
]
plt.legend(handles=legend_elements,frameon=False,fontsize=16)

fig.tight_layout()

# Output Data
outputdir="."
plt.savefig(outputdir+"/figure8" + '.pdf', dpi=1000)
# plt.show()