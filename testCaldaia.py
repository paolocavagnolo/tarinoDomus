import serial
import time

s = serial.Serial('/dev/ttyUSB0', 115200)


while (True):
  s.write('R100\0'.encode())
  s.flush()
  time.sleep(5)
  s.write('R90\0'.encode())
  s.flush()
  time.sleep(5)