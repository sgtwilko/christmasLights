#!/usr/bin/python
### BEGIN INIT INFO
# Provides:          christmas.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from neopixel import *

import argparse
import signal
import sys
#from signal import signal, SIGINT, SIGTERM

def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0), wait_ms=10)
        sys.exit(0)

def opt_parse():
        #parser = argparse.ArgumentParser()
        #parser.add_argument('-c', action='store_true', help='clear the display on exit')
        #args = parser.parse_args()
        #if args.c:
        signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_COUNT      = 307      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
LED_STAR_COUNT  = 7
LED_ON = 16
LED_FACTOR = LED_ON/float(LED_BRIGHTNESS)
START_TIME = time.time()

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)
		#starTwinkle(strip)

def theaterChase(strip, color, wait_ms=50, iterations=60):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(6):
			for i in range(0, strip.numPixels()-LED_STAR_COUNT, 6):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			starTwinkle(strip)
			for i in range(0, strip.numPixels()-LED_STAR_COUNT, 6):
				strip.setPixelColor(i+q, 0)

def theaterChaseAll(strip, wait_ms=50, iterations=60):
	"""Movie theater light style chaser animation."""
	colors = [Color(LED_ON,LED_ON,LED_ON), Color(LED_ON,0,0), Color(0, 0, LED_ON)]
	for j in range(iterations):
		for q in range(6):
			for i in range(0, strip.numPixels()-LED_STAR_COUNT, 6):
				strip.setPixelColor(i+q, colors[((i/6)-j) % 3])
			strip.show()
			time.sleep(wait_ms/1000.0)
			starTwinkle(strip)
			for i in range(0, strip.numPixels()-LED_STAR_COUNT, 6):
				strip.setPixelColor(i+q, 0)

def theaterChaseAllDuf(strip, wait_ms=50, iterations=60):
	"""Movie theater light style chaser animation."""
#	colors = [Color(127,127,127), Color(127,0,0), Color(0, 0, 127)]
	colors = [Color(LED_ON,LED_ON,LED_ON), Color(LED_ON,0,0), Color(0, 0, LED_ON)]
	for j in range(iterations):
		for q in range(6):
			for i in range(0, strip.numPixels()-LED_STAR_COUNT, 6):
				strip.setPixelColor(i+q, colors[((j+q)/6) % 3])
			strip.show()
			time.sleep(wait_ms/1000.0)
			starTwinkle(strip)
			for i in range(0, strip.numPixels()-LED_STAR_COUNT, 6):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(int((pos * 3) * LED_FACTOR), int((255 - pos * 3) * LED_FACTOR), 0)
	elif pos < 170:
		pos -= 85
		return Color(int((255 - pos * 3)*LED_FACTOR), 0, int((pos * 3)*LED_FACTOR))
	else:
		pos -= 170
		return Color(0, int((pos * 3)*LED_FACTOR), int((255 - pos * 3)*LED_FACTOR))

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(0, strip.numPixels()-LED_STAR_COUNT,3):
			strip.setPixelColor(i+(3-(j/3%3)), wheel((i+j) & 255))
			strip.setPixelColor(i+1+(3-(j/3%3)), 0)
			strip.setPixelColor(i+2+(3-(j/3%3)), 0)
		strip.show()
		time.sleep(wait_ms/1000.0)
		starTwinkle(strip)


def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(0, strip.numPixels()-LED_STAR_COUNT,3):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
			strip.setPixelColor(i+1, 0)
			strip.setPixelColor(i+2, 0)
		strip.show()
		time.sleep(wait_ms/1000.0)
		starTwinkle(strip)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels()-LED_STAR_COUNT, 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			starTwinkle(strip)
			for i in range(0, strip.numPixels()-LED_STAR_COUNT, 3):
				strip.setPixelColor(i+q, 0)

def starTwinkle(strip):
	x=(int(((time.time()-START_TIME)*1000)/100) % 7)+(LED_COUNT-LED_STAR_COUNT)
	for i in range(LED_COUNT-LED_STAR_COUNT, LED_COUNT):
		if i==x:
			strip.setPixelColor(i, Color(255,255,255))
		elif abs(i-x)==1: 
			strip.setPixelColor(i, Color(16,16,16))
		else:
			strip.setPixelColor(i, Color(0,0,0))
	strip.show()


# Main program logic follows:
if __name__ == '__main__':
        # Process arguments
        opt_parse()

	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	starTwinkle(strip)

	print ('Press Ctrl-C to quit.')
	while True:
		#print ('Color wipe animations.')
		#colorWipe(strip, Color(255, 0, 0))  # Red wipe
		#colorWipe(strip, Color(0, 255, 0))  # Blue wipe
		#colorWipe(strip, Color(0, 0, 255))  # Green wipe
		print ('Theater chase animations. All')
		theaterChaseAll(strip)  # White theater chase
		print('rainbow')
		rainbow(strip)
		print('theaterChase red')
		theaterChase(strip, Color(LED_ON,   0,   0))  # Red theater chase
		print('rainbow cycle')
		rainbowCycle(strip)
		print('theaterchase blue')
		theaterChase(strip, Color(  0,   0, LED_ON))  # Blue theater chase
		#print('theater chase rainbow')
		#theaterChaseRainbow(strip)
		print('rainbow')
		rainbow(strip)
		print('theaer chase white')
		theaterChase(strip, Color(LED_ON, LED_ON, LED_ON))  # White theater chase

