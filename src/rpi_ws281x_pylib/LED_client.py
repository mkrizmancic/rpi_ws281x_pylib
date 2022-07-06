#!/usr/bin/env python3
import random
import zmq
import time
import colorsys
import numpy as np
import math


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
        pixels = [LEDClient.hsv2rgb(h, 255, brightness)
                  for h in np.roll(np.linspace(0, 255, self.led_conf['count']), start)]
        self.socket.send_json(pixels)
        return self.socket.recv_json()

    def set_random(self, brightness):
        pixels = [LEDClient.hsv2rgb(random.random() * 255, 25, brightness) for i in range(self.led_conf['count'])]
        self.socket.send_json(pixels)
        return self.socket.recv_json()

    def add_line(self, pixels, index, color, color_space='rgb'):
        if index < 0 or index >= self.led_conf['width']:
            print("ERROR: Index out of range.")
            return

        if color_space == 'hsv':
            color = LEDClient.hsv2rgb(*color)

        for i in range(self.led_conf['height']):
            pixels[i * self.led_conf['width'] + index] = color

        return pixels

    def set_line(self, index, color, color_space='rgb'):
        pixels = [(0, 0, 0)] * self.led_conf['count']
        pixels = self.add_line(pixels, index, color, color_space)

        self.socket.send_json(pixels)
        return self.socket.recv_json()

    def set_percentage(self, percent, resolution, base_color, mode, color_space='rgb'):
        if color_space == 'rgb':
            base_color = LEDClient.rgb2hsv(*base_color)      

        if mode == 'center':
            resolution = int(resolution / 2)

        levels = resolution // self.led_conf['width']

        if mode == 'l2r':
            max_val = levels * self.led_conf['width'] - 1
        elif mode == 'center':
            max_val = levels * (self.led_conf['width'] // 2) - 1

        pixels = [(0, 0, 0)] * self.led_conf['count']

        x = LEDClient.interp(percent, 0, 1, 0, max_val)

        for i in range(x // levels + 1):
            if i < x // levels:
                color = base_color
            else:
                step = (x % levels + 1) / levels
                color = (base_color[0], int(round(base_color[1] * step)), base_color[2])

            if mode == 'l2r':
                pixels = self.add_line(pixels, i, color, color_space='hsv')
            elif mode == 'center':
                pixels = self.add_line(pixels, i + self.led_conf['width'] // 2, color, color_space='hsv')
                pixels = self.add_line(pixels, -i + self.led_conf['width'] // 2 - 1, color, color_space='hsv')

        self.socket.send_json(pixels)
        return self.socket.recv_json()
        

    @staticmethod
    def hsv2rgb(h, s, v):
        return tuple(int(round(i * 255)) for i in colorsys.hsv_to_rgb(h / 255, s / 255, v / 255))

    @staticmethod
    def rgb2hsv(r, g, b):
        return tuple(int(round(i * 255)) for i in colorsys.rgb_to_hsv(r / 255, g / 255, b / 255))

    @staticmethod
    def interp(x, in_min, in_max, out_min, out_max):
        x = max(min(x, in_max), in_min)
        return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


if __name__ == '__main__':
    lc = LEDClient()
    lc.connect()

    for i in range(4 * 32):
        lc.set_rainbow(15, i)
        time.sleep(0.1)

    lc.exit()
