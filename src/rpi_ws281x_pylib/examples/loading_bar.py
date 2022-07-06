import time

import numpy as np
from matplotlib import cm

from rpi_ws281x_pylib import LEDClient


def main():

    leds = LEDClient()
    leds.connect()
    leds.set_all((0, 0, 0))
    base_color = (0, 20, 0)

    while True:
        for i in np.linspace(0, 1, 100):
            leds.set_percentage(i, 160, base_color, mode='center')
            time.sleep(0.1)

    # while True:
    #     user_input = int(input("Enter % > "))
    #     leds.set_percentage(user_input / 100, 80, base_color, mode='center')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("LED Client exited.")