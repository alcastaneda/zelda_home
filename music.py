import pygame.mixer
from pygame.mixer import Sound
import time

pygame.mixer.init(32000)
confirm=Sound("Music/zelda.wav")


confirm.play()

time.sleep(confirm.get_length())


	