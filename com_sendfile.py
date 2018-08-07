import serial, time
#flcd = open('lcd_api.py','r')
flcd = open("lcd_api.py").read().splitlines()
print(flcd)
port = "COM8"
ser = serial.Serial(port)
ser.baudrate=115200
time.sleep(1)
ser.write(b"f=open('l.py','w')\r\n")
lcstr1="f.write('"
lcstr2="\n')\r\n"   
ser.write("f.write('ok\n')\r".encode())
ser.write(b"f.write('ok\n')\r\n")
for line in flcd:
        lstr=lcstr1+line+lcstr2
        ser.write(lstr.encode())
        ser.write(b'f.seek(0,2)\n\r')
time.sleep(1)
ser.write(b"f.close()\n\r")
ser.write(b"f=open('l.py','r')\r\n")
ser.write(b"f.readlines()\r\n")
while True:
        print(ser.readline().decode())
ser.close()


