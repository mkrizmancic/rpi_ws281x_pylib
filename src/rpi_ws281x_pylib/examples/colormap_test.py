import time

import numpy as np
from matplotlib import cm

from rpi_ws281x_pylib import LEDClient

colors = [(0.204, 0.0, 0.0), (0.203, 0.012, 0.0), (0.2, 0.024, 0.0), (0.194, 0.036, 0.0), (0.188, 0.046, 0.0), (0.18, 0.056, 0.0), (0.172, 0.064, 0.0), (0.164, 0.071, 0.0), (0.155, 0.078, 0.0), (0.148, 0.083, 0.0), (0.14, 0.088, 0.0), (0.133, 0.091, 0.0), (0.127, 0.094, 0.0), (0.12, 0.097, 0.0), (0.114, 0.1, 0.0), (0.108, 0.102, 0.0), (0.104, 0.104, 0.0), (0.103, 0.103, 0.024), (0.103, 0.103, 0.052), (0.102, 0.102, 0.076), (0.099, 0.1, 0.1), (0.09, 0.103, 0.103), (0.08, 0.106, 0.106), (0.067, 0.108, 0.108), (0.055, 0.11, 0.11), (0.041, 0.112, 0.112), (0.028, 0.114, 0.114), (0.015, 0.114, 0.114), (0.0, 0.115, 0.115), (0.0, 0.114, 0.124), (0.0, 0.112, 0.137), (0.0, 0.111, 0.149), (0.0, 0.109, 0.163), (0.0, 0.106, 0.184), (0.0, 0.102, 0.205), (0.0, 0.095, 0.235), (0.0, 0.087, 0.266), (0.0, 0.075, 0.301), (0.0, 0.054, 0.343), (0.0, 0.029, 0.372), (0.0, 0.0, 0.383)]


def interp(x, in_min, in_max, out_min, out_max):
    x = max(min(x, in_max), in_min)
    return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def main():

    leds = LEDClient()
    leds.connect()
    leds.set_all((0, 0, 0))

    # cmap = cm.get_cmap('RdYlGn')

    # i = 0
    # while True:
    #     for i in np.linspace(0, 1, 40):
    #         color = [int(x * 255) for x in cmap(i)[0:4]]
    #         print(color)
    #         leds.set_all((color[0], color[1], color[2]), color_space='rgb')
    #         time.sleep(0.5)

    # while True:
    #     for c in colors:
    #         color = [int(x * 255) for x in c]
    #         leds.set_all(color)
    #         time.sleep(0.1)

    while True:
        user_input = float(input("Enter error [-3, 3] > "))
        idx = interp(user_input, -3, 3, 0, len(colors) - 1)
        color = [int(x * 255) for x in colors[idx]]
        leds.set_all(color)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("LED Client exited.")