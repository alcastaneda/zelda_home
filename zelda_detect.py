#Tone detection shamelessly stolen from:
#https://benchodroff.com/2017/02/18/using-a-raspberry-pi-with-a-microphone-to-hear-an-audio-alarm-using-fft-in-python/
#Zelda song detection stolen from:
# https://github.com/Sufficiently-Advanced/ZeldaHomeAutomation
# Zelda songs downloaded from: http://www.zeldadungeon.net/Soundtracks-Ocarina-of-Time-Original-Soundtrack.php
#!/usr/bin/env python
import pyaudio
from numpy import zeros,linspace,short,fromstring,hstack,transpose,log
from scipy import fft
from time import sleep
from collections import deque
# import paho.mqtt.client as mqtt
# import requests
from lightsLib import *
from music import *

#change accordingly for your song confirmation sound file name/location
#mqtt stuff
# client = mqtt.Client()
# client.connect("localhost",1883,300)

#Volume Sensitivity, 0.05: Extremely Sensitive, may give false alarms
#             0.1: Probably Ideal volume
#             1: Poorly sensitive, will only go off for relatively loud
SENSITIVITY= 1.0

#Bandwidth for detection (i.e., detect frequencies within this margin of error of the TONE)
BANDWIDTH = 25

# Alarm frequencies (Hz) to detect (Use audacity to record a wave and then do Analyze->Plot Spectrum)
D4 = 630
E = 685
F = 755
G = 806
A = 890
B = 1000
D5 = 1175
#frequency ranges for each note
'''rangeD4 = range(D4-BANDWIDTH,D4+BANDWIDTH)
rangeE = range(E-BANDWIDTH,E+BANDWIDTH)
rangeF = range(F-BANDWIDTH,F+BANDWIDTH)
rangeG = range(G-BANDWIDTH,G+BANDWIDTH)
rangeA = range(A-BANDWIDTH,A+BANDWIDTH)
rangeB = range(B-BANDWIDTH,B+BANDWIDTH)
rangeD5 = range(D5-BANDWIDTH,D5+BANDWIDTH)'''
#These numbers work for my ocarina in my house with a blue yeti, ymmv
minD4 = D4-50
maxD4 = D4+BANDWIDTH
minE = E-BANDWIDTH
maxE = E+BANDWIDTH
minF = F-40
maxF = F+BANDWIDTH
minG = G-BANDWIDTH
maxG = G+BANDWIDTH
minA = A-BANDWIDTH
maxA = A+55
minB = B-BANDWIDTH
maxB = B+BANDWIDTH
minD5 = D5-BANDWIDTH
maxD5 = D5+BANDWIDTH

# Song note sequences
sun = deque(['A','E','D5','A','E','D5'])
time = deque(['A','D4','E','A','D4','E'])
storm = deque(['D4','E','D5','D4','E','D5'])
forest = deque(['D4','D5','B','A','B','A'])
saria = deque(['E','A','B','E','A','B'])
fire = deque(['E','D4','E','D4','A','E']) #This is just 6 notes, play all 8 if you want ;)
epona = deque(['D5','B','A','D5','B','A'])
zelda = deque(['B','D5','A','B','D5','A'])
heal = deque(['B','A','F','B','A','F'])
test = deque(['D4','F','A','B','D5','D4']) #Not a Zelda song, just nice to make sure everything's working
#heard note sequence deque
notes = deque(['G','G','G','G','G','G'], maxlen=6)

# Show the most intense frequency detected (useful for configuration)
frequencyoutput=True
freqNow = 1.0
freqPast = 1.0

#Set up audio sampler - 
NUM_SAMPLES = 2048 *4
SAMPLING_RATE = 44100 #make sure this matches the sampling rate of your mic!
pa = pyaudio.PyAudio()
_stream = pa.open(format=pyaudio.paInt16,
                  channels=1, rate=SAMPLING_RATE,
                  input=True,
                  frames_per_buffer=NUM_SAMPLES)

#print("Alarm detector working. Press CTRL-C to quit.")
lights =connect()
while True:
    while _stream.get_read_available()< NUM_SAMPLES: sleep(0.01)
    audio_data  = fromstring(_stream.read(
        _stream.get_read_available()), dtype=short)[-NUM_SAMPLES:]
    # Each data point is a signed 16 bit number, so we can normalize by dividing 32*1024
    normalized_data = audio_data / 32768.0
    intensity = abs(fft(normalized_data))[:NUM_SAMPLES/2]
    frequencies = linspace(0.0, float(SAMPLING_RATE)/2, num=NUM_SAMPLES/2)
    if frequencyoutput:
        which = intensity[1:].argmax()+1
        # use quadratic interpolation around the max
        if which != len(intensity)-1:
            y0,y1,y2 = log(intensity[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            freqPast = freqNow
            freqNow = (which+x1)*SAMPLING_RATE/NUM_SAMPLES
        else:
            freqNow = which*SAMPLING_RATE/NUM_SAMPLES
       # print "\t\t\t\tfreq=",freqNow,"\t",freqPast
    if minD4 <= freqPast <= maxD5 and abs(freqNow-freqPast) <= 25:
        if minA<=freqPast<=maxA and minA<=freqNow<=maxA and notes[-1]!='A':
            notes.append('A')
            print "You played A!"
        elif minF<=freqPast<=maxF and minF<=freqNow<=maxF and notes[-1]!='F':
            notes.append('F')
            print "You played F!"
        elif freqPast <= maxD4 and minD4 <= freqNow <= maxD4 and notes[-1]!='D4':
            notes.append('D4')
            print "You played D4!"
        elif minD5 <= freqPast <= maxD5 and minD5 <= freqNow <= maxD5 and notes[-1]!='D5':
            notes.append('D5')
            print "You played D5!"
        elif minB<=freqPast<=maxB and minB<=freqNow<=maxB and notes[-1]!='B':
            notes.append('B')
            print "You played B!"
        elif minE<=freqPast<=maxE and minE<=freqNow<=maxE and notes[-1]!='E':
            notes.append('E')
            print "You played E!"
        elif minG<=freqPast<=maxG and minG<=freqNow<=maxG and notes[-1]!='G':
            notes.append('G')
            print "You played G!"
        else:
            print "What the heck is that?"#prints when sound is in range but not identifiable as note
											#or when a note has already been registered and is "heard" again

# Lights
    if notes==sun:
        print "\t\t\t\tSun song!"
    	# client.publish("songID", "1") #1=Sun
    	_stream.stop_stream()
        play_song(songs[0])
        play_song(songs[7])
    	change_color_all([yellow,white])
    	notes.append('G')#append with 'G' to 'reset' notes, this keeps the song from triggering constantly
        _stream.start_stream()
    if notes==time:
        print "song of Time!"
    	# client.publish("songID", "2") #2=Time
    	_stream.stop_stream()
        play_song(songs[0])
        play_song(songs[8])
    	change_color_all([blue])
        notes.append('G')
        _stream.start_stream()
    if notes==storm:
        print "song of Storms!"
    	# client.publish("songID", "3") #3=Storm
    	play_song(songs[0])
        play_song(songs[6])
    	change_color_all([blue,purple])
    	notes.append('G')
        _stream.start_stream()
    if notes==forest:
        print "Minuet of Forest!"
    	# client.publish("songID", "4") #4=Forest
    	_stream.stop_stream()
        play_song(songs[0])
        play_song(songs[3])
    	change_color_all([green,yellow])
    	notes.append('G')
        _stream.start_stream()
    if notes==saria:
        print "Saria's song!" #5=Saria
    	_stream.stop_stream()
        # requests.post("https://maker.ifttt.com/trigger/YOUR_EVENT_NAME/with/key/YOUR_KEY")#You'll need your own Maker account and ifttt event
    	change_color_all([green])
    	notes.append('G')
    	play_song(songs[0])
        play_song(songs[5])
    	_stream.start_stream()
    if notes==fire:
        print "Bolero of fire!"
    	# client.publish("songID", "6") #6=Fire
    	_stream.start_stream()
        play_song(songs[0])
        play_song(songs[2])
    	change_color_all([red,yellow])
    	notes.append('G')
        _stream.start_stream()
    if notes==epona:
        print "Epona's song!"
    	# client.publish("songID", "7") #7=Epona
    	_stream.stop_stream()
        play_song(songs[0])
        play_song(songs[1])
    	change_color_all([yellow])
    	notes.append('G')
        _stream.start_stream()
    if notes==zelda:
        print "\t\t\t\tZelda's Lullaby!"
        # client.publish("songID", "8") #8=Zelda
    	_stream.stop_stream()
        play_song(songs[0])
        play_song(songs[9])
    	change_color_all()
        notes.append('G')
        _stream.start_stream()
    if notes==heal:
    	print "Song of Healing!"
        play_song(songs[0])
    	_stream.stop_stream()
    	# client.publish("songID", "6")
    	# client.publish("songID", "1")
    	# client.publish("songID", "3")
    	sleep(10)
    	# client.publish("songID", "8")
    	notes.append('G')
    	_stream.start_stream()
    if notes==test:
        print "Test Sequence Activated!"
        confirm.play()
        notes.append('G')
