import time, serial
 
ser = serial.Serial("COM5")
ser.baudrate = 115200
 
filename = 'test.py'
 
f = open(filename, 'w')
while True :
	line = ser.readline()
	f.write(line)
	print line
