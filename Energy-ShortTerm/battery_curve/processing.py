import pandas as pd
from statistics import mean

def get_charge_curve():
    df1 = pd.read_csv("battery_curve/charging_df_1.csv")
    df2 = pd.read_csv("battery_curve/charging_df_2.csv")

    df1 = df1[df1['Energy(Wh)'] <= 115]
    df2 = df2[df2['Energy(Wh)'] <= 115]

    df1_normalized = (df1['Energy(Wh)'] / 115) * 100
    df2_normalized = (df2['Energy(Wh)'] / 115) * 100

    battery_percentage = [mean(pair) for pair in zip(df1_normalized.to_list(), df2_normalized.to_list())]
    voltage = [mean(pair) for pair in zip(df1['Voltage(V)'].to_list(), df2['Voltage(V)'].to_list())]

    return voltage, battery_percentage

def get_discharge_curve():
    df1 = pd.read_csv("battery_curve/discharging_df_1.csv")
    df2 = pd.read_csv("battery_curve/discharging_df_2.csv")

    df1 = df1[df1['Energy(Wh)'] <= 115]
    df2 = df2[df2['Energy(Wh)'] <= 115]

    df1_normalized = (df1['Energy(Wh)'] / 115) * 100
    df2_normalized = (df2['Energy(Wh)'] / 115) * 100

    battery_percentage = [mean(pair) for pair in zip(df1_normalized.to_list(), df2_normalized.to_list())]
    voltage = [mean(pair) for pair in zip(df1['Voltage(V)'].to_list(), df2['Voltage(V)'].to_list())]

    return voltage, battery_percentage