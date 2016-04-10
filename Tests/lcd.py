#from: http://tutorials-raspberrypi.de/text-auf-16x2-zeichen-lcd-display-anzeigen-hd44780/
#!/usr/bin/python
import time
import RPi.GPIO as GPIO

# Zuordnung der GPIO Pins (ggf. anpassen)
LCD_RS = 4
LCD_E = 17
LCD_DATA4 = 18
LCD_DATA5 = 22
LCD_DATA6 = 23
LCD_DATA7 = 24

LCD_WIDTH = 16 		# Zeichen je Zeile
LCD_LINE_1 = 0x80 	# Adresse der ersten Display Zeile
LCD_LINE_2 = 0xC0 	# Adresse der zweiten Display Zeile
LCD_CHR = GPIO.HIGH
LCD_CMD = GPIO.LOW
E_PULSE = 0.0005
E_DELAY = 0.0005


def lcd_send_byte(bits, mode):
    GPIO.output(LCD_RS, mode)
    GPIO.output(LCD_DATA4, GPIO.LOW)
    GPIO.output(LCD_DATA5, GPIO.LOW)
    GPIO.output(LCD_DATA6, GPIO.LOW)
    GPIO.output(LCD_DATA7, GPIO.LOW)

    if bits & 0x10 == 0x10:
        GPIO.output(LCD_DATA4, GPIO.HIGH)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_DATA5, GPIO.HIGH)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_DATA6, GPIO.HIGH)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_DATA7, GPIO.HIGH)

    time.sleep(E_DELAY)
    GPIO.output(LCD_E, GPIO.HIGH)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, GPIO.LOW)
    time.sleep(E_DELAY)
    GPIO.output(LCD_DATA4, GPIO.LOW)
    GPIO.output(LCD_DATA5, GPIO.LOW)
    GPIO.output(LCD_DATA6, GPIO.LOW)
    GPIO.output(LCD_DATA7, GPIO.LOW)

    if bits & 0x01 == 0x01:
        GPIO.output(LCD_DATA4, GPIO.HIGH)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_DATA5, GPIO.HIGH)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_DATA6, GPIO.HIGH)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_DATA7, GPIO.HIGH)

    time.sleep(E_DELAY)
    GPIO.output(LCD_E, GPIO.HIGH)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, GPIO.LOW)
    time.sleep(E_DELAY)


def display_init():
    lcd_send_byte(0x33, LCD_CMD)
    lcd_send_byte(0x32, LCD_CMD)
    lcd_send_byte(0x28, LCD_CMD)
    lcd_send_byte(0x0C, LCD_CMD)
    lcd_send_byte(0x06, LCD_CMD)
    lcd_send_byte(0x01, LCD_CMD)


def pins_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_DATA4, GPIO.OUT)
    GPIO.setup(LCD_DATA5, GPIO.OUT)
    GPIO.setup(LCD_DATA6, GPIO.OUT)
    GPIO.setup(LCD_DATA7, GPIO.OUT)


def lcd_message(message):
    message = message.ljust(LCD_WIDTH, " ")
    for i in range(LCD_WIDTH):
        lcd_send_byte(ord(message[i]), LCD_CHR)


def clear_line(line):
    lcd_send_byte(line, LCD_CMD)


def clear_display():
    clear_line(LCD_LINE_1)
    lcd_message("")
    clear_line(LCD_LINE_2)
    lcd_message("")