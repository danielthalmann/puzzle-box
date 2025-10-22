import pygame
import os
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

pygame.mixer.init()


def play_sound(path):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    pygame.mixer.music.load(path)
    pygame.mixer.music.play(loops=-1)


play_sound('sound/relaxing.mp3')

while(True) :
    x = 1
