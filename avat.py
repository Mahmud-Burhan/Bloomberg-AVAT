# AVAT Function inspired from Bloomberg Terminal
# Replicated by: Mahmud bin Burhanudin (github.com/Mahmud-Burhan)
# Date: 2024-01-07
# Version: 1.0.0

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

get_ticker = str(input("Enter ticker: "))
get_days_range = int(input("Enter days range: (any integer 1-730) "))
# Valid days range refer https://www.qmr.ai/yfinance-library-the-definitive-guide/

ticker = yf.Ticker(get_ticker).history(period=f"{get_days_range + 1}d", interval="1h")
if ticker.empty:
    raise Exception("Ticker not found")
ticker = ticker.drop(columns=['Dividends', 'Stock Splits'])

mod_ticker = ticker.copy()
mod_ticker = mod_ticker[:-7] # remove last 7 rows
mod_ticker["Hour"] = mod_ticker.index.hour # get the hour
mod_ticker = mod_ticker.sort_values(by=['Hour'])

first_hour = []; second_hour = []; third_hour = []
fourth_hour = []; fifth_hour = []; sixth_hour = []
seventh_hour = []
START = 9; END = 16

# iterate through mod_ticker and append to the respective list
for index, row in mod_ticker.iterrows():
    if row['Hour'] == START:
        first_hour.append(row['Volume'])
    elif row['Hour'] == START + 1:
        second_hour.append(row['Volume'])
    elif row['Hour'] == START + 2:
        third_hour.append(row['Volume'])
    elif row['Hour'] == START + 3:
        fourth_hour.append(row['Volume'])
    elif row['Hour'] == START + 4:
        fifth_hour.append(row['Volume'])
    elif row['Hour'] == START + 5:
        sixth_hour.append(row['Volume'])
    elif row['Hour'] == START + 6:
        seventh_hour.append(row['Volume'])

# Convert to mean and set the cumulative volume
first_hour = np.mean(first_hour); second_hour = np.mean(second_hour) + first_hour
third_hour = np.mean(third_hour) + second_hour; fourth_hour = np.mean(fourth_hour) + third_hour
fifth_hour = np.mean(fifth_hour) + fourth_hour; sixth_hour = np.mean(sixth_hour) + fifth_hour
seventh_hour = np.mean(seventh_hour) + sixth_hour

cumulative_volume = [first_hour, second_hour, third_hour, fourth_hour, fifth_hour, sixth_hour, seventh_hour]

comparison_ticker = ticker[-7:] # get last 7 rows, DO NOT USE MOD_TICKER
c_first_hour = comparison_ticker.iloc[0]['Volume']; c_second_hour = comparison_ticker.iloc[1]['Volume']
c_third_hour = comparison_ticker.iloc[2]['Volume']; c_fourth_hour = comparison_ticker.iloc[3]['Volume']
c_fifth_hour = comparison_ticker.iloc[4]['Volume']; c_sixth_hour = comparison_ticker.iloc[5]['Volume']
c_seventh_hour = comparison_ticker.iloc[6]['Volume']
# Convert to mean and set the cumulative volume
c_first_hour = np.mean(c_first_hour); c_second_hour = np.mean(c_second_hour) + c_first_hour
c_third_hour = np.mean(c_third_hour) + c_second_hour; c_fourth_hour = np.mean(c_fourth_hour) + c_third_hour
c_fifth_hour = np.mean(c_fifth_hour) + c_fourth_hour; c_sixth_hour = np.mean(c_sixth_hour) + c_fifth_hour
c_seventh_hour = np.mean(c_seventh_hour) + c_sixth_hour

c_cumulative_volume = [c_first_hour, c_second_hour, c_third_hour, c_fourth_hour, c_fifth_hour, c_sixth_hour, c_seventh_hour]

percentage_change = (c_cumulative_volume[-1] - cumulative_volume[-1]) / cumulative_volume[-1] * 100

# plot the cumulative volume against the hours
plt.figure(figsize=(10, 5))
plt.plot(cumulative_volume, label="AVAT")
plt.plot(c_cumulative_volume, label="RECENT")
plt.xlabel("Hours")
plt.ylabel("Cumulative Volume")
plt.title(f"{get_ticker} AVAT {get_days_range} days")
plt.legend()
plt.figtext(0.5, -0.05, f"Percentage change is {percentage_change:.2f}%", ha="center", fontsize=10, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
plt.grid()
plt.show()