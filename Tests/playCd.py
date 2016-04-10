import pygame
import os
import serial
import atexit
import sys
import lcd
import datetime
from time import sleep

READY = "READY"

_s = serial.Serial('/dev/ttyACM0', 115200)
_files = []
_file_names = []
_current = 0
_current_volume = 0
_timer = 0
_current_displayed = ""


def cleanup():
    lcd.clear_display()
    pygame.quit()
    _s.write("disconnected")
    _s.close()
    sys.exit()


def init_cleanup():
    atexit.register(cleanup)


def init_serial():
    _s.open()


def init_display():
    pygame.display.init()
    pygame.display.set_mode((320, 240))


def init_mixer():
    pygame.mixer.init(48000, -16, 1, 1024)


def get_song_time():
    return pygame.mixer.music.get_pos()


def get_song_title():
    return _file_names[_current]


def send_ready():
    global _current_displayed

    if _current_displayed != READY:
        _current_displayed = READY
        lcd.clear_line(lcd.LCD_LINE_1)
        lcd.lcd_message("Ich bin bereit!")
        lcd.clear_line(lcd.LCD_LINE_2)
        lcd.lcd_message("Leg los!")


def send_time():
    global _current_displayed

    time = get_song_time()
    d = datetime.timedelta(milliseconds=time)
    time = str(d)[2:-7]
    if _current_displayed != time:
        _current_displayed = time

        if time != -1:
            lcd.clear_line(lcd.LCD_LINE_1)
            lcd.lcd_message(time)
            lcd.clear_line(lcd.LCD_LINE_2)
            lcd.lcd_message("")


def send_title():
    global _current_displayed

    if len(_file_names) != 0:
        title = get_song_title().split(".mp3")[0]

        if _current_displayed != title:

            _current_displayed = title
            if len(title) > 16:
                title_first = title[:15]
                title_second = title[16:len(title)]

                lcd.clear_line(lcd.LCD_LINE_1)
                lcd.lcd_message(title_first)
                lcd.clear_line(lcd.LCD_LINE_2)
                lcd.lcd_message(title_second)
            else:
                lcd.clear_line(lcd.LCD_LINE_1)
                lcd.lcd_message(title)
                lcd.clear_line(lcd.LCD_LINE_2)
                lcd.lcd_message("")


def set_volume():
    global _current_volume

    if _current_volume < 0:
        _current_volume = 0
    if _current_volume > 1:
        _current_volume = 1

    pygame.mixer.music.set_volume(_current_volume)

    _s.write(str(_current_volume).encode())


def volume_up():
    global _current_volume

    _current_volume = pygame.mixer.music.get_volume() + 0.2

    set_volume()


def volume_down():
    global _current_volume

    _current_volume = pygame.mixer.music.get_volume() - 0.2

    set_volume()


def set_key_events():
    pygame.event.set(pygame.constants.KEYDOWN)


def set_end_event():
    pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)


def play(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    set_end_event()


def next_song():
    global _current

    if _current == len(_files) - 1:
        _current = 0
    else:
        _current += 1

    play(_files[_current])


def previous_song():
    global _current

    if _current == 0:
        _current = len(_files) - 1
    else:
        _current -= 1

    play(_files[_current])


def load_playlist(playlist):
    global _files, _file_names

    _files = []
    _file_names = []

    for file in os.listdir("/home/pi/music/" + playlist):
        _files.append("/home/pi/music/" + playlist + "/" + file)
        _file_names.append(file)

    _file_names.sort()
    _files.sort()


def start_player():
    global _current

    _current = 0

    play(_files[_current])


def pause():
    pygame.mixer.music.pause()


def unpause():
    pygame.mixer.music.unpause()


def stop():
    pygame.mixer.music.stop()


def quit_pygame():
    pygame.mixer.quit()


def check_for_serial_input():
    response = str(_s.readline())

    mode = response[:1]
    value = response[1:]

    if mode == "-":
        return

    try:
        value = int(value)
    except:
        return

    if mode == "s":
        stop()
        return

    if mode == "t" or mode == "b":
        playlist = mode + "/" + str(value)

        load_playlist(playlist)
        start_player()

        return

    if len(_files) < 1:
        return

    if mode == "g":
        if value == 0:
            unpause()
        if value == 1:
            pause()
        if value == 2:
            next_song()
        if value == 3:
            previous_song()
        if value == 4:
            volume_up()
        if value == 5:
            volume_down()


def update_lcd():
    global _timer

    if pygame.mixer.music.get_busy():
        if _timer > 30:
            if _timer > 60:
                _timer = 0
            send_time()
        else:
            send_title()
        _timer += 1
    else:
        _timer = 0
        send_ready()


def init_lcd():
    lcd.pins_init()
    lcd.display_init()


def check_for_event():
    events = pygame.event.get()
    if events:
        for event in events:
            if event.type == pygame.USEREVENT and event.code == 0:
                next_song()


def init():
    global _current_volume

    init_lcd()
    init_cleanup()
    init_serial()
    init_display()
    init_mixer()

    _s.write("connected")

    sleep(3)

    _current_volume = pygame.mixer.music.get_volume()
    set_volume()


def loop():
    while True:
        update_lcd()
        check_for_serial_input()
        check_for_event()


init()
loop()