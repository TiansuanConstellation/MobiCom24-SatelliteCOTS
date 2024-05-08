#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.insert(0, "battery_curve")
from processing import get_discharge_curve, get_charge_curve
from scipy import interpolate

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# Set Input Path
dir_tele_1 = 'telemetries/all.csv'
dir_tele_2 = 'telemetries/payload.csv'

# Figure Config
plt.rcParams.update({'font.size': 20})

def split_arr(x, y):
    x1 = []
    x2 = []
    y1 = []
    y2 = []
    if len(x) != len(y):
        print("wrong input")
        return
    for i in range(len(x)):
        if y[i] >= 0:
            x1.append(x[i])
            y1.append(y[i])
        else:
            x2.append(x[i])
            y2.append(y[i])
    return x1, y1, x2, y2

def shrink(x, y, step):
    xx = []
    yy = []
    i = 0
    while i < len(x):
        x_sum = 0
        y_sum = 0
        for k in range(step):
            if (i+k) >= len(x):
                break
            x_sum = x_sum + x[i+k]
            y_sum = y_sum + y[i+k]
        xx.append(x_sum/step)
        yy.append(y_sum/step)
        i = i + step
    return xx, yy

def process_mppt(current_mppt):
    i = 1
    while (i+2) < len(current_mppt):
        if i == len(current_mppt)-1:
            break
        if i > 0:
            average_c = current_mppt[i] + current_mppt[i+1] + current_mppt[i+2]
            current_mppt[i] = average_c
            current_mppt[i+1] = average_c
            current_mppt[i+2] = average_c
            i = i + 3
    return current_mppt

def process_battery(battery_volt):
    battery_volt_2 = []
    battery_volt_0 = []
    for i in range(len(battery_volt)):
        if battery_volt[i]!=0 and i%4==0:
            battery_volt_2.append(battery_volt[i]/1000.0)
            battery_volt_2.append(battery_volt[i]/1000.0)
            battery_volt_2.append(battery_volt[i]/1000.0)
            battery_volt_2.append(battery_volt[i]/1000.0)
        elif battery_volt[i]!=0 and i%4==2:
            battery_volt_0.append(battery_volt[i]/1000.0)
            battery_volt_0.append(battery_volt[i]/1000.0)
            battery_volt_0.append(battery_volt[i]/1000.0)
            battery_volt_0.append(battery_volt[i]/1000.0)
    return battery_volt_0, battery_volt_2

# Read the CSV file
df = pd.read_csv(dir_tele_1)
df_2 = pd.read_csv(dir_tele_2)

current = df['Total_I'].to_numpy()
voltage = df['Total_U'].to_numpy()
current_mppt = df['MPPT_Iout'].to_numpy()
current_uv = df['UV_I'].to_numpy()
current_pobc = df['POBC_I_5V'].to_numpy()
current_x_1 = df['XMIT_A_12V'].to_numpy()
current_x_2 = df['XMIT_B_12V'].to_numpy()
voltage_b = df['Battery_U'].to_numpy()
current_b = df['Battery_I'].to_numpy()

p_comp = df_2['I_Atlas200DK-B'].to_numpy()
p_comp = p_comp * 12 / 1000

# cal total consumption
power = current * voltage / 1000000
p_battery = voltage_b * (-current_b) / 1000000

# cal solar panel power
p_mppt = process_mppt(current_mppt) * voltage / 1000000

# cal added communication power
p_uv = current_uv * 3.3
p_pobc = current_pobc * 5
p_x = (current_x_1 + current_x_2) * 12
p_comm = (p_uv + p_pobc + p_x) / 1000

i = 0
x = []
for i in range(len(power)):
    x.append(i)

x_comp = []
for i in range(len(p_comp)):
    x_comp.append(i * 2)

voltage, battery_percentage = get_discharge_curve()
v_charge, b_charge = get_charge_curve()
f = interpolate.interp1d(voltage, battery_percentage)
f_charge = interpolate.interp1d(v_charge, b_charge)
b0, b2 = process_battery(voltage_b)
_, b0 = shrink(x, b0, 10)
_, b2 = shrink(x, b2, 10)
percent_b0 = f(b0)
percent_b2 = f(b2)
percent_b0_charge = f_charge(b0)
percent_b2_charge = f_charge(b2)

xs, y_power = shrink(x, power, 10)
_, y_mppt = shrink(x, p_mppt, 10)
_, y_comm = shrink(x, p_comm, 10)
xs_comp, y_comp = shrink(x_comp, p_comp, 5)

xs_min = [s/60 for s in xs]
xs_comp_min = [s/60 for s in xs_comp]

fig, ax1 = plt.subplots(figsize=(10, 7))
ax1.set_xlabel("Time (min)")
ax1.set_ylabel("Power (W)")
ax1.set_ylim([0, 50])

ax1.plot(xs_min, y_mppt, label="Solar Power", color="#008200", linewidth=3)
ax1.plot(xs_min, y_power, label="Total Power", color="#f80404", linewidth=3)
ax1.plot(xs_min, y_comm, label="Communication Power", color="indigo", linewidth=3)
ax1.plot(xs_min, y_comp, label="Computing Power", color="#ff9f50", linewidth=3)
ax1.plot(xs_min, [x - y - z for x, y, z in zip(y_power, y_comm, y_comp)], label="Others Power", color="darkcyan", linewidth=3)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('Depth of Discharge (%)')
ax2.set_ylim([100, 0])
ax2.plot(xs_min, [ 100-(100-(x + y)/2) for x, y in zip(percent_b0, percent_b2)], label="DoD", color="#0606f4", linewidth=3)
ax2.tick_params(axis='y')
fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.03), frameon=False, ncol=3, fontsize=20, handlelength=1.5, handletextpad=0.6)

# Output Data
savedir='.'
plt.savefig(savedir+"/figure11" + '.pdf', dpi=1000)
# plt.show()