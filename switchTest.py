# coding=utf-8
#!/usr/bin/env python

import spidev
import time
import sys
import RPi.GPIO as GPIO
from MCP23S17 import MCP23S17 as SW

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000000

sw = SW(spi, 7)

if __name__ == "__main__":
	sw.initialise()
	try:
		while True:
			switches = '{0:08b}'.format(sw.readSwitches())
			switches = switches.replace('1', '\033[92m*').replace('0', '\033[91m0')
			print '\033[92mSwitches: ', switches, '\r', 
			sys.stdout.flush()
	except KeyboardInterrupt:
		sw.close()
		spi.close()
