# coding=utf-8
#!/usr/bin/env python

import spidev
import time
import RPi.GPIO as GPIO
from MAX31855 import MAX31855 as TEMP

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000000
T = TEMP(spi, 11, 12)

if __name__ == "__main__":
	try:
		while True:
			T0, T0Internal = T.read(0)
			print 'T0: {0:7.2f}, {1:6.2f}'.format(T0, T0Internal)
			T1, T1Internal = T.read(1)
			print 'T1: {0:7.2f}, {1:6.2f}'.format(T1, T1Internal), 
			print '\033[2A'
			time.sleep(.25)
	except KeyboardInterrupt:
		temp.close()
		spi.close()
