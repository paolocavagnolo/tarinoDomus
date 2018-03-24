import serial
import time

s = serial.Serial('/dev/ttyUSB0', 115200)


while (True):
  s.write(100)
  time.sleep(5)
  s.write(90)
  time.sleep(5)