# -*- coding: utf-8 -*-

# Copyright (C) 2021-2023  Mathieu Schopfer
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

import sys, time, hid

__author__ = 'Mathieu Schopfer'
__version__ = '1.0.0'


_watchers = []
_device = None


def _read_data():
    """Read current data from device. Return only when the whole data set is ready.

    Returns:
        float, float, float: time [Unix timestamp], co2 [ppm], and temperature [°C]
    """

    # It takes multiple reading from the device to read both co2 and temperature
    co2 = t = None
    while(co2 is None or t is None):

        try:
            data = list(_device.read(8, 10000))  # Times out after 10 s to avoid blocking permanently the thread
        except KeyboardInterrupt:
            _exit()
        except OSError as e:
            print('Could not read the device, check that it is correctly plugged:', e)
            _exit()

        key = data[0]
        value = data[1] << 8 | data[2]
        if (key == 0x50):
            co2 = value
        elif (key == 0x42):
            t = value / 16.0 - 273.15

    return time.time(), co2, t


def _exit():
    print('\nExiting ...', file=sys.stderr)
    _device.close()
    sys.exit(0)

def open_device():
    """Prepare the device."""

    global _device

    vendor_id=0x04d9
    product_id=0xa052
    _device = hid.device()
    _device.open(vendor_id, product_id)
    _device.send_feature_report([0x00, 0x00])  # Don't understand why we should send two 0 to put the device in read mode ...


def register_watcher(callback):
    """Add a callback function that will be called when a new data set from the device is ready.
    
    See also :func:watch
    """

    _watchers.append(callback)


def watch(interval=10):
    """Watch the device and call all the callbacks registered with :func:register_watcher once the device returns a data set.

    Parameters:
        delay (int): Data acquisition interval in seconds.
    """

    global _device, _watching

    if _device is None:
        open_device()

    _watching = True
    while True:
        t, co2, temperature = _read_data()
        for w in _watchers:
            w(t, co2, temperature)
        # Wait until reading further data and handle keyboard interruptions gracefully
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            _exit()
