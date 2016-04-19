#!/usr/bin/env python
#
# Kenwood Morse Beacon - turns a Kenwood TS-480 into a heli beacon
#
# Copyright (C) 2016 by Mir Rodriguez <mir.rodriguez@greenpeace.org>
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
MY Esperanza heli beacon
Turns the Kenwood TS-480 into a morse code NDB 
Works with a Bendix King KR87m which goes up to 1799. Kenwood can transmit from 1705 kHz
Transmits the ship's call sign in CW in a loop for a defined period
Connect the TS-480 to serial port
usage: python heli_beacon.py {timer in minutes}
Example: python heli_beacon.py 30

by mir - written on the Indian Ocean 2016.04.19
"""

from __future__ import print_function
import serial
import sys
import time
import os

serialport = '/dev/ttyUSB0'
serialspeed = 38400
freq = '1711' # Beacon frequency in KHz - remember to tune antenna first!
power = '10' # Transmitter Power in W
callsign = 'PD6464'

ser = serial.Serial(serialport, serialspeed, timeout=1)

def stopbeacon():
	ser.write('KY' + (' ' * 25) + ';') # Clears morse cache and stops transmitting
	ser.write('PS9;\n') # Puts transceiver on standby
	ser.close()

def main(argv=None):

	if argv is None:
		argv = sys.argv
	timermins = sys.argv[1]
	timersecs = float(timermins) * 60

	start = time.time()

	print ('Beacon timer set to ' + str(timersecs) + ' seconds\n')

	print ('Callsign: ' + callsign + '\n')

	print ('Turning transceiver on\n')
		
	ser.write('PS;') # Checks transceiver power status
	status = ser.read(4)

	while status != 'PS1;': # Iterates until transceiver is on
		ser.write(';;;;PS1;\n') # Tries to turn transceiver on
		ser.write('PS;')
		status = ser.read(4)
	print ('Transceiver is on!\n')
	time.sleep(2) # Waits for transceiver to boot
	ser.write('FA0000' + freq + '000;') # sets frequency
	# s = 'Freq: '+ ser.read(2) + '\n'
	ser.write('AN1;') # sets antenna
	# s += 'Antenna: ' + ser.read(2) + '\n'
	ser.write('EX01300003;') # Sets sidetone volume
	# s += 'Sidetone:' + ser.read(2) + '\n'
	ser.write('KS010;') # Sets 10 words per minute
	#s += 'Speed:' + ser.read(2) + '\n'
	ser.write('PC0'+power+';') # Sets 10 KW power
	#s += 'Power:' + ser.read(2) + '\n'
	ser.write('MD3;') # Sets CW mode
	#s += 'Mode:' + ser.read(2) + '\n'
	# print (s) # uncomment these and above for debugging

	print ('Starting beacon\n')

	elapsed = int(time.time() - start)
	current = elapsed
	status = 'start'

	while elapsed < timersecs:
		ser.write('KY;')
		status = ser.read(4)
		elapsed = int(time.time() - start)
		remaining = str(elapsed - int(timersecs))
		print ('Timer: ' + remaining, end='s \r')
		if status == 'KY1;':
			continue
		ser.write('KY ' + ((callsign + ' ') * 3) + '   ;')
		response = ser.read(2)
		ser.write('KY;')
		status = ser.read(4)

	stopbeacon()

	print ('End beacon')

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
	        print ('\nInterrupted!')
		stopbeacon()
	        try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

