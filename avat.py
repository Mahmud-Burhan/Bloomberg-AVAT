# AVAT Function inspired from Bloomberg Terminal
# Replicated by: Mahmud bin Burhanudin (github.com/Mahmud-Burhan)
# Date: 2024-01-07
# Version: 2.0.0

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime

get_ticker = str(input("Enter ticker: "))
get_days_range = int(input("Enter days range: (any integer 1-730) "))
# Valid days range refer https://www.qmr.ai/yfinance-library-the-definitive-guide/

ticker = yf.Ticker(get_ticker).history(period=f"{get_days_range + 1}d", interval="1h")
if ticker.empty:
    raise Exception("Ticker not found")
ticker = ticker.drop(columns=['Dividends', 'Stock Splits'])

recent_date = datetime.now().strftime('%Y-%m-%d')
weekday = datetime.today().weekday()
time = datetime.now().strftime('%H:%M:%S')
 # 9:30 AM EST where the market opens, CHANGE ACCORDING TO YOUR TIMEZONE AND DAYLIGHT SAVING
MARKET_OPEN = "14:30:00" # THIS IS 2:30 PM GMT (UK TIME)
# If the day is Saturday or Sunday or Monday and market doesnt open yet, get the Friday's date
# else if the time is before the market opens, get the previous day's date
if weekday >= 5 or (weekday == 0 and time < MARKET_OPEN):
    day_to_subtract = weekday - 4
    if weekday == 0:
        day_to_subtract = 3
    recent_date = (datetime.now() - pd.Timedelta(days=day_to_subtract)).strftime('%Y-%m-%d')
elif time < MARKET_OPEN:
    recent_date = (datetime.now() - pd.Timedelta(days=1)).strftime('%Y-%m-%d')
recent_date = recent_date + " 00:00:00"

mod_ticker = ticker.loc[:recent_date].copy()
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

comparison_ticker = ticker[recent_date:] # get recent data
comparison_ticker["Cum_Volume"] = comparison_ticker['Volume'].cumsum() # get the cumulative volume

c_cumulative_volume = comparison_ticker["Cum_Volume"].tolist() # convert to list

hour_to_compare = len(c_cumulative_volume) - 1
percentage_change = (c_cumulative_volume[hour_to_compare] - cumulative_volume[hour_to_compare]) / cumulative_volume[hour_to_compare] * 100

# plot the cumulative volume against the hours
plt.figure(figsize=(10, 5))
plt.plot(range(len(cumulative_volume)), cumulative_volume, label="AVAT")
plt.plot(range(len(c_cumulative_volume)), c_cumulative_volume, label=f"""Recent {datetime.strptime(recent_date, '%Y-%m-%d %H:%M:%S').strftime('%A')}""")
plt.xlabel("Hours (PM, GMT)")
# Convert the hours to time
hour_as_time = ["3:30", "4:30", "5:30", "6:30", "7:30", "8:30", "Close"]
plt.xticks(range(len(cumulative_volume)), hour_as_time)
plt.ylabel("Cumulative Volume")
plt.title(f"{get_ticker} AVAT {get_days_range} days")
plt.legend()
plt.figtext(0.5, -0.05, f"Percentage change is {percentage_change:.2f}%", ha="center", fontsize=10, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
plt.grid()
plt.show()
