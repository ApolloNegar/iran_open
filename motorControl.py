import serial
import time

serial_1 = serial.Serial("COM6", 9600)
serial_1.timeout = 1

def send_serial(angle):
    serial_1.write(angle.encode())
    time.sleep(0.5)
    print(serial_1.readline().decode('ascii'))


print(serial_1.readline().decode('ascii'))

serial_1.close()