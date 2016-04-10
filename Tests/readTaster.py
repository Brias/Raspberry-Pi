import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)

count = 0

try:
    while True:
        input_value = GPIO.input(24)
        if input_value:
            count += 1
            print("Taster" + count + "Mal gedrückt")
        time.sleep(.01)
except KeyboardInterrupt:
    print("Programm canceled manually")
except:
    print("Unexpected Error Occured!")
finally:
    GPIO.cleanup()
    exit()
