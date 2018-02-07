import pygame
import pygame.mixer
from pygame.mixer import Sound
import time

pygame.mixer.init(32000)
confirm=Sound("Music/zelda.wav")
# confirm=Sound("Music/OOT_Song_Correct.wav")

print("u")
confirm.play()
time.sleep (15)
# pygame.init()

# pygame.mixer.init()

# pygame.mixer.music.load("Music/OOT_Song_Correct.wav")
# pygame.mixer.music.play()
