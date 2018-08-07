import serial, time
 

port = "COM5"
ser = serial.Serial(port)
ser.baudrate=115200
time.sleep(2)
ser.write(b"f=open('boot_com.py','w')\r\n")
ser.write(b"f.write('ok1')\r\n")
ser.write(b"f.close()\r\n")
ser.close()
#ser.close()
#print('Найден последовательный порт:')

