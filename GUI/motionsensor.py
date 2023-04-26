
import serial
import time

def getSleepMode():
    porta = serial.Serial(port= "/dev/ttyS0", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
    data = porta.readline()
    sleepmode = 0
    print(data)
    print(" ")
    print("The data is", data) # still only need bit
    if(data == b'GPIO4_value: 0 \n'):
        sleepmode = 1
        time.sleep(5)
    elif (data == b'GPIO4_value: 1 \n'):
        sleepmode = 0
   
        
    return sleepmode
    


