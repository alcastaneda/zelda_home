import pygame.mixer
from pygame.mixer import Sound
import time

pygame.mixer.init(32000)

def play_song(song):
	s =Sound(song)
	s.play()
	time.sleep(s.get_length())