#!/usr/bin/python3
import pandas as pd
import numpy as np
import os

# Function to process the files
def process_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(directory, filename))
            df = df[df['INDEX'] >= 0]  # consider the part of data where INDEX >= 0
            df = df.sort_values(by='TIME')  # ensure data is sorted by TIME

            I = np.trapz(df['I_Atlas200DK-B'], df['TIME'])  # calculate the integral of 'Main(mA)' over 'TIME'
            total_energy = I * 12 / 1000  # calculate total energy
            max_index = df['INDEX'].max()  # get max INDEX

            averaged_energy = total_energy / max_index  # calculate averaged energy
            
            print(f"For file {filename}:")
            print(f"Total energy = {total_energy}")
            print(f"Averaged energy = {averaged_energy}")
            if filename.endswith('1T_180.csv'):
                print(f"100 Pic energy = {averaged_energy * 100}")
            else:
                print(f"100 Pic energy = {averaged_energy / 13}")
            print("\n")

process_files('Data/sat_atlas_infer')
