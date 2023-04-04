import serial

def getRange():
    ser = serial.Serial('/dev/ttyS0')  # Replace with the correct port for your UART connection
    ser.baudrate = 9600  # Set the baud rate to match your ESP32

    inRange = ser.readline().decode().strip()  # Read the data from the serial port
    print(f'inRange: {inRange}')  # Print the data to the console (for testing)
    # Add code here to update your GUI with the value of inRange       
