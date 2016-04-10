def check_for_key_pressed():
    press = pygame.key.get_pressed()

    if press[pygame.K_DOWN] != 0:
        volume_down()
        sleep(.5)
    if press[pygame.K_UP] != 0:
       volume_up()
       sleep(.5)
    if press[pygame.K_RIGHT] != 0:
       next_song()
       sleep(.5)
    if press[pygame.K_LEFT] != 0:
       previous_song()
       sleep(.5)
    if press[pygame.K_u] != 0:
        pygame.mixer.music.unpause()
        sleep(.5)
    if press[pygame.K_p] != 0:
        pygame.mixer.music.pause()
        sleep(.5)
    if press[pygame.K_s] != 0:
        pygame.mixer.music.stop()
        global _current
        _current = 0

        quit_pygame()

        sleep(.5)
    if press[pygame.K_r] != 0:
        play(_files[_current])
        sleep(.5)
    if press[pygame.K_1] != 0:
        init()
        load_playlist("playlist1")
        start_player()
    if press[pygame.K_2] != 0:
        init()
        load_playlist("playlist2")
        start_player()
    if press[pygame.K_3] != 0:
        init()
        load_playlist("playlist3")
        start_player()