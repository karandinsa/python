import serial
 

port = "COM5"
ser = serial.Serial(port)
ser.baudrate=115200
while True :
  line = ser.readline()
  print(line)
#ser.close()
#print('Найден последовательный порт:')

