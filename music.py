import pygame.mixer
from pygame.mixer import Sound
import time

pygame.mixer.init(32000)

songs=["Music/OOT_Song_Correct.wav", "Music/epona.wav", "Music/fire.wav",
		"Music/forest.wav", "Music/navi.wav", "Music/saria.wav",
		"Music/storms.wav", "Music/sun.wav", "Music/time.wav", "Music/zelda.wav"]

def play_song(song):
	s =Sound(song)
	s.play()
	time.sleep(s.get_length())