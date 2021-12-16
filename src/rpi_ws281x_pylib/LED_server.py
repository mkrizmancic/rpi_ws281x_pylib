#!/usr/bin/env python3
import sys
import signal
import time
import zmq
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_HEIGHT = 4        # Number of LED pixel rows.
LED_WIDTH = 8         # Number of LED pixel columns.
LED_COUNT = LED_HEIGHT * LED_WIDTH
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

class LEDServer(object):
    def __init__(self):
        self.config = {
            'count': LED_COUNT,
            'width': LED_WIDTH,
            'height': LED_HEIGHT,
        }

        # Create NeoPixel object with appropriate configuration.
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

        signal.signal(signal.SIGINT, self.exit)

        self.init_animation()
        print("LED strip is ready to receive commands.")

    def init_animation(self):
        for color in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (0, 0, 0)]:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(*color))
                self.strip.show()
                time.sleep(0.01)

    def run(self):
        context = zmq.Context()
        with context.socket(zmq.REP) as socket:
            socket.bind("tcp://*:5555")
            while True:
                msg = socket.recv_json()
                print(f"Client connected: {msg}")
                socket.send_json(self.config)

                while True:
                    data = socket.recv_json()
                    if data:
                        if data == 'Disconnect':
                            print("Client disconnected.")
                            socket.send_json(True)
                            break
                        else:
                            ret = self.set_pixels(data)
                            socket.send_json(ret)
                    else:
                        print("NO DATA")

    def exit(self, signum, frame):
        print("Turning off LEDs and exiting.")
        for i in range(LED_COUNT):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
        sys.exit(0)

    def set_pixels(self, pixels):
        for i, color in enumerate(pixels):
            self.strip.setPixelColor(i, Color(*color))
        self.strip.show()
        return True


if __name__ == '__main__':
    ls = LEDServer()
    ls.run()

