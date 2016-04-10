import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

p = GPIO.PWM(23, 50)
p.start(0)

try:
    while True:
        for dc in range(0, 100, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.05)
        for dc in range(100, 0, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.05)
except KeyboardInterrupt:
    print("Program canceled manually")
except:
    print("Unexpected Error occurred!")
finally:
    GPIO.cleanup()
    exit()