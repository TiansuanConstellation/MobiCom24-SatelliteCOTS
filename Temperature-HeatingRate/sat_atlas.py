#!/usr/bin/python3
import os
import pandas as pd
from scipy.stats import mode

def process_files(directory):
    # Step 1: Get a list of all files in the directory
    file_list = [f for f in os.listdir(directory) if f.endswith('.csv')]

    for filename in file_list:
        # Read the file
        df = pd.read_csv(os.path.join(directory, filename))

        # Step 2: Calculate average power
        # Power1 is calculated when 'INDEX' != -1
        df.loc[df['INDEX'] != -1, 'Power1'] = df[df['INDEX'] != -1]['I_Atlas200DK-B'] * 12 / 1000
        power1 = df['Power1'].mean()

        # Power2 is calculated when 'INDEX' == -1
        df.loc[df['INDEX'] == -1, 'Power2'] = df[df['INDEX'] == -1]['I_Atlas200DK-B'] * 12 / 1000
        power2 = df['Power2'].mean()

        # Calculate the global max in the first 66% of the time
        time_66_percent = df['TIME'].quantile(0.66)
        global_max = df[df['TIME'] <= time_66_percent]['TEMP'].max()
        global_min = df[df['TIME'] > time_66_percent]['TEMP'].min()

        # Update time1_end and time2_end
        time1_end = df[(df['TIME'] <= time_66_percent) & (df['TEMP'] == global_max)]['TIME'].min()
        time2_end = df[(df['TIME'] > time_66_percent) & (df['TEMP'] == global_min)]['TIME'].min()

        # Calculate time ranges and variances
        time1_start = df['TIME'].min()
        # time2_start = df[df['TEMP'] == time_66_percent]['TIME'].max()
        time2_start = time1_end

        var1 = df[(df['TIME'] >= time1_start) & (df['TIME'] <= time1_end)]['TEMP'].var()
        var2 = df[(df['TIME'] > time2_start) & (df['TIME'] <= time2_end)]['TEMP'].var()

        # df.set_index('TIME', inplace=True)
        nearest_time1_start = df.iloc[(df['TIME']-time1_start).abs().argsort()[:1]]['TEMP'].values[0]
        nearest_time1_end = df.iloc[(df['TIME']-time1_end).abs().argsort()[:1]]['TEMP'].values[0]
        nearest_time2_start = df.iloc[(df['TIME']-time2_start).abs().argsort()[:1]]['TEMP'].values[0]
        nearest_time2_end = df.iloc[(df['TIME']-time2_end).abs().argsort()[:1]]['TEMP'].values[0]

        time1_temp_diff = nearest_time1_end - nearest_time1_start
        time2_temp_diff = nearest_time2_end - nearest_time2_start

        # Step 4: Print the results
        print(f"Filename: {filename}")
        # print(f"Time2 start: {time2_start}")
        # print(f"Time2 end: {time2_end}")
        print(f"Average Power1 (W): {power1}")
        print(f"Average Power2 (W): {power2}")
        print(f"Time1 (min): {(time1_end - time1_start)/60}")
        print(f"Time2 (min): {(time2_end - time2_start)/60}")
        print('Time1 range:', time1_start, 'to', time1_end, ', Temp start:', nearest_time1_start, ', Temp end:', nearest_time1_end, ', Temp diff:', time1_temp_diff)
        print('Time2 range:', time2_start, 'to', time2_end, ', Temp start:', nearest_time2_start, ', Temp end:', nearest_time2_end, ', Temp diff:', time2_temp_diff)
        print(f"Var1: {var1}")
        print(f"Var2: {var2}")
        print("\n")

# Calling the function with the path of the directory
process_files('Data/sat_atlas_infer')
