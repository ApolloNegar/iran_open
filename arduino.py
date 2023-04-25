import serial
import time


serial_1 = serial.Serial("COM6", 9600)
serial_1.timeout = 1

while True:
    i = input("off/on: ")
    print(i)
    if i =='done':
        print("finished program")
        break

    serial_1.write(i.encode())
    time.sleep(0.5)
    print(serial_1.readline().decode('ascii'))

serial_1.close()