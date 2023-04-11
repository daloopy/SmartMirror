import serial

def getSleepMode():
    porta = serial.Serial(port= "/dev/ttyS0", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
    data = porta.readline().decode()
    print(" ")
    print("The data is", data) # still only need bit
    if(data == "GPIO4_value: 0 \n"):
        sleepmode = 1
    else:
        sleepmode = 0
        
    return sleepmode
    


