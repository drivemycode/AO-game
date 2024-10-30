import pygame, time
pygame.mixer.init()
pygame.mixer.music.load('file.midi')
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    print('Still playing :)')
    time.sleep(1)
