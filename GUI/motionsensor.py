import serial

def getSleepMode():
    porta = serial.Serial(port="/dev/ttyS0", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
    data = porta.readline()
    print("The data is", data)
    return data