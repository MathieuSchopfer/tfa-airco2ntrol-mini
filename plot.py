import argparse
from datetime import datetime
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates

_warning_threshold = 600
_danger_threshold = 800


parser = argparse.ArgumentParser(description='Plot a CO2 data set')
parser.add_argument('file', type=str, help='file containing the data to plot')

args = parser.parse_args()

data = pd.read_csv(args.file, usecols=['Time', 'CO2[ppm]'], converters={'Time': datetime.fromisoformat}, index_col='Time')

# Plot line
data.plot(ylabel='CO2 [ppm]', legend=False, color='black', linewidth=2)
ymax_default = 1000
ysup = ymax_default if data['CO2[ppm]'][-1] < ymax_default else data['CO2[ppm]'][-1]+100
plt.ylim(0, ysup)

# Add background colours
plt.axhspan(0, _warning_threshold, color='tab:green', alpha=0.5)
plt.axhspan(_warning_threshold, _danger_threshold, color='tab:orange', alpha=0.5)
plt.axhspan(_danger_threshold, 3000, color='tab:red', alpha=0.5)  # 3000 ppm is the device measurement limit

plt.gca().get_xaxis().set_major_formatter(dates.DateFormatter('%H:%M'))
plt.grid(color='whitesmoke', linestyle=':', linewidth=1)
plt.show()
