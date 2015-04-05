# coding=utf-8
#!/usr/bin/env python

import time
import serial
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.flush()

bRUN = true

# Based on http://reprap.org/wiki/G-code

if __name__ == "__main__":
    while bRUN:
	line = ser.readline()
	if len(line)>1:
	    print 'Line: ', line[:-1]
	    cmds = line[:-1].split(' ')
	    print cmds
	    if cmds[0] == 'M27':
		ser.write("idle\n")
    	    if cmds[0] == 'M105':
		ser.write("ok T0:22.1 /-273.1 T1:45.1 /-273.1 B:21.3 /-273.1 @:0\n")
	    if cmds[0] == 'M115':
		ser.write("ok PROTOCOL_VERSION:0.1 FIRMWARE_NAME:pyGCODE FIRMWARE_URL:http%3A//github.com/rmamba/gcode MACHINE_TYPE:troublemaker EXTRUDER_COUNT:2")
	time.sleep(.25)
    ser.close()