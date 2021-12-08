#!/usr/bin/env python3
import random
import zmq
import time
import colorsys
import numpy as np


# VERY BIG TODO: Check user inputs and prevent errors


class LEDClient(object):
    def __init__(self):
        self.is_connected = False
        self.led_conf = None
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)

    def connect(self):
        self.socket.connect("tcp://localhost:5555")
        self.is_connected = True
        self.socket.send_json("Hello!")
        self.led_conf = self.socket.recv_json()
        print('Connection successful, server config: ', self.led_conf)

    # def reconnect(self):
    #     if not self.is_connected:
    #         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.connect()

    def exit(self):
        print("Exiting.")
        self.socket.send_json("Disconnect")
        self.is_connected = False
        self.socket.close()

    def set_all(self, color, color_space='rgb'):
        if color_space == 'hsv':
            color = LEDClient.hsv2rgb(*color)
        pixels = [color] * self.led_conf['count']
        self.socket.send_json(pixels)
        return self.socket.recv_json()

    def set_square(self, color, size, top_left, color_space='rgb'):
        if color_space == 'hsv':
            color = LEDClient.hsv2rgb(*color)

        if not (top_left[0] >= 0 and top_left[1] >= 0
                and top_left[0] + size <= self.led_conf['height']
                and top_left[1] + size <= self.led_conf['width']):
            print("WARNING: Can't set the desired square.")

        pixels = [0] * self.led_conf['count']
        for i in range(self.led_conf['height']):
            for j in range(self.led_conf['width']):
                if (i >= top_left[0] and i < top_left[0] + size
                        and j >= top_left[1] and j < top_left[1] + size):
                    pixels[i * self.led_conf['width'] + j] = color
                else:
                    pixels[i * self.led_conf['width'] + j] = (0, 0, 0)
        self.socket.send_json(pixels)
        return self.socket.recv_json()

    def set_individual(self, array, color_space='rgb'):
        if len(array) == self.led_conf['height']:
            pixels = [val for subarray in array for val in subarray]
        else:
            pixels = array

        if color_space == 'hsv':
            pixels = [LEDClient.hsv2rgb(*val) for val in pixels]
        self.socket.send_json(pixels)
        return self.socket.recv_json()

    def set_rainbow(self, brightness, start=0):
        pixels = [LEDClient.hsv2rgb(h, 1, brightness / 255)
                  for h in np.roll(np.linspace(0, 1, self.led_conf['count']), start)]
        self.socket.send_json(pixels)
        return self.socket.recv_json()

    def set_random(self, brightness):
        pixels = [LEDClient.hsv2rgb(random.random(), 1, brightness / 255) for i in range(self.led_conf['count'])]
        self.socket.send_json(pixels)
        return self.socket.recv_json()

    @staticmethod
    def hsv2rgb(h, s, v):
        return tuple(int(round(i * 255)) for i in colorsys.hsv_to_rgb(h, s, v))


if __name__ == '__main__':
    lc = LEDClient()
    lc.connect()

    for i in range(4 * 32):
        lc.set_rainbow(15, i)
        time.sleep(0.1)

    lc.exit()
