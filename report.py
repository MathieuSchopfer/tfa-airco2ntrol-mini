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


from datetime import datetime
import time
from matplotlib import pyplot as plt
import numpy as np
import airco2ntrol_mini as aco2m


_co2_line = None
_last_point = None
_plot_range = 1800  # Plot range in seconds
_warning_threshold = 800
_danger_threshold = 1200


def _format_axis_time(t, pos=None):
    return datetime.fromtimestamp(t).strftime('%H:%M')


def update_plot(t, co2, _):
    timestamps = np.append(_co2_line.get_xdata(), t)
    co2s = np.append(_co2_line.get_ydata(), co2)

    # Remove data out of plot time range
    k = np.flatnonzero(timestamps[-1]-timestamps < _plot_range)
    timestamps = timestamps[k]
    co2s = co2s[k]

    xsup = timestamps[0]+_plot_range if timestamps[-1]-timestamps[0] < _plot_range else timestamps[-1]
    plt.xlim(timestamps[0], xsup)

    ymax_default = 1500
    ysup = ymax_default if co2s[-1] < ymax_default else co2s[-1]+100
    plt.ylim(0, ysup)

    _co2_line.set_xdata(timestamps)
    _co2_line.set_ydata(co2s)
    _last_point.set_xdata([t])
    _last_point.set_ydata([co2])

    fig = plt.gcf()
    fig.canvas.draw()
    fig.canvas.flush_events()


if __name__ == '__main__':

    try:
        aco2m.open_device()
    except OSError as e:
        print('Could not open the device, check that it is correctly plugged:', e)
    else:
        # Create log file
        timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')
        fileName = f'./airco2ntrol_{timestamp}.csv'
        with open(fileName, 'at', encoding='UTF-8', errors='replace', buffering = 1) as logFile:

            # CSV logging
            def logger(t, co2, temperature):

                # Log to file
                timestamp = datetime.fromtimestamp(t).strftime('%Y%m%dT%H%M%S')
                logFile.write(f'{timestamp:s},{co2:.0f},{temperature:.1f}\n')

                # Console output
                timestamp = datetime.fromtimestamp(t).strftime('%H:%M:%S')
                print(f'{timestamp:s}\t{co2:.0f} ppm\t\t{temperature:.1f} °C', end='\r')

            aco2m.register_watcher(logger)

            logFile.write('Time,CO2[ppm],Temperature[°C]\n')
            print('Time\t\tCO2\t\tTemperature')

            # Plotting
            aco2m.register_watcher(update_plot)
            plt.ion()  # Activate interactive plotting
            _co2_line, = plt.plot([], [], linewidth=2, color='tab:blue')  # Init line
            _last_point, = plt.plot([], [], marker='o', color='tab:blue')  # Init line

            # Add background colours
            plt.axhspan(0, _warning_threshold, color='limegreen', alpha=0.5)
            plt.axhspan(_warning_threshold, _danger_threshold, color='yellow', alpha=0.5)
            plt.axhspan(_danger_threshold, 3000, color='tomato', alpha=0.5)  # 3000 ppm is the device measurement limit

            # Customize look
            ax = plt.gca()
            ax.get_xaxis().set_major_formatter(_format_axis_time)
            plt.grid(color='lightgrey', linestyle=':', linewidth=1)
            plt.xlabel('Time')
            plt.ylabel('CO2 [ppm]')
            plt.title(f'CO2 concentration over the last {_plot_range/60:.0f} min')

            aco2m.watch()
