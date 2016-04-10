import RPi.GPIO as GPIO
import pygame.mixer
from time import sleep
from sys import exit

GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.IN)
GPIO.setup(4, GPIO.IN)
GPIO.setup(24, GPIO.IN)

pygame.mixer.init(48000, -16, 1, 1024)

sound_a = pygame.mixer.Sound("/home/pi/python_games/match0.wav")
sound_b = pygame.mixer.Sound("/home/pi/python_games/match1.wav")
sound_c = pygame.mixer.Sound("/home/pi/python_games/match2.wav")

sound_channel_a = pygame.mixer.Channel(1)
sound_channel_b = pygame.mixer.Channel(2)
sound_channel_c = pygame.mixer.Channel(3)

print("Soundboard bereit!")

try:
    while True:
        if GPIO.input(25):
            sound_channel_a.play(sound_a)
            sleep(.3)
        if GPIO.input(4):
            sound_channel_b.play(sound_b)
            sleep(.3)
        if GPIO.input(24):
            sound_channel_c.play(sound_c)
            sleep(.3)
        sleep(.01)
except KeyboardInterrupt:
    print("Programm canceled manually")
except:
    print("Unexpected Error Occured!")
finally:
    GPIO.cleanup()
    exit()