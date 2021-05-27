Cross-platform Python logger for TFA Dostmann Airco2ntrol Mini CO2 monitor (31.5006.02) relying on HIDAPI library.

# Prerequisites

This project needs:
 * Python 3
 * [HIDAPI library](https://github.com/libusb/hidapi)
 * [hidapi Python interface](https://pypi.org/project/hidapi/)

## Linux

See what package your distribution provides for the HIDAPI library.

## MacOS

The HIDAPI library may be easily installed on MacOS with Homebrew:
```shell
brew install hidapi
```

# Getting stared

Just run the logger script with:
```shell
python3 report.py
```

The script will create a log file `airco2ntrol_<date>T<time>.csv` and open a plotting window.

# Troubleshooting

## udev rules on Linux
If the script cannot access the device, update your system's udev rules as follow:

 1. Unplug the device
 2. Copy file `90-airco2ntrol_mini.rules` to `/etc/udev/rules.d`
 3. Reload the rules with `sudo udevadm control --reload-rules`
 4. Plug your device.

# Credits

Henryk Plötz was the first reverse engineer TFA Dotsmann CO2 monitors. Give a look at [his project](https://hackaday.io/project/5301-reverse-engineering-a-low-cost-usb-co-monitor).
