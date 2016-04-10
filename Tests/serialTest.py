import serial
import time

s = serial.Serial('/dev/ttyACM0', 9600)  # Namen ggf. anpassen
s.open()
time.sleep(5)  # der Arduino resettet nach einer Seriellen Verbindung, daher muss kurz gewartet werden

print("blubb")
s.write("test")
try:
    while True:
        response = s.readline()
        print("read")
        print(response)
        time.sleep(0.5)
except KeyboardInterrupt:
    s.close()