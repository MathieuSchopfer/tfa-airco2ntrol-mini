#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2021  Mathieu Schopfer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
from datetime import datetime
import os.path
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates

_warning_threshold = 600
_danger_threshold = 800

parser = argparse.ArgumentParser(description='Plot a CO2 data set')
parser.add_argument('file', type=str, help='file containing the data to plot')
args = parser.parse_args()

data = pd.read_csv(args.file, usecols=['Time', 'CO2[ppm]'], converters={'Time': datetime.fromisoformat}, index_col='Time', comment='#')

# Plot line
data.plot(ylabel='CO2 [ppm]', legend=False, color='black', linewidth=2)
ymax_default = 1000
co2max = data['CO2[ppm]'].max()
ysup = ymax_default if co2max < ymax_default-150 else co2max+150
plt.ylim(300, ysup)

# Add background colours
plt.axhspan(0, _warning_threshold, color='tab:green', alpha=0.5)
plt.axhspan(_warning_threshold, _danger_threshold, color='tab:orange', alpha=0.5)
plt.axhspan(_danger_threshold, 3000, color='tab:red', alpha=0.5)  # 3000 ppm is the device measurement limit

# Customize
parts = os.path.splitext(os.path.basename(args.file))[0].split('_')
info = ' '.join(parts[:-1])
date = datetime.fromisoformat(parts[-1]).date().isoformat()
plt.title(f'{info} - {date}')
plt.gca().get_xaxis().set_major_formatter(dates.DateFormatter('%H:%M'))
plt.grid(color='whitesmoke', linestyle=':', linewidth=1)

plt.tight_layout()
plt.show()
