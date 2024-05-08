#!/usr/bin/python3
import sys
import pandas as pd
from datetime import timedelta

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# Load data
def find_all_rounds(df):
    df['Time'] = pd.to_datetime(df['Time'])
    # Identify sunlit and shadow periods
    df['Sunlit'] = (df['MPPT1_Uin'] != 0) & (df['MPPT2_Uin'] != 0)
    # Initialize round starts/ends
    starts = []
    ends = []
    # Iterate over rows
    for i in range(1, len(df)):
        # Start of a new round
        if df.loc[i, 'Sunlit'] and not df.loc[i-1, 'Sunlit']:
            starts.append(df.loc[i, 'Time'])
        # End of a round
        elif (i+1) < len(df) and not df.loc[i, 'Sunlit'] and df.loc[i+1, 'Sunlit']:
            ends.append(df.loc[i, 'Time'])
    ends = ends[1:]
    # Pair round starts and ends to identify complete rounds
    rounds = list(zip(starts, ends))
    # # Filter rounds to those that last about 90 minutes (complete rounds)
    rounds = [(start, end) for start, end in rounds if 80 < (end - start).seconds / 60 < 100]
    return rounds

def find_longest_continuous_rounds(rounds):
    # Sort the rounds by start time
    rounds.sort(key=lambda x: x[0])
    longest_rounds = []
    current_rounds = [rounds[0]]
    # Iterate over the sorted rounds
    for i in range(1, len(rounds)):
        # If the start time of the next round is within 1 second from the end time of the current round
        # then they are considered as continuous
        if rounds[i][0] - current_rounds[-1][1] <= timedelta(seconds=1):
            current_rounds.append(rounds[i])
        else:
            # If the next round is not continuous, check if the current continuous rounds is longer
            if len(current_rounds) > len(longest_rounds):
                longest_rounds = current_rounds
            # Start a new sequence of continuous rounds
            current_rounds = [rounds[i]]
    # Check the last sequence of continuous rounds
    if len(current_rounds) > len(longest_rounds):
        longest_rounds = current_rounds
        
    return longest_rounds

def get_all_rounds(df):
    rounds = []
    is_sunlit = False
    round_start = None
    for i in range(len(df)):
        # Check if the satellite is in sunlit area
        if df.iloc[i]['MPPT1_Uin'] != 0 and df.iloc[i]['MPPT2_Uin'] != 0:
            if not is_sunlit:
                # The start of a round
                round_start = df.iloc[i]['Time']
                is_sunlit = True
        else:
            if is_sunlit:
                # The end of a round
                rounds.append([round_start, df.iloc[i]['Time']])
                is_sunlit = False
    return rounds

import datetime
from collections import Counter
def find_common_rounds(all_rounds):
    """
    Find the most common rounds considering a 10 minutes tolerance.

    Parameters:
    all_rounds (list): List of all rounds.

    Returns:
    list: List of the most common rounds.
    """
    # Create a new list of rounds normalized to a single day and rounded to the nearest 10 minutes
    normalized_rounds = []
    for round in all_rounds:
        normalized_rounds.append([
            datetime.datetime.combine(datetime.date.today(), round[0].time()) - datetime.timedelta(minutes=round[0].time().minute % 10, 
                                                                                                seconds=round[0].time().second),  # Start time
            datetime.datetime.combine(datetime.date.today(), round[1].time()) - datetime.timedelta(minutes=round[1].time().minute % 10, 
                                                                                                seconds=round[1].time().second)  # End time
        ])
    # Count the frequency of each round
    counter = Counter(tuple(round) for round in normalized_rounds)
    # Find the most common round
    most_common_round = counter.most_common(1)[0][0]
    # Find the exact dates of the most common round with a 10 minute tolerance
    most_common_round_dates = []
    for round in all_rounds:
        round_start = datetime.datetime.combine(datetime.date.today(), round[0].time())
        round_end = datetime.datetime.combine(datetime.date.today(), round[1].time())
        if abs((round_start - most_common_round[0]).total_seconds()) <= 600 and abs((round_end - most_common_round[1]).total_seconds()) <= 600:
            most_common_round_dates.append(round)
    return most_common_round_dates

from scipy.integrate import trapezoid
def check_and_drop_edges(df):
    # If 'Time' is not monotonically increasing
    if not df['Time'].is_monotonic_increasing:
        # Drop the first and last row
        df = df.iloc[1:-1]
    return df

def calculate_energy(df, rounds):
    energy_per_round = []
    index = 0
    for round in rounds:
        # Select the data for the current round
        data = df[(df['Time'] > round[0]) & (df['Time'] < round[1])]
        data = check_and_drop_edges(data)
        # Calculate the difference in hours between the start of the round and each timestamp
        time_diff_hours = (data['Time'] - round[0]).dt.total_seconds() / 3600
        if index == 36:
            print(data['Time'])
            print(time_diff_hours)
        # Calculate the total energy consumed in the round
        total_energy = trapezoid(data['Total_I'] * 0.9 / 1000 * data['Total_U'] / 1000, x=time_diff_hours)
        # Calculate the solar harvested energy in the round
        solar_harvested_energy = trapezoid(data['MPPT1_Iout'] / 1000 * data['Total_U'] / 1000 + data['MPPT2_Iout'] * 1.1 / 1000 * data['Total_U'] / 1000, x=time_diff_hours)
        # Calculate the communication energy in the round
        comm_energy = trapezoid(data['UV_I'] / 1000 * 3.3 + data['POBC_I_5V'] / 1000 * 5 + data['XMIT_A_12V'] / 1000 * 12 + data['XMIT_B_12V'] / 1000 * 12, x=time_diff_hours)
        # Calculate the payload energy in the round
        payload_energy = trapezoid(data['I_Atlas200DK-A'] / 1000 * 12 + data['I_Atlas200DK-B'] / 1000 * 12 + data['I_Pi-A'] / 1000 * 5 + data['I_Pi-B'] / 1000 * 5, x=time_diff_hours)
        # Calculate the other energy consumed in the round
        other_energy = total_energy - comm_energy - payload_energy
        # Store the results
        energy_per_round.append({
            'round_start': round[0],
            'round_end': round[1],
            'total_energy': total_energy,
            'solar_harvested_energy': solar_harvested_energy,
            'comm_energy': comm_energy,
            'payload_energy': payload_energy,
            'other_energy': other_energy,
        })
        index+=1
    # Convert the list of dictionaries to a DataFrame
    energy_df = pd.DataFrame(energy_per_round)
    return energy_df

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})

def plot_energy_consumption(energy_df, fig_name):
    fig, ax = plt.subplots(figsize=(12, 7.5))
    # Energy consumption plots
    ax.bar(range(len(energy_df)), energy_df['solar_harvested_energy'], color='green', label='Solar')
    ax.bar(range(len(energy_df)), -energy_df['comm_energy'], color='blue', label='Communication')
    ax.bar(range(len(energy_df)), -energy_df['payload_energy'], color='red', bottom=-energy_df['comm_energy'], label='Computing')
    ax.bar(range(len(energy_df)), -energy_df['other_energy'], color='purple', bottom=-(energy_df['comm_energy']+energy_df['payload_energy']), label='Others')
    # print(energy_df['solar_harvested_energy'].max())
    # print(energy_df['solar_harvested_energy'].mean())
    # Set labels
    ax.set_xlabel('Orbital Period Number')
    ax.set_ylabel('Energy (Wh)')
    # ax.set_xticks(np.arange(0, len(energy_df)+1, 2))
    # Set legend
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.13), ncol=4, frameon=False)
    plt.savefig(fig_name + '.pdf', dpi=1000)
    # Display the plot
    # plt.show()

if len(sys.argv) > 1:
    condition = sys.argv[1]
    if condition == 'longest':
        energy_df = pd.read_csv('Data/longest_rounds_energy_df.csv')
        plot_energy_consumption(energy_df, "figure12")
    elif condition == 'common':
        energy_df = pd.read_csv('Data/common_rounds_energy_df.csv')
        plot_energy_consumption(energy_df, "figure13")
    else:
        print("Invalid argument. Please use 'longest' or 'common'.")
else:
    print("No argument provided.")