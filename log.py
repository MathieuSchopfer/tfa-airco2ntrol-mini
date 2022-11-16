#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2022  Petr Špaček
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
import airco2ntrol_mini as aco2m

if __name__ == "__main__":

    try:
        aco2m.open_device()
    except OSError as e:
        print("Could not open the device, check that it is correctly plugged:", e)
    else:

        def logger(t, co2, temperature):
            _t = datetime.fromtimestamp(t)
            timestamp = _t.isoformat(timespec="seconds")
            print(f"{timestamp:s},{co2:.0f},{temperature:.1f}", flush=True)

        aco2m.register_watcher(logger)
        aco2m.watch()
