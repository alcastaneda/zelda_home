#!/usr/bin/python2

from phue import Bridge
import random
import time
import os

hue = os.environ.get('HUE_API')

def connect():
    b = Bridge(hue)
    b.connect()
    b.get_api()
    lights = b.get_light_objects('id')
    return lights

lights= connect()

yellow = 12750
green = 25500
blue=47000
purple = 52800
red = 65200
white = 35000

def change_color(color, bulb):
    lights[bulb].hue = color
    
def change_color_all(colors=[red],lights=range(1,4)):
    for light in lights:
        if len(colors) == len(lights):
            for color in colors:
                print(random.sample(colors,1))
                # change_color(color,light)
        else:
            for light in lights:
                change_color(random.sample(colors,1)[0], light)
    
#change_color(blue,1)
'''
for i in range(1,100,1):
    for i in [1,2,3]:
        lights[i].hue = blue
        time.sleep(1)
        lights[i].hue = 100
        time.sleep(1)
'''
# change_color_all([blue])
