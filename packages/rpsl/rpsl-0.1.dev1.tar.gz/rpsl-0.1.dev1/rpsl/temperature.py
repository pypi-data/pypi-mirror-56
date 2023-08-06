#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read temperature on a RaspberryPi with a DS18B20.

This module is based on
https://github.com/simonmonk/raspberrypi_cookbook_ed2/blob/master/temp_DS18B20.py

See also
--------

"The Raspberry Pi Cookbook" by Simon Monk Ed. Oreilly recipe 12.9 (1st edition)
"""

import datetime
import glob    # Unix style pathname pattern expansion
import time

SLEEP_TIME = 1


def _get_raw_data():
    '''Get raw data'''

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    # print(device_file)

    with open(device_file, 'r') as fd:
        lines = fd.readlines()

    return lines

 
def get_temperature_degree_celsius():
    '''Get formatted data'''

    lines = _get_raw_data()

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = _get_raw_data()

    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0

        return temp_c


def get_temperature_degree_fahrenheit():
    '''Get formatted data'''

    temp_c = get_temperature_degree_celsius()
    temp_f = temp_c * 9.0 / 5.0 + 32.0

    return temp_f

        
def log_temperature():
    '''Log data'''

    while True:
        dt = datetime.datetime.now().isoformat()
        temperature_c = get_temperature_degree_celsius()
        print("{} {:%f}°C".format(dt, temperature_c))
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    log_temperature()
