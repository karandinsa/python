import serial, time
#flcd = open('lcd_api.py','r')
flcd = open("lcd_api.py").read().splitlines()
port = "COM5"
ser = serial.Serial(port)
ser.baudrate=115200
time.sleep(1)
ser.write(b"f=open('boot.py','w')\r\n")
ser.write(b"f.readlines('ok\n')\r\n")
ser.write(b"f.write('ok\n')\r\n")
lcstr1='f.write("'
lcstr2='\n")\n\r'   
for line in flcd:
        lstr=lcstr1+line+lcstr2
        lw=lstr.encode()
#        ser.write(lw)
#        ser.write(b'f.seek(0,2)\n\r')
time.sleep(1)
ser.write(b"f.close()\r\n")
ser.close()