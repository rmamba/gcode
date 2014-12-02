# coding=utf-8
#!/usr/bin/env python

import time
import serial
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.flush()

if __name__ == "__main__":
    while True:
	line = ser.readline()
	if len(line)>1:
	    print 'Line: ', line[:-1]
	    cmds = line[:-1].split(' ')
	    print cmds
	    if cmds[0] == 'M27':
		ser.write("idle\n")
    	    if cmds[0] == 'M105':
		ser.write("ok T0:22.1 /-273.1 T1:45.1 /-273.1 B:21.3 /-273.1 @:0\n")
	time.sleep(.25)
    ser.close()