# coding=utf-8
#!/usr/bin/env python

import spidev
import time
import RPi.GPIO as GPIO
from MAX31855 import MAX31855 as TEMP

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000000
temp = TEMP(spi, 11, 12)

if __name__ == "__main__":
	try:
		while True:
			print 'T0: ', temp.readT(0)
			print 'T1: ', temp.readT(1)
			time.sleep(.25)
	except KeyboardInterrupt:
		spi.close()
