# coding=utf-8
#!/usr/bin/env python

import time
import serial
import spidev
from MAX31855 import MAX31855

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.flush()

bRUN = True

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000000

T = MAX31855(spi, 11, 12)

# Based on http://reprap.org/wiki/G-code

if __name__ == "__main__":
	desT0 = 0.0
	desT1 = 0.0
	desTBed = 0.0
	tool = 0
	isIncremental = False
	isMetric = True
	while bRUN:
		try:
			T0, iT0 = T.read(0)
			T1, iT1 = T.read(1)
			TBed = iT0
			line = ser.readline()
			if len(line)>1:
				cmds = line[:-1].split(' ')
				if cmds[0] == 'G90':
					isIncremental = False
				elif cmds[0] == 'G91':
					isIncremental = True
				elif cmds[0] == 'M27':
					ser.write("idle\n")
				elif cmds[0] == 'M104':
					if cmds[1] == 'T0' and cmds[2][0] == 'S':
						desT0 = float(cmds[2][1:])
					if cmds[1] == 'T1' and cmds[2][0] == 'S':
						desT1 = float(cmds[2][1:])
				elif cmds[0] == 'M105':
					ser.write("ok T0:{0:0.2f} /{1:0.2f} T1:{2:0.2f} /{3:0.2f} B:{4:0.2f} /{5:0.2f} @:0\n".format(T0, desT0, T1, desT1, TBed, desTBed))
				elif cmds[0] == 'M115':
					ser.write("ok PROTOCOL_VERSION:0.1 FIRMWARE_NAME:pyGCODE FIRMWARE_URL:http%3A//github.com/rmamba/gcode MACHINE_TYPE:troublemaker EXTRUDER_COUNT:2")
				elif cmds[0] == 'M140':
					desTBed = float(cmds[1][1:])
				elif cmds[0][0] == 'T':
					tool = int(cmds[0][1:])
				else:
#					print 'Line: ', line[:-1]
					print cmds
			time.sleep(.25)
		except KeyboardInterrupt:
			ser.close()
